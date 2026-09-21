# 15 — RECOMMENDED ARC-2B V0 ARCHITECTURE, BUILDABLE V0, and DO NOT BUILD YET

## 15.1 Recommended ARC-2B V0 architecture

### 1. Vehicle architecture
Single-rider electric ATV, 2.15 × 1.24 m, wheelbase 1.30 m, 487 kg curb, 150 kg payload. One central platform, four identical corner modules on identical nodes, a bolt-on 4130 rider frame, a chassis-mounted hitch. Three land modes (ROAD, ROBOTIC, SNOW) on the base vehicle; water by a removable hull first, a separate ARC-2B M variant later.

### 2. Chassis
Two 6082-T6 extruded sills (120 × 60 × 4) at Y ±0.30, four cross-members, a 3 mm 5083 tub floor as the shear panel, four machined 6082 pivot nodes on the outer sill faces at X ±0.161 (bearing span Y 0.265–0.415), battery tray between the sills (0.90 × 0.50 × 0.18 m), 4130 rider frame on six feet. Load paths in Section 4.3.

### 3. Front module
Leading arm 0.50 m (pivot behind the wheel, under the footboard) on a coaxial actuated carrier; steered knuckle (KPI 8°, caster 5°) with the tie-rod inner joint on the pivot axis; carrier-mounted motor + 6:1 with an inboard disc; ski adapter interface on the hub.

### 4. Rear module
Trailing arm 0.50 m (pivot ahead of the wheel, under the seat) on the same carrier; fixed hub; motor + 6:1 / 12:1 two-speed; inboard disc with parking brake; track-cassette interface on the hub with an anti-rotation hardpoint on the arm.

### 5. Suspension
Coil-over between arm and carrier, 0.22 m travel (0.12/0.10), motion ratio 0.55, 43 N/mm, semi-active damping option. Roll centre at ground, no camber gain (known compromise; Gen-2 semi-trailing option). Anti-dive 30%, anti-squat 28%.

### 6. Steering
Mechanical rack with EPS on the front pivot axis line, inner joints at Y ±0.26, tie-rods 439 mm, 32°/42°, turning radius 2.45 m; zero steer change over the full carrier sweep and travel (numerically proved).

### 7. Drive
Four carrier-mounted liquid-cooled PM motors (8–10 kW continuous, 15–20 kW peak) with plunging CV half-shafts; per-wheel torque control; no differential; kit drive coupling = the wheel bolt circle.

### 8. Brakes
Hydraulic, two circuits, four inboard 200 mm discs on the carriers, regen blend to 0.3 g, rear parking brake; braking unaffected by any transformation state.

### 9. Actuators
Four 48 V electromechanical ball-screw actuators, ≥ 7 kN, 120 mm stroke, 12 mm/s, spring-applied brake, IP69K static, inside the sill cavities on 160 mm carrier levers. They move; they never carry driving loads.

### 10. Locks
Per corner: spring-applied Ø20 pin into a 150 mm-radius sector with 5° slots (25.5 kN shear at 5 g), solenoid released through a hardware speed comparator, two switches, manual release; plus the actuator brake and the screw as second and third holds; PU hard stops at −2° and +55°.

### 11. Road mode
Carrier 12°; wheelbase 1.30 m; clearance 0.28 m; SSF 0.82 (CG 0.60 m TARGET); 60 km/h design; 140 Wh/km on the mixed cycle → ~73 km on 12 kWh.

### 12. Robotic mode
Carriers 12°–50° per corner in 5° pinned steps; HIGH at 38° (+0.204 m, wheelbase 1.11 m, SSF 0.61); leveling to ~12° cross-slope; obstacle stepping ≤ 0.30 m at ≤ 5 km/h; single-corner self-lift (0.28 m) for service and kit swaps; 25 km/h pinned / 5 km/h with a pin out.

### 13. Ski mode
Swap-in kits on the hubs using self-lift: front 1.10 × 0.22 m skis on hub adapters with a ski pivot, pressure spring and limiter strap; rear 1.10 × 0.30 m cassettes (13-tooth, 72.6 mm pitch, 30 mm lugs, spring/screw tensioner with an indicator switch, anti-rotation link to the arm); rear 12:1; 45 km/h cap; ~36 km on 12 kWh; ground pressure 6.3 kPa (upper edge of tracked-ATV practice).

### 14. Marine strategy
Base vehicle: no hull; optional swim kit (Ø 0.45 m sponsons, 15–30 kW jet module, ≤ 4 kn, calm water). First water product: a removable 3.2 × 1.8 m hull the ATV drives into (no retraction needed). Later: ARC-2B M variant with a 2.8 × 1.6 m planing hull, −50° retraction with hull flaps, 155–160 mm jet on an 80 kW marine motor, 20 kWh.

