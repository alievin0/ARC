# ARC-2B — AMPHIBIOUS TRANSFORMATION ENGINEERING STUDY

Follow-up to `docs/feasibility/` and `docs/architecture/`. Every number below is produced by the scripts in `calc/` (`python3 calc/run_all.py`); tags are TARGET (chosen, to validate), TBD, DERIVED, BENCH (from `docs/feasibility/REFERENCES.md`). Body frame as before: origin on the ground under the wheelbase midpoint in ROAD static, +X forward, +Y left, +Z up.

## 1. Executive conclusion

**Physics says YES, at displacement speed, with a deployable architecture that the land vehicle can carry.** It says NO to planing or semi-planing on the integrated vehicle.

The previous studies asked whether the ATV body could be a hull. It cannot (0.24 m³ of sealed volume against 0.69 m³ needed). This study asked a different question: what is the smallest *deployable* flotation the V0 body can carry without giving up its land role, and does anything credible exist there. The answer that survived the calculations is **ARC-2B AMPHIBIOUS V0 (Architecture H)**:

1. **The lower body becomes a watertight tub** (floor Z 0.28, inner arch walls at Y ±0.36 up to the fender crown Z 0.85, two bulkheads, sealed corner-cartridge bores, drain valves). It is a change to the base vehicle's structure worth making regardless of water: it closes the sill/floor section into a torsion box. It supplies 0.60 m³ of buoyancy but, alone, floats nothing useful.
2. **The fender side skins become fold-down outrigger rails**: each is a 2.2 m ribbed 6082 L-extrusion hinged along the fender's lower edge (Y 0.62, Z 0.62). On land it is the body side. Swung 90° outboard it is a 0.22 m horizontal rail with a 0.15 m down-flange at its tip, held by three folding stays with spring-pinned locks.
3. **Two inflatable three-chamber tubes (Ø 0.50 × 2.4 m)** are stored rolled inside the fender cavities above the arches (0.006 m³ each, in a 0.11 m³ cavity) with their bolt ropes captive in tracks on the flange. They inflate from a 12 V blower/compressor to 0.2 bar in about 5 minutes and hang outboard of the flange, 69 mm clear of a fully steered front tyre. Afloat width 2.68 m.
4. **The fender cavities are foam-filled** (0.16 m³) so that a flooded cockpit still floats.
5. **A stern pod** (8 kW ducted propeller on a 0.50 m folding arm, ±35° vectoring) stows under a rack lengthened by 0.18 m and swings down 65° to 0.22 m below the operating waterline. The handlebar steers the wheels on land and the pod afloat through the existing rack-position sensor; the wheels keep steering too, harmlessly.
6. **The corner modules contribute exactly two things** and are not forced to do more: they raise the body to HIGH for deployment and entry (tube bottoms 0.47 m and pod bottom 0.20 m above the ramp), and afloat they lift the tyres to the existing −2° hard stop. The tyres stay 0.40 m in the water and are the shallow-water landing gear; no −50° retraction, no bay doors, no actuator change.

| Result at maximum marine mass (694 kg: 487 curb + 82 marine hardware + rider 100 + 25 cargo) | Value |
|---|---|
| Total buoyant volume / reserve buoyancy | 1.63 m³ / 135% |
| Waterline / tub-rim freeboard / rail height above water | Z 0.527 m / 0.32 m / 0.09 m |
| GM transverse / longitudinal | 3.70 m / 1.39 m |
| Righting arm at 15° | 0.65 m (4.4 kNm) |
| Heel: rider 0.3 m off-centre / one chamber lost / half a tube lost | 0.7° / 2.1° / 3.9° |
| Cruise / maximum speed with an 8 kW pod | 6 km/h at 1.9 kW shaft / 9 km/h at 7.6 kW |
| Endurance at 6 km/h on 10 kWh usable | ~25 km, ~4 h |
| Added land mass / width / length | +82 kg (16.8%) / 0 / +0.18 m (rack) |

One automated check fails and is reported, not hidden (Section 25): a *flooded cockpit with one tube entirely lost* sinks (0.59 m³ available against 0.69 m³ needed: 0.10 m³ more foam must be packaged). A second case passes its survivability threshold but is flagged: the whole-tube-loss heel of 29° puts the cockpit rim under water. Both are double-failure cases behind three chambers per tube and pressure monitoring, and both must be closed before Prototype 4.

Semi-planing and planing are excluded: the tubes' hull speed is 7 km/h; at 10 km/h the screening model already needs 11 kW shaft with four tyres in the water, and planing (70–110 kW, a rigid planing bottom, 20 kWh) is the ARC-2B M variant from the previous study, which stays as a separate platform.

## 2. Existing technology

No new external source could be fetched in this environment (egress policy; search quota exhausted), so the base is `docs/feasibility/REFERENCES.md`, with the inflatable-craft facts below marked **(engineering knowledge, unsourced here; verify)**.

| Technology | What exists | How it works | Loads it carries | What ARC-2B takes | Limitation |
|---|---|---|---|---|---|
| Rigid-inflatable boats (RIB) | worldwide production | a rigid hull with inflatable tubes bonded/tracked along the sheer; tubes at 0.2–0.25 bar, multi-chamber; bolt-rope tracks are standard **(unsourced)** | the tube carries a large share of the boat's displacement through the bond/track line; RIBs are driven onto beaches on their tubes | the tube type, pressure, chamber count, bolt-rope track attachment, blower inflation | tubes puncture; UV ageing; the hull side must be a structural member |
| Displacement amphibious ATVs | Argo 8×8 [AMP-9] | sealed lower hull, tyres as paddles, ~5 km/h | full vehicle displacement | proof that ~5 km/h with wheels in the water is a real product class | no tubes; hull is the vehicle body |
| Amphibious car, displacement | Amphicar [AMP-5] | sealed body, propellers, ~7 mph | full displacement | speed benchmark for non-planing amphibians | body is a hull |
| Retractable-suspension amphibians | Gibbs Quadski [AMP-1][RET-2]; WaterCar [AMP-4][PAT-9] | hydraulic retraction of a whole corner above the waterline; planing hull | corner loads through sealed pivots | sealed pivot cartridges (already in V0); the "afloat detected by arm sensors" gate [PAT-41] | requires a planing hull of Quadski size |
| Retracting/driven wheels on a boat | Sealegs [AMP-6][PAT-8] | hydraulic legs pivoted above the waterline, ~600 kg system | wheel loads on a boat hull | wheels touching first in the shallows (landing gear logic) | boat-first |
| Foam-filled hull cavities | CAMI [AMP-8]; ISO 12217-3 / ABYC H-8 swamped tests [MST-1][MST-3] | closed-cell foam in voids gives flotation when flooded | swamped displacement | fender-cavity foam; the swamped check | foam volume must be found |
| Small electric jet/pod modules | ZeroJet [JET-7] | 14–30 kW, 48 V | thrust ~1 kN class | pod power class; a ducted propeller is chosen over a jet at 1–2.5 m/s | jets are inefficient below ~20 kn [JET-1] |
| Regulatory | RCD excludes amphibious vehicles [REG-5]; US flotation rules exclude them [MST-2] | — | — | ISO 12217-3-style checks are voluntary design targets | no certification path exists; the safety case must be self-imposed |

