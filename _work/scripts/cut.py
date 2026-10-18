import sys
from PIL import Image, ImageOps
from rembg import remove, new_session
s = new_session(sys.argv[1])
for f,n in [('20261004_092737.jpg','a'),('20261004_092804.jpg','b')]:
    im = ImageOps.exif_transpose(Image.open('/mnt/user-data/uploads/'+f)).convert('RGB')
    im.thumbnail((2400,2400)); im.save(n+'_orig.jpg', quality=92)
    remove(im, session=s).save(n+'_cut.png'); print(n, im.size, flush=True)
