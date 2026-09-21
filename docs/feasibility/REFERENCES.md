# References and source-verification status

## How to read the tags

| Tag | Meaning |
|---|---|
| **S** | Search-snippet level. The title, URL and the quoted numbers were seen in web-search result snippets during this study. The page itself could **not** be fetched (see below). Verify against the URL before quoting externally. |
| **F** | Fetched and read in full during this study (GitHub-hosted primary files only). |
| **B** | Standard textbook or standard; existence is not in doubt, but the specific clause/number quoted was not read during this study. |
| **N** | Not retrieved in this study; listed because it is the primary document to obtain. |

### Why there are no fetched manufacturer, patent or standards pages

This study was produced in a managed environment whose egress policy returned
HTTP 403 on every CONNECT to manufacturer, patent-office, standards-body,
publisher and encyclopaedia hosts (patents.google.com, iso.org, ecfr.gov,
eur-lex.europa.eu, polaris.com, camso.co, hamiltonjet.com, taigamotors.com,
thomsonlinear.com, linak.com, arxiv.org, ieeexplore.ieee.org, sciencedirect.com,
wikipedia.org and others). The web-search budget was also exhausted during the
research phase. The research team was instructed not to route around policy
denials. Consequently:

- **Every external number in this study is tagged S, B or N, never F,** except
  robot URDF/source files hosted on GitHub.
- Where two snippets disagreed, both values are given.
- The **first task on the "DO NOT BUILD YET" list (Part 18) is a citation
  verification pass** against the URLs below from an environment with normal
  web access. Nothing in this document should be quoted to a supplier,
  regulator or investor before that pass.

Nothing in this file is fabricated: each entry is a real title/URL as it
appeared in search results. Where a number could not be seen, the entry says
"not retrieved".

---

## A. Wheel-leg robots and articulated-wheel vehicles

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [WL-1] | Hyundai, "Hyundai unveils TIGER uncrewed Ultimate Mobility Vehicle concept" (2021), https://www.hyundai.news/eu/articles/press-releases/hyundai-unveils-tiger-uncrewed-ultimate-mobility-vehicle-concept.html ; Motor Authority coverage https://www.motorauthority.com/news/1131225_hyundai-tiger-x-1-concept-walking-car-could-be-a-lifesaver | S | TIGER X-1 is ~26 lb, cargo-only; Elevate was a show concept; no rider-scale walking car built |
| [WL-2] | Boston Dynamics Handle, https://robotsguide.com/robots/handle ; https://www.techbriefs.com/component/content/article/34258-boston-dynamics-wheeled-handle-robot-handles-boxes-and-warehouse-logistics | S | 105 kg, 2 m, ~9 mph, electric + hydraulic, warehouse only |
| [WL-3] | ETH RSL / Swiss-Mile wheeled-legged ANYmal, Science Robotics 9, eadi9641 (2024), https://www.science.org/doi/abs/10.1126/scirobotics.adi9641 ; arXiv 2405.01792 ; IEEE Spectrum https://spectrum.ieee.org/delivery-robot-anymal | S | 22 km/h, ~50 kg payload, hybrid walk/drive, ~50 kg robot |
| [WL-4] | ANYmal C URDF, https://raw.githubusercontent.com/leggedrobotics/anymal_c_simple_description/master/urdf/anymal.urdf | F | joint limits 80 N·m, 7.5 rad/s; leg link ~2 kg |
| [WL-5] | Klemm et al., Ascento, ICRA 2019 / arXiv 2005.11435; RL step climbing arXiv 2402.06143 | S | four-bar leg, one hip actuator, body height 31–66 cm, 15 cm steps |
| [WL-6] | NASA JPL ATHLETE, iSAIRAS 2008, https://robotics.jpl.nasa.gov/media/documents/ATHLETE_iSAIRAS_2008.pdf | S | ~850 kg, 300 kg payload, six 6-DOF limbs with wheels; ~10 km/h |
| [WL-7] | Lin et al., Quattroped (IEEE/ASME T-Mech 2014, doi 10.1109/TMECH.2013.2253615 as listed) and TurboQuad (IEEE T-RO 2017), https://ieeexplore.ieee.org/document/6508894/ ; https://ieeexplore.ieee.org/document/7932521/ | S | rim-splitting transformable wheel; same motors for both modes |
| [WL-8] | Momaro (Uni Bonn), arXiv 1810.01345; Frontiers Robotics & AI 2016 doi 10.3389/frobt.2016.00057 | S | four compliant legs each with steerable wheel pair; DRC 2015 |
| [WL-9] | Tencent Ollie, PMC9888428 | S | base-mounted five-bar legs, eight motors |
| [WL-10] | Unitree B2-W and Go2-W URDFs, https://raw.githubusercontent.com/unitreerobotics/unitree_ros/master/robots/b2w_description/urdf/b2w_description.urdf ; go2w_description.urdf ; product page https://www.docs.quadruped.de/projects/b2/html/b2_w_ott.html | F (URDF) / S (product) | B2-W: joint limits 200/200/320 N·m, wheel 20 N·m; wheel module adds ~2.8 kg per leg (~15%) |
| [WL-11] | LimX TRON1 WF URDF, https://raw.githubusercontent.com/limxdynamics/tron1-robot-description/master/pointfoot/WF_TRON1A/urdf/robot.urdf | F | 80 N·m leg joints, 40 N·m wheel |
| [WL-12] | DDT TITA SDK, https://github.com/DDTRobot/TITA-SDK-ROS2 | F | shipped wheel-leg product with 0.1–0.3 m height adjustment |
| [WL-13] | Mantis hexapod (Micromagic Systems), https://en.wikipedia.org/wiki/Mantis_the_spider_robot ; https://www.engineering.com/the-mantis-walking-machine/ | S | 1,900 kg rideable hydraulic hexapod, ~1 km/h; the only verified human-riding walking machine |
| [WL-14] | Swincar e-Spider spec sheet, https://www.swincar.net/public/files/68d26da8dbf90.pdf ; https://alma-groups.com/wp-content/uploads/2026/02/swincar.pdf ; New Atlas https://newatlas.com/automotive/swincar-tandem-mobility/ | S | ~200 kg with 4 kWh; 4 in-wheel motors 4.16 kW cont / 10 kW peak / 380 N·m; passive pendular arms |
| [WL-15] | Rivian "tank turn" cancellation, https://www.chicagobusiness.com/manufacturing-logistics/why-rivian-canceled-highly-touted-tank-turn-feature/ ; https://insideevs.com/news/532416/rivian-tank-turn-feature-delayed/ | S | mixed-mu and surface-damage problems of zero-radius turns |
| [WL-16] | Wensing et al., "Proprioceptive Actuator Design in the MIT Cheetah", IEEE T-RO 33(3), 2017; parameters from https://raw.githubusercontent.com/mit-biomimetics/Cheetah-Software/master/common/include/Dynamics/Cheetah3.h | S (paper) / F (params) | ~240 N·m knee on a ~45 kg robot; backdrivable planetary |
| [WL-17] | Open Dynamic Robot Initiative actuator module, https://raw.githubusercontent.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/master/mechanics/actuator_module_v1/README.md | F | belt-reduction actuator template |
| [WL-18] | Norton, *Design of Machinery*, 6th ed., McGraw-Hill 2020, ISBN 9781260113310 | B | four-bar synthesis, Grübler mobility |
| [WL-19] | "Design Optimization of a Four-Bar Leg Linkage for a Legged-Wheeled Balancing Robot", Springer 2022, doi 10.1007/978-3-031-15226-9_15 | S | four-bar leg optimisation |
| [WL-20] | "Design of Robot Leg with Variable Reduction Ratio Crossed Four-bar Linkage Mechanism" (ResearchGate 338938001); US 12,011,374 | S | variable mechanical advantage linkages |
| [WL-21] | SWheg arXiv 2210.15126; OmniWheg arXiv 2203.02118; "Ubiquitous Field Transportation Robots with Robust Wheel-Leg Transformable Modules" arXiv 2410.18507; Frontiers Mech. Eng. 2020 doi 10.3389/fmech.2020.609340 | S | minimal-actuator transformable wheels |

