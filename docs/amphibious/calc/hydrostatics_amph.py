"""Numerical hydrostatics for the tub + two-tube configuration (prismatic bodies).

Method: for a heel angle phi about X (positive = starboard/-Y side down), the
water surface in the body frame is z_w(y) = z0 - y*tan(phi). Each body's
immersed cross-section area and centroid are computed analytically (polygon
clipping for the tub, circular-segment formulas for the tubes), multiplied by
the body's effective length, and z0 is solved so that the displaced volume
equals mass/rho. The righting arm is GZ = -[(yB-yG) cos(phi) - (zB-zG) sin(phi)],
positive = righting for phi > 0. Equilibrium heel for asymmetric loads is the
root of GZ. Small-angle checks reproduce GM = KM - KG.
All numbers DERIVED from params_amph.py (TARGET geometry)."""
import math
from params_amph import *
from mass_amph import marine_hardware, table

# ---------- geometry primitives ----------
def clip_polygon(poly, phi, z0):
    """Keep the part of polygon (list of (y,z)) below the water line z = z0 - y tan(phi)."""
    t = math.tan(math.radians(phi))
    def inside(p): return p[1] <= z0 - p[0]*t
    def intersect(a, b):
        # line a->b with water line
        fa = a[1] - (z0 - a[0]*t); fb = b[1] - (z0 - b[0]*t)
        s = fa/(fa - fb)
        return (a[0] + s*(b[0]-a[0]), a[1] + s*(b[1]-a[1]))
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        ia, ib = inside(a), inside(b)
        if ia and ib: out.append(b)
        elif ia and not ib: out.append(intersect(a, b))
        elif not ia and ib: out.append(intersect(a, b)); out.append(b)
    return out

def poly_area_centroid(poly):
    if len(poly) < 3: return 0.0, (0.0, 0.0)
    A = 0.0; cy = 0.0; cz = 0.0
    n = len(poly)
    for i in range(n):
        y1, z1 = poly[i]; y2, z2 = poly[(i+1) % n]
        cr = y1*z2 - y2*z1
        A += cr; cy += (y1+y2)*cr; cz += (z1+z2)*cr
    A *= 0.5
    if abs(A) < 1e-12: return 0.0, (0.0, 0.0)
    return abs(A), (cy/(6*A), cz/(6*A))

def circle_immersed(cy, cz, r, phi, z0):
    """Immersed area and centroid of a circle below the water line."""
    p = math.radians(phi)
    n = (math.sin(p), math.cos(p))            # unit normal, air side
    a = (cy*n[0] + cz*n[1]) - z0*math.cos(p)  # signed distance of centre above the surface
    if a >= r: return 0.0, (cy, cz)
    if a <= -r: return math.pi*r*r, (cy, cz)
    th = math.acos(a/r)
    A = r*r*(th - math.sin(th)*math.cos(th))
    d = (4*r*math.sin(th)**3)/(3*(2*th - math.sin(2*th)))
    return A, (cy - n[0]*d, cz - n[1]*d)

# ---------- configuration ----------
def tub_polys():
    lo = [(-TUB_LOWER_Y, TUB_LOWER_Z[0]), (TUB_LOWER_Y, TUB_LOWER_Z[0]), (TUB_LOWER_Y, TUB_LOWER_Z[1]), (-TUB_LOWER_Y, TUB_LOWER_Z[1])]
    up = [(-TUB_UPPER_Y, TUB_UPPER_Z[0]), (TUB_UPPER_Y, TUB_UPPER_Z[0]), (TUB_UPPER_Y, TUB_UPPER_Z[1]), (-TUB_UPPER_Y, TUB_UPPER_Z[1])]
    return [lo, up]

def foam_polys():
    L = (FOAM_X[1]-FOAM_X[0])*FOAM_FILL
    left = [(FOAM_Y[0], FOAM_Z[0]), (FOAM_Y[1], FOAM_Z[0]), (FOAM_Y[1], FOAM_Z[1]), (FOAM_Y[0], FOAM_Z[1])]
    right = [(-y, z) for y, z in left][::-1]
    return [(left, L), (right, L)]

def bodies(tube_left=1.0, tube_right=1.0, tube_d=TUBE_D, tube_y=TUBE_Y, tube_z=TUBE_Z, foam=True, tub=True):
    """Returns a list of (kind, geom, length). tube_left/right scale the tube VOLUME (1 = full, 0 = absent)."""
    L_tub = (TUB_X[1]-TUB_X[0])*TUB_CB
    b = [("poly", p, L_tub) for p in tub_polys()] if tub else []
    if foam: b += [("poly", p, L) for p, L in foam_polys()]
    if tube_left > 0:  b.append(("circle", (+tube_y, tube_z, tube_d/2*math.sqrt(tube_left)), TUBE_L_EFF))
    if tube_right > 0: b.append(("circle", (-tube_y, tube_z, tube_d/2*math.sqrt(tube_right)), TUBE_L_EFF))
    return b

