# Part 9 — Marine system

## 9.1 Can the ARC-2B exterior body become the hull? No.

Three independent arguments, each sufficient:

**Volume.** `calc/buoyancy.py` (RC-0 assumptions) needs 0.61 m³ of displacement for 610 kg afloat with a rider. A tub filling the ATV underbody (1.95 × 1.10 × 0.45 m, block coefficient 0.62) holds 0.60 m³ *before* subtracting four wheel bays (0.36 m³). Available: **0.24 m³, i.e. −61% reserve buoyancy. It does not float.** Even ignoring the bays, draft would equal the tub depth (freeboard −0.01 m).

**Stability.** With the same geometry the estimated metacentric height is **−0.20 m** (KB 0.25 + BM 0.30 − KG 0.75). A negative GM capsizes at rest. The beam of an ATV (1.1 m tub between arches) is too narrow for a rider seated 0.9 m above the keel.

**Precedent.** The only production planing amphibious ATV, the Gibbs Quadski, is 3.26 m long, 1.59 m wide, 605 kg and needs 100 kW on water [AMP-1]; its patent claims length ≥ 2,400 mm, beam ≥ 1,250 mm and deadrise ≥ 10° as the planing envelope [PAT-29]. The exterior body of a 2.1 × 1.22 m ATV is below every one of those numbers.

An open ATV body also has footwells, a seat cut-out and a rear rack; there is no closed volume to seal. The brief's hidden-hull alternative is therefore mandatory, and it changes the vehicle's size.

## 9.2 What hull would work (parametric sweep)

`calc/buoyancy.py` sweeps hull plan size for ≥ 30% reserve buoyancy, ≥ 0.25 m freeboard and GM ≥ +0.25 m with the same bays and a 0.55 m depth:

| Hull L × B | Draft | Freeboard | Reserve | GM |
|---|---|---|---|---|
| 2.2 × 1.6 m | 0.28 m | 0.27 m | 38% | +0.45 m |
| 2.4 × 1.5 m | 0.27 m | 0.28 m | 42% | +0.34 m |
| 2.8 × 1.5 m | 0.23 m | 0.32 m | 76% | +0.48 m |

The smallest passing hull has 1.6× the plan area of the ATV tub and is wider than the ATV's overall width. Conclusion: **a planing marine ARC-2B is a different body, roughly Quadski-sized**, sharing the chassis platform and corner modules but not the exterior. Part 17 makes this the "ARC-2B M" variant.

## 9.3 The displacement "swim" option for the base vehicle

Case 3 of `calc/buoyancy.py`: with free-flooding arches (the retracted tyres themselves add 0.14 m³) and two deployable sponsons along the sills:

| Sponson Ø | Reserve buoyancy | GM |
|---|---|---|
| 0.30 m | −1% | +0.57 m |
| 0.40 m | +28% | +0.99 m |
| 0.50 m | +65% | +1.51 m |

Sponsons of 0.4–0.5 m diameter (inflatable, stowed in the sill panels, deployed by the marine interlock) make the base vehicle float and stable at rest, but the vehicle is then 2.0–2.2 m wide afloat and can only move at displacement speed: hull speed for a 1.95 m waterline is 3.4 kn (6.3 km/h) [HUL-2], and `calc/energy.py` estimates ~3 kW at 3 kn and ~13 kW at 5 kn. This is a **water-crossing capability** (river, lake shore, shallow bay in calm water) comparable to an Argo [AMP-9], not a marine sport mode. It is honest, cheap, and fits the "same machine, more horizons" promise without pretending to plane.

## 9.4 Conceptual design of the marine variant (ARC-2B M)

### Hull
- Structural tub in **5083-H116 aluminium** (welded, 4 mm bottom, 3 mm sides) or vacuum-infused glass/epoxy over a foam core; the tub *is* the lower chassis and carries the four pivot housings on its sides [MAR-2][MFG-5].
- Length 2.6 m, beam 1.5 m, depth 0.55 m, deadrise 12° at 0.4 LWL (ISO 12215-5 uses deadrise at 0.4 L_WL forward, bounded 10–30° [HUL-5]), two lifting strakes, a flat pad aft for the jet intake.
- The exterior body panels (angular black/white) are non-structural covers above the sheer line, so the ARC-2B identity survives; the hull is hidden below.
- Scantlings by ISO 12215-5 with planing kR = 1 [HUL-4]; local doublers around the four arch cut-outs.

### Wheel wells and retraction
- Free-flooding arches (not sealed bays): the arm passes through the tub side via the sealed pivot cartridge (Part 4); the wheel retracts to −70° carrier angle, putting the tyre's lowest point ≥ 0.2 m above the waterline (wheel centre 0.42 m above the pivot, pivot at ~0.5 m above the keel, draft ~0.27 m).
- Hinged **arch flaps** close the planing surface under the retracted wheel (Gibbs US 7,322,864 and WaterCar US 8,221,174 both claim this; the Gibbs family is estimated expired, the WaterCar patent possibly active to ~2029 [PAT-6][PAT-9], an FTO item). Exposed wheels add 14–28% resistance [AMP-10].
- Retraction drive: the base actuator covers 15°–60°; the marine variant adds a second lever position (two-stage crank) or a rotary worm sector to reach −70°. Load is only the arm and wheel self-weight plus hydrodynamic drag when afloat (Part 3: ~0.8 kN at the actuator).

