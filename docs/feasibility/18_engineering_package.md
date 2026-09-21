# Part 18 — Final engineering package

## 1. Recommended architecture
One central platform (extruded sills + tub + four machined pivot nodes + 4130 rider frame) with four identical corner modules: a trailing arm on a coaxial actuated carrier, spring/damper between arm and carrier, one 48 V self-locking actuator and one spring-applied pin per corner, a carrier-mounted liquid-cooled motor with a CV half-shaft, and a standard hub bolt circle that accepts wheels, ski adapters or track cassettes. 12 kWh class-B pack, four inverters, a separate safety-rated transformation controller. Marine as an optional displacement swim kit now and a separate planing hull variant later (Part 16).

## 2. Why it works
- Every driving load goes through a spring, a pin or a self-locking screw, never through an actuator motor, so the actuators are 6–10 kN purchased units instead of 3 kNm robot joints (Part 3).
- Tie-rod inner joints on the pivot axis make geometry change invisible to steering (Part 3.5).
- The motor rides on the carrier, so half-shaft angles never see the geometry change (Part 7).
- Kits use the interface production kits already use; the vehicle's own actuation replaces the jack (Parts 4, 8).
- Every mode is a set of verified hardware states; locks are held by springs, not software (Part 6).
- Every subsystem has a production precedent; only the combination is new (Part 1).

## 3. Biggest technical risks
1. Pivot cartridge: sealing, bearing life and fatigue at the arm root under 5 g loads with 45° of carrier sweep (no precedent at this load and sweep).
2. Lock sector wear and pin engagement reliability in ice, sand and mud.
3. Rollover margin in HIGH mode (SSF ~0.63 estimated) and rider behaviour at height.
4. Track-kit patent exposure (Camso, Soucy, Polaris families possibly active to 2028–2033).
5. Mass growth: 440 kg is a budget, not a measurement; every 10% adds 8 kg of pack for the same range.
6. Marine variant hydrostatics and swamped flotation with arches cut into the planing surface.

## 4. Biggest unsolved problems
- Validated dynamic load factors for this vehicle class (none exist publicly [IMP-2]); the study's 3 g / 5 g assumptions must be replaced by measurements.
- Kst/Kp compliance in each mode with a rider-active vehicle whose height changes.
- Homologation route: straddle ATV (16 CFR 1420 / ANSI/SVIA 1-2023 [REG-1]) in the US; in the EU either L7e-B1 type approval (≤ 450 kg excluding batteries, ≤ 90 km/h, ≥ 180 mm clearance [REG-3]) or the off-road-only route; the marine variant is excluded from the RCD's mandatory scope [REG-5] and from US federal flotation rules [MST-2], so its safety case is voluntary and must be self-imposed (ISO 12217-3, ISO 13590, ISO 16315).
- Functional-safety framework choice (ISO 26262 vs ISO 13849 vs ISO 25119) depends on that route.
- A snow-mode range of ~38 km on 12 kWh may not satisfy the product promise; a 16–18 kWh option adds ~30–40 kg.

## 5. Prototype sequence
Stage 0 packaging model → 1 single corner on a rig → 2 front + rear modules on a half-chassis → 3 rolling chassis → 4 road prototype (locks pack size and load factors) → 5 robotic/interlock prototype → 6 ski/track prototype → 7 marine (swim kit; variant hull) → 8 integrated pilot-series vehicle (Part 13).

## 6. Required engineering disciplines
Mechanism design and kinematics; structural (FEA, fatigue, welded-joint design); vehicle dynamics and tyre/track/ski mechanics; electric powertrain (motor, inverter, thermal); HV battery and functional safety (BMS, HVIL, IMD, ISO 26262/13849); embedded/safety-rated controls; industrial design and DFM (casting, thermoforming, composites); naval architecture (hydrostatics, planing hulls, ISO 12215/12217); homologation and standards; test engineering.

## 7. Required suppliers
CNC shop; automotive/chassis fabricator; actuator supplier (6–10 kN IP69K CAN); safety-rated controller partner; EV motor/inverter supplier; battery pack integrator with R100/UL 2580 experience; coil-over supplier; track/ski manufacturer (licensed); marine engineering firm and jet-pump supplier; composite/thermoforming shop (Part 14).

