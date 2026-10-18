import build_full, base64, pathlib
from playwright.sync_api import sync_playwright
from build import faces
th={k:build_full.TH[k] for k in ['Lite','Plus','Business','Expert','Turbo','Ultra']}
imgs=''.join(f'<img src="{th[k]}">' for k in ['Ultra','Turbo','Expert','Business','Plus','Lite'])
html=f'''<html dir="rtl"><head><meta charset="utf-8"><style>{faces}
body{{margin:0;width:1200px;height:630px;background:radial-gradient(90% 90% at 30% 40%,#16263a,#0a0c10 70%);font-family:Heebo;color:#f4f6f9;overflow:hidden}}
.w{{position:absolute;inset:0;padding:56px 64px;display:flex;flex-direction:column}}
.lg{{direction:ltr;text-align:right;font-size:46px;font-weight:300}}.lg b{{font-weight:800;color:#5ec4ff}}
.s{{direction:ltr;text-align:right;font-size:13px;letter-spacing:5px;color:#a7b0bf;margin-top:6px}}
h1{{font-size:64px;line-height:1.08;margin:34px 0 0;font-weight:800}}h1 em{{font-style:normal;color:#5ec4ff}}
p{{font-size:28px;color:#c9d1dc;margin:16px 0 0}}
.row{{position:absolute;left:56px;bottom:46px;display:flex;align-items:flex-end;gap:10px}}.row img{{height:190px;filter:drop-shadow(0 14px 16px rgba(0,0,0,.6))}}
</style></head><body><div class="w"><div class="lg">Gal<b>CLEAN</b></div><div class="s">WINDOW CLEANING SOLUTION</div>
<h1>מהיום כל אחד מנקה<br>חלונות <em>כמו מקצוען</em></h1><p>בלי סבון, בלי ניגוב ובלי ייבוש · 6 דגמים</p></div><div class="row">{imgs}</div></body></html>'''
pathlib.Path('og.html').write_text(html,encoding='utf-8')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1200,'height':630})
    pg.goto(pathlib.Path('og.html').resolve().as_uri()); pg.wait_for_timeout(500)
    pg.screenshot(path='/home/claude/galclean-catalog/preview.jpg',type='jpeg',quality=88); b.close()
