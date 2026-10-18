"""Full mobile catalogue: home line (Lite/Plus/Business) + professional line (Expert/Turbo/Ultra).
Builds two orders: A = home first, B = professional first."""
import base64, io, pathlib, sys
from PIL import Image
import build_mobile as bm
import build_combined as bc
from build import faces, ic, ICONS, PAGES as HOME
from proicons import PRO_ICONS

ICONS.update(PRO_ICONS)
HOME = [dict(q) for q in HOME]
for q in HOME:
    q["fit_short"] = q["fit"]
_b = HOME[2]
_b["sub"] = "ערכה לבתי עסק קטנים ולבתים גדולים"
_b["fit"] = "עסקים קטנים, כמו מסעדות, לוביים קטנים וחנויות, וגם בתים פרטיים ופנטהאוזים גדולים"
_b["fit_short"] = "עסקים קטנים, וגם בתים פרטיים ופנטהאוזים גדולים עם הרבה חלונות"
BUS_HOME = ("גם לבית פרטי", "לבתים פרטיים ופנטהאוזים גדולים עם הרבה חלונות או חלונות גבוהים. עוצמת מים של 2 ליטר לדקה, הגבוהה מבין הדגמים לבית ולעסק, מקצרת את זמן הניקוי של שטחי זכוכית גדולים. לחלונות גבוהים במיוחד אפשר לשלב מוט ארוך יותר מהתוספות.")
ICONS["reel_al"] = ICONS["reel"]
W = pathlib.Path(__file__).parent

def uri(path, h):
    im = Image.open(W / path); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

PRO = [
 dict(line="GALPRO", name="Expert", kind="pro", price="9,000", flow="4",
      sub="פתרון מקצועי ואמין לעסקים בינוניים ועבודה בגובה",
      img=uri("expert_final.png", 760), th=uri("expert_final.png", 300),
      power=("crew", "מנקה אחד", "צוות עבודה"),
      fit="חברות ניהול/ניקיון בינוניות, מלונות",
      use="עד גובה 4 קומות. ניקוי חלונות גדולים, ויטרינות ומבני זכוכית.",
      dims=None,
      kit=[("device", "מכשיר אוסמוזה הפוכה"), ("reel", "תוף עם 50 מ' צינור הזרמת מים"),
           ("head", 'ראש לניקוי חלונות 45 ס"מ'), ("pole", "מוט לעבודה עד 4 מטר"),
           ("trolley", "עגלה לניידות"), ("tds", "מד דיגיטלי TDS"),
           ("brush", "מברשת לניקוי רפרפות וצלונים")]),
 dict(line="GALPRO", name="Turbo", kind="pro", price="12,500", flow="6.5",
      sub="פתרון מקצועי לבנייני משרדים ומתחמי זכוכית",
      img=uri("turbo_final.png", 760), th=uri("turbo_final.png", 300),
      power=("crew", "2 מנקים במקביל", "צוות עבודה"),
      fit="בנייני משרדים, חברות ניקיון גדולות, וילות ואחוזות",
      use='<ul class="ul"><li>פרויקטים בגובה של עד 6 קומות</li><li>עבודה של 2 מנקים במקביל</li><li>ניקוי יעיל של צלונים / תריסים / חיפויים שחורים</li></ul>',
      dims="L/W/H 48x34x57cm, 35kg",
      kit=[("device", "מכשיר אוסמוזה הפוכה"), ("reel", "גלגלת עם 50 מ' צינור הזרמת מים"),
           ("head", 'ראש מקצועי לניקוי חלונות 55 ס"מ'), ("pole", "מוט לעבודה עד 4 מטר"),
           ("brush", "מברשת לניקוי רפרפות וצלונים"), ("tds", "מד דיגיטלי TDS"),
           ("trolley", "עגלה לניידות")]),
 dict(line="GALPRO", name="Ultra", kind="pro", price="18,000", flow="9",
      sub="לקומפלקסים ובנייני ענק לניקיון עד גובה 20 מ'",
      img=uri("ultra_final.png", 760), th=uri("ultra_final.png", 300),
      power=("crew", "3 מנקים במקביל", "צוות עבודה"),
      fit="מתחמי משרדים, חברות אחזקה",
      use='<ul class="ul"><li>פרויקטים בגובה של עד 6 קומות</li><li>עבודה של 3 מנקים במקביל</li><li>ניקוי חיצוני בקנה מידה גדול, כולל מבנים תעשייתיים</li></ul>',
      dims="L/W/H 54x38x57cm, 40kg",
      kit=[("device", "מכשיר אוסמוזה הפוכה"), ("reel_al", "תוף אלומיניום עם 50 מ' צינור הזרמת מים"),
           ("head", 'ראש מקצועי לניקוי חלונות 55 ס"מ'), ("pole", "מוט לעבודה עד 4 מטר, 2 יח'"),
           ("reel_al", "תוף אלומיניום עם 100 מ' צינור הזרמת מים"),
           ("head", 'ראש מקצועי לניקוי חלונות 35 ס"מ'), ("head", 'ראש מקצועי לניקוי חלונות 20 ס"מ'),
           ("trolley", "עגלה לניידות"), ("brush", "מברשת לניקוי תריסים, גדרות ואלומיניום"),
           ("tds", "מד דיגיטלי TDS")]),
]

