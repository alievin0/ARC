"""Bottom-up mass budget for RC-0.

Every line is an ASSUMPTION with a stated basis. The point of the exercise is
to show that the 80-150 kg total mass printed on the concept boards is not
achievable for a four-module transformable ATV, and to give the other scripts
a defensible gross mass.
"""
from params import *

# (item, kg, basis)
ITEMS = [
    ("Chassis: central welded space frame / tub, incl. hitch", 55.0,
     "ASSUMPTION: 4130 or 6082 space frame of ATV size is ~35-45 kg; +hitch tower and module hardpoints"),
    ("Battery pack, 12 kWh nominal, IP67 enclosure", 80.0,
     "DERIVED: energy.py sizes ~12 kWh; 150 Wh/kg pack-level (Part 11)"),
    ("Four traction motors + reduction (~8-10 kW cont each)", 48.0,
     "BENCHMARK-range: powersports-class liquid-cooled motors 8-14 kg + gearset"),
    ("Four inverters + HV junction box + DC-DC + charger", 22.0,
     "BENCHMARK-range: 15-25 kW inverters 3-5 kg each"),
    ("Four corner modules: arm, carrier, pivot, actuator, lock, sensors (x4 @ 16 kg)", 64.0,
     "ASSUMPTION: see Part 4; comparable to a heavy ATV A-arm set + actuator"),
    ("Four uprights/hubs/bearings/half-shafts (x4 @ 6 kg)", 24.0,
     "BENCHMARK-range: ATV hub + knuckle + CV shaft"),
    ("Four wheels + tyres (26x9-12 class, x4 @ 11 kg)", 44.0,
     "BENCHMARK-range: 12 in aluminium wheel ~4-5 kg + tyre ~6-7 kg"),
    ("Four spring/damper units (x4 @ 3.5 kg)", 14.0,
     "BENCHMARK-range: coil-over ATV shocks 3-4 kg"),
    ("Brakes (4 discs, calipers, master cyl, lines) + parking brake", 12.0,
     "BENCHMARK-range: ATV hydraulic disc brake set"),
    ("Steering (bars, column, EPS unit, rack/tie rods)", 10.0,
     "BENCHMARK-range: ATV EPS steering set"),
    ("Body panels, seat, fenders, footboards, lighting", 28.0,
     "ASSUMPTION: thermoformed/RIM panels ~20 kg + seat + lights"),
    ("Thermal system (pump, radiator, lines, coolant)", 8.0,
     "ASSUMPTION: liquid loop for motors, inverters and pack"),
    ("LV harness, controllers, sensors, HMI", 10.0,
     "ASSUMPTION"),
    ("Fasteners, misc, 5% contingency", 21.0,
     "ASSUMPTION: 5% of subtotal"),
]

def road_curb_mass():
    return sum(kg for _, kg, _ in ITEMS)

# Mode kits (ASSUMPTION; Part 8 and Part 9). These are what is carried in
# that mode, not what is stowed in the vehicle in road mode.
FRONT_SKI_PAIR_KG = 14.0        # two skis + spindle saddles + limiter straps
REAR_TRACK_CASSETTES_KG = 90.0  # two rear track cassettes (benchmark-range: ATV track kits are ~40-50 kg per corner)
MARINE_HULL_KIT_KG = 70.0       # sealed tub floor, bay doors, jet unit, bilge, flotation

if __name__ == "__main__":
    curb = road_curb_mass()
    print("RC-0 MASS BUDGET (road mode)")
    print("-" * 78)
    for name, kg, basis in ITEMS:
        print(f"{kg:6.1f} kg  {name}")
    print("-" * 78)
    print(f"{curb:6.1f} kg  CURB MASS, road mode (no rider)")
    print(f"{curb + PAYLOAD_KG:6.1f} kg  GROSS MASS, road mode (rider {RIDER_MASS_KG:.0f} kg + cargo {CARGO_MASS_KG:.0f} kg)")
    print()
    print("Mode variants (kit carried):")
    ski = curb - 2*11.0 + FRONT_SKI_PAIR_KG - 2*11.0 + REAR_TRACK_CASSETTES_KG
    print(f"{ski:6.1f} kg  curb, SKI/TRACK mode (front wheels off, skis on; rear wheels off, cassettes on)")
    mar = curb + MARINE_HULL_KIT_KG
    print(f"{mar:6.1f} kg  curb, MARINE variant (hull kit fitted, wheels retracted on board)")
    print(f"{mar + RIDER_MASS_KG:6.1f} kg  gross, MARINE variant with rider (no cargo)")
    print()
    print(f"Concept-board claim: 80-150 kg total. Bottom-up estimate is {curb/150:.1f}x the upper claim.")
