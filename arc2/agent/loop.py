"""The deliberative agent.

This is a SCRIPTED-REASONING agent, not a learned one, and that is
deliberate: Milestone 1 asks whether the ARCHITECTURE supports the cycle

    observe -> understand -> plan -> act -> observe result
            -> detect failure -> update model -> replan

A learned policy would make it impossible to tell whether the cycle worked or
whether the policy had memorised the arena. Every decision here is traceable
to a belief and a recorded outcome. Swapping this class for an LLM- or
RL-driven policy changes nothing below it -- it holds a RobotAPI and a
WorldModel, exactly as a learned agent would.

Failure is detected in three independent ways, and they are not the same:

  1. REPORTED   -- the ActionResult says BLOCKED/REFUSED/FAILED.
  2. MEASURED   -- the result claims progress but the pose barely moved.
  3. INFERRED   -- newly-perceived blockages intersect the remaining route,
                   so the plan is dead before we drive into it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from arc2.control.api import ActionResult, RobotAPI
from arc2.memory.episodic import EpisodicMemory
from arc2.perception.pipeline import integrate
from arc2.planning.action_planner import (ARRIVAL_TOLERANCE_M, Plan,
                                          next_steps, plan_route)
from arc2.planning.path import choose_frontier
from arc2.planning.task_planner import Decision, Phase, Strategy, TaskPlanner
from arc2.telemetry.episode_log import EpisodeLog
from arc2.types import ActionStatus, MobilityMode, Pose, Vec2
from arc2.world.model import Knowledge, WorldModel

#: A move that claims success but shifts the pose less than this is treated
#: as no progress regardless of what it reported.
MEASURED_PROGRESS_EPS = 0.05
#: How far ahead of the chassis to mark a proven blockage.
BLOCKAGE_STANDOFF_M = 0.55
PUSH_LEG_M = 0.8
GRASP_RANGE_M = 0.80


@dataclass
class AgentConfig:
    arena_w: float = 24.0
    arena_h: float = 16.0
    resolution: float = 0.25
    # Measured, not guessed: across seeds the baseline agent completes the
    # task in 458-1294 actions (it explores most of the arena before the
    # target happens to enter the camera's field of view). 900 -- the value
    # first picked arbitrarily -- cut off three of seven seeds AFTER they had
    # already acquired the payload. 1500 sits above the observed maximum
    # with margin; it is a budget, not a target.
    max_actions: int = 1500
    target_label: str = "canister"
    home_tolerance_m: float = 1.0
    scan_every: int = 4          # full 360 look-around cadence, in actions


class DeliberativeAgent:
    #: Failures against one goal before it is abandoned.
    GOAL_FAILURE_LIMIT = 4
    #: Consecutive blocked moves from the same spot before the agent stops
    #: re-planning and physically backs itself out.
    WEDGE_LIMIT = 3
    #: Turn applied when unwedging. Large enough to face away from whatever is
    #: in front; sign alternates so a symmetric trap does not loop.
    ESCAPE_TURN_RAD = 2.35
    ESCAPE_MOVE_M = 0.55

    def __init__(self, api: RobotAPI, log: EpisodeLog,
                 config: AgentConfig | None = None) -> None:
        self.api = api
        self.log = log
        self.cfg = config or AgentConfig()
        self.model = WorldModel(self.cfg.arena_w, self.cfg.arena_h,
                                self.cfg.resolution)
        self.memory = EpisodicMemory()
        self.task = TaskPlanner(self.cfg.target_label, self.cfg.home_tolerance_m)
        self.plan: Plan | None = None
        self.replans = 0
        self.actions_taken = 0
        self.mode = MobilityMode.WHEEL
        self._tried_modes: set[str] = set()
        self._last_decision: Decision | None = None
        self._stuck_counter = 0
        #: Frontier goals already reached or proven unreachable. A frontier is
        #: a hypothesis about where information is; once tested it must not be
        #: proposed again or the agent oscillates in place.
        self._exhausted: set[tuple[int, int]] = set()
        #: Failures accumulated while pursuing each goal. A goal that cannot
        #: be reached must be written off even if the route to it replans
        #: cleanly every time.
        self._goal_failures: dict[tuple[int, int], int] = {}
        self._wedge_count = 0
        self._escape_sign = 1.0

    # ------------------------------------------------------------------ run
    def run(self) -> dict:
        obs = self.api.observe()
        report = integrate(self.model, obs)
        self._log_observation(obs, report)

        while self.actions_taken < self.cfg.max_actions:
            pos = Vec2(self.model.pose_estimate.x, self.model.pose_estimate.y)
            decision = self.task.decide(self.model, self.memory, pos,
                                        self.api.get_robot_state()["carrying"])
            if decision != self._last_decision:
                self.log.emit("decision", obs.tick, obs.sim_time_s,
                              **decision.as_dict())
                self._last_decision = decision

            if decision.phase is Phase.DONE:
                break

            acted = self._pursue(decision, obs)
            if not acted:
                self.log.emit("note", obs.tick, obs.sim_time_s,
                              message="no action available; terminating",
                              phase=decision.phase.value)
                break

            obs = self.api.observe()
            report = integrate(self.model, obs)
            self._log_observation(obs, report)

            if self.plan is not None:
                why = self.plan.invalidated_by(self.model)
                if why is not None:
                    self._replan(f"inferred:{why}", obs)

        return self._finish()

    # ------------------------------------------------------------- pursuing
    def _pursue(self, d: Decision, obs) -> bool:
        """Execute ONE primitive toward the current decision. True if acted."""
        if d.strategy is Strategy.CHANGE_MOBILITY:
            return self._do_mode_change(obs)

        if d.phase is Phase.ACQUIRE:
            return self._do_grasp(d, obs)

        if d.phase is Phase.DELIVER:
            return self._do_place(d, obs)

        if d.strategy is Strategy.CLEAR_OBSTRUCTION:
            return self._do_push(obs)

        # A plan is kept until it COMPLETES or is FALSIFIED. Re-deriving a
        # goal every iteration turns nearest-frontier jitter into an infinite
        # replan loop -- measured: 445 replans for 5.6 m travelled.
        exploring = d.strategy is Strategy.EXPLORE_FRONTIER or d.goal is None
        if self.plan is None or self.plan.done:
            goal = self._pick_frontier_goal(obs) if exploring else d.goal
            if goal is None:
                return False
            self._replan(f"new_goal:{d.strategy.value}", obs, goal, d.rationale)
            if self.plan is None:
                if exploring:
                    self._exhausted.add(self._goal_key(goal))
                return False
        elif not exploring and d.goal is not None and \
                self.plan.goal.distance_to(d.goal) > 1.5:
            # The task itself moved the goalposts (e.g. the target was seen).
            self._replan("goal_changed", obs, d.goal, d.rationale)
            if self.plan is None:
                return False

        return self._follow_plan(obs)

    def _pick_frontier_goal(self, obs) -> Vec2 | None:
        bel = self.model.occupancy
        here = bel.to_cell(self.model.pose_estimate.x, self.model.pose_estimate.y)

        def penalty(wx: float, wy: float) -> float:
            p = Vec2(wx, wy)
            score = 0.0
            if self.memory.is_abandoned(p):
                # Graded, not absolute. An absolute exclusion here cost two
                # seeds their route home.
                score += 60.0
            if self._goal_key(p) in self._exhausted:
                score += 1000.0
            return score

        cell = choose_frontier(bel, here, penalise=penalty)
        if cell is None:
            return None
        goal = Vec2(*bel.to_world(*cell))
        if self._goal_key(goal) in self._exhausted:
            return None
        return goal

    @staticmethod
    def _goal_key(p: Vec2) -> tuple[int, int]:
        return (int(p.x // 0.75), int(p.y // 0.75))

    def _follow_plan(self, obs) -> bool:
        pose = self.model.pose_estimate
        wp = self.plan.current
        if wp is None:
            return False
        if Vec2(pose.x, pose.y).distance_to(wp) < ARRIVAL_TOLERANCE_M:
            self.plan.advance()
            if self.plan.done:
                self._exhausted.add(self._goal_key(self.plan.goal))
            return True                       # advancing the cursor is progress

        steps = next_steps(pose, wp)
        if not steps:
            self.plan.advance()
            if self.plan.done:
                self._exhausted.add(self._goal_key(self.plan.goal))
            return True

        step = steps[0]
        if step.kind == "turn":
            self._execute("turn", lambda: self.api.turn(step.value),
                          {"delta_rad": round(step.value, 4)}, obs)
            return True

        result = self._execute("move", lambda: self.api.move(step.value),
                               {"distance_m": round(step.value, 4)}, obs)
        self._assess(result, obs)
        return True

    # ------------------------------------------------------------- actions
    def _do_mode_change(self, obs) -> bool:
        target = (MobilityMode.LEG if self.mode is MobilityMode.WHEEL
                  else MobilityMode.WHEEL)
        if target.value in self._tried_modes:
            # Both modes tried and still stuck -- this is not a mode problem.
            self.task.strategy = Strategy.ALTERNATE_ROUTE
            self.log.emit("note", obs.tick, obs.sim_time_s,
                          message="both mobility modes tried; reverting to reroute")
            return True
        self._tried_modes.add(target.value)
        r = self._execute("change_mobility_mode",
                          lambda: self.api.change_mobility_mode(target),
                          {"mode": target.value}, obs)
        if r.progressed:
            self.mode = target
            self.task.on_progress()
            self.task.strategy = Strategy.DIRECT_ROUTE
            self.log.emit("task_progress", obs.tick, obs.sim_time_s,
                          event="mobility_mode_changed", mode=target.value)
        return True

    def _do_push(self, obs) -> bool:
        r = self._execute("push", lambda: self.api.push(PUSH_LEG_M),
                          {"distance_m": PUSH_LEG_M}, obs)
        if r.progressed and r.detail.get("displaced"):
            self.task.on_progress()
            self.log.emit("task_progress", obs.tick, obs.sim_time_s,
                          event="obstruction_displaced",
                          objects=r.detail["displaced"])
            self.task.strategy = Strategy.DIRECT_ROUTE
            self.plan = None
        else:
            self._assess(r, obs)
        return True

    def _do_grasp(self, d: Decision, obs) -> bool:
        tid = d.target_id
        if tid is None:
            return False
        belief = self.model.objects.get(tid)
        pos = Vec2(self.model.pose_estimate.x, self.model.pose_estimate.y)
        if belief is not None and pos.distance_to(belief.position) > GRASP_RANGE_M:
            self._replan("approach_for_grasp", obs, belief.position, "approach")
            return self._follow_plan(obs) if self.plan else False
        r = self._execute("interact", lambda: self.api.interact("pick_up", tid),
                          {"verb": "pick_up", "target_id": tid}, obs)
        if r.ok:
            self.task.on_progress()
            self.plan = None
            self.log.emit("task_progress", obs.tick, obs.sim_time_s,
                          event="payload_acquired", target_id=tid)
        else:
            self._assess(r, obs)
            # Out of reach means our belief about WHERE it is was wrong.
            if r.reason == "out_of_reach" and belief is not None:
                self._nudge_toward(belief.position, obs)
        return True

    def _do_place(self, d: Decision, obs) -> bool:
        carrying = self.api.get_robot_state()["carrying"]
        if not carrying:
            self.task.phase = Phase.DONE
            return True
        r = self._execute("interact",
                          lambda: self.api.interact("place", carrying[0]),
                          {"verb": "place", "target_id": carrying[0]}, obs)
        if r.ok:
            self.task.phase = Phase.DONE
            self.log.emit("task_progress", obs.tick, obs.sim_time_s,
                          event="payload_delivered", target_id=carrying[0])
        return True

    def _nudge_toward(self, goal: Vec2, obs) -> None:
        pose = self.model.pose_estimate
        steps = next_steps(pose, goal)
        if steps:
            s = steps[0]
            if s.kind == "turn":
                self._execute("turn", lambda: self.api.turn(s.value),
                              {"delta_rad": round(s.value, 4)}, obs)
            else:
                self._execute("move", lambda: self.api.move(min(0.4, s.value)),
                              {"distance_m": round(min(0.4, s.value), 3)}, obs)

    # ------------------------------------------------ execution + assessment
    def _execute(self, name: str, call, params: dict, obs) -> ActionResult:
        pose_before = self.model.pose_estimate
        cells_before = self.model.occupancy.known_cells()
        self.log.emit("action", obs.tick, obs.sim_time_s, action=name,
                      params=params, pose_estimate=pose_before.as_dict())
        result = call()
        self.actions_taken += 1
        cells_after = self.model.occupancy.known_cells()
        self.memory.record(obs.tick, result, pose_before, params,
                           info_gain=cells_after - cells_before)
        self.log.emit("action_result", obs.tick, obs.sim_time_s,
                      **result.as_dict())
        return result

    def _assess(self, result: ActionResult, obs) -> None:
        """Decide whether that outcome counts as a failure, and adapt."""
        pos = Vec2(self.model.pose_estimate.x, self.model.pose_estimate.y)

        reported = result.status in (ActionStatus.BLOCKED, ActionStatus.REFUSED,
                                     ActionStatus.FAILED, ActionStatus.INVALID)
        measured_stall = (result.action in ("move", "push")
                          and result.achieved < MEASURED_PROGRESS_EPS)

        if not (reported or measured_stall):
            self.task.on_progress()
            self._stuck_counter = 0
            self._wedge_count = 0
            self.model.record_success(result.action, pos, obs.tick)
            return

        if result.action in ("move", "push"):
            self._wedge_count += 1

        self._stuck_counter += 1
        self.model.record_failure(result.reason or result.status.value, pos,
                                  self.model.pose_estimate.heading, obs.tick,
                                  result.contact_id or "")
        # Write the blockage we just PROVED into the belief. This is stronger
        # evidence than a range return, so it overrides.
        if result.action in ("move", "push"):
            self.model.mark_blocked_ahead(pos, self.model.pose_estimate.heading,
                                          BLOCKAGE_STANDOFF_M)
            self.log.emit("world_update", obs.tick, obs.sim_time_s,
                          source="action_failure", kind=result.reason,
                          marked_blocked_ahead_m=BLOCKAGE_STANDOFF_M)

        self.log.emit("failure", obs.tick, obs.sim_time_s,
                      action=result.action, status=result.status.value,
                      reason=result.reason, contact_id=result.contact_id,
                      consecutive=self.task.consecutive_failures + 1,
                      detection=("reported" if reported else "measured_stall"))

        if self.plan is not None:
            key = self._goal_key(self.plan.goal)
            self._goal_failures[key] = self._goal_failures.get(key, 0) + 1
            if self._goal_failures[key] >= self.GOAL_FAILURE_LIMIT:
                self._exhausted.add(key)
                self.plan = None
                self.log.emit("note", obs.tick, obs.sim_time_s,
                              message="goal written off after repeated failure",
                              goal=[round(self.plan.goal.x, 3),
                                    round(self.plan.goal.y, 3)]
                              if self.plan else None,
                              failures=self._goal_failures[key])

        rationale = self.task.on_failure(result.reason, result.contact_id,
                                         self.model, self.memory, pos)

        if self._wedge_count >= self.WEDGE_LIMIT:
            self._unwedge(obs)
            return

        self._replan(f"failure:{result.reason}", obs, rationale=rationale)

    def _unwedge(self, obs) -> None:
        """Physically back out of a spot that re-planning cannot escape.

        Replanning from a wedged pose produces a valid-looking route whose
        first move is straight back into the obstruction. The only real fix is
        to change the pose, so: turn away, drive a short way, discard the plan.
        """
        self.log.emit("note", obs.tick, obs.sim_time_s,
                      message="wedged; executing escape manoeuvre",
                      consecutive_blocked=self._wedge_count)
        # NOTE: writing the pursued goal off here was tried and MEASURED AS A
        # REGRESSION (4/7 -> 3/7 seeds). Being wedged says the approach was
        # wrong, not that the destination is unreachable, and excluding it
        # cost one seed a route it needed. The escape itself is enough.
        turn = self.ESCAPE_TURN_RAD * self._escape_sign
        self._escape_sign *= -1.0
        self._execute("turn", lambda: self.api.turn(turn),
                      {"delta_rad": round(turn, 4), "purpose": "escape"}, obs)
        self._execute("move", lambda: self.api.move(self.ESCAPE_MOVE_M),
                      {"distance_m": self.ESCAPE_MOVE_M, "purpose": "escape"}, obs)
        self._wedge_count = 0
        self.plan = None

    def _replan(self, cause: str, obs, goal: Vec2 | None = None,
                purpose: str = "", rationale: str = "") -> None:
        had_plan = self.plan is not None
        if goal is None:
            goal = self.plan.goal if self.plan else self._pick_frontier_goal(obs)
        if goal is None:
            self.plan = None
            return

        new_plan = plan_route(self.model, self.model.pose_estimate, goal,
                              purpose or self.task.strategy.value, obs.tick)
        if had_plan:
            self.replans += 1
            self.log.emit("replan", obs.tick, obs.sim_time_s, cause=cause,
                          rationale=rationale,
                          strategy=self.task.strategy.value,
                          found=new_plan is not None,
                          goal=[round(goal.x, 3), round(goal.y, 3)])
        self.plan = new_plan
        if new_plan is not None:
            self.log.emit("plan", obs.tick, obs.sim_time_s, **new_plan.as_dict())

    # --------------------------------------------------------------- output
    def _log_observation(self, obs, report) -> None:
        if self.log.full_observations:
            payload = obs.as_dict()
            payload.pop("tick", None)
            payload.pop("sim_time_s", None)
        else:
            payload = {"pose_estimate": obs.pose_estimate.as_dict(),
                       "lidar_min": round(min(obs.lidar.ranges), 3),
                       "n_detections": len(obs.rgb.detections)}
        self.log.emit("observation", obs.tick, obs.sim_time_s, **payload)
        self.log.emit("perception", obs.tick, obs.sim_time_s, **report.as_dict())

    def _finish(self) -> dict:
        return {
            "actions_taken": self.actions_taken,
            "replans": self.replans,
            "strategy_changes": self.task.strategy_changes,
            "final_phase": self.task.phase.value,
            "memory": self.memory.summary(),
            "world_model": self.model.summary(),
        }