## B. Wheel retraction and active ride height

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [RET-1] | FAA-H-8083-31B, *Aviation Maintenance Technician Handbook — Airframe*, Vol. 2, Ch. 13 "Aircraft Landing Gear Systems", https://www.faa.gov/handbooksmanuals/aviation/aviation-maintenance-technician-handbook-airframe-volume-2 | S/B | over-centre side brace + locking link as downlock |
| [RET-2] | Gibbs Technologies, US 7,316,594 "Wheel suspension and retraction system"; US 7,314,394 "Amphibious vehicle retractable suspension" (priority GB 0311962.5, 24 May 2003), https://www.freepatentsonline.com/7316594.html ; https://www.freepatentsonline.com/7314394.html | S | hydraulic retraction isolated from coil springs/dampers; ≤ 5 s |
| [RET-3] | Gibbs, WO2009027646A1 "Amphibian"; US 2006/0234567 A1; US 11,766,908 B2 "Retractable wheel assembly for an amphibian"; US 2007/0006788 A1 "Hull for an amphibious vehicle"; US 7,766,709 B2 "Amphibious vehicle steering"; https://patents.google.com/patent/WO2009027646A1/en ; https://patents.google.com/patent/US11766908 ; https://patents.justia.com/assignee/gibbs-technologies-limited | S | planing amphibian with retractable suspension; family still being granted (2023) |
| [RET-4] | WaterCar, US 9,102,389 / US 10,953,966 "Wheel suspension and retraction apparatus", https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10953966 | S | hydraulic retraction, 8–15 s |
| [RET-5] | Audi predictive active suspension, https://www.audi-technology-portal.de/en/chassis/suspension-control-systems/audi-s8-predictive-active-suspension ; https://www.greencarcongress.com/2019/07/20190719-a8.html | S | 48 V electromechanical rotary actuator, ~1,100 N·m via harmonic drive, ±85 mm in 0.5 s, 10–200 W |
| [RET-6] | Mercedes E-Active Body Control, https://www.greencarcongress.com/2018/09/20180912-gle.html | S | 48 V hydraulic-over-air active suspension |
| [RET-7] | Bose Project Sound / ClearMotion, https://newatlas.com/clearmotion-bose-proactive-suspension/54375/ | S | linear EM active suspension abandoned for mass/cost; electro-hydraulic successor |
| [RET-8] | Polaris Dynamix / Fox Live Valve, https://www.polaris.com/en-us/off-road/technology/dynamix/ ; https://ridefox.com/blogs/stories/live-valve-x2-is-the-tech-behind-new-polaris-rzr-pro-r-and-turbo-r-ultimate-with-dynamix-dual-valve ; Can-Am Smart-Shox https://infoquad.com/en/dynamix-and-smart-shox-semi-active-suspension-revolutionizing-the-industry/ | S | powersports semi-active damping: 200 Hz, ~17 ms, damping only |

## C. Actuators

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [ACT-1] | Thomson Electrak HD brochure, https://www.thomsonlinear.com/downloads/actuators/Electrak_HD_Actuator_BRUK.pdf ; https://www.thomsonlinear.com/en/products/linear-actuators/electrak-hd | S | up to 16 kN dynamic / 18 kN static, IP67/IP69K static, IP66 dynamic, CAN J1939/CANopen, 16 kN models ≥ 5 mm/s |
| [ACT-2] | LINAK LA36 data sheet, https://cdn.linak.com/-/media/files/data-sheet-source/en/linear-actuator-la36-data-sheet-eng.pdf | S | 500–10,000 N, IP66 dyn / IP69K static, 5% duty at 10 kN |
| [ACT-3] | Curtiss-Wright Exlar Tritex II DC, https://actuation.curtisswright.com/en-gb/exlar-legacy-products/tritex-ii%C2%AE-dc-linear-actuator | S | 4.2 kN continuous roller-screw servo actuator, spring-applied brake option, IP65 |

