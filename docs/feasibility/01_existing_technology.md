# Part 1 — Existing technology

Reference keys in brackets point to `REFERENCES.md`, which states for each source whether it was fetched (F/D/M/P), seen only as a search snippet (S), or is a standard/textbook whose clause was not read (B). **Read the verification note at the top of `REFERENCES.md` before quoting any number externally.**

Classification used in the last column:
**PROVEN** = in series production for years with public engineering data · **COMMERCIAL** = sold, but niche or recently · **PROTOTYPE** = demonstrated by a research group or as a concept · **ASSUMPTION** = an engineering inference made in this study · **UNVALIDATED** = a concept with no demonstration found.

## 1.1 Wheel-leg transformation

| Technology | Existing example | What has actually been demonstrated | Limitations | Relevance to ARC-2B |
|---|---|---|---|---|
| Wheel-on-leg quadruped, hybrid walking/driving | ETH Zurich / Swiss-Mile wheeled ANYmal [WL-3][WL-4] | ~50 kg robot, 22 km/h, ~50 kg payload, RL-controlled walk/drive transitions, >10 km urban treks; joints limited to 80 N·m [F] | Robot mass class; joint torque an order of magnitude below a rider-carrying vehicle's corner loads | PROTOTYPE. Proves control of hybrid modes; does not prove actuators at vehicle scale |
| Wheel-leg quadruped, commercial | Unitree B2-W [WL-10] | ~75–78 kg (URDF sum) with 320 N·m knee joints, 20 N·m wheel motors [F]; IP67 claimed [S]; wheel module adds ≈ 2.8 kg per leg | Payload ~40 kg; wheel drive small; not a vehicle | COMMERCIAL (robotics). Best public mass/torque dataset for scaling |
| Rider-scale "walking car" | Hyundai Elevate concept (2019); TIGER X-1 (2021) [WL-1] | Elevate: show model. TIGER X-1: ~26 lb uncrewed platform | No rider-carrying walking car has been built | PROTOTYPE / UNVALIDATED at rider scale. The concept boards' "robotic mode" imagery descends from this |
| Six-limb wheel-on-limb heavy platform | NASA JPL ATHLETE [WL-6] | ~850 kg, 300 kg payload, wheels become feet, ~10 km/h | 36 limb joints, slow, research | PROTOTYPE. Only wheel-on-limb machine at ARC-2B mass; shows the joint count that true walking costs |
| Rideable walking machine | Mantis hexapod [WL-13] | 1,900 kg diesel-hydraulic hexapod carries a person at ~1 km/h | no wheels; hydraulic | PROTOTYPE. The only verified human-riding walking machine |
| Wheel-to-leg morphing wheel | NTU Quattroped / TurboQuad [WL-7]; Sarcos US 7,017,687 [PAT-1] | rim splits into legs; same motors for both modes | not tyre-compatible; small | PROTOTYPE. Not applicable to pneumatic tyres |
| Four-bar / five-bar leg with base-mounted actuators | Ascento [WL-5]; Tencent Ollie [WL-9] | one hip actuator gives 31–66 cm body height; five-bar with both motors at the base | small; balancing bipeds | PROTOTYPE. Confirms "actuators at the base, passive links outboard" as the mass-efficient pattern |
| Rider-carrying articulated-arm electric 4-wheeler | Swincar e-Spider [WL-14] | ~200 kg, 4 in-wheel motors 4.16 kW cont / 10 kW peak, long-travel independent arms with pendular (passive) body | articulation is passive, not actuated | COMMERCIAL. The closest product to ARC-2B's road/terrain character; shows 4-hub-motor + long-arm packaging works at 200 kg |
| Independent per-corner ride height (electric, production) | Audi predictive active suspension [RET-5][LV-2]; DDT TITA (0.1–0.3 m height) [WL-12] | Audi: 48 V rotary electromechanical actuator, ~1,100 N·m per wheel, ±85 mm in 0.5 s, 10–200 W | Audi is a passenger car (2 t) | PROVEN (car); COMMERCIAL (robot). Establishes that 48 V electromechanical actuation of corner geometry is production technology |

