from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
import pathlib
W=pathlib.Path('.').resolve()
names=['GALHOME-Lite','GALHOME-Plus','GALPRO-Business']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':900},device_scale_factor=2)
    for pre in ['m','mc']:
        for n in names:
            pg.set_viewport_size({'width':430,'height':900})
            pg.goto((W/f'{pre}_{n}.html').as_uri()); pg.wait_for_timeout(400)
            h=pg.evaluate("Math.ceil(document.querySelector('.page').getBoundingClientRect().height)")
            print(pre,n,h)
            pg.pdf(path=f'{pre}-{n}.pdf',width='430px',height=f'{h+1}px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
            if pre=='mc': pg.set_viewport_size({'width':430,'height':h}); pg.screenshot(path=f'mc_{n}.png')
    b.close()
w=PdfWriter()
for n in names:
    r=PdfReader(f'mc-{n}.pdf'); assert len(r.pages)==1; w.add_page(r.pages[0])
w.write('mobile-all.pdf')
for n in names:
    r=PdfReader(f'm-{n}.pdf'); assert len(r.pages)==1
print('links',[a.get_object()['/A'].get('/URI') for a in PdfReader('mobile-all.pdf').pages[0]['/Annots']])
