# 5 — The four corner mobility modules

## 5.1 Mechanism comparison (what was compared before choosing)

The feasibility study compared three mechanisms (`docs/feasibility/03_transformation_mechanism.md`). This document adds a fourth and revises the front-arm orientation.

| Criterion | A. Trailing/leading arm + actuated coaxial carrier | B. Four-bar wheel-leg (2 driven joints) | C. Double wishbone on an articulated carrier | D. Arm + carrier with camber link (semi-trailing, inclined pivot) |
|---|---|---|---|---|
| DOF per corner | 1 spring + 1 actuated/locked | 2 actuated + 1 compliant | 1 spring + 1 actuated/locked | 1 spring + 1 actuated/locked |
| Packaging | swept volume stays inside the fender arch; pivot under the footboard/seat | large links; hip actuators of 3 kNm class | quarter-cylinder sweep through the footwell (longitudinal drum) or a hinged sub-chassis as wide as the arms | as A, plus a lateral link on the carrier |
| Strength | one boxed arm, one pivot cartridge | many joints, actuator gearboxes in the load path | proven A-arms plus a large drum bearing | as A plus link joints |
| Weight per corner | ~20 kg + motor | 30–45 kg with two actuators | ~22 kg + drum | ~22 kg |
| Manufacturing | machined carrier, welded box arm, purchased actuator | robotics actuators (no IP ratings published [SUP-4]) | commodity A-arms + custom drum | as A + link |
| Actuator force | 6.8 kN linear (self-lift), 0 while driving | 1.0–3.8 kNm continuously through the actuator | 0.75 kNm to rotate; 0 while driving | as A |
| Locking | spring pin into a sector, 25.5 kN shear at 5 g | must lock every joint | pin at the drum | as A |
| Steering behaviour | zero height-steer with the tie-rod inner joint on the axis (proved numerically in `calc/steering.py`) | needs steer-by-wire | conventional rack works only if the drum axis is on the rack line | as A only if the camber link is also on the axis, which removes its purpose |
| Suspension behaviour | roll centre at ground, no camber gain; anti-dive 30% with inboard brakes; anti-squat 28% | controller-defined | proper camber gain (A-arms) but 1° camber per 1° of drum rotation | camber gain at the cost of height–camber coupling (~0.3–0.5° per degree of carrier rotation) |
| Failure modes | pin/seal/arm root fatigue | actuator backdrive under impact | drum bearing, camber-induced wear | link joints |
| Maintenance | one pivot cartridge, one actuator, one coil-over per corner | robotics-grade | ATV-standard + drum | as A + link |
| Cost | 4 actuators + 4 machined carriers | 8 high-torque actuators | 4 drums + 8 A-arms | as A + 4 links |
| Transformation complexity | one motion, one lock | coordinated two-joint motion | one motion but a large sweep | one motion |

**Decision: A, with the front arm leading and the rear trailing.** D is the Gen-2 upgrade path for camber gain if road-mode handling tests demand it; B is excluded for the same reasons as in the feasibility study; C fails packaging.

## 5.2 The module (identical carrier, pivot, actuator, lock, sensors front and rear)

```
 SECTION through a FRONT-LEFT module at the pivot axis (looking forward; Y to the left)
                    chassis sill (Y 0.24…0.36)
        ┌────────────┬────────────────────────────────┐
        │  battery   │ PIVOT NODE  ▣ (bolted to sill)  │
        │  bay       │  ┌──────────────────────────┐   │
        │            │  │ taper roller ● 0.265     │   │  ← 150 mm bearing spacing on a Ø50 shaft
        │            │  │ CARRIER housing (cast)   │   │     seals: double lip + labyrinth + grease purge
        │            │  │   motor + 6:1 + disc     │   │
        │            │  │ taper roller ● 0.415     │   │
        │            │  └──────────┬───────────────┘   │
        └────────────┴─────────────┼───────────────────┘
                                   │ ARM root boss (Y 0.34), arm goes forward (leading)
                                   ╘════ boxed arm ═════╗ upright at Y 0.49
                                                         ║ hub + wheel (Y 0.365…0.615)
```