## 1.2 Wheel retraction

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Hydraulic retraction of a complete suspension corner above the waterline | Gibbs Quadski / Aquada [AMP-1][AMP-2][RET-2][PAT-6][PAT-29] | ≤ 5 s retraction at a button press; retraction hydraulics isolated from the ride springs/dampers; ~1,000 Quadskis built 2012–16 | Quadski 605 kg, 3.26 m long, 100 kW; production ceased | PROVEN (low volume). The pattern to copy: actuator moves the suspension mount, not the wheel via the spring |
| Hydraulic retraction into open wells with closing flaps | WaterCar Panther [AMP-4][PAT-9] | 8–15 s retraction on a 1,338 kg vehicle; flaps close the hull cut-outs | large, petrol; WaterCar patent possibly active to ~2029 | COMMERCIAL (hand-built). Flap concept relevant to hull drag |
| Retracting driven wheels on a boat | Sealegs [AMP-6][PAT-8] | hydraulic legs pivoted above the waterline, ~600 kg system | heavy; boat-first | COMMERCIAL. Shows the mass cost of hydraulic land drive on a hull |
| Over-centre locks and lock-stays | FAA landing gear practice [RET-1]; Hamilton Sundstrand EMA patents [PAT-12] | universal aviation practice; electromechanical retract actuators with brakes and jam-tolerant unlocks | aviation cost | PROVEN. Source of the "load through the lock, not the actuator" rule |

## 1.3 Ski conversion

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Hub-mounted ATV ski kits | Diamond J ATSki and similar [SKI-2] | skis bolt to the ATV hub bolt circle with the stock lug nuts; ~1 h install; suitable for packed snow; deep snow needs rear tracks | limited flotation; steering geometry unchanged | COMMERCIAL. The exact interface ARC-2B adopts for the front kit |
| Snow-bike front ski | Timbersled ARO [SKI-1][PAT-22] | 7.25 kg front ski kit; 48 kg rear track kit; Polaris-owned since 2015 [SUP-8] | replaces the wheel entirely | COMMERCIAL. Mass benchmarks for ski and cassette |
| Snowmobile ski/spindle systems | BRP, Polaris (spindle patents expired) [PAT-17] | decades of production | — | PROVEN. Ski saddle, carbide runner, limiter strap designs are commodity |

## 1.4 Track conversion

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Bolt-on ATV/UTV track cassettes on the hub bolt circle | Camso Tatou 4S / UTV 4S1 [TRK-1]; Polaris Prospector Pro [TRK-2]; Can-Am Apache 360/Backcountry [TRK-3]; Mattracks LiteFoot [TRK-4] | production for two decades; ~97 lb per track (Prospector, likely per track); +7 in to ~16 in clearance; 1,716–2,830 in² contact; 0.44 psi (Backcountry) | 1–2 h install with a jack; speed limits and drivetrain load statements not retrieved; Camso/Soucy patents possibly active to 2028–2033 [PAT-19][PAT-20] | PROVEN. Drive coupling through the hub, anti-rotation link to the suspension, idler-based tension: all commodity |
| Cassette with internal suspension | Soucy US 8,851,581 [PAT-20] | patented; product lines exist | possibly active patent | COMMERCIAL |
| Snowmobile rear suspension/track | Ski-Doo / Polaris [SNO-1][SNO-2][SNO-3] | rail slide suspension; tension 7.3 kg → 32–50 mm deflection; pitch 2.86/3.0 in; widths 14–20 in | long (1.2–1.5 m) | PROVEN. Not packageable on an ATV corner; ATV cassettes are the right family |
| Retracting tracks into hull enclosures | Berardi US 5,181,478 (expired) [PAT-11] | patent only | no product | UNVALIDATED |

## 1.5 Marine conversion

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Planing amphibious ATV | Gibbs Quadski [AMP-1][PAT-29] | 605 kg, 100 kW on water, 72 km/h land and water, hull 3.26 × 1.59 m, deadrise ≥ 10° | production ceased; 5× the power and 1.6× the length of an ATV | PROVEN at low volume. Sets the physical scale a planing amphibian needs |
| Displacement amphibious ATV | Argo 8×8 [AMP-9]; Amphicar [AMP-5] | Argo: tyre-paddle propulsion ~5 km/h; Amphicar: 32 kW props, ~7 mph | slow | PROVEN. Shows what "swim mode" without planing looks like |
| Amphibious hydrodynamics | Ocean Eng. 2021/2020 papers [AMP-10] | exposed wheels raise resistance 14–28%; wheel-well flaps reduce drag | — | Research. Justifies full retraction and flaps for any planing variant |

## 1.6 Water jet

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| PWC axial-flow jet pump | Sea-Doo / Yamaha 155–160 mm pumps [JET-3]; iBR reverse bucket [JET-4][PAT-30] | millions of units; 100–200 kW through a 155–160 mm pump; bucket gives neutral/reverse/braking | ~40% propulsive efficiency at ~16 kn vs ~65% for a propeller [JET-1] | PROVEN. Right size class; electric drive changes nothing hydrodynamically |
| Electric jet PWC | Taiga Orca [JET-5][BAT-2]; Narke GT95 [JET-6] | Orca up to 120 kW, ~2 h claimed, 23 kWh, 355 V pack ~125 kg "IP68"; Narke 71 kW / 24 kWh / ~2 h / 50 km | 2-hour endurance needs ~24 kWh | COMMERCIAL. Energy budget benchmark: 10–12 kWh per hour of mixed jet use |
| Small electric jet module | ZeroJet [JET-7] | 14–30 kW, 48 V modules, ~20 kg motor | tender-scale, ~23 mph on a small tender | COMMERCIAL. Candidate for a displacement "swim mode" |
| Amphibian-specific jet packaging | Gibbs US 2006/0264126 (term ended) [PAT-26] | thrust/intake-length ≥ 18 kN/m to plane despite open arches | — | Design guidance now in the public domain |

