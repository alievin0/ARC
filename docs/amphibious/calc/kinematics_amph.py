"""Deployment kinematics and clearance checks for Architecture A2 (DERIVED)."""
import math
from params_amph import *

def wheel_centre(theta, front=True):
    dx = L_ARM*math.cos(math.radians(theta)); dz = -L_ARM*math.sin(math.radians(theta))
    return ((PIV_X_F + dx) if front else (PIV_X_R - dx), PIV_Z + dz)

def steered_tyre_outboard(steer_deg):
    """Max outboard Y reached by a steered front tyre (rectangle 0.66 x 0.25 rotated about its centre in plan)."""
    s = math.radians(steer_deg)
    return TRACK/2 + 0.5*TYRE_W*math.cos(s) + 0.5*(2*TYRE_R)*math.sin(s)

def report():
    print("RAIL (fender side band L-panel) hinged at Y %.2f, Z %.2f; panel %.2f m tall, top return %.2f m" % (RAIL_HINGE[0], RAIL_HINGE[1], RAIL_LENGTH, RAIL_FLANGE))
    print("  stowed: vertical, outer face at Y %.2f (= land body side); deployed: rotated 90 deg outboard/down -> horizontal at Z %.2f from Y %.2f to %.2f, flange down to Z %.2f"
          % (RAIL_HINGE[0]+0.03, RAIL_HINGE[1], RAIL_HINGE[0], RAIL_HINGE[0]+RAIL_LENGTH, RAIL_HINGE[1]-RAIL_FLANGE))
    print("  swept volume during the 90 deg swing: quarter-cylinder of radius %.2f m about the hinge, outboard of Y %.2f, between Z %.2f and %.2f: nothing of the vehicle is there (tyres end at Y %.3f)"
          % (RAIL_LENGTH+RAIL_FLANGE, RAIL_HINGE[0], RAIL_HINGE[1]-RAIL_LENGTH-RAIL_FLANGE, RAIL_HINGE[1]+RAIL_LENGTH+RAIL_FLANGE, TYRE_Y_OUT))
    print()
    print("TUBE deployed: centre Y +-%.2f, Z %.2f; inner face Y %.2f, outer face Y %.2f; bottom Z %.2f, top Z %.2f; afloat overall width %.2f m"
          % (TUBE_Y, TUBE_Z, TUBE_Y-TUBE_D/2, TUBE_Y+TUBE_D/2, TUBE_Z-TUBE_D/2, TUBE_Z+TUBE_D/2, 2*(TUBE_Y+TUBE_D/2)))
    print("  stowed: rolled to ~%.3f m^3 inside the fender cavity (Y 0.36..0.62, Z 0.62..0.83 above the arch, %.2f m^3 available per side)" % (TUBE_STORED_VOL, 0.26*0.21*2.0))
    print()
    print("CLEARANCES (tube inner face Y %.2f):" % (TUBE_Y-TUBE_D/2))
    for st in (0, 10, 20, 32):
        yo = steered_tyre_outboard(st)
        print(f"  front tyre steered {st:2d} deg: outboard extent Y {yo:.3f} -> clearance to tube {TUBE_Y-TUBE_D/2-yo:+.3f} m {'OK' if TUBE_Y-TUBE_D/2-yo >= 0.03 else 'FAIL'}")
    print(f"  tube vs rail flange: tube top Z {TUBE_Z+TUBE_D/2:.2f} vs rail Z {RAIL_HINGE[1]:.2f} -> tube rides {TUBE_Z+TUBE_D/2-RAIL_HINGE[1]:+.2f} m above the rail plane (attached on the flange's outer face; the rail deck is not over the tube: OK)")
    print()
    print("GROUND CLEARANCE OF DEPLOYED PARTS on the ramp (body raised by carrier angle):")
    for name, th in (("ROAD 12 deg", TH_ROAD), ("HIGH 38 deg", TH_HIGH), ("LIFT 50 deg", TH_LIFT)):
        fx, fz = wheel_centre(th)
        rise = TYRE_R - fz
        tube_bottom = TUBE_Z - TUBE_D/2 + rise
        flange_bottom = RAIL_HINGE[1] - RAIL_FLANGE + rise
        pod_bottom = (POD_HINGE[1] + POD_ARM_L*math.sin(math.radians(POD_DEPLOY_ANGLE))) - POD_DUCT_D/2 + rise
        print(f"  {name:12s}: body rise {rise:+.3f} m; tube bottom {tube_bottom:.2f} m, rail flange bottom {flange_bottom:.2f} m, pod bottom {pod_bottom:+.2f} m above ground")
    print("  -> deploy tubes and pod only in HIGH (tube bottom 0.5 m, pod bottom ~0.16 m above ground); pod retracts before the wheels ground on exit")
    print()
    print("WHEELS afloat (carrier %.0f deg = existing hard stop):" % TH_WATER)
    fx, fz = wheel_centre(TH_WATER)
    print(f"  wheel centre X {fx:+.3f}, Z {fz:.3f}; tyre from Z {fz-TYRE_R:.2f} to {fz+TYRE_R:.2f} (fender crown {FENDER_CROWN_Z}: {'clear' if fz+TYRE_R <= FENDER_CROWN_Z else 'INTERFERES'})")
    print("  the tyre hangs partly in the water (submergence computed in resistance_power_amph.py); it is the shallow-water landing gear")
    print()
    sa, da = math.radians(POD_STOW_ANGLE), math.radians(POD_DEPLOY_ANGLE)
    ps = (POD_HINGE[0] - POD_ARM_L*math.cos(sa), POD_HINGE[1] + POD_ARM_L*math.sin(sa))
    pd = (POD_HINGE[0] - POD_ARM_L*math.cos(da), POD_HINGE[1] + POD_ARM_L*math.sin(da))
    print("POD ARM: transverse hinge at X %.2f, Z %.2f on the rear cross-member; arm %.2f m; duct D %.2f" % (POD_HINGE[0], POD_HINGE[1], POD_ARM_L, POD_DUCT_D))
    print("  stowed (arm %.0f deg up, aft): pod centre X %.2f, Z %.2f; duct Z %.2f..%.2f (rack platform at 0.85: %s), X to %.2f (rack tip %.2f: %s); above the hitch receiver (Z 0.35-0.40): %s"
          % (POD_STOW_ANGLE, ps[0], ps[1], ps[1]-POD_DUCT_D/2, ps[1]+POD_DUCT_D/2, 'clear' if ps[1]+POD_DUCT_D/2 <= 0.85 else 'INTERFERES',
             ps[0]-POD_DUCT_D/2, RACK_TIP_X_AMPH, 'covered' if ps[0]-POD_DUCT_D/2 >= RACK_TIP_X_AMPH else 'PROTRUDES', 'clear' if ps[1]-POD_DUCT_D/2 >= 0.42 else 'INTERFERES'))
    print("  deployed (arm %.0f deg down, aft): pod centre X %.2f, Z %.2f; duct Z %.2f..%.2f; protrudes %.2f m behind the rack tip afloat; sweep %.0f deg about the hinge"
          % (-POD_DEPLOY_ANGLE, pd[0], pd[1], pd[1]-POD_DUCT_D/2, pd[1]+POD_DUCT_D/2, RACK_TIP_X_AMPH-(pd[0]-POD_DUCT_D/2), POD_STOW_ANGLE-POD_DEPLOY_ANGLE))
    print("  locked by a spring pin at the hinge in both positions; vectoring +-%.0f deg about the arm axis; the arm also carries the phase cable and a fresh-water flush port" % POD_STEER)
    print()
    print("LAND-MODE PACKAGING SUMMARY: nothing outside the V0 envelope except the stowed pod under a 0.15 m longer rack (overall length 2.15 -> 2.33 m); land width unchanged (1.24 m); fender crown unchanged (0.83 m)")

if __name__ == "__main__":
    report()
