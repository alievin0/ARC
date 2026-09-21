# Part 14 — What can be outsourced

No single factory builds this vehicle. The split below follows the industry pattern (powersports OEMs buy shocks, tracks, motors and inverters; amphibian builders buy jets and hulls). Supplier names are examples whose product classes were seen in this study; **none has been contacted or verified for availability, IP rating or price** (see `REFERENCES.md`, sections H and J).

| Part / subsystem | A. CNC shop | B. Automotive fabrication shop | C. Robotics company | D. EV drivetrain supplier | E. Suspension manufacturer | F. Track manufacturer | G. Marine engineering company | H. Composite manufacturer | I. Final integrator |
|---|---|---|---|---|---|---|---|---|---|
| Pivot housings, carrier housings (billet), lock sectors, knuckle adapters, ski/track hub adapters | **make** | | | | | | | | spec, inspect |
| Central platform sills, floor plate, nodes; hitch tower; rider frame (4130) | plate/nodes | **weld, bend, assemble** | | | | | | | design, test |
| Arm (welded aluminium box or casting) | machine root boss | **weld** | | | | | | | |
| Transformation actuator (6–10 kN, IP69K, CAN) | | | | | | | | | **buy** (Thomson/LINAK/TiMOTION class [ACT-1][ACT-2][SUP-5]) |
| Lock pin/solenoid assembly | pin | | | | | | | | buy solenoid, assemble |
| Interlock controller, redundant sensors, transformation software | | | **develop** (safety-rated controller, dual-channel sensing [FS-2]) | | | | | | own the safety case |
| Traction motors + 6:1 reduction (4×), inverters (4×), DC-DC, charger, VCU base software | | | | **supply** (EMRAX/Cascadia class; powersports-scale suppliers [MOT-4][MOT-7]) | | | | | integrate |
| Battery pack (12 kWh, IP67, BMS, contactors, IMD, HVIL) | | | | **pack integrator** (UN R100/UL 2580 capable) | | | | | HV safety sign-off |
| Coil-overs (semi-active option) | | | | | **buy** (Fox/Elka/Öhlins class; not verified) | | | | |
| Steering rack + EPS, brakes, hubs, half-shafts, wheels/tyres | | ATV/UTV supply chain | | | | | | | buy |
| Ski adapters + skis; track cassettes (custom, based on production kits) | adapters | | | | | **design-for-manufacture and supply** (Camso/Soucy/Mattracks class; note active patents [PAT-19][PAT-20]) | | | |
| Sponsons (rotomoulded), swim-mode jet module (15–30 kW) | | | | | | | **buy/adapt** (ZeroJet class [JET-7]) | | |
| Marine variant hull (5083 tub) or infused composite hull; arch flaps; bilge; jet pump 155–160 mm | | | | | | | **naval architecture, hydrostatics, hull scantlings, jet installation, inclining test** | **infused hull option** | |
| Body panels (thermoformed → RIM), seat, lighting | | | | | | | | **thermoform/RIM** | styling, fit |
| Harness, thermal loop | | harness shop | | | | | | | |
| Homologation, owner's manual, CPSC action plan / EU type approval | | | | | | | | | **own** |

## 14.1 Who must be in the room from day one

1. **The integrator** (the ARC-2B team): owns the corner-module design, the safety case, the interlock software, homologation, and every interface drawing.
2. **A safety-rated controls partner** (robotics/automotive functional-safety house): the transformation controller is the one subsystem with no powersports precedent.
3. **A pack integrator** who has passed UN R100 / UL 2580 tests before.
4. **A track/ski manufacturer** early, because the cassette geometry, sprocket PCD and anti-rotation hardpoint fix the rear module design and because their patents are the most active in the field.
5. **A naval architect** before any marine hardware is bought; the hydrostatics decide the variant's size.

## 14.2 What should not be outsourced

- The carrier/arm/pivot mechanism design and its test rig (Stage 1–2): it is the product.
- The interlock logic and the mode state machine: the safety case must be owned.
- The kit interface (hub PCD, adapter switch, kit ID): it defines the ecosystem.

## 14.3 Supplier verification status

Every supplier class above was identified from product classes seen in search results or mirrored documents. Battery module suppliers, suspension makers, track makers, jet-pump makers, sealed-bearing makers and brake makers **could not be verified at all in this environment** (no reachable page). Each needs a direct request for quotation with the interface drawings from Part 4 and Part 8 before Stage 1.
