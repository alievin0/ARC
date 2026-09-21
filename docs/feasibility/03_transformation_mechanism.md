# Part 3 — Transformation mechanism: three candidates, one selection

> **Revision note (V0 architecture).** `docs/architecture/` supersedes two decisions in this part after packaging and side-view-geometry checks: the front arm is **leading** (pivot behind the wheel, under the footboard), not trailing, and the brakes are **inboard** on the carriers. Reasons and numbers: `docs/architecture/02_master_geometry.md` §2.2 and `docs/architecture/calc/kinematics.py`.

> All numbers below are DERIVED from the RC-0 assumptions in `calc/params.py`
> by `calc/mechanism_statics.py`. They are sizing estimates for comparison,
> not a specification. Re-run `python3 calc/run_all.py` after changing an
> assumption.

## 3.0 What the corner module has to do (functional requirements)

| ID | Requirement | Value used for sizing (RC-0) | Basis |
|---|---|---|---|
| F1 | Road-mode wheel travel | 0.22 m | ATV benchmark range 0.21–0.25 m (Part 1) |
| F2 | Road-mode ground clearance | 0.28 m | ATV benchmark 0.28–0.30 m |
| F3 | Robotic-mode extra ride height | +0.20 m, per corner independent | Study target; comparable to 4×4 air-suspension lift ranges (Part 1, D) |
| F4 | Lift one loaded corner clear of the ground with the other three on the ground | static corner load 1.45 kN, plus friction | Needed for "self-jack" kit swaps and for obstacle stepping |
| F5 | Retract wheel above the marine waterline (marine variant only) | wheel centre ≥ 0.5 m above keel | Part 9 hydrostatics |
| F6 | Front steering ±35° that does not change with corner geometry | zero "height-steer" | Otherwise every corner adjustment steers the vehicle |
| F7 | Survive 3 g bump and 5 g landing loads at the wheel with the actuator NOT in the load path | 4.3 kN / 7.2 kN per corner | Part 10 load cases |
| F8 | Hold any commanded position with power off, mechanically | spring-applied lock | Part 6 ("never software alone") |
| F9 | Accept a ski (front) or a track cassette (rear) on the same hub/spindle interface | hub bolt pattern + anti-rotation point | Part 8 |
| F10 | Sealed for immersion of the lower half of the module (marine variant); sand/snow/salt for all | IP67 at joints, IP69K on actuator | Part 5, Part 9 |

Static corner load W (RC-0): gross mass 590 kg / 4 → **1.45 kN**.
Dynamic factors: 3.0 (bump), 5.0 (landing), 1.5 (lateral), 1.2 (braking).

### The one principle that decides the comparison

In every mature system that changes wheel geometry on a vehicle
(hydropneumatic ride-height, aircraft landing gear, Gibbs amphibians,
ATV track kits) **the actuator positions a reference and a mechanical
element (lock, over-centre link, self-locking screw, hydraulic check
valve) carries the driving loads**. The actuator never sees the 3–5 g wheel
impacts. An articulated robot leg is the opposite: the joint actuator carries
the ground reaction all the time, which is why legged robots need actuators
with 10× the torque density of anything sold for vehicles. ARC-2B must be
the former kind of machine, or it becomes the "four giant robot legs" the
brief excludes.

## 3.1 Option A — Actuated four-bar wheel-leg

```
      SIDE VIEW (one corner)              chassis
                                     ┌──────────────┐
      upper link  o================o │  hip actuator│
                 /                  \│  (T_hip)     │
      coupler   /   upright + hub    \──────────────┘
      (upright) o=====( W )=====o  lower link, driven
                          \_/  wheel
```

*Concept.* Upper and lower links from the chassis to an upright, like a
double wishbone seen from the side. One or both link angles are actuated
(hip, and knee-equivalent). Compliance comes from a series-elastic element in
the actuator or a small spring on one link. This is the family of ETH
ANYmal-on-wheels, Hyundai Elevate and every wheel-leg research platform
(Part 1, A).

