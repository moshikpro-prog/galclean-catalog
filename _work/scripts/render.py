from playwright.sync_api import sync_playwright
import pathlib
W=pathlib.Path('.').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':794,'height':1123},device_scale_factor=2)
    pg.goto((W/'catalog.html').as_uri()); pg.wait_for_timeout(800)
    # overflow check
    print(pg.evaluate("""[...document.querySelectorAll('.page')].map(s=>{const r=s.getBoundingClientRect();const f=s.querySelector('.foot').getBoundingClientRect();return [Math.round(r.height),Math.round(f.bottom-r.top)]})"""))
    pg.pdf(path='GalClean-GALHOME-GALPRO-Business.pdf',width='210mm',height='297mm',print_background=True,prefer_css_page_size=True)
    for i in range(3):
        pg.locator('.page').nth(i).screenshot(path=f'p{i+1}.png')
    b.close()
