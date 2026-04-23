from pathlib import Path
import json, sys
from PIL import Image, ImageOps, ImageDraw

base=Path(sys.argv[1])
limit=int(sys.argv[2]) if len(sys.argv)>2 else 16
cands=json.loads((base/'duplicate_candidates.json').read_text(encoding='utf-8'))['near_duplicate_candidates'][:limit]
out=[]
for i,c in enumerate(cands,1):
    pa=base/'cropped_photos2'/c['file_a']
    pb=base/'cropped_photos2'/c['file_b']
    ia=Image.open(pa).convert('RGB')
    ib=Image.open(pb).convert('RGB')
    h=max(ia.height, ib.height)
    canvas=Image.new('RGB',(ia.width+ib.width+30,h+40),'white')
    canvas.paste(ia,(0,40))
    canvas.paste(ib,(ia.width+30,40))
    d=ImageDraw.Draw(canvas)
    d.text((5,5),f"{i}: p{c['page_a']} {c['file_a']} vs p{c['page_b']} {c['file_b']} d={c['distance']}",fill='black')
    fp=base/f'candidate_{i:02d}_{c["page_a"]}_{c["page_b"]}.jpg'
    canvas.save(fp, quality=92)
    out.append(str(fp))
print('\n'.join(out))