## 3. Problem definition

Find a mechanically explainable LAND → WATER → LAND transformation for the V0 vehicle (487 kg curb, leading/trailing arms on actuated carriers, 26 in tyres, existing actuator 104 mm / 6.8 kN, lock 25.5 kN) that:
- floats the vehicle with rider and marine hardware with ≥ 30% reserve buoyancy, ≥ 0.25 m freeboard, positive stability under the eight load cases of Section 6;
- is carried on the vehicle in land mode without changing its width, clearance, travel or actuator range;
- has a stored position, deployment path, hinge/slider, actuator or manual mechanism, lock, load path, sealing and service access for every marine part;
- and states honestly which water speed regime results.

## 4. Mass model (`calc/mass_amph.py`)

| Item added to the land vehicle | kg | Basis |
|---|---:|---|
| Watertight tub upgrade (inner arch walls to Z 0.85, seams, two bulkheads, drain valves, cartridge bore seals) | 15 | TARGET |
| Fender rails: 2 × 2.2 m ribbed 6082 L-extrusion replacing the thermoformed side skins, hinges, 6 stays with lock pins | 14 | TARGET, net of the removed panels |
| Inflatable tubes 2 × Ø 0.50 × 2.4 m, 3 chambers, bolt ropes, valves | 12 | ~1.2 kg/m² fabric (unsourced) |
| Blower + top-off compressor + hoses + pressure sensors | 5 | TARGET |
| Stern pod: 8 kW motor, duct, propeller, steering actuator, arm, hinge, pin, cable | 22 | TARGET |
| Bilge: 2 pumps, float switches, alarm, wiring | 5 | ~2 kg per 1,100 GPH pump [MAR-1] |
| Corner-module immersion upgrade: IP68 carrier housings, vents, seals, anodes | 6 | TARGET |
| Safety: kill cord, seat switch, CO₂ emergency inflator, throwable flotation stowage | 3 | TARGET |
| **Marine hardware total** | **82** | 16.8% of curb |

| Condition | Mass | Required displacement |
|---|---:|---:|
| Land vehicle, curb | 487 kg | 0.487 m³ |
| Land vehicle + rider | 587 kg | 0.587 m³ |
| Marine dry mass | 569 kg | 0.569 m³ |
| Marine operating mass (+ rider) | 669 kg | 0.669 m³ |
| Marine maximum (+ rider + 25 kg cargo) | 694 kg | 0.694 m³ |
| Maximum + 5% water absorption/splash allowance | 729 kg | 0.729 m³ |

Water cargo is limited to 25 kg (land: 50 kg) by the freeboard margin, not by structure.

## 5. Buoyancy (`calc/hydrostatics_amph.py`, `calc/architectures_amph.py`)

**Minimum flotation volume.** With 30% reserve the vehicle needs 0.90 m³ of buoyant volume at maximum mass. The watertight tub supplies 0.60 m³; the deployable part must add ≥ 0.30 m³, and any volume that is *not* deployable must fit the land body, whose only free volumes are the two fender cavities above the arches (0.22 m³ together) and a 30 mm skin over the fender band (0.026 m³). That single comparison eliminates every rigid stowed-equals-deployed architecture (Section 7).

| Condition | Mass | Waterline Z | Tub-rim freeboard | Reserve buoyancy | KB | BM_T | GM_T | GM_L |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Land vehicle, curb | 487 | 0.463 | 0.39 | 234% | 0.38 | 5.41 | 5.18 | 1.99 |
| Marine operating (+ rider) | 669 | 0.519 | 0.33 | 143% | 0.41 | 4.05 | 3.85 | 1.45 |
| Marine maximum | 694 | 0.527 | 0.32 | 135% | 0.41 | 3.90 | 3.70 | 1.39 |
| Maximum + 5% | 729 | 0.537 | 0.31 | 123% | 0.42 | 3.71 | 3.52 | 1.32 |

Total buoyant volume 1.63 m³ = tub 0.604 + fender foam 0.160 + tubes 0.864. Waterline at maximum 0.527 m in the body frame: the tub floor (0.28) is 0.25 m under, the footboards (0.42) are 0.11 m under the outside water level inside a dry tub (kayak-cockpit condition), the rail deck (0.62) is 0.09 m above it, the fender cavities (0.64 up) stay dry. Draft below the tyre bottoms afloat: the tyres (at the −2° carrier stop) reach Z 0.12, i.e. 0.41 m below the waterline: the vehicle floats in ≥ 0.55 m of water and grounds on its wheels in less.

Centre of buoyancy 0.41 m; centre of gravity afloat 0.61 m (TARGET: land CG 0.60 with rider, marine hardware ~0.55, tubes at 0.52; a full build-up is a DO NOT BUILD YET item).

## 6. Stability (`calc/hydrostatics_amph.py`)

Method: prismatic bodies (stepped tub, two foam boxes, two cylindrical tubes); for a heel angle the water surface is tilted in the body frame, immersed areas and centroids are computed analytically (polygon clipping, circular segments), the waterline is solved for the displacement, and GZ = −[(y_B − y_G) cos φ − (z_B − z_G) sin φ]. Small angles reproduce GM = KM − KG.

Righting curve at 694 kg, KG 0.61:

| Heel | 2° | 5° | 10° | 15° | 20° | 30° | 40° |
|---|---|---|---|---|---|---|---|
| GZ (m) | 0.13 | 0.31 | 0.57 | 0.65 | 0.64 | 0.60 | 0.54 |
| Righting moment (kNm) | 0.9 | 2.1 | 3.8 | 4.4 | 4.3 | 4.1 | 3.7 |

Load cases (maximum mass):

| # | Case | Result |
|---|---|---|
| 1 | Rider centred | heel 0°, tub-rim freeboard 0.32 m, rail 0.09 m above water |
| 2 | Rider 0.30 m to port | heel 0.7° |
| 3 | Rider 0.30 m to starboard | heel 0.7° |
| 4 | Rider 0.30 m forward | trim 1.8° bow-down (GM_L 1.39 m) |
| 5 | Rider 0.30 m aft | trim 1.8° stern-down; 25 kg cargo at the rack: 1.6° |
| 6 | Asymmetric payload: 25 kg at 0.45 m + rider 0.2 m, same side | heel 0.7° |
| 7 | One flotation module partially deployed: starboard tube at 67% (one chamber lost) / 50% | heel 2.1° / 3.9°; low-side rail at the waterline at 50% |
| 7b | Starboard tube entirely lost | heel 29°; low-side tub rim 0.23 m under water: **cockpit floods**; the vehicle then floats swamped on the foam + one tube only if 0.10 m³ more foam is added (Section 25) |
| 8 | Wave disturbance, category D (Hs 0.3 m, crest ~0.2 m) | 0.12 m of freeboard margin over the crest at maximum mass; the rail deck is in the splash zone |

The vehicle is stiff (GM 3.7 m, like a small catamaran): the tubes at Y ±1.09 give a waterplane inertia of 2.7 m⁴. The stiffness is also why a lost tube matters so much: the righting comes almost entirely from the tubes, so losing one removes half of it and the vehicle rolls to the tub's own (poor) stability. Design consequence: three chambers per tube, pressure monitoring on every chamber, a CO₂ emergency re-inflation, and the swamped-flotation foam.

