"""Hydrostatics for the marine question (Part 9).

Can the ATV-sized envelope float the vehicle with wheels retracted into
bays? And if not, how large must a hull be? All DERIVED from ASSUMPTIONS in
params.py. This is first-order hydrostatics (block coefficient, waterplane
inertia); it is a screening tool, not a stability booklet.
"""
import math
from params import *
from mass_budget import road_curb_mass, MARINE_HULL_KIT_KG

def hydrostatics(L, B, D, Cb, m, bays_m3, KG, Cwp=0.85):
    V_req = m / WATER_DENSITY
    A_plan = L * B
    V_full = A_plan * D * Cb - bays_m3
    draft = V_req / (A_plan * Cb)            # ignores bays (optimistic)
    freeboard = D - draft
    reserve = (V_full - V_req) / V_req
    KB = 0.55 * draft
    I = L * B**3 / 12 * Cwp
    BM = I / V_req
    GM = KB + BM - KG
    return dict(V_req=V_req, V_full=V_full, draft=draft, freeboard=freeboard,
                reserve=reserve, KB=KB, BM=BM, GM=GM)

if __name__ == "__main__":
    curb = road_curb_mass()
    m = curb + MARINE_HULL_KIT_KG + RIDER_MASS_KG
    KG = 0.75   # ASSUMPTION combined CG above keel with rider seated, wheels up
    print(f"Marine gross mass {m:.0f} kg (curb {curb:.0f} + hull kit {MARINE_HULL_KIT_KG:.0f} + rider {RIDER_MASS_KG:.0f})")
    print()
    print("CASE 1 - ATV envelope tub with four wheel bays cut out (the concept as drawn)")
    h = hydrostatics(HULL_LENGTH_M, HULL_BEAM_M, HULL_DEPTH_M, HULL_BLOCK_COEFF, m, WHEEL_BAY_VOLUME_M3, KG)
    print(f"  tub {HULL_LENGTH_M} x {HULL_BEAM_M} x {HULL_DEPTH_M} m, Cb {HULL_BLOCK_COEFF}, bays {WHEEL_BAY_VOLUME_M3:.3f} m^3")
    print(f"  displaced volume required     {h['V_req']:.3f} m^3")
    print(f"  watertight volume available   {h['V_full']:.3f} m^3   -> reserve buoyancy {h['reserve']*100:+.0f}%")
    print(f"  draft if bays ignored         {h['draft']:.2f} m of {HULL_DEPTH_M} m -> freeboard {h['freeboard']:+.2f} m")
    print(f"  GM estimate                   {h['GM']:+.2f} m (KB {h['KB']:.2f} + BM {h['BM']:.2f} - KG {KG:.2f})")
    verdict = "DOES NOT FLOAT" if h['reserve'] < 0 else ("floats with negative GM (capsizes)" if h['GM'] < 0 else "floats")
    print(f"  VERDICT: {verdict}")
    print()
    print("CASE 2 - what hull would work? Sweep length/beam for >=30% reserve, freeboard >=0.25 m, GM >= +0.25 m")
    print("  (bays kept at the same volume; depth 0.55 m; Cb 0.62)")
    found = []
    for L in (2.2, 2.4, 2.6, 2.8, 3.0, 3.2):
        for B in (1.2, 1.3, 1.4, 1.5, 1.6):
            h = hydrostatics(L, B, 0.55, 0.62, m, WHEEL_BAY_VOLUME_M3, KG)
            ok = h['reserve'] >= 0.30 and h['freeboard'] >= 0.25 and h['GM'] >= 0.25
            if ok:
                found.append((L, B, h))
    for L, B, h in found[:8]:
        print(f"  L {L:.1f} m  B {B:.1f} m : draft {h['draft']:.2f} m, freeboard {h['freeboard']:.2f} m, reserve {h['reserve']*100:.0f}%, GM {h['GM']:+.2f} m")
    if found:
        L, B, _ = found[0]
        print(f"  Smallest passing hull in the sweep: {L:.1f} x {B:.1f} m, i.e. ~{(L*B)/(HULL_LENGTH_M*HULL_BEAM_M):.1f}x the plan area of the ATV tub.")
    print()
    print("CASE 3 - displacement 'swim' mode with deployable sponsons (Part 17 proposal)")
    # Free-flooding bays with the tyre inside: the tyre's air volume displaces water.
    # Tyre torus: major radius ~0.27 m, minor radius ~0.08 m (ASSUMPTION, 26 in tyre)
    V_tyre = 4 * 2 * math.pi**2 * 0.27 * 0.08**2
    print(f"  four retracted tyres in flooded bays add {V_tyre:.3f} m^3 of displacement")
    for d_sp in (0.30, 0.40, 0.50):
        V_sp = 2 * math.pi * (d_sp/2)**2 * 1.6   # two sponsons 1.6 m long along the sills
        h = hydrostatics(HULL_LENGTH_M, HULL_BEAM_M, HULL_DEPTH_M, HULL_BLOCK_COEFF, m,
                         WHEEL_BAY_VOLUME_M3 - V_sp - V_tyre, KG)
        h2 = hydrostatics(HULL_LENGTH_M, HULL_BEAM_M + 2*d_sp, HULL_DEPTH_M, HULL_BLOCK_COEFF*0.8, m,
                          WHEEL_BAY_VOLUME_M3 - V_sp - V_tyre, KG)
        print(f"  sponson dia {d_sp:.2f} m: volume {V_sp:.3f} m^3 -> reserve {h['reserve']*100:+.0f}%, GM (widened waterplane) {h2['GM']:+.2f} m")
    print("  Sponsons of ~0.5 m diameter rescue buoyancy and stability at rest, but the")
    print("  vehicle is then 2.2 m wide afloat and cannot plane; this is a displacement")
    print("  'water-crossing' capability at ~3 kn, not a marine sport mode.")
