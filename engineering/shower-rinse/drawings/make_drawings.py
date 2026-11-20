"""Generates the drawing sheets (SVG, A3 landscape, mm) from cad/geometry.py."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cad"))
from geometry import *

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "Arial, 'Noto Sans Hebrew', 'DejaVu Sans', sans-serif"
INK, BLUE, RED, GREY = "#111", "#1f6fd1", "#c62828", "#666"

class Sheet:
    def __init__(self, title, num, scale_note):
        self.e = []; self.title = title; self.num = num; self.scale_note = scale_note
        self.defs = []
    def add(self, s): self.e.append(s)
    def view(self, ox, oy, s):
        return lambda x, z: (ox + x * s, oy - z * s)
    def poly(self, T, pts, fill="none", stroke=INK, sw=0.35, extra=""):
        d = " ".join(f"{T(x,z)[0]:.3f},{T(x,z)[1]:.3f}" for x, z in pts)
        self.add(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
    def line(self, p1, p2, stroke=INK, sw=0.25, dash=None, marker=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        self.add(f'<line x1="{p1[0]:.3f}" y1="{p1[1]:.3f}" x2="{p2[0]:.3f}" y2="{p2[1]:.3f}" stroke="{stroke}" stroke-width="{sw}"{da}{mk}/>')
    def path(self, d, stroke=INK, sw=0.3, fill="none", dash=None, marker=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{da}{mk}/>')
    def circle(self, c, r, fill="none", stroke=INK, sw=0.3):
        self.add(f'<circle cx="{c[0]:.3f}" cy="{c[1]:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self, p, s, size=3.0, anchor="middle", color=INK, weight="normal", rot=0):
        tr = f' transform="rotate({rot} {p[0]:.2f} {p[1]:.2f})"' if rot else ""
        self.add(f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}"{tr}>{s}</text>')
    def dim(self, a, b, off, label, size=2.6, ext=True):
        """Aligned dimension between sheet points a,b, offset perpendicular by off (sheet mm)."""
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        A = (a[0] + nx * off, a[1] + ny * off); B = (b[0] + nx * off, b[1] + ny * off)
        if ext:
            self.line(a, (A[0] + nx * 1.2 * math.copysign(1, off), A[1] + ny * 1.2 * math.copysign(1, off)), GREY, 0.15)
            self.line(b, (B[0] + nx * 1.2 * math.copysign(1, off), B[1] + ny * 1.2 * math.copysign(1, off)), GREY, 0.15)
        self.add(f'<line x1="{A[0]:.3f}" y1="{A[1]:.3f}" x2="{B[0]:.3f}" y2="{B[1]:.3f}" stroke="{INK}" stroke-width="0.18" marker-start="url(#arr)" marker-end="url(#arr)"/>')
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90 or ang < -90: ang += 180
        m = ((A[0] + B[0]) / 2 + nx * 1.4 * math.copysign(1, off), (A[1] + B[1]) / 2 + ny * 1.4 * math.copysign(1, off))
        self.text((m[0], m[1] + size * 0.35), label, size, rot=ang)
    def callout(self, target, at, n):
        self.line(at, target, INK, 0.18, marker="dot")
        self.circle(at, 2.4, "#fff", INK, 0.3)
        self.text((at[0], at[1] + 1.05), str(n), 2.9, weight="bold")
    def frame(self):
        W, H = 420, 297
        self.add(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{INK}" stroke-width="0.7"/>')
        # title block (bottom right)
        x0, y0 = W - 10 - 150, H - 10 - 28
        self.add(f'<rect x="{x0}" y="{y0}" width="150" height="28" fill="#fff" stroke="{INK}" stroke-width="0.5"/>')
        for yy in (y0 + 10, y0 + 19):
            self.line((x0, yy), (x0 + 150, yy), INK, 0.3)
        self.line((x0 + 100, y0 + 10), (x0 + 100, y0 + 28), INK, 0.3)
        self.text((x0 + 147, y0 + 7), self.title, 4.2, "end", weight="bold")
        self.text((x0 + 97, y0 + 16), "מסילת שטיפה עצמית לזכוכית מקלחון – קונספט C (סעפת לחץ + סדק נימי)", 2.6, "end")
        self.text((x0 + 97, y0 + 25), "מידות במ\"מ · זכוכית בסיס 8 מ\"מ · גרסה 0.4 · טיוטה לאימות בניסוי – לא לייצור", 2.6, "end")
        self.text((x0 + 125, y0 + 16), f"גיליון {self.num}", 2.8)
        self.text((x0 + 125, y0 + 25), self.scale_note, 2.8)
    def save(self, name):
        self.frame()
        defs = f'''<defs>
<marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,1.5 L10,5 L0,8.5 z" fill="{INK}"/></marker>
<marker id="flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="2.2" markerHeight="2.2"><circle cx="5" cy="5" r="4" fill="{INK}"/></marker>
<pattern id="hAl" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)"><rect width="1.6" height="1.6" fill="#e9ecef"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="#555" stroke-width="0.22"/></pattern>
<pattern id="hCov" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(-45)"><rect width="1.6" height="1.6" fill="#e2e6ea"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="#555" stroke-width="0.22"/></pattern>
<pattern id="hSS" patternUnits="userSpaceOnUse" width="1.1" height="1.1" patternTransform="rotate(30)"><rect width="1.1" height="1.1" fill="#d5d8dc"/><line x1="0" y1="0" x2="0" y2="1.1" stroke="#333" stroke-width="0.25"/></pattern>
<pattern id="hGl" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(60)"><rect width="6" height="6" fill="#dff1f7"/><line x1="0" y1="0" x2="0" y2="6" stroke="#7fb6c9" stroke-width="0.25"/><line x1="1.2" y1="0" x2="1.2" y2="6" stroke="#7fb6c9" stroke-width="0.25"/></pattern>
{"".join(self.defs)}</defs>'''
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297">'
               f'<rect width="420" height="297" fill="#fff"/>{defs}{"".join(self.e)}</svg>')
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg)
        print("wrote", name)

def draw_section(sh, T, glass_bottom=-34, show_water=True, film_scale=1.0):
    gb = glass_bottom
    sh.poly(T, [(-T_GLASS, gb), (0, gb), (0, 0), (-T_GLASS, 0)], "url(#hGl)", INK, 0.35)
    # break line at glass bottom
    x0, y0 = T(-T_GLASS - 1.5, gb); x1, _ = T(1.5, gb)
    sh.path(f"M{x0},{y0} L{(x0+x1)/2-2},{y0} l1.2,-2.4 l1.6,4.8 l1.2,-2.4 L{x1},{y0}", INK, 0.25)
    sh.poly(T, BODY, "url(#hAl)", INK, 0.45)
    sh.poly(T, COVER, "url(#hCov)", INK, 0.45)
    for g in (LAND_GASKET, SETTING_BLOCK, WEDGE):
        sh.poly(T, g, "#222", INK, 0.2)
    c = T(*TUBE_C); s = abs(T(1, 0)[0] - T(0, 0)[0])
    sh.circle(c, TUBE_OD / 2 * s, "url(#hSS)", INK, 0.4)
    sh.circle(c, TUBE_ID / 2 * s, "#cfe6fb" if show_water else "#fff", INK, 0.4)
    # orifice
    hx0 = TUBE_C[0] - TUBE_OD / 2; hx1 = TUBE_C[0] - TUBE_ID / 2
    sh.poly(T, [(hx0, JET_Z - HOLE_D / 2), (hx1, JET_Z - HOLE_D / 2), (hx1, JET_Z + HOLE_D / 2), (hx0, JET_Z + HOLE_D / 2)],
            "#cfe6fb" if show_water else "#fff", INK, 0.2)
    if show_water:
        # jet
        a = T(hx0, JET_Z); b = T(0.05, JET_Z)
        sh.line(a, b, BLUE, 0.5 * s / 5, marker="flow")
        # water in slot (meniscus-held) + film on glass
        f = 0.21 * film_scale
        pts = [(0, -4.6), (0.3, -5.2), (0.5, -6.9), (1.0, -7.9), (1.0, -13.5), (f, -14.6), (f, gb), (0, gb)]
        sh.poly(T, pts, "#9cc9f5", BLUE, 0.2, 'fill-opacity="0.85"')
        for zz in (-8, -14, -22, -28):
            p = T(f / 2 + 0.25, zz); sh.line((p[0], p[1] - 4), (p[0], p[1] + 1), BLUE, 0.35, marker="flow")

def sheet1():
    sh = Sheet("חתך A-A – חתך רוחב ראשי", "1/5", "קנה מידה 5:1")
    T = sh.view(130, 115, 5.0)
    draw_section(sh, T, -32, True, 3.0)
    # dimensions
    sh.dim(T(-14, 4), T(17.6, 4), -8, "31.6")
    sh.dim(T(-14, -18), T(-14, 4), -8, "22")
    sh.dim(T(0, -13.5), T(0, 0), 118, "13.5 – גובה קו היציאה מתחת לשפת הזכוכית")
    sh.dim(T(0, 4), T(17.6, 4), -16, "17.6 (בליטה לצד המקלחת)")
    sh.dim(T(0, -15.0), T(1.0, -15.0), 6, "1.0")
    sh.dim(T(17.6, -5.5), T(17.6, 0), 10, "5.5")
    sh.dim(T(1.0, -13.5), T(1.0, -7.6), 18, "5.9")
    sh.text((T(*TUBE_C)[0], T(*TUBE_C)[1] + 1), "PE Ø10×8", 2.6)
    # callouts
    C = [((-4, -26), (40, 200), 1), ((-13, 0), (40, 100), 2), ((-10, -9), (40, 140), 3), ((-4, 1), (40, 70), 4),
         ((0.25, -2), (150, 55), 5), ((TUBE_C[0] + 3, TUBE_C[1] + 3), (205, 55), 6), ((TUBE_C[0] - 4.6, JET_Z), (240, 75), 7),
         ((0.5, -10), (120, 230), 8), ((1.2, -13.3), (170, 230), 9), ((11, -11.5), (215, 200), 10), ((17, -9), (255, 160), 11),
         ((0.3, -28), (120, 262), 12)]
    for t, a, n in C:
        sh.callout(T(*t), a, n)
    # legend
    L = ["זכוכית מחוסמת 6–12 מ\"מ (קיימת, לא משתנה)", "גוף מסילה – פרופיל אלומיניום 6063-T6 מאולגן", "אטם טריז EPDM (עובי לפי עובי הזכוכית)",
         "בלוק הושבה EPDM 70 ShA", "רצועת מגע 0.5 מ\"מ – ייחוס הסדק לזכוכית ואיטום עליון", "סעפת – צינור PE סטנדרטי Ø10×8 מחורר בלייזר (מחבר דחיפה, ללא מתכת)",
         "פיית Ø0.35, פסיעה 5 (198 ל-990 מ\"מ), 1.5 מ\"מ מהזכוכית", "סדק נימי 1.0 מ\"מ – בריכה נימית ~7.5–10 מ\"מ מאחדת את הסילונים לקו רציף",
         "שפת סכין 0.3 מ\"מ בולטת 1 מ\"מ מתחת לרצפה – קו יציאה ושבירת טפטוף", "כיסוי נשלף – עריסה משופעת לזכוכית (ניקוז טיפות), סנפיר ותפס", "תפס הצמדה לגוף המסילה",
         "יריעת מים על הזכוכית (עובי מוגדל ×3 לצורך המחשה)"]
    x, y = 405, 30
    sh.text((x, y), "מקרא", 3.6, "end", weight="bold")
    for i, s in enumerate(L):
        sh.circle((x - 2.4, y + 7 + i * 7.2 - 1), 2.1, "#fff", INK, 0.25)
        sh.text((x - 2.4, y + 7 + i * 7.2), str(i + 1), 2.5, weight="bold")
        sh.text((x - 6.5, y + 7 + i * 7.2), s, 2.7, "end")
    notes = ["עקרון: חלוקת הספיקה נקבעת ע\"י מפל לחץ בפיות (3.5 kPa ב-2 ל'/דק'/מ') – לא ע\"י פילוס.",
             "הטיה של 10 מ\"מ לאורך 1 מ' משנה את הספיקה המקומית בכ-1.4–2% – אין צורך במנגנון פילוס.",
             "הסדק אינו מכייל ספיקה; רוחבו קובע רק את גובה הבריכה הנימית (±0.15 מ\"מ).",
             "המים יוצאים מהסדק כשהם כבר על פני הזכוכית – אין מעבר משפה לזכוכית ואין מרווח לשמור עליו."]
    sh.text((x, 160), "הערות תכנון", 3.4, "end", weight="bold")
    for i, s in enumerate(notes):
        sh.text((x, 167 + i * 6.5), s, 2.6, "end")
    # water legend
    sh.add(f'<rect x="397" y="200" width="8" height="4" fill="#9cc9f5" stroke="{BLUE}" stroke-width="0.2"/>')
    sh.text((394, 203.3), "מים מטוהרים (RO/DI)", 2.7, "end")
    sh.save("S1_section_AA.svg")

def sheet2():
    sh = Sheet("פרטים – סדק, פייה ושפת יציאה", "2/5", "קנה מידה כמצוין")
    # Detail B: slot region 12:1
    T = sh.view(70, 25, 12.0)
    def clip(poly):  # crude: draw only polygons; viewport clipping via clipPath
        return poly
    sh.defs.append('<clipPath id="cB"><rect x="34" y="45" width="118" height="235"/></clipPath>')
    sh.add('<g clip-path="url(#cB)">')
    sh.poly(T, [(-3, -23), (0, -23), (0, -1), (-3, -1)], "url(#hGl)", INK, 0.35)
    sh.poly(T, BODY, "url(#hAl)", INK, 0.45)
    sh.poly(T, COVER, "url(#hCov)", INK, 0.45)
    sh.poly(T, LAND_GASKET, "#222", INK, 0.2)
    c = T(*TUBE_C); sh.circle(c, 5 * 12, "url(#hSS)", INK, 0.4); sh.circle(c, 4.2 * 12, "#cfe6fb", INK, 0.4)
    hx0, hx1 = TUBE_C[0] - 5.0, TUBE_C[0] - 4.0
    sh.poly(T, [(hx0, -5.75), (hx1, -5.75), (hx1, -5.25), (hx0, -5.25)], "#cfe6fb", INK, 0.25)
    sh.line(T(hx0, -5.5), T(0.05, -5.5), BLUE, 1.0, marker="flow")
    f = 0.21
    pts = [(0, -4.6), (0.3, -5.2), (0.5, -6.9), (1.0, -7.9), (1.0, -13.5), (f, -14.8), (f, -23), (0, -23)]
    sh.poly(T, pts, "#9cc9f5", BLUE, 0.25, 'fill-opacity="0.85"')
    sh.add('</g>')
    sh.add('<rect x="34" y="45" width="118" height="235" fill="none" stroke="#999" stroke-width="0.3" stroke-dasharray="2 1"/>')
    sh.text((94, 40), "פרט B – אזור הסדק (12:1)", 3.6, weight="bold")
    sh.dim(T(0, -16), T(1.0, -16), 0, "1.0 ±0.15")
    sh.dim(T(1.0, -13.5), T(1.3, -13.5), 8, "0.3")
    sh.dim(T(1.5, -3.6), T(0, -3.6), 0, "1.5")
    sh.dim(T(0, -23), T(0.21, -23), 10, "δ≈0.21 (2 ל'/דק')")
    sh.text(T(-1.5, -9), "זכוכית", 3.2, rot=-90)
    sh.text((158, 150), "מניסקוס מוחזק נימית", 2.8, "start", BLUE)
    sh.line((157, 149), T(0.9, -13), BLUE, 0.2, marker="dot")
    sh.text((158, 215), "קו יציאה רציף – המים כבר על הזכוכית", 2.8, "start", BLUE)
    sh.line((157, 214), T(0.5, -14.2), BLUE, 0.2, marker="dot")
    sh.text((158, 80), "פגיעת סילון בזכוכית – v≈1.7 מ'/ש'", 2.8, "start", BLUE)
    sh.line((157, 79), T(0.1, -5.5), BLUE, 0.2, marker="dot")
    # Detail C: tube with orifice, 8:1
    T2 = sh.view(290, 95, 7.0)
    c = (0, 0)
    sh.circle(T2(0, 0), 5 * 7, "url(#hSS)", INK, 0.4); sh.circle(T2(0, 0), 4.2 * 7, "#cfe6fb", INK, 0.4)
    sh.poly(T2, [(-5, -0.25), (-4.2, -0.25), (-4.2, 0.25), (-5, 0.25)], "#cfe6fb", INK, 0.3)
    sh.line(T2(-5, 0), T2(-9, 0), BLUE, 0.8, marker="flow")
    sh.dim(T2(-5, -5.6), T2(5, -5.6), 6, "Ø10 (h11)")
    sh.dim(T2(-4.2, 4.6), T2(4.2, 4.6), -4, "Ø8.0")
    sh.text(T2(-7, 1.6), "Ø0.35 ±0.01", 2.8)
    sh.text((290, 40), "פרט C – חתך סעפת ופייה (7:1)", 3.6, weight="bold")
    sh.text((290, 150), "פייה: קידוח CNC/לייזר בדופן 1 מ\"מ (L/d≈2.9), שפה חדה, ללא גרד פנימי", 2.7)
    sh.text((290, 156), "ציר הפיות בקו אחד (±0.5°) – מכוון ע\"י סימון חריטה על הצינור", 2.7)
    # Hole pattern strip
    y = 185
    sh.text((290, y - 8), "פריסת פיות לאורך המסילה (לא בקנ\"מ) – 198 פיות ל-990 מ\"מ", 3.2, weight="bold")
    x0, x1 = 200, 380
    sh.line((x0, y), (x1, y), INK, 0.6)
    pos = hole_positions(990)
    for p in pos:
        X = x0 + p / 990 * (x1 - x0)
        sh.line((X, y - 2), (X, y + 2), BLUE, 0.25)
    sh.text((x0 + 3, y + 8), "2.5", 2.6); sh.text((x1 - 3, y + 8), "2.5", 2.6); sh.text(((x0 + x1) / 2, y + 8), "198 × פסיעה 5", 2.6)
    sh.text((290, y + 16), "פסיעה אחידה 5 מ\"מ; פיצוי שוליים (אם יידרש) ייקבע בניסוי T2/T3", 2.7)
    # tolerance table
    rows = [("רוחב סדק", "1.0 ±0.15", "קובע גובה בריכה נימית"), ("קוטר פייה", "0.35 ±0.01", "CV ספיקה ≈5.7%/פייה"),
            ("פסיעת פיות", "5 ±0.1", "–"), ("ישרות סנפיר", "0.3 / 1000", "שמירת מרווח מגע"),
            ("גובה שפת יציאה", "±0.5", "אסתטי בלבד"), ("ישרות פרופיל", "0.5 / 1000", "EN 755-9 מדויק / יישור")]
    ty = 222
    sh.text((405, ty - 6), "סבולות עיקריות", 3.2, "end", weight="bold")
    for i, (a, b, c_) in enumerate(rows):
        sh.text((405, ty + i * 6), a, 2.7, "end"); sh.text((345, ty + i * 6), b, 2.7, "middle"); sh.text((310, ty + i * 6), c_, 2.7, "end")
    sh.save("S2_details.svg")

def sheet3():
    sh = Sheet("מבטים – חזית, על, צד וקצה", "3/5", "קנה מידה כמצוין")
    # Front elevation 1:10 (panel 1000 x 2000)
    s = 0.11; ox, oy = 30, 40
    sh.add(f'<rect x="{ox}" y="{oy}" width="{1000*s}" height="{2000*s}" fill="#e8f5fa" stroke="{INK}" stroke-width="0.4"/>')
    sh.add(f'<rect x="{ox}" y="{oy-0.4}" width="{1000*s}" height="{22*s+0.4}" fill="#9aa0a6" stroke="{INK}" stroke-width="0.3"/>')
    # film
    sh.add(f'<rect x="{ox+0.5}" y="{oy+22*s}" width="{1000*s-1}" height="{2000*s-22*s}" fill="#9cc9f5" fill-opacity="0.35"/>')
    for i in range(1, 12):
        X = ox + i * 1000 * s / 12
        sh.line((X, oy + 6), (X, oy + 30), BLUE, 0.25, marker="flow")
    # inlet hose
    sh.path(f"M{ox-1},{oy+1} q-4,0 -4,6 L{ox-5},{oy+60}", BLUE, 0.6)
    sh.text((ox - 7, oy + 70), "הזנה 3/8\" מארון שירות", 2.6, rot=-90)
    sh.dim((ox, oy + 2000 * s), (ox + 1000 * s, oy + 2000 * s), 6, "1000 (רוחב זכוכית לדוגמה)")
    sh.dim((ox + 1000 * s, oy), (ox + 1000 * s, oy + 2000 * s), -6, "2000")
    sh.text((ox + 55, oy - 6), "מבט חזית מתוך המקלחון (1:10)", 3.4, weight="bold")
    sh.text((ox + 55, oy + 120), "יריעת מים רציפה", 3.0, color=BLUE)
    sh.text((ox + 55, oy + 126), "(בתנאי θ_receding נמוך – ראה דוח)", 2.5, color=BLUE)
    # Side view 1:10 (glass edge) with rail at top
    sx = 165
    sh.add(f'<rect x="{sx}" y="{oy}" width="{8*s*1.0+0.6}" height="{2000*s}" fill="#cfe9f2" stroke="{INK}" stroke-width="0.3"/>')
    sh.add(f'<rect x="{sx-14*s*1.0-0.5}" y="{oy-0.4}" width="{33.6*s+1.2}" height="{2.4+0.4}" fill="#9aa0a6" stroke="{INK}" stroke-width="0.3"/>')
    sh.text((sx + 1, oy - 6), "מבט צד (1:10)", 3.4, weight="bold")
    sh.text((sx + 10, oy + 6), "→ צד המקלחת", 2.6, "start")
    # Top view of rail 1:4, partial with break
    T = lambda x, y: (200 + y * 0.18, 85 - x * 1.6)
    sh.text((290, 30), "מבט על – מסילה 1000 מ\"מ (אורך 1:5.5, רוחב 1.6:1)", 3.4, weight="bold")
    sh.poly(lambda x, y: T(x, y), [(-14, 0), (19.8, 0), (19.8, 1000), (-14, 1000)], "#eceff1", INK, 0.35)
    sh.line(T(0, 0), T(0, 1000), GREY, 0.2, dash="1.2 0.8")
    sh.line(T(-8, 0), T(-8, 1000), GREY, 0.2, dash="1.2 0.8")
    sh.line(T(TUBE_C[0], -20), T(TUBE_C[0], 1000), BLUE, 0.25, dash="3 1 0.6 1")
    for yy in (5, 995):
        sh.line(T(-14, yy), T(17.8, yy), INK, 0.3)
    sh.text(T(-4, 500)[0:1] + (T(-4, 500)[1] + 1,), "זכוכית (נסתר)", 2.6)
    sh.text((T(22, 500)[0], T(22, 500)[1] + 1), "סעפת (קו ציר)", 2.6, color=BLUE)
    sh.dim(T(-14, 1000), T(17.8, 1000), -6, "31.8")
    sh.dim(T(17.8, 0), T(17.8, 1000), -8, "1000 = רוחב הזכוכית")
    sh.text((T(TUBE_C[0], -24)[0] - 2, T(TUBE_C[0], -24)[1] + 1), "כניסה", 2.6, "end", BLUE)
    # End view 2:1 (inlet cap)
    T3 = sh.view(225, 205, 2.0)
    outline = CAP_OUTLINE
    sh.poly(T3, [(-8, -24), (0, -24), (0, 0), (-8, 0)], "url(#hGl)", INK, 0.3)
    sh.poly(T3, outline, "#2b2b2e", INK, 0.35)
    sh.circle(T3(*TUBE_C), 5 * 2.0, "#bfc4c9", "#fff", 0.3)
    sh.circle(T3(*TUBE_C), 3.0 * 2.0, "#e9ecef", "#fff", 0.3)
    sh.text((230, 182), "מבט קצה – פקק כניסה (2:1)", 3.4, weight="bold")
    sh.text(T3(8.5, -20), "מחבר דחיפה Ø10 / 3/8\"", 2.6, color="#333")
    sh.dim(T3(-14, 4.2), T3(17.8, 4.2), -6, "31.8")
    # Side elevation of rail end with fitting, 2:1
    T4 = sh.view(345, 215, 2.0)
    sh.poly(T4, [(0, -18), (5, -18), (5, 4.2), (0, 4.2)], "#2b2b2e", INK, 0.3)
    sh.poly(T4, [(5, -18), (25, -18), (25, 4), (5, 4)], "#c9ced3", INK, 0.3)
    sh.poly(T4, [(-20, -10.5), (0, -10.5), (0, -0.5), (-20, -0.5)], "#bfc4c9", INK, 0.3)
    sh.poly(T4, [(-30, -12.5), (-14, -12.5), (-14, 1.5), (-30, 1.5)], "#5f6368", INK, 0.3)
    sh.text((340, 182), "מבט צד – קצה כניסה (2:1)", 3.4, weight="bold")
    sh.text(T4(-22, -17), "מחבר דחיפה", 2.6)
    sh.text(T4(15, -24), "גוף + כיסוי", 2.6)
    sh.save("S3_views.svg")

def sheet4():
    sh = Sheet("ניתוח הקונספט המקורי – גלישה מעל סף", "4/5", "סכמטי, ללא קנ\"מ")
    T = sh.view(80, 95, 4.0)
    # glass
    sh.poly(T, [(-8, -40), (0, -40), (0, 2), (-8, 2)], "url(#hGl)", INK, 0.35)
    # trough + weir + sloped channel (original idea), schematic
    trough = [(30, 12), (32, 12), (32, -6), (14, -6), (14, 4), (12, 4), (12, -8), (32, -8)]
    sh.poly(T, [(12, -8), (34, -8), (34, 14), (32, 14), (32, -6), (14, -6), (14, 4), (12, 4)], "url(#hAl)", INK, 0.4)
    # water in trough
    sh.poly(T, [(14, -6), (32, -6), (32, 4.7), (14, 4.7)], "#9cc9f5", BLUE, 0.2)
    # sloped channel floor descending toward glass from weir crest (12,4) to lip near glass
    sh.poly(T, [(12, 4), (12, 2), (2, -6), (1.2, -6), (1.2, -4.8)], "url(#hAl)", INK, 0.4)
    sh.poly(T, [(12, 4), (12.6, 4.7), (1.4, -4.4), (1.2, -4.8)], "#9cc9f5", BLUE, 0.2)
    sh.line(T(30, 18), T(30, 12.5), BLUE, 0.5, marker="flow")
    sh.text(T(22, 8), "תא אגירה", 3.0); sh.text(T(7, 3), "תעלה משופעת", 2.8, rot=38)
    sh.text(T(13, 7.5), "סף גלישה", 2.8)
    sh.dim(T(12, 4), T(12, 4.7), -14, "h≈0.7 מ\"מ")
    sh.dim(T(0, -6), T(1.2, -6), 8, "מרווח")
    sh.text((130, 30), "קונספט מקורי (סכמטי)", 3.8, weight="bold")
    # problems list
    P = [("1", "עומד הגלישה ב-2 ל'/דק'/מ' הוא כ-0.69 מ\"מ (1.1 מ\"מ ב-4 ל'/דק'): קטן פי 4 מאורך הנימיות (2.7 מ\"מ)."),
         ("2", "ספיקה מקומית ∝ h^1.5: לאחידות ±10% נדרש פילוס הסף ±0.05 מ\"מ לאורך מטר – לא בר־השגה בהתקנה ביתית."),
         ("3", "הטיה של 1 מ\"מ/מ' → קצה אחד מקבל פי ~20 יותר מים מהשני; 2 מ\"מ/מ' → כרבע מהאורך יבש."),
         ("4", "מתח פנים וזווית מגע מקבעים את הגלישה בנקודה הנמוכה ביותר → פסים במקום יריעה (דורש אימות, אך צפוי)."),
         ("5", "סבולות: ישרות אקסטרוזיה סטנדרטית ~1 מ\"מ/מ'; התפשטות PETG ~1.4 מ\"מ ב-ΔT=20°; זכוכית מחוסמת – קשת עד 3 מ\"מ/מ'."),
         ("6", "מרווח קבוע 'קרוב מאוד לזכוכית' אינו נשמר בגלל קשת הזכוכית; שפה קשיחה עלולה לגעת/להתרחק מקומית."),
         ("7", "מים עומדים בתא אחרי כל שימוש (≈100–150 מ\"ל) – סיכון לביופילם ולמשקעים דווקא על קו הסף."),
         ("8", "משטח משופע (לא אנכי) מאט ומעבה את הזרם ונוטה לאי-יציבות 'אצבעות' של קו המגע – אינו מאחד פסים.")]
    x, y = 405, 150
    sh.text((x, y), "ממצאים – מדוע הקונספט הוחלף בעקרון מבוסס לחץ", 3.6, "end", weight="bold")
    for i, (n, s) in enumerate(P):
        sh.text((x, y + 9 + i * 7.5), f"{n}. {s}", 2.75, "end")
    # sensitivity chart: flow nonuniformity vs tilt for weir / v-notch / orifice
    cx, cy, cw, ch = 250, 35, 150, 85
    sh.add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#fafafa" stroke="{INK}" stroke-width="0.3"/>')
    sh.text((cx + cw / 2, cy - 4), "פיזור ספיקה (מקס'/מינ') כפונקציה של הטיית המסילה – 2 ל'/דק'/מ'", 3.0, weight="bold")
    import numpy as np
    tilts = np.linspace(0, 3, 61)
    def ratio_weir(h0, dz):
        lo, hi = h0 - dz / 2, h0 + dz / 2
        if lo <= 0: return 50
        return min(50, (hi / lo) ** 1.5)
    def ratio_v(h0, dz):
        lo, hi = h0 - dz / 2, h0 + dz / 2
        return min(50, (hi / lo) ** 2.5) if lo > 0 else 50
    def ratio_o(dp, dz):
        dpp = 997 * 9.81 * dz / 1000
        return math.sqrt((dp + dpp / 2) / (dp - dpp / 2))
    def ymap(r): return cy + ch - (math.log10(r) / math.log10(50)) * ch
    def xmap(t): return cx + t / 3 * cw
    for f, col, lab, arg in [(ratio_weir, RED, "סף רציף (h=0.69)", 0.69), (ratio_v, "#ef6c00", "סף משונן V, פסיעה 10 (h=2.25)", 2.25),
                             (ratio_o, "#2e7d32", "סעפת פיות (ΔP=3.5 kPa)", 3500)]:
        d = "M" + " L".join(f"{xmap(t):.2f},{ymap(f(arg, t)):.2f}" for t in tilts)
        sh.path(d, col, 0.6)
    for r in (1, 1.1, 1.5, 2, 5, 10, 50):
        yy = ymap(r); sh.line((cx, yy), (cx + cw, yy), "#ddd", 0.15); sh.text((cx - 2, yy + 1), str(r), 2.3, "end")
    for t in (0, 0.5, 1, 1.5, 2, 2.5, 3):
        sh.text((xmap(t), cy + ch + 4), str(t), 2.3)
    sh.text((cx + cw / 2, cy + ch + 9), "הטיה לאורך 1 מ' [מ\"מ]", 2.6)
    sh.text((cx - 9, cy + ch / 2), "יחס ספיקה מקס'/מינ' (לוג)", 2.6, rot=-90)
    sh.text((cx + cw / 2, cy + ch + 15), "ערך 50 = לפחות קטע אחד ללא זרימה כלל", 2.4, color=GREY)
    for i, (col, lab) in enumerate([(RED, "סף גלישה רציף (מקורי)"), ("#ef6c00", "סף משונן V (חלופה B)"), ("#2e7d32", "סעפת פיות בלחץ (מומלץ, C)")]):
        sh.line((cx + cw - 60, cy + 8 + i * 6), (cx + cw - 52, cy + 8 + i * 6), col, 0.8)
        sh.text((cx + cw - 50, cy + 9 + i * 6), lab, 2.5, "start")
    sh.save("S4_original_concept_analysis.svg")

def sheet5():
    sh = Sheet("סכמת מערכת – GalClean ומסילות", "5/5", "סכמטי")
    def box(x, y, w, h, t1, t2="", fill="#f4f6f8", t3=""):
        sh.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="{fill}" stroke="{INK}" stroke-width="0.4"/>')
        sh.text((x + w / 2, y + h / 2 - (3 if t2 else -1)), t1, 3.0, weight="bold")
        if t2: sh.text((x + w / 2, y + h / 2 + 2), t2, 2.4)
        if t3: sh.text((x + w / 2, y + h / 2 + 6.5), t3, 2.4)
    # wall compartment
    sh.add(f'<rect x="250" y="40" width="150" height="120" rx="2" fill="none" stroke="{GREY}" stroke-width="0.5" stroke-dasharray="3 1.5"/>')
    sh.text((396, 47), "תא ייעודי בקיר (מחוץ לאזורי הרטיבות)", 2.8, "end", GREY)
    w, h = 44, 28
    box(345, 55, w, h, "מים קרים", "ברז ניתוק + מז\"ח", "#f4f6f8")
    box(290, 55, w, h, "מכשיר GalClean", "אוסמוזה הפוכה + משאבה", "#e3f0fb", "קיים – ללא שינוי")
    box(345, 115, w, h, "חיישן נזילה", "ניתוק אוטומטי", "#fff7e6")
    box(290, 115, w, h, "בקר וספק כוח", "טיימר, אזורים, דופק", "#fff7e6")
    box(258, 85, 26, 22, "מסנן", "50 µm")
    sh.line((345, 69), (334.5, 69), BLUE, 0.6, marker="flow")
    sh.path("M290,69 L271,69 L271,84.5", BLUE, 0.6, marker="flow")
    sh.text((340, 98), "תרכיז RO → ניקוז", 2.4, color=GREY)
    # manifold of zone valves
    sh.path("M271,107 L271,200 L60,200", BLUE, 0.7)
    zones = [("אזור 1", "דופן חזית"), ("אזור 2", "דופן צד"), ("אזור 3", "אופציונלי")]
    for i, (zt, zd) in enumerate(zones):
        y = 165 + i * 0 
    xs = [180, 120, 60]
    for i, (zt, zd) in enumerate(zones):
        x = xs[i]
        box(x, 160, 34, 30, f"סולנואיד {i+1}", "24V DC, NC", "#f4f6f8")
        sh.line((x + 17, 160), (x + 17, 120.5), BLUE, 0.6, marker="flow")
        box(x - 4, 92, 42, 28, f"מסילה – {zt}", zd, "#e3f0fb")
        sh.line((x + 17, 200), (x + 17, 190.5), BLUE, 0.6, marker="flow")
    sh.text((128, 84), "המסילות מותקנות על השפה העליונה של כל דופן זכוכית, סביב המקלחון", 2.8)
    sh.path("M290,129 L240,129 L240,152 L60,152", "#ef6c00", 0.4, dash="2 1")
    for xx in (180, 120, 60): sh.line((xx + 30, 152), (xx + 30, 160), "#ef6c00", 0.4, dash="2 1")
    sh.path("M290,135 L250,135", "#ef6c00", 0.4, dash="2 1")
    box(20, 60, 60, 20, "לחצן IPX7 ליד המקלחון", "או הפעלה אוטומטית", "#fff7e6")
    sh.path("M80,70 L100,70 L100,42 L300,42 L300,115", "#ef6c00", 0.4, dash="2 1")
    notes = ["• מקור המים: מכשיר GalClean קיים בזרימה ישירה, ללא מיכל. הספיקה נקבעת ע\"י הממברנה; מפל הלחץ במסילה (~3.4 kPa) זניח מולה.",
             "• כשהספיקה אינה מספיקה לכל הדפנות בבת אחת – שטיפה לפי אזורים: כל דופן מקבלת את מלוא הספיקה בתורה (45 ש' לאזור).",
             "• צינור אחיד לכל הדגמים: 198×Ø0.35 בפסיעה 5 מ\"מ מתאים ל-1.5–4 ל'/דק'/מ' (מפל 2–15 kPa).",
             "• ספיקת RO יורדת בחורף (מים קרים) בכ-25% – יש לתכנן לפי ספיקת חורף ולאמת מול נתוני היצרן.",
             "• יש לוודא את אופן ההפעלה של משאבת המכשיר (מתג לחץ אוטומטי או מתג ידני) – קובע אם מספיק ברז סולנואיד או נדרש גם ממסר.",
             "• חשמל: 24V DC (SELV) בלבד באזורי האמבטיה; 230V רק בתא, לפי IEC 60364-7-701 ותקנות מקומיות. צינור הזנה 3/8\"."]
    for i, s_ in enumerate(notes):
        sh.text((405, 216 + i * 6.0), s_, 2.6, "end")
    sh.save("S5_system_schematic.svg")

if __name__ == "__main__":
    sheet1(); sheet2(); sheet3(); sheet4(); sheet5()
