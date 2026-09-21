"""Steering geometry: Ackermann targets and a numerical proof that a tie-rod whose
inner joint lies on the corner pivot axis produces zero steer change over the
full carrier sweep and the full suspension travel (DERIVED)."""
import math
from params_v0 import *

def rad(d): return math.radians(d)

# Ackermann
cot = lambda d: 1/math.tan(rad(d))
delta_i_ideal = math.degrees(math.atan(1/(cot(MAX_STEER_OUTER) - TRACK_F/WHEELBASE)))
R_outer = WHEELBASE/math.sin(rad(MAX_STEER_OUTER))
print(f"Ackermann: outer {MAX_STEER_OUTER:.0f} deg -> ideal inner {delta_i_ideal:.0f} deg; V0 inner target {MAX_STEER_INNER:.0f} deg (partial Ackermann, typical)")
print(f"Minimum turning radius to the outer front wheel: {R_outer:.2f} m; knuckle arm angle for Ackermann: {math.degrees(math.atan((TRACK_F/2)/WHEELBASE)):.1f} deg toward the rear axle centre")

# Geometry in 3D (front-left corner). Pivot axis: line through P parallel to Y.
L = L_ARM
PIV = (0.161, ARM_PLANE_Y, 0.434)     # from kinematics (front pivot)
INNER = (PIV[0], 0.26, PIV[2])         # tie-rod inner ball joint ON the axis, 80 mm inboard of the inner bearing
def rot_about_axis(p, theta):
    """Rotate point p about the Y-parallel axis through PIV by theta (rad), in the XZ plane."""
    x, y, z = p[0]-PIV[0], p[1], p[2]-PIV[2]
    c, s = math.cos(theta), math.sin(theta)
    return (PIV[0] + x*c + z*s, y, PIV[2] - x*s + z*c)
# Outer joint on the knuckle arm at ROAD: wheel centre + steering arm pointing rearward-inward
WC = (PIV[0] + L*math.cos(rad(TH_ROAD)), TRACK_F/2, PIV[2] - L*math.sin(rad(TH_ROAD)))
arm_ang = math.atan((TRACK_F/2)/WHEELBASE)
OUTER = (WC[0] - KNUCKLE_ARM*math.cos(arm_ang), WC[1] - KNUCKLE_ARM*math.sin(arm_ang), WC[2] - 0.02)
def dist(a, b): return math.dist(a, b)
L0 = dist(INNER, OUTER)
print(f"\nTie-rod length at ROAD static: {L0*1000:.1f} mm (inner joint on the pivot axis at Y={INNER[1]:.2f})")
print("Carrier/arm angle sweep -> tie-rod length change (mm) with the inner joint ON the axis:")
for th in (TH_ROAD - 14, TH_ROAD, TH_HIGH, TH_LIFT, TH_RETRACT):
    O = rot_about_axis(OUTER, rad(th - TH_ROAD))   # rotating the arm rotates the outer joint about the axis
    print(f"  arm {th:6.1f} deg: length change {(dist(INNER, O)-L0)*1000:+.3f} mm -> steer change 0.00 deg")
# Compare with a conventional layout: inner joint 60 mm below and 40 mm behind the axis
INNER_OFF = (PIV[0]-0.04, 0.26, PIV[2]-0.06)
L1 = dist(INNER_OFF, OUTER)
print("\nSame sweep with the inner joint 40 mm behind / 60 mm below the axis (conventional rack position):")
for th in (TH_ROAD - 14, TH_ROAD, TH_HIGH, TH_LIFT):
    O = rot_about_axis(OUTER, rad(th - TH_ROAD))
    dl = dist(INNER_OFF, O) - L1
    print(f"  arm {th:6.1f} deg: length change {dl*1000:+.1f} mm -> approx steer change {math.degrees(dl/KNUCKLE_ARM):+.1f} deg")
print("\nConclusion: the on-axis inner joint is a hard geometric requirement, not a tuning choice.")