### 15. Electronics
~350 V class-B pack, 12 kWh, 96–100s4p 21700 NMC, IP67 vented tray, BMS, two EV200-class contactors, precharge to ≥ 90–95%, HVIL, pyro + HV fuses, iso165C-class IMD, MSD; four inverters under the seat; DC-DC 12 V/48 V; VCU + separate safety-rated transformation controller; per-corner dual absolute angle sensors, arm sensor, pin switches, kit RFID.

### 16. Safety
Mode = verified hardware states; speed caps per state; hardware-gated pin release; ISO 13849 Cat 3 / PL d target (or ASIL B); ANSI/SVIA 1-2023 Kst/Kp and brake tests in every land mode; seat switch and kill cord afloat; the failure table of Section 10.

### 17. Manufacturing
CNC nodes and prototype carriers; cast carriers at pilot volume; formed/welded 5083 arms with unwelded machined roots; extruded sills; bent/TIG 4130 rider frame; thermoformed panels; purchased motors, inverters, actuators, coil-overs, knuckles, hubs, brakes, rack; licensed cassettes.

### 18. Prototype plan
See 15.2.

## 15.2 ARC-2B — BUILDABLE V0

**What we build first: one front corner module on a rig.** Not a vehicle, not a chassis: the carrier, pivot cartridge, arm, actuator, pin/sector and coil-over, loaded by a hydraulic ram at the hub, because every other number in this document (actuator force, pin wear, seal life, bump-steer, motor thermal) is validated or falsified there for the least money.

| Prototype | Build | Proves | Pass criteria |
|---|---|---|---|
| **0 — Packaging mockup** | 1:1 foam/MJF body on a plywood chassis with real tyres, a real seat, printed carrier discs and arms that pivot; a borrowed ski and a borrowed cassette | envelopes of Section 2.3; footboard/tyre clearance; rider ergonomics; kit clearance on the hub; grip height | no interference through 12°→50° and (variant) −50°; footboard leading edge confirmed at X ≤ +0.237 |
| **1 — One complete corner module** | billet carrier, welded arm, pivot cartridge, actuator, pin/sector, coil-over, dummy hub with a wheel, on a rigid frame with a 10 kN ram | actuator force vs angle (≤ 7 kN); pin engagement 10,000 cycles with sand/ice; 5 g static with the pin in; seal 0.5 m head; −25 °C operation; wiring/coolant loop 10,000 sweeps | force ≤ 7 kN; zero pin failures to seat after unload; no set at 7.8 kN; dry after immersion |
| **2 — Front + rear transformation modules** | front with knuckle, rack stub and tie-rod on the axis; rear with motor, 2-speed, half-shaft, inboard disc; a bench half-chassis | bump-steer < 0.5° over the full sweep; half-shaft angles; motor thermal at 8 kW/1 h in the housing; brake torque through the half-shaft; sprocket drive through the hub on a rig | steer change < 0.5°; CV angle < 40°; housing < 90 °C; 800 Nm brake torque without CV damage |
| **3 — Rolling chassis** | platform, four modules, wheels, steering, brakes, LV, actuators, ballast for the pack | mass on four scales (vs 487 kg budget); torsion stiffness; static cases 1, 2, 11; ROAD↔HIGH with a rider; LIFT of one corner with a 100 kg rider; tilt table ROAD/HIGH | transformation ≤ 10 s; LIFT unloads a corner; CG within the three-wheel triangle in LIFT |
| **4 — Road vehicle** | + 12 kWh pack, inverters, cooling, VCU, panels, lighting | Wh/km (locks pack size); 0–60; brakes to ANSI/SVIA §7; instrumented drop tests to replace the g-factors; 500 km; IP spray; EMC pre-scan; inboard-brake thermal on a 2 km descent | Wh/km ≤ 160; no HVIL/IMD event; no crack at 500 km; disc < 400 °C |
| **5 — Robotic transformation** | safety controller with redundant sensing; interlocks; leveling; stepping | every Section 10 failure injected; slope refusal; speed-cap enforcement; 10,000 cycles | no pin release above 5 km/h; no mode without switch confirmation |
| **6 — Ski system** | 2 ski adapters + skis; 2 cassettes (adapted production kits first); SNOW maps | swap time; drive-coupling check; tension switch; 200 km on snow; Kst tilt in SNOW; 20° snow climb in 12:1 | ≤ 10 min per corner; no derailment; climb achieved |
| **7 — Marine feasibility / separate variant** | (a) removable hull with a 40–60 kW jet module and the drive-in cradle; (b) swim-kit sponson test; (c) M-variant hull hydrostatics and inclining test | hydrostatics vs `calc/energy_buoyancy_v0.py`; sealed-corner immersion; retraction afloat (variant) | GM ≥ +0.25 m; dry battery box; displacement speed at ≤ 15 kW |

