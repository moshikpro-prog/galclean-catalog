"""
Single source of truth for the rail cross-section (mm).
Coordinates: x = horizontal, perpendicular to the glass (x>0 = shower interior, glass inner face at x=0)
             z = vertical (glass top edge at z=0).
Extrusion direction (rail length) = y.
Baseline: 8 mm tempered glass. Other thicknesses: change wedge-gasket thickness only.
"""
import math

T_GLASS = 8.0

# ---------------------------------------------------------------------------------------------
# v0.5  Two rail variants share the glass-side half (land, slot, cradle, tube position):
#   S = standard rail (29.6 mm): tube pocket only.
#   P = pass-through rail (38.6 mm): extra channel behind the tube for one 8x6 feed line that carries
#       water THROUGH this rail to the next zone without discharging.
# The tube is held by FORM, not by clamping (PE/PP relax clamp loads): the cover cradle wraps the tube
# from 200 to 330 deg and two body ribs close it from the top -> 0.05 mm clearance pocket.
# Rotation is locked by keyed end plugs; the blind end slides axially (thermal expansion ~4 mm/m).
# ---------------------------------------------------------------------------------------------
_R = 5.05
_TC = (6.5, -5.5)
def _arc(a0, a1, step=-10):
    return [(round(_TC[0] + _R * math.cos(math.radians(a)), 3), round(_TC[1] + _R * math.sin(math.radians(a)), 3))
            for a in range(a0, a1 + step, step)]

def _body(wall_x):
    w0, w1 = wall_x, wall_x + 2.0
    pts = [(-14, -18), (-11.3, -18), (-11.3, -16.8), (-12, -16.8), (-12, 2),
           (0.5, 2), (0.5, -3), (1.5, -3), (1.5, 2),
           (3.5, 2), (3.5, -0.95), (4.5, -0.95), (4.5, 2),
           (8.5, 2), (8.5, -0.95), (9.5, -0.95), (9.5, 2)]
    if wall_x > 15:                       # P variant: rib that holds the pass-through line from above
        pts += [(PASS_C[0] - 0.6, 2), (PASS_C[0] - 0.6, PASS_C[1] + PASS_OD / 2 + 0.05),
                (PASS_C[0] + 0.6, PASS_C[1] + PASS_OD / 2 + 0.05), (PASS_C[0] + 0.6, 2)]
    pts += [(w0, 2), (w0, -10.5), (w1, -10.5), (w1, -9), (w1 - 0.6, -9), (w1 - 0.6, -7.5), (w1, -7.5),
            (w1, 3), (w1 - 1, 4), (-13, 4), (-14, 3)]
    return pts

def _cover(wall_x):
    w1 = wall_x + 2.0
    lip0, lip1 = w1 + 0.1, w1 + 1.6
    return ([(1.0, -13.5), (1.3, -13.5), (2.2, -12.5), (3.0, -12.5), (3.0, -11.7), (3.8, -11.7), (3.8, -12.5),
             (lip1, -12.5), (lip1, -6), (lip0, -6), (lip0, -7.7), (w1 - 0.5, -8.0), (w1 - 0.5, -8.8), (lip0, -8.8),
             (lip0, -10.55), (11.6, -10.55), (11.6, -8.6)] + _arc(330, 200) + [(1.0, -7.6)])

PASS_C, PASS_OD, PASS_ID = (16.6, -6.5), 8.0, 6.0
WALL_S, WALL_P = 12.0, 21.0
BODY, COVER = _body(WALL_S), _cover(WALL_S)
BODY_P, COVER_P = _body(WALL_P), _cover(WALL_P)

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

def cap_outline(wall_x=WALL_S):
    r = wall_x + 3.8
    return [(-14, -18), (-8, -18), (-8, 0), (0, 0), (0, -14.1), (1.6, -14.1), (2.6, -13), (r, -13),
            (r, 4.2), (r - 2.8, 4.2), (-13.2, 4.2), (-14, 3.4)]
CAP_OUTLINE = cap_outline(WALL_S)
CAP_OUTLINE_P = cap_outline(WALL_P)

def circle(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

def area(poly):
    a = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2

if __name__ == "__main__":
    print("S body/cover kg/m", round(area(BODY)*2.7e-3,3), round(area(COVER)*2.7e-3,3), " P:", round(area(BODY_P)*2.7e-3,3), round(area(COVER_P)*2.7e-3,3), " width S/P", WALL_S+3.6+14, WALL_P+3.6+14)
    print("body area mm2", area(BODY), "mass kg/m", area(BODY) * 2.70e-3)
    print("cover area mm2", area(COVER), "mass kg/m (Al)", area(COVER) * 2.70e-3)
    t = math.pi / 4 * (TUBE_OD ** 2 - TUBE_ID ** 2)
    print("tube kg/m", t * 7.98e-3, "water in tube mL/m", math.pi / 4 * TUBE_ID ** 2)
    hp = hole_positions(); print("holes", len(hp), hp[:6], hp[-6:])
