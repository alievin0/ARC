# 4 — Chassis architecture

## 4.1 Structural layout

```
 TOP VIEW (body frame; X forward → ; Y up the page)
                                       +1.00 nose
      ┌──────────────────────────────────────────────┐
      │  rider frame (4130 tube) bolted to the sills  │
      │                                              │
 Y+0.30 ═══════════ LEFT SILL 120×60×4 6082 ══════════════   ← from X −0.75 to +0.75
      │   ▣ rear-left node        ▣ front-left node    │        nodes at X −0.161 / +0.161 on the outer sill faces
      │   ┌────────── battery tray ──────────┐         │
      │   │  X −0.50 … +0.40, Y ±0.25, Z 0.29…0.47 │   │
      │   └───────────────────────────────────┘         │
      │   ▣ rear-right node       ▣ front-right node   │
 Y−0.30 ═══════════ RIGHT SILL ═══════════════════════════
      │  cross-members: X −0.75 (hitch beam), −0.35, +0.35, +0.75 (front beam)  │
      └──────────────────────────────────────────────┘
     −1.10 rack
```

| Element | Design | Load role |
|---|---|---|
| **Main rails (sills)** | two 6082-T6 extrusions 120 × 60 × 4 mm, X −0.75…+0.75, Y ±0.30, Z 0.29…0.41; bonded + bolted to the floor | carry bending from the four nodes to the rider frame and the battery; the primary longitudinal members |
| **Tub floor** | 3 mm 5083-H116 laser-cut plate bonded/riveted under the sills, X −0.55…+0.55, full width 0.60 m; 4 mm UHMW skid under the battery | shear panel that gives the sill pair torsional stiffness; battery protection; on the M variant this becomes the 4 mm watertight tub |
| **Cross-members** | four: front beam (X +0.75, also the bumper mount), +0.35 and −0.35 (battery bay ends, also the seat-frame feet), rear/hitch beam (X −0.75, 60 × 60 × 4 steel welded into the hitch tower) | complete the torsion box with the floor; hitch loads |
| **Pivot nodes (4)** | machined 6082-T6 blocks 160 × 160 × 120 mm bolted to the outer sill faces at X ±0.161 with 8 × M12 10.9 and 2 dowels; each carries the pivot cartridge (2 taper rollers, Ø50 shaft), the lock sector seat and the actuator chassis anchor | the only place corner loads enter the chassis |
| **Battery structure** | the tray is a 5083 box bolted from below to the two middle cross-members and the sills (4 × M10 + 2 shear pins); it is not a structural member, but it is inside the torsion box | crash: protected by the sills laterally and by the cross-members longitudinally; the tray never carries chassis loads |
| **Rider frame** | 4130 tubes 25.4 × 2.0 mm (FSAE Size A minimum [STR-1]): two seat rails from the +0.35 cross-member to the rack, a steering mast from the front beam to the bar clamp, two side loops carrying the footboards | rider mass (static, 5 g landing), handlebar loads, rack loads; bolted to the sills at six feet so it can be replaced without touching the platform |
| **Rack / rear beam** | part of the rider frame, ends at X −1.10 | cargo 50 kg; rear impact |
| **Suspension mounting points** | coil-over upper mount and actuator anchor are on the **carrier** and the **node**, never on the rider frame | keeps suspension loads out of the tube frame |
| **Corner module mounting** | node bolt pattern only | one interface, four identical modules |
| **Underbody protection** | UHMW skid on the battery, TPO arch liners, aluminium plate under each node | |

## 4.2 What carries load, what must not

| Must carry | Must not carry |
|---|---|
| Sills + floor + cross-members: every corner load, rider load, hitch load, battery inertia | Battery tray: no chassis loads (mounted on isolators, never a shear panel) |
| Pivot nodes: every wheel force and moment | Body panels: none (thermoformed, snap + quarter-turn fasteners) |
| Carrier → lock pin → node: all driving loads in every mode | Transformation actuator: no driving load (only transformation and self-lift loads) |
| Rider frame: rider, bar, rack | Fender / arch liner: sand and mud only |
| Hitch beam: SAE J684 Class 1 loads into both sills | Arms: never the hitch (chassis-mounted by rule) |

## 4.3 Load paths

**Vertical wheel load (bump, landing)**
```
Tyre → hub → upright → arm (bending, 0.50 m) → pivot cartridge (shear) and coil-over (through the motion ratio)
     → carrier (spring seat + pivot) → lock pin / sector → pivot node → sill (bending) → floor + cross-members (shear)
     → opposite sill and the other three nodes
```

**Lateral (cornering, kerb)**
```
Tyre → upright → arm (torsion about its own axis, 0.15 m wheel offset) → pivot cartridge (bearing moment, 150 mm spacing)
     → node → sill (torsion) → floor shear panel → opposite sill
```

**Longitudinal (braking, inboard discs)**
```
Tyre → hub → half-shaft (brake torque) → carrier reduction/disc → caliper on the carrier → carrier → pin → node
Tyre longitudinal force itself → upright → arm (compression/tension) → pivot → node
```

**Drive**
```
Motor (on carrier) → 6:1 reduction → half-shaft → hub → tyre; reaction torque stays on the carrier → pin → node
```

**Rider**
```
Seat/footboards/bars → rider frame → six feet → sills (between the +0.35 cross-member and the rack)
```

**Hitch (towing, tongue)**
```
Coupler → hitch tower (4130) → rear beam → both sills (longitudinal, vertical) → floor (transverse)
```

**Frontal impact**
```
Bumper beam → front cross-member → both sills (axial) → floor and battery bay cross-member (the battery is behind the +0.35 member and never in the crush zone)
```

**Torsion (one wheel up, diagonal down)**
```
Diagonal nodes → sills in opposite bending → floor + cross-members in shear → target stiffness to be measured (IMU twist test, Prototype 3); no published value exists for this class [STR-4]
```

## 4.4 Serviceability of the chassis

- The platform (sills, floor, nodes, battery) is one sub-assembly; the rider frame is another; the four corner modules are four more. Any of the six can be replaced with hand tools.
- The battery drops from below on four bolts with the vehicle in LIFT on both rear corners (the vehicle raises itself 0.28 m).
- No welds on the aluminium platform in the load path except the floor-to-sill bonded/riveted joint; the 4130 rider frame is welded and designed at welded allowables (Sy 180 MPa [STR-1]).