Sequence rule: no prototype starts before the previous one's pass criteria are met, except 0 and 1, which run in parallel.

## 15.3 DO NOT BUILD YET — validation checklist

- [ ] Actuator force: 6.8 kN is derived from a 487 kg budget and a 160 mm lever; measure on Prototype 1 with the real mass.
- [ ] Lock strength and wear: 25.5 kN pin shear at 5 g; sector insert wear over 10,000 engagements; engagement under residual load.
- [ ] Bearing loads: ≈ 13 kN radial per pivot roller at 5 g with a 150 mm span; static safety factor s₀ ≥ 5 to be confirmed with a supplier.
- [ ] Chassis FEA: sills, nodes, floor shear, torsion target (none published for this class), hitch to J684 Class 1.
- [ ] Wheel travel: 0.22 m at every carrier angle without coil-over bind or strap snatch.
- [ ] Tyre clearance: node/tyre margin ≥ 0.10 m in LIFT and RETRACT; footboard/tyre Y gap raised from 5 mm to 15 mm; arch liner to the union envelope; 26 in maximum tyre.
- [ ] Steering geometry: on-axis inner joints (proved on paper), bump-steer < 0.5° on the rig; Ackermann 32°/42°; EPS maps.
- [ ] Brake capacity: inboard-disc heat rejection inside the body on repeated descents; half-shaft rating ≥ 1,000 Nm.
- [ ] Track load: 6.3 kPa at 701 kg; 1.56 kN pull per cassette; 420 Nm at the hub in 12:1; cassette patent review (Camso, Soucy, Polaris).
- [ ] Ski load: 6.7 kPa per ski (may need 0.25 m width); 4.1 kN tip impact; adapter fatigue.
- [ ] Water stability: base vehicle floats only with Ø ≥ 0.45 m sponsons (+39% reserve); variant hull GM +0.27 m at 1.5 m beam (prefer 1.6 m); every hydrostatic number is first-order and needs a naval architect.
- [ ] Battery mass: 78 kg at 150 Wh/kg for 12 kWh; pack size locked only after Prototype 4's Wh/km.
- [ ] Thermal system: 6 kW radiator; motor at 8 kW for 1 h inside the carrier; pack heater for < 0 °C charging; actuator/pin housings warmed.
- [ ] Manufacturing tolerance: ±0.05 mm bearing bores in the node and carrier; sector slot pitch tolerance vs pin engagement; arm root bonded joint qualification.
- [ ] Mass budget: 487 kg is a budget; weigh Prototype 3.
- [ ] CG height: 0.60 m (road, with rider) is a target; measure; SSF and all anti-dive/anti-squat figures depend on it.
- [ ] Load factors: 3 g / 5 g / 1.5 g / 1.2 g are unsourced assumptions; drop tests on Prototype 4.
- [ ] Rider-frame rollover case: static equivalency only; no ROPS claim.
- [ ] All supplier data: motors, inverters, actuators, coil-overs, cassettes, jet modules, bearings, connectors were identified by class, none verified against a datasheet in this environment.
- [ ] All external numbers tagged S/B/N in `docs/feasibility/REFERENCES.md`: verify from the originals before quoting.
- [ ] Homologation route: 16 CFR 1420 / ANSI-SVIA 1-2023 (US); L7e-B1 (≤ 450 kg excluding batteries) or off-road-only (EU); the marine products are outside the RCD and the US flotation rules, so their safety case is voluntary and must be written.

## 15.4 Final rule, applied

Ordered as the brief demands: safety (hardware-gated locks, speed caps, failure table) → physics (mass 487 kg, buoyancy, ground pressure) → structure (nodes, sills, load paths) → kinematics (one axis per corner, proved steering invariance) → dynamics (anti-dive 30%, SSF 0.82/0.61, wheelbase 1.30/1.11) → reliability (three holds per corner, sealed cartridge) → serviceability (self-lift, disc covers, module-as-unit) → manufacturability (job-shop processes only) → weight (no plausible path below ~440 kg) → cost (four actuators, four machined carriers, purchased everything else) → appearance (wheels leaving the arches is the only styling event, and it is free).

Two things in the original concept were changed to get there, and both are stated in Sections 2.2 and 8: the front arm orientation and brake location, and the marine strategy. The concept's visual identity survives intact.