## 7. Architecture options (`calc/architectures_amph.py`)

Required: ≥ 0.30 m³ deployable volume; stowable in 0.22 m³ of fender cavity plus a 30 mm skin; no land-width growth; no sealing under load that has no precedent.

| Architecture | Stowed m³ | Deployed m³ | Added kg | Verdict |
|---|---:|---:|---:|---|
| A. Folding rigid side pontoons (2 × 0.24 m³ rotomoulded) | 0.48 | 0.48 | 51 | **Fail, packaging**: stowed volume equals deployed volume; 0.48 m³ cannot live on the body (0.22 m³ available) |
| B. Telescoping side bodies (4 nested sections per side) | 0.24 | 0.65 | 52 | **Fail, packaging and sealing**: a 0.6 × Ø 0.5 housing does not fit the fender band; three sliding seals per side under water |
| C. Fold-out rigid catamaran hulls (2 × 0.45 m³) | 0.90 | 0.90 | 71 | **Fail, land impact**: stowed on the fenders the vehicle is 1.35 m tall with the CG 0.12 m higher |
| D. Central tub + rigid folding amas (2 × 0.16 m³) | 0.32 | 0.32 | 48 | **Marginal buoyancy (0.92 vs 0.90 m³), fail land width** (+0.36 m) |
| E. Expandable monocoque (folding sides + fabric skirt) | 0.02 | 0.48 | 22 | **Fail, sealing**: an open-bottom prism with a loaded flexible skirt has no precedent |
| F. Sealed 2.8 × 1.6 m planing hull, wheels to −50° (ARC-2B M) | 0 | 1.43 | 140 | Pass as a separate variant, not integrated |
| G. Removable drive-in hull (dock) | 0 | 2.0 | 0 | Pass, not integrated |
| **H. Watertight tub + fold-down fender rails + inflatable tubes + foam** | **0.012** | **1.02** | **82** | **Pass**: 1.63 m³ total, 135% reserve |
| I. Inflatable tubes directly on the fender edge (no rail) | 0.012 | 1.02 | 68 | Pass with a mechanical steering limiter afloat (tube inner face at Y 0.62 meets a steered tyre at Y 0.77): the fallback if the rail hinge proves troublesome |

Only an inflatable achieves the 70:1 stowed-to-deployed ratio the fender cavity demands. That is not a preference; it is the volume arithmetic.

## 8. Mechanism comparison (deployment of H versus I, and the rail itself)

| Criterion | H: fold-down rail + tube outboard of the flange | I: tube on the fender edge, no rail |
|---|---|---|
| Tube position | centre Y ±1.09, Z 0.52; inner face Y 0.84 | centre Y ±0.87, Z ~0.58; inner face Y 0.62 |
| Steering afloat | full ±32/42° (69 mm clearance to the steered tyre) | rack must be limited to ±5° mechanically; pod steered from the column torque sensor |
| GM_T | 3.7 m | ~2.6 m (tubes 0.22 m closer to the centreline) |
| Rail loads | 2.5 kN/m wave load on a 0.22 m cantilever: ribbed extrusion at 72 MPa; 3 stays at 3.2 kN | none (tube tracks on the fender skin, which must then be structural) |
| Moving parts | 2 rails (hinge + 3 stays each), 2 tubes, 1 pod arm | 2 tubes, 1 pod arm, 1 rack limiter |
| Land mode | rail is the body side skin; stack inside the cavity | tracks visible on the fender edge |
| Transformation time | +2 min (rails) | — |
| Failure modes | stay lock not engaged (rail folds under wave load → tube pushed against the tyre) | tyre chafing the tube in any steering excursion; limiter failure |
| Serviceability | stays and hinges are external and visible | simpler |

H is chosen because keeping the mechanical steering fully functional afloat removes a by-wire steering mode and its safety case; the cost is two hinged rails with locked stays, which are the same kind of hardware as a drop-leaf table and are inspectable at a glance. I remains the fallback.

## 9. Wheel retraction: what the wheels do afloat

| Option | Assessment |
|---|---|
| A. Retract vertically | no vertical guide exists; the corner is a rotating arm |
| B. Retract inward (along Y) | the arm plane is fixed at Y ±0.34; nothing moves inward |
| C. Rotate upward (to −50°, previous variant) | needs a marine-range drive (100° sweep), hull flaps and a hull whose waterline is below the wheels; on the tube configuration the wheels would sit beside the rider at Z 0.49–1.15 and still be partly in the water (waterline 0.53): **no benefit** |
| D. Remain partially exposed at the existing −2° stop | wheel centre (±0.661, 0.451), tyre Z 0.12–0.78, 0.40 m submerged; drag 440 N of the 515 N total at 6 km/h (1 kW of shaft power) | 
| E. Sealed wheel wells | the arches are free-flooding by design (the tub wall is inboard of them); sealing a well around a moving arm was rejected in the previous studies |

**Selected: D.** The corner actuator does what it already does (12° → −2°, 14° of the existing sweep, unloaded because the wheels are afloat) and nothing else. The tyres become keels (roll and yaw damping), landing gear (they touch first in < 0.55 m of water; at HIGH they reach the bottom at 0.70 m, at LIFT at 0.80 m, so the vehicle *drives* out of the water before the tubes touch anything) and even paddles at 1–2 km/h if the pod fails.

Packaging envelope of the wheel (front-left; rear mirrored in X):

| Mode | Carrier | Wheel centre (X, Z) | Tyre envelope X / Z | Y |
|---|---|---|---|---|
| LAND, ROAD | 12° | (+0.650, 0.330) | +0.32…+0.98 / 0…0.66 | 0.365…0.615 |
| LAND, HIGH (deployment/entry) | 38° | (+0.555, 0.126) | +0.23…+0.89 / −0.20…+0.46 (body raised 0.204) | same |
| WATER | −2° | (+0.661, 0.451) | +0.33…+0.99 / 0.12…0.78; waterline 0.53 crosses the tyre 0.41 m above its bottom | same; tube inner face at 0.84 |

Steering, brake, suspension, motor, half-shaft and wiring are all untouched; the carrier housing (Z 0.35–0.52, in the arch) is under water afloat, hence the IP68 housing upgrade, vents, anodes and the wet-brake rule. Sand/snow: nothing new; the tube tracks and stays are the only added contamination-sensitive items and both are on the outside of the body where they are seen.

## 10. Hull transformation (tub, rails, tubes)

**Watertight tub (permanent).** Floor Z 0.28 (4 mm 5083), sill outer faces at Y ±0.30 to Z 0.41, inner arch walls at Y ±0.36 from Z 0.41 to 0.85 (3 mm 5083 or infused composite, bonded to the sills), bulkheads at X −0.85 and +0.85 (front: radiator/controller bay; rear: pod bay), rim at Z 0.85 with a 40 mm inward lip. Penetrations: four pivot cartridges (sealed bores), two tie-rod boots, four HV/coolant bulkhead plates, two drain valves (servo, normally open on land, closed for water), bilge pump outlets, seat-box hatch (gasketed, latched, switch-monitored). The tub is the primary structure in both modes; the load paths of `docs/architecture/04_chassis.md` are unchanged.

