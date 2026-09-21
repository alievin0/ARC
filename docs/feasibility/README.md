# ARC-2B — Deep engineering feasibility study and manufacturable architecture

**Status:** engineering study, not a specification. Every number is either a
cited benchmark or a stated assumption (Reference Configuration RC-0,
`calc/params.py`), and the "DO NOT BUILD YET" list in Part 18 enumerates what
must be validated before fabrication.

**Source-verification notice.** This study was produced in an environment
whose egress policy blocked fetches to manufacturer, patent-office,
standards-body and publisher hosts, and whose web-search quota was exhausted
during research. `REFERENCES.md` tags every source with what was actually
read (official patent PDFs and a few datasheets/legal texts via mirrors were
read in full; most manufacturer and standards numbers are search-snippet
level). No source is fabricated; none of the snippet-level numbers should be
quoted externally before the verification pass listed first in Part 18.

**Follow-on document:** the CAD-ready master architecture in [`docs/architecture/`](../architecture/README.md) refines the geometry (front leading arm, inboard brakes, 487 kg budget) and adds the transformation sequences, design language and CAD package.

## Executive summary

1. **The product idea is sound; the concept as drawn is not.** Four modes on
   one platform is achievable, but not with 80–150 kg, not with skis and
   tracks stowed inside the wheel modules, and not with the ATV body as a
   planing hull. Each of these is redesigned in Part 17 with the smallest
   change that keeps the idea.
2. **Selected corner mechanism: trailing arm on a coaxial actuated carrier**
   (Part 3, Option C). One 48 V self-locking actuator and one spring-applied
   pin per corner; the spring/damper works at any carrier angle; the
   actuator is never in the driving load path; steering tie-rod inner joints
   sit on the pivot axis so height changes never steer the vehicle.
3. **Drivetrain: four carrier-mounted liquid-cooled motors with CV
   half-shafts** (Part 7). Hub motors are rejected on unsprung mass, sealing
   and track compatibility; the track "drive coupling" is the standard hub
   bolt circle, as on every production track kit.
4. **Ski and track modes are swap-in kits with vehicle self-lift** (Parts 4,
   8): park, lift one corner, click the kit onto the hub, lower; ~5 minutes
   per corner, no jack.
5. **Marine: the ATV envelope cannot float the vehicle** (−61% reserve
   buoyancy, negative GM; Part 9). Recommended: an optional displacement
   "swim kit" (sponsons + 15–30 kW jet, ≤ 4 kn) for the base vehicle and a
   separate ARC-2B M planing variant with a ~2.6 × 1.5 m hidden hull and
   60–90 kW, i.e. a Gibbs-Quadski-class programme.
6. **Mass and energy (RC-0):** ~440 kg curb, 590 kg gross; ~133 Wh/km on a
   mixed road duty cycle → 12 kWh pack for ~75 km road / ~38 km on tracks.
7. **Nothing in the recommended architecture is RED** in the feasibility
   matrix (Part 2); the planing marine variant is ORANGE.

## Contents

| Part | File | Words |
|---|---|---|
| 1 | [Existing technology](01_existing_technology.md) | tables with sources for wheel-leg, retraction, ski, track, marine, jet, electric AWD, adaptive suspension |
| 2 | [Feasibility matrix](02_feasibility_matrix.md) | GREEN/YELLOW/ORANGE/RED, as drawn vs as recommended |
| 3 | [Transformation mechanism](03_transformation_mechanism.md) | three candidates, statics, DOF, actuator sizing, weighted selection |
| 4 | [Corner module](04_corner_module.md) | 14 components, layout, ROAD↔ROBOTIC and ROAD↔SKI sequences, interface loads |
| 5 | [Failure analysis](05_failure_analysis.md) | 19 failures: detection → safe state → mechanical backup → software → recovery |
| 6 | [Safety interlocks](06_safety_interlocks.md) | state machine, gates for every transition, hardware-gated locks |
| 7 | [Drivetrain](07_drivetrain.md) | five architectures compared and selected |
| 8 | [Ski / track system](08_ski_track_system.md) | front ski module, rear cassette, packaging truth |
| 9 | [Marine system](09_marine_system.md) | hydrostatics, hull sizing sweep, swim kit, planing variant |
| 10 | [Structural engineering](10_structural.md) | 14 load cases, materials with welded allowables, joints, FEA/fatigue/test map |
| 11 | [Battery and electrical](11_battery_electrical.md) | sizing from duty cycle, HV architecture, standards map |
| 12 | [Vehicle dynamics](12_vehicle_dynamics.md) | CG, SSF by mode, pitch, yaw, travel, transformation stability |
| 13 | [Manufacturing](13_manufacturing.md) | process comparison, Stages 0–8 with parts, machines, tests, failure criteria |
| 14 | [Outsourcing](14_outsourcing.md) | who makes what |
| 15 | [Patents and IP](15_patents.md) | 44 families, status estimates, FTO review areas (not an FTO opinion) |
| 16 | [Final architecture](16_final_architecture.md) | one recommended architecture, system diagram, mode map |
| 17 | [Redesign](17_redesign.md) | seven "THIS PART SHOULD BE CHANGED" items |
| 18 | [Engineering package](18_engineering_package.md) | risks, unsolved problems, sequence, disciplines, suppliers, tests, DO NOT BUILD YET |
| — | [References](REFERENCES.md) | every source with its verification tag |
| — | [calc/](calc/) | reproducible calculations (`python3 calc/run_all.py`) |

## Reproducing the numbers

```bash
cd docs/feasibility/calc
python3 run_all.py
```

`params.py` holds every assumption with its basis. Change one, re-run, and
the mass budget, mechanism statics, energy, hydrostatics and rollover
figures update together.

## Relationship to the ARC-2 digital twin in this repository

The simulation in `arc2/` models an abstract wheel/leg robot with provisional
dimensions (see `docs/HARDWARE_TRANSITION.md`). This study is the physical
counterpart at rider scale: its corner-module state machine (Part 6) is what
`change_mobility_mode()` would have to confirm "completed" against, and its
Part 5 failure list is the set of `BLOCKED`/`FAILED` outcomes a hardware
backend must report rather than assume.