| Criterion | Value / assessment |
|---|---|
| Degrees of freedom (per corner) | Four-bar M = 1; to keep the upright attitude useful across the range you need either a parallelogram (M = 1, attitude constant) or two driven joints. Practical: **2 driven DOF** + 1 compliant DOF |
| Actuator count | 2 per corner (8 per vehicle) + 2 steering if steer-by-wire |
| Actuator location | at the chassis-side joints (good for sprung mass) |
| Mechanical advantage | none in the sense of a lock: torque at hip = W × horizontal reach = 1.45 kN × 0.43 m = **629 Nm static** |
| Worst-case actuator load | **1.9 kNm at 3 g, 3.1 kNm at 5 g** continuous through the actuator and its gearing |
| Joint loads | same as Option C at the pivots, but transmitted through the actuator's output bearing/gear as well |
| Wheel travel | whatever the controller allows; passive travel small unless a real spring is added |
| Ground clearance range | excellent (0 to > 0.4 m) |
| Packaging | links sweep a large volume; actuators at the hip are large (3 kNm class) |
| Unsprung mass | links + upright + wheel; actuators sprung if at the hip |
| Failure modes | actuator/gear failure = loss of corner; backdriving under impact; thermal limits of a motor holding torque statically |
| Locking | a separate lock is still required for road mode, otherwise the actuator holds 3 g loads all day |
| Maintenance | robotics-grade actuators, encoders, thermal management |
| Manufacturability | low-volume robotics supply chain; no powersports precedent at rider-carrying scale (Part 1: Hyundai Elevate was a scale model; no human-carrying wheel-leg vehicle has been demonstrated on public roads) |

**Verdict.** This is the architecture the brief rightly excludes. It is
technically what the concept boards draw ("robotic mode" arms), but it
places 3 kNm shock loads through eight actuators and needs research-grade
hardware. RED for a road-going product; YELLOW as a low-speed research
platform.

## 3.2 Option B — Conventional double wishbone on a rotating corner sub-frame ("drum")

```
      FRONT VIEW (one corner)
       chassis ┌────┐
               │drum│ ← rotates about a LONGITUDINAL axis, driven + locked
               │ o──┼───────o   upper A-arm   \
               │    │        \  upright        |  proven ATV geometry
               │ o──┼─────────o lower A-arm   /
               └────┘          ( W )
```

*Concept.* Keep the proven ATV double A-arm. Mount both inner pivots on a
corner sub-frame that can rotate about a longitudinal axis in chassis
bearings. A small rotation (0–25°) drops the wheel (raises the body); a
large rotation (≥ 90°) swings the whole suspension up beside the body.

| Criterion | Value / assessment |
|---|---|
| DOF | wishbone four-bar M = 1 (spring-controlled) + drum rotation 1 (actuator/lock) = **2** |
| Actuator count | 1 per corner (4) + mechanical steering |
| Actuator location | at the drum, fully sprung |
| Mechanical advantage | drum radius to wheel centre r ≈ 0.39 m; torque to rotate the loaded drum = W·r·(1+friction) ≈ **0.73 kNm**; while driving the LOCK carries 3 g = **1.7 kNm** and the actuator carries nothing |
| Worst-case actuator load | 0.73 kNm (rotating a loaded corner) |
| Joint loads | wishbone joints as any ATV; plus drum bearings carrying the whole corner |
| Wheel travel | unchanged ATV travel (0.22 m) at any drum angle |
| Ground clearance | +0.20 m needs ~30° of drum rotation, which puts **30° of camber** on the tyre unless the upright is re-angled (it cannot be, passively) |
| Packaging | the swept volume is a quarter-cylinder of radius ~0.55 m in the transverse plane: the retracted wheel ends up above the sill, inside the rider's footwell or fuel-tank volume. Very poor. With a transverse drum axis instead, the sub-frame has to be as wide as the A-arms (≈ 0.4 m) and becomes a hinged sub-chassis |
| Unsprung mass | lowest of the three (A-arms + upright + wheel, ~20 kg) |
| Failure modes | drum bearing/lock failure = corner collapse; camber-induced tyre wear/handling at height |
| Locking | discrete pin lock at the drum, straightforward |
| Maintenance | ATV-standard suspension service; drum bearings are new |
| Manufacturability | wishbones are commodity parts; the drum is a large machined/welded ring with bearings |

**Verdict.** Best road-mode behaviour (it *is* an ATV suspension), fewest
new parts in the load path, but the geometry change is the wrong kind:
height comes with camber, and retraction sweeps through the rider's space.
YELLOW for robotic mode, RED for retraction.

## 3.3 Option C — Trailing arm with an actuated carrier (coaxial)

