from pathlib import Path
import json, hashlib, itertools, sys
from PIL import Image, ImageStat

base=Path(sys.argv[1])
mp=json.loads((base/'page_image_text_mapping.json').read_text(encoding='utf-8'))
items=[]
for p in mp['pages']:
    for path in p['image_paths']:
        img=Image.open(path).convert('RGB')
        stat=ImageStat.Stat(img)
        mean=sum(stat.mean)/3
        var=sum(stat.var)/3
        items.append({'page':p['page_number_1_based'],'file':Path(path).name,'path':path,'md5':hashlib.md5(Path(path).read_bytes()).hexdigest(),'mean':mean,'var':var,'size':img.size})
exact={}
for it in items:
    exact.setdefault(it['md5'],[]).append(it)
exact_groups=[g for g in exact.values() if len({x['page'] for x in g})>1]
exact_groups=sorted(exact_groups,key=lambda g:(-len(g),g[0]['page']))
print('EXACT_GROUPS',len(exact_groups))
for g in exact_groups[:20]:
    print('pages',sorted({x['page'] for x in g}),'files',[x['file'] for x in g],'mean',round(g[0]['mean'],1),'var',round(g[0]['var'],1))

def ahash(img):
    small=img.resize((8,8)).convert('L')
    vals=list(small.getdata())
    avg=sum(vals)/len(vals)
    bits=''.join('1' if v>=avg else '0' for v in vals)
    return int(bits,2)
vals=[]
for it in items:
    img=Image.open(it['path']).convert('RGB')
    it['ah']=ahash(img)
    vals.append(it)
near=[]
for a,b in itertools.combinations(vals,2):
    if a['page']==b['page']: continue
    d=bin(a['ah']^b['ah']).count('1')
    if d<=2:
        near.append((d,a,b))
near=sorted(near,key=lambda x:(x[0],x[1]['page'],x[2]['page']))
print('NEAR<=2',len(near))
for d,a,b in near[:80]:
    print(d,a['file'],a['page'],round(a['var'],1),'::',b['file'],b['page'],round(b['var'],1))
