# Part 10 — Structural engineering

## 10.1 Load cases (RC-0: gross 590 kg road, 650 kg snow, 610 kg marine)

No public source gives validated load factors for a transformable ATV; the FSAE/Baja literature lists case *types* without g-multipliers [STR-4][IMP-2]. The factors below are **study assumptions** chosen conservatively from off-road chassis practice, and the first physical test in Part 13 (instrumented drop tests) exists to replace them with measurements. Static corner load W = 1.45 kN (road), 1.6 kN (snow).

| # | Case | Load definition (assumption) | Applied where | Governs |
|---|---|---|---|---|
| 1 | Static rider load | 1.0 g, rider 100 kg at seat, cargo 50 kg on rack/hitch | seat rails, rack, hitch | stiffness, sag |
| 2 | Maximum payload | 1.0 g, 150 kg payload + 100 kg overload check | as 1 | yield check |
| 3 | Landing from small jump | 5.0 g vertical at two wheels (one axle) or 3.5 g at four; 7.2 kN per corner | arm, pivot bearings, lock sector, chassis nodes | ultimate strength of the corner |
| 4 | Wheel impact (kerb/rock) | 3.0 g vertical + 2.0 g longitudinal at one wheel, simultaneously | arm root (bending + torsion), knuckle, half-shaft | arm and pivot |
| 5 | Side impact / lateral kerb | 1.5 g lateral at the contact patch of one wheel (2.2 kN) plus wheel-impact test per ISO 7141-style rim-flange strike [IMP-1] | knuckle, arm torsion, pivot bearings | bearing spacing |
| 6 | One-wheel obstacle (cross-axle twist) | one wheel at full compression, diagonal at full rebound, 1.0 g static | chassis torsion between front and rear pivot nodes | torsional stiffness (target: set by test; Baja-class frames are typically measured, not sourced [STR-4]) |
| 7 | Braking | 1.2 g deceleration, 70% front | knuckle, arm longitudinal, caliper mounts, pivot | arm bending in the longitudinal plane |
| 8 | Acceleration | 0.6 g (traction limited at μ 0.6), 290 Nm per wheel | half-shafts, motor mounts on the carrier, carrier-to-chassis lock | carrier and lock |
| 9 | Cornering | 1.0 g lateral (rider-active ATV, above the rollover threshold; the structure must survive even if the vehicle would tip) | knuckle, pivot | |
| 10 | Towing | SAE J684 Class 1 static tests: 26.7 kN longitudinal, 8.9 kN transverse, 11.1 kN vertical [TOW-1]; plus 49 CFR 393.71 tow-bar 3,000 lb longitudinal for towed weight < 5,000 lb [TOW-2]; tongue weight 10–15% of trailer mass [TOW-3] | hitch tower and its chassis nodes | hitch |
| 11 | Track traction | 1.6 kN pull per rear cassette at the sprocket, 250 Nm at the hub; anti-rotation link 1.0 kN | rear hub studs, arm hardpoint | studs |
| 12 | Ski impact | 3.0 g vertical + 2.0 g longitudinal at the ski tip (rut/ice ridge), 4.8 kN | ski adapter, knuckle, arm | adapter |
| 13 | Marine slamming (variant) | ISO 12215-5 bottom pressure with nCG from Savitsky–Brown/Fridsma seaway accelerations [HUL-5][HUL-6] (category D, Hs 0.3 m: nCG is small; design for category C envelope, Hs 2 m, as the safety margin) | hull bottom panels, arch doublers, pivot housings | hull scantlings |
| 14 | Frontal impact (rider protection reference) | FS impact attenuator benchmark: 7,350 J, ≤ 20 g average [STR-2] | nose structure | energy absorption |

Combination rule: cases 3–5 and 7–9 are applied with a 1.5 factor of safety on yield and 2.0 on ultimate for the corner module; the chassis uses 1.5 on yield with welded allowables.

## 10.2 Material candidates and allowables

| Material | Use | Design allowables used | Source |
|---|---|---|---|
| 4130 normalized steel tube | space frame (option A), pivot housings (welded steel version) | non-welded UTS 670 / yield 435 MPa; **welded joints designed at Sy 180 / Su 300 MPa** (FSAE welded steel equivalency values) unless the weld procedure is qualified | [STR-5][STR-1] |
| 6082-T6 / 6061-T6 aluminium | space frame (option B), machined carrier and pivot housing, arm (welded box) | non-welded Sy 240 / Su 290 MPa; **welded Sy 115 / Su 175 MPa** (as-welded) — ~50% yield loss in the HAZ; post-weld solution + age recovers it but distorts | [STR-1][MFG-4] |
| 7075-T6 aluminium | knuckle, lock sector carrier (bolted, never welded) | Sy ~500 MPa class (not verified this study); not fusion-weldable | engineering knowledge, flagged |
| 5083-H116 aluminium | marine hull tub | marine-grade, welded with ER5356 | [MAR-2] |
| A356-T6 cast aluminium | carrier housing at volume | sand-cast, machined bores | [MFG-5] |
| 42CrMo4 / 4140 steel | pivot shaft (Ø50), lock pin (Ø20), sprocket hub | through-hardened, ground | — |
| Glass/epoxy infusion | hull (alternative), body panels | FVF 50–60% infused | [MFG-5] |
| UHMW-PE | ski, skid plates | — | — |