## D. ATVs, electric powersports, tracks, skis, snowmobiles

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [ATV-1] | Polaris Sportsman 570 (2025) specs, https://www.polaris.com/en-us/off-road/sportsman/2025/models/sportsman-570/sportsman-570-eps-sage-green-specs/ ; https://www.jdpower.com/motorcycles/2025/polaris/sportsman-570-premium-567cc/specs | S | 348 kg dry, 50.5 in wheelbase, 290 mm clearance, 208/241 mm travel, 612 kg tow, racks 41/82 kg |
| [ATV-2] | Yamaha Grizzly 700 EPS specs, https://yamahamotorsports.com/models/grizzly-eps/specs ; https://www.atv.com/specs/yamaha/utility/2015/grizzly/700-fi-auto-4x4-eps/detail.html | S | 318 kg wet, 1,250 mm wheelbase, 287 mm clearance, 193/231 mm travel, 590 kg tow |
| [ATV-3] | Can-Am Outlander 1000R (2026), https://www.atv.com/specs/can-am/utility/2026/outlander/1000r/detail.html ; MY23 XT 1000R NZ sheet https://can-am.brp.com/content/dam/apac/en/can-am-off-road/my23/spec-sheets/atv/outlander/MY23-ATV-OUTLANDER-XT-1000R-NZ_FA.pdf | S | 427 kg dry, 1,342 mm wheelbase, 292 mm clearance, 830 kg tow |
| [EV-1] | Polaris Ranger XP Kinetic Ultimate specs, https://military.polaris.com/en-us/ranger-xp-kinetic-ultimate-icy-white-pearl/specs/ | S | 29.8 kWh, 110 hp / 140 lb-ft, 1,754 lb dry, 80 mi, 2,500 lb tow |
| [EV-2] | Taiga Nomad, https://www.taigamotors.com/en/products/nomad/ ; Electrek 2026 https://electrek.co/2026/03/12/taiga-launches-120-kw-electric-snowmobiles-ccs-fast-charging/ ; The Drive https://www.thedrive.com/new-cars/44588/driving-an-electric-snowmobile-is-a-blast-but-range-could-be-a-dealbreaker | S | 23 kWh, 90–120 hp, < 600 lb, 60–87 mi claimed; 2027 gen 120 kW peak, CCS |
| [EV-3] | Ski-Doo Grand Touring Electric MY26 spec sheet, https://ski-doo.brp.com/content/dam/global/en/ski-doo/my26/spec-sheets/na/en/SKI-MY26-GT-EV-SPEC-ENNA-Page-LR.pdf | N | Rotax E-Power; 120 × 14 in track (dealer listing) |
| [EV-4] | Volcon Grunt EVO, https://newatlas.com/motorcycles/volcon-grunt-evo/ ; DRR EV Stealth https://www.drrusa.com/adult-electric-atvs-utvs-motorcycles | S | 2.3–4 kWh recreational e-ATVs, 4–8 kW |
| [TRK-1] | Camso UTV 4S1, https://powersports.camso.co/en-us/atv-utv/track-systems/utv-4s1 ; Tatou 4S retail https://www.socalpowersports.com/series-356172-camso-tatou-4s-atv-track-systems.html ; Camso Tatou 4S manual MY2015 https://camso.co/assets/services/PS_AU/Tatou4S_Manual_English_MY2015.pdf | S / N | 2,470 in² footprint; "double tandem stabilizer"; Tatou 4S "73.0 lbs" (basis unclear) |
| [TRK-2] | Polaris Prospector Pro 2.0 ATV tracks, https://www.polaris.com/en-us/shop/off-road/accessories/tracks/atv-tracks/2889493/ ; kit instructions https://cdn.polarisportal.com/servicemanagement-public/KitInstructions/MY2022_PROSPECTOR_PRO_ATV_EN_A.pdf | S / N | 97 lb (likely per track), F 42.5 × 25 in, R 52 × 25 in |
| [TRK-3] | Can-Am Apache 360 / 360 LT / Backcountry, https://can-am-shop.brp.com/off-road/us/en/715006323-apache-360-track-system.html ; https://atvmag.com/article.asp?nid=4088 | S | ~16 in clearance; Backcountry 14 × 138 in rear, 13.5 × 96 in front, 2,830 in², 0.44 psi, +7 in clearance |
| [TRK-4] | Mattracks LiteFoot, https://www.forconstructionpros.com/equipment/attachments/track-systems/product/10082896/mattracks-litefoot-atv-track-system ; https://en.wikipedia.org/wiki/LiteFoot_ATV | S | 1,716 in² contact, pivoting four-link with adjustable down pressure |
| [TRK-5] | US 5,607,210 A "Wheel mount track conversion assembly", https://patents.google.com/patent/US5607210A/en | S | adjustable pillow-block idlers for tension; resilient anti-torque coupler |
| [TRK-6] | CA 2825509 A1 "Track assembly for an all-terrain vehicle"; US 10,266,215 B2 "Track system for traction of an off-road vehicle"; US 2012/0001478 A1; US 7,921,942 "Amphibious all terrain vehicle with track assemblies" | S | idler-based tensioning; pivoting idler links; amphibious tracked ATV precedent |
| [SKI-1] | Timbersled ARO 3 specs, https://www.timbersled.com/en-us/snow-bikes/aro-3/specs/ | S | front ski kit 7.25 kg; rear kit 48 kg; 1.83 m long |
| [SKI-2] | Diamond J Customs ATSki hub-mount ATV ski kit, https://diamondjcustoms.com/product/atski-conversion-kit-for-the-popular-4-144mm-and-4-156mm-bolt-patterns-2/ | S | skis bolt to hub bolt circle with stock lug nuts; ~1 h install; deep snow needs rear tracks |
| [SNO-1] | Ski-Doo track tension procedure, https://ski-doo.brp.com/us/en/owner-zone/how-to/maintenance-tips/how-to-adjust-track-tension-on-your-ski-doo-snowmobile.html ; Expedition manual https://www.manualslib.com/manual/1121027/Ski-Doo-Expedition-Series.html | S | 7.3 kg (16 lb) → 32–50 mm deflection |
| [SNO-2] | Polaris track tension KA-02677 / KA-01420, https://www.polaris.com/en-us/snowmobiles/owner-resources/help-center/article/KA-02677/ | S | 10 lb at 16 in ahead of rear idler → 7/8–1 1/8 in |
| [SNO-3] | Track pitch/width explainers, https://www.snowtechmagazine.com/track-pitch-changing-specification/ ; https://www.denniskirk.com/blog/2013/12/30/the-ultimate-snowmobile-traction-buying-guide/ | S (trade press) | 2.52 / 2.86 / 3.0 in pitch; 14–20 in widths |

