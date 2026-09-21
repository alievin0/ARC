# 7 — Modes: ROAD, ROBOTIC, SKI

## 7.1 ROAD mode (full definition)

| Parameter | Value | Status |
|---|---|---|
| Wheel positions | front (+0.650, ±0.490, 0.330), rear (−0.650, ±0.490, 0.330) | DERIVED |
| Carrier angle | 12° all corners, pinned | TARGET |
| Suspension travel | 0.22 m (0.12 bump / 0.10 droop) about ride height | TARGET |
| Ground clearance | 0.28 m (tub floor) | TARGET |
| Ride height | body reference Z 0 = ground at static | — |
| Steering angle | outer 32° / inner 42°; turning radius 2.45 m | TARGET / DERIVED |
| Wheel camber | 0° static; camber change = body roll (transverse pivot axes) | DERIVED |
| Toe | front 0 to +2 mm toe-in (TBD on the ride rig); rear fixed 0 | TARGET |
| Roll centre | ground level, front and rear (pure trailing/leading arms); roll stiffness comes from spring rate and track only | DERIVED |
| Centre of gravity | 0.60 m with rider (TARGET, to be measured); 45/55 front/rear | TARGET |
| Brake geometry | inboard discs on the carriers; anti-dive 30% with 65% front bias | DERIVED |
| Drive geometry | carrier-mounted motors; anti-squat 28% with 60% rear bias | DERIVED |
| Ride frequency | ~1.5 Hz; spring 43 N/mm at motion ratio 0.55 | TARGET |
| Speed | 60 km/h design; traction-limited launch 0.6 g; 37 kW at the wheels for 0–60 in 6 s | TARGET / DERIVED |

**Why this state suits speed.** It is the longest wheelbase (1.30 m), the lowest CG (0.60 m), the highest SSF (0.82), the geometry with the smallest wheel-centre longitudinal motion over travel (±0.02 m), and the only state in which the pins sit in the slots designed for 5 g (12° slot is the hardened, fatigue-tested one). It is also the state with no compromise from carrier angle: motor, half-shaft, coil-over and tie-rod are all at their design angles.

**Known compromise.** No camber gain and a ground-level roll centre mean the outer tyre cambers positive by the roll angle in a corner (4° roll → 4° positive camber). ATV swingarm rears live with this; ATV fronts do not. Mitigation in V0: firm springs (1.5 Hz), semi-active damping, tyre choice; Gen-2 option: inclined pivot axes (semi-trailing) for camber gain, which couples camber to carrier angle (~0.3–0.5° per degree) and must then be corrected in the HIGH map.

## 7.2 ROBOTIC mode (articulated geometry, not legs)

| Capability | Mechanism | Limit (V0) |
|---|---|---|
| Wheel extension / retraction (relative to the body) | carrier 12°…50° per corner | +0.279 m extension; no retraction on the base vehicle |
| Independent corner height | four carriers, pinned every 5° | ±0.20 m relative difference between any two corners before the arm-travel band is exhausted |
| Body leveling | controller sets carrier angles from IMU roll/pitch | levels on slopes up to ~12° cross-slope and ~15° fore-aft at HIGH; beyond that the low corners run out of upward travel |
| Wheel articulation | each wheel follows terrain with 0.22 m of passive travel at any carrier angle | no active wheel placement while rolling faster than 5 km/h |
| Obstacle climbing | lift the approaching corner 0.15–0.25 m before contact (front leading arm also moves the wheel forward-and-up on bump, which helps) | step ≤ 0.30 m at ≤ 5 km/h (tyre radius 0.33 + carrier lift); higher steps need the "self-lift then roll" sequence below |
| Rock traversal | HIGH (0.48 m clearance) + per-corner leveling; the tub floor is the lowest point | rocks ≤ 0.45 m between the wheels |
| Wheel-unloading prevention | arm sensors give a load proxy; the controller lowers a corner whose arm is at full rebound | works up to the carrier limit (50°) |
| Anti-tip | ESC "high" map: lateral acceleration ≤ 0.35 g at HIGH (SSF 0.61); pitch limit 25°; refuse HIGH transformation above 10° slope | speed cap 25 km/h pinned, 5 km/h with any pin out |

**How the vehicle handles a hole (one wheel drops):** the arm of that corner droops to full rebound (sensor); the controller lowers that carrier by up to +12° (5° steps) to regain contact if speed ≤ 5 km/h, then re-raises it as the wheel climbs out. If speed > 5 km/h it does nothing: the passive suspension handles it and the three loaded wheels keep the vehicle stable (pins in).

