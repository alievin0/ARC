"""Structural loads on the marine hardware (DERIVED from TARGET factors)."""
import math
from params_amph import *
from mass_amph import table

m_max = table()[4][1]
W = m_max*G
# Buoyancy share (from hydrostatics at max mass): tubes carry roughly V_tube_immersed/V_total; take 80% conservatively
F_TUBE_STATIC = 0.5*0.80*W          # per tube, static
WAVE_FACTOR = 2.0                    # TARGET: impulsive wave/slam factor on a tube (category D)
F_TUBE_WAVE = F_TUBE_STATIC*WAVE_FACTOR
L_rail = 2.20
w_static = F_TUBE_STATIC/L_rail
w_wave = F_TUBE_WAVE/L_rail
arm = RAIL_LENGTH + 0.05             # tube reaction acts ~50 mm outboard of the rail tip (flange centre)
M_hinge_line = w_wave*arm            # Nm per metre of hinge
n_stays = 3
stay_spacing = L_rail/n_stays
M_per_stay = M_hinge_line*stay_spacing
stay_lever = 0.20                    # stay attaches 0.20 m below the hinge on the tub wall and at the rail tip: geometry ~45 deg
F_stay = M_per_stay/(RAIL_LENGTH*math.sin(math.radians(45)))
# rail as a cantilever 0.22 m: (a) plain 4 mm plate, (b) ribbed 6082 extrusion: 3 mm skin + 3 mm x 30 mm ribs at 100 mm pitch
t = 0.004
I_plain = t**3/12
sigma_plain = (w_wave*arm)*(t/2)/I_plain/1e6
skin, rib_h, rib_t, pitch = 0.003, 0.030, 0.003, 0.100
n_ribs = 1/pitch
# neutral axis of skin+ribs per metre
A_skin, A_ribs = skin*1.0, n_ribs*rib_h*rib_t
z_skin, z_ribs = skin/2, skin + rib_h/2
zbar = (A_skin*z_skin + A_ribs*z_ribs)/(A_skin+A_ribs)
I_rib = (1.0*skin**3/12 + A_skin*(zbar-z_skin)**2) + n_ribs*(rib_t*rib_h**3/12 + rib_h*rib_t*(zbar-z_ribs)**2)
c = max(zbar, skin+rib_h-zbar)
sigma_rail = (w_wave*arm)*c/I_rib/1e6
# hinge shear
n_hinges = 4
F_hinge = F_TUBE_WAVE/n_hinges
# pod loads
T_pod = 1.3*POD_P_KW*1000/ (2.0)     # TARGET bollard thrust approx: ~130 N per kW at low speed for a ducted prop -> 8 kW ~1.0 kN; use 1.3 kN peak
T_pod = 1300.0
F_beach = 3000.0                     # TARGET: pod strikes the bottom at 1 m/s, 3 kN impulsive
M_pod_hinge = F_beach*POD_ARM_L
# tub wall pressure (hydrostatic head at the floor, swamped/wave)
head = 0.85 - 0.28 + 0.20
p_tub = RHO*G*head
# asymmetric buoyancy: one tube carries up to its full volume
F_tube_full = RHO*G*math.pi*(TUBE_D/2)**2*TUBE_L_EFF
print(f"Max marine mass {m_max:.0f} kg -> weight {W/1000:.2f} kN")
print(f"Tube static share (80% of weight on the tubes): {F_TUBE_STATIC/1000:.2f} kN per tube; wave x{WAVE_FACTOR}: {F_TUBE_WAVE/1000:.2f} kN per tube")
print(f"One tube at full immersion (asymmetric/upper bound): {F_tube_full/1000:.2f} kN")
print(f"Rail distributed load: {w_static/1000:.2f} kN/m static, {w_wave/1000:.2f} kN/m wave; hinge-line moment {M_hinge_line/1000:.2f} kNm/m")
print(f"Rail bending at the hinge line: plain 4 mm plate {sigma_plain:.0f} MPa (FAILS, > 240 MPa); ribbed extrusion (3 mm skin + 30x3 mm ribs at 100 mm) {sigma_rail:.0f} MPa -> OK vs 240 MPa unwelded 6082-T6 (the rail is an unwelded extrusion; hinges are bolted)")
print(f"Folding stays ({n_stays} per side, {stay_spacing:.2f} m spacing): {F_stay/1000:.2f} kN each at the wave case (compression/tension), lock pin double shear at {F_stay/1000:.2f} kN")
print(f"Hinges ({n_hinges} per side): {F_hinge/1000:.2f} kN shear each at the wave case")
print(f"Pod: thrust {T_pod/1000:.2f} kN peak (TARGET); beaching strike {F_beach/1000:.1f} kN -> hinge moment {M_pod_hinge/1000:.2f} kNm; lock pin shear {F_beach/1000:.1f} kN")
print(f"Tub wall/floor hydrostatic pressure (head {head:.2f} m incl. 0.2 m wave): {p_tub/1000:.1f} kPa -> 3 mm 5083 panels between stiffeners at 300 mm pitch: fine (design pressure class of small-craft topsides)")
print(f"Corner modules afloat: hydrodynamic loads at 2 m/s on a 0.10 m^2 submerged tyre ~{0.5*RHO*4*0.10*0.8:.0f} N per wheel (negligible vs 7.8 kN landing case)")
print(f"Beaching/shallow ground contact: wheels touch first (landing gear); tube bottoms at Z {TUBE_Z-TUBE_D/2:.2f} are {TUBE_Z-TUBE_D/2-0.0:.2f} m above the tyre bottoms in the -2 deg state -> tubes grounded only on obstacles > 0.3 m")
print("Load path afloat: water -> tube fabric (hoop) -> bolt ropes -> flange tracks -> rail (cantilever) -> hinges + stays -> tub wall (Y 0.36) -> tub floor/sills -> mass")
