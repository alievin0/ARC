# Part 17 — Redesign where the concept is unrealistic

Each item names the smallest change that preserves the ARC-2B product idea (one premium electric ATV, several modes, rider-focused, technology hidden).

## 17.1 THIS PART SHOULD BE CHANGED — the mass claim (80–150 kg)

**Why.** A bottom-up budget with four articulated corners, four motors, a 12 kWh pack and an ATV-class structure is ~440 kg curb (`calc/mass_budget.py`); the closest electric comparables are 318–427 kg for combustion ATVs [ATV-1..3], ~270 kg for an electric snowmobile with a 23 kWh pack [EV-2], and 200 kg for a Swincar with only 4 kWh and no body [WL-14].
**Smallest change.** Publish 400–450 kg as the target and 150 kg as the payload. Nothing else in the concept depends on the wrong number, but every calculation does.

## 17.2 THIS PART SHOULD BE CHANGED — "robotic mode" as walking legs

**Why.** No rider-carrying actuated wheel-leg vehicle exists [WL-1][WL-6][WL-13]; an actuator in the load path needs 3 kNm-class joints at every corner (Part 3, Option A).
**Smallest change.** Define ROBOTIC as *articulated geometry*: per-corner ride height (+0.20 m), body leveling on slopes, self-lift of one corner, obstacle stepping at walking pace. The rider still sees the wheels climb and the body level; the hardware is one 48 V actuator and a pin per corner instead of eight robot joints.

## 17.3 THIS PART SHOULD BE CHANGED — skis and tracks deploying from inside the modules

**Why.** A 1.1–1.3 m, 45 kg cassette and a 1.0 m ski cannot share the module with a 26 in wheel inside an ATV body (Part 8.1).
**Smallest change.** Swap-in kits on the standard hub bolt circle (the interface every production kit already uses), with the vehicle lifting its own corner so the swap needs no jack and no tools beyond a lug wrench. The customer promise ("one vehicle, road and snow") survives; the storyboard changes from "wheels retract, skis deploy" to "the vehicle lifts a corner, the kit clicks on".

## 17.4 THIS PART SHOULD BE CHANGED — the exterior body as a planing marine hull with sealed wheel bays

**Why.** The ATV-envelope tub does not float (−61% reserve buoyancy) and would capsize (GM −0.20 m) (`calc/buoyancy.py`); planing needs 60–90 kW and 20+ kWh; the only precedent is 3.26 m long and 100 kW [AMP-1][PAT-29].
**Smallest change, two tiers.**
1. Base vehicle: an optional **swim kit** (deployable Ø 0.4–0.5 m sponsons in the sills, a 15–30 kW electric jet module, bilge pumps, sealed corners) for calm-water crossings at ≤ 4 kn. Honest, cheap, uses the same retraction sweep only if the marine-range drive is fitted; otherwise wheels stay down in shallow water.
2. A separate **ARC-2B M** variant with a 2.6 × 1.5 m hidden planing hull under ARC-2B panels, sharing the platform and corner modules. This is the Quadski-class product the boards actually depict.

## 17.5 THIS PART SHOULD BE CHANGED — sealed, door-closed wheel bays

**Why.** Sealing a bay door around a moving arm is a leak path with no production precedent; Gibbs and WaterCar use free-flooding arches with a sealed pivot and flaps on the planing surface [PAT-6][PAT-9].
**Smallest change.** Free-flooding arches; one sealed pivot cartridge per corner; arch flaps only on the marine variant.

## 17.6 THIS PART SHOULD BE CHANGED — mechanical "drivetrain switching" for tracks

**Why.** Unnecessary: every production track kit is driven through the wheel hub [TRK-1..4][PAT-23].
**Smallest change.** None to the exterior. The hub bolt circle is the coupling; the rear motors get a 2-speed (crawl/track) reduction instead of any clutch or transfer mechanism.

## 17.7 THIS PART SHOULD BE CHANGED — steering through a large corner articulation

**Why.** Any tie-rod not on the pivot axis steers the vehicle every time a corner moves.
**Smallest change.** Put the tie-rod inner joints on the front pivot axis line (Part 3.5). Invisible to the customer.

## 17.8 What does NOT need to change

- The four exposed large wheels, the low central body, the angular black/white panels, the amber accents and the front identity (the carriers and pivot housings live inside the fender volumes).
- The open rider position; the rider never moves between modes (Part 12.12).
- The chassis-mounted rear hitch.
- "Same DNA" across modes: one platform, four identical corner modules, kits that use one interface.

## 17.9 Resulting concept statement

*ARC-2B is a premium electric ATV whose four corners can independently change height, level the body, and lift themselves so that skis and track cassettes clip onto the standard hubs in minutes. A swim kit lets it cross calm water at walking pace. A later, longer-hulled ARC-2B M variant is the planing amphibian.*
