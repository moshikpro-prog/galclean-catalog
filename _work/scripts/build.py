import base64, pathlib
W = pathlib.Path(__file__).parent
FD = W / "node_modules/@fontsource/heebo/files"

def b64(p): return base64.b64encode(p.read_bytes()).decode()

faces = ""
for wt in (300, 400, 500, 700, 800):
    for sub, rng in (("hebrew", "U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F"), ("latin", "U+0000-00FF,U+2000-206F,U+2190-21FF")):
        faces += f"@font-face{{font-family:'Heebo';font-weight:{wt};src:url(data:font/woff2;base64,{b64(FD/f'heebo-{sub}-{wt}-normal.woff2')}) format('woff2');unicode-range:{rng};}}\n"

IMG_HOME = "data:image/png;base64," + b64(W / "a_final3.png")
IMG_BIZ = "data:image/png;base64," + b64(W / "b_final3.png")

# ---------- icons (24x24 line, stroke=currentColor) ----------
S = 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
 "device": f'<svg viewBox="0 0 24 24" {S}><rect x="6" y="3" width="12" height="18" rx="2.2"/><rect x="8.6" y="5.6" width="6.8" height="12.8" rx="1"/><path d="M10.5 8h3"/><circle cx="12" cy="15.6" r=".6" fill="currentColor"/></svg>',
 "reel": f'<svg viewBox="0 0 24 24" {S}><circle cx="12" cy="11" r="6.2"/><circle cx="12" cy="11" r="1.6"/><path d="M12 4.8v4.6M12 12.6v4.6M5.8 11h4.6M13.6 11h4.6"/><path d="M8 19.5h8M9.5 17l-1.5 2.5M14.5 17l1.5 2.5"/><path d="M18.2 11c2 .3 3 1.6 3 3.4"/></svg>',
 "head": f'<svg viewBox="0 0 24 24" {S}><rect x="2.5" y="12" width="19" height="3.6" rx="1"/><path d="M4 15.6v2.4M7 15.6v2.4M10 15.6v2.4M14 15.6v2.4M17 15.6v2.4M20 15.6v2.4"/><path d="M12 12V8.5"/><path d="M10.4 8.5h3.2l-.6-5h-2z"/></svg>',
 "pole": f'<svg viewBox="0 0 24 24" {S}><path d="M7 20.5 17.5 3.5"/><path d="M5.8 22.4l1.9-3.1"/><path d="M9.1 17.2l1.6.95M12.2 12.2l1.6.95M15.1 7.5l1.4.85"/><path d="M16.6 2.2l2.6 1.6"/></svg>',
 "trolley": f'<svg viewBox="0 0 24 24" {S}><path d="M8 3.5h2.5L13 18"/><path d="M13 18h7"/><rect x="11.5" y="7.5" width="7" height="7.5" rx="1" transform="rotate(-10 15 11)"/><circle cx="12.4" cy="20" r="1.6"/></svg>',
 "tds": f'<svg viewBox="0 0 24 24" {S}><rect x="7" y="2.5" width="10" height="14" rx="2"/><rect x="9" y="5" width="6" height="4" rx=".6"/><path d="M10 12h4"/><path d="M10.5 16.5v3.2a1.5 1.5 0 0 0 3 0v-3.2"/></svg>',
 "brush": f'<svg viewBox="0 0 24 24" {S}><path d="M3 21 11 13"/><rect x="10" y="4" width="10" height="9" rx="2" transform="rotate(45 15 8.5)"/><path d="M14.2 6.6l3.2 3.2M12.6 8.2l3.2 3.2M15.8 5l3.2 3.2"/></svg>',
 "connect": f'<svg viewBox="0 0 24 24" {S}><path d="M3 12h4"/><rect x="7" y="9" width="4.2" height="6" rx="1"/><path d="M11.2 10.5h1.6v3h-1.6"/><rect x="12.8" y="9" width="4.2" height="6" rx="1"/><path d="M17 12h4"/></svg>',
 "mat": f'<svg viewBox="0 0 24 24" {S}><path d="M3 15.5 8 8.5h13l-5 7z"/><path d="M6.5 12h8.8M5 14h9.6M8.6 10h8.4"/><path d="M12 3.5c-.9 1.3-1.4 2-1.4 2.7a1.4 1.4 0 0 0 2.8 0c0-.7-.5-1.4-1.4-2.7z"/></svg>',
 "filter": f'<svg viewBox="0 0 24 24" {S}><rect x="4" y="4" width="4.4" height="16" rx="1.6"/><rect x="9.8" y="4" width="4.4" height="16" rx="1.6"/><rect x="15.6" y="4" width="4.4" height="16" rx="1.6"/><path d="M4 8h4.4M9.8 8h4.4M15.6 8h4.4"/></svg>',
 "pad": f'<svg viewBox="0 0 24 24" {S}><rect x="3" y="8" width="18" height="8" rx="2"/><path d="M5.5 10.5c1 1 2 1 3 0s2-1 3 0 2 1 3 0 2-1 3 0M5.5 13.5c1 1 2 1 3 0s2-1 3 0 2 1 3 0 2-1 3 0"/></svg>',
 "drop": f'<svg viewBox="0 0 24 24" {S}><path d="M12 3c-3.2 4.4-5.4 7.3-5.4 10.1a5.4 5.4 0 0 0 10.8 0C17.4 10.3 15.2 7.4 12 3z"/><path d="M9.6 13.6a2.5 2.5 0 0 0 2.4 2.4"/></svg>',
 "plug": f'<svg viewBox="0 0 24 24" {S}><path d="M9 3v4M15 3v4"/><path d="M7 7h10v3.5a5 5 0 0 1-10 0z"/><path d="M12 15.5V21"/></svg>',
 "noplug": f'<svg viewBox="0 0 24 24" {S}><path d="M9 3v4M15 3v4"/><path d="M7 7h10v3.5a5 5 0 0 1-10 0z"/><path d="M12 15.5V21"/><path d="M4 4l16 16"/></svg>',
 "home": f'<svg viewBox="0 0 24 24" {S}><path d="M3.5 10.5 12 4l8.5 6.5"/><path d="M5.5 9v11h13V9"/><rect x="9.5" y="12" width="5" height="4.5" rx=".4"/><path d="M12 12v4.5M9.5 14.2h5"/></svg>',
 "spark": f'<svg viewBox="0 0 24 24" {S}><path d="M12 3.5l1.8 5.2 5.2 1.8-5.2 1.8L12 17.5l-1.8-5.2L5 10.5l5.2-1.8z"/><path d="M18.5 16.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/></svg>',
 "phone": f'<svg viewBox="0 0 24 24" {S}><path d="M6.6 3.5h2.6l1.4 4-2 1.4a10.5 10.5 0 0 0 6.5 6.5l1.4-2 4 1.4v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/></svg>',
 "globe": f'<svg viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.4 3.4 5.3 3.4 8.5s-1 6.1-3.4 8.5c-2.4-2.4-3.4-5.3-3.4-8.5s1-6.1 3.4-8.5z"/></svg>',
 "demo": f'<svg viewBox="0 0 24 24" {S}><path d="M3.5 10.5 12 4l8.5 6.5"/><path d="M5.5 9v11h13V9"/><path d="M9.3 14.2l1.9 1.9 3.7-3.9"/></svg>',
 "wheel": f'<svg viewBox="0 0 24 24" {S}><rect x="5" y="3.5" width="14" height="13" rx="2"/><path d="M9 3.5V2M15 3.5V2"/><circle cx="8" cy="19.5" r="1.6"/><circle cx="16" cy="19.5" r="1.6"/></svg>',
}
from icons import ICONS2
from kitphotos import kit_html, video_html, KIT_CSS_A4, KIT_CSS_M, IMG as KIMG
ICONS.update(ICONS2)
ICONS['flatbrush'] = f'<img src="{KIMG["bluebrush"]}" alt="">'
def ic(n): return f'<span class="ic">{ICONS[n]}</span>'

