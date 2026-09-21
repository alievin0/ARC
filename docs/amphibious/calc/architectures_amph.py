"""Parametric packaging/buoyancy screening of the candidate deployable architectures (DERIVED).
Needed buoyant volume: 0.694 m^3 at max + 30% reserve = 0.90 m^3 minimum total, of which the tub
supplies 0.60 m^3 only if the lower body is made watertight (all options assume that upgrade)."""
import math
from params_amph import *
from mass_amph import table
V_REQ = table()[4][1]/RHO
V_MIN_TOTAL = V_REQ*1.30
V_TUB = 0.604
V_DEPLOY_NEEDED = V_MIN_TOTAL - V_TUB
FENDER_CAVITY = 2*0.26*0.21*2.0       # m^3, both sides, above the arches
BODY_SIDE_BAND = 2*0.03*0.22*2.0      # a 30 mm thick skin over the fender band, both sides

def rigid_shell_mass(V, wall=0.006, rho=940):
    # rotomoulded PE box of volume V with aspect ~ 2.4 x 0.45 x (V/(2.4*0.45)); surface area estimate
    L, B = 2.4, 0.45
    H = V/(L*B)
    S = 2*(L*B + L*H + B*H)
    return S*wall*rho

rows = []
# A. Folding rigid side pontoons (2 x rotomoulded, hinged at the fender edge)
Vd = 2*0.24; m = 2*rigid_shell_mass(0.24) + 12   # hinges/locks
rows.append(("A  Folding rigid side pontoons (2 x 0.24 m^3)", Vd, Vd, m, "stowed volume equals deployed volume: 0.48 m^3 must live on the body; fender cavity holds %.2f m^3" % FENDER_CAVITY, "FAIL packaging"))
# B. Telescoping side bodies: 4 nested sections, stowed length 0.6 m
Vd = 2*(0.6*(math.pi*(0.25**2 + 0.22**2 + 0.19**2 + 0.16**2)))
Vs = 2*0.6*math.pi*0.25**2
rows.append(("B  Telescoping side bodies (4 nested sections/side)", Vs, Vd, 2*rigid_shell_mass(Vd/2, 0.005) + 16, "stowed 0.6 x D0.5 housing per side does not fit the 0.26 x 0.21 m fender band; 3 sliding seals per side under water", "FAIL packaging + sealing"))
# C. Fold-out catamaran hulls stowed over the fenders
Vd = 2*0.45; rows.append(("C  Fold-out rigid catamaran hulls (2 x 0.45 m^3)", Vd, Vd, 2*rigid_shell_mass(0.45) + 20, "stowed on top of the fenders: vehicle height 1.35 m, +0.12 m CG on land", "FAIL land impact"))
# D. Central tub + rigid amas on folding arms (small rigid outriggers)
Vd = 2*0.16; rows.append(("D  Central tub + rigid folding amas (2 x 0.16 m^3)", Vd, Vd, 2*rigid_shell_mass(0.16) + 14, "amas stowed vertically along the body sides add +0.36 m to the land width (1.24 -> 1.60 m); buoyancy marginal: tub + amas = %.2f m^3 vs %.2f needed" % (V_TUB+Vd, V_MIN_TOTAL), "MARGINAL buoyancy / FAIL land width"))
# E. Expandable monocoque: side panels fold down 0.3 m with a fabric skirt (prism 2.0 x 0.3 x 0.4)
Vd = 2*2.0*0.3*0.4; rows.append(("E  Expandable monocoque (folding sides + fabric skirt)", 0.02, Vd, 22, "hinged rigid sides + a flexible bottom skirt: open-bottom prism, sealing under load unproven; skirt must carry %.1f kN" % (Vd*RHO*G/2/1000), "FAIL sealing (research-grade)"))
# F. Sealed central hull + full wheel retraction (previous ARC-2B M variant)
rows.append(("F  Sealed 2.8 x 1.6 m planing hull, wheels to -50 deg (ARC-2B M)", 0.0, 1.43, 140, "a different body: 2.8 x 1.6 m, planing needs 73-109 kW and 20 kWh", "PASS as a separate variant, not integrated"))
# G. Docking module (removable hull)
rows.append(("G  Removable drive-in hull (3.2 x 1.8 m dock)", 0.0, 2.0, 0, "zero land impact; not carried on the vehicle; trailer item", "PASS, not integrated"))
# H. Selected: watertight tub + fold-down fender rails + inflatable tubes
Vd = 0.864 + 0.160
rows.append(("H  Watertight tub + fold-down rails + inflatable tubes + foam (A2)", 2*TUBE_STORED_VOL, Vd, 82, "stored 0.012 m^3 inside the fender cavities; deployed %.2f m^3; total %.2f m^3 (%.0f%% reserve)" % (Vd, V_TUB+Vd, ((V_TUB+Vd)/V_REQ-1)*100), "PASS"))
# I. Direct tubes on the body side (no rail), steering limited to +-5 deg afloat
rows.append(("I  Inflatable tubes directly on the fender edge (no rail)", 2*TUBE_STORED_VOL, 0.864 + 0.160, 68, "tube inner face at Y 0.62 conflicts with a steered tyre (Y 0.77 at 32 deg): needs a mechanical rack limiter and a torque-based pod steering afloat", "PASS with steering limiter (fallback)"))

print(f"Required displacement at max: {V_REQ:.3f} m^3; minimum buoyant volume with 30% reserve: {V_MIN_TOTAL:.3f} m^3; tub supplies {V_TUB:.3f} -> deployable/added volume needed >= {V_DEPLOY_NEEDED:.3f} m^3")
print(f"Space available on the land body for stowage: fender cavities {FENDER_CAVITY:.3f} m^3 (both sides); a 30 mm side-skin volume {BODY_SIDE_BAND:.3f} m^3")
print()
print(f"{'Architecture':70s} {'stowed m^3':>10s} {'deployed m^3':>12s} {'added kg':>8s}  verdict")
for n, vs, vd, m, note, v in rows:
    print(f"{n:70s} {vs:10.3f} {vd:12.3f} {m:8.0f}  {v}")
    print(f"{'':70s} note: {note}")