def displaced(bs, phi, z0):
    V = 0.0; my = 0.0; mz = 0.0
    for kind, g, L in bs:
        if kind == "poly":
            A, (cy, cz) = poly_area_centroid(clip_polygon(g, phi, z0))
        else:
            A, (cy, cz) = circle_immersed(g[0], g[1], g[2], phi, z0)
        V += A*L; my += A*L*cy; mz += A*L*cz
    if V <= 0: return 0.0, (0.0, 0.0)
    return V, (my/V, mz/V)

def solve_waterline(bs, mass, phi=0.0):
    Vreq = mass/RHO
    lo, hi = -0.5, 2.0
    for _ in range(80):
        mid = 0.5*(lo+hi)
        V, _ = displaced(bs, phi, mid)
        if V < Vreq: lo = mid
        else: hi = mid
    z0 = 0.5*(lo+hi)
    V, cb = displaced(bs, phi, z0)
    return z0, V, cb

def total_volume(bs):
    V = 0.0
    for kind, g, L in bs:
        if kind == "poly": V += poly_area_centroid(g)[0]*L
        else: V += math.pi*g[2]**2*L
    return V

def GZ(bs, mass, phi, yG, zG):
    z0, V, (yB, zB) = solve_waterline(bs, mass, phi)
    p = math.radians(phi)
    return -((yB - yG)*math.cos(p) - (zB - zG)*math.sin(p)), z0

def equilibrium_heel(bs, mass, yG, zG):
    """Find phi where GZ = 0 (bisection on [-60, 60] deg, assumes a single crossing)."""
    lo, hi = -60.0, 60.0
    glo = GZ(bs, mass, lo, yG, zG)[0]
    for _ in range(60):
        mid = 0.5*(lo+hi)
        g = GZ(bs, mass, mid, yG, zG)[0]
        if (g > 0) == (glo > 0): lo, glo = mid, g
        else: hi = mid
    return 0.5*(lo+hi)

def waterplane_inertia(bs, z0):
    """Transverse and longitudinal waterplane second moments at heel 0 (for GM_T check and GM_L)."""
    It = 0.0; Il = 0.0; Aw = 0.0
    for kind, g, L in bs:
        if kind == "poly":
            ys = [p[0] for p in g]; zs = [p[1] for p in g]
            if min(zs) < z0 < max(zs):
                b = max(ys) - min(ys)
                It += L*b**3/12; Il += b*L**3/12; Aw += b*L
        else:
            cy, cz, r = g
            if abs(z0 - cz) < r:
                half = math.sqrt(r*r - (z0-cz)**2); b = 2*half
                It += L*b**3/12 + b*L*cy**2; Il += b*L**3/12; Aw += b*L
    return It, Il, Aw

def cg_afloat(mass_condition):
    """Combined CG height afloat: land CG with rider 0.60 m; marine hardware ~0.55 m; tubes deployed at tube_z."""
    return 0.61  # TARGET; a full CG build-up is a DO NOT BUILD YET item