# professional add-ons: price-list (catalogue) values, before VAT, rounded
ADDONS_PRO = [
 ("pole", "מוט פיברגלס 7.6 מ'", 750), ("pole", "מוט קרבון 8 מ'", 1750), ("pole", "מוט קרבון 10 מ'", 2500),
 ("pole", "מוט קרבון 12 מ'", 3100), ("pole", "מוט קרבון 13.5 מ'", 3900), ("pole", "מוט קרבון 15.5 מ'", 5900),
 ("pole", "מוט קרבון 18 מ'", 8500), ("modular", "מוט קרבון מודולרי עד 20 מ', ליח' של 1.8 מ'", 680),
 ("filter", "סט פילטרים Expert", 350), ("filter", "סט פילטרים Turbo", 650), ("filter", "סט פילטרים Ultra", 550),
 ("softener", "מרכך מים 5 ל'", 3000), ("softener", "מרכך מים 8 ל'", 4000),
 ("sprayer", "מרסס נייד 45 ל'", 3100), ("sprayer", "מרסס 20 ל'", 390),
 ("blade", "GALBLADE סכין מקצועית לחלון", 750),
 ("squeegee", "High Flyer 35", 330), ("squeegee", "High Flyer 45", 380), ("fiberbrush", "מברשת סיבים", 425),
]

EXTRA2 = r'''
.pro .hero img{height:330px}
.ul{margin:2px 0 0;padding:0 18px 0 0}.ul li{margin:3px 0}
.spec.hl{border-color:rgba(94,196,255,.4);background:linear-gradient(135deg,rgba(94,196,255,.12),rgba(255,255,255,.02))}
.spec.hl .lbl{color:var(--ac);font-weight:700}
.hl3{color:var(--tx);font-weight:700}
.pvnote{font-size:14px;color:var(--mut);margin:-4px 0 12px}
.pvl{font-size:12px;color:var(--mut);margin-top:3px}
.next .tp small{font-size:12px;color:var(--mut);font-weight:500;margin-right:6px}
.mc .pr small{font-size:11px;color:var(--mut);font-weight:500;margin-right:4px}
.bar{grid-template-columns:repeat(3,1fr)}
.bar .grp{grid-column:1/-1;font-size:12px;color:var(--dim);margin:4px 2px -2px}
.xsec{margin-top:22px;display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;padding:16px 18px;border-radius:18px;
 border:1px solid rgba(94,196,255,.3);background:linear-gradient(135deg,rgba(94,196,255,.10),rgba(255,255,255,.02))}
.xsec .k{font-size:13px;color:var(--ac);font-weight:700}
.xsec b{display:block;font-size:18px;font-weight:800;margin-top:3px;line-height:1.3}
.xsec span.s{display:block;font-size:14px;color:var(--mut);margin-top:3px;direction:ltr;text-align:right}
.xsec .th3{display:flex;align-items:flex-end;gap:2px}.xsec .th3 img{height:58px;filter:drop-shadow(0 6px 8px rgba(0,0,0,.6))}
'''
VIA = 'לפני מע"מ'

