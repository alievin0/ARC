# Part 12 — Vehicle dynamics

All numbers are RC-0 derived (`calc/rollover.py`, `calc/mechanism_statics.py`) unless a reference key is given.

## 12.1 Centre of gravity

| Configuration | Vehicle CG height (assumption) | Combined CG with 100 kg rider (rider CG at seat + 0.25 m) | Note |
|---|---|---|---|
| ROAD | 0.45 m (battery on the floor) | **0.58 m** | ATV benchmarks are not public; the CPSC/SEA work measured them but numbers were not retrievable [STB-4] |
| ROBOTIC high (+0.20 m) | 0.65 m | **0.78 m** | rider rises with the body |
| SNOW (tracks +0.06 m, +90 kg low) | 0.51 m | **0.62 m** | cassettes add low mass |
| MARINE variant afloat, wheels up | ~0.75 m above keel | — | Part 9 |

Longitudinal: 45/55 front/rear static with rider (rider seated over the rear third); the body shifts 0.12 m rearward relative to the wheels in HIGH (Part 3), moving the split to ~40/60. Acceptable at ≤ 25 km/h; it is why HIGH is speed-capped.

## 12.2 Roll stability

Static stability factor SSF = T/(2h) [DYN-5][STB-1]:

| Mode | Track | h | SSF |
|---|---|---|---|
| ROAD | 0.98 m | 0.58 m | **0.85** |
| ROBOTIC high | 0.98 m | 0.78 m | **0.63** |
| ROBOTIC high with the arm geometry widening the track 0.15 m (not in RC-0; possible with a small toe-out of the pivot axes) | 1.13 m | 0.78 m | 0.73 |
| SNOW | 1.03 m | 0.62 m | **0.83** |

For scale: NHTSA rates passenger cars from SSF 1.04 (1 star) to 1.45 (5 stars) [STB-1]. ATVs live far below that and rely on the rider's weight shift (rider-active vehicle), which is why ANSI/SVIA 1 uses an unoccupied lateral stability coefficient Kst ≥ 1.0 and pitch coefficient Kp > 1.0 [STB-2] rather than SSF, and ROHVA uses tilt-table angles of 24°/30° and a J-turn [STB-3]. The Kst formula was not retrievable; the vehicle must be measured on a tilt table in each mode (the UNSW quad-bike work found stability "primarily a function of track width and CoG" [STB-5]).

**Consequences built into the design**
- HIGH mode is 25% worse than ROAD in SSF; hence the 25 km/h cap and the ESC "high" map (torque limiting when lateral acceleration exceeds 0.35 g).
- Per-corner leveling on a side slope (raising the downhill corners) restores the body to level and *improves* the effective stability on slopes up to ~10°, which is the genuine dynamic benefit of ROBOTIC mode.
- A future track-widening geometry (pivot axes toed out ~8° so that carrier rotation moves the wheels outboard) would recover most of the loss; noted as a Gen-2 refinement, not in RC-0.

## 12.3 Pitch stability

Wheelbase 1.30 m, CG 0.58 m → static pitch-over angle = atan(0.65/0.58) ≈ 48° uphill with a 50/50 split; with the actual 45/55 split and a rider leaning forward it is above 40°, beyond the traction limit (31° at μ 0.6). In HIGH: atan(0.65/0.78) ≈ 40° with a rearward shift; the interlock refuses HIGH above 10° slope for the transformation itself, and the ESC pitch limit is set at 25° in HIGH. Kp > 1.0 (ANSI/SVIA) is to be verified by tilt table [STB-2].

## 12.4 Yaw

Four independent motors give per-wheel torque vectoring at ≥ 100 Hz (Rivian/Rimac practice [TV-1]); with the trailing-arm rear there is no rear steer. Rear-biased torque in ROAD, symmetric in ROBOTIC, rear-only propulsion in SNOW (skis have no drive). Zero-radius "tank turn" is not offered: Rivian withdrew it for surface damage and mixed-μ instability [WL-15].

