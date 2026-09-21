"""Displacement-mode resistance, power, speed, endurance (first-order, DERIVED).
Method: ITTC-57 friction on the wetted surface of tubes + tub + fender foam boxes,
a residuary (wave) component scaled with Froude number for slender tubes,
bluff-body drag on the four partly submerged tyres, and a pod propulsive
efficiency. This is a screening estimate; a tank test replaces it (Prototype 3)."""
import math
from params_amph import *
from mass_amph import table
from hydrostatics_amph import bodies, solve_waterline, circle_immersed, poly_area_centroid, clip_polygon, tub_polys, foam_polys

NU = 1.0e-6     # m^2/s kinematic viscosity (fresh water ~15 C)
ETA_D = 0.45    # TARGET overall propulsive efficiency of a small ducted prop at 1-2.5 m/s (unsourced; verify by test)
CD_TYRE = 0.8   # TARGET bluff-body coefficient for a partly submerged rotating-free tyre

def wetted_and_length(m):
    bs = bodies()
    z0, V, cb = solve_waterline(bs, m)
    S = 0.0
    # tubes: arc length below the waterline x length
    for cy, cz, r in ((TUBE_Y, TUBE_Z, TUBE_D/2), (-TUBE_Y, TUBE_Z, TUBE_D/2)):
        a = cz - z0
        if a < r:
            th = math.acos(max(-1, min(1, a/r)))
            S += 2*th*r*TUBE_L_EFF + 2*(r*r*(th - math.sin(th)*math.cos(th)))  # arc + two end caps
    # tub: bottom + two sides below the waterline
    L_tub = (TUB_X[1]-TUB_X[0])*TUB_CB
    depth = max(0.0, z0 - TUB_LOWER_Z[0])
    S += 2*TUB_LOWER_Y*L_tub + 2*depth*L_tub + 2*(2*TUB_LOWER_Y*depth)
    if z0 > TUB_UPPER_Z[0]:
        S += 2*(z0-TUB_UPPER_Z[0])*L_tub + 2*(2*(TUB_UPPER_Y-TUB_LOWER_Y))*L_tub
    return z0, S

def tyre_drag(v, z0, theta=TH_WATER):
    fz = PIV_Z - L_ARM*math.sin(math.radians(theta))
    sub = max(0.0, min(2*TYRE_R, z0 - (fz - TYRE_R)))      # submerged height of the tyre
    A = TYRE_W*sub
    return 4*0.5*RHO*v*v*A*CD_TYRE, sub

def resistance(v, m):
    z0, S = wetted_and_length(m)
    L = TUBE_L
    Re = max(v*L/NU, 1e5)
    Cf = 0.075/(math.log10(Re)-2)**2
    Rf = 0.5*RHO*v*v*S*Cf*1.15          # form factor 1.15
    Fn = v/math.sqrt(G*L)
    # residuary: slender tubes; steep rise approaching Fn ~0.45 (hull speed); coefficient TARGET
    Cr = 0.0015*(1 + (Fn/0.30)**4)
    Rr = 0.5*RHO*v*v*S*Cr
    Rt, sub = tyre_drag(v, z0)
    return Rf, Rr, Rt, Rf+Rr+Rt, z0, S, sub

if __name__ == "__main__":
    m = table()[3][1]   # operating
    z0, S = wetted_and_length(m)
    print(f"Operating mass {m:.0f} kg, waterline Z {z0:.3f}, wetted surface {S:.2f} m^2; tube length {TUBE_L} m -> hull speed 1.34*sqrt(L ft) = {1.34*math.sqrt(TUBE_L/0.3048):.1f} kn = {1.34*math.sqrt(TUBE_L/0.3048)*1.852:.1f} km/h")
    _, sub = tyre_drag(1.0, z0)
    print(f"Tyres at carrier {TH_WATER:.0f} deg: submerged {sub:.2f} m of {2*TYRE_R:.2f} m diameter; four tyres act as keels and as the main drag item")
    print()
    print(f"{'km/h':>5s} {'m/s':>5s} {'Fn':>5s} {'R_fric N':>9s} {'R_wave N':>9s} {'R_tyres N':>10s} {'R_total N':>10s} {'P_eff kW':>9s} {'P_shaft kW':>10s} {'P_batt kW':>9s} {'range km on 10 kWh':>18s}")
    for kmh in (3, 4, 5, 6, 7, 8, 9, 10):
        v = kmh/3.6
        Rf, Rr, Rt, R, z0, S, sub = resistance(v, m)
        Pe = R*v
        Ps = Pe/ETA_D
        Pb = Ps/0.90 + 300   # inverter/motor 90%, 300 W hotel (pumps, controller)
        rng = 10000/Pb*kmh
        Fn = v/math.sqrt(G*TUBE_L)
        print(f"{kmh:5d} {v:5.2f} {Fn:5.2f} {Rf:9.0f} {Rr:9.0f} {Rt:10.0f} {R:10.0f} {Pe/1000:9.2f} {Ps/1000:10.2f} {Pb/1000:9.2f} {rng:18.0f}")
    print()
    print(f"Pod sizing: {POD_P_KW:.0f} kW shaft (TARGET) -> continuous speed where P_shaft = {POD_P_KW:.0f} kW is read from the table; a 15 kW pod would add ~1.5 km/h at a steeply rising cost")
    # acceleration: thrust at low speed ~ (P/v) limited by bollard ~ 130 N/kW (TARGET)
    T_boll = 130*POD_P_KW
    print(f"Bollard thrust ~{T_boll:.0f} N (TARGET 130 N/kW) -> initial acceleration {T_boll/m:.2f} m/s^2; 0 to 5 km/h in ~{(5/3.6)/(T_boll/m - 0.5*resistance(0.7, m)[3]/m):.0f} s")
    # turning: vectored pod at the stern, lever ~1.9 m from the CG; turning radius ~1-1.5 boat lengths (TARGET, unverified)
    print("Turning: vectored stern thrust (+-35 deg) about a ~1.9 m lever; expected radius 1-1.5 tube lengths (3-4 m) at 5 km/h; TBD by test")
    print("Shallow water: floats in >= 0.55 m; below that the tyres touch and the vehicle drives on the bottom (HIGH: tyres reach the bottom at 0.7 m depth, LIFT at 0.8 m)")
