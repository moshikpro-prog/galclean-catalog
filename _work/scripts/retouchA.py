from PIL import Image
import numpy as np, cv2
im=Image.open('a_final.png').convert('RGBA'); a=np.array(im).astype(np.float32)
H,W=a.shape[:2]; rgb=a[...,:3].copy(); al=a[...,3].copy()
lum=rgb.mean(-1)
# 1) clip halo above lid line
Y,X=np.mgrid[0:H,0:W]
top=82+(X/W)*43
al[Y<top]=0
# 2) masks
sil=(al>60).astype(np.uint8)
sil=cv2.morphologyEx(sil,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
cs,_=cv2.findContours(sil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
fill=np.zeros_like(sil); cv2.drawContours(fill,[max(cs,key=cv2.contourArea)],-1,1,-1)
dd=cv2.distanceTransform(fill,cv2.DIST_L2,5)
al=np.where(dd>3,255,np.where(fill>0,np.maximum(al,dd/3*255),0)).astype(np.float32)
solid=fill>0
glass=(lum<125)&solid&(X>40)&(X<672)&(Y>top+18)
glass=cv2.morphologyEx(glass.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((25,25),np.uint8))
glass=cv2.morphologyEx(glass,cv2.MORPH_OPEN,np.ones((9,9),np.uint8)).astype(bool)
# keep largest comp
n,lab,st,_=cv2.connectedComponentsWithStats(glass.astype(np.uint8)); glass=lab==(1+np.argmax(st[1:,4]))
lid=(Y<top+16)
white=solid&~glass&~lid&((lum>110)|(X>620))
# 3) normalized blur for white panels (removes reflections)
def nblur(img,mask,s):
    m=mask.astype(np.float32); out=np.zeros_like(img)
    den=cv2.GaussianBlur(m,(0,0),s)+1e-4
    for c in range(3): out[...,c]=cv2.GaussianBlur(img[...,c]*m,(0,0),s)/den
    return out
smooth=nblur(rgb,white,40)
# lift & neutralize whites slightly
sm_l=smooth.mean(-1,keepdims=True); smooth=np.clip(sm_l*1.04+8,0,255)*np.array([0.985,0.99,1.0])
# keep fine seams in lower area: high-pass of original, only negative thin lines
hp=lum-cv2.GaussianBlur(lum,(0,0),3)
seam=np.clip(hp,-60,0)*((Y>1100)|(X>W-60)).astype(np.float32)*white
newwhite=np.clip(smooth+seam[...,None]*0.9,0,255)
# preserve edges of white panel (anti-aliasing) : blend by distance to non-white
dist=cv2.distanceTransform(white.astype(np.uint8),cv2.DIST_L2,5)
wb=np.clip((dist-1)/5,0,1)[...,None]
rgb=np.where(white[...,None],rgb*(1-wb)+newwhite*wb,rgb)
# 4) glass repaint
gy=(Y-Y[glass].min())/(Y[glass].max()-Y[glass].min()+1)
gx=(X-X[glass].min())/(X[glass].max()-X[glass].min()+1)
base=np.stack([30+20*(1-gy), 33+21*(1-gy), 42+24*(1-gy)],-1)
# soft diagonal sheen
d=(gx*0.9+gy*0.55); sheen=np.exp(-((d-0.55)/0.12)**2)*14 + np.exp(-((gx-0.08)/0.05)**2)*10
newglass=base+sheen[...,None]
# logo/text from original: bright pixels in logo box
box=(X>150)&(X<560)&(Y>290)&(Y<530)
bg_local=cv2.medianBlur(lum.astype(np.uint8),31).astype(np.float32)
txt=np.clip((lum-85)/75,0,1)*box*glass
txt=cv2.GaussianBlur(txt.astype(np.float32),(0,0),0.6)
txtcol=np.array([205,208,214])
gd=cv2.distanceTransform(glass.astype(np.uint8),cv2.DIST_L2,5)
gb=np.clip((gd-3)/8,0,1)[...,None]
g2=newglass*(1-txt[...,None])+txtcol*txt[...,None]
rgb=np.where(glass[...,None],rgb*(1-gb)+g2*gb,rgb)
out=np.dstack([rgb,al]).clip(0,255).astype(np.uint8)
o=Image.fromarray(out); o=o.crop(o.getbbox()); o.save('a_final3.png'); print(o.size)
bg=Image.new('RGBA',o.size,(10,12,16,255)); bg.alpha_composite(o); bg.convert('RGB').resize((o.width*2//3,o.height*2//3)).save('a3_prev.jpg')
