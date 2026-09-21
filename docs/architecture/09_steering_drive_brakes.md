# 9 — Steering, drive and braking systems

## 9.1 Steering: comparison

| Option | How it would work on ARC-2B | Verdict |
|---|---|---|
| Mechanical (rack, tie-rods) | rack on the chassis, tie-rod inner joints **on the front pivot axis line**; EPS assist on the column | **Selected.** Zero height-steer and zero bump-steer by geometry (`calc/steering.py`: 0.000 mm length change over −50°…+50°); fails safe (mechanical) |
| Electric assist (EPS) | column-mounted assist motor on the mechanical system | **Selected** as the assist layer; maps per mode (road/snow) |
| Steer-by-wire | steering actuator on each front carrier; no column | rejected for V0: safety case (fail-operational dual channels [FS-2]) and cost, with no geometric benefit once the tie-rod is on the axis |
| Hub steering | kingpin inside the hub (motorcycle hub-centre) | rejected: incompatible with the ski/track hub interface and adds unsprung mass |
| Carrier steering | rotate the whole carrier about a vertical axis | rejected: the carrier already rotates about Y; a second axis on a 3 kNm-loaded node is a cardan joint on the chassis |
| Knuckle steering | conventional kingpin knuckle at the arm end | **Selected** (it is what the mechanical system steers) |

### Geometry
- Rack at X +0.161 (on the axis line), Z 0.434, inner joints at Y ±0.26 (80 mm inboard of the inner pivot bearing), rack travel ±60 mm.
- Tie-rod 439 mm at ROAD; outer joint on the knuckle arm 120 mm behind the wheel centre at 20.7° toward the rear axle centre (Ackermann direction).
- Steer angles 32° outer / 42° inner (ideal Ackermann inner would be 50°: partial Ackermann is normal on loose surfaces). Turning radius 2.45 m to the outer wheel.
- KPI 8°, caster 5°, scrub radius ≤ 20 mm (inboard brakes make this easy because there is no caliper at the hub).

### Steering in each mode
| Mode | Behaviour |
|---|---|
| ROAD | full mechanical + EPS "road" map; ±32/42° |
| ROBOTIC | identical geometry at any carrier angle (proved); EPS "crawl" map (more assist at zero speed); the interlock requires ±10° for a transformation only so the tie-rods stay near the axis plane during the move (they would work anyway, this is conservatism about the rack's cover) |
| SKI | same knuckle, ski pivots on the hub adapter; EPS "snow" map (+30% assist for carbide bite); ski pitch is free about the adapter pin |
| MARINE (variant) | the handlebar also drives the jet nozzle through a cable from the rack; wheels retracted; the tie-rods stay attached and simply rotate with the arms |

**How the front module transforms without changing steering geometry:** the tie-rod's inner joint lies on the axis about which the arm and the carrier rotate, so any rotation of the carrier or the arm is a rigid rotation of the triangle {axis, tie-rod, knuckle arm}. The same script shows that a rack placed 40 mm behind and 60 mm below the axis would steer the vehicle by up to 20° over the sweep. This is the single most important geometric rule in the vehicle.

## 9.2 Drive system: comparison

| Option | Unsprged / notes | Verdict |
|---|---|---|
| 4 independent hub motors | +18–39 kg per corner unsprung; motor immersed; incompatible with cassette sprocket geometry [MOT-1][MOT-2][MOT-6] | rejected |
| 2 axle motors + mechanical differentials | a prop-shaft/diff to corners that rotate 38° needs plunge and angle beyond CV limits unless the diff itself sits on a rotating cross-carrier; open diffs lose torque on mixed grip | rejected |
| 2 motors + 4WD coupling | same driveline problem, plus a transfer mechanism | rejected |
| Carrier-mounted motors, 4 | motor rotates with the carrier; half-shaft sees only suspension angles (±15°); no immersion on the base vehicle; standard hub for kits; per-wheel torque control | **Selected** |

### Design
| Element | V0 |
|---|---|
| Motor | 4 × PM liquid-cooled, 8–10 kW continuous / 15–20 kW peak, ~35 Nm peak, ≤ 6,500 rpm, IP67 as a unit, on the carrier with axis parallel to Y |
| Gear reduction | 6:1 planetary integral with the motor; rear carriers add a dog-clutch 2-speed (6:1 / 12:1) shifted at standstill for SNOW/crawl (Mercedes G 580 uses a per-motor 2-speed for the same reason [TV-1]) |
| Differential | none (four independent motors; "virtual lock" by torque control) |
| Driveshaft | plunging CV half-shaft, ~0.42 m, rated ≥ 1,000 Nm (brake torque 800 Nm at 1.2 g on the front passes through it) |
| Brake | inboard disc on the reduction output (see 9.3) |
| Regen | up to 0.3 g blended, per-wheel; 0.15 g cap in SNOW |
| Mechanical disconnect | none needed: an unpowered PM motor free-wheels through the planetary; the marine variant opens the traction contactor |
| Ski/track drive coupling | the hub bolt circle (4 × M10 on 110 mm PCD): the cassette's sprocket hub bolts on like a wheel |

## 9.3 Braking

| Item | V0 |
|---|---|
| Hydraulic vs electric | hydraulic service brakes (two independent circuits: front pair, rear pair, ANSI/SVIA practice) + regenerative blending; no brake-by-wire in V0 |
| Discs | 4 × 200 mm inboard on the carriers, ventilated, on the reduction output; exposed on the carrier's inboard face under the body for cooling |
| Calipers | single-piston floating, ATV class; rear with a mechanical parking lever |
| Parking brake | cable-operated on both rear calipers; required for LIFT and KIT_SWAP; holds on 30% |
| Emergency braking | any circuit alone gives ≥ 0.4 g; regen adds ~0.3 g without hydraulics; the E-stop cuts torque but does not apply brakes |
| Redundancy | two circuits + regen + parking brake = four independent retarders |
| During transformation | service brakes released (creep) at ≤ 5 km/h; parking brake mandatory for LIFT; brake lines have 45° service loops in the sill (no line crosses the arm because the caliper is on the carrier) |
| If the transformation actuator fails | braking is unaffected: the caliper and disc are on the carrier, which is pinned; a corner frozen at any angle still brakes |
| Marine | no wheel braking; the reverse bucket |
| Thermal (TBD) | 637 kg from 60 km/h = 88 kJ per stop; repeated descents need the inboard disc to reject heat inside the body: a ducted airflow path from the arch is planned and must be validated (Prototype 4) — this is the cost of choosing inboard brakes for anti-dive |