**Rails (2).** 2.2 m ribbed 6082-T6 L-extrusions (3 mm skin, 30 × 3 mm ribs at 100 mm), 0.22 m panel + 0.15 m return; hinge line at (Y 0.62, Z 0.62) with four hinges per side; three folding stays per side from the flange to the tub wall at Z 0.42 (45°), each with a spring-applied pin engaged by hand or by the stay's own over-centre geometry, with a switch. Stored: vertical (it is the body side, outer face at Y 0.65); the return lies on the fender top. Deployed: horizontal at Z 0.62 from Y 0.62 to 0.84, flange down to Z 0.47. Swept volume during the 90° swing: a quarter-cylinder of radius 0.37 m about the hinge, outboard of Y 0.62 between Z 0.25 and 0.99; the tyre outer face is at Y 0.615, so nothing is in the way at any carrier angle. Actuation: manual (the rail with the rolled tube weighs ~9 kg) with a gas strut assisting; an electric option (one 48 V actuator per rail) is a Gen-2 refinement.

**Tubes (2).** Ø 0.50 × 2.40 m (2.20 m cylindrical equivalent), three chambers with baffles and individual valves, 1100 dtex PU-coated fabric (TBD supplier), two bolt ropes along the inboard side running in two tracks on the flange's outer face (Z 0.60 and 0.49), so the tube centre sits at (Y ±1.09, Z 0.52): inner face 0.84, bottom 0.27, top 0.77. Stored: deflated and rolled (0.006 m³) inside the fender cavity behind the rail, attached; when the rail swings down the roll comes out with it and inflates outboard of the flange. Inflation: 12 V high-volume blower to 0.05 bar (unfolds and positions the tube, ~2 min), compressor to 0.20 bar (~3 min), pressure sensors on every chamber, relief valves at 0.30 bar. Deflation: blower reversed, ~3 min, then hand-rolled into the cavity (the rail return guides the roll). Emergency: a CO₂ cartridge per tube for a 30-second re-inflation of a leaking chamber.

**Foam.** 85% of each fender cavity (0.08 m³ per side) filled with closed-cell PE foam blocks around the tube roll and the blower.

**Stern pod.** Section 11.

Sealing strategy of the whole: the tub is the only volume that must stay dry; everything outside it (arches, carriers, rails, tubes, pod bay) is wet by design. There is no seal on any moving marine part except the tube valves and the pod's motor (an IP68 unit).

## 11. Water propulsion (`calc/resistance_power_amph.py`)

| Option | Efficiency at 1–2.5 m/s | Packaging | Safety | Steering | Shallow water | Reverse | Debris | Cooling | Maintenance | Integration | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A. Single water jet | poor below ~20 kn (~40% at best [JET-1]); at 2 m/s worse | intake must be in a planing bottom the vehicle does not have | good (no exposed blade) | nozzle | excellent | bucket | weeds clog intakes | raw-water loop | impeller wear | needs a hull pad and a 30+ kW motor to make useful thrust at 2 m/s | rejected |
| B. Open propeller on a shaft | good (~55–60%) | a shaft through the tub floor, stuffing box, strut | exposed blade near the tyres and swimmers | rudder needed | poor (lowest point) | motor reversal | fouling | motor inside the tub | seal | shaft seal in the tub floor | rejected |
| C. Twin water jets | as A, doubled | — | — | differential | — | — | — | — | — | — | rejected |
| D. Single central jet, retractable | as A | — | — | — | — | — | — | — | — | — | rejected |
| E. Electric outboard-type pod on a folding arm | good (~45–55% with a duct) | stows under the rack; nothing in the tub | duct guards the blade; kill cord | vectoring ±35° | retracts before grounding; the wheels touch first | motor reversal | duct grate; weed-shedding blade | motor is water-cooled by immersion (sealed IP68 unit) | pod removed with two pins and one connector | one hinge, one pin, one cable | **selected** |
| F. Ducted propeller fixed under the tub | as E | lowest point, below the floor → grounds first | — | rudder | poor | — | — | — | — | — | rejected |

Selected: **E**, an 8 kW (shaft) ducted-propeller pod, Ø 0.30 m duct, 48 V or HV-fed (HV through an IP68 connector with HVIL; 48 V would need ~200 A: HV chosen), steering actuator ±35° about the arm axis, on a 0.50 m arm hinged at (X −0.75, Z 0.32). Stowed at 45° up: pod centre (−1.10, 0.67), duct Z 0.52–0.82, under the lengthened rack (tip −1.28) and above the hitch. Deployed at 20° down: pod centre (−1.22, 0.15), duct Z 0.00–0.30, 0.22 m under the operating waterline over the duct top, 0.12 m behind the rack tip. Locked by a spring pin at the hinge in both positions.

Performance (operating mass 669 kg, tyres 0.40 m submerged, propulsive efficiency 0.45 TARGET):

| Speed | Resistance (friction / wave / tyres / total) | Shaft power | Battery power | Range on 10 kWh usable |
|---|---|---|---|---|
| 3 km/h | 10 / 4 / 110 / 125 N | 0.23 kW | 0.56 kW | 54 km |
| 5 km/h | 26 / 17 / 307 / 350 N | 1.1 kW | 1.5 kW | 33 km |
| **6 km/h (cruise)** | 37 / 37 / 442 / 515 N | **1.9 kW** | 2.4 kW | **25 km (4 h)** |
| 7 km/h (hull speed) | 48 / 77 / 601 / 726 N | 3.1 kW | 3.8 kW | 18 km |
| 8 km/h | 62 / 154 / 785 / 1,001 N | 4.9 kW | 5.8 kW | 14 km |
| 9 km/h (8 kW pod limit) | 76 / 294 / 994 / 1,365 N | 7.6 kW | 8.7 kW | 10 km |
| 10 km/h | 93 / 534 / 1,227 / 1,854 N | 11.4 kW | 13 kW | 8 km |

The tyres are 85% of the drag at 6 km/h; raising them further would need the fender crown raised (the tyre top is already at 0.78 against a 0.83 crown), so the drag is accepted: 1 kW. Acceleration 0–5 km/h in ~1 s (bollard ~1 kN). Turning radius 3–4 m at 5 km/h (TBD). This is a **5–6 km/h cruise, 8–9 km/h maximum, sheltered-water** vehicle. It is not a 40 km/h vehicle and will never be one on this architecture.

## 12. Water steering

| Option | Assessment |
|---|---|
| Steerable pod (vectoring) | selected: the whole thrust vector turns, works at zero speed, reverse steers the "wrong" way like an outboard (acceptable, familiar) |
| Rudder | needs way on; another deployable part; rejected |
| Differential propulsion | needs two pods; rejected |
| Vectoring nozzle (jet) | jet rejected in Section 11 |

