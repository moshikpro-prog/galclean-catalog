from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
import pathlib
W=pathlib.Path('.').resolve()
files=['mc_00-cover.html','mc_01.html','mc_02.html','mc_03.html']
links=[]  # (page, rect_px, target, height)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':900},device_scale_factor=2)
    for k,f in enumerate(files):
        pg.set_viewport_size({'width':430,'height':900})
        pg.goto((W/f).as_uri()); pg.wait_for_timeout(400)
        h=pg.evaluate("Math.ceil(document.querySelector('.page').getBoundingClientRect().height)")+1
        rs=pg.evaluate("[...document.querySelectorAll('[data-goto]')].map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,+e.dataset.goto]})")
        for r in rs: links.append((k,r,h))
        pg.pdf(path=f'c{k}.pdf',width='430px',height=f'{h}px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
        pg.set_viewport_size({'width':430,'height':h}); pg.screenshot(path=f'c{k}.png')
        print(f,h,len(rs))
    b.close()
w=PdfWriter()
for k in range(len(files)):
    r=PdfReader(f'c{k}.pdf'); assert len(r.pages)==1; w.add_page(r.pages[0])
for k,(x1,y1,x2,y2,t),h in links:
    s=0.75; H=h*s
    w.add_annotation(page_number=k, annotation=Link(rect=(x1*s,H-y2*s,x2*s,H-y1*s), target_page_index=t))
w.write('mobile-all.pdf'); print('links added',len(links))
from pypdf.generic import ArrayObject, NameObject, FloatObject
w=PdfWriter(clone_from='mobile-all.pdf')
for pg in w.pages:
    for a in pg.get('/Annots',[]):
        o=a.get_object()
        if '/Dest' in o:
            t=int(o['/Dest'][0]); o[NameObject('/Dest')]=ArrayObject([w.pages[t].indirect_reference,NameObject('/FitH'),FloatObject(float(w.pages[t].mediabox.top))])
w.write('mobile-all.pdf'); print('dests fixed')
