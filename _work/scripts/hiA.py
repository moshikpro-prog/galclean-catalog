from PIL import Image, ImageOps
import numpy as np, cv2
from rembg import remove, new_session
full=ImageOps.exif_transpose(Image.open('/mnt/user-data/uploads/20261004_092737.jpg')).convert('RGB')
s=full.width/2400
lo=np.array(Image.open('a_cut.png'))[...,3]
ys,xs=np.where(lo>20); 
# use main body bbox from a_final crop: recompute
x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
box=(int(x0*s)-60,int(y0*s)-60,int(x1*s)+60,int(y1*s)+60); print(box)
crop=full.crop(box)
out=remove(crop,session=new_session('isnet-general-use'))
a=np.array(out); m=(a[...,3]>20).astype(np.uint8); n,lab,st,_=cv2.connectedComponentsWithStats(m,8)
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); a[...,3]=np.where(lab==big,a[...,3],0)
im=Image.fromarray(a); im=im.crop(im.getbbox()); im.save('a_final.png'); print(im.size)