**Land:** handlebar → column → EPS → rack → tie-rods (inner joints on the corner pivot axis) → wheels. **Water:** the same handlebar and rack; the rack-position sensor (already present for the interlocks) commands the pod's steering actuator at a 1:1 map (±32° bar-equivalent → ±35° pod); the wheels keep turning with the bar and act as weak rudders in the same sense. **Transition:** none for the rider; the controller enables the pod-follow map when WATER is declared and disables it on LAND. Failure of the pod steering actuator: the pod centres itself under a spring; the wheels' rudder effect and a reverse/forward pulse give a limp turning capability; the wheels can be driven as paddles asymmetrically (torque vectoring at 1–2 km/h) for the same purpose.

## 13. LAND → WATER transformation sequence

Precondition: at the shore, water depth ≥ 0.6 m within reach, bottom slope ≤ 15°, Category D water (sheltered, Hs ≤ 0.3 m). Everything below is confirmed by a switch or a sensor before the next step; the interlock rules of `docs/feasibility/06_safety_interlocks.md` apply (mode = verified hardware states, pins spring-applied).

| Step | Component | Movement | Axis | Travel | Actuator | Lock | Sensor | Structural load | Seal | Failure condition |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Vehicle | stops on the ramp above the waterline; Park set | — | — | — | rear parking brakes | speed 0, pitch/roll ≤ 15° | static | — | slope > 15° → refuse |
| 2 | Carriers ×4 | ROAD → HIGH | corner pivot axes | +26° | 4 linear actuators | pins at 38° | carrier sensors, pin switches | corner loads through pins | — | any pin unconfirmed → abort to ROAD |
| 3 | Drain valves ×2, seat hatch | close | — | — | 2 servo valves | latch | valve position, hatch switch | — | tub becomes closed | valve/hatch open → refuse |
| 4 | Bilge pumps ×2 | self-test run 5 s | — | — | — | — | pump current, float switches dry | — | — | dry test fail → refuse |
| 5 | IMD | isolation check | — | — | — | — | ≥ 500 Ω/V | — | — | below → refuse |
| 6 | Rails ×2 | rider unlatches and swings each rail down 90° (gas-strut assisted), then closes the three stays | rail hinge line (Y 0.62, Z 0.62) | 90° | manual + gas strut | 3 stay pins per side, spring-applied | 6 stay switches, 2 rail-down switches | rail carries the rolled tube only | — | any stay switch open → tubes not inflated |
| 7 | Tubes ×2 | inflate: blower to 0.05 bar (tube unfolds outboard of the flange), compressor to 0.20 bar | — | — | blower + compressor | valves | 6 chamber pressure sensors ≥ 0.18 bar | tube fabric hoop; bolt ropes in tracks | tube valves | any chamber < 0.18 bar after 8 min → abort (deflate, rails up) |
| 8 | Pod arm | unlocks, swings down 65° to the deployed stop, locks | transverse hinge (X −0.75, Z 0.32) | 65° | 48 V linear actuator (2 kN) | spring pin at the hinge | arm angle sensor, pin switch | arm/pin sized for 3 kN beaching | pod motor IP68 | pin unconfirmed → pod not enabled |
| 9 | Pod motor | spin test 5 s at 10% in air/shallows | — | — | pod inverter | — | motor current plausible | — | — | no current → refuse WATER |
| 10 | Steering | pod-follow map armed (not yet active) | — | — | — | — | rack sensor OK | — | — | — |
| 11 | Vehicle | drives down the ramp at ≤ 5 km/h in HIGH on wheel drive (tube bottoms 0.47 m, pod bottom 0.20 m above the ramp) | — | — | traction motors | — | wheel speeds | — | — | — |
| 12 | Afloat detection | all four arm sensors at full rebound for 3 s (wheels unloaded) | — | — | — | — | arm sensors ×4, hull water-level sensor | — | — | not afloat within 20 m → reverse out |
| 13 | Carriers ×4 | HIGH → −2° (wheels up to the stop) | corner pivot axes | −40° | 4 actuators (unloaded) | pins at −2° | carrier sensors, pin switches | none (afloat) | — | a corner not reaching −2° → allowed, drag only |
| 14 | Traction | land drive torque to zero (motors free); brakes released | — | — | — | — | inverter state | — | — | — |
| 15 | Controller | declares **WATER**: pod enabled, pod-follow steering active, 9 km/h cap, kill cord and seat switch armed, amber lines steady | — | — | — | — | all of the above | — | — | — |

Time: ~8 minutes, of which 5 are inflation. Hard interlocks: the pod cannot be enabled with a stay switch open or a chamber below pressure; the vehicle cannot leave HIGH on the ramp with the rails up (tubes would ground).

## 14. WATER → LAND

| Step | Action | Confirmation |
|---|---|---|
| 1 | Approach the shore at ≤ 3 km/h; carriers −2° → LIFT (50°) so the tyres reach 0.80 m below the waterline and touch the bottom early | carrier sensors, pins |
| 2 | Wheels touch (arm sensors leave full rebound on ≥ 2 corners); land drive enabled at 3 km/h with the pod still running | arm sensors |
| 3 | Pod stops, arm retracts 65° and locks before the pod's depth (0.15 m under the tyre bottoms at LIFT) can ground | pod pin switch |
| 4 | Vehicle drives out on the wheels in LIFT, then HIGH once clear (tube bottoms 0.47 m above ground) | — |
| 5 | Stop above the waterline; Park; tubes deflate (blower reversed, 3 min); rider rolls each tube into the cavity; rails swing up; rail latches closed | rail-up switches, stay switches open, tube pressure 0 |
| 6 | Drain valves open; bilge pumps run until dry; seat hatch may open | float switches |
| 7 | Brakes: two full applications at walking pace to dry the discs (inboard discs were immersed) | brake pressure, deceleration |
| 8 | Carriers HIGH → ROAD; pins; wheel IDs; steering pod-follow map off | standard ROAD declaration |
| 9 | Fresh-water flush reminder (salt); IMD trend logged | — |

Safe land configuration is reached at step 8; steps 5–7 can be completed later if the rider chooses to drive in HIGH with the rails still down (the interlock allows HIGH with rails down at ≤ 10 km/h on a beach, never ROAD).

## 15. Emergency modes and failure table

**SAFE LAND STATE:** ROAD or HIGH, pins engaged, rails latched up, tubes deflated, pod stowed and pinned, drains open.
**SAFE WATER STATE:** afloat, both tubes ≥ 0.18 bar in all chambers, stays locked, pod deployed and pinned, land drive off, kill cord in.
**TRANSFORMATION ABORT STATE:** whatever is deployed stays deployed and locked; nothing else moves; speed 0 on land or displacement drift afloat; the rider is told which gate failed. Retraction of a deployed item is never automatic.

