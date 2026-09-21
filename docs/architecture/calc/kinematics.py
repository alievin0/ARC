"""Corner-module kinematics, packaging envelopes and side-view geometry (V0).

Front arm LEADING (pivot behind the wheel), rear arm TRAILING (pivot ahead).
Body frame: origin on the ground at the wheelbase midpoint in ROAD static.
All outputs DERIVED from params_v0.py.
"""
import math
from params_v0 import *
from mass_budget_v0 import curb

def rad(d): return math.radians(d)

# Pivot positions (body frame), from the ROAD static wheel-centre positions
PIV_Z = WHEEL_R + L_ARM*math.sin(rad(TH_ROAD))          # 0.434
PIV_X_F = +WHEELBASE/2 - L_ARM*math.cos(rad(TH_ROAD))    # front pivot BEHIND the front wheel
PIV_X_R = -WHEELBASE/2 + L_ARM*math.cos(rad(TH_ROAD))    # rear pivot AHEAD of the rear wheel

def wheel_centre(theta_deg, front=True):
    """Wheel centre in the body frame for arm angle theta (deg, + = below horizontal)."""
    dx = L_ARM*math.cos(rad(theta_deg))
    dz = -L_ARM*math.sin(rad(theta_deg))
    if front:
        return (PIV_X_F + dx, PIV_Z + dz)
    return (PIV_X_R - dx, PIV_Z + dz)

def travel_angle(dz):  # arm angle change for a wheel-centre vertical move dz (small-angle exact via asin)
    return math.degrees(math.asin(dz/L_ARM))

STATES = {
 "ROAD static":        TH_ROAD,
 "ROAD full bump":     TH_ROAD - travel_angle(BUMP),
 "ROAD full droop":    TH_ROAD + travel_angle(DROOP),
 "HIGH static":        TH_HIGH,
 "HIGH full bump":     TH_HIGH - travel_angle(BUMP),
 "LIFT (max)":         TH_LIFT,
 "RETRACT (variant)":  TH_RETRACT,
}

