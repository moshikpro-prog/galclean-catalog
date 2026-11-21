"""Simple explainer: water enters the door through the hinge axis (closed vs open)."""
import math
import make_meeting_figs as mf
f = mf.Fig()
INK, GREY, BLUE, OR = mf.INK, mf.GREY, mf.BLUE, mf.ORANGE
mf.txt(f, (60, 60), "איך המים עוברים לדלת: דרך הציר, לא דרך צד הפתיחה", 34, "start", INK, "bold")

def panel(cx, cy, open_deg, title):
    mf.txt(f, (cx + 120, cy - 230), title, 30, "middle", INK, "bold")
    # wall on the left
    f.add(f'<rect x="{cx-40}" y="{cy-170}" width="26" height="300" fill="#c9cfd4"/>')
    # fixed glass from wall to hinge
    hx, hy = cx + 220, cy
    f.line((cx - 14, cy), (hx - 10, hy), "#9fd3e8", 12)
    f.line((cx - 14, cy - 14), (hx - 10, hy - 14), "#58656f", 8)                  # rail on fixed glass
    f.line((cx - 14, cy - 22), (hx, hy - 22), BLUE, 5)                           # feed line inside fixed rail
    # door rotated around hinge
    L = 360
    a = math.radians(-open_deg)
    ex, ey = hx + L * math.cos(a), hy + L * math.sin(a)
    f.line((hx + 10 * math.cos(a), hy + 10 * math.sin(a)), (ex, ey), "#9fd3e8", 12)
    ox, oy = -14 * math.sin(a), 14 * math.cos(a)
    f.line((hx + 14 * math.cos(a) - ox, hy + 14 * math.sin(a) - oy), (ex - ox, ey - oy), "#58656f", 8)   # door rail
    f.line((hx - 22 * math.sin(a) * 0 + 20 * math.cos(a) - 1.6 * ox, hy + 20 * math.sin(a) - 1.6 * oy),
           (ex - 1.6 * ox, ey - 1.6 * oy), BLUE, 5)                                                        # door tube
    # hinge with rotary joint
    f.circle((hx, hy - 22), 20, "#ffffff", INK, 3); f.circle((hx, hy - 22), 8, OR, OR, 1)
    mf.txt(f, ((cx + hx) / 2, cy + 50), "זכוכית קבועה", 22, "middle", GREY)
    mf.txt(f, ((hx + ex) / 2 + (40 if open_deg else 0), (hy + ey) / 2 + (40 if not open_deg else 0)), "דלת", 26, "middle", INK, "bold")
    # latch side marker
    mf.txt(f, (ex + 10, ey + 50 if open_deg < 45 else ey - 20), "צד הפתיחה", 22, "middle", GREY)
    return (hx, hy - 22)

h1 = panel(220, 420, 0, "דלת סגורה")
h2 = panel(1000, 420, 60, "דלת פתוחה")
for h in (h1, h2):
    f.line((h[0], h[1] + 30), (h[0] + 40, h[1] + 170), GREY, 1.6, marker="dot")
mf.txt(f, (h1[0] + 50, h1[1] + 200), "ציר עם מחבר מסתובב", 24, "middle", OR, "bold")
mf.txt(f, (h2[0] + 50, h2[1] + 200), "אותו חיבור – הדלת רק הסתובבה", 24, "middle", OR, "bold")
rows = ["המים מגיעים בקו (כחול) עד הציר.",
        "בציר יש מחבר שמסתובב עם הדלת, כמו מחבר מסתובב בצינור גינה.",
        "מהציר המים ממשיכים לצינור עם החורים במסילה של הדלת.",
        "צד הפתיחה לא מחובר לכלום, ולכן אין שם נתק."]
for i, r in enumerate(rows):
    f.circle((1540 - 0, 720 + i * 44 - 8), 14, BLUE, "#ffffff", 2); mf.txt(f, (1540, 720 + i * 44 - 1), str(i + 1), 18, color="#ffffff", weight="bold")
    mf.txt(f, (1515, 720 + i * 44), r, 24, "end", INK)
mf.txt(f, (60, 880), "שרטוט עקרוני, מבט מלמעלה · הצינור לא נמתח: ליד הציר כמעט אין תנועה", 20, "start", GREY)
f.save("F_DOOR_hinge.svg")