**How it handles a rock in front of one wheel:** at ≤ 5 km/h, the controller raises the body on that corner by lowering... no: it *raises the wheel* by rotating that carrier toward 12° (less extension) so the wheel meets the rock higher on its radius, while the other three carriers stay at 38°; the front leading arm then lets the wheel move up-and-forward over the rock on its own travel. After the rock, the carrier returns to 38°. Maximum "wheel lift" relative to the other three: 0.204 m.

**Uneven terrain (cross-axle):** leveling holds the body within ±3° while the four carriers differ by up to 26°; the CG stays inside the support polygon because all four wheels remain loaded (the controller never lifts a wheel above 5 km/h).

**Limits of motion** (from the hard stops and the travel band): carrier −2° to +55°; arm relative to carrier −14° (bump stop) to +24° (rebound strap); the intersection of the two, plus the pins' 5° pitch, is the reachable set. Anything outside is refused by the interlock and blocked by the stops.

## 7.3 SKI mode (designed as a real vehicle)

| Item | Value | Status | Basis |
|---|---|---|---|
| Front ski dimensions | 1.10 m long × 0.22 m wide, 40 mm deep keel, tip rise 0.15 m | TARGET | `calc/ski_track.py` pressure 6.7 kPa per ski; snowmobile skis run ~3–5 kPa, so this is the upper edge and may need 0.25 m width |
| Ski material | UHMW-PE moulded body over an aluminium spine; steel keel with a carbide runner insert (0.25 m long) | TARGET | commodity snowmobile construction |
| Ski pivot | Ø20 pin on the hub adapter plate, ±25° pitch freedom, polymer bushings; rubber ski-pressure spring; limiter strap with switch | TARGET | |
| Ski suspension | the corner coil-over (unchanged); carrier 12° nominal, 20° for deep snow | TARGET | |
| Rear track width | 0.30 m | TARGET | |
| Track length (ground contact) | 1.10 m; cassette overall 1.30 m | TARGET | |
| Track pitch | 72.6 mm (2.86 in family) | TARGET | [SNO-3] |
| Lug geometry | 30 mm lugs, staggered, with internal guide horns (anti-derail) | TARGET | [PAT-21] |
| Drive sprocket | 13 teeth, 150 mm radius, positive drive | DERIVED | |
| Track tension | 70 N mid-span → 25–35 mm deflection; spring-loaded rear idler + screw adjuster; indicator switch | TARGET | snowmobile practice [SNO-1][SNO-2] |
| Drive ratio | rear 12:1 (crawl) in SNOW; 6:1 gives only 210 Nm at the hub vs 282 Nm needed for a 20° snow climb with margin | DERIVED | `calc/ski_track.py` |
| Track motor | the rear traction motors (no separate motor) | — | |
| Snow load / ice load | ski impact 4.1 kN vertical + 2.8 kN longitudinal at the tip (3 g + 2 g); cassette anti-rotation link 1.0 kN; sprocket hub 235 Nm continuous, 420 Nm peak | DERIVED | |
| Ground pressure, tracks | 6.3 kPa per cassette at 701 kg operating | DERIVED | tracked ATVs 3.8–6.2 kPa [TER-2]: at the top of the range; a 0.33 m track brings it to 5.7 kPa |
| Speed | 45 km/h cap (sprocket 795 rpm; 4,770 rpm motor in 6:1; crawl 12:1 limited to ~25 km/h by motor speed) | DERIVED | |

**Is the track adequate for the real mass?** At 701 kg operating, yes for traction (420 Nm available vs 282 needed in crawl), marginal for flotation (6.3 kPa vs the 3.8–6.2 kPa range of production tracked ATVs). Deep-powder capability will be below a snowmobile's (~3.4 kPa); this is inherent to a 700 kg machine on 0.66 m² of track and is the honest trade of a four-wheel platform. A 0.33 m track or a longer 1.20 m cassette are the levers, at +4 kg each.

## 7.4 SNOW-mode dynamics notes

Unequal front (ski) and rear (track) stances make ANSI/SVIA-style Kst the right metric [STD-2]; measured on a tilt table with the kits fitted. Steering effort rises (ski carbide bite): EPS "snow" map. Regen is limited to 0.15 g (track slip on ice). The interlock refuses SNOW above 5 °C ambient with a warning only (tracks on dirt are allowed but noisy and hard on the cassette).