def report():
    print("CONFIGURATION: tub %.2f x %.2f/%.2f x (%.2f..%.2f) m, Cb %.2f; tubes D %.2f x %.2f m eff. at Y +-%.2f, Z %.2f"
          % (TUB_X[1]-TUB_X[0], 2*TUB_LOWER_Y, 2*TUB_UPPER_Y, TUB_LOWER_Z[0], TUB_UPPER_Z[1], TUB_CB, TUBE_D, TUBE_L_EFF, TUBE_Y, TUBE_Z))
    bs = bodies()
    Vtot = total_volume(bs)
    Vtub = total_volume(bodies(0, 0, foam=False))
    Vfoam = total_volume(bodies(0, 0, foam=True)) - Vtub
    print(f"Total buoyant volume: {Vtot:.3f} m^3 (tub {Vtub:.3f} + fender foam {Vfoam:.3f} + tubes {Vtot-Vtub-Vfoam:.3f})")
    print()
    print(f"{'Condition':62s} {'kg':>6s} {'V m^3':>7s} {'z_w':>6s} {'tub fb':>7s} {'reserve':>8s} {'KB':>5s} {'BM_T':>6s} {'GM_T':>6s} {'BM_L':>6s} {'GM_L':>6s}")
    for name, m in table():
        z0, V, (yB, zB) = solve_waterline(bs, m)
        It, Il, Aw = waterplane_inertia(bs, z0)
        KG = cg_afloat(m)
        BMt, BMl = It/V, Il/V
        print(f"{name:62s} {m:6.0f} {V:7.3f} {z0:6.3f} {TUB_RIM_Z-z0:7.3f} {(Vtot-V)/V*100:7.0f}% {zB:5.2f} {BMt:6.2f} {zB+BMt-KG:6.2f} {BMl:6.2f} {zB+BMl-KG:6.2f}")
    print("  (tub fb = freeboard from the water to the tub rim at Z %.2f; KG afloat %.2f m TARGET)" % (TUB_RIM_Z, cg_afloat(0)))
    print()
    m = table()[4][1]   # marine maximum
    KG = cg_afloat(m)
    z0, V, cb = solve_waterline(bs, m)
    print(f"RIGHTING CURVE at {m:.0f} kg (max), rider centred, KG {KG:.2f}:")
    for phi in (0, 2, 5, 10, 15, 20, 30, 40):
        gz, zw = GZ(bs, m, phi, 0.0, KG)
        print(f"  heel {phi:3d} deg: GZ {gz:+.3f} m, righting moment {m*G*gz/1000:+.2f} kNm")
    print()
    print("EQUILIBRIUM HEEL / TRIM for load cases (max mass):")
    cases = [
     ("rider centred", 0.0, 1, 1),
     ("rider 0.30 m to port (+Y)", 100*0.30/m, 1, 1),
     ("rider 0.30 m to starboard", -100*0.30/m, 1, 1),
     ("25 kg cargo 0.45 m to port + rider 0.2 m port", (25*0.45+100*0.2)/m, 1, 1),
     ("starboard tube at 50% volume (one chamber lost, partial)", 0.0, 1, 0.5),
     ("starboard tube at 33% lost (one of three chambers)", 0.0, 1, 0.667),
     ("starboard tube fully lost (0%) -- swamped-flotation case", 0.0, 1, 0.0),
     ("starboard tube lost + rider leaning 0.3 m to port (recovery posture)", 100*0.30/m, 1, 0.0),
    ]
    for name, yG, tl, tr in cases:
        b = bodies(tl, tr)
        phi = equilibrium_heel(b, m, yG, KG)
        z0, V, (yB, zB) = solve_waterline(b, m, phi)
        # freeboard at the low-side tub rim corner
        low_y = -TUB_UPPER_Y if phi > 0 else TUB_UPPER_Y
        fb_low = (TUB_RIM_Z - (z0 - low_y*math.tan(math.radians(phi)))) * math.cos(math.radians(phi))
        # freeboard at the low-side rail hinge (Y +-0.62, Z 0.62)
        ry = -RAIL_HINGE[0] if phi > 0 else RAIL_HINGE[0]
        fb_rail = (RAIL_HINGE[1] - (z0 - ry*math.tan(math.radians(phi)))) * math.cos(math.radians(phi))
        print(f"  {name:66s} heel {phi:+6.1f} deg; low-side tub-rim freeboard {fb_low:+.2f} m; low-side rail freeboard {fb_rail:+.2f} m")
    # swamped: cockpit tub flooded (its volume no longer counts), tubes + foam only, at max mass
    b_sw = bodies(1, 1, tub=False)
    z0s, Vs, cbs = solve_waterline(b_sw, m)
    print(f"  SWAMPED (tub flooded, both tubes + foam): waterline Z {z0s:.3f} (tub rim 0.85 -> {'still above water' if z0s < TUB_RIM_Z else 'rim submerged'}), buoyant volume available {total_volume(b_sw):.3f} m^3 vs {m/RHO:.3f} needed -> {'FLOATS' if total_volume(b_sw) > m/RHO else 'SINKS'}")
    b_sw1 = bodies(1, 0, tub=False)
    print(f"  SWAMPED + one tube lost: available {total_volume(b_sw1):.3f} m^3 vs {m/RHO:.3f} -> {'FLOATS' if total_volume(b_sw1) > m/RHO else 'SINKS (foam volume insufficient: see DO NOT BUILD YET)'}")
    # trim
    z0, V, cb = solve_waterline(bs, m)
    It, Il, Aw = waterplane_inertia(bs, z0)
    GMl = cb[1] + Il/V - KG
    for name, arm in (("rider 0.30 m forward", 0.30), ("rider 0.30 m aft", -0.30), ("25 kg cargo at the rack (-1.05 m)", -1.05*25/100)):
        M = 100*G*arm
        trim = math.degrees(math.atan(M/(m*G*GMl)))
        print(f"  trim, {name:40s}: {trim:+.2f} deg (GM_L {GMl:.2f} m)")
    print()
    print("WAVE CHECK (design category D, Hs 0.3 m): crest ~0.15-0.20 m above still water; tub-rim freeboard must exceed it.")
    z0, V, cb = solve_waterline(bs, m)
    print(f"  still-water tub-rim freeboard {TUB_RIM_Z - z0:.2f} m -> margin over a 0.20 m crest {TUB_RIM_Z - z0 - 0.20:+.2f} m; rail underside at Z {RAIL_HINGE[1]:.2f} is {RAIL_HINGE[1]-z0:+.2f} m above still water (splash zone)")
    return z0

if __name__ == "__main__":
    report()
