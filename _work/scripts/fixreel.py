from PIL import Image
import numpy as np, cv2
a=np.array(Image.open('reel_cut.png').convert('RGBA'))
# 1) smudge above bracket clamp
box=a[52:98,862:942]; box[...,3]=np.where(box[...,3]<235,0,box[...,3])
# also remove any light low-sat pixels above the tube line in that box
Y,X=np.mgrid[52:98,862:942]
tube_top=57+(X-780)*(97-57)/(870-780)
box[...,3]=np.where((Y<tube_top-2)&(X<870),0,box[...,3])
# 2) sticker: inpaint red label + white text
rgb=a[...,:3].copy(); hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
reg=np.zeros(a.shape[:2],np.uint8)
y0,y1,x0,x1=640,712,660,790
sub=hsv[y0:y1,x0:x1]; s=rgb[y0:y1,x0:x1].astype(int)
red=((sub[...,0]<12)|(sub[...,0]>168))&(sub[...,1]>90)&(sub[...,2]>80)
white=(s.mean(-1)>150)
m=((red|white)|(s.mean(-1)>48)).astype(np.uint8)
m[4:68,6:124]=1
m=cv2.dilate(m,np.ones((7,7),np.uint8))
reg[y0:y1,x0:x1]=m
bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
inp=cv2.inpaint(bgr,reg,9,cv2.INPAINT_TELEA)
inp=cv2.cvtColor(inp,cv2.COLOR_BGR2RGB)
# add subtle matte noise so it does not look flat
noise=np.random.default_rng(1).normal(0,2.2,inp.shape)
inp=np.where(reg[...,None]>0,np.clip(inp+noise,0,255),inp).astype(np.uint8)
a[...,:3]=inp
print('sticker px',int(reg.sum()))
Image.fromarray(a).save('reel_fix.png')
bg=Image.new('RGBA',(a.shape[1],a.shape[0]),(12,14,18,255)); bg.alpha_composite(Image.fromarray(a))
bg.convert('RGB').crop((520,560,900,780)).resize((760,440)).save('reel_sticker.jpg')
bg.convert('RGB').crop((780,0,1003,200)).save('reel_sm2.jpg')