# ---------- data ----------
ADDONS = [  # catalog prices incl. VAT, rounded to whole shekel
 ("pole", "מוט קרבון 6 מ'", 1475),
 ("pole", "מוט קרבון 4 מ'", 1021),
 ("pole", "מוט פיברגלס 5.5 מ'", 708),
 ("pole", "מוט פיברגלס 4.2 מ'", 472),
 ("flatbrush", "מברשת לניקוי חיפויים וגדרות", 500),
 ("mat", "שטיח לספיגה", 350),
 ("filter", "סט פילטרים", 266),
 ("tds", "מד TDS", 177),
 ("pad", "מיקרופייבר להחלפה", 65),
]

PAGES = [
 dict(num="01", line="GALHOME", name="Lite", sub="ערכה לניקוי חלונות ומרפסות", price="2,950", img=IMG_HOME, kind="home",
      flow="1", power=("noplug", "ללא חשמל", "ללא משאבה, ללא חיבור לחשמל"),
      fit="דירות, מרפסות ובתים",
      use="פתרון מהיר לבעלי בתים לניקוי חלונות ומרפסות. עד מפלס אחד.",
      kit=[("device","מכשיר אוסמוזה הפוכה"),("reel","תוף עם 20 מ' צינור הזרמת מים"),("head","ראש לניקוי חלונות 25 ס\"מ"),("pole","מוט לעבודה עד 4 מטר")]),
 dict(num="02", line="GALHOME", name="Plus", sub="ערכה לניקוי בתים פרטיים ופנטהאוזים", price="4,450", img=IMG_HOME, kind="home",
      flow="1.5", power=("plug", "משאבה חשמלית", "עוצמת מים גבוהה יותר"),
      fit="בתים פרטיים עם חלונות גדולים ופנטהאוזים",
      use="ניקוי חלונות גדולים יותר, משטחים חלקים ומעקות ארוכים.",
      kit=[("device","מכשיר אוסמוזה הפוכה עם משאבה"),("reel","תוף עם 50 מ' צינור הזרמת מים"),("head","ראש מקצועי לניקוי חלונות 35 ס\"מ"),("pole","מוט לעבודה עד 4 מטר")]),
 dict(num="03", line="GALPRO", name="Business", sub="ערכה לניקוי בתי עסק קטנים", price="5,900", img=IMG_BIZ, kind="biz",
      flow="2", power=("plug", "משאבה חשמלית", "מאפשר ניוד קל"),
      fit="עסקים קטנים, כמו מסעדות, לוביים קטנים וחנויות",
      use="ניקוי ויטרינות, סגירות חורף ולוביים, עם ניוד קל. מתאים להסרת לכלוך קל עד בינוני.",
      kit=[("device","מכשיר אוסמוזה הפוכה עם משאבה"),("reel","תוף עם 50 מ' צינור הזרמת מים"),("head","ראש מקצועי לניקוי חלונות 35 ס\"מ"),("pole","מוט לעבודה עד 4 מטר"),("trolley","עגלה לניידות"),("tds","מד TDS דיגיטלי"),("brush","מברשת לניקוי רפרפות וצלונים"),("connect","סט מחברי מים מהירים")]),
]

