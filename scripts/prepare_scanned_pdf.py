from pathlib import Path
import fitz, json, shutil, sys
from PIL import Image

pdf=Path(sys.argv[1])
base=Path(sys.argv[2])
base.mkdir(parents=True, exist_ok=True)
local_pdf=base/pdf.name
if not local_pdf.exists():
    shutil.copy2(pdf, local_pdf)
render=base/'rendered_pages'
render.mkdir(exist_ok=True)
imgdir=base/'cropped_photos'
imgdir.mkdir(exist_ok=True)
doc=fitz.open(str(local_pdf))
page_count=doc.page_count
for i in range(page_count):
    out=render/f'page_{i+1:03d}.jpg'
    if out.exists():
        continue
    page=doc.load_page(i)
    pix=page.get_pixmap(matrix=fitz.Matrix(1.8,1.8), alpha=False)
    pix.save(str(out))
boxes=[('a',(0.14,0.43,0.53,0.64)),('b',(0.14,0.64,0.53,0.86))]
pages=[]
for pg in sorted(render.glob('page_*.jpg')):
    im=Image.open(pg)
    w,h=im.size
    paths=[]
    for suffix,(l,t,r,b) in boxes:
        out=imgdir/f'{pg.stem}_{suffix}.jpg'
        if not out.exists():
            crop=im.crop((int(l*w), int(t*h), int(r*w), int(b*h)))
            crop.save(out, quality=90)
        paths.append(str(out))
    pages.append({'page_number_1_based': int(pg.stem.split('_')[1]), 'image_paths': paths, 'raw_text': '', 'fields': {}, 'page_image': str(pg)})
(base/'doc_meta.json').write_text(json.dumps({'source_pdf':str(pdf),'local_pdf':str(local_pdf),'page_count':page_count,'document_class':'scanned','render_dir':str(render)},ensure_ascii=False,indent=2),encoding='utf-8')
(base/'page_image_text_mapping.json').write_text(json.dumps({'source_dir':str(base),'ocr_method':'pending','pages':pages,'notes':'image crops are heuristic photo regions from scanned pages'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'page_count':page_count,'rendered':len(list(render.glob('page_*.jpg'))),'cropped':len(list(imgdir.glob('*.jpg')))},ensure_ascii=False))
