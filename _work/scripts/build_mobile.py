"""Mobile-first version: narrow page (430 CSS px) so a phone shows it at ~1:1 scale."""
import pathlib
import build  # reuses fonts, icons, images and verified data
from build import faces, ic, ADDONS, PAGES
from kitphotos import kit_html, video_html, KIT_CSS_M

W = pathlib.Path(__file__).parent
TEL = "tel:+972733744487"
WA = "https://tinyurl.com/galcleangeneral"  # official WhatsApp link used on galclean.co.il
WEB = "https://galclean.co.il"

CSS = r'''
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0c10;--card:#12161d;--line:rgba(255,255,255,.10);--tx:#f4f6f9;--mut:#a7b0bf;--dim:#7c8596;--ac:#5ec4ff}
html,body{background:var(--bg);width:430px}
body{font-family:'Heebo',sans-serif;color:var(--tx);direction:rtl;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.page{width:430px;padding:26px 22px 0;position:relative;overflow:hidden;
 background:radial-gradient(140% 40% at 50% 22%,#152030 0%,var(--bg) 70%)}
.ic{display:inline-flex;width:24px;height:24px;color:var(--ac);flex:none}.ic svg{width:100%;height:100%}
.ic .f{fill:currentColor;fill-opacity:.16;stroke:none}

.top{display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;flex-direction:column;direction:ltr;align-items:flex-start}
.wm{font-size:26px;font-weight:300;line-height:1}.wm b{font-weight:800;color:var(--ac)}
.wm-s{font-size:7.5px;letter-spacing:2.6px;color:var(--mut);margin-top:5px}
.tag{font-size:13px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:5px 12px}

.strap{margin-top:20px;padding-top:18px;border-top:1px solid var(--line)}
.strap h2{font-size:24px;line-height:1.25;font-weight:800;letter-spacing:-.3px}
.strap p{font-size:15px;line-height:1.6;color:var(--mut);margin-top:8px;font-weight:300}

.hero{position:relative;height:400px;margin-top:6px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:22px}
.spot{position:absolute;left:50%;top:50%;width:380px;height:380px;transform:translate(-50%,-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(150,195,235,.22) 0%,rgba(94,196,255,.07) 45%,transparent 70%)}
.hero img{position:relative;z-index:2;filter:drop-shadow(0 18px 22px rgba(0,0,0,.6))}
.home .hero img{height:360px}.biz .hero img{height:330px}
.floor{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);width:260px;height:26px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.75),transparent 70%)}

.title{text-align:center}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:15px;color:var(--mut)}
.eyebrow .dot{width:7px;height:7px;border-radius:50%;background:var(--ac);box-shadow:0 0 10px var(--ac)}
h1{display:flex;flex-direction:column;align-items:center;line-height:.95;margin-top:10px}
h1 .l1{font-size:20px;font-weight:300;letter-spacing:8px;color:var(--mut);padding-left:8px}
h1 .l2{font-size:66px;font-weight:800;letter-spacing:-2px;background:linear-gradient(180deg,#fff 30%,#b9c6d6);-webkit-background-clip:text;color:transparent;padding-bottom:4px}

.price{margin-top:18px;display:flex;flex-direction:column;align-items:center;padding:16px;border-radius:18px;
 border:1px solid rgba(94,196,255,.35);background:linear-gradient(135deg,rgba(94,196,255,.14),rgba(94,196,255,.03))}
.amt{font-size:50px;font-weight:800;letter-spacing:-1px;line-height:1;direction:ltr}
.cur{font-weight:400;color:var(--ac);margin-right:4px;font-size:.6em}
.vat{font-size:15px;color:var(--mut);margin-top:6px}

.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.stat{padding:16px;border:1px solid var(--line);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:6px}
.stat .lbl{font-size:14px;color:var(--dim);font-weight:500}
.flow-n{font-size:40px;font-weight:300;color:var(--ac);line-height:1;direction:ltr;text-align:right}
.flow-n small{font-size:14px;color:var(--mut);font-weight:500;margin-left:4px}
.stat b{font-size:19px;font-weight:700;line-height:1.2}
.stat .sub{font-size:14px;color:var(--mut);line-height:1.4}
.stat .ic{width:30px;height:30px}

.spec{margin-top:10px;padding:16px 18px;border:1px solid var(--line);border-radius:18px;background:var(--card);display:flex;gap:14px;align-items:flex-start}
.spec .ic{width:28px;height:28px;margin-top:2px}
.spec .lbl{font-size:14px;color:var(--dim);font-weight:500}
.spec .val{font-size:17px;line-height:1.55;margin-top:2px}

.sec{display:flex;align-items:center;gap:10px;margin:30px 0 12px}
.sec span{font-size:20px;font-weight:800;white-space:nowrap}
.sec em{font-style:normal;font-size:13px;color:var(--dim);white-space:nowrap}
.sec i{flex:1;height:1px;background:var(--line)}

.kit{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.kit-i{display:flex;flex-direction:column;gap:10px;padding:16px 14px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.025)}
.kit-i .ic{width:34px;height:34px;padding:8px;border-radius:12px;background:rgba(94,196,255,.10);box-sizing:content-box}
.kit-t{font-size:15.5px;line-height:1.4}

.tech{margin-top:16px;display:flex;gap:12px;align-items:flex-start;padding:16px 18px;border-radius:16px;background:rgba(94,196,255,.07);border:1px solid rgba(94,196,255,.2)}
.tech .ic{width:24px;height:24px;margin-top:2px}
.tech p{font-size:16px;line-height:1.5;color:var(--mut)}.tech b{color:var(--tx);font-weight:700;display:block}

.adds{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.add{display:flex;flex-direction:column;align-items:center;text-align:center;padding:14px 6px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
.add .ic{width:26px;height:26px;color:var(--mut)}
.add-t{font-size:13px;line-height:1.3;color:var(--mut);margin-top:8px;min-height:34px;display:flex;align-items:center}
.add-p{font-size:19px;font-weight:700;margin-top:4px;direction:ltr}

.demo{margin-top:30px;padding:18px;border-radius:18px;background:linear-gradient(135deg,#1b2a3c,#121822);border:1px solid rgba(94,196,255,.3);display:flex;gap:14px;align-items:center}
.demo .ic{width:34px;height:34px}
.demo b{font-size:19px;font-weight:800;display:block}.demo span{font-size:15px;color:var(--mut)}

.cta{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.btn{display:flex;align-items:center;justify-content:center;gap:9px;padding:15px 10px;border-radius:14px;font-size:17px;font-weight:700}
.btn .ic{width:22px;height:22px;color:inherit}
.btn.p{background:var(--ac);color:#06121d}
.btn.s{border:1px solid var(--line);background:var(--card)}
.phone{display:flex;justify-content:center;align-items:center;gap:10px;margin-top:14px;font-size:24px;font-weight:800;direction:ltr}
.phone .ic{width:22px;height:22px}
.web{display:block;text-align:center;font-size:16px;color:var(--mut);margin-top:6px;direction:ltr}
.end{height:30px}
'''

