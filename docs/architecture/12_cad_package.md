# 12 — CAD master package

All models in the vehicle body frame of Section 2 (origin at the ground under the wheelbase midpoint, ROAD static; +X forward, +Y left, +Z up). Each item lists what the drawing must show and which calculation it must agree with.

## A — Master vehicle
| # | Drawing | Must show | Agrees with |
|---|---|---|---|
| 1 | Side (left) | wheel centres (±0.650, 0.330); pivot axes (±0.161, 0.434); arch openings X +0.29…+0.99 / −0.99…−0.29; fender crown Z ≥ 0.83; footboard X −0.25…+0.23 at Z 0.42; seat Z 0.88; grips (+0.28, 1.16); nose X +1.00…+1.05; rack −1.10; hitch (−1.05, 0.35); ground clearance 0.28 | `calc/kinematics.py` sweep table |
| 2 | Front | track 0.98; tyre faces ±0.615; overall width 1.24; light bar 620 × 28 at Z 0.86, fascia rake 16°; carriers visible below the fascia | Section 1 |
| 3 | Rear | tail light 500 mm at Z 0.84; hitch receiver; carrier discs; cassette envelope to X −1.15 when fitted | |
| 4 | Top | sills Y ±0.30; nodes at X ±0.161; battery X −0.50…+0.40, Y ±0.25; inverters under the seat; radiator in the nose; rack | Section 2 table |
| 5 | Bottom | tub floor X ±0.55 at Z 0.28; skid; node plates; arch liners; drains | |
| 6 | Isometric | ROAD and HIGH side by side (wheels dropped 0.204 m, inward 0.095 m) | |

## B — Chassis
| 7 | Bare chassis | sills, four cross-members (X −0.75, −0.35, +0.35, +0.75), floor, four nodes, rider frame feet; bolt patterns | Section 4 |
| 8 | Chassis section at X = +0.161 (through the front nodes) | sill 120 × 60 × 4; node 160 × 160 × 120 on the outer sill face; pivot bearing span Y 0.265–0.415; battery tray inboard; floor at Z 0.28 | Section 6.5 collision check |
| 9 | Battery packaging | tray 0.90 × 0.50 × 0.18 m, 4 bolts + 2 shear pins from below, MSD position, HV exits, vent, float switch, cold plate/heater | Section 11 of the feasibility study |
| 10 | Corner mounting structure | node detail: 8 × M12 pattern, 2 dowels, bearing bores (Ø, tolerance ±0.05), sector seat, actuator anchor, hard-stop blocks at −2°/+55°, cable/coolant bulkhead position | |

## C — Front corner module (leading arm)
| 11 | Exploded view | carrier, pivot shaft, two bearing pairs, arm with root boss, knuckle, hub, half-shaft, motor + 6:1 + inboard disc + caliper, coil-over, actuator, lever, pin, solenoid, sector insert, sensors, disc cover, seals | Section 5.2 |
| 12 | Assembly | as installed at ROAD, carrier 12° | |
| 13 | Section through the pivot axis | concentric rotations: arm on shaft, shaft in carrier bearings, carrier in node bearings; seal stack; grease purge | |
| 14 | Road position | arm 12°; tie-rod inner joint ON the axis at Y 0.26; tie-rod 439 mm; knuckle arm 120 mm at 20.7°; KPI 8°, caster 5° | `calc/steering.py` |
| 15 | Robotic position | carrier 38°; wheel (+0.555, 0.126); actuator extended 72 mm; pin in the 38° slot; tie-rod unchanged | |
| 16 | Ski position | carrier 12° (and 20° deep-snow); wheel removed; adapter plate on the 4 studs; ski pivot pin, pressure spring, limiter strap + switch; ski 1.10 × 0.22 | Section 7.3 |

## D — Rear corner module (trailing arm)
| 17 | Exploded view | as 11 without the knuckle; fixed hub carrier; parking-brake lever; 2-speed dog clutch; arm hardpoint for the cassette anti-rotation link at 0.30 m from the hub | |
| 18 | Road | carrier 12°; wheel (−0.650, 0.330) | |
| 19 | Robotic | carrier 38°; wheel (−0.555, 0.126) | |
| 20 | Track deployed | carrier 25°; cassette on the 4 studs: sprocket r 150 mm, 13 T; idlers; walking beam; tensioner + indicator switch; anti-rotation link; cassette envelope X to −1.15 | `calc/ski_track.py` |