def report():
    m = curb() + RIDER + CARGO
    W = m*G/4
    print(f"Pivot axes (body frame): front X={PIV_X_F:+.3f} m, rear X={PIV_X_R:+.3f} m, Z={PIV_Z:.3f} m, arm plane Y=+-{ARM_PLANE_Y:.2f} m")
    print(f"Pivot separation along X: {PIV_X_F-PIV_X_R:.3f} m (both pivots under the rider, inside the wheelbase)")
    print()
    print(f"{'state':20s} {'arm deg':>8s} {'F wheel X':>10s} {'F wheel Z':>10s} {'R wheel X':>10s} {'wheelbase':>10s} {'body rise':>10s} {'tyre top Z':>11s}")
    for name, th in STATES.items():
        fx, fz = wheel_centre(th, True)
        rx, rz = wheel_centre(th, False)
        wb = fx - rx
        rise = WHEEL_R - fz          # body rise above ROAD static (positive = body higher above the wheel)
        print(f"{name:20s} {th:8.1f} {fx:10.3f} {fz:10.3f} {rx:10.3f} {wb:10.3f} {rise:10.3f} {fz+WHEEL_R:11.3f}")
    print()
    # Envelope requirements
    fx_b, fz_b = wheel_centre(TH_ROAD - travel_angle(BUMP), True)
    fx_h, fz_h = wheel_centre(TH_HIGH - travel_angle(BUMP), True)
    print("FRONT TYRE ENVELOPE (body frame, Y from %.3f to %.3f m):" % (TRACK_F/2 - TYRE_W/2, TRACK_F/2 + TYRE_W/2))
    print(f"  ROAD full bump : X {fx_b-WHEEL_R:+.3f}..{fx_b+WHEEL_R:+.3f}, top Z {fz_b+WHEEL_R:.3f}  -> fender inner skin >= {fz_b+WHEEL_R+0.05:.2f} m")
    print(f"  HIGH full bump : X {fx_h-WHEEL_R:+.3f}..{fx_h+WHEEL_R:+.3f}, top Z {fz_h+WHEEL_R:.3f}  -> footboard leading edge must be behind X {fx_h-WHEEL_R-0.05:+.3f}")
    fx_d, fz_d = wheel_centre(TH_ROAD + travel_angle(DROOP), True)
    print(f"  ROAD full droop: X {fx_d-WHEEL_R:+.3f}..{fx_d+WHEEL_R:+.3f} (nose must extend to X >= {fx_d+WHEEL_R+0.05:+.3f} for a bumper ahead of the tyre)")
    fx_r, fz_r = wheel_centre(TH_RETRACT, True)
    print(f"  RETRACT (variant): centre X {fx_r:+.3f}, Z {fz_r:.3f}; tyre bottom Z {fz_r-WHEEL_R:.3f}, top Z {fz_r+WHEEL_R:.3f}; tyre inner face Y {TRACK_F/2-TYRE_W/2:.3f} (footboard outer edge Y {FOOTBOARD_Y[1]:.2f})")
    print(f"  Footboard box X {FOOTBOARD_X}, Z {FOOTBOARD_Z}: Y ranges do not overlap the tyre (tyre inner face {TRACK_F/2-TYRE_W/2:.3f} > footboard {FOOTBOARD_Y[1]:.2f}), so only the fender/side panel must clear the sweep.")
    print()
    # Actuator
    sweep = TH_LIFT - TH_ROAD
    stroke = 2*ACT_LEVER*math.sin(rad(sweep/2))
    T_road = W*L_ARM*math.cos(rad(TH_ROAD))*1.3
    r_eff = ACT_LEVER*math.cos(rad(ACT_ANGLE_OFFSET_MAX))
    print(f"ACTUATOR (base vehicle, {TH_ROAD:.0f}->{TH_LIFT:.0f} deg = {sweep:.0f} deg sweep on a {ACT_LEVER*1000:.0f} mm lever)")
    print(f"  stroke {stroke*1000:.0f} mm; carrier torque to lift a loaded corner at road angle {T_road:.0f} Nm (W={W:.0f} N x {L_ARM*math.cos(rad(TH_ROAD)):.3f} m x 1.3)")
    print(f"  worst-case actuator force {T_road/r_eff/1000:.1f} kN (lever effective radius {r_eff*1000:.0f} mm at {ACT_ANGLE_OFFSET_MAX:.0f} deg off-perpendicular)")
    print(f"  ROAD->HIGH ({TH_HIGH-TH_ROAD:.0f} deg): stroke {2*ACT_LEVER*math.sin(rad((TH_HIGH-TH_ROAD)/2))*1000:.0f} mm; at 12 mm/s -> {2*ACT_LEVER*math.sin(rad((TH_HIGH-TH_ROAD)/2))/0.012:.1f} s")
    print(f"  lock loads: 3 g bump {W*L_ARM*math.cos(rad(TH_ROAD))*LF_BUMP:.0f} Nm, 5 g landing {W*L_ARM*math.cos(rad(TH_ROAD))*LF_LANDING:.0f} Nm -> pin shear on a 150 mm sector {W*L_ARM*math.cos(rad(TH_ROAD))*LF_LANDING/0.15/1000:.1f} kN")
    marine_sweep = TH_LIFT - TH_RETRACT
    print(f"  MARINE variant sweep {marine_sweep:.0f} deg: exceeds a single linear-actuator lever; needs a two-stage crank or a rotary sector drive (unloaded wheel: ~{0.25*T_road/1.3/r_eff/1000:.1f} kN equivalent)")
    print()
    # Side-view geometry: anti-dive / anti-squat. IC = pivot for a single arm.
    h_cg = 0.60   # TARGET combined CG height with rider, road (see dynamics)
    # front: contact patch at (fx, 0); pivot at (PIV_X_F, PIV_Z); pivot is behind and above -> anti-dive for a leading arm
    fx, fz = wheel_centre(TH_ROAD, True)
    tan_phi_patch = PIV_Z/(fx - PIV_X_F)
    tan_phi_wc = (PIV_Z - fz)/(fx - PIV_X_F)
    ad_outboard = tan_phi_patch*BRAKE_FRONT_FRACTION/(h_cg/WHEELBASE)*100
    ad_inboard = tan_phi_wc*BRAKE_FRONT_FRACTION/(h_cg/WHEELBASE)*100
    rx, rz = wheel_centre(TH_ROAD, False)
    tan_phi_r_wc = (PIV_Z - rz)/(PIV_X_R - rx)
    asq = tan_phi_r_wc*DRIVE_REAR_FRACTION/(h_cg/WHEELBASE)*100
    print("SIDE-VIEW GEOMETRY (Milliken convention; IC = arm pivot; h_cg %.2f m TARGET)" % h_cg)
    print(f"  front LEADING arm, anti-dive with OUTBOARD (hub) brakes: {ad_outboard:.0f}%  <- excessive (nose rises under braking)")
    print(f"  front LEADING arm, anti-dive with INBOARD (carrier) brakes: {ad_inboard:.0f}%  <- selected")
    print(f"  rear TRAILING arm, anti-squat with carrier-mounted motor (torque reacted on carrier): {asq:.0f}%")
    print(f"  a front TRAILING arm would give PRO-dive of the same magnitude ({-ad_outboard:.0f}% with hub brakes): rejected")
    print("  roll centre: at ground level (transverse pivot axes); camber change = body roll; no camber gain")
    print()
    # Pitch-over and stability by mode
    for name, th, hc in (("ROAD", TH_ROAD, h_cg), ("HIGH", TH_HIGH, h_cg + 0.20*(1.0)), ("LIFT", TH_LIFT, h_cg+0.25)):
        fx, _ = wheel_centre(th, True); rx, _ = wheel_centre(th, False)
        wb = fx - rx
        print(f"  {name:5s}: wheelbase {wb:.2f} m, CG {hc:.2f} m -> static pitch-over {math.degrees(math.atan((wb/2)/hc)):.0f} deg, SSF {TRACK_F/(2*hc):.2f}")

if __name__ == "__main__":
    report()
