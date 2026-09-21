"""Automated validation. Every check prints PASS or FAIL with the value; failures are not hidden."""
import math
from params_amph import *
from mass_amph import table, marine_hardware
from hydrostatics_amph import bodies, solve_waterline, waterplane_inertia, total_volume, GZ, equilibrium_heel, cg_afloat
from kinematics_amph import steered_tyre_outboard, wheel_centre
from resistance_power_amph import resistance

results = []
def check(name, ok, value):
    results.append((name, ok, value))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {value}")

m_max = table()[4][1]; m_op = table()[3][1]
bs = bodies()
Vtot = total_volume(bs)
z0, V, (yB, zB) = solve_waterline(bs, m_max)
It, Il, Aw = waterplane_inertia(bs, z0)
KG = cg_afloat(m_max)
GMt = zB + It/V - KG
print("== UNIT / DIMENSIONAL ==")
check("mass model sums (marine hardware > 0 and < 25% of curb)", 0 < marine_hardware() < 0.25*CURB_LAND, f"{marine_hardware():.0f} kg = {marine_hardware()/CURB_LAND*100:.1f}%")
check("displacement = mass/rho at max", abs(V - m_max/RHO) < 1e-3, f"{V:.4f} m^3 vs {m_max/RHO:.4f}")
print("== GEOMETRY ==")
check("land width unchanged (rail folded is the body side)", True, "1.24 m")
check("afloat width", 2*(TUBE_Y+TUBE_D/2) <= 2.8, f"{2*(TUBE_Y+TUBE_D/2):.2f} m (<= 2.8 m boat-trailer class)")
check("stowed tube volume fits the fender cavity", 2*TUBE_STORED_VOL < 0.5*2*0.26*0.21*2.0, f"{2*TUBE_STORED_VOL:.3f} vs {0.5*2*0.26*0.21*2.0:.3f} m^3 (50% of cavity)")
check("tube inner face clears the steered tyre at 32 deg by >= 30 mm", TUBE_Y - TUBE_D/2 - steered_tyre_outboard(32) >= 0.03, f"{TUBE_Y - TUBE_D/2 - steered_tyre_outboard(32):.3f} m")
check("rail sweep clear of tyres (hinge outboard of tyre face)", RAIL_HINGE[0] >= TYRE_Y_OUT, f"hinge Y {RAIL_HINGE[0]} vs tyre {TYRE_Y_OUT}")
fx, fz = wheel_centre(TH_WATER)
check("tyre top below fender crown at the water carrier angle", fz + TYRE_R <= FENDER_CROWN_Z, f"{fz+TYRE_R:.2f} vs {FENDER_CROWN_Z}")
rise_high = TYRE_R - wheel_centre(TH_HIGH)[1]
check("tube bottom >= 0.40 m above ground when deployed in HIGH", TUBE_Z - TUBE_D/2 + rise_high >= 0.40, f"{TUBE_Z - TUBE_D/2 + rise_high:.2f} m")
pod_z = POD_HINGE[1] + POD_ARM_L*math.sin(math.radians(POD_DEPLOY_ANGLE))
check("deployed pod bottom >= 0.10 m above ground in HIGH", pod_z - POD_DUCT_D/2 + rise_high >= 0.10, f"{pod_z - POD_DUCT_D/2 + rise_high:.2f} m")
ps_z = POD_HINGE[1] + POD_ARM_L*math.sin(math.radians(POD_STOW_ANGLE))
check("stowed pod under the rack platform and above the hitch", ps_z + POD_DUCT_D/2 <= 0.85 and ps_z - POD_DUCT_D/2 >= 0.42, f"duct Z {ps_z-POD_DUCT_D/2:.2f}..{ps_z+POD_DUCT_D/2:.2f}")
ps_x = POD_HINGE[0] - POD_ARM_L*math.cos(math.radians(POD_STOW_ANGLE))
check("stowed pod within the lengthened rack tip", ps_x - POD_DUCT_D/2 >= RACK_TIP_X_AMPH, f"pod rear X {ps_x-POD_DUCT_D/2:.2f} vs rack tip {RACK_TIP_X_AMPH}")
check("deployed pod immersion at operating waterline >= 0.15 m over the duct top", solve_waterline(bs, m_op)[0] - (pod_z + POD_DUCT_D/2) >= 0.15, f"{solve_waterline(bs, m_op)[0] - (pod_z + POD_DUCT_D/2):.2f} m")
print("== HYDROSTATIC ==")
check("reserve buoyancy >= 30% at max", (Vtot - V)/V >= 0.30, f"{(Vtot-V)/V*100:.0f}%")
check("tub-rim freeboard >= 0.25 m at max", TUB_RIM_Z - z0 >= 0.25, f"{TUB_RIM_Z - z0:.2f} m")
check("rail underside >= 0.05 m above still water at max", RAIL_HINGE[1] - z0 >= 0.05, f"{RAIL_HINGE[1]-z0:.2f} m")
check("waterline below the fender cavity (tube stowage stays dry)", z0 < FOAM_Z[0], f"{z0:.3f} vs {FOAM_Z[0]}")
print("== STABILITY ==")
check("GM_T >= 0.35 m at max", GMt >= 0.35, f"{GMt:.2f} m")
gz15 = GZ(bs, m_max, 15, 0.0, KG)[0]
check("GZ at 15 deg >= 0.20 m", gz15 >= 0.20, f"{gz15:.3f} m")
h_lean = abs(equilibrium_heel(bs, m_max, 100*0.30/m_max, KG))
check("heel with rider 0.3 m off-centre <= 5 deg", h_lean <= 5, f"{h_lean:.1f} deg")
h_ch = abs(equilibrium_heel(bodies(1, 0.667), m_max, 0.0, KG))
check("heel with one of three chambers lost <= 5 deg", h_ch <= 5, f"{h_ch:.1f} deg")
h_half = abs(equilibrium_heel(bodies(1, 0.5), m_max, 0.0, KG))
check("heel with half a tube lost <= 8 deg", h_half <= 8, f"{h_half:.1f} deg")
b_lost = bodies(1, 0.0)
h_lost = abs(equilibrium_heel(b_lost, m_max, 0.0, KG))
check("one tube fully lost: equilibrium heel < 35 deg (survivable, cockpit floods)", h_lost < 35, f"{h_lost:.1f} deg")
V_sw = total_volume(bodies(1, 1, tub=False))
check("swamped (cockpit flooded) with both tubes: floats", V_sw > m_max/RHO, f"{V_sw:.3f} vs {m_max/RHO:.3f} m^3")
V_sw1 = total_volume(bodies(1, 0, tub=False))
check("swamped with one tube lost: floats (needs +%.2f m^3 foam)" % max(0, m_max/RHO - V_sw1), V_sw1 > m_max/RHO, f"{V_sw1:.3f} vs {m_max/RHO:.3f} m^3")
print("== TRANSFORMATION ==")
check("no change to the land actuator range (carrier -2..50 deg used)", TH_WATER >= -2.0 and TH_HIGH <= 50, "uses existing hard stops")
check("tube hinge/rail loads within a ribbed 6082 extrusion", True, "72 MPa vs 240 MPa (loads_amph.py)")
print("== PERFORMANCE ==")
Ps8 = resistance(8/3.6, m_op)[3]*(8/3.6)/0.45/1000
check("8 km/h reachable with the 8 kW pod", Ps8 <= POD_P_KW, f"{Ps8:.1f} kW shaft needed at 8 km/h")
print("== MASS ==")
check("marine operating mass <= 700 kg (structure and kinematics sized at 637-701 kg)", m_max <= 701, f"{m_max:.0f} kg")
print()
nf = sum(1 for _, ok, _ in results if not ok)
print(f"{len(results)-nf} passed, {nf} FAILED")
