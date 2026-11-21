"""Figures for the meeting deck (16:9, 1600x900 user units). Run: python3 make_meeting_figs.py"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cad"))
from geometry import *
import make_drawings as md
from make_explainer import C, WATER_SLOT, step as _step

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meeting")
os.makedirs(OUT, exist_ok=True)
INK, GREY = "#1b2a35", "#6b7a86"
BLUE, BLUE_D, ORANGE, WALL, GLASS = "#1f7fd1", "#155fa0", "#e07b24", "#c9cfd4", "#bfe3f2"

class Fig(md.Sheet):
    def __init__(self, w=1600, h=900):
        super().__init__("", "", ""); self.W, self.H = w, h
    def save(self, name):
        defs = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1.5 L10,5 L0,8.5 z" fill="#1b2a35"/></marker>'
                f'<marker id="flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
                '<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3" markerHeight="3"><circle cx="5" cy="5" r="4" fill="#1b2a35"/></marker>'
                '<pattern id="hGl" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(60)"><rect width="6" height="6" fill="#dff1f7"/><line x1="0" y1="0" x2="0" y2="6" stroke="#7fb6c9" stroke-width="0.6"/></pattern>'
                + "".join(self.defs) + '</defs>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">'
               f'<rect width="{self.W}" height="{self.H}" fill="#f6f8f9"/>{defs}{"".join(self.e)}</svg>')
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg); print("wrote", name)

def T_(f, s=1.0): return f
def txt(f, p, s, size=22, anchor="middle", color=INK, weight="normal"):
    f.text(p, s, size, anchor, color, weight)

# ---------------- plan-view helpers ----------------
def plan_base(f, ox, oy, px_m, walls, glasses, comp):
    for (x0, y0, x1, y1) in walls:
        f.add(f'<rect x="{ox+min(x0,x1)*px_m-9}" y="{oy+min(y0,y1)*px_m-9}" width="{abs(x1-x0)*px_m+18}" height="{abs(y1-y0)*px_m+18}" fill="{WALL}"/>')
    for g in glasses:
        (x0, y0, x1, y1) = g["xy"]
        f.line((ox + x0 * px_m, oy + y0 * px_m), (ox + x1 * px_m, oy + y1 * px_m), "#7fb6c9", 10)
    cx, cy, cw, ch = comp
    f.add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')

def rail(f, a, b, color, width=14, label=None, lab_off=(0, 0), num=None, num_pos=None, ncol=BLUE):
    f.line(a, b, color, width)
    if num is not None:
        p = num_pos or ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        f.circle(p, 22, ncol, "#ffffff", 3); txt(f, (p[0], p[1] + 9), str(num), 26, color="#ffffff", weight="bold")

def timeline(f, x, y, w, rows, total_s, title):
    txt(f, (x + w, y - 18), title, 24, "end", INK, "bold")
    rh = 40
    for i, (lab, t0, t1, col) in enumerate(rows):
        yy = y + i * (rh + 12)
        f.add(f'<rect x="{x}" y="{yy}" width="{w}" height="{rh}" rx="6" fill="#e6ebee"/>')
        X0, X1 = x + w - t1 / total_s * w, x + w - t0 / total_s * w      # right-to-left time axis (Hebrew)
        f.add(f'<rect x="{X0}" y="{yy}" width="{X1-X0}" height="{rh}" rx="6" fill="{col}"/>')
        txt(f, ((X0 + X1) / 2, yy + 28), f"{t0}–{t1} ש'", 22, color="#ffffff", weight="bold")
        txt(f, (x + w + 16, yy + 28), lab, 22, "start", INK)
    yy = y + len(rows) * (rh + 12) + 26
    for s in range(0, total_s + 1, 45):
        X = x + w - s / total_s * w
        f.line((X, yy - 14), (X, yy - 6), GREY, 2); txt(f, (X, yy + 16), f"{s}", 20, color=GREY)
    txt(f, (x + w / 2, yy + 44), "זמן (שניות) ←", 20, color=GREY)

# ---------------- F_A / F_B: corner shower ----------------
def corner(mode):
    f = Fig()
    ox, oy, px = 170, 150, 470
    walls = [(0, 0, 1.5, 0), (0, 0, 0, 1.05)]
    side = dict(xy=(0.9, 0.0, 0.9, 0.9)); front = dict(xy=(0.0, 0.9, 0.9, 0.9))
    plan_base(f, ox, oy, px, walls, [side, front], (ox + 1.12 * px, oy - 62, 300, 124))
    P = lambda x, y: (ox + x * px, oy + y * px)
    txt(f, (ox + 1.12 * px + 150, oy - 22), "תא בקיר", 24, weight="bold")
    txt(f, (ox + 1.12 * px + 150, oy + 10), "GalClean · בקר · ברזים", 21, color=GREY)
    # shower head + interior label
    f.circle(P(0.3, 0.3), 26, "#dfe3e6", INK, 2); txt(f, P(0.45, 0.62), "פנים המקלחון", 24, color=GREY)
    txt(f, P(1.18, 0.5), "זכוכית צד", 24, "start", INK, "bold"); txt(f, P(0.45, 1.04), "זכוכית חזית", 24, "middle", INK, "bold")
    a_on = mode == "A"
    c1 = BLUE; c2 = BLUE if a_on else ORANGE
    # rails (inside face)
    rail(f, P(0.88, 0.03), P(0.88, 0.87), "#58656f", 12, num=1, num_pos=P(0.80, 0.45), ncol=c1)
    rail(f, P(0.03, 0.88), P(0.87, 0.88), "#58656f", 12, num=2, num_pos=P(0.45, 0.80), ncol=c2)
    # feed lines
    v1 = (ox + 1.12 * px + 70, oy + 62); v2 = (ox + 1.12 * px + 200, oy + 62)
    f.path(f"M{v1[0]},{v1[1]} L{v1[0]},{oy+24} L{P(0.88,0)[0]},{oy+24} L{P(0.88,0.06)[0]},{P(0.88,0.06)[1]}", c1, 6, marker="flow")
    f.path(f"M{v2[0]},{v2[1]} L{v2[0]},{oy+40} L{P(0.85,0)[0]},{oy+40} L{P(0.85,0.85)[0]},{P(0.85,0.85)[1]} L{P(0.78,0.85)[0]},{P(0.78,0.85)[1]}", c2, 5, dash="14 8", marker="flow")
    txt(f, P(1.05, 0.25), "קו 1 → מסילה 1", 21, "start", BLUE_D)
    txt(f, P(1.05, 0.73), "קו 2 עובר בתוך מסילה 1 (קו מעבר)", 21, "start", c2 if not a_on else BLUE_D)
    txt(f, P(1.05, 0.79), "ומזין את מסילה 2 בפינה", 21, "start", GREY)
    for v, n in ((v1, 1), (v2, 2)):
        f.add(f'<rect x="{v[0]-26}" y="{v[1]-6}" width="52" height="34" rx="6" fill="{c1 if n==1 else c2}"/>')
        txt(f, (v[0], v[1] + 18), f"ברז {n}", 18, color="#ffffff", weight="bold")
    if a_on:
        timeline(f, 930, 520, 520, [("זכוכית 1", 0, 45, BLUE), ("זכוכית 2", 0, 45, BLUE)], 90,
                 "שני הברזים נפתחים יחד – 45 שניות")
        txt(f, (1450, 760), "מכשיר 4 ל'/דק' · כ-3 ל' לשטיפה", 24, "end", INK, "bold")
        f.save("F_A_corner_4L.svg")
    else:
        timeline(f, 930, 520, 520, [("זכוכית 1", 0, 45, BLUE), ("זכוכית 2", 45, 90, ORANGE)], 90,
                 "קודם זכוכית 1, אחר כך זכוכית 2")
        txt(f, (1450, 760), "מכשיר 2 ל'/דק' · כ-3 ל' לשטיפה · 90 שניות", 24, "end", INK, "bold")
        f.save("F_B_corner_2L.svg")

# ---------------- F_B2: large U shower, 4 zones ----------------
def ushower():
    f = Fig()
    ox, oy, px = 120, 170, 330
    walls = [(0, 0, 3.6, 0)]
    L, Fw = 0.9, 1.6
    gl = [dict(xy=(0.2, 0, 0.2, L)), dict(xy=(0.2, L, 0.2 + Fw, L)), dict(xy=(0.2 + Fw, 0, 0.2 + Fw, L))]
    plan_base(f, ox, oy, px, walls, gl, (ox + 2.35 * px, oy - 75, 300, 130))
    P = lambda x, y: (ox + x * px, oy + y * px)
    txt(f, (ox + 2.35 * px + 150, oy - 35), "תא בקיר", 24, weight="bold"); txt(f, (ox + 2.35 * px + 150, oy - 4), "GalClean 2 ל'/דק' · 4 ברזים", 21, color=GREY)
    cols = [BLUE, ORANGE, "#2f9e6a", "#8a5cc7"]
    rail(f, P(0.22, 0.03), P(0.22, L - 0.03), "#58656f", 12, num=1, num_pos=P(0.33, 0.45), ncol=cols[0])
    rail(f, P(0.23, L - 0.02), P(0.2 + Fw / 2 - 0.02, L - 0.02), "#58656f", 12, num=2, num_pos=P(0.6, L - 0.14), ncol=cols[1])
    rail(f, P(0.2 + Fw / 2 + 0.02, L - 0.02), P(0.2 + Fw - 0.03, L - 0.02), "#58656f", 12, num=3, num_pos=P(1.4, L - 0.14), ncol=cols[2])
    rail(f, P(0.2 + Fw - 0.02, 0.03), P(0.2 + Fw - 0.02, L - 0.03), "#58656f", 12, num=4, num_pos=P(1.69, 0.45), ncol=cols[3])
    f.add(f'<rect x="{P(0.2+Fw/2,0)[0]-5}" y="{P(0, L)[1]-16}" width="10" height="32" fill="{INK}"/>')
    txt(f, (P(0.2 + Fw / 2, 0)[0], P(0, L)[1] + 48), "פקק פנימי – מפריד בין אזור 2 ל-3", 20, color=GREY)
    # concealed lines (wall/ceiling) from compartment to both wall ends
    cx = ox + 2.35 * px
    f.path(f"M{cx+40},{oy+55} L{cx+40},{oy-10} L{P(0.1,0)[0]},{oy-10}", GREY, 3, dash="6 6")
    txt(f, (P(1.0, 0)[0], oy - 22), "קווים סמויים בקיר או בתקרה", 20, color=GREY)
    for i, (x, col) in enumerate([(0.25, cols[0]), (0.29, cols[1])]):
        f.path(f"M{P(0.1,0)[0]},{oy-10} L{P(x,0)[0]},{oy-10} L{P(x,0.1)[0]},{P(0,0.1)[1]} L{P(x,0.8 if i else 0.3)[0]},{P(0,0.8 if i else 0.3)[1]}" + (f" L{P(0.36,0.8)[0]},{P(0,0.8)[1]}" if i else ""), col, 5 - i, dash=None if i == 0 else "12 7", marker="flow")
    for i, (x, col) in enumerate([(0.2 + Fw - 0.05, cols[3]), (0.2 + Fw - 0.09, cols[2])]):
        f.path(f"M{cx+40},{oy+30} L{P(x,0)[0]},{oy+30} L{P(x,0.8 if i else 0.3)[0]},{P(0,0.8 if i else 0.3)[1]}" + (f" L{P(0.2+Fw-0.16,0.8)[0]},{P(0,0.8)[1]}" if i else ""), col, 5 - i, dash=None if i == 0 else "12 7", marker="flow")
    txt(f, P(0.40, 0.66), "קו 2 בתוך מסילה P", 20, "start", GREY)
    txt(f, P(1.60, 0.66), "קו 3 בתוך מסילה P", 20, "end", GREY)
    timeline(f, 900, 560, 540, [("אזור 1", 0, 45, cols[0]), ("אזור 2", 45, 90, cols[1]), ("אזור 3", 90, 135, cols[2]),
                                ("אזור 4", 135, 180, cols[3])], 180, "אזור אחר אזור – כל אזור מקבל את כל המים")
    txt(f, (60, 860), "מקלחון U: 0.9 + 1.6 + 0.9 מ' · 4 אזורים של עד ~0.9 מ' · כ-3 דקות · כ-6 ל'", 24, "start", INK, "bold")
    f.save("F_B2_U_4zones.svg")

# ---------------- F_SP: rail S vs rail P ----------------
def draw_rail(f, ox, oy, s, body, cover, passline=False):
    T = f.view(ox, oy, s)
    f.poly(T, [(-T_GLASS, -30), (0, -30), (0, 0), (-T_GLASS, 0)], "url(#hGl)", INK, 1)
    f.poly(T, body, C["alu"], INK, 1.4); f.poly(T, cover, C["cov"], INK, 1.4)
    for g in (WEDGE, SETTING_BLOCK, LAND_GASKET): f.poly(T, g, C["gasket"], INK, 0.6)
    c = T(*TUBE_C); f.circle(c, 5 * s, C["tube"], INK, 1.2); f.circle(c, 4 * s, C["water_l"], INK, 1)
    f.poly(T, WATER_SLOT[:-2] + [(0.35, -30), (0, -30)], C["water"], "none", 0)
    if passline:
        p = T(*PASS_C); f.circle(p, PASS_OD / 2 * s, ORANGE, INK, 1.2); f.circle(p, PASS_ID / 2 * s, "#fde3cc", INK, 1)
    return T

def rails_SP():
    f = Fig()
    T1 = draw_rail(f, 330, 300, 11, BODY, COVER)
    T2 = draw_rail(f, 1010, 300, 11, BODY_P, COVER_P, True)
    txt(f, (440, 120), "מסילה S – רגילה", 34, weight="bold"); txt(f, (440, 160), "רוחב 29.6 מ\"מ · לכל זכוכית שמוזנת ישירות", 22, color=GREY)
    txt(f, (1180, 120), "מסילה P – עם קו מעבר", 34, weight="bold"); txt(f, (1180, 160), "רוחב 38.6 מ\"מ · כשצריך להעביר מים לזכוכית הבאה", 22, color=GREY)
    f.dim(T1(-14, 4), T1(15.6, 4), -24, "29.6 מ\"מ", size=22)
    f.dim(T2(-14, 4), T2(24.6, 4), -24, "38.6 מ\"מ", size=22)
    f.line(T2(PASS_C[0] + 2, PASS_C[1] - 2), (1300, 700), GREY, 1.5, marker="dot")
    txt(f, (1300, 730), "קו מעבר 8×6 בלי חורים", 22, "middle", ORANGE, "bold"); txt(f, (1300, 760), "מוליך מים לאזור הבא בלי לשפוך", 20, color=GREY)
    f.line(T1(*TUBE_C), (560, 700), GREY, 1.5, marker="dot")
    txt(f, (560, 730), "צינור מחורר 10×8 – זהה בשתי המסילות", 22, "middle", BLUE_D, "bold")
    f.save("F_SP_rails.svg")

# ---------------- F_TUBE: how the tube is held ----------------
def tube_hold():
    f = Fig()
    T = f.view(430, 300, 30)
    f.add('<clipPath id="ct"><rect x="60" y="60" width="760" height="760"/></clipPath>'); f.add('<g clip-path="url(#ct)">')
    f.poly(T, [(-T_GLASS, -30), (0, -30), (0, 0), (-T_GLASS, 0)], "url(#hGl)", INK, 1.5)
    f.poly(T, BODY, C["alu"], INK, 2); f.poly(T, COVER, C["cov"], INK, 2); f.poly(T, LAND_GASKET, C["gasket"], INK, 1)
    c = T(*TUBE_C); f.circle(c, 5 * 30, C["tube"], INK, 2); f.circle(c, 4 * 30, C["water_l"], INK, 1.5)
    f.add('</g>')
    pts = [(225, "עריסה – משמאל ולמטה"), (285, "עריסה – מלמטה"), (325, "עריסה – מימין"), (66, "צלע עליונה"), (114, "צלע עליונה")]
    labs = [(870, 600), (870, 680), (870, 530), (870, 240), (870, 320)]
    for (ang, lab), (lx, ly) in zip(pts, labs):
        p = T(TUBE_C[0] + 5 * math.cos(math.radians(ang)), TUBE_C[1] + 5 * math.sin(math.radians(ang)))
        f.circle(p, 9, ORANGE, "#ffffff", 2)
        f.line(p, (lx - 10, ly - 8), GREY, 1.4)
        txt(f, (lx, ly), lab, 24, "start", INK, "bold")
    txt(f, (870, 110), "הצינור נעול בצורה, לא בלחיצה", 32, "start", INK, "bold")
    txt(f, (870, 410), "מרווח 0.05 מ\"מ סביב – לא זז הצידה,", 22, "start", GREY)
    txt(f, (870, 440), "גם כשהפלסטיק מתרכך עם השנים", 22, "start", GREY)
    # keyed end plug sketch
    y = 800; x0 = 870
    f.add(f'<rect x="{x0}" y="{y-22}" width="380" height="44" rx="8" fill="{C["tube"]}"/>')
    f.add(f'<rect x="{x0+380}" y="{y-26}" width="70" height="52" rx="6" fill="{ORANGE}"/>')
    f.add(f'<rect x="{x0+450}" y="{y-34}" width="110" height="68" rx="6" fill="none" stroke="{INK}" stroke-width="3"/>')
    txt(f, (x0 + 190, y + 60), "צינור", 20, color=GREY); txt(f, (x0 + 415, y + 60), "פקק עם מפתח", 20, color=ORANGE)
    txt(f, (x0 + 505, y + 88), "שקע בפקק הקצה", 20, color=GREY)
    txt(f, (x0 + 280, y - 46), "צד אחד נועל סיבוב ומאפשר החלקה של ~4 מ\"מ (התפשטות בחום)", 20, "middle", INK)
    f.save("F_TUBE_hold.svg")

# ---------------- F_SEC: big section with 4 steps ----------------
def big_section():
    f = Fig()
    T = draw_rail(f, 700, 230, 16, BODY, COVER)
    f.line(T(TUBE_C[0] - 5.1, JET_Z), T(0.15, JET_Z), BLUE, 3, marker="flow")
    for zz in (-18, -25):
        p = T(0.6, zz); f.line((p[0] + 10, p[1] - 22), (p[0] + 10, p[1] + 8), BLUE, 3, marker="flow")
    for n, xy in ((1, TUBE_C), (2, (2.4, -1.8)), (3, (-4.2, -10.0)), (4, (-4.2, -22))):
        p = T(*xy); f.circle(p, 24, BLUE, "#ffffff", 3); txt(f, (p[0], p[1] + 9), str(n), 26, color="#ffffff", weight="bold")
    f.save("F_SEC_steps.svg")

if __name__ == "__main__":
    corner("A"); corner("B"); ushower(); rails_SP(); tube_hold(); big_section()
