# 10 — Failure modes, transformation safety, environmental durability

## 10.1 Failure modes

The feasibility study lists 19 cases with detection → safe state → mechanical backup → software response → recovery (`docs/feasibility/05_failure_analysis.md`). The table below covers the cases named in the master brief, including five not in that list (motor, bearing, wheel jam, overheating of a motor/inverter, collision during transformation).

| Failure | Detection | Safe state | Mechanical backup | Recovery |
|---|---|---|---|---|
| Actuator failure (power, jam, drive fault) | CAN heartbeat, current vs position, carrier sensor static | geometry frozen; pin engaged at the nearest slot if not already; speed cap 25 km/h (all pinned) or 5 km/h (a pin out) | self-locking brake on the screw; spring-applied pin | hand-crank the screw through the disc cover; replace the actuator (4 bolts, 2 connectors) |
| Lock failure (pin not engaged / sheared / iced) | two pin switches disagree or read "out" | screw + brake carry the load; 25 km/h cap | sector hard stops (−2°/+55°) prevent collapse beyond the range even with no pin | jog ±2° and retry; de-ice; replace pin/solenoid |
| Sensor failure (carrier, arm, pin, kit ID) | 2-of-3 disagreement; out-of-range | transformations refused; mode retained; 25 km/h cap if a corner's angle is uncertain | pin holds regardless | replace; no re-zeroing (absolute, keyed magnets) |
| Power loss (48 V or 12 V) | rail monitors | everything holds: pins are spring-applied, actuator brakes spring-applied | — | restore supply; 12 V backup runs the pin release once and the bilge pumps |
| Motor failure (one) | inverter fault, phase current, temperature | torque to zero on that corner; three-wheel drive; 25 km/h | PM motor free-wheels through the planetary; brake and steering unaffected | tow or drive home at reduced speed; replace the motor from the arch with the carrier at 50° |
| Bearing failure (pivot, carrier, hub) | corner accelerometer vibration, temperature, play detected as sensor jitter | 5 km/h cap; if the pivot bearing fails, the node's hard stops and the shaft keep the arm captive | shaft shoulders and the node housing retain the arm even with a destroyed bearing | pivot cartridge replaced inboard-out |
| Linkage failure (arm, upright) | sensor step, IMU step, wheel-speed anomaly | torque cut on the corner; stop | rebound strap and hard stops keep the arm within the arch | tow; life-limited part inspection |
| Track failure (derailment, breakage) | sprocket speed vs hub speed, vibration | torque cut on that side; stop | guide horns keep a slack track on the sprocket for a stop | re-track or swap cassette (self-lift) |
| Ski failure (ski breaks, strap fails) | strap switch, steering torque asymmetry | 10 km/h; return | the adapter keeps the saddle captive on the pin (circlip) | replace ski |
| Wheel jam (debris between tyre and arch, frozen hub) | wheel-speed 0 with torque, motor current | torque cut on that corner; stop | — | clear debris; with the corner lifted the wheel is free to inspect |
| Sand contamination (sector, pin, actuator boot) | pin seating failures, actuator current trend | as lock/actuator failure | downward-open sector slots, tapered pin nose, rod boot and drain | wash-down through the disc cover; re-grease |
| Ice contamination | as above with T < 0 °C | as above | coolant-warmed housings; 150% "break-ice" solenoid pulse | thaw |
| Water ingress (carrier housing, battery box, sill cavity) | float/conductivity switches; IMD isolation trend | HV isolation warning → stop when safe → contactors open below 100 Ω/V | sealed motor (IP67 unit), vented housings, drains | dry, find leak; battery box ingress = pack inspection |
| Overheating (motor/inverter) | temperature sensors | derate to 50% then 0; coolant pump to max | thermal fuse in the inverter | cool; check coolant |
| Overheating (battery) | BMS: > 55 °C warn, > 60 °C limit, runaway signature | derate → stop → contactors open; 5-minute warning target | vent path and cell barriers | pack diagnostic |
| Collision during transformation (vehicle struck or strikes an object with pins out) | IMU shock > 3 g, actuator current spike, carrier-vs-actuator position divergence | actuators stop; brakes on; pins commanded in at the nearest slot; 0 km/h until inspected | screw + brake hold; hard stops; the arm cannot leave the arch | inspection of the sector and pin (dye check), actuator rod straightness |

## 10.2 Transformation safety: interlocks and state machine

Refuse any transformation if: speed > 5 km/h; |pitch| or |roll| > 10°; steering > ±10°; parking brake not set (for LIFT); any pin's two switches disagree; any carrier's two angle sensors disagree by > 2°; actuator-vs-sensor disagreement > 2°; 48 V < 44 V; HV SOC < 10%; kit IDs inconsistent with the requested mode; a wheel load proxy (arm sensor) shows a corner already airborne (except in LIFT).