| Failure | Detection | Safe state | Mechanical backup | Recovery |
|---|---|---|---|---|
| Power loss (48 V / 12 V) mid-transformation | rail monitors | ABORT: pins hold the carriers, stays hold the rails, tube valves hold pressure (check valves), pod pin holds | all locks are spring-applied | 12 V backup runs pumps and one pin release; hand-crank the carriers; tubes deflate by hand valve |
| Carrier actuator failure | as in the land studies | ABORT; afloat the wheels stay where they are (drag only) | pin | as in the land studies |
| Lock (stay) failure on a rail | stay switch | tubes not inflated (on land) or, afloat, 9 → 4 km/h cap and return; the rail can rotate up under wave load, pushing the tube toward the tyre | the hinge stops at 90° up; the tube fabric tolerates contact | re-seat the stay; the pin is manual |
| Hull (tube) deployment failure: a chamber does not reach pressure | pressure sensors | ABORT on land: deflate, rails up. Afloat: 3-chamber margin (2.1° heel), return at 4 km/h | CO₂ re-inflation | patch kit |
| Tube fully lost afloat | all three sensors of one side at 0 | heel 29°, cockpit floods; vehicle floats swamped on foam + the other tube **only with the 0.10 m³ additional foam (open item)** | foam | rider stays with the vehicle; tow |
| Pod failure (motor, actuator) | current, angle sensor | drift; wheel paddling at 1–2 km/h with torque vectoring for steering; anchor | pod spring-centres | tow or paddle to shore |
| Wheel deployment failure (a carrier will not go to LIFT for exit) | carrier sensor | exit on three lowered wheels at walking pace | pins | crank by hand |
| Sensor disagreement (any pair) | 2-of-3 logic | ABORT; keep state | locks | replace sensor |
| Flooding of the tub | float switches, high-water alarm at 50 mm | pumps on; return; if > 150 mm the rider leaves the water at the nearest shore; swamped flotation keeps it afloat | foam + tubes | find the leak (cartridge bores, valves, hatch) |
| Asymmetric deployment (one rail down, one up) | rail switches | tubes not inflated; on land only | — | complete or reverse the rail |
| Collision afloat (tube against a rock) | pressure drop | as chamber loss | multi-chamber | patch |
| Beaching with the pod down | arm strain (current), impact | pod arm pin sized for 3 kN; the arm folds up on its stop if the pin shears (designed fuse) | fuse pin | replace the pin |

## 16. Safety

- Water mode is only ever declared from HIGH on a ramp with every gate above satisfied; the pod is inhibited by hardware (stay switches and pressure switches in series with the pod inverter enable) as well as by software.
- Kill cord and seat switch cut the pod; the wheels' drive is off afloat.
- Category D only (sheltered, Hs ≤ 0.3 m); the freeboard margin is 0.12 m over a 0.2 m crest.
- The vehicle floats swamped with both tubes; the *swamped + one tube lost* case is an open item that must be closed with foam before Prototype 4.
- Throwable flotation and a paddle are stowed under the seat; the tubes double as grab surfaces.
- Regulatory: amphibious vehicles are outside the RCD and the US flotation rules; ISO 12217-3 / ABYC H-8 swamped and offset-load tests and ISO 13590's flooding/off-throttle clauses are adopted voluntarily as the safety case.

## 17. Packaging study (`calc/kinematics_amph.py`)

| Marine component | Land mode (where it lives) | During transformation | Water mode | Volume | Interferes with | Clearance result |
|---|---|---|---|---|---|---|
| Tub walls/bulkheads | are the lower body (permanent) | — | — | 0.60 m³ enclosed | pivot cartridges, tie-rods, HV/coolant (all through sealed bores/boots) | — |
| Rail (each) | vertical, is the fender side skin, Y 0.62–0.65, Z 0.62–0.84; return on the fender top | quarter-cylinder sweep r 0.37 m about (0.62, 0.62), outboard of the tyre face (0.615) | horizontal at Z 0.62, Y 0.62–0.84, flange to Z 0.47 | 2.2 × 0.22 × 0.03 | nothing (tyre face 5 mm inboard of the hinge; no steering excursion reaches the swept zone above Z 0.25 at the hinge plane) | OK |
| Tube (each) | rolled 0.006 m³ inside the fender cavity (0.11 m³) | unfolds outboard of the flange while inflating | centre (±1.09, 0.52), Ø 0.50 | 0.43 m³ each | steered front tyre: outboard extent 0.771 at 32° vs tube inner face 0.84 | 69 mm OK |
| Foam | fender cavities, 85% | — | — | 0.16 m³ | tube roll, blower (share the cavity) | OK |
| Blower/compressor | rear of the left fender cavity | — | — | 0.01 m³ | — | OK |
| Pod + arm | under the rack, centre (−1.10, 0.67), duct Z 0.52–0.82, rear face −1.25 | 65° swing about (−0.75, 0.32) | centre (−1.22, 0.15), duct Z 0–0.30 | 0.03 m³ | rack (0.85): 30 mm; hitch receiver (0.35–0.40): 120 mm; rack tip (−1.28): 30 mm; ramp in HIGH: 0.20 m | OK after lengthening the rack 0.18 m |
| Bilge pumps | tub floor at X −0.80 and +0.80 | — | — | small | battery tray (between them) | OK |
| Stays (6) | folded flat against the tub wall behind the rail | swing with the rail | 45° struts, flange to Z 0.42 | — | arch liner (cut-out) | OK |
| Wheels | as V0 | HIGH on the ramp | −2°: tyre Z 0.12–0.78 | — | fender crown 0.83: 50 mm | OK |
| Rider/footrests | inside the tub; footboards 0.11 m below the outside waterline | — | same | — | tub rim 0.85 at the knees: the footboard outer lip meets the rim | OK |
| Battery | inside the tub, dry | — | — | — | — | OK |
| Tracks/skis | never fitted afloat (kit IDs must read "wheel") | — | — | — | — | — |

Land-mode geometry changes: overall length 2.15 → 2.33 m (rack); everything else unchanged. Afloat: width 2.68 m, length 2.45 m (pod).

## 18. Structural loads (`calc/loads_amph.py`)

| Load | Value | Path |
|---|---|---|
| Tube buoyancy, static (80% of 6.8 kN on the tubes) | 2.7 kN per tube | fabric hoop → bolt ropes → flange tracks → rail |
| Wave/slam factor 2.0 | 5.4 kN per tube; 2.5 kN/m on the rail | rail cantilever (0.27 m to the tube reaction) |
| Rail bending at the hinge line | 0.67 kNm/m; plain 4 mm plate 251 MPa (fails); ribbed extrusion 72 MPa (OK vs 240 MPa unwelded 6082-T6) | rail → hinges + stays |
| Stays (3 per side at 45°) | 3.2 kN each; lock pin double shear 3.2 kN | stay → tub wall at Z 0.42 |
| Hinges (4 per side) | 1.4 kN shear each | hinge → tub wall/fender structure |
| One tube fully immersed (asymmetric) | 4.2 kN upward on one rail | as above, one side |
| Pod thrust | 1.3 kN peak | arm → hinge → rear cross-member |
| Beaching strike on the pod | 3 kN → 1.5 kNm at the hinge; pin sized as a fuse | arm → pin → cross-member |
| Tub wall/floor pressure | 7.6 kPa (0.77 m head incl. a 0.2 m wave) | 3 mm 5083 between stiffeners at 300 mm |
| Corner modules afloat | ~160 N per tyre at 2 m/s: negligible against the 7.8 kN landing case | — |
| Roll/side loading | GM 3.7 m: the tubes react 4.4 kNm of righting moment at 15° as ±2.2 kN differential on the rails, within the wave case | rails |
| Landing/beaching on the wheels | the land load cases (unchanged) | corners |
| Collision afloat | tube contact at 2 m/s: fabric and pressure absorb it; the rail sees ≤ the wave case | rail |

