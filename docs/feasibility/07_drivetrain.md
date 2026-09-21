# Part 7 — Drivetrain architecture

## 7.1 The five candidates

| | A. Four hub motors | B. Four inboard (chassis) motors + half-shafts | C. Two front + two rear motors on the corner carriers | D. Central motor(s) + mechanical differentials | E. Rear motor + mechanical track drive coupling |
|---|---|---|---|---|---|
| Layout | motor inside each wheel; wheel bolts to the rotor flange | motors on the chassis; CV half-shafts to each hub | motor + reduction on each carrier (sprung, rotates with geometry); short CV half-shaft to the hub | one or two motors on the chassis; front/rear differentials; half-shafts | one chassis motor drives the rear pair through a differential; track sprockets driven by that same output; front motors optional |

## 7.2 Analysis

| Criterion | A. Hub | B. Inboard chassis | C. Carrier-mounted | D. Central + diffs | E. Rear motor + track PTO |
|---|---|---|---|---|---|
| **Unsprung mass** | worst: +18 kg (QS273 [MOT-6]) to +28–39 kg (Pd16/Pd18 [MOT-1]) per corner on a corner whose sprung share is only ~120 kg; Lotus found +30 kg "noticeable" on a 2 t car [UNS-1]; on ARC-2B the unsprung ratio would exceed 0.35 | best: 25 kg per corner (Part 3) | as B (the motor is on the carrier, which is pinned to the chassis, so it is sprung) | as B | as B |
| **Torque** | direct-drive hub motors of ATV size give 200–400 Nm peak [MOT-2][MOT-6]; 26 in tyre needs ~1,150 Nm per wheel for a 0.6 g launch (590 kg × 0.6 × 9.81 × 0.33 m / 4 wheels... see note 1) — only the 28–39 kg car units reach that | any motor with a 6:1 reduction: EMRAX 188 (100 Nm peak) → 600 Nm at the wheel [MOT-4]; with 2-speed (G 580 pattern [TV-1]) 1,100 Nm for tracks | as B | one 60–80 kW motor with a diff; open diffs lose torque on mixed grip unless locked | as D at the rear |
| **Cooling** | motor sits in the wheel: mud, snow, water, thermal shock on seals [UNS-3] | liquid-cooled inside the body | liquid-cooled inside the carrier housing; coolant service loop over 45° | inside the body | inside the body |
| **Waterproofing** | the motor is the thing that gets immersed; IP67 claims are marketing-grade [MOT-6] | motor never immersed on the base vehicle | motor inside the carrier housing; on the marine variant the housing is above the waterline when retracted, and the pivot seal is the only water interface | as B | as B |
| **Serviceability** | wheel change = motor handling; hub motor bearing failure = motor replacement | half-shaft and CV boots (ATV-standard) | as B; the motor is reachable from the arch (Part 4) | diff and prop-shaft service | as D |
| **Transformation complexity** | none for road/robotic; retraction carries 18–39 kg extra on the arm | half-shaft angle must accommodate 45° of carrier rotation plus travel: exceeds CV limits (~45–50° max) → **not compatible with Option C** unless the motor output is on the pivot axis | half-shaft sees only suspension travel angles (±15°) because the motor rotates with the carrier | half-shafts from a central diff have the same 45° problem as B; a rear-only diff could sit on a rear cross-carrier | prop-shaft/diff to a rotating carrier: same problem |
| **Track compatibility** | the cassette sprocket must clear a 16–18 in motor: incompatible with production cassette geometry; and a 30 kg hub motor plus a 45 kg cassette on one arm is 75 kg unsprung | cassette bolts to the hub as on any ATV | as B, plus a track/low-range gear on the carrier reduction (2-speed) | as B | as B by definition |
| **Wheel replacement** | motor-specific rim, non-standard | standard ATV wheel | standard ATV wheel | standard | standard |
| **Cost** | 4 car-grade in-wheel units are the most expensive route; light e-moto hubs are cheap but under-torqued | 4 motors + 4 inverters | 4 motors + 4 inverters; carrier casting more complex | 1–2 motors, 1–2 inverters, 2 diffs, prop-shaft: cheapest hardware, but a differential in a vehicle whose corner geometry changes needs a plunging prop-shaft | 1–3 motors |
| **Torque vectoring / traction** | full per-wheel | full per-wheel | full per-wheel | needs locking diffs or brake-based vectoring | partial |
| **Failure containment** | motor fault = wheel fault | motor fault = one corner; 3-wheel drive continues | same | motor fault = axle or vehicle | motor fault = rear axle |

