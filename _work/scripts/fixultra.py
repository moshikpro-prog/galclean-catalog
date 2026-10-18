from PIL import Image, ImageDraw
import numpy as np, cv2
a=np.array(Image.open('ultra_cutfull.png')).astype(np.float32)
H,W=a.shape[:2]; Y,X=np.mgrid[0:H,0:W]
TOP=518
rgb=a[...,:3]; al=a[...,3]
lum=rgb.mean(-1)
body=(al>200)&(Y>=TOP)&(Y<1335)&(X<898)
protect=np.zeros((H,W),bool)
protect[982:1058,318:698]=True; protect[982:1084,318:432]=True     # logo
protect[585:682,400:566]=True      # display
# 1) scratches / stains: bright marks vs local background
bgl=cv2.medianBlur(lum.astype(np.uint8),41).astype(np.float32)
marks=(lum-bgl>16)&body&~protect
marks=cv2.dilate(marks.astype(np.uint8),np.ones((5,5),np.uint8))
bgr=cv2.cvtColor(rgb.clip(0,255).astype(np.uint8),cv2.COLOR_RGB2BGR)
inp=cv2.inpaint(bgr,marks,6,cv2.INPAINT_TELEA)
inp=cv2.cvtColor(inp,cv2.COLOR_BGR2RGB).astype(np.float32)
print('mark px',int(marks.sum()))
# 2) gentle smoothing of grime on the panels (outside logo/display)
sm=cv2.bilateralFilter(inp.astype(np.uint8),9,22,9).astype(np.float32)
pan=(body&~protect)[...,None]
rgb=np.where(pan,sm,inp)
# subtle uniform noise so the matte paint does not look plastic
rgb=np.where(pan,rgb+np.random.default_rng(3).normal(0,1.6,rgb.shape),rgb)
# 2b) lid top strip where the hose bundle rested: rebuild from the clean row below
ref=rgb[552:560].mean(0)
for y in range(TOP,548):
    t=(y-TOP)/30
    row=ref*(0.82+0.18*t)
    m=(al[y]>0)&(X[y]>90)&(X[y]<890)
    rgb[y][m]=row[m]
rgb[TOP:TOP+3]=rgb[TOP:TOP+3]*0.6
# 2c) gentle lift so the dark-grey body separates from the dark page
lift=(Y>=TOP)&(Y<1335)
rgb=np.where(lift[...,None],np.clip(rgb*1.14+6,0,255),rgb)
# 3) remove hoses above the lid and the bag on the right side
al=np.where(Y<TOP,0,al)
al=np.where((X>898)&(Y>=TOP)&(Y<1335),0,al)
img=Image.fromarray(np.dstack([rgb,al]).clip(0,255).astype(np.uint8))
# 4) rebuild the telescopic handle that the hoses covered
d=ImageDraw.Draw(img)
for (x0,x1) in [(399,415),(561,577)]:
    for x in range(x0,x1):
        t=(x-x0)/(x1-x0); s=int(24+30*np.sin(t*np.pi)); d.line([(x,446),(x,TOP+2)],fill=(s,s,s+2,255))
d.rounded_rectangle([397,432,579,456],radius=10,fill=(26,26,28,255))
d.rounded_rectangle([430,434,546,454],radius=8,fill=(34,34,37,255))   # rubber grip
d.line([(432,436),(544,436)],fill=(70,70,74,255),width=2)
img=np.array(img)
m=(img[...,3]>20).astype(np.uint8); k,lab,st,_=cv2.connectedComponentsWithStats(m,8)
b=1+np.argmax(st[1:,4]); img[...,3]=np.where(lab==b,img[...,3],0)
O=Image.fromarray(img); O=O.crop(O.getbbox()); O.save('ultra_final.png'); print(O.size)
bg=Image.new('RGBA',O.size,(16,20,26,255)); bg.alpha_composite(O); bg.convert('RGB').resize((O.width//2,O.height//2)).save('ultra_fprev.jpg',quality=88)