def pro_adds_block():
    adds = "".join(f'<div class="add">{ic(i)}<div class="add-t">{t}</div><div class="add-p"><span class="cur">₪</span>{v:,}</div></div>' for i, t, v in ADDONS_PRO)
    return f'<div class="sec"><span>תוספות מומלצות לקו המקצועי</span><i></i></div><div class="pvnote">המחירים {VIA}</div><div class="adds">{adds}</div>'

def home_adds_block():
    from build import ADDONS
    adds = "".join(f'<div class="add">{ic(i)}<div class="add-t">{t}</div><div class="add-p"><span class="cur">₪</span>{v:,}</div></div>' for i, t, v in ADDONS)
    return f'<div class="sec"><span>תוספות מומלצות</span><i></i></div><div class="adds">{adds}</div>'

def pro_page_html(p):
    h = bm.page(p, show_adds=False)
    h = h.replace('<div class="vat">המחיר כולל מע"מ</div>', f'<div class="vat">המחיר {VIA}</div>')
    h = h.replace('<span class="tag">ערכה לעסקים</span>', '<span class="tag">ערכה מקצועית</span>')
    h = h.replace("הדגמה בבית הלקוח", "הדגמה במקום הלקוח")
    if p.get("dims"):
        anchor = '<div class="sec"><span>מה מגיע בערכה</span>'
        dims = f'<div class="spec">{ic("ruler")}<div><div class="lbl">מידות ומשקל</div><div class="val" dir="ltr" style="text-align:right">{p["dims"]}</div></div></div>\n  '
        h = h.replace(anchor, dims + anchor, 1)
    return h

TH = {p["name"]: bc.TH[p["kind"]] for p in HOME}
TH.update({p["name"]: p["th"] for p in PRO})

def cards(models, start_idx, pro):
    out = ""
    for k, p in enumerate(models):
        pv = ""
        out += f'''
  <div class="mc" data-goto="{start_idx+k}">
    <span class="num">{k+1}</span>
    <div class="th"><img src="{TH[p["name"]]}"></div>
    <div class="bd">
      <div class="ln">{p["line"]}</div><div class="nm">{p["name"]}</div>
      <div class="fit">{p.get("fit_short", p["fit"])}</div>
      <div class="row"><span class="pr"><span class="cur">₪</span>{p["price"]}{pv}</span><span class="fl">{p["flow"]} ל'/דקה</span></div>
      {f'<div class="pvl">{VIA}</div>' if pro else ''}
      <div class="go">לכל הפרטים ←</div>
    </div>
  </div>'''
    return out

def xsec(target_idx, pro_target):
    if pro_target:
        k, b, s, names = "קו מקצועי", "לחברות ניקיון, ניהול ואחזקה ולפרויקטים גדולים", "Expert · Turbo · Ultra", ["Expert", "Turbo", "Ultra"]
    else:
        k, b, s, names = "לבית ולעסק", "לדירות, בתים פרטיים ועסקים קטנים", "Lite · Plus · Business", ["Lite", "Plus", "Business"]
    th = "".join(f'<img src="{TH[n]}">' for n in names)
    return f'<div class="xsec" data-goto="{target_idx}"><div><div class="k">גם במסמך הזה · {k}</div><b>{b}</b><span class="s">{s}</span><div class="go" style="font-size:14px;font-weight:700;color:var(--ac);margin-top:6px">למעבר ←</div></div><div class="th3">{th}</div></div>'

