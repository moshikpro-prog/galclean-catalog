"""Plain-language explainer sheet: cutaway 3D view + coloured section + front view (S6)."""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cad"))
from geometry import *
from make_drawings import Sheet, INK, BLUE, GREY

C = dict(alu="#cfd5da", alu_d="#aeb6bd", alu_t="#e6eaed", cov="#b9c2c9", cov_d="#9aa4ac", cov_t="#d6dce1",
         glass="#d7eef6", glass_d="#b9dcea", water="#5aa6f0", water_l="#a9d1f7", gasket="#2b2d30",
         tube="#7d868d", tube_d="#5f676d", ink=INK)
WATER_SLOT = [(0, -4.6), (0.3, -5.2), (0.5, -6.9), (1.0, -7.9), (1.0, -13.5), (0.35, -14.6), (0.35, -36), (0, -36)]

def area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))) / 2

def ccw(p): return p if area(p) > 0 else p[::-1]

def cutaway(sh, ox, oy, s, Lmm, k=0.55, ang=32):
    """Oblique cutaway: near end (y=0) is the cut face; extrusion recedes up-left."""
    dx, dy = -k * math.cos(math.radians(ang)) * s, -k * math.sin(math.radians(ang)) * s
    P = lambda x, z, y=0.0: (ox + x * s + y * dx, oy - z * s + y * dy)
    v = (1.0, 0.55)                    # direction toward the viewer in the profile plane
    GL = [(-T_GLASS, -30), (0, -30), (0, 0), (-T_GLASS, 0)]
    parts = [("glass", GL, C["glass"], C["glass_d"]), ("wedge", WEDGE, C["gasket"], C["gasket"]),
             ("block", SETTING_BLOCK, C["gasket"], C["gasket"]), ("land", LAND_GASKET, C["gasket"], C["gasket"]),
             ("body", BODY, C["alu"], C["alu_d"]), ("cover", COVER, C["cov"], C["cov_d"]),
             ("tube", circle(TUBE_C, TUBE_OD / 2, 40), C["tube"], C["tube_d"])]
    quads = []
    for name, poly, col, cold in parts:
        p = ccw(poly)
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            n = (b[1] - a[1], -(b[0] - a[0]))
            nl = math.hypot(*n) or 1
            dot = (n[0] * v[0] + n[1] * v[1]) / nl
            if dot <= 0: continue
            top = n[1] / nl > 0.6
            fill = C["alu_t"] if (top and name == "body") else C["cov_t"] if (top and name == "cover") else (col if dot > 0.5 else cold)
            if name == "glass": fill = C["glass"] if dot > 0.5 else C["glass_d"]
            key = ((a[0] + b[0]) / 2 * v[0] + (a[1] + b[1]) / 2 * v[1])
            quads.append((key, [a, b], fill, name))
    quads.sort(key=lambda q: q[0])
    # water curtain on glass face (drawn after glass faces, before rail)
    for key, (a, b), fill, name in quads:
        pts = [P(*a, 0), P(*b, 0), P(*b, Lmm), P(*a, Lmm)]
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        op = ' fill-opacity="0.75"' if name == "glass" else ""
        sh.add(f'<polygon points="{d}" fill="{fill}" stroke="{INK}" stroke-width="0.25" stroke-linejoin="round"{op}/>')
        if name == "glass" and abs(a[0]) < 1e-6 and abs(b[0]) < 1e-6:   # inner face of glass: add the water sheet
            wq = [P(0.05, -13.5, 0), P(0.05, -30, 0), P(0.05, -30, Lmm), P(0.05, -13.5, Lmm)]
            sh.add('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in wq) + f'" fill="{C["water_l"]}" fill-opacity="0.85" stroke="none"/>')
            for t in range(1, 6):
                yy = Lmm * t / 6
                a1, a2 = P(0.05, -16, yy), P(0.05, -28, yy)
                sh.line(a1, a2, C["water"], 0.35, marker="flow")
    # cut face (near end)
    T = lambda x, z: P(x, z, 0)
    sh.poly(T, GL, "url(#hGl)", INK, 0.4)
    sh.poly(T, BODY, C["alu"], INK, 0.5)
    sh.poly(T, COVER, C["cov"], INK, 0.5)
    for g in (WEDGE, SETTING_BLOCK, LAND_GASKET): sh.poly(T, g, C["gasket"], INK, 0.2)
    sh.poly(T, circle(TUBE_C, TUBE_OD / 2, 60), C["tube"], INK, 0.4)
    sh.poly(T, circle(TUBE_C, TUBE_ID / 2, 60), C["water_l"], INK, 0.3)
    sh.poly(T, WATER_SLOT[:-2] + [(0.35, -30), (0, -30)], C["water"], "none", 0)
    sh.line(T(TUBE_C[0] - 5.0, JET_Z), T(0.1, JET_Z), C["water"], 0.6, marker="flow")
    # break line at glass bottom
    a, b = P(-T_GLASS - 2, -30), P(2, -30)
    sh.path(f"M{a[0]},{a[1]} L{(a[0]+b[0])/2-2},{a[1]} l1,-2 l1.5,4 l1,-2 L{b[0]},{b[1]}", INK, 0.3)
    return P

def section(sh, ox, oy, s):
    T = sh.view(ox, oy, s)
    sh.poly(T, [(-T_GLASS, -36), (0, -36), (0, 0), (-T_GLASS, 0)], "url(#hGl)", INK, 0.4)
    sh.poly(T, BODY, C["alu"], INK, 0.6)
    sh.poly(T, COVER, C["cov"], INK, 0.6)
    for g in (WEDGE, SETTING_BLOCK, LAND_GASKET): sh.poly(T, g, C["gasket"], INK, 0.25)
    c = T(*TUBE_C)
    sh.circle(c, TUBE_OD / 2 * s, C["tube"], INK, 0.5)
    sh.circle(c, TUBE_ID / 2 * s, C["water_l"], INK, 0.4)
    sh.poly(T, WATER_SLOT, C["water"], "none", 0)
    sh.line(T(TUBE_C[0] - 5.1, JET_Z), T(0.15, JET_Z), C["water"], 1.0, marker="flow")
    for zz in (-19, -26, -33):
        p = T(0.6, zz); sh.line((p[0] + 2.5, p[1] - 5), (p[0] + 2.5, p[1] + 2), C["water"], 0.7, marker="flow")
    # break
    a, b = T(-T_GLASS - 1.5, -36), T(1.5, -36)
    sh.path(f"M{a[0]},{a[1]} L{(a[0]+b[0])/2-2},{a[1]} l1,-2.4 l1.6,4.8 l1,-2.4 L{b[0]},{b[1]}", INK, 0.3)
    return T

def step(sh, at, n, color="#1f6fd1"):
    sh.circle(at, 3.4, color, "#fff", 0.6)
    sh.text((at[0], at[1] + 1.4), str(n), 4.0, color="#fff", weight="bold")

def label(sh, target, at, text, anchor="end", size=3.0, color=INK, sub=None):
    sh.line(at, target, GREY, 0.25, marker="dot")
    off = -1.5 if anchor == "end" else 1.5
    sh.text((at[0] + off, at[1] + 1.1), text, size, anchor, color, "bold")
    if sub: sh.text((at[0] + off, at[1] + 5.2), sub, 2.5, anchor, GREY)

sh = Sheet("איך המסילה עובדת", "6/6", "הסבר – ללא קנ\"מ")
sh.add('<rect x="10" y="10" width="400" height="18" fill="#f2f6f9"/>')
sh.text((405, 22), "מסילת שטיפה לזכוכית מקלחון – מבט מבחוץ וחתך פנימי", 6.0, "end", weight="bold")
sh.text((15, 22), "המים מסומנים בכחול", 3.2, "start", "#1f6fd1", "bold")

# ---------- panel A: cutaway ----------
sh.text((140, 38), "א. מבט מבחוץ, עם חיתוך בקצה", 4.4, "middle", weight="bold")
sh.text((140, 44), "קטע מהמסילה כשהיא יושבת על שפת הזכוכית. הקצה הקרוב \"חתוך\" כדי לראות מה בפנים", 2.6, "middle", GREY)
import base64, json
REN = os.path.join(os.path.dirname(__file__), "..", "renders")
img = base64.b64encode(open(os.path.join(REN, "render_cutaway.png"), "rb").read()).decode()
LB = json.load(open(os.path.join(REN, "cutaway_labels.json")))
ix, iy, iw, ih = 18, 48, 180, 144
sh.defs.append(f'<clipPath id="cutclip"><rect x="{ix}" y="{iy+3}" width="{iw}" height="{ih-3}"/></clipPath>')
sh.add(f'<g clip-path="url(#cutclip)"><image href="data:image/png;base64,{img}" x="{ix}" y="{iy}" width="{iw}" height="{ih}" preserveAspectRatio="none"/></g>')
M = lambda k: (ix + LB[k][0] / LB["w"] * iw, iy + LB[k][1] / LB["h"] * ih)
rows = [("body", "פרופיל אלומיניום", "יושב על שפת הזכוכית מלמעלה", None),
        ("tube", "צינור המים", "198 חורים זעירים לכל האורך", None),
        ("slot", "מרווח צר של 1 מ\"מ", "כאן המים מתאספים ומתפזרים", C["water"]),
        ("cover", "כיסוי נשלף", "נפתח לניקוי", None),
        ("wedge", "אטם גומי", "בצד החיצוני של המקלחון", None),
        ("water", "וילון מים", "יורד על הצד הפנימי של הזכוכית", C["water"]),
        ("glass", "הזכוכית הקיימת", "לא מחליפים ולא קודחים", None)]
for i, (k, t, sub, col) in enumerate(rows):
    label(sh, M(k), (204, 62 + i * 19), t, "start", color=col or INK, sub=sub)
sh.text((108, 196), "החיתוך בקצה מראה את פנים המסילה. המסילה ממשיכה לכל רוחב הזכוכית.", 2.5, "middle", GREY)
# ---------- panel B: big section with steps ----------
sh.line((262, 34), (262, 255), "#dde3e8", 0.4)
sh.text((336, 38), "ב. חתך פנימי – הדרך של המים", 4.4, "middle", weight="bold")
T = section(sh, 322, 64, 3.1)
sh.text(T(-4, -30), "זכוכית", 2.8, "middle", INK)
step(sh, T(*TUBE_C), 1)
step(sh, T(2.6, -2.2), 2)
step(sh, T(-4.0, -10.5), 3)
step(sh, T(-4.0, -22), 4)
sh.line(T(-2.6, -10.5), T(0.5, -10.5), "#1f6fd1", 0.3, dash="1 0.8")
sh.line(T(-2.6, -22), T(0.2, -22), "#1f6fd1", 0.3, dash="1 0.8")
a1, a2, a3 = T(1.45, -6.0), T(0.9, -7.0), T(0.15, -6.9)
sh.path(f"M{a1[0]:.2f},{a1[1]:.2f} Q{a2[0]:.2f},{a2[1]:.2f} {a3[0]:.2f},{a3[1]:.2f}", "#e8590c", 0.5, dash="1.2 0.8", marker="flow")
sh.line(T(1.8, -8.0), (356, 147), GREY, 0.25, marker="dot")
sh.text((405, 148), "בזרם חלש (התחלה וסוף)", 2.7, "end", "#e8590c", "bold")
sh.text((405, 152.5), "הטיפה נוגעת בזכוכית ועוברת אליה;", 2.4, "end", GREY)
sh.text((405, 156.5), "מה שנופל מתנקז בשיפוע לסדק", 2.4, "end", GREY)
sh.dim(T(-14, 4), T(17.6, 4), -6, "רוחב 3.2 ס\"מ")
sh.dim(T(-14, -18), T(-14, 4), -6, "גובה 2.2 ס\"מ")
steps = [("1", "המים המזוקקים נכנסים לצינור", "מגיעים מתא הקיר וממלאים את הצינור לכל האורך."),
         ("2", "יוצאים מ-198 חורים זעירים", "חור כל 5 מ\"מ. כל חור מוציא אותה כמות, ישר לעבר הזכוכית."),
         ("3", "מתאספים ב\"בריכה\" צרה", "במרווח של 1 מ\"מ בין הכיסוי לזכוכית המים מתפזרים לצדדים ומתחברים."),
         ("4", "יורדים כשכבה אחת רציפה", "יוצאים מתחת לשפה כשהם כבר צמודים לזכוכית ושוטפים אותה עד למטה.")]
for i, (n, h, d) in enumerate(steps):
    y = 190 + i * 15
    step(sh, (401, y), n)
    sh.text((395, y + 1.2), h, 3.2, "end", weight="bold")
    sh.text((395, y + 6.3), d, 2.55, "end", GREY)

# ---------- panel C: front view ----------
sh.text((70, 205), "ג. מבט מתוך המקלחון", 3.8, "middle", weight="bold")
gx, gy, gw, gh = 30, 212, 52, 42
sh.add(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="{C["glass"]}" stroke="{INK}" stroke-width="0.4"/>')
sh.add(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="{C["water_l"]}" fill-opacity="0.6"/>')
sh.add(f'<rect x="{gx-0.5}" y="{gy-2.4}" width="{gw+1}" height="2.8" fill="{C["alu_d"]}" stroke="{INK}" stroke-width="0.3"/>')
for i in range(1, 10):
    X = gx + gw * i / 10; sh.line((X, gy + 3), (X, gy + gh - 3), C["water"], 0.35, marker="flow")
sh.text((gx + gw + 4, gy + 1), "המסילה למעלה", 2.8, "start", weight="bold")
sh.text((gx + gw + 4, gy + 13), "וילון מים אחיד", 2.8, "start", C["water"], "bold")
sh.text((gx + gw + 4, gy + 18), "לכל רוחב הזכוכית", 2.6, "start", GREY)
sh.text((gx + gw + 4, gy + 30), "פועל כ-45 שניות", 2.6, "start", GREY)
sh.text((gx + gw + 4, gy + 35), "אחרי המקלחת", 2.6, "start", GREY)
sh.save("S6_explainer.svg")
