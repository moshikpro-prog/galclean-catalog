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
BODY = [(-14, -18), (-11.3, -18), (-11.3, -16.8), (-12, -16.8), (-12, 2),
        (0.5, 2), (0.5, -4), (2.5, -4), (2.5, 2),
        (5.5, 2), (5.5, -1.1), (6.5, -1.1), (6.5, 2),
        (10.5, 2), (10.5, -1.1), (11.5, -1.1), (11.5, 2),
        (16, 2), (16, -10.5), (18, -10.5), (18, -9), (17.4, -9), (17.4, -7.5), (18, -7.5),
        (18, 3), (17, 4), (-13, 4), (-14, 3)]

# Snap-on cover / slot fin (extruded aluminium or ASA). CCW polygon.  v0.3: slot 1.0 mm, fin rises to just
# below the jets (capillary pool wall), knife tip protrudes 1 mm below the floor as a drip break.
COVER = [(1.0, -13.5), (1.3, -13.5), (2.2, -12.5), (19.6, -12.5), (19.6, -6),
         (18.1, -6), (18.1, -7.7), (17.5, -8.0), (17.5, -8.8), (18.1, -8.8), (18.1, -10.5),
         (2.2, -10.5), (2.2, -6.5), (1.0, -6.5)]

# Manifold tube (v0.3: PVDF 10 x 1, no galvanic couple with the aluminium body)
TUBE_C = (8.5, -5.5)
TUBE_OD, TUBE_ID = 10.0, 8.0
HOLE_D = 0.35           # CNC micro-drilled or laser, +/-0.01
HOLE_PITCH = 5.0
HOLE_DIR = (-1.0, 0.0)  # jets toward glass, horizontal

# Gaskets / blocks
LAND_GASKET = [(0, -4), (0.5, -4), (0.5, 0), (0, 0)]                     # 0.5 mm EPDM/PE adhesive strip
SETTING_BLOCK = [(-T_GLASS, 0), (0, 0), (0, 2), (-T_GLASS, 2)]            # EPDM 70 ShA
WEDGE = [(-12, -16.8), (-T_GLASS, -16.8), (-T_GLASS, -1.0), (-9.5, -0.2), (-12, -0.2)]  # EPDM wedge

# Functional features (for drawings)
SLOT = dict(x0=0.0, x1=1.0, z_top=-4.0, z_fin_top=-6.5, z_exit=-13.5)
JET_Z = -5.5

# Hole pattern for a body length Lb (mm): uniform pitch, first/last hole half a pitch from the end walls
def hole_positions(Lb=990.0, pitch=HOLE_PITCH):
    n = int(round(Lb / pitch))
    return [round(pitch * (i + 0.5), 3) for i in range(n)]

CAP_OUTLINE = [(-14, -18), (-8, -18), (-8, 0), (0, 0), (0, -14.1), (1.6, -14.1), (2.6, -13), (19.8, -13),
               (19.8, 4.2), (17, 4.2), (-13.2, 4.2), (-14, 3.4)]

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