### Seals and bulkheads
- Pivot cartridge: double lip seals + labyrinth + grease-purge, tested to 0.5 m head for 1 h (ISO 12217-3 swamped tests are the design reference [MST-1]).
- Three watertight compartments: forward (foam-filled), centre (battery + electronics, sealed box within the tub), aft (jet, pumps).
- Battery box: IP67 as a unit, mounted above the bilge, its own float switch; HV connectors IP68/IP6K9K with HVIL [BAT-4].

### Buoyancy, CG and CB
- Rider seated CG ≈ 0.75 m above the keel (assumption); KB ≈ 0.15 m, BM ≈ 0.55 m at 2.6 × 1.5 m → GM ≈ +0.4 m (sweep). Heel by a 100 kg rider leaning 0.5 m: heeling moment 0.5 kNm vs righting ≈ 610 kg × 9.81 × 0.4 × sin(heel): equilibrium at ~12° heel. Acceptable at rest; must be verified on a proper hydrostatics model and by the offset-load test of ISO 12217-3.
- Swamped condition: forward and side voids foam-filled (CAMI practice [AMP-8]) so that the flooded vehicle stays afloat with the battery mass supported; the base rule set is ISO 12217-3 / ABYC H-8 (US federal flotation rules explicitly exclude amphibious vessels [MST-2], and the EU RCD excludes amphibious vehicles from its scope [REG-5], so these are voluntary design targets, not certifications).

### Water jet
- 155–160 mm axial single-stage PWC-class pump [JET-3], driven by a dedicated marine motor (not the traction motors, which are on the carriers): 60–90 kW peak for planing at 610 kg (0.10–0.15 kW/kg from `calc/energy.py`; Quadski runs 165 W/kg [AMP-1]), 20–30 kW continuous cruise.
- Intake: flush grate in the aft pad with a weed-shedding rake; the Gibbs guidance of thrust per intake length ≥ 18 kN/m to plane with open arches is public domain [PAT-26].
- Steering nozzle: ±25° electric or cable-driven from the handlebar; the same handlebar steers the wheels (cable coupling as in expired Gibbs US 7,766,709 [PAT-28]).
- Reverse/brake: electrically actuated reverse bucket with neutral detent (iBR pattern [JET-4]); the bucket, not motor reversal, provides braking.
- Cooling: closed glycol loop for the motor/inverter with a keel cooler or a raw-water heat exchanger on the jet's pressure tap (PWC practice), never raw water through the motor.

### Battery isolation and electrical
- Marine mode adds ISO 16315 (electric propulsion in small craft) and ABYC E-30 (> 50 V DC) requirements [MST-6][MST-7]; a 48 V marine drive would stay under the ABYC E-11 threshold but 60–90 kW at 48 V is 1,500–1,900 A, which is impractical. The pack therefore stays class B (Part 11) and the marine drive uses the same HV bus through its own contactor.
- Lanyard kill-cord and seat switch interrupt the marine drive (PWC practice, ISO 13590 [MST-5]).

### Emergency flotation and bilge
- Two 12 V bilge pumps of the 1,100 GPH class (~4 A each [MAR-1]) with independent float switches in the centre and aft compartments, wired directly to the LV battery through their own fuses.
- High-water alarm at 50 mm.
- Inflatable emergency flotation collar (CO₂) in the sill panels for the swamped case.
- Drain plugs at the transom for trailer drainage; arch scuppers.

### Energy
Planing consumes 10–12 kWh per hour of mixed use on comparable electric PWCs [JET-6]. A 12 kWh land pack gives well under one hour on the plane; the marine variant needs ≥ 20 kWh (≈ 130–150 kg), which is another reason it is a separate variant rather than a mode of the base vehicle.

## 9.5 Marine stability while transforming

Retraction happens afloat with the wheels unloaded, so the vehicle's CG moves *up* by roughly 4 × 25 kg × 0.53 m / 610 kg ≈ 0.09 m as the wheels rise. GM falls from ~0.4 m to ~0.3 m at the RC-0 hull. The retraction sequence must therefore be symmetric (both sides together) and refused above sea state for design category D (Hs 0.3 m [MST-4]).

## 9.6 Summary

| Question from the brief | Answer |
|---|---|
| Can the exterior body be the hull? | No (volume, stability, precedent) |
| Hidden hull under the body? | Yes, but only at ~2.4–2.8 m × 1.5 m, i.e. a longer, wider variant |
| Does adding a jet make it seaworthy? | No. Buoyancy, reserve buoyancy, GM, swamped flotation, freeboard and 60–90 kW are all needed first |
| Cheapest honest marine capability for the base vehicle? | Displacement swim mode with deployable sponsons and a 15–30 kW electric jet module [JET-7], ≤ 4 kn, calm water |