| # | Component | Design (V0) | Manufacturing |
|---|---|---|---|
| 1 | **Module housing / main carrier** | A356-T6 sand casting (billet 6082 for prototypes), 0.30 m disc footprint, coaxial with the pivot; carries the motor + reduction + inboard disc, the coil-over upper eye, the actuator lever (160 mm), the lock sector (150 mm radius, 5° slots, hardened insert), the coolant/HV bulkhead fittings and the absolute angle magnet | casting + CNC bores |
| 2 | **Pivot** | Ø50 42CrMo4 shaft, two taper-roller bearings 150 mm apart in the node; the carrier rotates on the shaft on its own bearing pair; the arm is keyed to the inner end of the shaft… **no**: the arm and the carrier both rotate about the same axis but independently: arm on the shaft (fixed to the shaft), shaft in carrier bearings, carrier in node bearings. Two concentric bearing pairs | machined + purchased bearings |
| 3 | **Arm** | 0.50 m boxed 5083 sheet (3 mm) welded box 90 × 60 mm section at the root tapering to 60 × 40 at the upright, with a machined 6082 root boss bonded/bolted in (no weld at the root); wheel plane 0.15 m outboard of the arm plane | laser-cut, formed, MIG, CNC boss |
| 4 | **Steering knuckle (front)** | forged/machined 7075 or 4140 upright on two sealed spherical bearings, KPI 8°, caster 5°, steering arm 120 mm at 20.7° toward the rear axle centre; rear: fixed hub carrier integral with the arm end | purchased ATV-class forging or CNC |
| 5 | **Wheel hub** | UTV-class sealed unit bearing, 4 × 110 mm PCD, 4 × M10 studs; the kit interface | purchased |
| 6 | **Brake** | inboard: 200 mm disc on the reduction output shaft inside the carrier's open inboard face; single-piston floating caliper; rear carriers add a mechanical parking lever | purchased ATV caliper, custom disc |
| 7 | **Drive motor** | 8–10 kW continuous / 15–20 kW peak PM motor, liquid-cooled, on the carrier with its axis parallel to Y; 6:1 planetary; rear adds a 2-speed (6:1 / 12:1) shifted by a dog clutch at standstill | purchased motor; gearset purchased/custom |
| 8 | **Damper + spring** | ATV coil-over, 110 mm stroke, 43 N/mm coil, piggyback reservoir; lower eye on the arm at 0.275 m from the pivot (motion ratio 0.55), upper eye on the carrier | purchased |
| 9 | **Actuator** | see 5.3 | purchased |
| 10 | **Mechanical lock** | Ø20 mm hardened pin, spring-applied (400 N spring), 24 V solenoid released, engages the carrier sector from the node; two inductive switches (engaged / retracted); manual release lever behind the disc cover | machined + purchased |
| 11 | **Hard stops** | polyurethane blocks on the node at carrier angles −2° and +55° (base) or −55° and +55° (variant); arm bump stop in the coil-over; arm rebound strap at 24° | bonded PU |
| 12 | **Bearings** | pivot taper rollers C₀ ≥ 60 kN; carrier bearing pair; knuckle spherical bearings; hub unit; all sealed | purchased |
| 13 | **Seals** | pivot: double-lip + labyrinth + grease purge; carrier housing: gasket + ePTFE vent; motor: IP67 unit; half-shaft CV boots | purchased |
| 14 | **Sensors** | carrier absolute angle (14-bit magnetic, ×2 redundant, IP67); arm angle (×1, cross-check); actuator internal position; pin switches (×2); hub wheel-speed; kit ID (RFID) in the hub adapter; motor temperature; corner accelerometer | purchased |
| 15 | **Wiring routing** | HV (2 × 25 mm² + shield), coolant (2 × 12 mm) and signal enter the carrier through a bulkhead plate on its inboard face at the pivot axis height; the 45° carrier sweep is absorbed by a 200 mm service loop inside the sill cavity; no cable crosses the arm pivot (the arm has only the hub speed sensor wire and, front, the ABS-type harness clip) | |
| 16 | **Service access** | remove the Ø0.30 m disc cover (4 quarter-turns): sector, pin, actuator rod end, coolant fittings, disc/caliper visible; wheel arch with the carrier at 50°: coil-over, half-shaft, CV boots; pivot cartridge removed inboard-out after pulling the shaft from the arch side | |

Correction to item 2 (kept visible on purpose): the arm is fixed to the shaft; the shaft turns in the carrier's bearings (suspension motion); the carrier turns in the node's bearings (geometry). Two concentric rotations, one axis.

## 5.3 Actuator system

| Parameter | Value (V0) | Status |
|---|---|---|
| Type | electromechanical ball-screw linear actuator, integrated 48 V brushless drive, CAN | TARGET |
| Voltage | 48 V (class A, no HVIL) | TARGET |
| Force | ≥ 7 kN dynamic (calc: 6.8 kN worst case), ≥ 10 kN static hold | DERIVED / TARGET |
| Stroke | 104 mm for 12°→50°; 120 mm ordered | DERIVED |
| Speed | 12 mm/s at 5 kN → ROAD→HIGH in 6 s; ≥ 20 mm/s unloaded | TARGET |
| Duty cycle | ≤ 10% at 7 kN; 25% at 3 kN (leveling); commercial units of this class list 5% duty at 10 kN [ACT-2], so leveling on the move is not a use case | BENCH |
| Self-locking | ball screw is back-drivable: a spring-applied holding brake (≥ 10 kN equivalent) is mandatory; a lead screw (self-locking) is the alternative at half the speed | TARGET |
| Position sensor | internal absolute (encoder on the screw) | |
| Load sensor | motor current (calibrated), plus the coil-over position as a load proxy | |
| Mechanical lock | separate pin/sector (5.2 item 10); the actuator is unloaded when the pin is engaged | rule |
| Emergency release | manual lever releases the pin; hex drive on the actuator screw through the disc cover for hand cranking | |
| Environment | IP69K static / IP66 dynamic, −30…+70 °C, salt spray 500 h; mounted inside the sill cavity | BENCH class [ACT-1] |
| Candidates | Thomson Electrak HD (to 16 kN), LINAK LA36/LA77 (to 10 kN), TiMOTION MA2 (8 kN), Exlar Tritex II (4.2 kN continuous, brake option) — none verified against a datasheet in this study | N |

Rule restated: **the actuator moves; the pin carries the load.** In ROBOTIC leveling with the pin out, the brake + screw carry the load at ≤ 5 km/h, which is why that state is speed-capped.