def page(p):
    kit = "".join(f'<div class="kit-i">{ic(i)}<div class="kit-t">{t}</div></div>' for i, t in p["kit"])
    adds = "".join(f'<div class="add">{ic(i)}<div class="add-t">{t}</div><div class="add-p"><span class="cur">₪</span>{v:,}</div></div>' for i, t, v in ADDONS)
    pi, pt, ps = p["power"]
    return f'''
<section class="page {p["kind"]}">
  <div class="glow"></div>
  <header class="top">
    <div class="brand"><span class="wm">Gal<b>CLEAN</b></span><span class="wm-s">WINDOW CLEANING SOLUTION</span></div>
    <div class="pager"><span>{p["num"]}</span><i></i><span>03</span></div>
  </header>
  <div class="strap">
    <h2>מהיום כל אחד מנקה חלונות כמו מקצוען</h2>
    <p>מכשירי אוסמוזה הפוכה פרטיים יחידים מסוגם בישראל, לניקוי קירות מסך, מעקות זכוכית, אלומיניום, תריסים, רפפות, צלונים, מראות ודלתות. מתאימים מכשיר לפי הצורך ומוט לפי הגובה הדרוש.</p>
  </div>

  <div class="hero">
    <div class="h-text">
      <div class="eyebrow"><span class="dot"></span>{p["line"]} · {p["sub"]}</div>
      <h1 dir="ltr"><span class="l1">{p["line"]}</span><span class="l2">{p["name"]}</span></h1>
      <div class="price"><div class="amt" dir="ltr"><span class="cur">₪</span>{p["price"]}</div><div class="vat">המחיר כולל מע"מ</div></div>
      <div class="flow">
        <div class="flow-n" dir="ltr">{p["flow"]}<small>L/min</small></div>
        <div class="flow-t"><b>עוצמת מים</b><span>{p["flow"]} ליטר לדקה</span></div>
      </div>
      <div class="pwr">{ic(pi)}<div><b>{pt}</b><span>{ps}</span></div></div>
    </div>
    <div class="h-img"><div class="spot"></div><img src="{p["img"]}"><div class="floor"></div></div>
  </div>

  <div class="specs">
    <div class="spec">{ic("home")}<div><div class="lbl">מתאים ל</div><div class="val">{p["fit"]}</div></div></div>
    <div class="spec">{ic("spark")}<div><div class="lbl">שימושים</div><div class="val">{p["use"]}</div></div></div>
  </div>

  <div class="kit">
    <div class="sec"><span>מה מגיע בערכה</span><i></i></div>
    {kit_html(p, ic, "a4")}
  </div>

  <div class="tech">{ic("drop")}<span><b>מים מזוקקים באוסמוזה הפוכה.</b> מנקים בלי סבון, בלי ניגוב ובלי ייבוש ידני.</span></div>

  <div class="adds">
    <div class="sec"><span>תוספות מומלצות</span><i></i></div>
    <div class="add-g">{adds}</div>
  </div>

  <footer class="foot">
    {'' if p['name']=='Lite' else '<div class="demo">'+ic("demo")+'<div><b>הדגמה בבית הלקוח: 99 ₪</b><span>הסכום מנוכה במלואו מהרכישה</span></div></div>'}
    <div class="contact">
      <div>{ic("phone")}<span dir="ltr">073-3744487</span><em>טלפון / וואטסאפ</em></div>
      <div>{ic("globe")}<span dir="ltr">galclean.co.il</span></div>
    </div>
  </footer>
</section>'''