## E — Transformation
| 21 | ROAD → ROBOTIC | 5-frame side view, all four corners; carrier angles 12/18/25/32/38°; body rise 0/0.05/0.10/0.15/0.204; wheel-centre path arcs about the pivots; pin states | Section 6.7 A |
| 22 | ROBOTIC → ROAD | reverse | |
| 23 | ROAD → SKI | per corner: LIFT to 50° (body corner rises 0.28 m, arm to full rebound), wheel off, adapter on, lower to 12° (front) / 25° (rear); the removed wheel drawn outside the vehicle | Section 6.3 |
| 24 | SKI → ROAD | reverse | |

## F — Marine (ARC-2B M variant and the removable hull)
| 25 | Land version | base vehicle with swim kit stowed (sponsons in the sills) | Section 8 |
| 26 | Marine variant | 2.8 × 1.5 (1.6) m hull under ARC-2B panels; sheer at Z 0.55; wheels at −50° (+0.482, 0.817); flaps | |
| 27 | Hull section at the front axle | tub, arch, hull flap, pivot cartridge through the tub side, waterline Z 0.28, tyre bottom Z 0.49 | Section 6.5 sketch |
| 28 | Wheel bay | free-flooding arch, flap hinge on the hull, scuppers, liner | |
| 29 | Jet propulsion | 155–160 mm pump, intake grate in the aft pad, motor, nozzle ±25°, reverse bucket, cooling loop | |
| 29b | Removable hull ("dock") | 3.2 × 1.8 × 0.6 m hull, bow ramp, cradle, hitch-pin lock, four dry wells, jet module, HV umbilical | Section 8.2 |

## G — Engineering
| 30 | Load paths | the seven paths of Section 4.3 drawn on the side/top views with arrows and magnitudes for case 3 (7.8 kN) | Section 4.3 |
| 31 | Actuator loads | force vs carrier angle curve (max 6.8 kN at 12°), stroke 104 mm, lever 160 mm, off-perpendicular ≤ 25° | `calc/kinematics.py` |
| 32 | Lock loads | pin Ø20 double shear at 25.5 kN (5 g), sector 150 mm radius, 5° slots, hard stops | |
| 33 | Steering geometry | rack on the axis line; tie-rod length invariance proof table; Ackermann 32°/42°; turning radius 2.45 m | `calc/steering.py` |
| 34 | Suspension geometry | side-view IC at the pivot; anti-dive 30% (inboard brakes) vs 125% (hub brakes); anti-squat 28%; roll centre at ground; motion ratio 0.55; spring 43 N/mm | |
| 35 | Transformation envelope | union of the tyre envelopes for all states (Section 2.3), the arch liner cut line, the footboard leading-edge limit X +0.237, fender crown Z 0.83, node clearance in LIFT/RETRACT (≥ 0.10 m) | Section 6.5 |

## Master geometry table (dimensioned)

| Parameter | Target | Status |
|---|---:|---|
| Length | 2.15 m | Engineering (nose ≥ +1.00 forced) |
| Width | 1.24 m | Engineering |
| Height (grips) | 1.16 m | TBD (ergonomics rig) |
| Wheelbase ROAD / HIGH | 1.30 / 1.11 m | Engineering / Calculation |
| Wheel Ø | 0.66 m (26 in) | Engineering |
| Track width F / R | 0.98 / 0.98 m | Engineering |
| Ground clearance ROAD / HIGH | 0.28 / 0.484 m | Engineering / Calculation |
| Curb mass | 487 kg | Calculation |
| Payload | 150 kg | Requirement |
| Actuator stroke / force | 104 mm / 6.8 kN | Calculation |
| Wheel travel | 0.22 m | Engineering |
| Arm length | 0.50 m | Engineering |
| Carrier angles | 12 / 38 / 50 / (−50) ° | Engineering |
| Pin shear (5 g) | 25.5 kN | Calculation |
| Pivot bearing radial (5 g) | ≈ 13 kN each | Calculation |
| Battery | 12 kWh, 81 L, 78 kg | Calculation |
| Motor | 4 × 8–10 kW cont., 6:1 (+12:1 rear) | Engineering |
| Tie-rod length | 439 mm | Calculation |
| Turning radius | 2.45 m | Calculation |
| SSF ROAD / HIGH | 0.82 / 0.61 | Calculation (CG TBD) |
| Ski | 1.10 × 0.22 m | Engineering (TBD by test) |
| Track | 1.10 × 0.30 m, 72.6 mm pitch | Engineering |
