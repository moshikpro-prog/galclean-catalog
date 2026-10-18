from PIL import Image, ImageOps, ImageDraw
import numpy as np, cv2
src=ImageOps.exif_transpose(Image.open('expert_src.jpg')).convert('RGB'); src.thumbnail((1800,1800))
cut=np.array(Image.open('expert_cutfull.png')).astype(np.float32)
H,W=cut.shape[:2]; S=4
mk=Image.new('L',(W*S,H*S),0); d=ImageDraw.Draw(mk)
def R(x0,y0,x1,y1,r=0,v=255):
    d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],radius=r*S,fill=v)
def E(x0,y0,x1,y1,v=255): d.ellipse([x0*S,y0*S,x1*S,y1*S],fill=v)
# handle grip (rounded) with inner opening
R(815,85,1008,172,20); R(842,108,980,138,8,0)
# aluminium posts
R(817,168,836,268,3); R(984,168,1003,268,3)
# filter dome (white) between posts
E(852,206,972,262); R(846,232,978,276,4)
# lower black frame bar + blue tank
R(810,264,1006,312,6); R(848,300,972,328,4)
# connection knobs on the lid
for a,b in [(672,775),(783,892),(903,1012)]: E(a,310,b,336)
# inlet / outlet fittings
pass
mk=np.array(mk.resize((W,H),Image.LANCZOS)).astype(np.float32)
TOP=322
al=cut[...,3].copy()
al[:TOP,:]=0
al=np.maximum(al,mk)
rgb=np.where((mk>0)[...,None], np.array(src).astype(np.float32), cut[...,:3])
# remove the long white hose on the right side of the body
lum=rgb.mean(-1)
Y,X=np.mgrid[0:H,0:W]
al=np.where((X>=1168)&(Y>380)&(Y<740)&(lum>110),0,al)
al=np.where((X>=1080)&(Y<345)&(lum>150)&(Y<TOP+24),0,al)
o=np.dstack([rgb,al]).clip(0,255).astype(np.uint8)
m=(o[...,3]>20).astype(np.uint8); k,lab,st,_=cv2.connectedComponentsWithStats(m,8)
b=1+np.argmax(st[1:,4]); o[...,3]=np.where(lab==b,o[...,3],0)
O=Image.fromarray(o); O=O.crop(O.getbbox()); O.save('expert_final.png'); print(O.size)
bg=Image.new('RGBA',O.size,(16,20,26,255)); bg.alpha_composite(O); bg.convert('RGB').save('expert_fprev.jpg',quality=88)
