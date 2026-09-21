# Part 8 — Ski / track system

## 8.1 The packaging question first

The brief asks how the wheel and the track can occupy the same physical volume. They cannot, and this study does not pretend otherwise:

| Item | Size (benchmarks) | Mass |
|---|---|---|
| 26 in ATV wheel + tyre | Ø 0.66 m × 0.25 m | ~11 kg |
| ATV track cassette (Prospector Pro rear) | 52 in (1.32 m) long × 24.7 in (0.63 m) tall × 25 in wide [TRK-2] | ~97 lb (44 kg) per track (likely per-track figure [TRK-2]) |
| Snow-bike rear track kit | 1.83 m long [SKI-1] | 48 kg |
| Snowmobile-type ski | ~1.0–1.1 m long × 0.15–0.2 m wide | ~7 kg incl. leg [SKI-1] |

The rear cassette alone is longer than the wheelbase of the vehicle. Stowing it "inside the module" would require an ATV whose rear body is 1.3 m long and 0.65 m tall behind the seat, i.e. not an ATV. Stowing the ski alongside the retracted front wheel would put a 1 m blade inside the front fender, where the wheel must also sweep; it is conceivable with a two-piece folding ski, but that is new, unproven hardware whose only purpose is to avoid a five-minute swap.

**THIS PART SHOULD BE CHANGED** (Part 17): skis and tracks are **swap-in kits mounted on the standard hub interface**, and the vehicle's own corner actuation does the lifting. The "transformation" the rider experiences is: park, press "swap", pull four pins and lug nuts, click the kits on, press "lower". No jack, no lifting, no tools beyond the lug wrench.

Everything below is designed for that architecture.

## 8.2 Front: ski module

```
  SIDE VIEW, front-left, ski fitted (arm at 15°, ROAD geometry)

      carrier ⊙───────── arm ───────────╮
                                        │ knuckle (steered, kingpin)
                                        ├─ hub flange (4 studs) ── SKI ADAPTER PLATE
                                        │                           ├─ transverse ski pivot pin (Ø20)
                                        │                           ├─ rubber ski-pressure spring
                                        │                           └─ limiter strap + switch
                             ═══════════╧════════ SKI (1.0 m, keel + carbide) ══════════
```

| Element | Design | Basis |
|---|---|---|
| **Ski pivot** | Ø20 mm hardened pin through the adapter's saddle, polymer bushings, transverse axis at the ski's balance point; ±25° pitch freedom | snowmobile saddle practice (BRP/Polaris spindle patents expired [PAT-17]) |
| **Steering knuckle** | the same knuckle as ROAD; the ski steers about the kingpin because the adapter is bolted to the hub flange downstream of the knuckle; caster ~5° gives self-centring on snow; tie-rods unchanged | hub-mount ATV ski kits [SKI-2] |
| **Ski suspension** | the corner's coil-over (unchanged); ski pressure set by the carrier angle (15° nominal; 20° adds ~50 mm front lift for deep snow) and by the rubber ski-pressure spring on the adapter | snowmobile ski-pressure practice via limiter strap; adjustable without tools by the carrier |
| **Deployment linkage** | none. The "deployment" is the LIFT sequence (Part 4.5) | — |
| **Mechanical lock** | the adapter is retained by the four wheel lug nuts (torque-striped); the ski by one quick-release pin with a secondary circlip; the limiter strap closes a switch when the ski is captive | the same interface that carries the wheel |
| **Ski** | 1.0 m plastic/UHMW ski with a steel keel and carbide runner, 0.18 m wide; flotation area per ski ~0.15 m² | commodity snowmobile ski families |
| **Mass** | ~7 kg per ski assembly (Timbersled front kit 7.25 kg [SKI-1]) | |

Steering geometry check: with the tie-rod inner joint on the pivot axis, ski steer angle equals wheel steer angle at any carrier angle; Ackermann is unchanged because the knuckle arm is unchanged.

## 8.3 Rear: track cassette

