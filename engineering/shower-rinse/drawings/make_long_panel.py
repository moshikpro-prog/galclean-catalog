"""Long glass (>1.2 m): split into two halves with an internal plug; two feed cases."""
import make_meeting_figs as mf
f = mf.Fig()
INK, GREY, BLUE, OR = mf.INK, mf.GREY, mf.BLUE, mf.ORANGE
mf.txt(f, (60, 60), "זכוכית ארוכה מ-1.2 מ': מחלקים לשני חצאים", 34, "start", INK, "bold")

def row(y, both_walls, title, sub):
    mf.txt(f, (1540, y - 150), title, 28, "end", INK, "bold"); mf.txt(f, (1540, y - 116), sub, 22, "end", GREY)
    x0, x1 = 160, 1440
    f.add(f'<rect x="{x0-30}" y="{y-60}" width="26" height="150" fill="#c9cfd4"/>')
    if both_walls: f.add(f'<rect x="{x1+4}" y="{y-60}" width="26" height="150" fill="#c9cfd4"/>')
    f.line((x0, y + 40), (x1, y + 40), "#9fd3e8", 12)                                   # glass
    f.add(f'<rect x="{x0}" y="{y-4}" width="{x1-x0}" height="40" rx="8" fill="#dfe4e8" stroke="#8a969f" stroke-width="2"/>')
    xm = (x0 + x1) / 2
    ty = y + 22
    f.line((x0 + 20, ty), (xm - 14, ty), BLUE, 9); f.line((xm + 14, ty), (x1 - 20, ty), OR, 9)
    for x in range(int(x0 + 40), int(xm - 20), 30): f.line((x, ty + 5), (x, y + 34), BLUE, 2.5)
    for x in range(int(xm + 30), int(x1 - 20), 30): f.line((x, ty + 5), (x, y + 34), OR, 2.5)
    f.add(f'<rect x="{xm-8}" y="{ty-16}" width="16" height="32" fill="{INK}"/>')
    mf.txt(f, (xm, y + 100), "פקק פנימי באמצע", 22, color=INK, weight="bold")
    mf.txt(f, ((x0 + xm) / 2, y + 100), "חצי 1", 24, color=BLUE, weight="bold")
    mf.txt(f, ((xm + x1) / 2, y + 100), "חצי 2", 24, color=OR, weight="bold")
    # feeds
    f.path(f"M{x0-17},{y-70} L{x0-17},{ty} L{x0+18},{ty}", BLUE, 6, marker="flow")
    if both_walls:
        f.path(f"M{x1+17},{y-70} L{x1+17},{ty} L{x1-18},{ty}", OR, 6, marker="flow")
    else:
        f.path(f"M{x0-8},{y-70} L{x0-8},{y+6} L{xm+20},{y+6}", OR, 6, dash="14 8", marker="flow")
        mf.txt(f, ((x0 + xm) / 2, y - 16), "צינורית בלי חורים עד האמצע", 22, color=OR)

row(250, True, "שני הצדדים קבועים (קיר או פינה)", "כל חצי מוזן מהקצה הקרוב אליו")
row(590, False, "רק צד אחד קבוע (למשל דלת רחבה)", "החצי הרחוק מקבל צינורית מעבר בתוך אותה מסילה")
mf.txt(f, (60, 870), "בכל חצי עד כ-1 מ' – החלוקה אחידה (כ-1% הפרש במקום 11% בזכוכית של 1.6 מ' בצינור אחד)", 22, "start", GREY)
f.save("F_LONG_panel.svg")
