import build  # noqa (writes catalog.html)
from build import ICONS, CSS, faces
cells="".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;color:#5ec4ff"><span class="ic" style="width:96px;height:96px">{v}</span><span style="color:#999;font:12px sans-serif">{k}</span></div>' for k,v in ICONS.items())
open('sheet.html','w').write(f'<html><head><style>{CSS}</style></head><body style="direction:ltr;background:#0a0c10;padding:30px"><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:30px">{cells}</div></body></html>')