## 12.5 Suspension travel and rates

| Parameter | Value | Basis |
|---|---|---|
| Wheel travel | 0.22 m at any carrier angle | ATV class 0.19–0.24 m [ATV-1..3] |
| Ride frequency target | 1.5 Hz sprung | ATV/UTV practice |
| Wheel rate | ~13 N/mm (147 kg corner) | derived |
| Spring rate at 0.55 motion ratio | ~43 N/mm | derived (K_s = K_w / MR² [DYN-5]) |
| Damper | semi-active (Live Valve class) in ROAD; firm in HIGH and SNOW | [RET-8] |
| Anti-squat / anti-dive | trailing arm with pivot ~0.35 m above ground and 0.45 m ahead of the rear wheel gives ~40% anti-squat at ROAD angle; it rises with carrier angle (pivot effectively higher), which is acceptable at the lower HIGH speeds | side-view geometry [DYN-5] |
| Trailing-arm front | wheel moves rearward on bump (like a telescopic fork); accepted compromise (Part 3) | |

## 12.6 Wheel load distribution and cross-axle

Independent corner height makes the vehicle statically indeterminate in HIGH; the controller equalises wheel loads using the arm sensors as load proxies (spring deflection × wheel rate). One-wheel-airborne detection (Part 5) uses the same signal.

## 12.7 Braking and acceleration

Braking 1.2 g design case is above what an ATV achieves on dirt (~0.6–0.8 g); brake proportioning 70/30 front/rear plus regen up to 0.3 g blended. Acceleration 0–60 km/h in ~6 s (34 kW at the wheels) is traction-limited on loose surfaces before it is power-limited. ANSI/SVIA 1-2023 §7 stopping distances are to be met and were not read in this study [BRK-1].

## 12.8 Rollover risk during transformation

During ROAD ↔ ROBOTIC all four corners move together, so the body stays parallel to the ground; CG rises 0.20 m in ~8 s at ≤ 5 km/h. On the 10° maximum slope permitted, the lateral acceleration is 0.17 g, far below the 0.63 SSF of the final state. Single-corner LIFT tilts the body by up to atan(0.3/0.98) ≈ 17° with the vehicle stationary and parked; the CG projection stays inside the three-wheel support triangle for the rider seated centrally (checked geometrically for RC-0; must be re-checked with the actual CG).

## 12.9 Track mode

Tracks add 90 kg low, raise the vehicle 60 mm and widen the stance 50 mm; SSF stays ~0.83. Ski/track dynamics (ski pressure, track slip) are governed by the same corner geometry and the carrier angles set by the interlock. Snow friction is low (compacted snow μ 0.12–0.18 is a blog-grade figure [TER-4]); the ESC snow map limits yaw demand accordingly. Kst with unequal front/rear "track widths" is exactly the case ROHVA chose Kst over SSF for [STD-2].

## 12.10 Ski mode

Front skis on the standard knuckles keep caster and Ackermann; steering effort rises (EPS map); the ski pivot's limiter strap sets ski pressure. Speed cap 45 km/h.

## 12.11 Marine stability

Part 9: base vehicle with sponsons GM ≈ +1.0 m (0.4 m sponsons); marine variant hull GM ≈ +0.3–0.5 m; rider lean of 100 kg × 0.5 m gives ~12° heel at rest on the variant hull. Planing dynamics (porpoising, chine walking) are a tank/lake test matter.

## 12.12 Can the rider position stay the same in every mode? Yes, with caveats

The rider sits in the same seat at the same height relative to the chassis in every mode; the chassis moves relative to the ground. Caveats: in HIGH the rider is 0.20 m higher above the ground and speed is capped; in SNOW the footboards are 60 mm higher; in the marine variant the seat is 0.2 m higher above the keel than an equivalent PWC seat because the wheels and arches occupy the lower hull, which is why beam must grow to 1.5 m for stability. No mode requires the rider to move.