## 8. Required testing
Stage-gated (Part 13): actuator/lock rig tests; seal head and freeze tests; bump-steer over the carrier sweep; motor thermal in housing; chassis torsion; static load cases; instrumented drop tests; tilt table (Kst, Kp) in every mode; brake tests to ANSI/SVIA §7; 10,000 transformation cycles with fault injection; pack tests per UN R100/R136 (and UL 2580 seawater immersion for marine); IP spray/immersion and hot-into-cold thermal shock; hitch pull to SAE J684 Class 1; snow 200 km; marine inclining, swamped flotation, retraction afloat; 2,000 km durability.

## 9. Approximate engineering difficulty
| Item | Difficulty | Comparable to |
|---|---|---|
| Road mode on the new platform | moderate | a new electric ATV programme |
| Corner module (mechanism + lock + actuator) | high | an active-suspension corner plus landing-gear lock, at powersports cost |
| Interlock/safety controller | high | brake-by-wire level safety case at a small company |
| Ski/track kits with self-lift | moderate | adapting production kits |
| Swim kit | moderate | Argo-class capability |
| ARC-2B M planing variant | very high | recreating the Gibbs Quadski programme with an electric drivetrain |

## 10. What can realistically be built today
A road-going electric ATV with four self-leveling, height-adjustable corners that lift themselves for tool-free ski and track swaps (Stages 0–6). Every component class exists; the work is integration, validation and safety.

## 11. What should remain future-generation technology
- Onboard stowage/deployment of skis or tracks.
- Walking (leg-like stepping with the wheel used as a foot).
- Planing amphibious operation on the base body; the ARC-2B M variant is a separate programme after the base vehicle is proven.
- Zero-radius tank turns.
- Track-widening pivot geometry for better SSF in HIGH (Gen 2 refinement).

---

## DO NOT BUILD YET — everything requiring validation before fabrication

**Sources and claims**
1. Citation verification pass: every S/B/N-tagged source in `REFERENCES.md` must be read from the original (this environment could not fetch them).
2. Motor, inverter, actuator, pack, coil-over, track, jet and bearing datasheets obtained directly from suppliers (IP ratings, continuous ratings, duty cycles).
3. ANSI/SVIA 1-2023 clauses read (Kst formula, Kp, brake §7), plus EN 15997 and SSCC applicability.
4. Professional patent search with legal-status confirmation for the families in Part 15.3.

**Numbers (all RC-0 assumptions)**
5. Curb mass 440 kg (bottom-up budget, not a measurement).
6. Load factors 3 g bump / 5 g landing / 1.5 g lateral / 1.2 g braking (no public source; replace with drop-test data).
7. Rolling resistance 0.04 (gravel) and 0.12 (tracks on snow); CdA 1.1 m²; 133 Wh/km; 12 kWh pack.
8. Pack-level 150 Wh/kg; 350 V; 96–100s4p.
9. Corner geometry: 450 mm arm, 15°/45°/60° carrier angles, 0.55 motion ratio, 160 mm actuator lever, 5.1 kN lift force.
10. CG heights 0.45 m (vehicle) / 0.58 m (with rider); SSF 0.85 / 0.63; wheelbase shift 0.12 m in HIGH.
11. Hull block coefficient 0.62, bay volume 0.36 m³, sponson sizes, GM estimates, 60–90 kW planing power, 10–12 kWh/h marine energy.
12. Track cassette ground pressure ~6 kPa, 1.6 kN pull per side, 45 km/h cap.

**Components with no precedent at this load/sweep**
13. Pivot cartridge (Ø50 shaft, 150 mm bearing spacing, seals).
14. Lock sector and pin (wear, ice, engagement under residual load).
15. Carrier housing with integrated motor mount and coolant/HV service loops through 45° of sweep.
16. Tie-rod-on-axis steering geometry (bump-steer must be measured < 0.5°).
17. Ski adapter with pivot, pressure spring, limiter strap and switch.
18. Custom track cassette (or the licensed alternative).
19. Transformation controller hardware (speed comparator, dual sensors) and software (state machine, fault injection).
20. Swim-kit sponsons, jet module and bilge integration; marine-variant hull, arch flaps, jet installation.

**Claims that must not be made until tested**
21. Towing capacity (set by J684 tests and vehicle tests, never assumed).
22. Range in any mode.
23. Top speed 60 km/h and 0–60 km/h time.
24. Rollover/stability compliance in HIGH and SNOW.
25. Any "amphibious", "planing" or "seaworthy" claim.
26. Transformation times (8–10 s road↔robotic; 5 min per corner swap).
27. IP67/IP68 immersion of any module.
