# 6 — Exact transformation mechanism, wheel storage, and frame-by-frame sequences

Every motion below is one of two rotations about one axis per corner:
- **Arm rotation** (suspension): the arm turns on its shaft inside the carrier. Passive, spring/damper.
- **Carrier rotation** (geometry): the carrier turns in the node's bearings, driven by the actuator, held by the pin.

The axis is the corner pivot axis: front at (X +0.161, Z 0.434), rear at (X −0.161, Z 0.434), parallel to Y, at Y from 0.265 to 0.415 m (bearing span). Nothing else moves. There are no bay doors, no deployable skis or tracks, no second linkage. Numbers from `calc/kinematics.py`.

## 6.1 What moves, about what, by how much

| Transition | Moving part | Axis | Angle | Wheel-centre motion (body frame) | What stays fixed | What carries the load at the end |
|---|---|---|---|---|---|---|
| ROAD → HIGH | carrier (+ arm, spring, wheel with it) | corner pivot axis | +26° (12° → 38°) | front: 0.095 m rearward, 0.204 m down; rear: 0.095 m forward, 0.204 m down | node, sill, tie-rod inner joint (on the axis), motor (on the carrier: rotates but its output/half-shaft geometry is unchanged) | pin in the 38° slot; loads: tyre → arm → spring/pivot → carrier → pin → node |
| HIGH → ROAD | carrier | same | −26° | reverse | same | pin in the 12° slot |
| ROAD → LIFT (one corner) | that carrier | same | +38° (12° → 50°) | wheel 0.168 m inward, 0.279 m down relative to the body; since the other three corners are pinned, the body rises at that corner until the arm reaches full rebound and the wheel unloads | other three corners (pinned) | pin at 50°; the lifted corner carries nothing (wheel off the ground) |
| ROAD → RETRACT (M variant only) | carrier | same | −62° (12° → −50°) | wheel 0.168 m inward, 0.487 m up; tyre bottom ends 0.487 m above the keel line | as above | pin at −50°; hydrodynamic and inertia loads only |

Hard stops: PU blocks on the node at −2° and +55° (base vehicle), −55° and +55° (variant). Arm rebound strap at +24° relative to the carrier; coil-over bump stop at −14°.

## 6.2 ROAD → ROBOTIC (HIGH), all four corners, step by step

| Step | Action | Sensor / state confirmation | Load path during the step |
|---|---|---|---|
| 1 | Vehicle slows to ≤ 5 km/h; rider selects HIGH and confirms within 5 s | wheel speeds ×4, IMU pitch/roll ≤ 10°, steering ±10°, no faults, 48 V ≥ 44 V, SOC ≥ 10% | normal driving path |
| 2 | Brake state: service brakes released; drive torque limited to 30% (creep allowed) | brake pressure sensors, inverter torque | |
| 3 | Suspension state read: all four arm angles within 12° ± 8° of the carrier (not on a bump stop) | arm sensors | |
| 4 | Actuator brakes release; actuators pre-load +0.3 kN toward the target to unload the pins | actuator current | pins still carry the driving load |
| 5 | Pin solenoids energise; pins retract 12 mm | 2 switches per pin: "retracted" within 300 ms; else abort (re-brake, de-energise) | load moves from pins to actuators + brakes (≤ 5 km/h, so ≤ 1.5 g) |
| 6 | Actuators extend 72 mm at 12 mm/s (6 s); the controller synchronises the four carrier angles within ±2°; the arms ride along at their spring-set angle; the wheels stay loaded; the body rises 0.204 m | carrier sensors ×2 per corner, actuator positions | tyre → arm → spring → carrier → actuator + brake → node |
| 7 | Target 38° ± 1° reached; arm angles still within their travel band (nothing jammed) | sensors | |
| 8 | Solenoids de-energise; pins drop into the 38° slot under spring force; if a pin does not seat, the actuator jogs ±2° once | 2 switches per pin: "engaged" | |
| 9 | Actuator brakes apply; actuator current → 0 | brake feedback | pins carry the load |
| 10 | Controller declares ROBOTIC: torque map "crawl", ESC "high", speed cap 25 km/h, amber light lines steady | — | tyre → arm → spring/pivot → carrier → pin → node |

Time: ~8 s including checks. Same sequence in reverse for HIGH → ROAD with the additional gate that four wheel-ID tags are present.

Per-corner adjustments in ROBOTIC (leveling, obstacle stepping) run steps 4–9 on one or two corners at a time at ≤ 5 km/h. The pins re-engage at the nearest 5° slot after each move; the vehicle never drives faster than 5 km/h with a pin out.

