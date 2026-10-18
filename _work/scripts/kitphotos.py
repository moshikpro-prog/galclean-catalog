"""Real product photos for the 'what's in the kit' section (A4 + mobile)."""
import base64, io, pathlib
import numpy as np
from PIL import Image

W = pathlib.Path(__file__).parent

def _uri(im, max_w=None, max_h=None):
    im = im.copy()
    if max_w or max_h:
        im.thumbnail((max_w or 10**5, max_h or 10**5), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def _pole():
    im = Image.open(W / "pole_cut.png").convert("RGBA"); a = np.array(im)
    # trim the loose hose end that sticks up past the pole tip (top rows, right of the tip)
    for y in range(0, 100):
        xs = np.where(a[y, :, 3] > 128)[0]
        if len(xs):
            a[y, :max(xs.min() - 2, 0), 3] = 0
    a[:12, :, 3] = 0
    im = Image.fromarray(a); im = im.crop(im.getbbox())
    im = im.rotate(-38, resample=Image.BICUBIC, expand=True)
    return im.crop(im.getbbox())

IMG = {
    "reel": _uri(Image.open(W / "reel_fix.png"), max_w=560),
    "head": _uri(Image.open(W / "mop_cut.png"), max_w=820),
    "bluebrush": _uri(Image.open(W / "bluebrush_cut.png"), max_w=260),
    "pole": _uri(_pole(), max_w=620),
    "dev_home": _uri(Image.open(W / "a_final3.png"), max_h=420),
    "dev_biz": _uri(Image.open(W / "b_final3.png"), max_h=420),
}

KITS = {
    "Lite": dict(dev=("מכשיר אוסמוזה הפוכה", "ללא חשמל"), reel=("תוף עם צינור הזרמת מים", "20 מ'"),
                 head=("ראש לניקוי חלונות", '20 ס"מ'), pole=("מוט לעבודה", "עד 4 מטר"), extra=[]),
    "Plus": dict(dev=("מכשיר אוסמוזה הפוכה עם משאבה", "משאבה חשמלית"), reel=("תוף עם צינור הזרמת מים", "50 מ'"),
                 head=("ראש מקצועי לניקוי חלונות", '35 ס"מ'), pole=("מוט לעבודה", "עד 4 מטר"), extra=[]),
    "Business": dict(dev=("מכשיר אוסמוזה הפוכה עם משאבה", "משאבה חשמלית"), reel=("תוף עם צינור הזרמת מים", "50 מ'"),
                 head=("ראש מקצועי לניקוי חלונות", '35 ס"מ'), pole=("מוט לעבודה", "עד 4 מטר"),
                 extra=[("trolley", "עגלה לניידות"), ("tds", "מד TDS דיגיטלי"),
                        ("brush", "מברשת לניקוי רפרפות וצלונים"), ("connect", "סט מחברי מים מהירים")]),
}

PHOTO = {"reel": "reel", "head": "head", "pole": "pole"}

def _tile(key, inner, text):
    return (f'<div class="kt k-{key}"><div class="ph"><span class="glow"></span>{inner}<span class="sh"></span></div>'
            f'<div class="cap"><b>{text}</b></div></div>')

def kit_html(p, ic, mode):
    """Same items, same order, same text as before. Only reel / head / pole become photos."""
    items = p["kit"]
    main, rest = items[:4], items[4:]
    tiles = ""
    for key, text in main:
        if key in PHOTO:
            tiles += _tile(key, f'<img src="{IMG[PHOTO[key]]}">', text)
        else:
            tiles += _tile("icon", f'<span class="bigic">{ic(key)}</span>', text)
    def _rest_ic(i):
        if i == "brush":  # louvre/slat brush: real photo instead of icon
            return f'<span class="ic kph"><img src="{IMG["bluebrush"]}" alt=""></span>'
        return ic(i)
    rest_html = "".join(f'<div class="kit-i">{_rest_ic(i)}<div class="kit-t">{t}</div></div>' for i, t in rest)
    if mode == "a4":
        out = f'<div class="kg4">{tiles}</div>'
        if rest: out += f'<div class="kit-g n8 krest">{rest_html}</div>'
        return out
    out = f'<div class="kgm">{tiles}</div>'
    if rest: out += f'<div class="kit krest">{rest_html}</div>'
    return out

_TILE = r'''
.kt{position:relative;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,.08);
 background:linear-gradient(165deg,#1a222e 0%,#11161d 55%,#0d1015 100%)}
.kt:after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.07)}
.kt .ph{position:relative;display:flex;align-items:center;justify-content:center}
.kt .glow{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(160,205,245,.20) 0%,rgba(94,196,255,.06) 45%,transparent 70%)}
.kt img{position:relative;z-index:2;filter:drop-shadow(0 0 .7px rgba(255,255,255,.5)) drop-shadow(0 10px 12px rgba(0,0,0,.55))}
.k-pole .glow{background:radial-gradient(circle,rgba(185,220,250,.34) 0%,rgba(94,196,255,.10) 45%,transparent 72%)!important}
.k-pole img{filter:drop-shadow(0 0 1px rgba(255,255,255,.7)) drop-shadow(0 0 6px rgba(160,210,255,.25)) drop-shadow(0 10px 12px rgba(0,0,0,.55))!important}
.kt .sh{position:absolute;left:50%;transform:translateX(-50%);border-radius:50%;z-index:1;
 background:radial-gradient(ellipse,rgba(0,0,0,.65),transparent 70%)}
.kt .cap{position:relative;display:flex;flex-direction:column;align-items:flex-start}
.kt .cap b{font-weight:700;line-height:1.3}
.kt .cap em{font-style:normal;font-weight:700;color:var(--ac);border:1px solid rgba(94,196,255,.35);
 background:rgba(94,196,255,.08);border-radius:999px;white-space:nowrap;direction:rtl}
.kx-i{display:flex;align-items:center;border:1px solid var(--line);background:rgba(255,255,255,.025)}
.kx-i .ic{flex:none;border-radius:10px;background:rgba(94,196,255,.10);box-sizing:content-box}
.kx-h{color:var(--mut);font-weight:600}
.k-icon .bigic{position:relative;z-index:2;display:flex;align-items:center;justify-content:center;border-radius:50%;
 background:rgba(94,196,255,.10);border:1px solid rgba(94,196,255,.25)}
.k-icon .bigic .ic{width:100%;height:100%}
.k-icon .sh{display:none}
'''

KIT_CSS_A4 = _TILE + r'''
.kg4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.kg4 .ph{height:108px}
.kg4 .glow{width:120px;height:120px}
.kg4 .sh{bottom:8px;width:96px;height:12px}
.kg4 .cap{padding:2px 12px 11px;gap:5px}
.kg4 .k-icon .bigic{width:58px;height:58px;padding:13px}
.krest{margin-top:8px}
.kg4 .cap b{font-size:11px;font-weight:500;line-height:1.35}
.kg4 .cap em{font-size:9.6px;padding:2px 8px}
.kg4 .k-dev img{max-height:88px;max-width:104px}
.kg4 .k-head img{max-width:132px;max-height:100px}
.kg4 .k-reel img{max-width:112px;max-height:96px}
.kg4 .k-pole img{max-width:140px;max-height:100px}
.kx{margin-top:8px;display:flex;align-items:center;gap:10px}
.kx-h{font-size:10px;white-space:nowrap}
.kx-g{flex:1;display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.kx-i{gap:7px;padding:6px 8px;border-radius:10px;font-size:9.6px;line-height:1.25}
.kx-i .ic{width:18px;height:18px;padding:4px}
'''

KIT_CSS_M = _TILE + r'''

.kgm{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.kgm .ph{height:160px}.kgm .glow{width:170px;height:170px}.kgm .sh{bottom:10px;width:130px;height:14px}
.kgm .k-icon .bigic{width:72px;height:72px;padding:17px}
.krest{margin-top:10px}
.kgm .cap{padding:2px 16px 16px;gap:7px}
.kgm .cap b{font-size:15.5px;font-weight:500;line-height:1.4}
.kgm .cap em{font-size:14px;padding:3px 11px}
.kgm .k-head img{max-width:160px;max-height:120px}

.kgm2 .ph{height:170px}.kgm2 .glow{width:170px;height:170px}.kgm2 .sh{bottom:10px;width:130px;height:14px}
.kgm .k-reel img{max-width:140px;max-height:132px}
.kgm .k-pole img{max-width:165px;max-height:140px}
.kgm .k-dev{display:grid;grid-template-columns:110px 1fr;align-items:center}
.kgm .k-dev .ph{height:150px}.kgm .k-dev .glow{width:130px;height:130px}.kgm .k-dev .sh{bottom:12px;width:80px;height:10px}
.kgm .k-dev img{max-height:118px;max-width:96px}
.kgm .k-dev .cap{padding:16px 4px 16px 16px}
.kx{margin-top:12px}
.kx-h{font-size:15px;margin:4px 0 10px}
.kx-g{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.kx-i{gap:10px;padding:12px;border-radius:14px;font-size:14.5px;line-height:1.3}
.kx-i .ic{width:24px;height:24px;padding:6px}
'''

VIDEO_URL = "https://youtube.com/shorts/6QKcgYBsCE0"
PLAY = '<svg viewBox="0 0 24 24"><path d="M8.5 5.8v12.4a.8.8 0 0 0 1.2.7l9.6-6.2a.8.8 0 0 0 0-1.4L9.7 5.1a.8.8 0 0 0-1.2.7z" fill="currentColor"/></svg>'

def video_html(mode):
    if mode == "a4":
        return f'<a class="vid4" href="{VIDEO_URL}"><span class="pl">{PLAY}</span><div><b>צפו בסרטון</b><span>מתאימים לכל מקום</span></div></a>'
    return (f'<a class="vidm" href="{VIDEO_URL}"><span class="ring"><span class="pl">{PLAY}</span></span>'
            f'<div class="vt"><span class="k">סרטון קצר · YouTube</span><b>צפו בסרטון: מתאימים לכל מקום</b><span class="go">לצפייה ←</span></div></a>')

VID_CSS_A4 = r'''
.vid4{display:flex;align-items:center;gap:9px;padding:7px 12px 7px 14px;border-radius:999px;border:1px solid rgba(94,196,255,.4);background:rgba(94,196,255,.08);color:var(--tx);text-decoration:none}
.vid4 .pl{width:26px;height:26px;border-radius:50%;background:var(--ac);color:#06121d;display:flex;align-items:center;justify-content:center}
.vid4 .pl svg{width:14px;height:14px;margin-left:2px}
.vid4 div{display:flex;flex-direction:column;line-height:1.2}.vid4 b{font-size:11.5px;font-weight:700}.vid4 span{font-size:9.5px;color:var(--mut)}
'''
VID_CSS_M = r'''
.vidm{margin-top:14px;display:flex;align-items:center;gap:16px;padding:16px 18px;border-radius:18px;text-decoration:none;color:var(--tx);
 border:1px solid rgba(94,196,255,.35);background:radial-gradient(120% 140% at 100% 0%,rgba(94,196,255,.18),transparent 60%),linear-gradient(160deg,#18222f,#10151c)}
.vidm .ring{flex:none;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid rgba(94,196,255,.45);box-shadow:0 0 0 6px rgba(94,196,255,.08)}
.vidm .pl{width:46px;height:46px;border-radius:50%;background:var(--ac);color:#06121d;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(94,196,255,.35)}
.vidm .pl svg{width:22px;height:22px;margin-left:3px}
.vidm .vt{display:flex;flex-direction:column;gap:3px}
.vidm .k{font-size:13px;color:var(--mut)}.vidm b{font-size:18px;font-weight:800;line-height:1.3}.vidm .go{font-size:14px;font-weight:700;color:var(--ac)}
'''
KIT_CSS_A4 += VID_CSS_A4
KIT_CSS_M += VID_CSS_M

ADD_CSS = r'''
.add .ic:has(img){width:auto!important;height:auto!important;color:inherit}
.add .ic img{display:block;object-fit:contain;filter:drop-shadow(0 0 .6px rgba(255,255,255,.45)) drop-shadow(0 4px 5px rgba(0,0,0,.5))}
'''
KIT_CSS_A4 += ADD_CSS + ".add .ic img{width:40px;height:28px;margin:0 0 -6px}"
KIT_CSS_M += ADD_CSS + ".add .ic img{width:52px;height:36px;margin:0 0 -8px}"

KPH = r'''
.kit-i .ic.kph{background:radial-gradient(circle,rgba(160,205,245,.22),rgba(94,196,255,.06) 60%,transparent 75%)!important;padding:0!important}
.kit-i .ic.kph img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 .6px rgba(255,255,255,.45)) drop-shadow(0 4px 5px rgba(0,0,0,.5))}
'''
KIT_CSS_A4 += KPH + ".kit-g.n8 .kit-i .ic.kph{width:46px;height:34px;border-radius:10px}"
KIT_CSS_M += KPH + ".kit-i .ic.kph{width:78px;height:60px;border-radius:14px;background:radial-gradient(circle,rgba(170,210,250,.30),rgba(94,196,255,.08) 62%,transparent 78%)!important}"
