# Part 4 — The corner module

> **Revision note (V0 architecture).** `docs/architecture/` supersedes two decisions in this part after packaging and side-view-geometry checks: the front arm is **leading** (pivot behind the wheel, under the footboard), not trailing, and the brakes are **inboard** on the carriers. Reasons and numbers: `docs/architecture/02_master_geometry.md` §2.2 and `docs/architecture/calc/kinematics.py`.

This part designs one complete corner module of the selected architecture
(Part 3, Option C: trailing arm + actuated coaxial carrier). The front and
rear modules share the carrier, pivot, actuator, lock and sensor set; they
differ in the arm end (steered knuckle at the front, fixed hub at the rear)
and in the kit interface (ski saddle at the front, track cassette at the
rear). All dimensions are RC-0 assumptions from `calc/params.py`.

## 4.1 Bill of components (one corner)

| # | Component | Function | Design choice (RC-0) | Purchased / made |
|---|---|---|---|---|
| 1 | **Main chassis attachment** | carries the whole corner into the central platform | Machined aluminium (6082-T6) pivot housing bolted to a steel/aluminium chassis node with 4 × M12 10.9 bolts on a 160 × 160 mm pattern; locating dowels; the housing carries the pivot bearing pair and the lock sector | made (CNC) |
| 2 | **Upper structural link = carrier** | positions the spring anchor, motor and lock relative to the chassis | Cast or machined aluminium housing, coaxial with the pivot, rotating on the same shaft; carries: coil-over upper mount, traction motor + reduction, lock sector plate, actuator lever, absolute angle sensor | made (casting for volume, CNC billet for prototypes) |
| 3 | **Lower structural link = arm** | reacts wheel loads to the pivot; carries the spring lower mount and the hub | Boxed trailing arm, 450 mm pivot-to-wheel-centre, formed 3 mm 5083/6082 sheet welded box or a hollow aluminium casting; arm root is a 60 mm bore on a 50 mm hardened steel pivot shaft; arm is offset outboard so the wheel sits 150 mm outboard of the arm plane | made |
| 4 | **Wheel carrier / upright** | front: steered knuckle on kingpin; rear: fixed hub carrier | Front: knuckle with two sealed spherical bearings (kingpin inclination ~8°, caster ~5°); rear: hub carrier integral with the arm end | purchased (ATV knuckle-class forgings) or made |
| 5 | **Wheel / hub** | 12 in aluminium wheel, 26 × 9-12 tyre; 4 × 110/115 mm hub bolt circle | Sealed unit bearing hub (UTV class), flange also carries ski/track adapters | purchased |
| 6 | **Brake** | service + regenerative; parking at the rear | Hydraulic single-piston floating caliper on a 220 mm stainless disc (ATV class) at each corner; rear calipers with mechanical parking lever; brake hose routed with a 150° service loop at the pivot | purchased |
| 7 | **Steering interface (front)** | tie-rod inner joint on the pivot axis (Part 3.5) | Rack on the chassis between the front modules; inner tie-rod ball joints at the pivot axis line; outer joint on the knuckle arm; steering angle ±35° | purchased rack (EPS UTV class) + made tie-rods |
| 8 | **Spring/damper** | wheel rate ~13 N/mm at 0.55 motion ratio → ~43 N/mm coil; 2.63 kN at ride height | ATV coil-over (piggyback reservoir), 110 mm stroke, between the carrier upper mount and the arm | purchased |
| 9 | **Transformation actuator** | rotates the carrier 15° → 60° | Electromechanical ball-screw linear actuator, 6–10 kN, 150 mm stroke, IP69K static, integrated brake, absolute feedback, CAN; mounted chassis-to-carrier lever at 160 mm radius | purchased (Part 1, [ACT-1..3]) |
| 10 | **Mechanical lock** | holds the carrier without power or software | Spring-applied, solenoid-released hardened pin (Ø20 mm) into a 5°-pitch sector plate on the carrier; 24 V hold-open solenoid; manual release access | made + purchased solenoid |
| 11 | **Position sensors** | carrier angle, arm angle, lock state | Two independent absolute magnetic angle sensors (carrier/chassis and arm/carrier), IP67, redundant outputs; lock pin position via two inductive proximity switches (engaged/retracted); actuator internal position; wheel speed from the hub | purchased |
| 12 | **Hard stops** | limit carrier and arm regardless of control | Carrier: bonded polyurethane stop blocks at 10° and 65° on the pivot housing; arm: bump stop in the coil-over plus a rebound stop strap | made |
| 13 | **Sealed bearings/joints** | pivot shaft, knuckle, spring eyes | Pivot: two taper-roller bearings (50 mm bore, 150 mm apart) with double-lip seals and an outer labyrinth; knuckle: sealed spherical plain bearings; spring eyes: polyurethane bushings; CV boots on the half-shaft | purchased |
| 14 | **Service access** | maintenance without removing the module | Actuator, lock solenoid, coil-over and motor coolant fittings are reached from the wheel arch with the carrier at 60° and the wheel removed; the pivot bearing pair is a cartridge removable inboard-out after pulling the pivot shaft | design rule |

