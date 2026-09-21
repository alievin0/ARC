# 1 — Design language (in geometry, not adjectives)

Every statement below is tied to the master geometry of Section 2 and to the
kinematic envelopes computed in `calc/kinematics.py`. Where a value is a
styling choice rather than a physical necessity it is marked **(style)**;
where it is forced by engineering it is marked **(forced)**.

## 1.1 Category and character

| Item | Definition |
|---|---|
| Category | Straddle-seat, handlebar-steered, four-wheel electric off-road vehicle (ATV class); one rider; optional second-generation two-up |
| Character | **Technical-premium.** The vehicle shows its mechanism where the mechanism is the product (the four corner carriers) and hides everything else (battery, inverters, harness, actuators, cooling) behind smooth panels |
| Style words, translated | *Industrial* = visible machined aluminium carrier discs and exposed arms; *Premium* = tight, consistent panel gaps (3 mm target) and no visible fasteners on A-surfaces; *Minimal* = one lighting element per face, no fake vents; *Technical* = every visible surface break coincides with a real part boundary (fender/panel, panel/carrier); *Rugged* = every lower edge is a replaceable UHMW or TPO wear part; *Futuristic* = the wheels visibly drop out of the fenders in HIGH mode, which no ATV does |

## 1.2 Proportions and stance (body frame, ROAD static)

| Parameter | Value | Why |
|---|---|---|
| Wheelbase / overall length | 1.30 / 2.15 m = 0.60 | ATV class (benchmarks 0.58–0.62); short overhangs read as "capable" and are what the tyre sweep allows: nose ≥ +1.00 m (forced by the front tyre at full droop, `kinematics.py`), rack end −1.10 m |
| Track / overall width | 0.98 / 1.24 m = 0.79 | tyre outer faces at ±0.615 m; fenders end at ±0.62 m, so the tyres are flush with the body side in plan **(style, but also the maximum for a 1.25 m trail-width class)** |
| Wheel diameter / body height at the fender line | 0.66 / 0.83 m = 0.80 | the fender crown is forced to ≥ 0.83 m by the tyre top at full bump (0.78 m + 50 mm); a 0.80 ratio makes the wheels the dominant visual mass, which is the concept's identity **(forced + style)** |
| Wheel exposure | full: the tyre is uncovered from the hub centre downward on the outside; the fender covers only the top 120° of the tyre in ROAD | anything lower collides with the sweep in HIGH+bump |
| Seat height / wheel diameter | 0.88 / 0.66 = 1.33 | ATV ergonomics; the rider's hip sits above the rear carrier |
| Ground clearance / wheel radius | 0.28 / 0.33 = 0.85 in ROAD; 0.48 / 0.33 = 1.45 in HIGH | the underbody is a flat tub between the sills; in HIGH the vehicle stands visibly "on tiptoe" |

## 1.3 Exterior architecture, element by element

**Front-end.** A single horizontal light bar 620 mm wide, 28 mm tall, centred at Z = 0.86 m, recessed 20 mm into a matte-black fascia whose surface rakes rearward 16° from vertical between Z = 0.70 and 1.00 m. Below the bar the fascia steps back 60 mm to a recessed grille-free structural nose (the bumper beam cover) whose lower edge at Z = 0.55 m is a replaceable black TPO skid. Between the nose and the front tyres the leading arms and the front carriers are visible from ahead: the "eyes above, machinery below" layout is the identity element on every board and it survives because the front pivots are behind the wheels, leaving the nose clear **(forced: no pivot housing in the nose)**.

**Side profile.** Three horizontal bands: (1) the fender/panel band from Z = 0.62 to 0.90 m, white or body colour, one continuous surface from nose to rack with two arch cut-outs of radius 0.40 m centred on the wheel centres (the arch radius is the tyre radius + 70 mm, forced); (2) the mechanical band from Z = 0.30 to 0.62 m, where the machined carrier discs (Ø 0.30 m, natural anodised) sit on the sills at X = ±0.161 m and the black boxed arms run outboard to the wheels; (3) the underbody band below Z = 0.30 m, black, with the tub floor and skid plates. In HIGH the wheels move 0.204 m down and 0.095 m inward along X, so the arch cut-outs no longer frame the tyres, which is intended: the mode is legible from ten metres.

