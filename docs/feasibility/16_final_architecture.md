# Part 16 — Recommended ARC-2B architecture

> **Revision note (V0 architecture).** `docs/architecture/` supersedes two decisions in this part after packaging and side-view-geometry checks: the front arm is **leading** (pivot behind the wheel, under the footboard), not trailing, and the brakes are **inboard** on the carriers. Reasons and numbers: `docs/architecture/02_master_geometry.md` §2.2 and `docs/architecture/calc/kinematics.py`.

One vehicle platform, two bodies:
- **ARC-2B** (base): road, robotic, snow (swap-in kits), optional displacement swim kit.
- **ARC-2B M** (marine variant, later generation): same platform and corner modules under a 2.6 × 1.5 m planing hull with a PWC-class jet.

## 16.1 Architecture summary

| System | Recommendation | Part |
|---|---|---|
| **Chassis** | central platform: two 6082-T6 extruded sills + laser-cut 5083 floor (the "tub") + four machined 6082 pivot-housing nodes; 4130 tube rider frame bolted on top; battery between the sills; wheelbase 1.30 m, track 0.98 m, clearance 0.28 m road / 0.48 m high | 10 |
| **Four corner modules** | identical carrier/pivot/actuator/lock; trailing arm front and rear (450 mm); front arm ends in a steered knuckle, rear in a fixed hub; 25 kg unsprung per corner | 3, 4 |
| **Suspension** | coil-over between arm and carrier, 0.22 m travel at any carrier angle; semi-active damping in road mode | 12 |
| **Steering** | mechanical rack with EPS on the chassis; tie-rod inner joints on the front pivot axis (zero height-steer); ±35° | 3.5 |
| **Brakes** | hydraulic discs at all four hubs, two circuits, regen blend ≤ 0.3 g, rear mechanical parking brake (required for kit swaps) | 7 |
| **Motors** | four carrier-mounted liquid-cooled motors, 8–10 kW continuous / 15–20 kW peak each, 6:1 reduction, rear pair with a 2-speed (crawl/track) option; CV half-shafts | 7 |
| **Battery** | 12 kWh nominal, ~350 V, 21700 NMC, IP67 tray with vent, heater plate, cold plate; sized from the duty cycle, locked only after Stage 3 measurements | 11 |
| **Control system** | VCU (traction, vectoring, ESC maps per mode) + separate safety-rated transformation controller (Cat 3 / PL d target) + BMS + four inverters on CAN; 48 V actuator bus | 6, 11 |
| **Wheel-leg mechanism** | carrier rotates 15°–60° on a self-locking 6–10 kN ball-screw actuator with brake; spring-applied pin into a 5° sector; two absolute angle sensors per corner; hard stops at 10° and 65° | 3, 4 |
| **Ski mechanism** | hub-flange adapter with saddle pivot, ski-pressure spring, limiter strap + switch; commodity snowmobile ski; fitted with the corner self-lifted | 8 |
| **Track mechanism** | 1.10 m × 0.30 m rear cassette on the hub bolt circle, idlers, walking-beam bogies, screw/spring tensioner with a tension switch, anti-rotation link to the arm; from a licensed track manufacturer | 8, 15 |
| **Marine hull** | base vehicle: none structural; optional deployable sponsons (Ø 0.4–0.5 m) for displacement swim. Variant: 5083 or infused planing tub 2.6 × 1.5 × 0.55 m, deadrise 12°, free-flooding arches with flaps, three watertight compartments, foam-filled voids | 9 |
| **Water jet** | base swim kit: 15–30 kW electric jet module, ≤ 4 kn. Variant: 155–160 mm axial PWC pump on a dedicated 60–90 kW motor, steering nozzle ±25°, electric reverse bucket, keel-cooled loop, 20+ kWh pack | 9 |
| **Hitch** | 50 mm receiver on a 4130 tower bolted to the rear nodes of the chassis (never to the arms); designed to SAE J684 Class 1 loads; towing rated by test, permitted in ROAD only | 10 |
| **Safety locks** | per corner: pin (spring-applied), self-locking screw, actuator brake; solenoid supply gated by a hardware speed comparator; kit adapter switches and kit IDs; seat switch and kill-cord afloat | 5, 6 |

