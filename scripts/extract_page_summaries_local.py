from pathlib import Path
import json,re,sys
base=Path(sys.argv[1])
mp=json.loads((base/'page_image_text_mapping.json').read_text(encoding='utf-8'))
rows=[]
for p in mp['pages']:
    text=p['raw_text']
    m=re.search(r'(20\d{2}年\s*\d{1,2}月\s*\d{1,2})', text)
    date=m.group(1).replace(' ','') if m else ''
    bullets=re.findall(r'\n\d+[、,.]?\s*([^\n]+)', text)
    if not bullets:
        bullets=re.findall(r'\d+[、,.]?([^\n]+)', text)
    bullets=[b.strip() for b in bullets if len(b.strip())>1][:6]
    rows.append({'page':p['page_number_1_based'],'date':date,'summary':'；'.join(bullets),'text_excerpt':text[:400].replace('\n',' / ')})
(base/'page_summaries.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(base/'page_summaries.json')
