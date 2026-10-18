from PIL import Image, ImageDraw
import numpy as np, cv2
im=Image.open('b_cut.png').convert('RGBA'); a=np.array(im); H,W=a.shape[:2]
CUT=893
keep=np.zeros((H,W),bool)
for y in range(CUT,H):
    xr = 1161 if y<1100 else int(1161-(y-1100)*10/600)
    keep[y,:max(xr,1140)]=True
keep[540:750,385:795]=True
a[...,3]=np.where(keep,a[...,3],0)
img=Image.fromarray(a); d=ImageDraw.Draw(img)
# lid top surface: rows from CUT down to the black front band top line
def band_top(x): return 946 + (x-115)*(905-946)/(1165-115)
for x in range(105,1162):
    yb=int(band_top(x))
    for y in range(CUT-2,yb+2):
        t=(y-(CUT-2))/max(1,(yb+2-(CUT-2)))
        v=int(22+18*t); d.point((x,y),fill=(v,v,v+3,255))
# subtle back highlight
d.line([(120,CUT+1),(1158,CUT+1)],fill=(70,72,78,255),width=2)
for (x0,x1) in [(398,450),(729,786)]:
    for x in range(x0,x1):
        t=(x-x0)/(x1-x0); s=int(26+34*np.sin(t*np.pi))
        d.line([(x,745),(x,int(band_top(x))-6)],fill=(s,s,s+2,255))
    yb=int(band_top((x0+x1)//2))-6
    d.ellipse([x0-4,yb-6,x1+4,yb+6],fill=(18,18,20,255))
    for x in range(x0,x1):
        t=(x-x0)/(x1-x0); s=int(26+34*np.sin(t*np.pi)); d.line([(x,745),(x,yb-2)],fill=(s,s,s+2,255))
    d.line([(x0,790),(x1-1,790)],fill=(80,80,84,255),width=2)
a=np.array(img)
m=(a[...,3]>20).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(m,8)
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); a[...,3]=np.where(lab==big,a[...,3],0)
out=Image.fromarray(a); out=out.crop(out.getbbox()); out.save('b_final.png'); print(out.size)
bg=Image.new('RGBA',out.size,(240,240,240,255)); bg.alpha_composite(out); bg.convert('RGB').crop((0,0,out.width,600)).save('b_top_prev.jpg')
