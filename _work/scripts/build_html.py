import re, pathlib, build_full
W=pathlib.Path('.')
VID_R='XoUpxtDleBA'; VID_L='Ll4vgSTiU6k'
def yt(v, auto):
    q=(f'autoplay=1&mute=1&loop=1&playlist={v}&' if auto else '')+'playsinline=1&rel=0&cc_load_policy=0&iv_load_policy=3'
    return f'<div class="yt"><iframe src="https://www.youtube.com/embed/{v}?{q}" title="GalClean" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin" loading="eager"></iframe></div>'
VIDEOS=f'<div class="ytrow">{yt(VID_R,True)}{yt(VID_L,False)}</div>'  # RTL: first = right
CSS_ADD='''
html{width:auto!important;background:#05070a}
body{width:430px!important;margin:0 auto!important;box-shadow:0 0 60px rgba(0,0,0,.6)}
[data-goto]{cursor:pointer}
.ytrow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}
.yt{position:relative;aspect-ratio:9/16;border-radius:16px;overflow:hidden;border:1px solid rgba(94,196,255,.3);background:#000;box-shadow:0 10px 24px rgba(0,0,0,.5)}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
'''
JS='''<script>
document.querySelectorAll('[data-goto]').forEach(function(e){e.addEventListener('click',function(){var t=document.getElementById('p'+e.getAttribute('data-goto'));if(t)t.scrollIntoView({behavior:'smooth'});});});
</script>'''
def build(order,out):
    files=build_full.build(order)
    style=None; secs=[]
    for k,f in enumerate(files):
        s=(W/f).read_text(encoding='utf-8')
        if style is None: style=re.search(r'<style>.*?</style>',s,re.S).group(0)
        body=re.search(r'<body>(.*)</body>',s,re.S).group(1)
        body=body.replace('<section class="page',f'<section id="p{k}" class="page',1)
        if k==0:
            i=body.index('</h2>')+5; body=body[:i]+VIDEOS+body[i:]
        secs.append(body)
    style=style.replace('</style>',CSS_ADD+'</style>')
    html=f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=430"><meta name="referrer" content="strict-origin-when-cross-origin"><title>GalClean | קטלוג מכשירים</title>{style}</head><body>{"".join(secs)}{JS}</body></html>'
    (pathlib.Path('/home/claude')/out).write_text(html,encoding='utf-8'); print(out, round(len(html)/1e6,1),'MB')
build('home','GalClean-catalog-home-first.html')
build('pro','GalClean-catalog-pro-first.html')
