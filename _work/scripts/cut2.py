from PIL import Image, ImageOps
import numpy as np, cv2
from rembg import remove, new_session
s=new_session('isnet-general-use')
for n in ['reel','brush','pole']:
    im=ImageOps.exif_transpose(Image.open(n+'_src.jpg')).convert('RGB'); print(n, im.size, flush=True)
    out=np.array(remove(im,session=s))
    m=(out[...,3]>20).astype(np.uint8); k,lab,st,_=cv2.connectedComponentsWithStats(m,8)
    big=1+np.argmax(st[1:,4]); out[...,3]=np.where(lab==big,out[...,3],0)
    o=Image.fromarray(out); o=o.crop(o.getbbox()); o.save(n+'_cut.png'); print(n,'->',o.size)
    bg=Image.new('RGBA',o.size,(12,14,18,255)); bg.alpha_composite(o); bg.convert('RGB').save(n+'_cprev.jpg',quality=85)