Also on the module: traction motor (see Part 7) mounted on the carrier with a
6:1 planetary reduction, driving the hub through a plunging CV half-shaft;
coolant and HV cable service loops for the 45° carrier sweep.

## 4.2 Layout

```
 SIDE VIEW, rear-left module, ROAD MODE (arm at +15°)      ↑ forward = left
                                                             
    chassis rail ══════════════════════════════════════════
                ┌────────────────────────────────┐
                │ PIVOT HOUSING (chassis)         │
                │  ┌────────────────────────┐     │  ● lock pin (spring-applied)
                │  │ CARRIER                │ ●───┼── into 5° sector on carrier
                │  │  [motor+6:1]  ◄coil-over upper mount
                │  │       ⊙ pivot axis (50 mm shaft, 2× taper roller)
    actuator ───┼──┤ lever r=160 mm          │     │
    (chassis→   │  └────────────────────────┘     │
     carrier)   └───────────┼─────────────────────┘
                            │\
                            │ \  ARM (boxed), 450 mm
                  half-shaft│  \___________ 
                  (CV, CV)  │   coil-over  \
                            │       ↓       \__ hub + brake + wheel
                                              ( W )  26 in tyre
```

```
 REAR VIEW, same module                     wheel offset 150 mm outboard of arm plane
        chassis
   ┌──────────────┐
   │ pivot housing│──── 150 mm bearing spacing ────┐
   │  [brg]  [brg]│                                │
   └──────┬───────┘                                │
          │ arm root (60 mm bore)                  │
          │══════ arm ═══════╗                     │
                             ║ upright/hub         │
                          ┌──╨──┐                  │
                          │wheel│                  │
                          └─────┘
```

## 4.3 Mechanism states

| State | Carrier angle | Arm rest angle to horizontal | Wheel centre vs road state | Lock | Actuator | Speed allowed |
|---|---|---|---|---|---|---|
| ROAD | 15° | wheel 0.116 m below pivot | reference | pin engaged | brake on, unpowered | full |
| HIGH (robotic) | 45° | wheel 0.318 m below pivot | +0.20 m body height, wheel 0.12 m forward | pin engaged at 5° steps | brake on | ≤ 25 km/h (Part 12) |
| LEVEL (robotic, continuous) | any 15°–60° per corner | — | per-corner | pin retracted while moving, engaged when settled | powered, self-locking screw | ≤ 5 km/h while pins are out |
| LIFT (self-jack) | 60° on one corner while the other three stay | — | that wheel pushes down and lifts the corner | pins on other three engaged | powered | 0 |
| KIT SWAP | corner lifted (LIFT) | — | wheel off ground | — | brake on | 0, vehicle in Park |
| RETRACT (marine variant only) | −70° | wheel 0.42 m above pivot | wheel beside hull above waterline | pin engaged | secondary drive (Part 9) | afloat only |

## 4.4 ROAD → ROBOTIC → ROAD (front and rear identical in principle)

**ROAD → ROBOTIC**
1. Controller receives a mode request; the interlock (Part 6) verifies speed
   ≤ 5 km/h, steering within ±10°, no fault flags, battery SOC and 24 V
   supply adequate, all four lock pins reported "engaged" by both switches.
2. Actuator brakes release; actuators pre-load toward the commanded direction
   (removing the pin's shear load so it can retract; a pin cannot be pulled
   under load).
3. Lock solenoids energise; both proximity switches on each pin must report
   "retracted" within 300 ms, otherwise abort (re-brake, de-energise).
4. Actuators extend at 10–15 mm/s. Carriers rotate 15° → 45° (83 mm stroke),
   all four synchronised to within ±2° by the controller to keep the body
   level; the coil-overs simply ride along, so the wheels stay loaded and
   the vehicle may creep at ≤ 5 km/h during the move.
5. The absolute carrier sensors confirm 45° ± 1°; the arm sensors confirm
   the arm is within its normal travel band (i.e. nothing is jammed).
6. Solenoids de-energise; pins drop into the nearest 5° slot under spring
   force; both switches per pin report "engaged"; the actuator brakes apply;
   the controller then declares ROBOTIC and lifts the speed cap to 25 km/h.
   Total time ≈ 8–10 s.

**Per-corner adjustment in ROBOTIC** (leveling, obstacle stepping): the same
sequence on one or two corners at a time at ≤ 5 km/h; the vehicle remains
drivable because the actuator's self-locking screw holds the load with the
pin out, and the pin re-engages at the next 5° slot as soon as motion stops.

**ROBOTIC → ROAD**: the reverse. Additional check: all four carriers must
be commanded to 15° together; if one corner cannot reach 15° ± 1° (jam,
sensor disagreement), the vehicle stays in ROBOTIC with a speed cap and a
fault, because a mixed geometry is safer at low speed than a false ROAD
declaration.

**Front module specifics.** Because the tie-rod inner joint lies on the
pivot axis, the steering angle does not change during the move (Part 3.5).
The half-shaft angle changes only with suspension travel (± ~15°), not with
carrier angle, because the motor rotates with the carrier.

