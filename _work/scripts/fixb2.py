from PIL import Image, ImageDraw, ImageFilter
import numpy as np, cv2
a=np.array(Image.open('b_final.png').convert('RGBA')).astype(np.int32)
H,W=a.shape[:2]
# handle region rows 0..335 in this crop
R=slice(0,336)
rgb=a[R,:,:3]; al=a[R,:,3]
lum=rgb.mean(-1)
orange=(rgb[...,0]>170)&(rgb[...,1]<150)&(rgb[...,2]<110)
bad=(lum>110)&~orange
al=np.where(bad,0,al); al=np.where(al>140,255,0).astype(np.uint8)
al=cv2.morphologyEx(al,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
al=cv2.erode(al,np.ones((2,2),np.uint8))
al=cv2.GaussianBlur(al,(3,3),0)
a[R,:,3]=al
# rebuild lid top as trapezoid with rounded corners (supersampled)
S=4
y0,y1=335,392  # back edge row, front edge (left side) approx
mask=Image.new('L',(W*S,(400)*S),0); d=ImageDraw.Draw(mask)
poly=[(28,338),(W-26,336),(W-4,350),(W-4,358),(14,398),(4,384)]
d.polygon([(x*S,y*S) for x,y in poly],fill=255)
mask=mask.resize((W,400),Image.LANCZOS); m=np.array(mask).astype(float)/255
for y in range(330,400):
    t=(y-335)/60; v=np.clip(20+20*t,18,42)
    row=m[y]
    sel=row>0
    a[y,sel,0]=(a[y,sel,0]*(1-row[sel])+v*row[sel]); a[y,sel,1]=a[y,sel,0]; a[y,sel,2]=a[y,sel,0]+2
    a[y,sel,3]=np.maximum(a[y,sel,3]*(row[sel]<0.99), (row[sel]*255)).astype(int)
# clear any pixels above lid outside handle posts/grip that are now opaque leftovers
a[330:338,:,3]=np.where(m[330:338]>0.5,a[330:338,:,3],0)
img=Image.fromarray(a.clip(0,255).astype(np.uint8))
# redraw posts over lid
d=ImageDraw.Draw(img)
for (x0,x1) in [(298,350),(629,686)]:
    yb=376 if x0<400 else 364
    d.ellipse([x0-5,yb-6,x1+5,yb+7],fill=(14,14,16,255))
    for x in range(x0,x1):
        t=(x-x0)/(x1-x0); s=int(26+38*np.sin(t*np.pi)); d.line([(x,190),(x,yb)],fill=(s,s,s+2,255))
    d.line([(x0,236),(x1-1,236)],fill=(85,85,90,255),width=2)
img.save('b_final2.png')
bg=Image.new('RGBA',img.size,(240,240,240,255)); bg.alpha_composite(img); bg.convert('RGB').crop((0,0,W,520)).save('b_top_prev.jpg')
a=np.array(img).astype(np.int32)
for y in range(325,400):
    for x in range(W):
        bl=398+(x-14)*(358-398)/(W-4-14)
        if y<bl-3 and m[y,x]<0.5 and not (290<x<360 or 620<x<695): a[y,x,3]=0
img=Image.fromarray(a.astype(np.uint8)); img.save('b_final2.png')
bg=Image.new('RGBA',img.size,(240,240,240,255)); bg.alpha_composite(img); bg.convert('RGB').crop((0,0,W,520)).save('b_top_prev.jpg')
bg=Image.new('RGBA',img.size,(12,14,18,255)); bg.alpha_composite(img); bg.convert('RGB').resize((W//2,img.height//2)).save('b_full_prev.jpg')