```
  SIDE VIEW, rear-left cassette (ROAD-height arm at 25°)

              carrier ⊙────── arm ──────╮
                                        │ hub flange (4 studs)
                             ┌──────────┼──────────┐  anti-rotation link → hardpoint on ARM
                             │      DRIVE SPROCKET  │  (compliant bushing, ±8°)
                   tensioner │   ○               ○  │ idler (front)      idler (rear, on spring-loaded link)
                   screw ───►│ ○    ○    ○    ○   ○ │ bogie rollers on a walking beam
                             └─────────────────────┘
                   ═════════════ rubber track 0.30 m wide × 1.10 m ═════════════
```

| Element | Design | Basis |
|---|---|---|
| **Track cassette frame** | welded 6082 or formed steel triangle frame, sprocket at the apex; 1.10 m ground length, 0.30 m track width (rear), contact ≈ 0.33 m² per cassette → four-corner contact ≈ 1.1 m² with front skis excluded; ground pressure with 650 kg gross ≈ 6 kPa on the rear pair carrying 60% (≈ 3.9 kN / 0.66 m²) | tracked ATV pressure 3.8–6.2 kPa [TER-2]; Backcountry 0.44 psi (3 kPa) [TRK-3] |
| **Drive sprocket** | positive-drive lugged sprocket on a hub that bolts to the wheel flange (4 × M10 studs, same PCD as the wheel); sprocket Ø 0.30 m so that 240 Nm at the hub gives 1.6 kN track pull per side | production kits drive through the hub [TRK-1][PAT-23] |
| **Idlers** | front and rear idlers Ø 0.20 m on sealed double-row bearings; rubber-coated to resist icing | Prospector rollers "double-sealed bearings" [TRK-2] |
| **Rollers** | 4 bogie rollers Ø 0.12 m on a pivoting walking beam so the track conforms | Camso "double tandem stabilizer" [TRK-1]; Mattracks pivoting four-link [TRK-4] |
| **Tensioner** | rear idler on a spring-loaded link (coil spring, 2 kN preload) with a screw adjuster; a spring-loaded indicator switch closes only within the correct tension window | idler-based tensioning on pillow blocks [PAT-23][TRK-5]; snowmobile deflection specs are 7–16 lb for 22–50 mm [SNO-1][SNO-2] |
| **Suspension interface** | the cassette pivots about the hub axis; an anti-rotation link with a compliant bushing goes to a hardpoint on the *arm* so the cassette follows suspension travel and carrier angle without changing its approach angle; the corner's coil-over remains the suspension | resilient anti-torque coupler [PAT-23]; kits attach the anti-rotation link to the suspension arm |
| **Drive coupling** | the hub bolt circle. Confirmed at zero risk by spinning the track a quarter-turn with the corner lifted (Part 6.4) | production kits |
| **Deployment linkage** | none; LIFT sequence | — |
| **Speed** | 45 km/h cap in SNOW (production kits publish speed limits that could not be retrieved [TRK-1]; snowmobile-style 60 km/h+ would need a snowmobile track and drive) | interlock |
| **Track** | 0.30 m × 2.86 in pitch moulded rubber with guide lugs (anti-derail horns [PAT-21]) | commodity |
| **Mass** | ~45 kg per cassette (benchmark 44 kg [TRK-2]); two rear cassettes 90 kg | |

The carrier is commanded to 25° in SNOW to raise the body ~60 mm (approach angle) and to move the cassette's centre slightly forward under the seat; the front stays at 15° to keep ski pressure. Both are set by the interlock, not by the rider.

## 8.4 Why not a front track too?

Four tracks (Camso-style) give better flotation but need four cassettes (180 kg), keep the front heavy and remove the "ski" identity of the concept. Front skis + rear tracks is the snow-bike pattern and the brief's stated intent. The cost is flotation in deep powder; the interlock allows a "4-track" kit variant later because the front hub interface is identical.

## 8.5 Front ski on the front module: does the retracted wheel need to be there?

No. In the swap-in architecture the front wheel is removed, so the front module carries only the ski. The module never has to house both, which is the packaging impossibility the brief warned against.