**Rear module specifics.** Identical; the rear carriers also carry the
parking brake cable service loop. The hitch (Part 10) is on the chassis, so
raising the rear does not change the hitch height relative to the chassis,
only relative to the ground; towing is only permitted in ROAD (Part 6).

## 4.5 ROAD → SKI → ROAD

Part 8 and Part 17 establish that a snowmobile-class ski (≈ 1.0 m long) and
a track cassette (≈ 1.1 m long, 40–50 kg) cannot be stowed inside an
ATV-sized corner module together with a 26 in wheel. The ski/track mode is
therefore a **swap-in kit** using the module's self-lift function; the
module never has to "deploy" anything from inside itself. The sequence is
still fully defined by the vehicle:

**ROAD → SKI (front module)**
1. Vehicle stopped on firm ground, Park engaged, HV drive disabled by the
   interlock, steering centred.
2. Rider selects "Swap front-left". Controller runs the LIFT sequence on
   that corner only: the other three pins are verified engaged; the
   front-left actuator drives its carrier to 60°, pushing the wheel down;
   since the other three corners are locked and the coil-over on the lifted
   corner is bottomed by the actuator load, the body rises on that corner
   until the arm sensor shows the arm at full rebound (wheel unloaded).
   Actuator brake applies; pin engages at 60°.
3. Rider removes the wheel (4 lug nuts) and bolts the **ski adapter** to the
   hub flange: a hub-face plate carrying a transverse ski pivot pin, a
   rubber ski-pressure spring and a limiter strap. The ski saddle attaches
   to the pivot pin with one quick-release pin. This is exactly how
   production hub-mount ATV ski kits attach [SKI-2].
4. Rider confirms "kit fitted" on the HMI; the controller reads the kit ID
   from an RFID/contact tag in the adapter (ski vs track vs wheel).
5. Controller lowers the corner (carrier back to 15°), pin engages, and
   repeats for the other front corner.
6. The front modules are now in ROAD geometry carrying skis; steering works
   because the ski pivots on the knuckle's hub, downstream of the same
   tie-rods.

**ROAD → SKI (rear module)**
1. LIFT sequence on the rear-left corner as above.
2. Rider removes the wheel and mounts the **track cassette**: its drive
   sprocket hub bolts to the hub flange (drive coupling = the wheel bolt
   circle, the same as every production ATV track kit [TRK-1..4]); its
   anti-rotation link clips to a dedicated hardpoint on the *arm* (not the
   chassis, so the cassette follows suspension motion and carrier angle);
   the cassette's tensioner is pre-set at the factory and verified by a
   spring-loaded indicator (Part 8).
3. Kit ID read; controller lowers the corner; repeat on the other side.
4. With all four kits reported, the controller asks for a rider confirmation
   and then offers SNOW mode: torque limits, traction control map, speed
   cap and regen map change (Part 6). The rear carriers may be commanded to
   25° to raise the body slightly and to re-centre the cassette's approach
   angle; the front carriers stay at 15° so ski pressure remains correct.

**SKI → ROAD**: the reverse. A wheel-ID tag on each wheel lets the
controller refuse ROAD mode until four wheels are reported.

Time: with practice about 5 minutes per corner, 20 minutes total, no jack,
no lifting of the vehicle by the rider, and the only tools are the lug
wrench and the cassette's quick-release pins. This is materially better
than production track kits, which need a lift or a jack and 1–2 hours
[SKI-2], and it preserves the product promise ("one vehicle, several
modes") without any hidden deployment hardware.

## 4.6 Loads at the module interfaces (RC-0, from Part 10)

| Interface | Load case | Load |
|---|---|---|
| Pivot bearings (pair, 150 mm apart) | 5 g landing + wheel offset moment | 7.2 kN vertical; ≈ 12 kN radial per bearing |
| Lock pin (Ø20, double shear) | 5 g landing torque 3.1 kNm on 150 mm sector radius | 21 kN shear; pin stress ≈ 33 MPa per shear plane (ample; sized for wear, not strength) |
| Actuator | lifting a loaded corner | 5.1 kN (below the 6–10 kN units' dynamic rating) |
| Actuator | driving loads | 0 (brake applied, pin engaged; the lever geometry means any residual is ≤ 10%) |
| Coil-over | 3 g bump through 0.55 motion ratio | 7.9 kN |
| Arm root | 5 g landing bending | 7.2 kN × 0.45 m = 3.2 kNm; plus 1.1 kNm torsion from the 150 mm wheel offset |
| Chassis attachment (4 × M12) | 5 g landing moment + lateral 1.5 g | ≈ 3.5 kNm resolved on a 160 mm bolt square → ≈ 22 kN per bolt pair (10.9 M12 proof ≈ 70 kN each) |

## 4.7 What is new versus an ATV corner

Only three parts have no direct powersports precedent: the carrier, the
pivot cartridge with its sealed 50 mm shaft, and the lock sector. Everything
else (arm, knuckle, hub, brake, coil-over, rack, half-shaft, motor) exists
in the ATV/UTV/e-motorcycle supply chain. That is the point of Option C.