## 16.2 Simplified system diagram

```mermaid
flowchart TB
    subgraph CHASSIS["CENTRAL PLATFORM (sills + tub + 4 pivot nodes) — carries battery, rider frame, hitch"]
        BAT[12 kWh pack: BMS, contactors, IMD, HVIL, MSD]
        VCU[VCU: traction, vectoring, ESC maps]
        TC[Transformation controller: interlocks, locks, kit IDs — safety-rated]
        RACK[Steering rack + EPS]
        HITCH[Hitch on chassis]
        COOL[Cooling loop]
    end
    subgraph FL["FRONT-LEFT MODULE"]
        CFL[Carrier: motor+6:1, coil-over mount, sector] --> AFL[Trailing arm 450 mm] --> KFL[Steered knuckle + hub + disc]
        ACTFL[Actuator 6–10 kN + brake] --> CFL
        PINFL[Spring-applied pin] --> CFL
        KFL --> WFL[Wheel | Ski adapter]
    end
    subgraph FR["FRONT-RIGHT MODULE"]
        CFR[Carrier] --> AFR[Arm] --> KFR[Knuckle + hub] --> WFR[Wheel | Ski]
    end
    subgraph RL["REAR-LEFT MODULE"]
        CRL[Carrier + 2-speed] --> ARL[Arm] --> HRL[Hub + disc + parking brake] --> WRL[Wheel | Track cassette]
    end
    subgraph RR["REAR-RIGHT MODULE"]
        CRR[Carrier + 2-speed] --> ARR[Arm] --> HRR[Hub + disc + parking brake] --> WRR[Wheel | Track cassette]
    end
    BAT --> INV[4 inverters] --> CFL & CFR & CRL & CRR
    BAT --> DCDC[DC-DC 12 V / 48 V] --> ACTFL & TC & RACK
    RACK -->|tie-rods, inner joints on pivot axis| KFL & KFR
    TC -->|CAN| ACTFL & PINFL
    TC <-->|sensors: carrier angle ×2, arm angle, pin switches ×2, kit ID| FL & FR & RL & RR
    VCU <--> TC
    COOL --> BAT & INV & CFL & CFR & CRL & CRR
    OPT[Optional: sponsons + 15–30 kW jet module — swim mode] -.-> CHASSIS
    VAR[Variant ARC-2B M: planing tub, 155 mm jet, 20+ kWh] -.-> CHASSIS
```

## 16.3 Mode map

| Mode | Carrier angles | Kits | Speed cap | Drive |
|---|---|---|---|---|
| ROAD | 15° all | 4 wheels | 60 km/h design | 4WD, vectoring |
| ROBOTIC | 15°–60° per corner | 4 wheels | 25 km/h pinned, 5 km/h while adjusting | 4WD, crawl map |
| LIFT / KIT SWAP | one corner at 60° | any | 0 | off, parked |
| SNOW | front 15°, rear 25° | 2 skis + 2 tracks | 45 km/h | rear 2WD, low range |
| SWIM (optional kit) | −70° (needs the marine-range drive) or wheels down in shallow water | sponsons + jet module | 4 kn | jet |
| MARINE (variant) | −70° | hull | displacement until planing gates pass | 60–90 kW jet |

## 16.4 What the rider sees

An ATV that raises and levels itself, lifts a corner so a ski or a track clicks on in minutes, and, as a later variant, becomes a Quadski-class amphibian. The technology is hidden inside the carriers and the tub; the exterior keeps the four exposed wheels, the low body, the angular black/white panels and the ARC-2B front identity.
