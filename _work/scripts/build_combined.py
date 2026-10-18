"""Combined mobile file: cover page with the 3 models + in-page navigation between models."""
import base64, io, pathlib
from PIL import Image
import build_mobile as bm
from build import faces, ic, PAGES

W = pathlib.Path(__file__).parent

def thumb(path, h=300):
    im = Image.open(W / path); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

TH = {"home": thumb("a_final3.png"), "biz": thumb("b_final3.png")}
N = len(PAGES)

EXTRA = r'''
/* cover */
.cover{padding-bottom:30px}
.badge{display:inline-flex;align-items:center;gap:8px;margin-top:26px;padding:7px 14px;border-radius:999px;background:rgba(94,196,255,.12);border:1px solid rgba(94,196,255,.35);color:var(--ac);font-size:14px;font-weight:700}
.cv-h{font-size:38px;line-height:1.12;font-weight:800;letter-spacing:-.8px;margin-top:26px}
.cv-h em{font-style:normal;color:var(--ac)}
.cv-p{font-size:15.5px;line-height:1.6;color:var(--mut);margin-top:12px;font-weight:300}
.cv-lbl{display:flex;align-items:center;gap:10px;margin:28px 0 12px;font-size:15px;color:var(--mut)}
.cv-lbl b{color:var(--tx);font-size:20px;font-weight:800}.cv-lbl i{flex:1;height:1px;background:var(--line)}
.mc{display:grid;grid-template-columns:118px 1fr;gap:14px;align-items:center;padding:14px 16px 14px 14px;margin-bottom:12px;border-radius:20px;background:var(--card);border:1px solid var(--line);position:relative;overflow:hidden}
.mc:before{content:"";position:absolute;inset:0;background:radial-gradient(60% 90% at 85% 50%,rgba(94,196,255,.10),transparent 70%)}
.mc .num{position:absolute;top:12px;left:14px;width:28px;height:28px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:var(--mut)}
.mc .th{height:150px;display:flex;align-items:flex-end;justify-content:center;position:relative}
.mc .th img{max-height:150px;max-width:118px;filter:drop-shadow(0 10px 12px rgba(0,0,0,.6))}
.mc .bd{position:relative}
.mc .ln{font-size:12px;letter-spacing:4px;color:var(--mut);direction:ltr;text-align:right}
.mc .nm{font-size:30px;font-weight:800;line-height:1;direction:ltr;text-align:right;letter-spacing:-.5px}
.mc .fit{font-size:14px;color:var(--mut);line-height:1.4;margin-top:6px}
.mc .row{display:flex;align-items:center;justify-content:space-between;margin-top:10px;gap:8px}
.mc .pr{font-size:24px;font-weight:800;direction:ltr}.mc .pr .cur{font-size:.6em}
.mc .fl{font-size:13px;color:var(--ac);border:1px solid rgba(94,196,255,.3);border-radius:999px;padding:3px 9px;white-space:nowrap}
.mc .go{margin-top:10px;font-size:14px;font-weight:700;color:var(--ac)}
.cv-note{font-size:13px;color:var(--dim);text-align:center;margin-top:2px}
.scroll{margin-top:22px;display:flex;flex-direction:column;align-items:center;gap:6px;color:var(--mut);font-size:15px}
.scroll svg{width:26px;height:26px;color:var(--ac)}
.cv-demo{margin-top:22px}

/* model nav (combined file) */
.mnav{margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}
.mnav-h{font-size:14px;color:var(--mut);display:flex;justify-content:space-between;align-items:center}
.mnav-h b{color:var(--tx);font-weight:700}
.bar{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:10px}
.chip{padding:10px 6px;border-radius:12px;border:1px solid var(--line);text-align:center;font-size:15px;font-weight:600;color:var(--mut);direction:ltr;background:rgba(255,255,255,.02)}
.chip.on{background:var(--ac);border-color:var(--ac);color:#06121d;font-weight:800}

/* next model teaser */
.next{margin-top:26px;display:grid;grid-template-columns:1fr 70px;gap:12px;align-items:center;padding:16px 18px;border-radius:20px;border:1px dashed rgba(94,196,255,.5);background:rgba(94,196,255,.06)}
.next .k{font-size:13px;color:var(--ac);font-weight:700}
.next b{display:block;font-size:24px;font-weight:800;direction:ltr;text-align:right;margin-top:2px}
.next span{font-size:14px;color:var(--mut);display:block}
.next .tp{font-size:20px;font-weight:800;color:var(--tx);direction:ltr;text-align:right;margin-top:4px}.next .tp .cur{display:inline;font-size:.6em;color:var(--ac)}
.next img{max-height:84px;justify-self:center;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}
.next .arr{grid-column:1/-1;display:flex;align-items:center;gap:8px;font-size:14px;color:var(--mut);margin-top:2px}
.next .arr svg{width:18px;height:18px;color:var(--ac)}
.back{display:block;text-align:center;margin-top:20px;padding:13px;border-radius:14px;border:1px solid var(--line);font-size:15px;font-weight:600;color:var(--mut)}
'''
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/><path d="M6 4l6 6 6-6" opacity=".45"/></svg>'