## E. Amphibians, water jets, hulls, marine standards

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [AMP-1] | Gibbs Quadski, https://en.wikipedia.org/wiki/Gibbs_Quadski ; https://gibbsamphibians.com/platform/quadski/ ; https://www.jetdrift.com/gibbs-quadski-review/ ; https://www.autoevolution.com/news/the-gibbs-quadski-was-a-revolutionary-amphibious-vehicle-that-deserves-to-be-remembered-197204.html | S | 605 kg, 100 kW on water (≈ 60 kW on land), 72 km/h land and water, 3.26 m × 1.59 m, wheelbase 1.79 m, 226 mm clearance, ≤ 5 s retraction, ~1,000 built 2012–16, production ceased |
| [AMP-2] | Gibbs Aquada, https://en.wikipedia.org/wiki/Gibbs_Aquada | S | 1,450 kg, 130 kW, 30 mph water |
| [AMP-3] | Gibbs Biski/Triski/Terraquad concepts, https://newatlas.com/gibbs-sports-amphibians-concept-vehicles/39912/ ; https://utvactionmag.com/feature-gibbs-terraquad/ | S | Biski 41 kW → 37 mph water on a two-wheeler; Terraquad 140 hp, 45 mph water |
| [AMP-4] | WaterCar Panther, https://en.wikipedia.org/wiki/Panther_(amphibious_vehicle) ; https://newatlas.com/watercar-panther-amphibious-jet-boat-water-fun/28099/ | S | 1,338 kg, 227 kW, hydraulic retraction into open wells, 44 mph water |
| [AMP-5] | Amphicar 770, https://en.wikipedia.org/wiki/Amphicar | S | 32 kW, twin props, ~7 mph displacement |
| [AMP-6] | Sealegs, https://en.wikipedia.org/wiki/Sealegs_Amphibious_Craft ; https://www.proboat.com/2015/07/amphibious-add-on/ | S | hydraulic retracting/driven wheels; system mass ~600 kg; wheels retract above hull |
| [AMP-7] | Iguana Yachts, https://www.iguana-yachts.com/technology/ | S | tracked landing gear deploys/locks in 8 s |
| [AMP-8] | CAMI Hydra Spyder, https://camillc.com/hydra-spyder/ | S | wheels tuck in to form flat hull; cavities foam-filled |
| [AMP-9] | Argo 8×8, https://www.shanksargo.com/operating-your-argo-on-water/ ; https://www.tradefarmmachinery.com.au/review-argo-8x8-frontier/ | S | tyre-paddle propulsion ~5 km/h; water payload derated |
| [AMP-10] | Amphibious hydrodynamics: Ocean Eng. 2021 S0029801821004042 (wheels raise resistance 14–28%); Ocean Eng. 2020 S0029801820304790; Ships & Offshore Structures 18(7) 2023 doi 10.1080/17445302.2022.2093032; US 12,097,733 (wheel-well flaps) | S | exposed wheels add 14–28% resistance; wheel-well closure matters |
| [JET-1] | Soundings, "Waterjets: the other marine propulsion", https://soundingsonline.com/news/on-powerboats-waterjets-the-other-marine-propulsion/ ; GlobalSecurity waterjet page; US 6,193,571 | S | ~40% propulsive efficiency for jets vs ~65% props at ~16 kn; cavitation at low speed/high power |
| [JET-2] | HamiltonJet, https://www.hamiltonjet.com/why-waterjets ; HJ brochure https://www.hamiltonjet.com/assets/main/hj-series-brochure-eng-2014.pdf | S | HJ range 80–900 kW (too large); selection by displacement |
| [JET-3] | PWC pumps: Sea-Doo 155.5/159 mm, https://jetskisint.com/blog/post/seadoo_impeller_chart ; Yamaha 155/160 mm axial single-stage, https://www.greenhulk.net/forum/personal-watercraft-performance-skis/yamaha-pwc-performance/yamaha-pwc-performance-4-stroke/124567-155-mm-vs-160mm | S (aftermarket) | 155–160 mm axial pumps carry 100–200 kW in PWCs |
| [JET-4] | Sea-Doo iBR, https://sea-doo.brp.com/us/en/discover/technologies/vehicle-technologies/ibr.html | S | reverse bucket for neutral/reverse/braking |
| [JET-5] | Taiga Orca, https://www.taigamotors.com/en/products/orca-p2/ ; https://www.jetdrift.com/taiga-orca-review/ | S | up to 120 kW, ~2 h claimed; kWh and mass not retrieved |
| [JET-6] | Narke GT95 Electrojet, https://www.mby.com/gear/narke-electrojet-gt95-carbon-jet-ski-116824 | S | 71 kW, 24 kWh, 43–47 mph, ~2 h / 50 km |
| [JET-7] | ZeroJet, https://www.zerojet.com/zerojet-systems ; https://newatlas.com/marine/zerojet-electric-outboard-motor/ | S | 14–30 kW 48 V electric jet modules, ~20 kg motor |
| [JET-8] | Candela C-8, https://candela.com/leisure-boats/candela-c-8/ | S | foiling reference: ~16 kW at 22 kn for 1,605 kg |
| [HUL-1] | Savitsky, "Hydrodynamic Design of Planing Hulls", SNAME Marine Technology 1(4), 1964; overview via https://par.nsf.gov/servlets/purl/10220322 | B/S | planing lift/drag method |
| [HUL-2] | Hull speed / Froude number, https://en.wikipedia.org/wiki/Hull_speed | S | 1.34 √LWL(ft) kn, Fn ≈ 0.4 |
| [HUL-3] | Sea-Doo Spark MY24 spec sheet, https://sea-doo.brp.com/content/dam/global/en/sea-doo/my24/documents/specs-sheets/na/en/SEA-MY24-REC-SPA-SPEC-ENNA-Page-PDFx.pdf | S | 194–207 kg dry, 60/90 hp, 2.79 m hull |
| [HUL-4] | ISO 12215-5:2019, https://www.iso.org/standard/69552.html | B/S | design pressures and scantlings, 2.5–24 m, planing kR = 1 |
| [MST-1] | ISO 12217-3 (EN ISO 12217-3:2025), https://www.iso.org/standard/79074.html | B/S | stability/buoyancy of boats < 6 m; swamped tests; categories C/D |
| [MST-2] | 33 CFR 183 Subparts F/G/H, https://www.ecfr.gov/current/title-33/chapter-I/subchapter-S/part-183/subpart-F | S | flotation rules; amphibious vessels explicitly excluded |
| [MST-3] | ABYC H-8-2022, https://webstore.ansi.org/standards/abyc/abyc2022-2483768 | B/S | flotation for boats < 6 m |
| [MST-4] | Directive 2013/53/EU (RCD), https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32013L0053 ; RCD Application Guide 2nd ed. 2022 | B/S | design categories C (Hs ≤ 2 m) and D (Hs ≤ 0.3 m) |
| [MST-5] | ISO 13590:2022 Personal watercraft, https://www.iso.org/standard/76684.html | B/S | PWC construction standard incl. flooding, off-throttle steering |
| [MST-6] | ISO 16315:2026 electric propulsion in small craft, https://www.iso.org/standard/84203.html | B/S | DC < 1,500 V propulsion systems |
| [MST-7] | ABYC E-30-2021 electric propulsion; ABYC E-13 lithium batteries, https://webstore.ansi.org/standards/abyc/abyc302021 ; https://panbo.com/abyc-publishes-updated-battery-and-electrical-standards/ | B/S | > 50 V DC treated as lethal; BMS, certification, restraint |
| [MAR-1] | Rule bilge pumps (1100 GPH), https://shop.hamiltonmarine.com/products/rule-bilge-pump-1100-gph--rule-a-matic--with-built-in-float-switch-12-volt-28547.html | S | ~4,160 L/h, ~4–5 A at 12 V |
| [MAR-2] | Marine aluminium alloys, https://continentalsteel.com/blog/marine-grade-aluminum-guide/ | S (trade) | 5083-H116 for hulls; 6061-T6 pitting/HAZ concerns |
| [MAR-3] | ISO 12944 corrosivity classes, https://international.brand.akzonobel.com/m/5f44067b30402a97/original/ISO12944_UK_LR.pdf | S/B | C5 marine; 80–200 µm/yr unprotected steel |

## F. Standards and regulation (land)

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [STD-1] | ANSI/SVIA 1-2017 and CPSC 16 CFR 1420, https://svia.org/about-the-atv-standard/ ; https://www.ecfr.gov/current/title-16/chapter-II/subchapter-B/part-1420 ; Federal Register 2023-15478 | N / S | mandatory US ATV standard (pitch/lateral stability, brakes, speed limiters) |
| [STD-2] | ANSI/ROHVA 1 (via CPSC docket), https://downloads.regulations.gov/CPSC-2009-0087-0118/attachment_6.pdf | S | Kst chosen over SSF because front/rear track widths may differ; tilt-table pitch stability |
| [STD-3] | Regulation (EU) 168/2013 Annex I, https://eur-lex.europa.eu/eli/reg/2013/168/oj/eng ; UK L-category classification annex | S | L7e-B heavy all-terrain quad: 15 kW net power cap; mass classes 425/450/600 kg |


## G. Patents (official front-page PDFs read where marked P)

Tag **P** = the official granted-patent or published-application PDF was fetched from Google Patents' document store and its front page (number, title, assignee, dates, abstract, PTA) was read. Legal status flags were not visible; expiry estimates are nominal (20 years from earliest non-provisional filing plus printed PTA, if maintenance fees were paid). **This is not a freedom-to-operate opinion.**

