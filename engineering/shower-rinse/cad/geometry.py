"""
Single source of truth for the rail cross-section (mm).
Coordinates: x = horizontal, perpendicular to the glass (x>0 = shower interior, glass inner face at x=0)
             z = vertical (glass top edge at z=0).
Extrusion direction (rail length) = y.
Baseline: 8 mm tempered glass. Other thicknesses: change wedge-gasket thickness only.
"""
import math

T_GLASS = 8.0

# Aluminium body (open profile, 6063-T6). CCW polygon.
# v0.4: tube moved 2 mm toward the glass (hole exit 1.5 mm from the glass), glass-contact land thinned to
# 1.0 mm and ending 3 mm below the glass edge so it clears the tube; ribs and right wall shifted -2 mm.
BODY = [(-14, -18), (-11.3, -18), (-11.3, -16.8), (-12, -16.8), (-12, 2),
        (0.5, 2), (0.5, -3), (1.5, -3), (1.5, 2),
        (3.5, 2), (3.5, -0.95), (4.5, -0.95), (4.5, 2),
        (8.5, 2), (8.5, -0.95), (9.5, -0.95), (9.5, 2),
        (14, 2), (14, -10.5), (16, -10.5), (16, -9), (15.4, -9), (15.4, -7.5), (16, -7.5),
        (16, 3), (15, 4), (-13, 4), (-14, 3)]

# Snap-on cover / slot fin (extruded aluminium). The cradle hugs the tube from 200 to 270 deg; its top slopes
# down toward the glass so any start/stop drip or splash drains into the slot (no stagnant pocket).
# Slot 1.0 mm; knife tip 0.3 mm protruding 1 mm below the floor, plus a drip groove in the floor underside
# (geometric drip break, no coating needed).
_R = 5.05
_TC = (6.5, -5.5)
_ARC = [(round(_TC[0] + _R * math.cos(math.radians(a)), 3), round(_TC[1] + _R * math.sin(math.radians(a)), 3))
        for a in range(270, 199, -10)]
COVER = ([(1.0, -13.5), (1.3, -13.5), (2.2, -12.5), (3.0, -12.5), (3.0, -11.7), (3.8, -11.7), (3.8, -12.5),
          (17.6, -12.5), (17.6, -6), (16.1, -6), (16.1, -7.7), (15.5, -8.0), (15.5, -8.8), (16.1, -8.8),
          (16.1, -10.55)] + _ARC + [(1.0, -7.6)])

# Manifold tube (v0.4: standard PE 10 x 8 tubing, laser perforated; no galvanic couple, push-fit native)
TUBE_C = (6.5, -5.5)
TUBE_OD, TUBE_ID = 10.0, 8.0
HOLE_D = 0.35           # CNC micro-drilled or laser, +/-0.01
HOLE_PITCH = 5.0
HOLE_DIR = (-1.0, 0.0)  # jets toward glass, horizontal

# Gaskets / blocks
LAND_GASKET = [(0, -3), (0.5, -3), (0.5, 0), (0, 0)]                     # 0.5 mm EPDM/PE adhesive strip
SETTING_BLOCK = [(-T_GLASS, 0), (0, 0), (0, 2), (-T_GLASS, 2)]            # EPDM 70 ShA
WEDGE = [(-12, -16.8), (-T_GLASS, -16.8), (-T_GLASS, -1.0), (-9.5, -0.2), (-12, -0.2)]  # EPDM wedge

# Functional features (for drawings)
SLOT = dict(x0=0.0, x1=1.0, z_top=-3.0, z_fin_top=-7.6, z_exit=-13.5)
JET_TRAVEL = TUBE_C[0] - 5.0   # 1.5 mm
JET_Z = -5.5

# Hole pattern for a body length Lb (mm): uniform pitch, first/last hole half a pitch from the end walls
def hole_positions(Lb=990.0, pitch=HOLE_PITCH):
    n = int(round(Lb / pitch))
    return [round(pitch * (i + 0.5), 3) for i in range(n)]

CAP_OUTLINE = [(-14, -18), (-8, -18), (-8, 0), (0, 0), (0, -14.1), (1.6, -14.1), (2.6, -13), (17.8, -13),
               (17.8, 4.2), (15, 4.2), (-13.2, 4.2), (-14, 3.4)]

def circle(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

def area(poly):
    a = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2

if __name__ == "__main__":
    print("body area mm2", area(BODY), "mass kg/m", area(BODY) * 2.70e-3)
    print("cover area mm2", area(COVER), "mass kg/m (Al)", area(COVER) * 2.70e-3)
    t = math.pi / 4 * (TUBE_OD ** 2 - TUBE_ID ** 2)
    print("tube kg/m", t * 7.98e-3, "water in tube mL/m", math.pi / 4 * TUBE_ID ** 2)
    hp = hole_positions(); print("holes", len(hp), hp[:6], hp[-6:])