## 1.7 Electric AWD

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Electric UTV | Polaris Ranger XP Kinetic [EV-1][SUP-7] | 29.8 kWh, 110 hp, 1,754 lb dry, 2,500 lb tow, $37,499 | heavy (800 kg) | PROVEN. Shows the mass/energy scale of an electric utility powersports vehicle |
| Electric ATV | Can-Am Outlander Electric [SUP-7] | 8.9 kWh, $12,999, 3 regen levels | — | PROVEN. Closest electric ATV comparable |
| Electric snowmobile | Taiga Nomad [EV-2]; Ski-Doo Grand Touring Electric [EV-3] | 23 kWh, 90–120 hp, < 600 lb, 60–87 mi claimed; 120 kW peak and CCS on 2027 gen | range | PROVEN (low volume). Snow-mode energy benchmark |
| In-wheel motors (car) | Protean Pd16/Pd18 [MOT-1]; Elaphe S400/M700/L1500 [MOT-2] | Pd16 28 kg / 40 kW peak; S400 17.6 kg / 40 kW peak / 400 Nm | 18–39 kg unsprung per corner; 15–19 in rims | PROVEN (car). Too heavy per corner for a 440 kg ATV (Part 7) |
| In-wheel motors (light vehicle) | Swincar 4 × 10 kW peak [WL-14]; QS273 8 kW / 18 kg [MOT-6] | 200 kg vehicle | limited torque without reduction | COMMERCIAL |
| Inboard axial-flux motors | EMRAX 188/228 [MOT-4]; YASA P400 [MOT-3] | 188: 7.9 kg, 37 kW cont; 228: 13.5 kg, 55–75 kW cont | IP rating not seen; need reduction | COMMERCIAL. Candidate carrier-mounted motors |
| Quad-motor torque vectoring / low range | Rivian; Mercedes G 580 (4 × 108 kW, per-motor 2-speed 1:11 / 1:21) [TV-1] | production | cost | PROVEN. G 580's per-motor 2-speed is the closest analogue to a "track/robotic low range" |
| Unsprung mass effect | Lotus/Protean study [UNS-1]; Wu et al. 2025 [UNS-2] | +30 kg per wheel on a 2 t car "noticeable", largely recoverable with damping; heavier unsprung mass raises wheel dynamic load and travel | car-scale study | Research. On a 440 kg vehicle the ratio is far worse (Part 7) |

## 1.8 Adaptive suspension

| Technology | Existing example | Demonstrated | Limitations | Relevance |
|---|---|---|---|---|
| Semi-active damping (powersports) | Polaris Dynamix / Fox Live Valve; Can-Am Smart-Shox [RET-8] | 200 Hz sensing, ~17 ms valve response; damping only | no height control | PROVEN. Should be the ARC-2B damper technology in ROAD |
| Electromechanical active/height suspension | Audi eAWS [RET-5][LV-2] | 48 V, 1,100 N·m, ±85 mm in 0.5 s | passenger car | PROVEN |
| Hydraulic active | Mercedes E-ABC [RET-6]; ClearMotion [RET-7] | production | hydraulic power unit mass | PROVEN |
| Linear electromagnetic active | Bose Project Sound [RET-7] | prototypes | abandoned for mass and cost | PROTOTYPE. Argues against direct linear EM actuation |
| Hydropneumatic retraction/height on an amphibian | Gibbs US 2005/0034911 [PAT-7] | gas accumulators, height-sensor gating | term ended | PROVEN pattern, now public |

## 1.9 What this survey establishes

1. **Every ARC-2B mode exists somewhere, but never together and never at ATV mass.** Road (ATV), articulated corners (Swincar, Audi), retraction (Gibbs), ski/track (Camso, Timbersled), planing amphibian (Quadski) are each PROVEN or COMMERCIAL individually.
2. **No rider-carrying actuated wheel-leg vehicle has been demonstrated.** The "robotic mode" must therefore be scoped as articulated geometry change (proven) rather than walking (unproven).
3. **The planing amphibian precedent is 1.6× longer and ~5× more powerful than an ATV.** That is the central conflict addressed in Parts 9 and 17.
4. **Track and ski kits are hub-interface products.** No production system stows a track inside a wheel module.
