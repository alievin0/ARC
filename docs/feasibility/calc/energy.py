"""Power and energy estimates for RC-0 (Part 7, Part 11).

All DERIVED from ASSUMPTIONS in params.py. The battery size is an OUTPUT of
this script, not an input.
"""
import math
from params import *
from mass_budget import road_curb_mass, REAR_TRACK_CASSETTES_KG, FRONT_SKI_PAIR_KG, MARINE_HULL_KIT_KG

def road_power(v_kph, m, grade=0.0, c_rr=C_RR_GRAVEL):
    v = v_kph / 3.6
    f_rr = c_rr * m * G * math.cos(math.atan(grade))
    f_aero = 0.5 * AIR_DENSITY * CDA_M2 * v**2
    f_grade = m * G * math.sin(math.atan(grade))
    f = f_rr + f_aero + f_grade
    return f * v / DRIVE_EFFICIENCY  # W at battery

if __name__ == "__main__":
    curb = road_curb_mass()
    m_road = curb + PAYLOAD_KG
    print(f"ROAD MODE, gross {m_road:.0f} kg")
    for v in (20, 40, 60):
        for grade in (0.0, 0.10, 0.30):
            print(f"  {v:3d} km/h, grade {grade*100:3.0f}%: {road_power(v, m_road, grade)/1000:6.1f} kW battery")
    # Duty-cycle mix (ASSUMPTION): 20% at 20 km/h 10% grade, 50% at 40 km/h flat, 30% at 60 km/h flat
    p_avg = 0.2*road_power(20, m_road, 0.10) + 0.5*road_power(40, m_road) + 0.3*road_power(60, m_road)
    v_avg = 0.2*20 + 0.5*40 + 0.3*60
    wh_per_km = p_avg / v_avg
    print(f"  Duty-cycle mix: avg {p_avg/1000:.1f} kW at {v_avg:.0f} km/h -> {wh_per_km:.0f} Wh/km")
    for rng in (50, 60, 80):
        e_nom = rng * wh_per_km / USABLE_SOC_FRACTION / 1000
        print(f"  Range {rng} km -> nominal pack {e_nom:5.1f} kWh -> {e_nom*1000/PACK_ENERGY_DENSITY_WH_KG:5.0f} kg pack")
    # Peak power for 0-60 km/h in ~6 s on flat (ASSUMPTION for 'premium' feel)
    a = (60/3.6)/6.0
    f_acc = m_road * a + road_power(60, m_road)*DRIVE_EFFICIENCY/(60/3.6)
    print(f"  Peak wheel power for 0-60 km/h in 6 s: {f_acc*(60/3.6)/1000:.0f} kW at the wheels (end of run)")
    # Grade-limited traction at 100% torque split: mu = 0.6 (ASSUMPTION)
    print(f"  Traction-limited tractive force at mu=0.6: {0.6*m_road*G/1000:.1f} kN -> max grade ~{math.degrees(math.atan(0.6)):.0f} deg")
    print()
    m_snow = curb - 4*11.0 + FRONT_SKI_PAIR_KG + REAR_TRACK_CASSETTES_KG + PAYLOAD_KG
    print(f"SNOW MODE, gross {m_snow:.0f} kg, c_rr(track+snow) {C_RR_SNOW_TRACK}")
    for v in (15, 30, 45):
        print(f"  {v:3d} km/h flat: {road_power(v, m_snow, 0.0, C_RR_SNOW_TRACK)/1000:6.1f} kW battery")
    p_snow = road_power(30, m_snow, 0.0, C_RR_SNOW_TRACK)
    print(f"  Wh/km at 30 km/h: {p_snow/30:.0f} -> 12 kWh nominal gives ~{12000*USABLE_SOC_FRACTION/(p_snow/30):.0f} km")
    print()
    m_marine = curb + MARINE_HULL_KIT_KG + RIDER_MASS_KG
    print(f"MARINE, gross {m_marine:.0f} kg")
    # Displacement-speed drag: crude flat-plate + form; use effective drag D ~ 0.5*rho*v^2*S*Cd, Cd 0.25 on wetted area (ASSUMPTION)
    S_wet = 2.2   # m^2 ASSUMPTION
    for v_kn in (3, 5, 7):
        v = v_kn * 0.5144
        D = 0.5*WATER_DENSITY*v**2*S_wet*0.25
        P = D*v/0.35   # jet propulsive efficiency at low speed ~0.35 ASSUMPTION
        print(f"  {v_kn} kn displacement: drag ~{D:.0f} N, shaft+jet power ~{P/1000:.1f} kW")
    # Planing: power-to-weight benchmark: ~0.10-0.15 kW/kg for small PWC to plane and reach 60-70 km/h (see Part 9)
    for kwkg in (0.06, 0.10, 0.15):
        print(f"  Planing at {kwkg:.2f} kW/kg -> {kwkg*m_marine:.0f} kW")
    hull_speed_kn = 1.34 * math.sqrt(HULL_LENGTH_M / 0.3048)
    print(f"  Displacement hull speed for LWL {HULL_LENGTH_M} m: {hull_speed_kn:.1f} kn ({hull_speed_kn*1.852:.1f} km/h)")
