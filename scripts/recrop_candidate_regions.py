from pathlib import Path
import json, sys
from PIL import Image

base=Path(sys.argv[1])
render=base/'rendered_pages'
imgdir=base/'cropped_photos2'
imgdir.mkdir(exist_ok=True)
boxes=[('l',(0.24,0.424,0.485,0.503)),('r',(0.523,0.423,0.760,0.504))]
mp=json.loads((base/'page_image_text_mapping.json').read_text(encoding='utf-8'))
for page in mp['pages']:
    pg=Path(page['page_image'])
    im=Image.open(pg)
    w,h=im.size
    paths=[]
    for suffix,(l,t,r,b) in boxes:
        out=imgdir/f'{pg.stem}_{suffix}.jpg'
        crop=im.crop((int(l*w), int(t*h), int(r*w), int(b*h)))
        crop.save(out, quality=92)
        paths.append(str(out))
    page['image_paths']=paths
(base/'page_image_text_mapping.json').write_text(json.dumps(mp, ensure_ascii=False, indent=2), encoding='utf-8')
(base/'page_mapping.json').write_text(json.dumps(mp, ensure_ascii=False, indent=2), encoding='utf-8')
print(imgdir)