def doc(title, body):
    return f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{title}</title><style>{faces}{bm.CSS}{EXTRA}</style></head><body>{body}</body></html>'

def cover():
    cards = ""
    for i, p in enumerate(PAGES):
        cards += f'''
  <div class="mc" data-goto="{i+1}">
    <span class="num">{i+1}</span>
    <div class="th"><img src="{TH[p["kind"]]}"></div>
    <div class="bd">
      <div class="ln">{p["line"]}</div><div class="nm">{p["name"]}</div>
      <div class="fit">{p["fit"]}</div>
      <div class="row"><span class="pr"><span class="cur">₪</span>{p["price"]}</span><span class="fl">{p["flow"]} ל'/דקה</span></div>
      <div class="go">לכל הפרטים ←</div>
    </div>
  </div>'''
    return f'''
<section class="page cover">
  <header class="top">
    <div class="brand"><span class="wm">Gal<b>CLEAN</b></span><span class="wm-s">WINDOW CLEANING SOLUTION</span></div>
    <span class="tag">ערכות לבית ולעסק</span>
  </header>
  <h2 class="cv-h">מהיום כל אחד מנקה חלונות <em>כמו מקצוען</em></h2>
  <p class="cv-p">מכשירי אוסמוזה הפוכה פרטיים יחידים מסוגם בישראל, לניקוי קירות מסך, מעקות זכוכית, אלומיניום, תריסים, רפפות, צלונים, מראות ודלתות. מתאימים מכשיר לפי הצורך ומוט לפי הגובה הדרוש.</p>

  <div class="cv-lbl"><b>איזה מכשיר מתאים לכם?</b><i></i></div>
  {cards}
  <div class="cv-note">המחירים כוללים מע"מ · הקישו על דגם כדי לעבור אליו</div>

  <div class="scroll"><span>גללו למטה לפרטים המלאים של כל דגם</span>{DOWN}</div>

  <div class="demo cv-demo">{ic("demo")}<div><b>הדגמה בבית הלקוח: 99 ₪</b><span>לדגמי Plus ו-Business · הסכום מנוכה במלואו מהרכישה</span></div></div>
</section>'''

def model_page(i, p):
    html = bm.page(p, show_adds=(i == N - 1))
    # replace the repeated strap with model navigation
    s0 = html.index('<div class="strap">'); s1 = html.index('</div>', html.index('</p>', s0)) + len('</div>')
    chips = "".join(f'<div class="chip{" on" if j == i else ""}" data-goto="{j+1}">{q["name"]}</div>' for j, q in enumerate(PAGES))
    nav = f'<div class="mnav"><div class="mnav-h"><span>דגם <b>{i+1}</b> מתוך {N}</span><span data-goto="0">← כל הדגמים</span></div><div class="bar">{chips}</div></div>'
    html = html[:s0] + nav + html[s1:]
    # bottom: next model teaser, or back to overview on the last page
    if i < N - 1:
        q = PAGES[i + 1]
        tail = f'''<div class="next" data-goto="{i+2}"><div><div class="k">הדגם הבא · {i+2} מתוך {N}</div><b>{q["line"]} {q["name"]}</b><span>{q["sub"]}</span><span class="tp"><span class="cur">₪</span>{q["price"]}</span></div><img src="{TH[q["kind"]]}"><div class="arr">{DOWN}ממשיכים לגלול או מקישים כאן</div></div>'''
    else:
        tail = '<div class="back" data-goto="0">↑ חזרה להשוואת הדגמים</div>'
    return html.replace('<div class="end"></div>', tail + '<div class="end"></div>')

(W / "mc_00-cover.html").write_text(doc("GalClean | 3 דגמים", cover()), encoding="utf-8")
for i, p in enumerate(PAGES):
    (W / f"mc_{i+1:02d}.html").write_text(doc(f"GalClean {p['line']} {p['name']}", model_page(i, p)), encoding="utf-8")
print("combined ok")