Overall load path afloat: water → tube → bolt ropes → flange → rail → hinges and stays → tub wall (Y 0.36) → tub floor and sills → mass. The tub wall between the hinge line (Z 0.62) and the stay foot (Z 0.42) carries 0.67 kNm/m of couple: a 3 mm 5083 wall with the fender ribs at 0.6 m pitch (already needed for the fender structure) is adequate; FEA required (Section 25).

## 19. Materials

| Part | Material | Reason |
|---|---|---|
| Tub floor, inner walls, bulkheads | 5083-H116, 4 mm floor / 3 mm walls, welded ER5356, or vacuum-infused glass/epoxy over the same geometry | marine grade, weldable to itself, proven for small hulls [MAR-2] |
| Rails | 6082-T6 ribbed extrusion, hard-anodised 25 µm, PTFE-isolated stainless hinge pins | unwelded, corrosion-resistant, extrudable ribs |
| Hinges, stays, pins | 316 stainless with PTFE bushings; lock pins 17-4PH | salt water, no galvanic couple with the anodised rail (isolated) |
| Tubes | PU-coated 1100 dtex polyester (TBD) or Hypalon-type; UV-stabilised; bolt ropes in 6082 tracks | RIB practice (unsourced here) |
| Foam | closed-cell PE, 30 kg/m³ | flotation, no water absorption |
| Pod | glass-filled PA duct, bronze or composite propeller, IP68 motor housing (anodised aluminium) with a sacrificial zinc/aluminium anode | as small electric outboards |
| Carrier housings (immersed) | as V0 (A356-T6) with hard anodising, ePTFE vents, anode boss | immersion |
| Fasteners in the wet zone | A4 stainless with isolating washers; anti-seize | corrosion |
| Coatings | ISO 12944 C5-class system on any steel (rider frame, hitch tower) [MAR-3] | salt spray |

## 20. Manufacturing

| Part | Method |
|---|---|
| Tub walls/bulkheads | laser-cut and formed 5083 sheet, MIG/TIG welded to the floor and sills (or one infused composite tub on a CNC plug at pilot volume) |
| Rails | aluminium extrusion die (open-tooling class), cut to length, CNC hinge bores, anodised; tracks machined into the flange |
| Hinges, stays | machined 316 bar; purchased gas struts and spring pins |
| Tubes | RF-welded or glued fabric by an inflatable-boat manufacturer (purchased, to drawing) |
| Foam | CNC-cut PE blocks |
| Pod | purchased motor unit; duct injection-moulded (GF-PA) or printed for prototypes; arm laser-cut/welded 5083 |
| Blower/compressor, pumps, valves, sensors | purchased marine parts |
| Drain valves, hatch | purchased marine hardware |

Nothing requires a shipyard: an inflatable-boat supplier makes the tubes, a metal shop the tub and rails, and the rest is catalogue hardware.

## 21. Serviceability

| Task | Procedure |
|---|---|
| Inspect/replace a tube | rail down, deflate, slide the bolt ropes out of the tracks (end caps removed), new tube in; 30 min |
| Patch a chamber | on the water or ashore with the RIB patch kit; CO₂ re-inflation |
| Replace a stay or pin | two bolts; visible from outside |
| Service the pod | two pins, one HV connector: the pod comes off the arm; propeller nut; anode |
| Clean the tracks/hinges | wash-down; they are on the outside of the body |
| Access the tub | seat hatch (electronics), floor drains (sediment), bilge pumps on brackets through the hatch |
| After salt water | fresh-water flush of arches, carriers, pod, tracks; check the anodes |
| Wet brakes | two applications at walking pace before ROAD |

## 22. CAD package (additions to `docs/architecture/12_cad_package.md`)

| # | Drawing | Must show |
|---|---|---|
| 1 | Land master assembly (amphibious variant) | as V0 plus: tub walls at Y ±0.36 to Z 0.85; rails as side skins; pod under the 2.33 m body; foam cavities |
| 2 | Marine master assembly | rails down, tubes at (±1.09, 0.52) Ø 0.50, pod deployed, wheels at −2°, waterline Z 0.527 |
| 3 | Hull (tub) | floor, walls, bulkheads, rim lip, penetrations (4 cartridge bores, 2 tie-rod boots, 4 bulkhead plates, drains, hatch) |
| 4 | Flotation structures | tube profile and chambers, bolt ropes, tracks on the flange, foam blocks |
| 5 | Wheel envelope afloat | tyre at −2°: Z 0.12–0.78, waterline crossing; HIGH and LIFT on the ramp |
| 6 | Corner module (immersion variant) | IP68 housing, vent, anode, seal stack |
| 7 | Propulsion pod | duct, motor, propeller, steering axis, arm, hinge, pin |
| 8 | Steering system | rack sensor → pod actuator map; wheels as rudders |
| 9 | Deployment mechanism | rail hinge line, 90° sweep, gas strut, stays, pins |
| 10 | Lock mechanism | stay pin, pod hinge pin, rail latch; switch positions |
| 11 | Seal system | cartridge bore seal, tie-rod boot, hatch gasket, drain valve, bulkhead plate |
| 12 | Transformation envelope | union of the rail sweep, tube inflation volume, pod sweep, wheel envelopes |
| 13 | Cross-section at the front axle | tub, arch, tyre, rail, flange, tube, waterline, foam (the Section 17 geometry) |
| 14–17 | Top, side, front, rear (marine) | dimensions: 2.68 m wide, 2.45 m long afloat, freeboard 0.32 m |
| 18 | Exploded assembly | rails, stays, tubes, pod, foam, valves, pumps |
| 19 | Land → Water sequence | Section 13 in 8 frames |
| 20 | Water → Land sequence | Section 14 in 8 frames |

## 23. Calculation scripts (`calc/`)

| Script | Computes |
|---|---|
| `params_amph.py` | every assumption with its tag |
| `mass_amph.py` | marine hardware and the condition table |
| `hydrostatics_amph.py` | waterline, KB, BM, GM, righting curve, heel/trim for eight cases, swamped cases |
| `kinematics_amph.py` | rail sweep, tube position, tyre clearances, ramp clearances, wheel and pod envelopes |
| `architectures_amph.py` | stowed/deployed volume and mass screening of nine architectures |
| `resistance_power_amph.py` | resistance components, shaft/battery power, speed, range |
| `loads_amph.py` | tube, rail, stay, hinge, pod, tub-wall loads and the rail section check |
| `checks_amph.py` | 29 automated checks with PASS/FAIL (28 pass, 1 fails: swamped + one tube lost) |
| `run_all.py` | runs everything |

## 24. Recommended architecture: ARC-2B AMPHIBIOUS V0

