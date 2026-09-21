# ARC-2B — Master Engineering & Transformation Architecture (V0)

The CAD-ready layer on top of the feasibility study in `docs/feasibility/`.
Where the feasibility study asked "can it be built", this document says
"build it like this", in the vehicle's coordinate system, with every number
tagged TARGET, TBD, DERIVED or BENCH and reproduced by `calc/run_all.py`.

**Two corrections to the feasibility study are made here and explained
(Section 2.2):** the front arm is *leading* (pivot behind the wheel), not
trailing, and the brakes are *inboard* on the carriers. Both follow from the
packaging and anti-dive numbers in `calc/kinematics.py`; the trailing front
put the pivot at the bumper face and 125% pro-dive under braking.

**Research status:** no new external sources could be fetched in this
environment (egress policy); the research base is `docs/feasibility/REFERENCES.md`
with its per-entry verification tags. New content here is design work on that
base; anything needing a new source is marked TBD.

| Section | File | Brief sections covered |
|---|---|---|
| 1 | [Design language](01_design_language.md) | 2 |
| 2 | [Master geometry](02_master_geometry.md) | 3, 30 |
| 3 | [Mass budget](03_mass_budget.md) | 4 |
| 4 | [Chassis and load paths](04_chassis.md) | 5 |
| 5 | [Corner modules, mechanism comparison, actuators](05_corner_modules.md) | 6, 7, 21 |
| 6 | [Exact transformation, wheel storage, frame sequences](06_transformation.md) | 8, 11, 12, 14, 15, 33, 34 |
| 7 | [Modes: road, robotic, ski](07_modes.md) | 9, 10, 13 |
| 8 | [Marine options and variant](08_marine.md) | 16, 17 |
| 9 | [Steering, drive, brakes](09_steering_drive_brakes.md) | 18, 19, 20 |
| 10 | [Failures, interlocks, environment](10_failures_safety_environment.md) | 22, 23, 24 |
| 11 | [Load cases, materials, manufacturing, service](11_structure_materials_manufacturing_service.md) | 25, 26, 27, 28 |
| 12 | [CAD master package and dimensioned table](12_cad_package.md) | 29, 30 |
| 13 | [Design bible and image description](13_design_bible.md) | 31, 32 |
| 14 | [Research base and existing technology](14_existing_technology.md) | 35, 36 |
| 15 | [Recommended V0, Buildable V0, DO NOT BUILD YET](15_final_architecture_v0.md) | 37, 38, 39, 40 |
| — | [calc/](calc/) | `params_v0.py`, `mass_budget_v0.py`, `kinematics.py`, `steering.py`, `ski_track.py`, `energy_buoyancy_v0.py` |

**Follow-on:** [`docs/amphibious/`](../amphibious/README.md) revisits water mode with deployable flotation and finds a displacement-speed integrated architecture (tub + fold-down rails + inflatable tubes + stern pod).

## The vehicle in one paragraph

A 487 kg single-rider electric ATV (2.15 × 1.24 m, wheelbase 1.30 m, 26 in
tyres) whose four corners are identical modules: a 0.50 m boxed arm (leading
at the front, trailing at the rear) turning on a coaxial carrier that a 48 V
7 kN actuator rotates between 12° and 50° and a spring-applied pin locks
every 5°. The motor and the inboard brake sit on the carrier; the steering
tie-rods pivot on the carrier axis so height changes never steer. ROAD is
12°; ROBOTIC is 12°–50° per corner with body leveling and a 0.28 m single-
corner self-lift; SKI/SNOW is a five-minute-per-corner swap of hub-mounted
skis and track cassettes using that self-lift. Water is a removable hull
first and a longer-hulled ARC-2B M variant later, because the ATV body
cannot float.

## Reproduce the numbers

```bash
cd docs/architecture/calc && python3 run_all.py
```
