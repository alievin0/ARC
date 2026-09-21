"""Energy and hydrostatics at the V0 masses, reusing the feasibility-study models."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'feasibility', 'calc'))
import params as fp
from energy import road_power
from buoyancy import hydrostatics
from mass_budget_v0 import curb, KIT_SKI_PAIR, KIT_TRACK_PAIR, KIT_SWIM, VARIANT_MARINE_DELTA
from params_v0 import RIDER, CARGO, G

m_road = curb() + RIDER + CARGO
print(f"ROAD, {m_road:.0f} kg:")
p_avg = 0.2*road_power(20, m_road, 0.10) + 0.5*road_power(40, m_road) + 0.3*road_power(60, m_road)
wh_km = p_avg/42
print(f"  mixed duty cycle {wh_km:.0f} Wh/km -> 12 kWh nominal (85% usable) gives {12000*0.85/wh_km:.0f} km; 60 km needs {60*wh_km/0.85/1000:.1f} kWh")
print(f"  60 km/h flat {road_power(60, m_road)/1000:.1f} kW; 60 km/h 10% {road_power(60, m_road, 0.10)/1000:.1f} kW; 30% grade at 20 km/h {road_power(20, m_road, 0.30)/1000:.1f} kW")
a = (60/3.6)/6.0
print(f"  0-60 km/h in 6 s: {(m_road*a*(60/3.6) + road_power(60, m_road)*0.85)/1000:.0f} kW at the wheels at the end of the run")
m_snow = curb() - 44 + KIT_SKI_PAIR + KIT_TRACK_PAIR + RIDER + CARGO
p_snow = road_power(30, m_snow, 0.0, fp.C_RR_SNOW_TRACK)
print(f"SNOW, {m_snow:.0f} kg: {p_snow/30:.0f} Wh/km at 30 km/h -> 12 kWh gives {12000*0.85/(p_snow/30):.0f} km")
m_swim = curb() + KIT_SWIM + RIDER
m_var = curb() + VARIANT_MARINE_DELTA + RIDER
print(f"SWIM kit afloat, {m_swim:.0f} kg: displacement {m_swim/1000:.3f} m^3 required")
V_tyre = 4*2*math.pi**2*0.27*0.08**2
for d in (0.40, 0.45, 0.50):
    V_sp = 2*math.pi*(d/2)**2*1.6
    h = hydrostatics(fp.HULL_LENGTH_M, fp.HULL_BEAM_M, fp.HULL_DEPTH_M, fp.HULL_BLOCK_COEFF, m_swim, fp.WHEEL_BAY_VOLUME_M3 - V_sp - V_tyre, 0.78)
    h2 = hydrostatics(fp.HULL_LENGTH_M, fp.HULL_BEAM_M + 2*d, fp.HULL_DEPTH_M, fp.HULL_BLOCK_COEFF*0.8, m_swim, fp.WHEEL_BAY_VOLUME_M3 - V_sp - V_tyre, 0.78)
    print(f"  sponsons dia {d:.2f} m x 1.6 m: reserve buoyancy {h['reserve']*100:+.0f}%, GM {h2['GM']:+.2f} m")
print(f"ARC-2B M variant afloat, {m_var:.0f} kg: displacement {m_var/1000:.3f} m^3")
for L, B in ((2.6, 1.5), (2.8, 1.5), (2.8, 1.6)):
    h = hydrostatics(L, B, 0.55, 0.62, m_var, fp.WHEEL_BAY_VOLUME_M3, 0.80)
    print(f"  hull {L} x {B} m: draft {h['draft']:.2f} m, freeboard {h['freeboard']:.2f} m, reserve {h['reserve']*100:.0f}%, GM {h['GM']:+.2f} m")
print(f"  planing power at 0.10-0.15 kW/kg: {0.10*m_var:.0f}-{0.15*m_var:.0f} kW")
