# Part 2 — ARC-2B feasibility matrix

Colour key: 🟢 **GREEN** technically mature · 🟡 **YELLOW** possible but difficult · 🟠 **ORANGE** major engineering challenge · 🔴 **RED** currently unrealistic or requires redesign.

Two ratings are given for several rows: **"as drawn"** (the concept boards: fully self-contained deployment, 80–150 kg, ATV envelope) and **"as recommended"** (Parts 16–17: swap-in kits with self-lift, marine as a separate hull variant).

| Feature | As drawn | As recommended | Basis |
|---|---|---|---|
| **Road mode** | 🟢 | 🟢 | Electric ATVs and UTVs are in production [EV-1][SUP-7]; the corner module keeps ATV travel and clearance (Part 4) |
| **Robotic mode** (per-corner ride height, leveling, self-lift, obstacle stepping at walking pace) | 🟠 if it means walking legs (no rider-scale precedent [WL-1][WL-6]) | 🟡 as quasi-static geometry change: 48 V electromechanical corner actuation is production technology on cars [RET-5]; new at ATV scale | Part 3 |
| **Ski mode** | 🟠 skis deploying from inside the front module: packaging of a ~1 m ski beside a 26 in wheel is not shown feasible in the ATV envelope | 🟢 as hub-mounted swap-in skis (production ATV kits [SKI-2]) with vehicle self-lift | Part 8 |
| **Marine mode** | 🔴 the ATV-envelope tub with four wheel bays cannot float the vehicle (Part 9: available volume 0.24 m³ vs 0.61 m³ needed) and cannot plane at ATV power | 🟡 displacement "swim" capability with deployable sponsons (≤ 4 kn); 🟠 planing marine variant with a Quadski-class hull (2.4 × 1.5 m minimum from the sweep, 60–90 kW, 15–25 kWh) | Part 9, `calc/buoyancy.py` |
| **Road → Robotic transition** | 🟡 | 🟡 one actuator per corner, 8–10 s, pins, interlocks (Parts 4, 6) | |
| **Robotic → Road transition** | 🟡 | 🟡 same, with the additional "all corners at 15°" gate | |
| **Road → Ski transition** | 🟠 (onboard deployment) | 🟢 swap-in, ~5 min per corner, no jack | Part 4.5 |
| **Ski → Road transition** | 🟠 | 🟢 | |
| **Road → Marine transition** | 🔴 (no hull) | 🟡 marine variant: proven Gibbs sequence (afloat → confirm thrust → retract) [PAT-41][PAT-42] | Part 6.5 |
| **Marine → Road transition** | 🔴 | 🟡 | |
| **Simultaneous suspension + transformation** | 🟠 if the actuator is in the load path (Option A) | 🟢 by construction in Option C: the spring/damper works at any carrier angle; transformation at ≤ 5 km/h | Part 3 |
| **Waterproofing** | 🟠 sealed wheel bays with doors on a moving arm are an unsolved sealing problem | 🟡 sealed tub + free-flooding arches + one sealed pivot per corner (Gibbs pattern); IP67 motors and IP69K actuators exist [MOT-7][ACT-1] | Parts 4, 9, 11 |
| **Wheel retraction** | 🟡 | 🟡 marine variant only; Gibbs/WaterCar precedent [RET-2][RET-4]; on the base vehicle the arm sweeps only 45° | Part 3 |
| **Track deployment** | 🔴 a 40–50 kg, ~1.1 m cassette cannot be stowed inside an ATV corner with the wheel | 🟢 swap-in cassette on the hub bolt circle (production kits [TRK-1..4]) | Part 8 |
| **Steering** | 🟡 | 🟢 mechanical rack with tie-rod inner joints on the pivot axis (zero height-steer); EPS assist | Part 3.5 |
| **Braking** | 🟢 | 🟢 hydraulic discs at the hub (work with wheels, skis via the hub, tracks via the sprocket) + regen; no braking afloat (reverse bucket) | Part 7 |
| **Drivetrain switching** | 🟠 (mechanical coupling to a stowed track) | 🟢 the hub bolt circle is the coupling; no clutch, no switch | Part 7 |
| **Battery protection** | 🟡 | 🟡 IP67 pack, UN R100 / UL 2580 style tests, HVIL, IMD, thermal propagation design; immersion adds UL 2580 seawater test [HV-5] | Part 11 |
| **Structural strength** | 🟡 | 🟡 conventional space frame with four new pivot nodes; FEA + fatigue + drop tests required (no sourced load factors exist for this vehicle class [IMP-2]) | Part 10 |
| **Rider safety** | 🟠 (rollover at height; unvalidated modes) | 🟡 speed caps by mode, ANSI/SVIA-style Kst/Kp checks in each mode [STB-2], kill cord and seat switch afloat | Part 12 |
| **Towing** | 🟡 | 🟡 chassis-mounted hitch designed to SAE J684 Class 1 loads [TOW-1]; capacity to be set by test, not assumed | Part 10 |
| **Mass target on the boards (80–150 kg)** | 🔴 | — bottom-up estimate 440 kg curb (`calc/mass_budget.py`) | Part 17 |

## 2.1 Reading the matrix

- Nothing in the recommended architecture is RED. Two items are ORANGE only in the planing marine variant.
- The concept as drawn has three REDs (marine hull, track deployment, mass) and they share one cause: the ATV envelope is fixed by the rider, and a 26 in wheel plus a track cassette plus a hull do not fit inside it. Part 17 resolves each with the smallest change that keeps the product idea.
- YELLOW items are yellow because they are new *combinations* of proven parts, not because any part is unproven. Their risk is integration and validation effort, which Part 18 quantifies.
