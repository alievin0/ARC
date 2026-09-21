"""Static Stability Factor by mode (Part 12). DERIVED from ASSUMPTIONS."""
from params import *
from mass_budget import road_curb_mass, REAR_TRACK_CASSETTES_KG

def ssf(track, h_cg):
    return track / (2.0 * h_cg)

if __name__ == "__main__":
    curb = road_curb_mass()
    # CG heights (ASSUMPTION): vehicle-only CG at 0.45 m road mode (battery low);
    # rider CG ~ seat height + 0.25 m
    h_veh = 0.45
    h_rider = SEAT_HEIGHT_M + 0.25
    def combined(h_veh_mode, extra_low_mass=0.0):
        m_v = curb + extra_low_mass
        return (m_v*h_veh_mode + RIDER_MASS_KG*(h_rider + (h_veh_mode-h_veh))) / (m_v + RIDER_MASS_KG)
    h_road = combined(h_veh)
    dh = GROUND_CLEARANCE_HIGH_M - GROUND_CLEARANCE_ROAD_M
    h_high = combined(h_veh + dh)
    h_track = combined(h_veh + 0.06, REAR_TRACK_CASSETTES_KG)  # tracks raise ~60 mm ASSUMPTION
    print(f"Combined CG height: road {h_road:.2f} m, robotic-high {h_high:.2f} m, track {h_track:.2f} m")
    print(f"SSF road   (track {TRACK_M:.2f} m): {ssf(TRACK_M, h_road):.2f}")
    print(f"SSF high   (track {TRACK_M:.2f} m): {ssf(TRACK_M, h_high):.2f}")
    print(f"SSF high, track widened by 0.15 m via arm geometry: {ssf(TRACK_M+0.15, h_high):.2f}")
    print(f"SSF track mode (track {TRACK_M+0.05:.2f} m): {ssf(TRACK_M+0.05, h_track):.2f}")
    print("For reference: NHTSA relates SSF < 1.05 to elevated rollover risk for passenger")
    print("vehicles; ATVs are rider-active vehicles and operate at SSF well below that")
    print("(see Part 12 and the CPSC/ANSI Kst discussion).")