| Key | Patent | Assignee / priority | Tag | Relevance |
|---|---|---|---|---|
| [PAT-1] | US 7,017,687 B1 "Reconfigurable articulated leg and wheel" | Sarcos, 2002 | P | wheel/leg morphing corner; est. expired ~2024 |
| [PAT-2] | US 7,398,843 B2 "Reconfigurable robot drive" | Boston Dynamics, 2005 | P | eccentric-axle wheel/leg; est. expiry ~Sep 2026 |
| [PAT-3] | US 7,734,375 B2 "Robot and robot leg mechanism"; US 8,126,592 B2 "Actuator system" | Boston Dynamics, 2004 / 2008 | P | hip abduction; load-staged hydraulic leg actuators; possibly active to ~2027 / ~2030 |
| [PAT-4] | US 6,502,657 B2 "Transformable vehicle" | Draper Lab, 2000 | P | stowed/deployed wheels; expired |
| [PAT-5] | US 12,103,331 B2 "Transformable wheel and leg assembly"; US 11,603,149 B2 "Vehicles and systems and components thereof"; US 2017/0120672 A1; WO2023205766A1; CN112623059A; CN109292017B | not confirmed (Hyundai-type and CN filings) | S | live post-2015 wheel-leg families needing professional search |
| [PAT-6] | US 7,322,864 B2 "Amphibious vehicles with retractable wheels" | Gibbs Technologies, GB 2004 | P | suspension protrudes through gaps in the planing surface; hinged covers; est. expired Oct 2025 |
| [PAT-7] | US 2005/0034911 A1 "Amphibious vehicle retractable suspension" | Darby (Gibbs), GB 2003 | P | hydropneumatic retraction; height-sensor gating; term ended 2024 |
| [PAT-8] | US 7,520,239 B2 "Retractable leg assembly for amphibious vehicle"; US 7,004,801 B2 "Amphibious vehicle" | Sealegs, NZ 2003 / 2001 | P | externally pivoted retracting leg with in-leg drive and extension-gated steering; est. expired |
| [PAT-9] | US 8,221,174 B2 and US 8,764,499 B1 "Amphibious vehicle" | J. D. March (WaterCar), 2007 | P | pneumatic retraction, self-closing hull flaps, wheel-to-jet steering coupling; **possibly active to ~2029** |
| [PAT-10] | US 5,531,179 A "Wheel-retraction apparatus and method for amphibious vehicle" | Roycroft, NZ 1994 | P | wheels to above-waterline position; steering self-cancels when retracted; expired |
| [PAT-11] | US 5,181,478 A "Amphibious vehicle with retractable wheels" | Berardi, 1991 | P | tracks/wheels retract into hermetically closed hull enclosures; expired |
| [PAT-12] | US 8,070,094 B2 "Aircraft landing gear actuator"; US 8,123,161 B1 "Aircraft landing gear unlock actuator" | Hamilton Sundstrand, 2008 | P | redundant EMA with brake; jam-tolerant lock-stay release; possibly active to ~2030 |
| [PAT-13] | US 7,188,804 B1 "Float retractable landing gear" | Boetto, 2004 | P | over-centre toggle down-lock; est. expired |
| [PAT-14] | US 2012/0032023 A1 "Flying vehicle retractable wing hinge and truss" | Samson Motorworks, 2010 | P | loads through latches, not hinges |
| [PAT-15] | US 6,095,275 A "Conversion system for all terrain vehicles" | Shaw, 1995 | P | front skis on spindle + rear tracks on rear axle; expired |
| [PAT-16] | US 8,418,792 B2 "Quick-release ATV skis" (+ US 9,457,831 B2) | Rivard, 2010 | P / S | ski-over-tyre clamp; possibly active to ~2031 |
| [PAT-17] | US 6,860,352 B2 "Spindle for convertible ski stance" | BRP, 2001 | P | ski spindle geometry; expired |
| [PAT-18] | US 6,874,586 B2 "Track assembly for an all-terrain vehicle" | A&D Boivin (Camoplast lineage), 2002 | P | early ATV track kit; expired |
| [PAT-19] | US 8,347,991 B2 and US 8,662,214 B2 "Track assembly for an all-terrain vehicle" | Camoplast Solideal (Camso), CA 2007 | P | asymmetric track contact patch; **possibly active to ~2028** |
| [PAT-20] | US 8,851,581 B2 "Independent suspension traction system for a vehicle" | Soucy International, 2010 | P | track cassette with internal suspension; **possibly active to ~2033** |
| [PAT-21] | US 7,425,044 B2 "Guide horn structure for endless track of high-speed multi-terrain vehicles" | Soucy, 2001 | P | rubber track carcass/guide horns; expired |
| [PAT-22] | US 8,910,738 B2 "Snow bike conversion system" | Mangum (Timbersled/Polaris), 2011 | P | cassette on existing pivots, jackshaft drive; possibly active to ~2031 |
| [PAT-23] | US 5,607,210 A "Wheel mount track conversion assembly" | Brazier (Mattracks), 1994 | P | bolt-on cassette with drive drum, idlers, tension adjuster, resilient anti-torque coupler; expired |
| [PAT-24] | US 2014/0231157 A1 "Continuous track drive system for a vehicle" | Green, 2011 | P | idler/tensioner geometry |
| [PAT-25] | US 9,457,853; US 10,005,507; US 9,643,667; US 2020/0079443 | Camso / Soucy continuations | S | active hydraulic tensioner with passive fallback; later track families |
| [PAT-26] | US 2006/0264126 A1 "Jet drive for an amphibious vehicle" | Gibbs, GB 2003 | P | thrust/intake-length ≥ 18 kN/m to plane despite open arches; term ended 2024 |
| [PAT-27] | US 7,438,611 B2 "Propulsion system for an amphibious vehicle" | Gibbs, GB 2003 | P | shared prime mover mode logic, starter interlock; est. expired May 2024 |
| [PAT-28] | US 7,766,709 B2 "Amphibious vehicle steering" | Gibbs, GB 2003 | P | rack links fold on retraction; cable to steerable jet; est. expired |
| [PAT-29] | US 7,311,567 B2 "Amphibious vehicle" (sit-astride) | Gibbs, GB 2004 | P | the Quadski patent: planing ATV, length ≥ 2,400 mm, beam ≥ 1,250 mm, deadrise ≥ 10°; est. expired Oct 2025 |
| [PAT-30] | US 6,428,370 B1; US 6,652,332 B1 (reverse gates) | BRP, 2001 | P | jet reverse gate/braking; expired |
| [PAT-31] | US 7,892,053 B2 "Commonly actuated trim and reverse system" | Teleflex Megatech, 2006 | P | one actuator for trim + reverse; possibly active to ~2027 |
| [PAT-32] | US 6,729,918 B2 "Jet-propelled watercraft" | Honda, 2001 | P | bucket cable routing; expired |
| [PAT-33] | US 7,597,169 B2 "Wheel module" | GM, 2001 | P | everything-in-the-corner module with by-wire coupling; expiry ~Sep 2026 |
| [PAT-34] | US 8,720,623 B1 "In-wheel motor system" | Hyundai Mobis, KR 2012 | P | steered in-wheel cooling packaging; possibly active to ~2033 |
| [PAT-35] | US 7,938,210 B2 "Wheel-embedded suspension" | MIT, 2004 | P | removable robot-wheel corner; est. expired |
| [PAT-36] | US 6,257,604 B1 | Michelin, FR 1998 | P | Active Wheel root; expired |
| [PAT-37] | US 8,465,211 B2 "Compact wheel end and corner module" | Timken, 2009 | P | compact hub unit; possibly active to ~2030 |
| [PAT-38] | US 5,623,818 A "Rotatable in place powered vehicle" | Ledbetter, 1995 | P | tank-turn + mode switch + ride height; expired |
| [PAT-39] | US 2017/0043643 A1; WO2015158976A1; EP1885594B1 (pendular nacelle) | Swincar / Rambaud | S | pendular articulated vehicle |
| [PAT-40] | US 2023/0256787 A1 (REE adaptive suspension); US 11,590,977 B2 (Rivian K-turn); US 2024/0246607 A1; US 2023/0227102 A1 (Mobis 4WS); US 9,302,577 B2 (Protean) | as named | S | live corner-module families |
| [PAT-41] | US 2005/0239351 A1 "Amphibious vehicle" (mode-change controller with fault safeguards); US 2005/0170710 A1 (buoyancy-fraction sensing for mode change) | Gibbs family, GB 2003 / 2001 | P | transition supervisor and buoyancy gating; terms ended |
| [PAT-42] | US 5,562,066 A "Amphibious vehicle" | Aquastrada, 1992 | P | retract only when marine thrust confirmed; expired |
| [PAT-43] | US 7,938,358 B2 "Roadable aircraft with folding wings…" | Terrafugia, 2006 | P (front) / S (interlock detail) | multi-condition transformation interlock; possibly active to ~2030 |
| [PAT-44] | US 3,246,861 A "Convertible aircraft" | Curci, 1964 | P | mechanical mode-change interlock; expired |

## H. Manufacturing, suppliers, cost benchmarks

