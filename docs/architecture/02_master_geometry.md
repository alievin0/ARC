# 2 — Master geometry (V0)

Coordinate system: origin on the ground plane, on the centreline, at the
wheelbase midpoint with the vehicle in ROAD static; +X forward, +Y left,
+Z up. Every CAD model in Section 12 uses this frame. Status column: TARGET
(chosen, to be validated), TBD (placeholder), DERIVED (computed in `calc/`),
BENCH (benchmark range from `docs/feasibility/REFERENCES.md`).

## 2.1 Master table

| Parameter | Value | Status | Basis |
|---|---:|---|---|
| Overall length | 2.15 m | TARGET | nose ≥ +1.00 m forced by front tyre at full droop; rack end −1.10 m for cassette visibility |
| Overall width | 1.24 m | TARGET | tyre outer faces ±0.615 m; fits 1.25 m trail class |
| Overall height (grips) | 1.16 m | TBD | ergonomics rig, Prototype 0 |
| Wheelbase, ROAD | 1.300 m | TARGET | ATV benchmarks 1.25–1.34 m |
| Wheelbase, HIGH | 1.110 m | DERIVED | both wheels move 0.095 m inward |
| Front track / rear track | 0.98 / 0.98 m | TARGET | equal; ROHVA-style Kst check still needed for SNOW where the effective widths differ |
| Ground clearance ROAD / HIGH / LIFT | 0.28 / 0.484 / 0.559 m | TARGET / DERIVED / DERIVED | tub floor at Z 0.28 |
| Tyre | 26 × 10-12 | TARGET | Ø 0.66 m, 0.25 m section |
| Wheel | 12 × 8 in aluminium, 4 × 110 mm PCD | TARGET | common ATV PCD; kit interface |
| Front wheel centres, ROAD | (+0.650, ±0.490, 0.330) | DERIVED | |
| Rear wheel centres, ROAD | (−0.650, ±0.490, 0.330) | DERIVED | |
| Front pivot axes | X +0.161, Z 0.434, arm plane Y ±0.340 | DERIVED | leading arm, 0.50 m at 12° |
| Rear pivot axes | X −0.161, Z 0.434, arm plane Y ±0.340 | DERIVED | trailing arm |
| Pivot bearing pair | 150 mm apart, Y 0.265–0.415 | TARGET | |
| Arm length (pivot to wheel centre) | 0.500 m | TARGET | |
| Arm angles road / high / lift / retract | 12° / 38° / 50° / −50° | TARGET | |
| Wheel travel | 0.22 m (0.12 bump, 0.10 droop) | TARGET | ATV benchmarks 0.19–0.24 |
| Rider hip point (seat reference) | (−0.10, 0, 0.88) | TARGET | |
| Seat height | 0.88 m | TARGET | benchmarks 0.85–0.90 |
| Footboards | X −0.25…+0.23, Y ±(0.18…0.36), top Z 0.42 | DERIVED (X limit) | front tyre sweep in HIGH+bump |
| Handlebar grips | (+0.28, ±0.36, 1.16) | TBD | |
| Battery envelope | X −0.50…+0.40, Y ±0.25, Z 0.29…0.47 | TARGET | 0.90 × 0.50 × 0.18 m = 81 L for 12 kWh |
| Motors | inside each carrier at (±0.161 + 0.05 toward the wheel, ±0.34, 0.434), axis parallel to Y | TARGET | motor on carrier, half-shaft to hub |
| Inverters (4) | under the seat, X −0.30…+0.05, Z 0.50…0.62 | TARGET | short HV runs to the carriers |
| HV junction box, DC-DC, charger | under the seat rear, X −0.35…−0.10 | TARGET | |
| Transformation controller + VCU | behind the fascia, X +0.85…+0.95, Z 0.65…0.80 | TARGET | |
| Cooling radiator | nose, X +0.90…+0.98, Z 0.45…0.75, 0.40 m wide | TARGET | |
| Steering rack | X +0.161 (on the front pivot axis line), Z 0.434, Y ±0.26 inner joints | DERIVED (forced) | zero height-steer |
| Hitch receiver | (−1.05, 0, 0.35), 50 mm square | TARGET | chassis-mounted |
| Structural chassis envelope | sills Y ±0.30 (120 × 60 section) from X −0.75 to +0.75; tub floor Z 0.28; rider frame to Z 1.10 | TARGET | |
| Curb mass | 487 kg | DERIVED | `calc/mass_budget_v0.py` |
| Payload | 150 kg | REQUIREMENT | rider 100 + cargo 50 |
| Total operating mass ROAD / SNOW / SWIM | 637 / 701 / 636 kg | DERIVED | |
| Static corner load | 1.56 kN | DERIVED | |
| Actuator stroke / force | 104 mm / 6.8 kN | DERIVED | 38° sweep, 160 mm lever |
| Lock pin shear (5 g) | 25.5 kN | DERIVED | 150 mm sector radius |
| SSF ROAD / HIGH | 0.82 / 0.61 | DERIVED | CG 0.60 m TARGET |
| Anti-dive (inboard brakes) / anti-squat | 30% / 28% | DERIVED | |
| Turning radius (outer wheel) | 2.45 m | DERIVED | 32° outer steer |