## 10.3 Tube/plate architecture

Recommendation: **a hybrid platform**.

- **Central platform**: two longitudinal 6082-T6 extruded sills (100 × 60 × 4 mm) tied by machined 6082 pivot-housing nodes at the four corners and by a laser-cut 5083 floor plate (the "tub", 3 mm, which on the marine variant becomes 4 mm and watertight). The battery box sits between the sills on the floor.
- **Upper structure**: 4130 tube (25.4 × 2.0 mm, FSAE Size A minimum [STR-1]) for the rider frame, handlebar mast, seat rails and rack, bolted to the sills at the nodes. Steel here because it takes abuse, is easily repaired and its weld fatigue class is ~3× aluminium's [STR-6].
- **Corner modules**: bolted to the nodes with 4 × M12 10.9 and two Ø12 dowels each.
- **Hitch**: a 4130 tower welded to a 6 mm 5083 plate that bolts to the rear node pair, 50 mm receiver, height 0.35 m above ground in ROAD; designed to SAE J684 Class 1 [TOW-1]. It is on the chassis, so corner geometry changes never load it through the suspension.

Why not an all-aluminium welded frame: welded 6061 designs at 115 MPa yield weigh nearly what steel does and fatigue three times worse [STR-1][STR-6]. Why not all steel: the four pivot housings need precision bores and immersion corrosion resistance, which machined aluminium gives.

## 10.4 Joints, fasteners, welds, bearings, shafts, bushings

| Item | Specification |
|---|---|
| Node-to-sill joints | bolted (M12 10.9, 8 per node) with a bonded interface (structural epoxy) to share load and seal |
| Welds (steel) | TIG, ER70S-2 on thin wall, no PWHT below 3 mm wall [MFG-3]; assess fatigue at IIW FAT 71 (toe) / FAT 36–56 (cruciform) [STR-6] |
| Welds (aluminium tub/arm) | MIG/TIG 5356; FAT 25–36 [STR-6]; keep welds out of the arm root — the root is a machined boss bonded/bolted into the box |
| Fasteners | 10.9 zinc-flake steel on aluminium with isolating washers; stainless A4 only on the marine variant's wet side; all critical fasteners torque-striped |
| Pivot bearings | two taper-roller bearings Ø50 bore, 150 mm apart; static rating C₀ ≥ 60 kN each (dynamic radial 12 kN at 5 g → s₀ ≥ 5 [STR-9]); double-lip seals + labyrinth |
| Pivot shaft | Ø50 42CrMo4, hardened journals, keyed to the carrier; shear/bending at 5 g: M ≈ 7.2 kN × 0.075 m = 0.54 kNm → bending stress ≈ 44 MPa: ample |
| Knuckle bearings | sealed spherical plain bearings (kingpin) Ø20, ATV class |
| Bushings | polyurethane 80 Shore A at spring eyes and anti-rotation links |
| Lock pin | Ø20 42CrMo4, double shear 21 kN → 33 MPa: sized for wear, not strength |
| Hub | UTV-class sealed unit bearing, 4 × M10 studs (10.9); stud shear at 250 Nm on a 110 mm PCD ≈ 4.5 kN total: ample |

## 10.5 Which cases need FEA, fatigue analysis, physical testing

| Component | FEA (static) | Fatigue analysis | Physical test | Why |
|---|---|---|---|---|
| Arm | cases 3, 4, 5, 7, 12 | yes: aluminium has no endurance limit [STR-8]; target 10⁶ cycles at 1.5 g spectrum, Goodman corrected | drop test, rig fatigue 10⁶ cycles | primary structure, new geometry |
| Carrier + lock sector | cases 3, 8 | yes (pin bearing on sector, fretting) | rig: 10⁴ lock cycles under load; 5 g impact with pin engaged | no precedent |
| Pivot housing / node | cases 3, 5, 6 | yes at bolted joints | rig + vehicle torsion test (IMU twist method [STR-4]) | load concentration |
| Chassis sills + floor | 1, 2, 6, 10 | welds (FAT classes) | torsion test, hitch pull test to J684 loads | |
| Knuckle, hub, half-shaft | 4, 5, 7, 8 | supplier data | ISO 7141-style wheel impact [IMP-1] | mostly purchased |
| Hitch | 10 | yes | J684 static tests; then tow test to set the rating | capacity is set by test, per the brief |
| Ski adapter, track sprocket hub | 11, 12 | yes | field test on snow | |
| Hull (variant) | 13 | panel fatigue (ISO 12215-5) | tank/lake slamming with accelerometers | |
| Rider frame | 14 + rollover (ROPS-style static, Baja practice [STR-3]) | no | static push test | |

Inspection intervals for life-limited parts (arm root, sector, pivot shaft) are to be set from the fatigue test scatter, with a dye-penetrant check at each track-season changeover.
