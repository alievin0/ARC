"""V0 mass budget with the categories requested in the master brief.
Every line is a TARGET/BENCH-range estimate; the total is DERIVED."""
from params_v0 import *

ITEMS = [
 ("Chassis (sills, tub floor, 4 pivot nodes, rider frame, hitch)", 58, "TARGET; 4130 frame ~30 kg + 6082 sills/nodes ~22 + hitch 6"),
 ("Body panels, fenders, covers, lighting",                        24, "TARGET; thermoformed ABS/TPO ~18 + lamps"),
 ("Wheels 4 x 12 in aluminium",                                    18, "BENCH-range 4-5 kg each"),
 ("Tyres 4 x 26x10-12",                                            26, "BENCH-range 6-7 kg each"),
 ("Suspension: 4 coil-overs (semi-active option)",                  14, "BENCH-range 3-4 kg each"),
 ("Corner modules: 4 x (carrier, arm, pivot cartridge, upright/hub, half-shaft)", 80, "TARGET 20 kg per corner"),
 ("Motors + 6:1 reduction (4), rear 2-speed (+2 x 2 kg)",           48, "BENCH-range 8-11 kg per motor incl. gearset"),
 ("Inverters (4) + HV junction box + DC-DC + on-board charger",     23, "BENCH-range"),
 ("Battery 12 kWh nominal incl. tray, cold plate, heater",           78, "DERIVED from energy at 150 Wh/kg pack level"),
 ("BMS + contactors + IMD + fuses + MSD",                            4, "BENCH: EV200 0.43 kg each, iso165C < 0.22 kg"),
 ("Brakes: 4 inboard discs/calipers, 2 master cylinders, lines, parking", 11, "BENCH-range"),
 ("Steering: bars, column, rack, EPS, tie rods",                    10, "BENCH-range"),
 ("Transformation actuators (4)",                                    18, "BENCH-range 4-5 kg each for 6-10 kN class"),
 ("Mechanical locks (4 pins, solenoids, sectors)",                    6, "TARGET"),
 ("Wiring / harness / connectors",                                   10, "TARGET"),
 ("Cooling: pump, radiator, fan, lines, coolant (dry)",               7, "TARGET"),
 ("Electronics: VCU, transformation controller, sensors, HMI",        5, "TARGET"),
 ("Seat, grips, footboards",                                          8, "TARGET"),
 ("Protection: skid plates, bumpers, arch liners, guards",            12, "TARGET"),
]
CONTINGENCY = 0.05
FLUIDS = 4.0   # coolant + brake fluid

KIT_SKI_PAIR = 16.0        # two 1.10 x 0.22 m skis + adapters
KIT_TRACK_PAIR = 92.0      # two rear cassettes at ~46 kg (BENCH ~44 kg per production track)
KIT_SWIM = 49.0            # sponsons 2x9, jet module 25, bilge/wiring 6
VARIANT_MARINE_DELTA = 140.0   # hull tub, flaps, seals, PWC jet+motor, +8 kWh; replaces tub floor

def dry():
    s = sum(kg for _, kg, _ in ITEMS)
    return s * (1 + CONTINGENCY)

def curb():
    return dry() + FLUIDS

if __name__ == "__main__":
    print("ARC-2B V0 MASS BUDGET")
    print("-"*90)
    for n, kg, b in ITEMS:
        print(f"{kg:6.1f} kg  {n:72s}")
    s = sum(kg for _, kg, _ in ITEMS)
    print("-"*90)
    print(f"{s:6.1f} kg  subtotal")
    print(f"{s*CONTINGENCY:6.1f} kg  contingency {CONTINGENCY*100:.0f}%")
    print(f"{dry():6.1f} kg  DRY MASS (road configuration, no fluids)")
    print(f"{curb():6.1f} kg  CURB MASS (dry + fluids)")
    print(f"{RIDER+CARGO:6.1f} kg  PAYLOAD (rider {RIDER:.0f} + cargo {CARGO:.0f})")
    print(f"{curb()+RIDER+CARGO:6.1f} kg  TOTAL OPERATING MASS, ROAD/ROBOTIC")
    snow = curb() - 18 - 26 + KIT_SKI_PAIR + KIT_TRACK_PAIR
    print(f"{snow:6.1f} kg  curb, SNOW (wheels+tyres off, skis+cassettes on)")
    print(f"{snow+RIDER+CARGO:6.1f} kg  TOTAL OPERATING MASS, SNOW")
    print(f"{curb()+KIT_SWIM:6.1f} kg  curb, base vehicle with SWIM kit")
    print(f"{curb()+KIT_SWIM+RIDER:6.1f} kg  operating, SWIM with rider")
    print(f"{curb()+VARIANT_MARINE_DELTA:6.1f} kg  curb, ARC-2B M variant")
    print(f"{curb()+VARIANT_MARINE_DELTA+RIDER:6.1f} kg  operating, ARC-2B M with rider")
    W = (curb()+RIDER+CARGO)*G/4
    print(f"\nStatic corner load (road, even split): {W:.0f} N")
    print("Concept-board claim 80-150 kg: not achievable; the budget is 3x the upper claim.")