## 2.2 What changed versus the feasibility study and why

| Item | Feasibility RC-0 | V0 | Reason |
|---|---|---|---|
| Front arm | trailing (pivot ahead of the wheel) | **leading** (pivot behind, under the footboard) | with a 0.45–0.50 m arm the trailing pivot lands at the bumper face, and raising the body shifted the CG to ~31% front load (`calc/kinematics.py` logic). Leading front + trailing rear keeps the CG centred and gives anti-dive instead of pro-dive |
| Arm length / angles | 0.45 m; 15/45/60° | 0.50 m; 12/38/50° | smaller angular sweep for the same +0.20 m: wheelbase shortening 0.19 m instead of 0.24 m; actuator stroke 104 mm |
| Brakes | hub discs | **inboard discs on the carriers** | with outboard brakes the leading arm gives 125% anti-dive (nose rises under braking); inboard brakes bring it to 30%. Also removes calipers from mud, sand and salt |
| Curb mass | 440 kg | 487 kg | protection, seat, fluids, heavier corner module added explicitly |
| Retraction angle (variant) | −70° | −50° | sufficient to put the tyre bottom 0.49 m above the keel line |

## 2.3 Wheel-centre positions in every state (body frame, from `calc/kinematics.py`)

| State | Arm angle | Front wheel (X, Z) | Rear wheel (X, Z) | Wheelbase | Body rise | Tyre top Z |
|---|---:|---|---|---:|---:|---:|
| ROAD static | 12.0° | (+0.650, 0.330) | (−0.650, 0.330) | 1.300 | 0 | 0.660 |
| ROAD full bump | −1.9° | (+0.661, 0.450) | (−0.661, 0.450) | 1.321 | −0.120 | 0.780 |
| ROAD full droop | 23.5° | (+0.619, 0.234) | (−0.619, 0.234) | 1.239 | +0.096 | 0.564 |
| HIGH static | 38.0° | (+0.555, 0.126) | (−0.555, 0.126) | 1.110 | +0.204 | 0.456 |
| HIGH full bump | 24.1° | (+0.617, 0.230) | (−0.617, 0.230) | 1.235 | +0.100 | 0.560 |
| LIFT max | 50.0° | (+0.482, 0.051) | (−0.482, 0.051) | 0.965 | +0.279 | 0.381 |
| RETRACT (variant) | −50.0° | (+0.482, 0.817) | (−0.482, 0.817) | — | — | 1.147 |

"Body rise" is how much higher the body sits above the wheel centre than in
ROAD static; Z values are in the body frame (the body's ground reference in
ROAD).
