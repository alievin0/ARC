# 14 — Research base and existing technology table

## 14.1 Research status

The research for this architecture is the seven-cluster survey compiled for the feasibility study (`docs/feasibility/REFERENCES.md`, 220 entries with verification tags). It covers wheel-leg robots, four-bar and trailing-arm mechanisms, active suspension, ATV snow conversions, snowmobile tracks, ski steering, amphibious ATVs, retractable wheels, water jets, hulls, automotive suspension references, robotics actuators, locks (landing-gear practice), sealed actuators, off-road EV platforms, vehicle dynamics, patents (55 official front pages read), existing products and prototypes, and manufacturing.

**Constraint restated:** in this environment every fetch to manufacturer, standards, patent-office and publisher hosts was refused by the egress policy and the search quota was exhausted; the reference file states, per entry, what was actually read. No additional research was possible for this document; the new content here is design work on the existing base, and every value that would need a new source is marked TBD.

## 14.2 Existing technology (what exists, how it works, what ARC-2B takes from it)

| Technology | Existing example | How it works | ARC-2B relevance | Limitation |
|---|---|---|---|---|
| Retracting a whole suspension corner with an actuator isolated from the ride spring | Gibbs Quadski / Aquada [AMP-1][RET-2] | hydraulic ram rotates the suspension mount; coil springs/dampers unchanged; ≤ 5 s | the carrier concept is this pattern in electromechanical form | Gibbs used hydraulics; production ended 2016 |
| Hydraulic retraction with self-closing hull flaps | WaterCar Panther [AMP-4][PAT-9] | pneumatic/hydraulic cylinders; flaps close the wells | flaps on the M variant | patent possibly active to ~2029 |
| Over-centre locks and lock-stays | aircraft landing gear [RET-1][PAT-12] | actuator moves, a locking link carries the load | the pin/sector lock and the rule "actuator moves, lock carries" | aviation cost |
| Electromechanical corner geometry control | Audi predictive active suspension [RET-5] | 48 V motor + harmonic drive, 1,100 N·m per wheel, ±85 mm in 0.5 s | proves 48 V electromechanical corner actuation in production | passenger-car scale, ±85 mm only |
| Trailing arm + radius rods rear suspension | UTV practice (RZR class) | arm carries vertical/longitudinal, rods control toe/camber | the boxed trailing arm | not sourced in this study (engineering knowledge) |
| Leading-arm front suspension | Citroën 2CV | wheel moves forward-and-up on bump; anti-dive from the pivot behind the wheel | the front module orientation | not sourced in this study (engineering knowledge) |
| Wheel-leg hybrid locomotion | ETH/Swiss-Mile ANYmal, Unitree B2-W [WL-3][WL-10] | actuated joints carry ground loads; wheels at the feet | shows what ARC-2B deliberately does not do (walking); joint torques 80–320 N·m at 50–80 kg | no rider-scale precedent |
| Rider-carrying long-arm 4-motor electric off-roader | Swincar e-Spider [WL-14] | passive pendular arms, 4 in-wheel motors, ~200 kg | closest product in character | passive articulation, no body |
| Hub-mounted ATV ski kits | Diamond J ATSki [SKI-2] | ski bracket bolts to the hub with the lug nuts | the front ski adapter | packed snow only without rear tracks |
| Bolt-on ATV track cassettes | Camso, Polaris Prospector, Can-Am Apache, Mattracks [TRK-1..4] | sprocket hub on the wheel bolt circle; anti-rotation link to the suspension; idler tensioning | the rear cassette and its interface | 1–2 h install with a jack; Camso/Soucy patents possibly active to 2028–2033 [PAT-19][PAT-20] |
| Snowmobile track/ski hardware | Ski-Doo, Polaris [SNO-1..3] | rail suspension, 2.86/3.0 in pitch, carbide skis, limiter straps | pitch, lug, tension practice | too long for an ATV corner |
| Per-motor 2-speed reduction for crawl | Mercedes G 580 [TV-1] | 1:11 / 1:21 per motor | rear 6:1 / 12:1 | car scale |
| Torque vectoring with four motors | Rivian, Rimac [TV-1] | ≥ 100 Hz per-wheel torque control | traction/ESC maps per mode | |
| PWC water jet, reverse bucket | Sea-Doo, Yamaha [JET-3][JET-4] | 155–160 mm axial pump; bucket for neutral/reverse/brake | M variant propulsion | ~40% propulsive efficiency at hump speed [JET-1] |
| Small electric jet module | ZeroJet [JET-7] | 14–30 kW, 48 V | swim kit / removable hull propulsion | tender-scale |
| Electric PWC energy budget | Taiga Orca, Narke [JET-5][JET-6] | 23–24 kWh for ~2 h | M variant pack sizing | |
| HV safety hardware | TE EV200, Bender iso165C [HV-10][HV-11] | hermetic contactor, isolation monitor | pack architecture | |
| Sealed enclosure venting | ePTFE vents [BAT-5] | equalise pressure on thermal cycling | every sealed housing | |

**What has been done:** every row above exists as a product or a documented prototype.
**What has not been done:** a rider-carrying vehicle whose four corners change geometry under electromechanical actuation with mechanical locks; a self-lifting vehicle for tool-free ski/track swaps; a zero-height-steer mechanical steering layout on articulated corners.
**What is new in ARC-2B:** those three things, and only those. Everything else is integration of proven parts.