CSS += KIT_CSS_M

WA_ICON = '<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1.3-4A8 8 0 1 1 8.2 19z"/><path d="M9 9.2c.2 2.6 2.2 4.8 5 5.4l1-1.3-1.8-.9-.8.7c-.9-.3-1.9-1.3-2.2-2.2l.7-.8-.9-1.8z"/></svg></span>'

def page(p, show_adds=True):
    kit = "".join(f'<div class="kit-i">{ic(i)}<div class="kit-t">{t}</div></div>' for i, t in p["kit"])
    adds = "".join(f'<div class="add">{ic(i)}<div class="add-t">{t}</div><div class="add-p"><span class="cur">₪</span>{v:,}</div></div>' for i, t, v in ADDONS)
    pi, pt, ps = p["power"]
    adds_block = (f'<div class="sec"><span>תוספות מומלצות</span><i></i></div><div class="adds">{adds}</div>') if show_adds else ''
    return f'''
<section class="page {p["kind"]}">
  <header class="top">
    <div class="brand"><span class="wm">Gal<b>CLEAN</b></span><span class="wm-s">WINDOW CLEANING SOLUTION</span></div>
    <span class="tag">{"ערכה ביתית" if p["kind"]=="home" else "ערכה לעסקים"}</span>
  </header>
  <div class="strap">
    <h2>מהיום כל אחד מנקה חלונות כמו מקצוען</h2>
    <p>מכשירי אוסמוזה הפוכה פרטיים יחידים מסוגם בישראל, לניקוי קירות מסך, מעקות זכוכית, אלומיניום, תריסים, רפפות, צלונים, מראות ודלתות. מתאימים מכשיר לפי הצורך ומוט לפי הגובה הדרוש.</p>
  </div>

  <div class="hero"><div class="spot"></div><img src="{p["img"]}"><div class="floor"></div></div>

  <div class="title">
    <div class="eyebrow"><span class="dot"></span>{p["sub"]}</div>
    <h1 dir="ltr"><span class="l1">{p["line"]}</span><span class="l2">{p["name"]}</span></h1>
  </div>
  <div class="price"><div class="amt"><span class="cur">₪</span>{p["price"]}</div><div class="vat">המחיר כולל מע"מ</div></div>

  <div class="stats">
    <div class="stat"><span class="lbl">עוצמת מים</span><div class="flow-n">{p["flow"]}<small>L/min</small></div><span class="sub">{p["flow"]} ליטר לדקה</span></div>
    <div class="stat">{ic(pi)}<b>{pt}</b><span class="sub">{ps}</span></div>
  </div>
  <div class="spec">{ic("home")}<div><div class="lbl">מתאים ל</div><div class="val">{p["fit"]}</div></div></div>
  <div class="spec">{ic("spark")}<div><div class="lbl">שימושים</div><div class="val">{p["use"]}</div></div></div>

  <div class="sec"><span>מה מגיע בערכה</span><i></i></div>
  {kit_html(p, ic, "m")}

  <div class="tech">{ic("drop")}<p><b>מים מזוקקים באוסמוזה הפוכה</b>מנקים בלי סבון, בלי ניגוב ובלי ייבוש ידני.</p></div>


  {'' if p['name']=='Lite' else '<div class="demo">'+ic("demo")+'<div><b>הדגמה בבית הלקוח: 99 ₪</b><span>הסכום מנוכה במלואו מהרכישה</span></div></div>'}
  <div class="cta">
    <a class="btn p" href="{WA}">{WA_ICON}וואטסאפ</a>
    <a class="btn s" href="{TEL}">{ic("phone")}חיוג</a>
  </div>
  <a class="phone" href="{TEL}">{ic("phone")}073-3744487</a>
  <a class="web" href="{WEB}">galclean.co.il</a>
  {adds_block}
  <div class="end"></div>
</section>'''

def html(p, show_adds=True):
    return f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=430"><title>GalClean {p["line"]} {p["name"]}</title><style>{faces}{CSS}</style></head><body>{page(p, show_adds)}</body></html>'

for i, p in enumerate(PAGES):
    n = f"{p['line']}-{p['name']}"
    (W / f"m_{n}.html").write_text(html(p, True), encoding="utf-8")              # standalone: add-ons on the page
    (W / f"mc_{n}.html").write_text(html(p, i == len(PAGES)-1), encoding="utf-8")  # combined: add-ons on last page only
print("ok")