CSS = r'''
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0c10;--card:#12151b;--line:rgba(255,255,255,.09);--tx:#f3f5f8;--mut:#9aa3b2;--dim:#6b7383;--ac:#5ec4ff;--ac2:#2f8fe0}
html,body{background:var(--bg)}
body{font-family:'Heebo',sans-serif;color:var(--tx);direction:rtl;-webkit-font-smoothing:antialiased}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:30px 44px 0;display:flex;flex-direction:column;
 background:radial-gradient(120% 70% at 25% 30%,#141a24 0%,var(--bg) 60%)}
.page:last-child{page-break-after:auto}
.glow{position:absolute;inset:0;pointer-events:none;background:radial-gradient(50% 30% at 22% 32%,rgba(94,196,255,.10),transparent 70%)}
.ic{display:inline-flex;width:22px;height:22px;color:var(--ac);flex:none}.ic svg{width:100%;height:100%}.ic .f{fill:currentColor;fill-opacity:.16;stroke:none}

.top{display:flex;justify-content:space-between;align-items:center;position:relative}
.brand{display:flex;flex-direction:column;direction:ltr;align-items:flex-start}
.wm{font-size:24px;font-weight:300;letter-spacing:.2px;line-height:1}.wm b{font-weight:800;color:var(--ac)}
.wm-s{font-size:6.6px;letter-spacing:2.6px;color:var(--mut);margin-top:4px}
.pager{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--mut);direction:ltr;font-weight:500;letter-spacing:1px}
.pager span:first-child{color:var(--tx)}.pager i{width:26px;height:1px;background:var(--line)}

.strap{margin-top:18px;padding:13px 0 13px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);position:relative}
.strap h2{font-size:17px;font-weight:700;letter-spacing:-.1px}
.strap p{font-size:10.6px;line-height:1.55;color:var(--mut);margin-top:3px;font-weight:300}

.hero{display:grid;grid-template-columns:1fr 1.05fr;gap:10px;height:412px;position:relative;margin-top:6px}
.h-text{display:flex;flex-direction:column;justify-content:center;padding-top:6px}
.eyebrow{font-size:10.5px;color:var(--mut);display:flex;align-items:center;gap:8px;font-weight:400}
.eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--ac);box-shadow:0 0 10px var(--ac)}
h1{display:flex;flex-direction:column;align-items:flex-end;line-height:.95;margin-top:12px}
h1 .l1{font-size:23px;font-weight:300;letter-spacing:7px;color:var(--mut)}
h1 .l2{font-size:68px;font-weight:800;letter-spacing:-2px;background:linear-gradient(180deg,#fff 30%,#b9c6d6);-webkit-background-clip:text;color:transparent;padding-bottom:4px}
.price{margin-top:20px;display:flex;align-items:baseline;gap:12px}
.amt{font-size:40px;font-weight:700;letter-spacing:-1px;line-height:1}
.amt .cur,.add-p .cur{font-weight:400;color:var(--ac);margin-right:3px;font-size:.62em}
.vat{font-size:10.5px;color:var(--mut)}
.flow{margin-top:24px;display:flex;align-items:center;gap:14px;padding:12px 16px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(135deg,rgba(94,196,255,.08),rgba(255,255,255,.015))}
.flow-n{font-size:34px;font-weight:300;line-height:1;color:var(--ac);display:flex;align-items:baseline;gap:5px}
.flow-n small{font-size:10px;color:var(--mut);font-weight:500;letter-spacing:.5px}
.flow-t{display:flex;flex-direction:column;border-right:1px solid var(--line);padding-right:14px}
.flow-t b{font-size:12px;font-weight:600}.flow-t span{font-size:10.5px;color:var(--mut)}
.pwr{margin-top:10px;display:flex;align-items:center;gap:12px;padding:10px 16px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.015)}
.pwr div{display:flex;flex-direction:column}.pwr b{font-size:12px;font-weight:600}.pwr span{font-size:10.5px;color:var(--mut)}

.h-img{position:relative;display:flex;align-items:flex-end;justify-content:center;padding-bottom:26px}
.spot{position:absolute;left:50%;top:48%;width:360px;height:360px;transform:translate(-50%,-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(150,190,230,.20) 0%,rgba(94,196,255,.06) 45%,transparent 70%)}
.h-img img{position:relative;z-index:2;filter:drop-shadow(0 18px 24px rgba(0,0,0,.55))}
.home .h-img img{height:370px}
.biz .h-img img{height:312px}
.biz .hero{height:362px}
.biz .kit{margin-top:12px}
.floor{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);width:270px;height:26px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.7),transparent 70%);z-index:1}

.specs{margin-top:4px;display:grid;grid-template-columns:1fr 1.25fr;gap:10px;position:relative}
.spec{display:flex;gap:12px;align-items:flex-start;padding:13px 16px;background:var(--card);border:1px solid var(--line);border-radius:14px}
.lbl{font-size:10px;color:var(--dim);letter-spacing:.4px;font-weight:500}
.val{font-size:12px;line-height:1.5;margin-top:2px;font-weight:400}

.sec{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.sec span{font-size:12px;font-weight:700;white-space:nowrap}
.sec em{font-style:normal;font-size:9.5px;color:var(--dim);white-space:nowrap}
.sec i{flex:1;height:1px;background:var(--line)}
.kit{margin-top:16px;position:relative}
.kit-g{display:grid;gap:8px}
.kit-g.n4{grid-template-columns:repeat(4,1fr)}
.kit-g.n8{grid-template-columns:repeat(4,1fr)}
.kit-i{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.02)}
.kit-i .ic{width:28px;height:28px;padding:5px;border-radius:9px;background:rgba(94,196,255,.09);box-sizing:content-box}
.kit-t{font-size:10.4px;line-height:1.35}
.n4 .kit-i{flex-direction:column;align-items:flex-start;padding:13px 13px;min-height:92px}
.n4 .kit-i .ic{width:30px;height:30px}
.n4 .kit-t{font-size:11px;margin-top:4px}

.tech{margin-top:12px;display:flex;align-items:center;gap:10px;font-size:10.8px;color:var(--mut);position:relative}
.tech b{color:var(--tx);font-weight:600}
.tech .ic{width:18px;height:18px}

.adds{margin-top:auto;padding-top:14px;position:relative}
.add-g{display:grid;grid-template-columns:repeat(9,1fr);border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--card)}
.add{display:flex;flex-direction:column;align-items:center;text-align:center;padding:11px 4px 10px;border-left:1px solid var(--line)}
.add:last-child{border-left:0}
.add .ic{width:20px;height:20px;color:var(--mut)}
.add-t{font-size:8.6px;line-height:1.3;color:var(--mut);margin-top:6px;min-height:22px;display:flex;align-items:center}
.add-p{font-size:13px;font-weight:700;margin-top:4px;direction:ltr}

.foot{margin:14px -44px 0;padding:14px 44px 18px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,.25);position:relative}
.demo{display:flex;align-items:center;gap:10px}.demo div{display:flex;flex-direction:column}
.demo b{font-size:12px;font-weight:600}.demo span{font-size:10px;color:var(--mut)}
.contact{display:flex;gap:22px}
.contact div{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:600}
.contact em{font-style:normal;font-size:9.5px;color:var(--dim);font-weight:400}
.contact .ic{width:16px;height:16px}
'''

CSS += KIT_CSS_A4 + '.foot:has(> :only-child){justify-content:center}'
html = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>GalClean — ערכות GALHOME ו-GALPRO Business</title><style>{faces}{CSS}</style></head><body>{"".join(page(p) for p in PAGES)}</body></html>'
(W / "catalog.html").write_text(html, encoding="utf-8")
print("ok", len(html)//1024, "KB")