Tag **M** = fetched from a GitHub-hosted mirror of the primary text (legal texts: high fidelity; curated engineering reference sheets: secondary).

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [MFG-1] | Protolabs CNC tolerance guidance (cached in github.com/DimosGougousis/ProtoLabKB); Hubs manufacturing standards | M / S | ±0.13 mm standard, ±0.05 mm tight; ISO 2768 default |
| [MFG-2] | Tube bending guides (testtalkhq, Ever-Roll, The Fabricator) | S | mandrel bending CLR ≥ 2× OD for chromoly; rotary draw 2–4× OD |
| [MFG-3] | Lincoln Electric "TIG Welding Chrome-Moly Tubing" | S | no PWHT needed for thin-wall 4130 (< 0.120 in); 1,100 °F stress relief above; ER70S-2 / ER80S-D2 |
| [MFG-4] | ESAB "How to pass the tensile test with 6061-T6"; AWS D1.2 | S | as-welded 6061-T6 minimum 24 ksi vs 45 ksi parent; 30–50% HAZ loss |
| [MFG-5] | Process reference sheets (github.com/lpolovets/reference; github.com/giodl73-repo/MAXIM) | M (secondary) | sand casting $500–20k tooling; investment $5–50k; permanent mould $40–200k; rotomould $3–25k; RIM $5–50k; thermoform $5–50k; injection $50–500k; OOA prepreg vs infusion FVF and void data; metal PBF ±0.1 mm, Ti powder $200–400/kg; PA12 MJF ±0.3 mm |
| [MFG-6] | Protolabs / Jiga / Innovation Works injection-moulding break-even; Plastic Components Inc. thermoforming economics | S | break-even ~300–2,000 units; thermoforming cheaper below ~3,000–5,000/yr |
| [MFG-7] | Protolabs DMLS material data (cached); AlSi10Mg powder datasheet (github.com/Auricoalloys) | M | AlSi10Mg UTS 48–50 ksi; Ti-6Al-4V 144–153 ksi; AlSi10Mg yield 220–290 MPa |
| [SUP-1] | EMRAX 228 datasheet v1.7 values mirrored in github.com/jonelay/phase-sweep | M | 118 Nm cont / 220 Nm peak; 68 kW cont / 124 kW peak; 13.5 kg; 630 V |
| [SUP-2] | Cascadia Motion CM200DX / PM100DZ (FSAE team data mirrors) | M (secondary) | 80 kW peak class inverters used by low-volume builders |
| [SUP-3] | Elaphe M700 / L1500 (marketing text mirror); Kelly KLS-8080H; NetGain HyPer9; Sevcon Gen4; Delta-Q QuiQ | M (marketing, low confidence) | in-wheel 50 kW cont / 75 kW peak class; 72–96 V controllers; charger price $435 |
| [SUP-4] | Robotics actuator database github.com/nathmo/actuatorReview (cites MyActuator/CubeMars/Unitree manuals) | M (secondary) | RMD-X15 145/450 Nm, 3.5 kg, €1,600; X12 85/320 Nm; AK80-64 48/120 Nm; no IP ratings published |
| [SUP-5] | Linear actuator research note github.com/toneron2/robosnomo | M (secondary, uncited) | LINAK LA77 to 10 kN IP66–69K; TiMOTION MA2 to 8 kN IP66/67; Warner B-Track K2 9.8 kN |
| [SUP-6] | AMS AS5048A (project docs citing DS000298) | M | 14-bit absolute magnetic angle sensor |
| [SUP-7] | FlowBondTech research note (GitHub) | M (secondary) | Ranger XP Kinetic Ultimate $37,499 / 29.8 kWh; Can-Am Outlander Electric $12,999 / 8.9 kWh / 3 regen levels; e-ATV regen 10–33% |
| [SUP-8] | Polaris 10-K FY2015 (SEC text mirror) | M | Timbersled acquired 2015; SSCC standards adopted as regulation in some states/Canada with independent lab testing; ROHVA history; MSRP ranges |
| [SUP-9] | 2012 news mirror: Gibbs Quadski "around $40,000" | M | launch price |

