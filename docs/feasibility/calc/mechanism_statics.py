"""Planar statics for the three candidate corner mechanisms (Part 3).

Conventions: per-corner static wheel load W from the gross mass. Dynamic
factors from params.py. All results are DERIVED from ASSUMPTIONS.

Option A  Actuated four-bar wheel-leg: the actuator drives the lower link
          angle and is IN the load path at all times (no separate spring
          reference). Torque at the hip = W * horizontal reach.
Option B  Double wishbone on a rotating corner sub-frame ("drum"): road loads
          go through the wishbones into the drum, and through the LOCK into
          the chassis. The actuator sees load only while rotating the drum.
Option C  Trailing/leading arm with an actuated carrier: the spring/damper
          reacts between arm and carrier; the carrier is positioned by the
          actuator and held by a lock/non-backdrivable drive.
"""
import math
from params import *
from mass_budget import road_curb_mass

def corner_static_load():
    m_gross = road_curb_mass() + PAYLOAD_KG
    return m_gross * G / 4.0, m_gross

def optA(W):
    reach = ARM_LENGTH_M * math.cos(math.radians(ARM_ANGLE_ROAD_DEG))
    torque_static = W * reach
    return {
        "hip torque static (Nm)": torque_static,
        "hip torque 3g bump (Nm)": torque_static * LOAD_FACTOR_BUMP,
        "hip torque 5g landing (Nm)": torque_static * LOAD_FACTOR_LANDING,
        "actuators per corner": 2,   # hip + knee to get useful clearance range
        "actuator in dynamic load path": True,
    }

def optB(W):
    # Drum axis longitudinal; wheel centre offset from drum axis ~ half track
    r = TRACK_M / 2.0 - 0.10   # ASSUMPTION drum axis 100 mm inboard of body side
    torque_static = W * r
    return {
        "drum torque static (Nm)": torque_static,
        "drum torque to rotate while loaded (Nm)": torque_static * 1.3,  # + friction ASSUMPTION
        "lock load at 3g bump (Nm)": torque_static * LOAD_FACTOR_BUMP,
        "actuators per corner": 1,
        "actuator in dynamic load path": False,
        "camber change per deg of drum rotation (deg)": 1.0,
    }

def optC(W):
    reach_road = ARM_LENGTH_M * math.cos(math.radians(ARM_ANGLE_ROAD_DEG))
    reach_high = ARM_LENGTH_M * math.cos(math.radians(ARM_ANGLE_HIGH_DEG))
    t_static = W * reach_road
    # Linear actuator on a lever; worst case is lifting the loaded corner
    F_act_lift = t_static * 1.3 / ACTUATOR_LEVER_M   # + friction ASSUMPTION
    # Spring force at road ride height through motion ratio
    F_spring = W / SPRING_MOTION_RATIO
    return {
        "carrier torque static, road angle (Nm)": t_static,
        "carrier torque static, high angle (Nm)": W * reach_high,
        "lock/worm load at 3g bump (Nm)": t_static * LOAD_FACTOR_BUMP,
        "lock/worm load at 5g landing (Nm)": t_static * LOAD_FACTOR_LANDING,
        "linear actuator force to lift loaded corner (kN)": F_act_lift / 1000.0,
        "linear actuator force to swing unloaded wheel (kN)": (0.20 * t_static) / ACTUATOR_LEVER_M / 1000.0,  # ASSUMPTION 20% (arm+wheel self-weight)
        "spring force at ride height (kN)": F_spring / 1000.0,
        "actuators per corner": 1,
        "actuator in dynamic load path": False,
        "wheel longitudinal shift road->high (m)": reach_road - reach_high,
        "ride height gain road->high (m)": ARM_LENGTH_M * (math.sin(math.radians(ARM_ANGLE_HIGH_DEG)) - math.sin(math.radians(ARM_ANGLE_ROAD_DEG))),
    }

def grubler_planar(n_links, n_full_joints, n_half_joints=0):
    """Kutzbach-Gruebler mobility for planar mechanisms: M = 3(n-1) - 2j1 - j2."""
    return 3 * (n_links - 1) - 2 * n_full_joints - n_half_joints

if __name__ == "__main__":
    W, m = corner_static_load()
    print(f"Gross mass {m:.0f} kg -> static corner load W = {W:.0f} N")
    print()
    print("Mobility (Kutzbach-Gruebler, planar, per corner, transformation joints only):")
    print("  Option A four-bar with 2 actuated joints: M =", grubler_planar(4, 4), "+1 actuated => 2 DOF (both must be driven or locked)")
    print("  Option B wishbone four-bar (M=1 suspension) on drum (+1) =>", grubler_planar(4, 4), "+ 1 = 2 DOF; 1 spring-controlled, 1 actuator/lock-controlled")
    print("  Option C arm (M=1 suspension) + carrier (+1) => 2 DOF; 1 spring-controlled, 1 actuator/lock-controlled")
    print()
    for name, fn in (("OPTION A", optA), ("OPTION B", optB), ("OPTION C", optC)):
        print(name)
        for k, v in fn(W).items():
            if isinstance(v, float):
                print(f"  {k:55s} {v:10.2f}")
            else:
                print(f"  {k:55s} {v}")
        print()
