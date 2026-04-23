from pathlib import Path
import json, re, sys

base=Path(sys.argv[1])
mapping_path=base/'page_image_text_mapping.json'
ocr_dir=base/'ocr_text'
mp=json.loads(mapping_path.read_text(encoding='utf-8'))
key_map=['日期','施工部位','天气状况','养护单位','项目经理','路段长','突发事件']
for page in mp['pages']:
    n=page['page_number_1_based']
    md=ocr_dir/f'doc_{n-1:03d}.md'
    text=md.read_text(encoding='utf-8', errors='ignore') if md.exists() else ''
    page['raw_text']=text
    page['ocr_md_path']=str(md)
    flat=re.sub(r'[ \t]+',' ',text)
    fields={}
    for key in key_map:
        m=re.search(key + r'[:：]?\s*([^\n]{0,60})', flat)
        if m:
            fields[key]=m.group(1).strip()
    page['fields']=fields
mp['ocr_method']='macOS Vision OCR on rendered page images'
(base/'page_image_text_mapping.json').write_text(json.dumps(mp, ensure_ascii=False, indent=2), encoding='utf-8')
(base/'page_mapping.json').write_text(json.dumps(mp, ensure_ascii=False, indent=2), encoding='utf-8')
print(mapping_path)
