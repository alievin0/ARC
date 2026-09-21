"""Ski and track sizing checks against the V0 mass (DERIVED)."""
import math
from params_v0 import *
from mass_budget_v0 import curb, KIT_SKI_PAIR, KIT_TRACK_PAIR

m_snow = curb() - 18 - 26 + KIT_SKI_PAIR + KIT_TRACK_PAIR + RIDER + CARGO
Wt = m_snow*G
F_FRONT = 0.40   # TARGET front load fraction in SNOW (rider slightly rearward)

# Ski (TARGET)
SKI_L, SKI_W = 1.10, 0.22
ski_area = 0.85*SKI_L*SKI_W        # effective bearing area (tapered ends)
p_ski = Wt*F_FRONT/2/ski_area
# Track (TARGET)
TRK_L, TRK_W = 1.10, 0.30          # ground contact length x width per cassette
PITCH = 0.0726                     # 2.86 in
TEETH = 13
LUG_H = 0.030
r_sprocket = PITCH*TEETH/(2*math.pi)
trk_area = TRK_L*TRK_W
p_trk = Wt*(1-F_FRONT)/2/trk_area

# Traction demand: 20 deg snow slope + rolling
grade = math.radians(20)
F_req = Wt*math.sin(grade) + 0.12*Wt*math.cos(grade)
T_hub = F_req/2*r_sprocket

print(f"SNOW operating mass {m_snow:.0f} kg -> {Wt:.0f} N")
print(f"Ski {SKI_L} x {SKI_W} m, effective area {ski_area:.3f} m^2: pressure {p_ski/1000:.1f} kPa per ski (snowmobile ~3-5 kPa BENCH-range; target <= 7 kPa -> TBD by test)")
print(f"Track {TRK_L} x {TRK_W} m per cassette ({trk_area:.2f} m^2): pressure {p_trk/1000:.1f} kPa (tracked ATV 3.8-6.2 kPa BENCH)")
print(f"Sprocket: {TEETH} teeth x {PITCH*1000:.1f} mm pitch -> radius {r_sprocket*1000:.0f} mm; lug height {LUG_H*1000:.0f} mm")
print(f"20 deg snow climb: tractive force {F_req/1000:.2f} kN total -> {F_req/2/1000:.2f} kN per track -> {T_hub:.0f} Nm at each rear hub")
for ratio, Tm in ((6, 35), (12, 35)):
    print(f"  motor {Tm} Nm peak x {ratio}:1 = {Tm*ratio} Nm at the hub -> {'OK' if Tm*ratio >= T_hub*1.2 else 'INSUFFICIENT'} (needs {T_hub*1.2:.0f} Nm with 20% margin)")
v = 45/3.6
w_spr = v/r_sprocket
print(f"45 km/h track speed: sprocket {w_spr*60/(2*math.pi):.0f} rpm -> motor {w_spr*60/(2*math.pi)*6:.0f} rpm in 6:1, {w_spr*60/(2*math.pi)*12:.0f} rpm in 12:1 (crawl range must be capped ~25-30 km/h)")
# Track tension (snowmobile practice: small force, large deflection)
print("Tension spec (TARGET, from snowmobile practice): 70 N mid-span load -> 25-35 mm deflection; indicator switch closes inside that window")
# Snow / ice loads on the ski adapter (TARGET)
print(f"Ski impact case: 3 g vertical + 2 g longitudinal on one ski = {3*Wt*F_FRONT/2/1000:.1f} kN vertical, {2*Wt*F_FRONT/2/1000:.1f} kN longitudinal at the ski tip")