```
      SIDE VIEW (rear corner, road mode)          SIDE VIEW (high mode)
                                 chassis
      ┌───────────────────────────────┐          ┌──────────────────────────┐
      │  motor  ┌────────┐            │          │  motor ┌────────┐        │
      │  on     │CARRIER │ lock pin ● │          │        │CARRIER │ ●      │
      │  carrier│  ⊙ ────┼── coil-over│          │        │  ⊙─────┼── c/o  │
      └─────────┴───┼────┴────────────┘          └────────┴───┼────┴────────┘
             pivot  │\  arm  θ=15°                            │ \
             axis   │ \_________                              │  \  arm θ=45°
                    │           \___( W )                     │   \
                                                              │    \____( W )
      ride height = L·sin(θ_carrier + θ_arm)     wheel moves 0.12 m forward, body rises 0.20 m
```

*Concept.* One boxed structural arm pivots about a transverse axis in a
**carrier**. The carrier is coaxial with the arm and can itself be rotated
relative to the chassis by a self-locking actuator, then pinned. The
spring/damper reacts between the arm and the carrier, so:

- suspension motion = arm relative to carrier (passive, spring/damper);
- geometry = carrier relative to chassis (actuated, slow, locked);
- the traction motor sits on the carrier (sprung, hidden) and drives the
  hub through a plunging CV half-shaft;
- steering tie-rod inner joints lie on the pivot axis, so carrier rotation
  and suspension travel produce zero steer change (see 3.5).

Front and rear both use trailing arms (pivot ahead of the wheel). Raising
the body moves *both* wheels forward by the same amount, so the wheelbase
is constant and only the body shifts back by 0.12 m relative to the wheels
(a leading front arm would shorten the wheelbase by 0.24 m at full height).

| Criterion | Value / assessment |
|---|---|
| DOF | arm/carrier 1 (spring) + carrier/chassis 1 (actuator + lock) = **2**; +1 steer at the front (mechanical) |
| Actuator count | **1 per corner (4)**; steering mechanical; no other actuators for road/robotic modes |
| Actuator location | on the chassis, inside the body, fully sprung |
| Mechanical advantage | linear ball-screw actuator on a 0.16 m lever; 30° of carrier rotation = 83 mm stroke; lever effect keeps the actuator at ≤ 6 kN |
| Worst-case actuator load | lifting a loaded corner: **5.1 kN** (629 Nm × 1.3 friction / 0.16 m). Swinging an unloaded wheel: 0.8 kN |
| Lock load | 3 g bump: **1.9 kNm**; 5 g landing: **3.1 kNm** through the pin/sector, never through the actuator |
| Joint loads | pivot bearings react vertical 7.2 kN (5 g) plus ~1.8 kNm of overturning moment from the wheel offset → ≈ 12 kN radial per bearing at 150 mm spacing (Part 10) |
| Wheel travel | 0.22 m at any carrier angle (spring/damper geometry moves with the carrier) |
| Ground clearance | +0.20 m at 45° carrier angle; up to +0.30 m at 60° with reduced wheelbase margin |
| Packaging | swept volume lies in the fender arch (the space an ATV already gives the wheel); the retracted position (marine variant only) puts the wheel beside the body above the waterline, as on the Gibbs Quadski, not inside a sealed bay |
| Unsprung mass | wheel/tyre 11 + hub/knuckle/brake 7 + half arm 5 + half-shaft 1.5 ≈ **25 kg** (0.20 of corner sprung mass) |
| Failure modes | pin lock failure (spring-applied so fails engaged); actuator failure holds position (self-locking screw); arm fatigue at the pivot boss; seal failure at the pivot |
| Locking | spring-applied, power-released pin into a sector plate (5° pitch) + self-locking screw + actuator brake (three independent holds) |
| Maintenance | pivot bearings and seals at the arm root; one actuator; one coil-over; CV boots. All reachable from the wheel arch with the arm at high angle |
| Manufacturability | arm = laser-cut/formed sheet box or cast aluminium; carrier = machined aluminium housing; pivot = commodity taper-roller pair; actuator and coil-over are purchased parts |

**Verdict.** Meets F1–F10 with one purchased actuator per corner and one
new structural part (the carrier). The compromise is a trailing-arm front
end (wheel moves rearward on bump, like a telescopic motorcycle fork), and a
longitudinal wheel shift with height. GREEN for road, YELLOW for robotic,
YELLOW for marine retraction (variant only).

## 3.4 Selection matrix

Weights reflect the brief's priorities: realism and safety first, then
maintainability and minimal hardware, then appearance. Scores 1 (poor) to 5
(good).

