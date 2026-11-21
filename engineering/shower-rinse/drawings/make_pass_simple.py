"""Simple explainer: how the pass-through line feeds the far glass (corner, sequential mode)."""
import make_meeting_figs as mf
f = mf.Fig()
INK, GREY, BLUE, OR = mf.INK, mf.GREY, mf.BLUE, mf.ORANGE
# walls
f.add('<rect x="150" y="110" width="1300" height="26" fill="#c9cfd4"/>')          # back wall (top)
f.add('<rect x="150" y="110" width="26" height="560" fill="#c9cfd4"/>')           # side wall (left)
mf.txt(f, (800, 96), "קיר", 22, color=GREY)
# glass 1 (vertical, right side) and glass 2 (horizontal, bottom)
gx, gy0, gy1 = 1000, 136, 640        # glass 1 x, from wall (top) to corner
hy, hx0 = 640, 176                   # glass 2 y, from wall (left) to corner
f.line((gx, gy0), (gx, gy1), "#9fd3e8", 12); f.line((hx0, hy), (gx, hy), "#9fd3e8", 12)
mf.txt(f, (gx + 40, 345), "זכוכית 1", 28, "start", INK, "bold")
mf.txt(f, (560, hy + 60), "זכוכית 2 (הרחוקה)", 28, "middle", INK, "bold")
# rail bodies (grey bands, inside the shower)
f.add(f'<rect x="{gx-70}" y="{gy0}" width="62" height="{gy1-gy0-6}" rx="8" fill="#dfe4e8" stroke="#8a969f" stroke-width="2"/>')
f.add(f'<rect x="{hx0}" y="{hy-70}" width="{gx-hx0-8}" height="62" rx="8" fill="#dfe4e8" stroke="#8a969f" stroke-width="2"/>')
# perforated tube in rail 1 (blue, close to glass) with holes facing glass
t1x = gx - 26
f.line((t1x, gy0 + 10), (t1x, gy1 - 90), BLUE, 10)
for y in range(gy0 + 40, gy1 - 100, 26): f.line((t1x + 6, y), (gx - 10, y), BLUE, 2.5)
f.add(f'<rect x="{t1x-9}" y="{gy1-96}" width="18" height="12" fill="{INK}"/>')                 # plug at corner end
# pass-through line in rail 1 (orange, behind the tube, no holes)
p1x = gx - 54
f.line((p1x, gy0 + 10), (p1x, hy - 40), OR, 10)
# elbow at corner -> start of tube 2
f.path(f"M{p1x},{hy-40} Q{p1x},{hy-26} {p1x-14},{hy-26}", OR, 10)
f.circle((p1x - 8, hy - 32), 16, "#ffffff", INK, 3)
# perforated tube in rail 2 (blue)
t2y = hy - 26
f.line((p1x - 22, t2y), (hx0 + 30, t2y), BLUE, 10)
for x in range(hx0 + 50, p1x - 30, 26): f.line((x, t2y + 6), (x, hy - 10), BLUE, 2.5)
f.add(f'<rect x="{hx0+18}" y="{t2y-9}" width="12" height="18" fill="{INK}"/>')                # plug at wall end
# feeds from compartment
f.add('<rect x="1130" y="150" width="300" height="120" rx="12" fill="#ffffff" stroke="#1b2a35" stroke-width="2"/>')
mf.txt(f, (1280, 192), "תא בקיר", 26, weight="bold"); mf.txt(f, (1280, 226), "GalClean + ברז 1 + ברז 2", 21, color=GREY)
f.path(f"M1200,150 L1200,126 L{t1x},126 L{t1x},{gy0+14}", BLUE, 6)
f.path(f"M1360,150 L1360,118 L{p1x},118 L{p1x},{gy0+14}", OR, 6)
# numbered callouts
def call(n, at, target, text, sub, col):
    f.line(at, target, GREY, 1.6, marker="dot")
    f.circle(at, 24, col, "#ffffff", 3); mf.txt(f, (at[0], at[1] + 9), str(n), 26, color="#ffffff", weight="bold")
    mf.txt(f, (at[0] + 40, at[1] - 2), text, 26, "start", INK, "bold"); mf.txt(f, (at[0] + 40, at[1] + 30), sub, 22, "start", GREY)
call(1, (1110, 420), (t1x, 420), "ברז 1 → הצינור עם החורים", "שוטף רק את זכוכית 1", BLUE)
call(2, (1110, 520), (p1x, 500), "ברז 2 → צינורית בלי חורים", "עוברת מאחורי הצינור של זכוכית 1", OR)
call(3, (1110, 760), (p1x - 8, hy - 32), "בפינה: מרפק קטן", "מחבר לתחילת הצינור של זכוכית 2", OR)
call(4, (300, 780), (hx0 + 24, t2y), "הקצה השני סגור", "פקק בצד הקיר", "#58656f")
mf.txt(f, (60, 60), "איך מים מגיעים לזכוכית הרחוקה בלי לשפוך על הקרובה", 34, "start", INK, "bold")
mf.txt(f, (60, 870), "שרטוט עקרוני, לא בקנה מידה · מבט מלמעלה על מקלחון פינתי", 20, "start", GREY)
f.save("F_PASS_simple.svg")
