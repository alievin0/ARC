# 8 — Marine: four options, one honest answer

## 8.1 The options

| | A. Same chassis + sealed flotation body | B. Separate marine variant (ARC-2B M) | C. Removable marine hull ("dock" the ATV drives into) | D. Amphibious integrated hull on every ARC-2B |
|---|---|---|---|---|
| Buoyancy | ATV-envelope tub with four arches: **does not float** (0.24 m³ available vs 0.64 m³ needed at 636 kg; `docs/feasibility/calc/buoyancy.py`); with Ø 0.45 m deployable sponsons: +39% reserve, GM +1.1 m (`calc/energy_buoyancy_v0.py`) | 2.8 × 1.5 m hull: draft 0.28 m, freeboard 0.27 m, reserve 48%, GM +0.27 m at 727 kg | a proper small boat sized for the ATV (3.2 × 1.8 m): trivially adequate | as B, but on every unit |
| Speed | displacement only, ≤ 4 kn with sponsons; cannot plane | planing with 73–109 kW and ≥ 20 kWh | planing possible with the dock's own 40–60 kW jet/outboard | as B |
| Land penalty | +49 kg swim kit only when fitted | +140 kg and a 2.8 × 1.5 m body: a different vehicle | zero: the ATV is unchanged | +140 kg on every unit; the body grows to 2.8 × 1.5 m |
| Retraction needed | only if the marine-range drive is fitted; wheels can stay down in shallow water | yes (−50°) with hull flaps | **no**: the ATV sits in dry wells inside the dock | yes |
| Complexity | sponsons + 15–30 kW jet module + bilge + sealed corners | new hull, jet, flaps, seals, second pack, naval architecture | a boat + a locking interface (hitch + node hardpoints) + an HV connector | as B |
| Product story | "it can cross water" | "it is a Quadski" | "it comes with a boat" | "every ARC-2B is amphibious" |
| Verdict | **swim kit: viable, cheap, honest** | **the real amphibious product; a separate programme** | **lowest-risk way to sell a water mode; recommended as the first marine offer** | rejected: forces the marine mass and size on riders who never see water |

**Clear statement:** the land chassis, as an ATV-sized body, cannot become a boat. Weight (636 kg afloat) and size (1.95 × 1.10 m tub with four arches) prevent it. Any drawing that shows the ATV body planing with wheels tucked into sealed bays is not achievable at this size.

## 8.2 Recommended marine strategy

1. **Now (V0):** Option C, the removable hull. A 3.2 × 1.8 × 0.6 m rotomoulded PE or 5083 landing-craft hull with four dry wheel wells, a bow ramp, a 40–60 kW electric jet module and its own 15–20 kWh pack (or an HV umbilical from the ATV). The ATV drives in over the ramp, its front bumper engages a cradle, the hitch pin locks to the transom bracket, the rider stays seated. Buoyancy and stability are boat problems solved by a boat; the ATV's only marine requirements are IP67 corners and an HV connector.
2. **Later:** Option B, ARC-2B M, when the land vehicle is proven.
3. **Optional:** the swim kit (Option A with sponsons) for calm-water crossings at walking pace, if the product needs it; it is the only option that makes the base vehicle itself float.

## 8.3 ARC-2B M variant design (so the future programme has a starting point)

| Item | V0 value | Status |
|---|---|---|
| Hull geometry | 2.8 m LOA, 1.5 m beam, 0.55 m depth, deadrise 12° at 0.4 LWL, two lifting strakes, flat aft pad for the intake; 5083-H116 (4 mm bottom, 3 mm sides) or infused glass/epoxy | TARGET |
| Displacement / buoyancy | 727 kg → 0.727 m³; hull volume 1.43 m³ less arches 0.36 m³ → reserve 48% | DERIVED |
| CG / CB | CG 0.80 m above keel with rider (TARGET); KB 0.15 m; BM 0.92 m at 2.8 × 1.5 → GM +0.27 m at rest; +0.46 m at 1.6 m beam | DERIVED (first order) |
| Stability | ISO 12217-3 offset-load and swamped tests as voluntary targets (the RCD excludes amphibious vehicles [REG-5]; US federal flotation rules exclude them [MST-2]); rider lean 100 kg × 0.5 m → ~15° heel at GM 0.27: **prefer 1.6 m beam** | TARGET |
| Waterline / freeboard | draft 0.28 m, freeboard 0.27 m (2.8 × 1.5) | DERIVED |
| Sealing | one sealed pivot cartridge per corner through the tub side (double lip + labyrinth + purge, 0.5 m head test); three watertight compartments; battery box IP68 with a float switch | TARGET |
| Wheel wells | free-flooding arches; hull-hinged flaps close the planing surface under the retracted wheels (WaterCar family possibly active to ~2029 [PAT-9]: FTO item) | TARGET |
| Water intake | flush grate, weed rake, aft pad; Gibbs guidance thrust/intake-length ≥ 18 kN/m [PAT-26] | TARGET |
| Jet | 155–160 mm axial PWC pump on a dedicated 80 kW peak / 30 kW continuous marine motor (not the traction motors) | TARGET |
| Steering nozzle | ±25°, cable from the handlebar coupled with the rack (expired Gibbs pattern [PAT-28]) | TARGET |
| Reverse | electric reverse bucket with neutral detent (iBR pattern [JET-4]); braking afloat is the bucket | TARGET |
| Cooling | closed glycol loop, keel cooler or raw-water heat exchanger on the pump's pressure tap | TARGET |
| Drainage | two 1,100 GPH bilge pumps on independent float switches [MAR-1], transom drain plugs, arch scuppers | TARGET |
| Flood protection | foam-filled forward and side voids; high-water alarm at 50 mm; inflatable collar in the sills | TARGET |
| Energy | 20 kWh (+8 kWh over the base pack) for ~1.5 h mixed use at 10–12 kWh/h [JET-6] | TARGET |

## 8.4 Marine transformation (variant): is it really possible?

Yes, with the constraints of Section 6.7 Sequence D and only on the variant hull: stop → hatch/bilge/IMD confirmation → afloat detection (arm sensors) → thrust confirmation → symmetric retraction to −50° with hull flaps → land drive contactor open → displacement mode → planing gates. The sequence is the one Gibbs and Aquastrada documented (expired) [PAT-41][PAT-42]. It is not possible on the base vehicle because there is no hull to float on; the swim kit's sponsons make the base vehicle float, but with the wheels down or only partly raised (the base actuator sweeps 12°→50°, not to −50°), at displacement speed.