| Criterion | Weight | A: four-bar leg | B: wishbone + drum | C: arm + carrier |
|---|---|---|---|---|
| Actuator out of the dynamic load path | 5 | 1 | 5 | 5 |
| Actuator count / vehicle | 4 | 1 (8+) | 4 (4) | 5 (4) |
| Worst-case actuator load | 4 | 1 (3 kNm) | 4 (0.73 kNm) | 4 (5 kN linear) |
| Road-mode handling fidelity to an ATV | 4 | 2 | 5 | 4 |
| Height change without camber/steer side effects | 4 | 4 | 1 | 4 (zero-steer axis) |
| Retraction packaging (marine variant) | 3 | 3 | 1 | 4 |
| Steering integration (mechanical) | 4 | 2 | 4 | 4 |
| Track/ski interface at the hub | 3 | 3 | 4 | 5 |
| Unsprung mass | 3 | 3 | 5 | 3 |
| Sealing / immersion | 3 | 2 | 3 | 4 (single sealed pivot) |
| Maintainability | 3 | 2 | 4 | 4 |
| Manufacturability at low volume | 4 | 1 | 4 | 4 |
| Precedent at rider-carrying scale | 5 | 1 (none) | 4 (ATV + Gibbs-like drum: none) | 4 (Gibbs Quadski trailing-arm retraction; snowmobile rear arm; motorcycle swingarm) |
| **Weighted total (max 245)** | | **93** | **181** | **207** |

Option C is selected. It wins not because it is elegant but because it is
the only candidate that satisfies F4 (self-lift), F6 (zero height-steer),
F7 (actuator outside the load path) and F9 (hub interface for kits)
simultaneously with one actuator per corner.

## 3.5 Zero height-steer: the tie-rod trick

If the inner ball joint of each front tie-rod sits exactly on the module
pivot axis, then rotating the arm (suspension travel) or the carrier
(geometry change) about that axis is a rigid-body rotation of the triangle
{pivot axis, tie-rod, knuckle arm}. The tie-rod length and its angle to the
knuckle arm do not change, so the steer angle does not change. A single
steering rack on the chassis, with both inner joints on the common front
pivot axis line, steers both front wheels regardless of what each carrier is
doing. This is the same geometric argument used to eliminate bump steer on
trailing-arm steered wheels (2CV-type leading/trailing arm front ends;
hub-centre-steered motorcycles).

Practical consequence: the pivot shaft cannot be continuous across the
vehicle; the inner tie-rod joint sits on the axis line just inboard of the
inner pivot bearing, and the rack sits between the two front modules.

```
   TOP VIEW, front axle line
   ┌─────────────────────────────────────────────┐
   │        EPS rack (chassis)                    │
   │   ●───────────────────rack────────────────●  │  inner tie-rod joints ON the pivot axis line
   │   │ carrier L                    carrier R │  │
   ═══╪═══ pivot axis ═════════════════ pivot axis ═╪═══
   │   │\                                    /│  │
   │   │ \ arm                          arm / │  │
   │   │  \ tie-rod → knuckle    knuckle ← /  │  │
   └───┴───(WL)──────────────────────────(WR)─┴──┘
```

## 3.6 Actuator and lock sizing (Option C, RC-0)

| Item | Value | Note |
|---|---|---|
| Carrier rotation, driving modes | 15° (road) → 45° (high) → 60° (max, low speed only) | 45° of total sweep |
| Actuator stroke for 45° on a 0.16 m lever | 122 mm | chord 2·r·sin(θ/2) |
| Actuator force, lift loaded corner | 5.1 kN | includes 30% friction allowance |
| Actuator force, normal height change (vehicle on 4 wheels, load shared) | ≈ 2.5–3.5 kN | corner load partially carried by the other corners as the body rises |
| Actuator speed target | 10–15 mm/s → 30° in 6–8 s | slow by design: robotic mode is quasi-static, not active suspension |
| Actuator class | 6–10 kN electromechanical ball-screw, IP69K, integrated brake, absolute feedback | see Part 1 (F) for candidate off-the-shelf units and their actual ratings |
| Lock | spring-applied pin, 20 mm hardened, into a 5°-pitch sector; shear capacity ≫ 3.1 kNm / 0.15 m = 21 kN | double shear |
| Retraction (marine variant only) | additional −70° to −110° of carrier sweep, wheel unloaded (afloat) | separate rotary drive or two-stage lever; see Part 9 |

## 3.7 What Option C does NOT do

- It does not make the vehicle walk. Lifting one corner is a service and
  obstacle function at walking pace, with the other three wheels planted.
- It does not provide active (bandwidth > 1 Hz) ride control. The spring
  and damper do that, exactly as on an ATV.
- It does not stow skis or track cassettes inside the vehicle. See Part 8
  and Part 17 for why, and for the swap-in solution that uses the self-lift
  function instead.