Note 1: the wheel-torque figure is for the "premium" launch target (0.6 g), computed as 0.6 × 590 kg × 9.81 m/s² × 0.33 m radius / 4 ≈ 286 Nm per wheel *at the tyre* for a symmetric split; 1,150 Nm is the single-wheel figure if all traction goes to one wheel (rock crawling). Numbers are RC-0 derived.

## 7.3 Selection: Option C (carrier-mounted motors, two front + two rear)

Option C is the only candidate that is simultaneously compatible with:
- the selected corner mechanism (the half-shaft never sees the carrier angle),
- production track cassettes (standard hub bolt circle, no motor in the wheel),
- sealing (motor inside a housing, never immersed in normal use),
- low unsprung mass (25 kg per corner instead of 43–64 kg with a hub motor).

It costs one more casting (the carrier housing integrates the motor mount) and four motor coolant/HV service loops. It does *not* require a central differential, prop-shaft or drive switching of any kind: the track "drive coupling" is the wheel bolt circle, as on every production track kit [TRK-1..4][PAT-23].

### Motor sizing (RC-0, derived in `calc/energy.py`)

| Requirement | Value | Motor consequence |
|---|---|---|
| Steady 60 km/h on gravel, flat | 8.1 kW at the battery → ~7 kW at the wheels | ~2 kW per motor continuous: trivial |
| 60 km/h up 10% grade | 19.4 kW | ~4 kW per motor continuous |
| 0–60 km/h in ~6 s | ~34 kW at the wheels at the end of the run | ~8.5 kW per motor for 6 s |
| Snow at 45 km/h (tracks) | 12.8 kW | ~5 kW per rear motor continuous if the rear pair does most of the work |
| Traction-limited hill (μ 0.6) | 3.5 kN tractive force → ~1,150 Nm total at the wheels | 290 Nm per wheel with a symmetric split |

Candidate class: **8–10 kW continuous / 15–20 kW peak, 30–40 Nm peak at the motor, 6:1 planetary reduction → 180–240 Nm at the wheel per corner, ~720–960 Nm total**, liquid-cooled, 96–150 V class or 300–400 V class (Part 11). EMRAX 188 (7.9 kg, 37 kW cont, 100 Nm peak [MOT-4]) is over-specified but proves the mass class; Motenergy ME1616 (26 kg, 20 kW cont, IP67 [MOT-6]) is the heavy end. A purpose-selected 8–10 kg motor with integrated 6:1 gearset and a 2-speed option for the rear (track/crawl range, G 580 pattern [TV-1]) is the target; **the exact motor must be chosen against verified datasheets, not this table.**

### Why not a hub motor at the front only?

Part 3 considered driving the front with light hub motors to avoid the front half-shaft. Rejected because (a) the steered knuckle already carries a CV half-shaft on every 4×4 ATV, so there is no novelty to avoid, and (b) two different corner designs cost more than one common carrier design.

### Braking

Hydraulic discs at all four hubs (ATV class), two-circuit, with EPS-independent hand/foot controls per ANSI/SVIA practice [STD-1]; regenerative braking via the four inverters blended at ≤ 0.3 g; mechanical parking brake on the rear calipers, required for LIFT and KIT_SWAP states (Part 6). Track mode: the hub disc brakes the sprocket, as on production kits. Marine: no wheel braking; deceleration by the jet reverse bucket [JET-4].
