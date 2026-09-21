"""Mass model for the integrated amphibious ARC-2B (Architecture A2)."""
from params_amph import *

MARINE_HARDWARE = [
 ("Watertight tub upgrade: inner arch walls to Z 0.85, sealed seams, 2 bulkheads, drain valves, cartridge bore seals", 15.0, "TARGET"),
 ("Fender-band rails (2 x 2.2 m 6082 L-extrusion) replacing the thermoformed side panel, hinges, 6 folding stays with lock pins", 14.0, "TARGET (net of the removed panel)"),
 ("Inflatable tubes (2 x D0.50 x 2.4 m, 3 chambers, 1100 dtex PU/PVC fabric, bolt ropes, valves)", 12.0, "TARGET; fabric ~1.2 kg/m^2 (unsourced, verify)"),
 ("Inflation: 12 V high-volume blower + top-off compressor + hoses + pressure sensors", 5.0, "TARGET"),
 ("Stern pod: 8 kW motor, duct, propeller, steering actuator, arm, hinge, lock pin, cable", 22.0, "TARGET"),
 ("Bilge: 2 pumps, float switches, high-water alarm, wiring", 5.0, "BENCH ~2 kg per 1100 GPH pump"),
 ("Corner-module immersion upgrade: IP68 carrier housings, vents, extra seals, anodes", 6.0, "TARGET"),
 ("Safety: kill cord, seat switch, emergency CO2 inflator, throwable flotation stowage", 3.0, "TARGET"),
]

def marine_hardware():
    return sum(m for _, m, _ in MARINE_HARDWARE)

def table():
    hw = marine_hardware()
    rows = [
     ("Land vehicle, curb (no marine hardware)", CURB_LAND),
     ("Land vehicle + rider", CURB_LAND + RIDER),
     ("Marine dry mass (curb + marine hardware)", CURB_LAND + hw),
     ("Marine operating mass (+ rider)", CURB_LAND + hw + RIDER),
     ("Marine maximum (+ rider + 25 kg cargo)", CURB_LAND + hw + RIDER + CARGO_WATER),
     ("Marine maximum + 5% water absorption/splash allowance", (CURB_LAND + hw + RIDER + CARGO_WATER)*1.05),
    ]
    return rows

if __name__ == "__main__":
    print("MARINE HARDWARE (Architecture A2)")
    for n, m, b in MARINE_HARDWARE:
        print(f"  {m:5.1f} kg  {n}  [{b}]")
    print(f"  {marine_hardware():5.1f} kg  TOTAL added to the land vehicle ({marine_hardware()/CURB_LAND*100:.1f}% of curb)")
    print()
    print(f"{'Condition':62s} {'Mass kg':>8s} {'Displacement m^3':>17s}")
    for n, m in table():
        print(f"{n:62s} {m:8.1f} {m/RHO:17.3f}")