## 6.3 ROAD → SKI: what actually happens

There is no onboard ski or track storage (Section 6.5 shows why). The transformation is a **self-lifted swap**, and it is fully mechanical and sequenced:

**Front-left corner (repeat FR, then RL, RR)**
1. Vehicle stopped on ground within 5° of level; Park (rear parking brakes) engaged; HV drive disabled by the interlock; steering centred.
2. Rider selects "Swap FL". The controller runs the LIFT sequence on FL only: pins of the other three corners verified engaged; FL actuator drives its carrier 12° → 50° (104 mm stroke, up to 6.8 kN); as the carrier rotates, the FL wheel is pushed down against the ground; because the other three corners are pinned, the body rises at FL until the FL arm reaches full rebound (arm sensor at +24° relative to the carrier) — the wheel is now unloaded, 0.279 m of body rise at that corner (the body tilts about 12° in roll/pitch combined; the CG stays inside the three-wheel triangle, checked in `calc/kinematics.py` logic for the RC-0 CG and to be re-checked with the measured CG).
3. Pin engages at 50°; actuator brake on.
4. Rider removes the four lug nuts and the wheel (11 kg).
5. Rider fits the **ski adapter**: a hub-face plate that bolts to the same four studs with the same lug nuts; the plate carries the transverse ski pivot pin (Ø20), a rubber ski-pressure spring and a limiter strap. The ski saddle slides onto the pivot pin and is secured by one quick-release pin with a secondary circlip; the limiter strap closes a switch.
6. Kit ID (RFID in the adapter) is read: "SKI". Adapter seated switch closed. Strap switch closed.
7. Rider confirms; controller lowers FL: carrier 50° → 12°, pin engages at 12°. The ski is now on the ground under the same knuckle, steering through the same tie-rod.

**Rear corners**
1–4 as above.
5. Rider fits the **track cassette** (46 kg, rolled on its own track): its sprocket hub slides over the four studs and takes the lug nuts (the drive coupling is the wheel bolt circle, as on every production track kit); its anti-rotation link clips with one quick-release pin to the hardpoint on the arm at 0.30 m from the hub; the cassette's tensioner is factory-set.
6. Kit ID "TRACK"; adapter seated switch; tension indicator switch closed (idler in window).
7. Drive-coupling check with the corner still lifted: the rear motor turns the sprocket one quarter-turn at 10% torque; sprocket-speed sensor on the cassette must agree with the hub speed within 2%.
8. Lower the corner: carrier to 25° (raises the rear body 60 mm for approach angle and re-centres the cassette under the seat); pin engages.

With four kit IDs, four adapter switches and two tension switches confirmed, the rider confirms SNOW: rear 2-speed to 12:1, torque maps, 45 km/h cap, front carriers at 12°, rear at 25°.

**Where do the removed wheels go?** On the trailer or at the base. An optional accessory carries two wheels on the rack (22 kg, X −0.9 to −1.1 m); four wheels on the vehicle are not proposed (44 kg, 1.3 m of rack length).

Time: ~5 min per corner with practice; 20 min total; no jack, no lift, no tools beyond the lug wrench.

## 6.4 SKI → ROAD, ROBOTIC → ROAD, and SNOW-mode geometry changes

SKI → ROAD is 6.3 in reverse; ROAD is declared only with four wheel IDs, four adapter switches open, and all carriers at 12°. In SNOW the controller may still command the rear carriers between 20° and 38° (cassette approach angle) and the front between 12° and 20° (ski pressure) at ≤ 5 km/h with the same pin logic; front skis at more than 20° would lift the ski tips (limiter strap) and are refused.

## 6.5 Wheel storage: the cross-sections that decide it

**Question: where is the wheel when it "retracts"?**

On the base vehicle, the wheel never retracts. It moves within the fender arch between full bump (top at Z 0.78 m) and LIFT (top at Z 0.38 m). It stays fully exposed at the body side and it is removed, not stowed, for SKI.

On the M variant, the wheel is swung **upward and inward along X** (not inward along Y: the arm plane is fixed at Y ±0.34, the wheel plane at Y ±0.49) to −50°: wheel centre at X ±0.482, Z 0.817, tyre from Z 0.487 to 1.147. It ends up beside the rider's shin (front) and hip (rear), outboard of the footboards (tyre inner face Y 0.365 vs footboard outer edge Y 0.36), partially exposed like the Gibbs Quadski's. It is above the waterline (draft 0.28–0.30 m on the variant hull) by ~0.2 m at the tyre bottom.