**Rear profile.** A horizontal tail light 500 mm wide at Z = 0.84 m under the rack; the two rear carrier discs visible below the rack at the body sides; the 50 mm hitch receiver centred at Z = 0.35 m in a black structural cross-member cover **(forced: the hitch is chassis-mounted)**. The rear track cassettes, when fitted, extend to X = −1.15 m; the rack is set at X = −1.10 m so the cassette stays visible behind it.

**Underbody.** Flat 5083 floor from X = −0.55 to +0.55 m at Z = 0.28 m (the tub); a 4 mm UHMW skid on the battery zone; open arches; no tunnels or exposed lines. The two pivot nodes per side are the only protrusions below the sills (Z ≥ 0.29 m).

**Cockpit.** Straddle seat 0.36 m wide at the hips narrowing to 0.28 m at the knees, top at Z = 0.88 m, front edge at X = +0.10 m; footboards from X = −0.25 to +0.23 m at Z = 0.42 m, 0.18 m wide (Y 0.18–0.36) with a 40 mm raised outer lip; the footboard length is limited by the front tyre sweep in HIGH+bump **(forced, `kinematics.py`)**. Handlebar grips at X = +0.28 m, Y = ±0.36 m, Z = 1.16 m (TBD by ergonomics) on a 22 mm bar; a 7 in display in the bar pad; mode selector and confirm button under the left thumb, throttle under the right.

**Lighting signature.** One amber 3 mm light line runs along the top edge of each carrier disc cover (a 120° arc) and along the underside of the fender edge; it is the same amber as the boards, used only where a moving part meets a fixed one, so the light line is also the mode indicator (steady = locked, breathing = moving, red = fault) **(style tied to function)**.

**Branding.** "ARC-2B" in 60 mm letters on the front fascia below the light bar and on both rear rack side rails; the "A" mark debossed 3 mm into each carrier disc cover.

**Surface transitions and panel gaps.** Panels meet at real part boundaries only: fender/sill, sill/carrier cover, fascia/fender. Gap 3 ± 1 mm at all thermoformed-to-thermoformed joints; 5 mm where a panel meets a machined part (thermal growth). Edge radii: 6 mm on A-surfaces, 2 mm on machined edges, 12 mm on any edge the rider's leg can touch.

**Protective structures.** Front bumper beam (4130, 32 × 2 mm) inside the nose at Z = 0.55–0.65 m; rear rack as the rear beam; UHMW wear strips 8 mm thick on the arm lower faces and the carrier disc rims (sand and rock contact); brush guards are an accessory, not the base design.

**Visible vs hidden.** Visible: tyres, wheels, arms, carrier discs, coil-overs (through the arch), hitch, light bars. Hidden: battery, inverters, DC-DC, harness, coolant loop, actuators (inside the sills behind the carrier discs), pins and sectors (behind the disc covers), motors (inside the carriers), steering rack.

**Service panels.** Each carrier disc cover (Ø 0.30 m, 4 quarter-turn fasteners) exposes the sector, pin, actuator rod end and the motor coolant fittings. The seat lifts on a latch to expose the HV junction box, MSD and DC-DC. The footboards unclip to expose the sill harness runs. The floor tub has no service access from above; the battery is dropped from below on four bolts.

**Fasteners.** None on A-surfaces. Quarter-turn on service covers, torque-striped 10.9 hex on structure, stainless on anything in the arch.

**Material transitions.** Painted thermoformed panels (white/body colour) → matte-black TPO (fenders' inner edges, skids, footboards) → natural anodised machined aluminium (carrier discs, pivot nodes) → black powder-coated boxed aluminium (arms) → rubber (tyres, grips). The sequence is always light-to-dark-to-metal from top to bottom, so the vehicle reads as a light body floating over dark machinery on bright hubs.
