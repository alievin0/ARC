# 3 — Mass budget (V0)

From `calc/mass_budget_v0.py`. Every line is a TARGET or a BENCH-range estimate; totals are DERIVED. The budget is deliberately bottom-up so that it can be challenged line by line.

| Group | kg | Basis |
|---|---:|---|
| Chassis (sills, tub floor, 4 pivot nodes, rider frame, hitch) | 58 | 4130 rider frame ~30, 6082 sills/nodes ~22, hitch 6 |
| Body panels, fenders, covers, lighting | 24 | thermoformed ABS/TPO ~18 + lamps |
| Wheels (4 × 12 in aluminium) | 18 | 4–5 kg each |
| Tyres (4 × 26×10-12) | 26 | 6–7 kg each |
| Suspension (4 coil-overs) | 14 | 3–4 kg each |
| Corner modules (4 × carrier, arm, pivot cartridge, upright/hub, half-shaft) | 80 | 20 kg per corner |
| Motors + 6:1 reduction (4), rear 2-speed | 48 | 8–11 kg each incl. gearset |
| Inverters (4) + HV junction + DC-DC + charger | 23 | |
| Battery 12 kWh nominal (tray, cold plate, heater) | 78 | 150 Wh/kg pack level |
| BMS, contactors, IMD, fuses, MSD | 4 | EV200 0.43 kg each; iso165C < 0.22 kg |
| Brakes (4 inboard discs/calipers, master cylinders, lines, parking) | 11 | |
| Steering (bars, column, rack, EPS, tie rods) | 10 | |
| Transformation actuators (4) | 18 | 4–5 kg each, 6–10 kN class |
| Mechanical locks (4 pins, solenoids, sectors) | 6 | |
| Wiring / harness / connectors | 10 | |
| Cooling (pump, radiator, fan, lines) | 7 | |
| Electronics (VCU, transformation controller, sensors, HMI) | 5 | |
| Seat, grips, footboards | 8 | |
| Protection (skid plates, bumpers, arch liners, guards) | 12 | |
| **Subtotal** | **460** | |
| Contingency 5% | 23 | |
| **Dry mass** | **483** | road configuration, no fluids |
| Fluids (coolant, brake fluid) | 4 | |
| **Curb mass** | **487** | |
| Payload (rider 100 + cargo 50) | 150 | requirement |
| **Total operating mass, ROAD / ROBOTIC** | **637** | |

Kits and variants:

| Configuration | Curb | Operating |
|---|---:|---:|
| SNOW (wheels and tyres off; 2 skis 16 kg + 2 cassettes 92 kg on) | 551 | 701 |
| SWIM kit on the base vehicle (sponsons, 25 kg jet module, bilge) | 536 | 636 (rider only) |
| ARC-2B M variant (hull tub, flaps, seals, PWC jet and motor, +8 kWh) | 627 | 727 (rider only) |

## 3.1 Is the whole design consistent?

- **The concept boards say 80–150 kg. The budget says 487 kg.** The boards' number cannot be approached: the tyres and wheels alone are 44 kg, the battery for a 60 km range is 78 kg, and four articulated corners with motors are 128 kg before any structure. This is not a refinement problem; it is a different vehicle class. The right comparison set is 318–427 kg combustion ATVs and ~270 kg electric snowmobiles with 23 kWh packs [ATV-1..3][EV-2].
- **Mass drives everything downstream:** static corner load 1.56 kN → actuator 6.8 kN → lock pin shear 25.5 kN → pivot bearings; 140 Wh/km → 12 kWh; 636 kg afloat → the sponson sizes and the 2.6–2.8 m hull. Each of those numbers moves 1:1 with mass, so the budget is the first thing to re-validate at Prototype 3 (rolling chassis weighed on four scales).
- **Where mass could still be cut** (in order of realism): battery to 10 kWh if the measured duty cycle is under 120 Wh/km (−13 kg); corner modules to 17 kg each with cast carriers (−12 kg); rider frame in 6082 instead of 4130 (−8 kg, at a fatigue cost). A credible floor is ~440 kg curb; nothing plausible reaches 300 kg.