def home_cover(first_idx, other_cover_idx):
    return f'''
<section class="page cover">
  <header class="top">
    <div class="brand"><span class="wm">Gal<b>CLEAN</b></span><span class="wm-s">WINDOW CLEANING SOLUTION</span></div>
    <span class="tag">ערכות לבית ולעסק</span>
  </header>
  <h2 class="cv-h">מהיום כל אחד מנקה חלונות <em>כמו מקצוען</em></h2>
  <p class="cv-p">מי ברז מכילים מינרלים. כשהמים מתייבשים על הזכוכית המינרלים נשארים, ואלה הסימנים והכתמים הלבנים שאתם רואים גם אחרי שניקיתם את החלון. מכשירי האוסמוזה ההפוכה שלנו, יחידים מסוגם בישראל לשימוש פרטי, מזקקים את מי הברז עד 0 מינרלים, ומים מזוקקים מתייבשים מעצמם בלי להשאיר סימן. כך מנקים <b class="hl3">בלי סבון, בלי ניגוב ובלי ייבוש</b>, ועם מוט מהקרקע מגיעים בלי סולם לחלונות, קירות מסך, מעקות זכוכית, תריסים, רפפות וצלונים.</p>
  <div class="cv-lbl"><b>איזה מכשיר מתאים לכם?</b><i></i></div>
  {cards(HOME, first_idx, False)}
  <div class="cv-note">המחירים כוללים מע"מ · הקישו על דגם כדי לעבור אליו</div>
  <div class="scroll"><span>גללו למטה לפרטים המלאים של כל דגם</span>{bc.DOWN}</div>
  <div class="demo cv-demo">{ic("demo")}<div><b>הדגמה בבית הלקוח: 99 ₪</b><span>לדגמי Plus ו-Business · הסכום מנוכה במלואו מהרכישה</span></div></div>
  {xsec(other_cover_idx, True)}
</section>'''

def pro_cover(first_idx, other_cover_idx):
    return f'''
<section class="page cover">
  <header class="top">
    <div class="brand"><span class="wm">Gal<b>CLEAN</b></span><span class="wm-s">WINDOW CLEANING SOLUTION</span></div>
    <span class="tag">ערכות מקצועיות</span>
  </header>
  <h2 class="cv-h">המכשיר של המקצוענים <em>לניקיון חלונות מהיר</em></h2>
  <p class="cv-p">פתרון מקצועי בשיטת אוסמוזה הפוכה לניקוי חלונות, מעקות זכוכית וקירות מסך. המכשיר מזקק את מי הברז עד 0 מינרלים, והמים מתייבשים מעצמם בלי להשאיר כתמים לבנים: עובדים <b class="hl3">בלי סבון, בלי ניגוב ובלי ייבוש</b>. עם מוט מהקרקע מנקים במהירות שורות ארוכות של חלונות בגובה הרחוב, מגיעים למקומות שהגישה אליהם מאתגרת, ועד גובה 20 מ'. עוצמה, יעילות וחיסכון בזמן עבודה, לעסקים, פרויקטים גדולים ותעשייה.</p>
  <div class="cv-lbl"><b>איזה מכשיר מתאים לכם?</b><i></i></div>
  {cards(PRO, first_idx, True)}
  <div class="cv-note">המחירים {VIA} · הקישו על דגם כדי לעבור אליו</div>
  <div class="scroll"><span>גללו למטה לפרטים המלאים של כל דגם</span>{bc.DOWN}</div>
  <div class="demo cv-demo">{ic("demo")}<div><b>הדגמה במקום הלקוח: 99 ₪</b><span>הסכום מנוכה במלואו מהרכישה</span></div></div>
  {xsec(other_cover_idx, False)}
</section>'''