| Item | Definition |
|---|---|
| Architecture | H: watertight lower-body tub + fold-down fender rails + two inflatable three-chamber tubes + foam-filled fender cavities + stern vectoring pod; wheels stay on their carriers at the −2° stop afloat |
| Transformation | Section 13 (8 min, 5 of inflation) and Section 14 |
| Mass | curb 569 kg marine-dry (487 + 82); operating 669; maximum 694 (water cargo 25 kg) |
| Dimensions | land 2.33 × 1.24 m (length +0.18 m for the pod); afloat 2.45 × 2.68 m; tube Ø 0.50 × 2.4 m at Y ±1.09, Z 0.52 |
| Displacement | 0.694 m³ at max; buoyant volume 1.63 m³; reserve 135%; waterline Z 0.527; tub-rim freeboard 0.32 m; draft below the tyres 0.41 m |
| Propulsion | 8 kW ducted-propeller pod on a 0.50 m folding arm; 6 km/h cruise (1.9 kW), 9 km/h max; ~25 km / 4 h on 10 kWh usable |
| Steering | mechanical rack (unchanged) + pod vectoring ±35° following the rack sensor; wheels act as rudders |
| Stability | GM_T 3.70 m, GM_L 1.39 m, GZ 0.65 m at 15°; heel 0.7° for a 0.3 m rider offset; 2.1° with a chamber lost; trim 1.8° for 0.3 m rider offsets |
| Sealing | the tub only; four cartridge bores, two tie-rod boots, four bulkhead plates, hatch, drains; everything else wet by design |
| Locks | carrier pins (existing), 6 stay pins, 2 rail latches, pod hinge pin, valve check valves |
| Actuators | existing 4 corner actuators; blower + compressor; pod arm actuator (2 kN); pod steering actuator; 2 drain servos |
| Failure states | Section 15; two open items (Section 25) |
| Water regime | displacement only, category D; not semi-planing, not planing |
| Land impact | +82 kg (+16.8%), width 0, clearance 0, travel 0, actuator range 0, CG +~0.01 m, length +0.18 m, departure angle unchanged (~41°, hitch-limited), approach and breakover unchanged, acceleration −14%, braking distance +~15% at the same tyres |

## 25. DO NOT BUILD YET

Failed check (reported by `calc/checks_amph.py`, 28 of 29 pass):
- [ ] **Swamped + one tube lost sinks** (0.59 m³ available vs 0.69 needed): package ≥ 0.10 m³ more closed-cell foam (candidates: nose bay behind the radiator ~0.03, tail bay around the pod arm ~0.03, seat base ~0.03, footboard undersides ~0.02) or accept a documented double-failure limitation; the check stays red until the foam is packaged in CAD.
- [ ] **Whole-tube loss heels to 29° and floods the cockpit** (passes the < 35° survivability check, flagged): the same foam closes the consequence; pressure monitoring on all six chambers and the CO₂ re-inflation are the mitigations of the cause.

Assumptions that must be validated:
- [ ] CG afloat 0.61 m (build-up), and the land CG 0.60 m it rests on.
- [ ] Propulsive efficiency 0.45, tyre drag coefficient 0.8, residuary-resistance coefficient: tank or lake test of a scale model (Prototype 0) then full scale (Prototype 3).
- [ ] Tube pressure, fabric, chamber count, bolt-rope track loads: inflatable-boat supplier data and a pull test of the track at 2.5 kN/m.
- [ ] Rail extrusion section (72 MPa estimate), hinge and stay loads under a 2.0 wave factor: FEA and a rig test with the tube inflated against a load frame.
- [ ] Tub wall couple between hinge line and stay foot; tub penetration seals to a 0.6 m head for 2 h (cartridges, tie-rod boots, bulkhead plates).
- [ ] Carrier housing IP68 with the motor and inboard disc immersed for 4 h; hot-into-cold thermal shock; anode sizing; wet-brake recovery.
- [ ] Pod immersion (0.22 m over the duct at operating mass) against ventilation in waves; the 3 kN beaching fuse pin.
- [ ] Afloat detection by arm sensors (full rebound for 3 s) against false positives on a rough ramp.
- [ ] Wave factor 2.0 and category-D assumption; freeboard margin 0.12 m over a 0.2 m crest.
- [ ] Inflation time (5 min for 1.1 m³ to 0.2 bar) with a 12 V blower/compressor: supplier data.
- [ ] Marine hardware mass 82 kg: weigh the parts.
- [ ] Land handling with 82 kg added (mostly on the fender line and under the rack): tilt table and the ANSI/SVIA-style checks repeated.
- [ ] Every RIB-practice statement in this document is unsourced in this environment and must be verified against manufacturer documentation.

## 26. Prototype plan (integrated amphibious architecture survives; therefore:)

| Prototype | Build | Proves | Pass criteria |
|---|---|---|---|
| 0 — Scale buoyancy model | 1:4 tub + tubes + weighted mass model in a tank; also full-scale tube section (0.5 m) on a track sample | waterline, GM, righting curve, resistance vs speed (Froude-scaled), swamped case | GM within 20% of `hydrostatics_amph.py`; resistance within 30% of `resistance_power_amph.py` |
| 1 — Deployable rail mechanism | one full-scale rail (2.2 m extrusion), hinges, three stays, gas strut, on a rigid wall; load frame simulating 2.5 kN/m upward | rail stress, stay loads, deployment ergonomics, lock engagement 1,000 cycles | ≤ 100 MPa measured; stays engage every cycle; one person deploys in < 60 s |
| 2 — Wheel/corner sealing | one V0 corner module (from the land Prototype 1) immersed 4 h with the motor running at 2 kW; hot-into-cold | IP68 housing, cartridge bore seal, IMD trend, brake dry-out | dry housing; isolation ≥ 500 Ω/V throughout |
| 3 — Water propulsion test | pod on a test raft of the same displacement (700 kg), then on a floating tub mock-up | bollard thrust, speed vs power, steering response, ventilation depth | 6 km/h at ≤ 2.5 kW shaft; ≥ 900 N bollard; no ventilation at 0.2 m |
| 4 — Full-scale amphibious module | complete tub with rails, tubes, foam, pod and pumps on a ballasted frame (no drivetrain); lake test | stability cases 1–8 with people as movable ballast; swamped test; one-tube-lost test with the foam packaged | matches Section 6 within 20%; swamped floats; one-tube-lost floats |
| 5 — Integrated ARC-2B marine prototype | the land road prototype fitted with the module | transformation sequence, interlocks, ramp entry/exit in HIGH/LIFT, corners immersed with the vehicle live | 8-minute transformation; all gates verified by switches; no water in the tub |
| 6 — Land/water transformation testing | 100 cycles LAND → WATER → LAND on a real shore, salt and fresh; abort at every step; failure injection of Section 15 | reliability, corrosion, service intervals | no unsafe state reached; all aborts hold |

The full vehicle is not built first: Prototypes 0–4 need no drivetrain and settle every physics question for a fraction of the cost.

---

**Final statement.** ARC-2B can be amphibious, in the way a rigid-inflatable boat is a boat: a sealed lower body, tubes that appear from its own sides, and a small pod at the stern. It floats with large margins, it is very stiff in roll, it carries the rider dry, and it moves at walking-to-jogging pace in sheltered water. It does not plane, it does not retract its wheels into sealed bays, and it will never reach the speeds the concept boards implied; the calculations that say so are in `calc/`, and the two checks that still fail are listed above rather than hidden. The land vehicle keeps its width, clearance, travel, actuators and steering, and gains 82 kg and 0.18 m of rack. Whether that trade is worth it is a product decision; that it is physically and mechanically real is now established to the level a mechanical engineer needs to open CAD.