## I. Regulation (verified legal text via mirrors)

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [REG-1] | 16 CFR 1420.3 (eCFR mirror github.com/AlextheYounga/ecfr) | M | ATVs made on/after 1 Jan 2025 must comply with ANSI/SVIA 1-2023 (owner's manual section per 1-2017) and be covered by a CPSC-approved ATV action plan |
| [REG-2] | 33 CFR 183.1 (eCFR mirror) | M | scope of USCG boat standards; amphibious applicability under 46 USC 43 not verified |
| [REG-3] | Regulation (EU) 168/2013 (mirror github.com/legalize-dev/legalize-eu) | M | L7e mass in running order ≤ 450 kg (passengers) excluding propulsion batteries; L7e-B ground clearance ≥ 180 mm; L7e-B1 ≤ 90 km/h, two straddle seats, handlebar; Art. 2 excludes vehicles primarily intended for off-road use |
| [REG-4] | Regulation (EU) 44/2014 and 2019/129 recitals (same mirror) | M | static stability (tilt) test requirements for L7e-B; OBD II exemption |
| [REG-5] | Directive 2013/53/EU (mirror github.com/DTMC-marketplace/governance) | M | **Art. 2(2)(a)(xiii): amphibious vehicles are excluded** from the RCD's design/construction requirements; PWC defined as < 4 m with water-jet primary propulsion |
| [REG-6] | Ontario O. Reg. 316/03 s.10 (mirror) | M | ORVs must meet ANSI/SVIA 1, ANSI/ROHVA 1, COHV 1/2/3 |

## J. Electric drivetrain, HV safety, battery, LV (Tag **D** = primary datasheet/manual PDF text extracted from a mirror)

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [MOT-1] | Protean ProteanDrive Pd18 datasheet (2018), https://www.proteanelectric.com/f/2018/05/Pd18-Datasheet-Master.pdf ; 2026 Pd18/Pd16 news mirror (github.com/zzzlf-1802/NEV-ElectricDrive) | S / M | Pd18 36–39 kg, 65–80 kW, 1,250–1,500 Nm; Pd16 28 kg, 40 kW peak / 26 kW cont, 800 Nm |
| [MOT-2] | Elaphe L1500 / M700 / S400, https://in-wheel.com/en/news/elaphe-announces-production-of-worlds-highest-performance-in-wheel-hub-motor/ ; https://www.emobility-engineering.com/elaphe-l1500-in-wheel-motor/ | S | L1500 33.3 kg; M700 ~23 kg, 75/50 kW; S400 17.6 kg, 40/29 kW, 400 Nm |
| [MOT-3] | YASA P400 series, https://yasa.com/media/2021/05/yasa-p400rdatasheet-rev-14.pdf | S / M | < 24 kg, 180/100 kW, 390/300 Nm axial-flux inboard |
| [MOT-4] | EMRAX 228 / 268 / 188 datasheets (v1.5–1.7) as quoted in FSAE repos, https://emrax.com/e-motors/emrax-228/ | M (secondary, consistent across 4 sources) | 228: 12.9–13.5 kg, 124 kW peak / 55–75 kW cont, 220–230 Nm peak; 188: 7.9 kg, 60/37 kW, 100/56 Nm; 268: 21.9 kg, 210/117 kW |
| [MOT-5] | Zero Z-Force 75-10, https://zeromotorcycles.com/en-au/model/zero-srf | S | 83 kW peak / 35 kW cont, 190 Nm, passive air cooling |
| [MOT-6] | HPEVS AC-34, Motenergy ME1616 (IP67, liquid, 26 kg, 55/20 kW), QS Motor QS273 (18 kg, 12/8 kW, IP67 claim), Plettenberg Nova 30 (6.2 kg, 30 kW peak), https://www.motenergy.com/mepmwaco.html ; http://www.qs-motor.com/product/3000w-8000w-electric-car-hub-motor273-model/ | S | powersports-scale motor options |
| [MOT-7] | Cascadia Motion CM200 inverter, https://www.cascadiamotion.com/cm-200 ; Swindon datasheet mirror | S / M | 6.8 kg, up to 225 kW, IP6K9K/IP67, HVIL support, 50–480 V DC |
| [UNS-1] | Lotus Engineering / Protean unsprung-mass study, https://www.proteanelectric.com/f/2020/06/The-maddening-myth-of-unsprung-mass_1.pdf ; IEEE Spectrum coverage | S | +30 kg per wheel on a Focus was "noticeable" but largely recoverable with damping |
| [UNS-2] | Wu et al., Proc. IMechE Part D 2025, https://journals.sagepub.com/doi/abs/10.1177/09544070241288615 ; Vehicle System Dynamics 64(5) 2025 doi 10.1080/00423114.2025.2465367 | S | increased unsprung mass raises wheel dynamic load and suspension travel |
| [UNS-3] | Hub motor sealing practice (trade), https://letrigo.com/blogs/knowledge/ebike-hub-motor-life-expectancy | S | thermal-shock seal failure (hot hub into cold water) |
| [TV-1] | Rivian quad-motor, https://rivian.com/quad ; Mercedes G 580 (Magna), https://www.designnews.com/automotive-engineering/magna-provides-the-mercedes-g-580-s-579-horsepower-electric-drivetrain ; Rimac torque vectoring page | S | per-wheel torque control at ≥ 100 Hz; G 580 uses 4 inboard motors each with a 2-speed reduction |
| [HV-1] | ISO 6469-1/-2/-3/-4, https://www.iso.org/standard/81746.html (Part 3) | B/S | class B voltage circuits, isolation Ω/V, HVIL, contact protection |
| [HV-2] | ISO 21498-1:2021 / LV123, https://www.iso.org/standard/78209.html | B/S | voltage class A ≤ 60 V DC; class B 60–1,500 V DC |
| [HV-3] | IEC 60529 / ISO 20653 IP codes; connector field guide mirror | M / S | IP67 = 1 m / 30 min; IP68 = declared; IP69K = 80–100 bar 80 °C jets (not immersion) |
| [HV-4] | UN R100 Rev.3 Part II Annexes 9A–9J, https://unece.org/sites/default/files/2024-01/R0100r3e.pdf | S | vibration, thermal shock, mechanical shock/integrity, fire, short, overcharge/discharge, over-temperature/current; 5-min thermal-propagation warning; no immersion test seen |
| [HV-5] | UL 2580, https://www.swri.org/markets/automotive-transportation/automotive/battery-testing-research/ul-2580-standard-battery-testing | S | includes seawater immersion and single-cell-failure tolerance |
| [HV-6] | FMVSS 305 / 305a NPRM 2024 | S | ≥ 500 Ω/V, or ≥ 100 Ω/V DC with isolation monitoring |
| [HV-7] | ISO 13063-1/-2/-3:2022 (electric mopeds/motorcycles); UN R136 (L-category REESS incl. drop test) | S | closest L-category HV safety analogues |
| [HV-8] | ISO 16750-2/-3/-4 | S | automotive environmental tests: transients, vibration by mounting location, thermal shock, salt spray, dust/water |
| [HV-9] | Formula Student EV rules (IMD ≥ 500 Ω/V, hardware shutdown without programmable logic; approved Bender IR155 / iso165C / iso175) | M | implementation floor for IMD |
| [HV-10] | **TE / Kilovac EV200 contactor datasheet** (mirror github.com/natecostello/van_two_point_oh) | D | 12–900 V DC, 500 A carry, 2,000 A break once, 0.43 kg, hermetic, 1.7 W hold, make ≤ 650 A to avoid welding; 50,000 cycles at 90% precharge vs 50 cycles at 80% |
| [HV-11] | **Bender ISOMETER iso165C / iso165C-1 manual D00154 rev. 04** (mirror github.com/DrJeffCooke/IsolationMonitorBender) | D | 0–600 V DC, 9–16 V supply < 2.5 W, defaults warning 300 kΩ / error 55 kΩ (C) and 400 / 250 kΩ (C-1), response ≤ 20 s, < 220 g, −40…+85 °C, CAN |
| [HV-12] | Precharge design notes: foxBMS docs; ZombieVerter training; Sensata whitepaper; Tesla PCS (95% threshold) | M / S | close main contactor at ≥ 90–95% bus voltage; 40–100 Ω / 50–100 W typical; abort on timeout |
| [HV-13] | HVIL practice: Aptiv, EV Engineering Online; foxBMS interlock driver (10 mA trip) | S / M | series 12 V loop through every HV connector/MSD/cover; last-make/first-break pins |
| [HV-14] | Eaton Bussmann EBPS pyro fuse; HV fuse sizing rules (IEC 60269-4; JASO D622) | S / M | < 1 ms interruption; 1.0–1.6 A/mm² conductor targets |
| [HV-15] | DC-link discharge rule (< 60 V within seconds after crash) | M | ISO 6469-3 practice |
| [BAT-1] | Molicel P45B / P42A 21700 (242 / 230 Wh/kg), Samsung 50E, LG M50 (256–270 Wh/kg); CATL LFP 205 Wh/kg cell; pack penalty 15–25%; industry pack mean ~162–175 Wh/kg, https://www.batterydesign.net/pack-gravimetric-energy-density/ | M / S | pack-level 150 Wh/kg is a conservative planning value |
| [BAT-2] | Taiga Orca pack, https://electrek.co/2019/09/18/taiga-motors-orca-electric-jetski/ | S | 23 kWh, 355 V, ~125 kg (≈ 184 Wh/kg), "IP68", temporary submersion (marketing) |
| [BAT-3] | Honda Mobile Power Pack e: (1.3 kWh, 10.3 kg, IP65); Gogoro (1.3 kWh, 9 kg) | S | swappable module benchmarks |
| [BAT-4] | Amphenol HVSL1000 / PowerLok; TE HVA HD400 (IP68 + IP6K9K, HVIL); Deutsch DT (LV) | S / M | sealed HV/LV connector classes |
| [BAT-5] | Sealed enclosure "breathing" note (ePTFE vents, 176 mbar vacuum on quench) — GitHub harness packaging research | M (secondary) | pressure-equalising vents mandatory on sealed modules |
| [BAT-6] | Thermal propagation mitigation (mica 1–3 mm, aerogel 2–5 mm, vent paths); GB 38031-2020 5-min rule | M / S | pack design requirements |
| [FS-1] | ISO 26262 ASIL metrics (SPFM/LFM/PMHF) — mirrored summaries; ISO 13849-1 categories/PL; ISO 25119 (agricultural) | M / S | safety framework choices for transformation actuators |
| [FS-2] | Steer-by-wire fail-operational MBSE example (dual sensors, dual 48 V feeds, force-fight detection > 20% for > 50 ms) | M (secondary) | reusable redundancy pattern |
| [FS-3] | UN R79 SbW amendments; UN R13-H EMB work | S | by-wire steering/braking regulatory direction |
| [LV-1] | Delta DAP-2500AB (Tesla DC-DC): 220–430 V in, 2.5 kW; Bel 350DNG40-12-8: 4 kW, IP67/IP6K9K, liquid | M / S | DC-DC class |
| [LV-2] | Audi eAWS 48 V electromechanical active suspension, https://www.audi-mediacenter.com/en/press-releases/comfortable-and-agile-audis-eaws-technology-turns-suvs-into-quick-change-artists-13080 | S | 48 V actuator precedent, 1,100 Nm per wheel |

## K. Structures, materials, fatigue, dynamics, stability, terramechanics, towing

| Key | Source | Tag | What it supports |
|---|---|---|---|
| [STR-1] | Formula SAE Rules 2024 §F.3 (text mirror github.com/anniedoris/design_qa) | M | tubing minimums (Size A 2.0 mm wall, 173 mm², 11,320 mm⁴); steel design values non-welded Sy 305 / Su 365 MPa, **welded Sy 180 / Su 300 MPa**; 6061-T6 non-welded Sy 240 / Su 290, **welded Sy 115 / Su 175 MPa**; composite attachment ≥ 30 kN |
| [STR-2] | Formula Student Rules 2025 T3 (mirror github.com/EmesOrdCo/3YP_Tracy) | M | impact attenuator test: 300 kg at 7 m/s, ≥ 7,350 J, ≤ 20 g average, ≤ 40 g peak |
| [STR-3] | Baja SAE roll-cage baseline quoted in NAU capstone / IOSR-JMCE papers | S | 1018 steel 25.4 × 3.05 mm baseline; equivalency by bending stiffness and strength |
| [STR-4] | Baja chassis FEA load-case practice (Ansys course; IJSR/IJARIIT papers) | S | case list: inertial, impacts, rollover, torsion, modal; **no g-factors given** |
| [STR-5] | AISI 4130 normalized (MatWeb) | S | UTS 670 MPa, yield 435 MPa, 25.5% elongation |
| [STR-6] | IIW Recommendations for Fatigue Design of Welded Joints (Hobbacher 2016) summarised in github.com/Morebenk/Stage-Ahmed | M (secondary) | FAT classes at 2×10⁶: steel butt 80–112, fillet toe 63–71, cruciform 36–56; aluminium 25–71; slope m = 3 |
| [STR-7] | EN 1993-1-9 detail categories (screening tool github.com/clay-good/anvilate) | M (secondary) | Δσ_C ladder 36–160 MPa; m = 3 to 5×10⁶, m = 5 to 10⁸ |
| [STR-8] | Aluminium has no endurance limit (machine-design notes; sdcverifier; Engineers Edge) | M (tertiary) / S | finite-life design with Goodman correction; 5×10⁸-cycle reference strength |
| [STR-9] | ISO 281 bearing life (SKF catalogue PUB BU/P1 17000/1 EN 2018 via calculators) | S | L10 = (C/P)^a; static safety s₀ for shock |
| [DYN-1] | Milliken & Milliken, *Race Car Vehicle Dynamics*, SAE 1995, ISBN 9781560915263 | B (bibtex verified) | installation ratio, roll centres, load transfer |
| [DYN-2] | Gillespie, *Fundamentals of Vehicle Dynamics*, SAE 1992, ISBN 9781560911999 | B (bibtex verified) | vehicle dynamics fundamentals |
| [DYN-3] | Wong, *Theory of Ground Vehicles*, Wiley, 4th ed. 2008 ISBN 978-0470170380 (5th ed. 2022) | B/S | terramechanics, tracked vehicle mechanics |
| [DYN-4] | Reimpell, Stoll, Betzler, *The Automotive Chassis*, 2nd ed. 2001, ISBN 9780750650540; Dixon, *Suspension Geometry and Computation*, Wiley 2009, ISBN 9780470510216 | B/S | suspension geometry |
| [DYN-5] | Load-transfer, anti-dive/anti-squat and SSF formulas (FSAE kinematics test suite github.com/frederikexd/kinematik; NHTSA SSF definitions) | M / S | ΔW = m·a_y·h/t; anti-% = F_x·tan φ/ΔW; SSF = T/2h |
| [STB-1] | NHTSA NCAP rollover SSF bands (ESV 05-0450; open tool) | S / M (tertiary) | 1 star ≤ 1.04; 5 stars ≥ 1.45; cars 1.3–1.5; SUVs 1.0–1.3 |
| [STB-2] | ANSI/SVIA 1 stability coefficients (Federal Register 2017-19341, 2023-15478; CPSC canvass) | S | **Kst ≥ 1.0 unoccupied; Kp > 1.0**; Kst formula not seen |
| [STB-3] | ANSI/ROHVA 1 stability tests (CPSC docket; 2014 NPRM) | S | tilt table 24° loaded / 30° two occupants; J-turn at 30 mph, 110° wheel input, ≤ 2 of 10 runs with two-wheel lift |
| [STB-4] | CPSC / SEA ATV attribute-modification baseline testing (Jan 2016) | S | SSF and Kst computed from lab measurements; J-turn correlation study; numeric CG not seen |
| [STB-5] | UNSW TARS Quad Bike Performance Project (2015) | S | stability primarily track width and CG; active rider effect |
| [TER-1] | Bekker, *Theory of Land Locomotion* (1956), *Introduction to Terrain-Vehicle Systems* (1969); Project Chrono SCM terrain header (verified) | M | p = (k_c/b + k_φ) z^n; Janosi–Hanamoto shear |
| [TER-2] | Ground pressure comparison (snowmobileinfo.org trail doc; Wikipedia ground-pressure table) | S | snowmobile ≈ 3.4 kPa; tracked ATV 3.8–6.2 kPa; wheeled ATV ≈ 13.8 kPa |
| [TER-3] | Sand tyre deflation (Wikipedia "Off-roading" mirror) | M (tertiary) | 35 psi → 12–14 psi for flotation |
| [TER-4] | Snow/ice friction (blog-grade; arXiv 2212.08524; Annals of Glaciology snow-block friction) | S (blog) | fresh snow μ 0.35–0.45; compacted/ice 0.12–0.18 (unverified) |
| [TER-5] | Snowmobile ride-dynamics model (ResearchGate 264440552); track–snow DEM/MBD papers (Springer 2024, IOP 2021) | S | modelling approaches |
| [HUL-5] | ISO 12215-5:2019 identity (relaton record) and 2008-text pressure approach (n_CG definition; deadrise bounds 10–30°) | M / S | slamming design pressure method; coefficients not seen |
| [HUL-6] | OpenPlaning (github.com/elcf/python-openplaning) implementing Savitsky 1964, Savitsky & Brown 1976, Fridsma 1971 | M | seaway acceleration estimation for planing hulls |
| [TOW-1] | SAE J684 coupling strength classes (PDF mirror) | S | Class 1: 26.7 kN longitudinal, 8.9 kN transverse, 11.1 kN vertical; Class 2: 46.7 / 13.3 / 20.0 kN |
| [TOW-2] | 49 CFR 393.71 (eCFR mirror) | M | tow-bar longitudinal strength 3,000 lb for towed GW < 5,000 lb; beam 0.6 × GW; two safety chains |
| [TOW-3] | Tongue weight guidance (GM via Wikipedia mirror) | M (tertiary) | 10–15% of trailer mass |
| [IMP-1] | ISO 7141:2005/2022 wheel impact test (relaton record; ISO sample pages); SAE J175 | M / S | 13° wheel axis; rim-flange impact; striker mass formula not seen |
| [IMP-2] | "3 g bump / 2 g braking / 1.5 g cornering" factors | **NOT FOUND in any source** | treated as study ASSUMPTIONS in `calc/params.py`, to be replaced by instrumented drop-test data |
| [BRK-1] | ANSI/SVIA 1-2023 §7 brake performance (read-only copy at svia.org/ansi-svia-1-2023/) | N | stopping-distance requirements not read |
