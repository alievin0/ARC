# 11 — Structural load cases, materials, manufacturing, serviceability

## 11.1 Load cases (V0 masses: 637 kg road, 701 kg snow; static corner 1.56 kN)

| # | Case | Definition (TARGET factors, to be replaced by drop-test data [IMP-2]) | Corner load | Governs |
|---|---|---|---|---|
| 1 | Static rider load | 1 g, rider 100 kg at the hip point | 1.56 kN | stiffness, sag |
| 2 | Maximum payload | 1 g, +100 kg overload check | 1.8 kN | yield |
| 3 | Hard landing / jump | 5 g on one axle | 7.8 kN | arm ultimate, pin (25.5 kN shear), pivot bearings (≈ 13 kN radial each) |
| 4 | Wheel drop (into a hole) | rebound strap snatch: 2 kN; then 3 g on landing | 4.7 kN | strap, arm root |
| 5 | Kerb strike | 3 g vertical + 2 g longitudinal, one wheel | 4.7 + 3.1 kN | arm bending + torsion, half-shaft, knuckle |
| 6 | Rock strike (underbody) | 3 g on a 100 mm dome at the tub | 19 kN on the floor | floor, sills, battery isolation |
| 7 | Braking | 1.2 g, 65% front; inboard: 800 Nm through the front half-shafts | 2.4 kN longitudinal per front wheel | half-shaft, carrier caliper mount, pin |
| 8 | Acceleration | 0.6 g traction-limited, 60% rear; 290 Nm per rear wheel | 1.9 kN | half-shaft, motor mount |
| 9 | Cornering | 1.0 g lateral (structure survives even where the vehicle would tip) | 2.3 kN lateral at the patch | arm torsion (0.15 m offset), pivot bearing moment |
| 10 | Rollover | rider frame static: 1.5× vehicle mass vertical + 1× lateral at the bar clamp (Baja-style equivalency [STR-3]) | — | rider frame |
| 11 | Uneven wheel loading | diagonal 1 g / 0 g | — | chassis torsion |
| 12 | Track traction | 1.56 kN pull per cassette; 420 Nm peak at the hub; anti-rotation 1 kN | — | studs, arm hardpoint |
| 13 | Ski impact | 4.1 kN vertical + 2.8 kN longitudinal at the tip | — | adapter, knuckle |
| 14 | Towing | SAE J684 Class 1: 26.7 / 8.9 / 11.1 kN [TOW-1] | — | hitch, rear beam, sills |
| 15 | Frontal impact | 7.35 kJ, ≤ 20 g average (FS attenuator benchmark [STR-2]) | — | nose, front beam |

**Where FEA is mandatory:** arm (cases 3, 5, 9), carrier + sector (3, 7, 8), pivot node + sill (3, 9, 11), chassis torsion (11), hitch (14), rider frame (10, 15), ski adapter (13), sprocket hub (12). **Fatigue analysis:** arm root, carrier sector, node bolts, welded 4130 joints (IIW FAT classes [STR-6]), aluminium finite-life with Goodman correction [STR-8]. **Physical tests:** drop tests to replace the g-factors; rig fatigue 10⁶ cycles on one corner; torsion test; hitch pull; wheel impact (ISO 7141-type [IMP-1]).

## 11.2 Materials

| Component | Material | Why |
|---|---|---|
| Chassis sills, cross-members | 6082-T6 extrusion | stiffness per mass, corrosion, extrudable section; joints bolted/bonded so the HAZ penalty (welded Sy 115 MPa [STR-1]) is avoided |
| Tub floor | 5083-H116 3 mm (4 mm on the variant) | marine-grade, formable, weldable to itself for the variant tub [MAR-2] |
| Pivot nodes, carriers (prototype) | 6082-T6 billet | machinable, anodisable, precision bores |
| Carriers (pilot series) | A356-T6 sand casting, machined | integrates motor mount, sector seat, lever, bulkhead in one part at low tooling cost [MFG-5] |
| Arms | 5083 sheet box + 6082 root boss (bonded/bolted, unwelded root) | formable box, fatigue-critical root kept out of the HAZ |
| Steering knuckles | forged 4140 (or 7075-T6 billet) | high strength, no welding, spherical-bearing bores |
| Wheel hubs | purchased steel unit bearing hub | commodity |
| Pivot shaft, lock pin, sprocket hub | 42CrMo4 hardened | wear and shear |
| Lock sector insert | case-hardened steel, replaceable | wear at the pin interface |
| Rider frame, hitch tower, bumper beam | 4130 normalized tube, TIG, ER70S-2 | toughness, repairability, weld fatigue class ~3× aluminium; welded allowable Sy 180 MPa [STR-1][STR-6] |
| Body panels | thermoformed ABS/TPO (painted) → RIM PU at volume | tooling cost at ≤ 500/yr [MFG-5] |
| Skids, wear strips, footboard tops | UHMW-PE | abrasion |
| Skis | UHMW-PE body, aluminium spine, steel keel, carbide runner | snowmobile practice |
| Tracks | moulded rubber with polyester/Kevlar cords, steel rods, internal guide horns | production ATV track construction [PAT-21] |
| Fasteners | 10.9 zinc-flake steel with PTFE/nylon isolators on aluminium; A4 stainless in the arches and on the variant's wet side | galvanic isolation |
| Protective plates | 5083 4 mm under the nodes; UHMW under the battery | |
| Hull (variant) | 5083-H116 or infused glass/epoxy | [MAR-2][MFG-5] |