```
 CROSS-SECTION at the front axle plane, M variant, wheels RETRACTED (looking forward)
                       rider
                        ▲
        ┌───────────────┼────────────────┐   Z 1.15 tyre top
        │ tyre  ┌───┐   │    ┌───┐ tyre  │
        │ (Y    │   │   │    │   │ (Y    │   Z 0.82 wheel centre, X +0.48
        │ 0.365 │   │ footboard │   │ 0.615)│   Z 0.49 tyre bottom
        │ …0.615└───┘Y0.36 │   └───┘       │
   ═════╪═══════════════ sheer / deck ═══════╪═════  Z 0.55
        │      arch flap closed             │
        │  ╲    sealed tub (5083)         ╱ │   waterline Z ≈ 0.28
        │    ╲__________________________╱   │
        └───────────────────────────────────┘   keel Z 0
```

**Collision and packaging checks (from the sweep table in Section 2.3):**
- Tyre vs chassis: the tyre's inner face is at Y 0.365; the sill outer face at Y 0.36 + node 0.415… **the node extends to Y 0.415 and the tyre inner face is at 0.365: they overlap in Y by 50 mm.** They do not collide because they never share X and Z: the node occupies X ±0.161 ± 0.08, Z 0.35–0.52; the tyre's nearest approach is in LIFT/RETRACT at X ±0.482 ± 0.33 → X from ±0.15 to ±0.81, Z 0.05–0.38 (LIFT) or 0.49–1.15 (RETRACT). At X = 0.24 (node edge) the tyre's Z range in LIFT is 0.05–0.24 (below the node at 0.35) and in RETRACT 0.62–1.02 (above the node at 0.52). Margin ≥ 0.10 m both ways. **Passes.** A 27 in tyre (+13 mm radius) still passes; a 28 in tyre does not without moving the node.
- Suspension vs body: the coil-over lies between the carrier (inboard, Z 0.55 upper eye) and the arm at 0.275 m out; its envelope rotates with the carrier inside the arch; the arch liner is cut to the union of all states (fender inner skin ≥ 0.83 m; arch opening from X +0.29 to +0.99 at the front).
- Steering: the tie-rod inner joint is on the axis, so the tie-rod rotates with the arm and never changes length (`calc/steering.py`); the rack sits on the axis line inside the chassis, between the two front nodes.
- Brake lines: none cross the arm (inboard brakes); the caliper is on the carrier; the hydraulic line has a 45° service loop inside the sill cavity.
- Motor wiring and coolant: enter the carrier at the axis height through a bulkhead; 200 mm service loops in the sill cavity absorb the 38°/100° sweep with bend radii ≥ 8× cable diameter; verified by 10,000-cycle rig test (Prototype 1).
- Sand/snow: the sector slots open downward (self-clearing); the pin has a tapered nose; the disc cover is a labyrinth, not a seal; the carrier housing has a drain; the arch is open at the bottom.

## 6.6 What is explicitly NOT done (the "no cheating" list)

- No wheel disappears: on the base vehicle it is unbolted by the rider; on the variant it is visible beside the body.
- No ski or track appears: they are separate kits, carried on the trailer.
- No bay door closes over a moving arm; the variant has only a planing-surface flap under the retracted wheel, hinged on the hull, clear of the arm (Gibbs/WaterCar pattern [PAT-6][PAT-9]).
- No component shares space: checked above for tyre/node, tyre/footboard (Y separation 5 mm minimum: increase to 15 mm by moving the footboard edge to Y 0.35 in CAD), coil-over/arch, tie-rod/axis, node/battery (the node is outboard of the sill, the battery inboard).
- No invisible actuator: it is inside the sill cavity behind the disc cover, 120 mm stroke, and it is reachable.

## 6.7 Frame-by-frame sequences for visualisation

**SEQUENCE A — ROAD → ROBOTIC (HIGH)**