def build(order):
    """order: 'home' (home first) or 'pro' (professional first)."""
    groups = [("home", HOME), ("pro", PRO)] if order == "home" else [("pro", PRO), ("home", HOME)]
    seq = []  # (type, payload)
    cover_idx = {}
    for g, models in groups:
        cover_idx[g] = len(seq); seq.append(("cover", g))
        for p in models: seq.append(("model", (g, p)))
    model_pos = [(i, s[1]) for i, s in enumerate(seq) if s[0] == "model"]
    total = len(model_pos)
    pages = []
    for i, (t, payload) in enumerate(seq):
        if t == "cover":
            g = payload; other = "pro" if g == "home" else "home"
            body = home_cover(i + 1, cover_idx[other]) if g == "home" else pro_cover(i + 1, cover_idx[other])
            pages.append(bc.doc("GalClean", body)); continue
        g, p = payload
        h = pro_page_html(p) if g == "pro" else bm.page(p, show_adds=False)
        if p["name"] == "Business":
            h = h.replace('<span class="tag">ערכה לעסקים</span>', '<span class="tag">ערכה לבית ולעסק</span>')
            box = f'<div class="spec hl">{ic("home")}<div><div class="lbl">{BUS_HOME[0]}</div><div class="val">{BUS_HOME[1]}</div></div></div>\n  '
            anchor = '<div class="sec"><span>מה מגיע בערכה</span>'
            h = h.replace(anchor, box + anchor, 1)
        # nav replaces the repeated strap
        s0 = h.index('<div class="strap">'); s1 = h.index('</div>', h.index('</p>', s0)) + len('</div>')
        n = [k for k, (pi, _) in enumerate(model_pos) if pi == i][0]
        chips = ""
        for gg, models in groups:
            chips += f'<div class="grp">{"לבית ולעסק" if gg == "home" else "קו מקצועי"}</div>'
            for q in models:
                qi = [pi for pi, (g2, q2) in model_pos if q2 is q][0]
                chips += f'<div class="chip{" on" if q is p else ""}" data-goto="{qi}">{q["name"]}</div>'
        nav = f'<div class="mnav"><div class="mnav-h"><span>דגם <b>{n+1}</b> מתוך {total}</span><span data-goto="{cover_idx[g]}">← כל הדגמים</span></div><div class="bar">{chips}</div></div>'
        h = h[:s0] + nav + h[s1:]
        # add-ons at the end of the last model of each group
        last_of_group = (p is (HOME if g == "home" else PRO)[-1])
        tail = ""
        if last_of_group:
            tail += home_adds_block() if g == "home" else pro_adds_block()
        if n < total - 1:
            ni, (ng, q) = model_pos[n + 1]
            target = ni if ng == g else cover_idx[ng]
            k = "הדגם הבא" if ng == g else ("ממשיכים לקו המקצועי" if ng == "pro" else "ממשיכים לדגמים לבית ולעסק")
            pv = f'<small>{VIA}</small>' if ng == "pro" else ""
            tail += f'''<div class="next" data-goto="{target}"><div><div class="k">{k} · {n+2} מתוך {total}</div><b>{q["line"]} {q["name"]}</b><span>{q["sub"]}</span><span class="tp"><span class="cur">₪</span>{q["price"]}{pv}</span></div><img src="{TH[q["name"]]}"><div class="arr">{bc.DOWN}ממשיכים לגלול או מקישים כאן</div></div>'''
        else:
            tail += '<div class="back" data-goto="0">↑ חזרה לתחילת המסמך</div>'
        h = h.replace('<div class="end"></div>', tail + '<div class="end"></div>')
        pages.append(bc.doc(f"GalClean {p['line']} {p['name']}", h))
    files = []
    for i, html in enumerate(pages):
        f = W / f"full_{order}_{i:02d}.html"
        f.write_text(html.replace("</style>", EXTRA2 + "</style>", 1), encoding="utf-8"); files.append(f.name)
    return files

if __name__ == "__main__":
    for o in ("home", "pro"):
        print(o, build(o))