## 11.3 Manufacturing method per component

| Component | Method | Notes |
|---|---|---|
| Sills, cross-members | extrusion + CNC ends | standard die or open-tooling profile |
| Tub floor, arm blanks, sector plates, brackets | laser-cut 5083/6082 sheet, CNC press-brake forming | |
| Pivot nodes | CNC from billet (all volumes; 4 per vehicle) | ±0.05 mm on bearing bores [MFG-1] |
| Carrier | CNC billet (Prototypes 1–6); sand-cast A356-T6 + CNC (pilot series) | |
| Arm | formed sheet + MIG box weld + bonded/bolted CNC root boss | weld away from the root |
| Knuckle | purchased ATV forging machined to suit, or CNC 7075 | |
| Hub, bearings, CV shafts, coil-overs, calipers, rack, EPS, motors, inverters, actuators, solenoids, sensors, connectors | purchased | |
| Lock pin, pivot shaft, sprocket hub | CNC turned 42CrMo4, hardened, ground | |
| Rider frame, hitch, bumper | CNC tube bending (CLR ≥ 2.5× OD [MFG-2]) + TIG welding 4130 | |
| Body panels | thermoforming (prototype/pilot), RIM (volume) | |
| Ski adapter plate | CNC 7075 or laser-cut/formed 4130 | |
| Track cassette | licensed from a track manufacturer (Section 15 of the feasibility study) or fabricated: laser-cut frame + purchased idlers/track | |
| Sponsons (swim kit) | rotomoulded PE | [MFG-5] |
| Hull (variant) | welded 5083 or vacuum-infused composite | |
| Prototype covers, ducts, sensor housings | MJF PA12 | [MFG-5] |
| Coolant/HV bulkhead manifold in the carrier | metal AM (AlSi10Mg) for prototypes, cast at volume | [MFG-7] |

Nothing above needs a factory that does not exist: every process is available at job-shop level in any industrial region.

## 11.4 Serviceability procedures

| Task | Procedure | Time (target) |
|---|---|---|
| Change a wheel | select "Swap" on that corner: the vehicle lifts it; 4 lug nuts | 5 min, no jack |
| Change a pivot bearing | corner at 50° (lifted), wheel off; remove the disc cover; pull the pivot shaft outboard (it is a cartridge with the arm root); the taper rollers come out inboard-out from the node; press new ones; re-shim preload | 2 h |
| Change the actuator | disc cover off; two pins (rod end, chassis anchor); two connectors; the pin lock holds the carrier meanwhile | 30 min |
| Change a brake (pads/disc) | the caliper is on the carrier's inboard face: reachable from under the body with the corner lifted; pads slide out; the disc comes off the reduction output with 6 bolts | 30 min pads / 1.5 h disc |
| Remove a corner module | wheel off, disc cover off, HV/coolant/signal bulkhead disconnected (dry-break coolant couplings), tie-rod outer joint (front), 8 × M12 node bolts: the module comes off the sill as one unit with the carrier, arm, actuator, motor | 1.5 h |
| Access wiring | footboards unclip (sill harness); seat lifts (HV junction, DC-DC); fascia panel (controllers) | 10 min |
| Change a track | corner lifted; tensioner backed off; rear idler link swung; track slides off the sprocket | 40 min |
| Change a ski | quick-release pin + circlip | 5 min |
| Access the motor | disc cover off (coolant fittings, phase connector); motor + reduction unbolt from the carrier's inboard face; with the corner lifted the carrier can be rotated to 50° for clearance | 1.5 h |
| Drop the battery | vehicle in LIFT on both rear corners (0.28 m rise), 4 bolts + 2 shear pins from below, MSD out first, HVIL broken | 45 min |