| Frame | What moves | Direction | Axis | Opens / closes | Wheel | Lock | Load carried by |
|---|---|---|---|---|---|---|---|
| 1 | nothing; amber lines change from steady to breathing | — | — | — | in the arch, tyre top flush with the fender crown line minus 0.17 m | pins engaged at 12° | pins |
| 2 | four pins withdraw 12 mm inboard | −Y (into the node) | — | — | unchanged | pins out | actuators + brakes (vehicle ≤ 5 km/h) |
| 3 | four carriers rotate 13° (half-way); front wheels swing down-and-rearward, rear wheels down-and-forward; body rises 0.10 m | front: carrier turns so the leading arm's tip goes down/back; rear: trailing arm's tip goes down/forward | corner pivot axes (Y-parallel, at the carrier disc centres visible on the body sides) | nothing opens; the wheel begins to drop out of the arch | centre 0.05 m inward, 0.10 m lower relative to the body | out | actuators |
| 4 | carriers reach 38°; body up 0.204 m; wheels 0.095 m inward | same | same | — | tyre top now 0.10 m below the arch lip: the arch visibly frames empty space above the tyre | pins drop into the 38° slots | pins |
| Final | actuator brakes apply; lines steady; vehicle stands 0.48 m clear, wheelbase 1.11 m | — | — | — | — | engaged | tyre → arm → carrier → pin → node |

**SEQUENCE B — ROBOTIC → ROAD**: frames in reverse; frame 4 becomes "carriers reach 12°, tyres re-fill the arches"; final gate adds "four wheel IDs present".

**SEQUENCE C — ROAD → SKI (front-left shown; the other corners repeat)**

| Frame | What moves | Direction | Axis | Opens / closes | Where the wheel goes | Where the ski comes from | Lock | Load carried by |
|---|---|---|---|---|---|---|---|---|
| 1 | vehicle parked, Park on, HV drive off; FL pin withdraws | — | — | — | on the ground | on the trailer | FL pin out, others in | other three corners |
| 2 | FL carrier rotates 12° → 50°; the wheel is pushed down; the body's FL corner rises 0.28 m; the FL arm extends to full rebound | wheel down and rearward relative to the body | FL pivot axis | — | still on the ground, then off it as the body rises past its reach | — | pin engages at 50° | three corners + the FL actuator until the pin seats |
| 3 | rider removes four lug nuts; wheel comes off the hub | −Y (outboard) | — | — | **off the vehicle**, onto the trailer | — | engaged | three corners |
| 4 | ski adapter plate goes onto the four studs; lug nuts on; ski saddle onto the pivot pin; quick-release pin in; limiter strap clipped | +Y onto the hub | — | strap switch closes | — | from the trailer onto the hub | engaged | three corners |
| 5 | FL carrier rotates 50° → 12°; the ski reaches the ground and takes the corner load; pin engages at 12° | ski down | FL pivot axis | — | — | on the ground under the same knuckle | engaged at 12° | ski → adapter → hub → knuckle → arm → carrier → pin → node |
| Rear corners | as above with the cassette on the studs, anti-rotation pin to the arm hardpoint, quarter-turn drive check with the corner lifted, lower to 25° | | | tension switch closes | off the vehicle | from the trailer, rolled on its own track | engaged at 25° | track → sprocket → hub → arm → carrier → pin → node |
| Final | rear 2-speed shifts to 12:1 at standstill; SNOW declared | — | — | — | — | — | all engaged | — |

**SEQUENCE D — ROAD → MARINE (ARC-2B M variant only)**

| Frame | What moves | Direction | Axis | Opens / closes | Wheel | Lock | Load carried by |
|---|---|---|---|---|---|---|---|
| 1 | vehicle drives down the ramp at ≤ 5 km/h; hull hatches confirmed closed; bilge dry; IMD ≥ 500 Ω/V | — | — | hatch switches | on the ground | pins at 12° | wheels |
| 2 | afloat: all four arms at full rebound for 3 s (buoyancy ≥ 90%) | — | — | — | hanging in the water | pins | hull (buoyancy) |
| 3 | jet spins to 10% in neutral (bucket down); thrust confirmed by motor current | — | — | — | — | — | hull |
| 4 | pins withdraw; both front carriers rotate 12° → −50° together, then both rear (symmetric, ≤ sea state D); the wheels swing up and inward along X to beside the rider | wheel up and toward the vehicle centre | pivot axes | arch flaps (hull-hinged) close under the retracted wheels | tyre bottom 0.49 m above the keel line, ~0.2 m above the waterline; visible beside the footboards/hips | pins engage at −50° | hull; wheel inertia through the pins |
| 5 | land drive contactor opens; hub brakes irrelevant; MARINE-DISPLACEMENT declared (≤ 4 kn) | — | — | — | stowed | engaged | hull |
| Final | planing gates (seat switch, kill cord, depth ≥ 1 m, bilge dry) → planing enabled | — | — | — | — | — | hull (planing lift) |

MARINE → ROAD is the reverse: wheels down while afloat, then ramp; land drive enabled only when two arm sensors show wheel load and the hull water-level sensor shows the keel above water.