Refuse to *declare* a mode unless: all pins report "engaged" on both switches; all carriers within ±1° of the mode's target set; actuator brakes applied; kit IDs match; (SNOW) both tension switches closed and the quarter-turn drive check passed; (MARINE) hatches, bilge, IMD, afloat and thrust gates passed.

```
ROAD ─► REQUEST ─► VERIFY (gates) ─► UNLOCK (pre-load, solenoids, 2 switches) ─► MOVE (sync ±2°) ─► VERIFY POSITION (2 sensors + arm band)
     ─► LOCK (de-energise, jog once) ─► VERIFY LOCK (2 switches each) ─► BRAKE ON ─► MODE ACTIVE (maps, caps, lights)
any failure at any arrow ─► TRANSITION_FAULT (hold, 5 km/h, message) ─► LIMP if a pin is unconfirmed
```

Hardware, not software: the pin solenoid supply passes through a discrete speed comparator (≤ 5 km/h) and the E-stop/brake/parking-brake contacts; no software state can release a pin above 5 km/h. Mode declarations require switch states, not sensor estimates. The transformation controller is a separate node with a safety target of ISO 13849-1 Cat 3 / PL d (or ASIL B under ISO 26262 for an L-category approval) [FS-1]. The full state machine and gate tables are in `docs/feasibility/06_safety_interlocks.md`.

## 10.3 Environmental durability

| Environment | Threat | Design response (V0) | Test |
|---|---|---|---|
| **Desert: sand ingress** | sector/pin, actuator rod, pivot seals, motor cooling, connectors | downward-open sector slots; labyrinth disc covers; rod boots; double-lip + labyrinth pivot seals with grease purge; IP69K actuators; IP68 HV connectors; radiator with a reversible fan | sand/dust chamber (ISO 16750-4 style), 10,000 transformation cycles with sand dosing (Prototype 1 rig) |
| **Desert: dust** | electronics, HMI | IP67 enclosures with ePTFE vents (no sealed box without a vent [BAT-5]) | dust chamber |
| **Desert: heat** | battery > 45 °C ambient, motors, inverters, tyres | liquid loop with a 6 kW radiator; battery derate above 50 °C cell; pack heater irrelevant | 45 °C soak + duty cycle |
| **Desert: UV** | panels, tyres, grips | UV-stabilised ABS/TPO, painted A-surfaces; UHMW wear parts | 1,000 h UV |
| **Rocks: impact** | tub floor, arms, carrier discs, nodes | 4 mm UHMW skid over 3 mm 5083 floor; 8 mm UHMW strips on the arm lower faces; carrier disc rims proud of the arm by 5 mm as sacrificial contact; node plates | rock strike 5 g case (Part 10 of the feasibility study) |
| **Rocks: abrasion** | tyre sidewalls, arm faces, skids | replaceable strips | field |
| **Rocks: underbody strike** | battery | the battery tray is inside the sills and above the floor; a strike loads the floor and sills, not the tray | drop test on a 100 mm dome at 3 g |
| **Snow: packing** | arches, sector, tracks | open arches; arch liner stand-off 25 mm from the tyre; sector heated by the coolant return; cassette walking-beam sheds snow | cold chamber −25 °C with snow |
| **Snow/ice: low temperature** | seals, actuator grease, battery charging (< 0 °C restricted for NMC) | −30 °C rated seals and grease; pack heater plate (1 kW) before charge; solenoid break-ice pulse | −30 °C soak, transformation, charge |
| **Water: corrosion** | 6082 nodes vs steel pins, fasteners, hull | anodised aluminium, PTFE-isolated stainless fasteners, sacrificial anode on the jet (variant), ISO 12944 C5 coating on the 4130 frame [MAR-3]; fresh-water flush procedure | 500 h salt spray on the corner module |
| **Water: sealing** | pivot cartridge, carrier housing, battery box | IP67 corner (base), 0.5 m head for 1 h on the pivot (variant), IP68 battery box | immersion tests, hot-into-cold thermal shock (65 °C part into 5 °C water) |
| **Water: pressure** | hull panels, hatches (variant) | ISO 12215-5 scantlings | slamming with accelerometers |
| **Water: electrical isolation** | HV to chassis | IMD ≥ 500 Ω/V, HVIL, class-A 48 V actuators | isolation test at 3× bus voltage |

IP requirements by zone: corner module assembly IP67 (base) / IP68 short-term (variant); actuator IP69K static, IP66 dynamic; battery IP67 (base) / IP68 (variant); inverters IP6K9K; HMI IP67; connectors IP68/IP6K9K with HVIL. Drainage: every sealed housing has a vent and a drain at its lowest point; the sill cavities drain at the nodes; the arch liners have scuppers.
