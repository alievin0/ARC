# 13 — Visual design specification (Design Bible) and image-generation description

The engineering fixes the geometry (Sections 1, 2, 6); this section fixes only what is left to style.

## 13.1 Colours

| Role | Specification | Where |
|---|---|---|
| Primary | satin off-white (near RAL 9016, 20% gloss) | fender/panel band Z 0.62–0.90, fascia upper |
| Secondary | matte black (RAL 9005, ≤ 5% gloss), textured TPO | fascia lower, arch inner lips, footboards, skids, arms (powder-coat), tub |
| Accent | amber (RAL 2000 class) light lines 3 mm; amber anodised pin covers | carrier disc arcs (120°), fender underside edge, mode indication |
| Mechanical | natural clear-anodised aluminium (machined finish visible), bead-blasted | carrier discs, pivot nodes, hub faces, rack ends |
| Interior (cockpit) | black grips and seat with grey stitching; display bezel black; one amber "confirm" button | |
| Variant M | hull below the sheer in matte black; sheer line amber | |

## 13.2 Materials
Metal: clear-anodised 6082 (carriers, nodes), black powder-coated 5083 (arms), 4130 frame powder-coated black with C5 primer. Composite/plastic: painted ABS/TPO panels (RIM PU at volume), UHMW wear parts (natural white-grey on the arm undersides, black on skids). Rubber: 26 × 10-12 tyres with a 15 mm sidewall lug pattern; grips 30 mm Ø. Glass: 7 in display with a bonded anti-glare cover. Lighting: LED bars behind 3 mm polycarbonate, amber lines are 3 mm side-emitting fibre in aluminium channels.

## 13.3 Surface language
Panels are single-curvature developable surfaces (thermoformable) with one crease line per panel running parallel to the ground at Z 0.75 m, which is the shadow line that makes the body read as thin over the machinery. No compound "muscle" surfaces; the drama comes from the wheels leaving the arches, not from the panels.

## 13.4 Edge language and radius philosophy
A-surface edges R 6 mm; machined edges R 2 mm (visible chamfers on the discs, 1 × 45°); rider-contact edges R 12 mm; panel-to-machined transitions with a 5 mm shadow gap; arch lip radius 0.40 m (tyre radius + 70 mm) centred on the ROAD wheel centre.

## 13.5 Lighting signature
Front: one 620 × 28 mm bar at Z 0.86, amber DRL line below it. Rear: one 500 mm bar at Z 0.84. Sides: the four 120° amber arcs on the carrier discs, doubling as mode indicators (steady locked, breathing moving, red fault, off in ROAD unless "show" mode). Underside: amber line on the fender lower edge. No other lamps.

## 13.6 Branding and logo placement
"ARC-2B" 60 mm on the fascia below the bar; 40 mm on each rack side rail; the "A" mark debossed 3 mm in each carrier disc cover and printed on the display boot screen. No badges on panels.

## 13.7 Fastener visibility
Zero on A-surfaces. Four quarter-turn fasteners on each disc cover (visible, black, part of the mechanical band). Torque-striped hex heads on the nodes are visible from below only.

## 13.8 Panel architecture
Left and right fender/side panels (one piece each, nose to rack), fascia upper, fascia lower skid, seat, two footboards, four disc covers, rack rails, rear light housing, tub floor cover strips. Twelve exterior parts.

## 13.9 Mechanical visibility
Visible by design: tyres/wheels, boxed arms, carrier discs, coil-overs through the arch, hitch, (SNOW) skis and cassettes. Hidden by design: actuators, pins, motors, half-shafts (behind the arm), harness, coolant, battery, inverters, rack.

## 13.10 Protective elements
Front skid (TPO, replaceable), UHMW strips on arm undersides and disc rims, arch liners, footboard lips 40 mm, rear rack as the rear bumper, node plates. A brush guard is an accessory bolted to the front beam.

## 13.11 What the vehicle should look like (CAD/image-generation description)

*Silhouette.* A low, wide, single-seat electric ATV, 2.15 m long, 1.24 m wide, with the fender line at 0.83 m and the seat at 0.88 m; four large exposed 26-inch knobby tyres fill 80% of the body height; the body is a thin satin-white shell floating over black machinery; short overhangs (0.40 m front, 0.45 m rear).

*Proportions.* Wheelbase 1.30 m, track 0.98 m; tyre outer faces flush with the fender edges; wheels dominate; the rider sits over the rear wheels' leading edge with knees ahead of the rear arches.

*Front.* A matte-black fascia raked 16° with one narrow horizontal white light bar 620 mm wide near its top; below it a stepped-back nose with a black skid; below the nose, between the wheels, the two leading arms in black and the front carrier discs in bright anodised aluminium are visible; no grille, no bull bar.

*Side.* Three bands: white panel band with two large round arches; a mechanical band showing a 300 mm anodised disc at each corner on the body side (slightly ahead of the front wheel, slightly behind the rear wheel… no: the front disc is *behind* the front wheel centre by 0.49 m, the rear disc *ahead* of the rear wheel centre by 0.49 m, i.e. both discs sit under the rider, 0.32 m apart), with black boxed arms reaching outward to the wheels (forward from the front discs, rearward from the rear discs); an all-black underbody band with a flat floor. In ROBOTIC mode the wheels hang 0.20 m lower and 0.10 m closer to the discs, leaving visible space above each tyre inside the arch.

*Rear.* A 500 mm horizontal light bar under a flat rack; a 50 mm square hitch receiver in a black cross-member; the rear carrier discs visible at the body sides; optional track cassettes extend behind the rack.

*Top.* Flat white fenders, black footboards inboard of them from the front arches to the seat, a narrow black seat, a 22 mm handlebar with a 7 in display in the pad; nothing on the rack but its rails.

*Cockpit.* Straddle seat 0.36 m wide, grips at 1.16 m, mode selector and amber confirm button under the left thumb.

*Wheels and suspension.* 12 in machined-face wheels, 4-stud; one coil-over per corner visible through the arch between the arm and the carrier; inboard brake discs not visible.

*Corner modules.* The four anodised discs with a 120° amber light arc each; behind each a black boxed arm 0.50 m long.

*Body panels.* Twelve parts, 3 mm gaps, single crease at 0.75 m height, no visible fasteners.

*Lighting.* White front bar, red rear bar, amber lines on the discs and fender undersides.

*Materials and colours.* Satin off-white panels, matte black TPO/tub/arms, clear-anodised aluminium discs and nodes, amber accents, black tyres.

*Mechanical exposure.* Arms, discs, coil-overs, hitch, tyres exposed; nothing else.

*Modes for a sequence.* ROAD: tyres fill the arches, body 0.28 m clear. ROBOTIC: body 0.48 m clear, wheels dropped and pulled toward the discs. SKI: front wheels replaced by 1.10 m white skis under the same knuckles; rear wheels replaced by 1.30 m black track cassettes on the same hubs; the body 60 mm higher at the rear. MARINE (variant only): a longer, wider black hull under the white panels, the four wheels swung up beside the rider's legs and hips above the waterline, a jet nozzle at the transom.
