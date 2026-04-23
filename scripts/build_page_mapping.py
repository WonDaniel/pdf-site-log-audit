#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def extract_cells(text: str):
    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', text, flags=re.S | re.I)
    out = []
    for c in cells:
        c = re.sub(r'<img[^>]*>', '', c, flags=re.I)
        c = re.sub(r'<[^>]+>', '', c)
        c = re.sub(r'\s+', ' ', c.replace('\n', ' ')).strip()
        out.append(c)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('ocr_dir')
    ap.add_argument('--log')
    ap.add_argument('--output', default='page_image_text_mapping.json')
    args = ap.parse_args()

    base = Path(args.ocr_dir).resolve()
    page_map = {}
    lines = []
    if args.log:
        lines = Path(args.log).read_text(errors='ignore').splitlines()
        current_page = None
        for line in lines:
            m = re.search(r'doc_(\d+)\.md', line)
            if m:
                current_page = int(m.group(1))
                page_map.setdefault(current_page, {'doc': f'doc_{current_page}.md', 'images': [], 'layout': None})
            m2 = re.search(r'imgs/(img_[^\s]+\.jpg)', line)
            if m2 and current_page is not None:
                page_map.setdefault(current_page, {'doc': f'doc_{current_page}.md', 'images': [], 'layout': None})['images'].append(m2.group(1))
            m3 = re.search(r'(layout_det_res_(\d+)\.jpg)', line)
            if m3 and current_page is not None:
                page_map.setdefault(current_page, {'doc': f'doc_{current_page}.md', 'images': [], 'layout': None})['layout'] = m3.group(1)
    else:
        for md in sorted(base.glob('doc_*.md')):
            idx = int(re.search(r'doc_(\d+)\.md$', md.name).group(1))
            page_map.setdefault(idx, {'doc': md.name, 'images': [], 'layout': None})

    for idx, item in sorted(page_map.items()):
        md_path = base / item['doc']
        text = md_path.read_text(encoding='utf-8', errors='ignore') if md_path.exists() else ''
        cells = extract_cells(text)
        fields = {}
        for i in range(len(cells)-1):
            if cells[i] in ['日期','施工部位','天气状况','养护单位','项目经理','路段长','突发事件']:
                fields[cells[i]] = cells[i+1]
        item['page_number_1_based'] = idx + 1
        item['md_path'] = str(md_path)
        item['layout_path'] = str(base / item['layout']) if item['layout'] else None
        item['image_paths'] = [str(base / 'imgs' / name) for name in item['images']]
        item['fields'] = fields
        item['raw_text'] = text

    payload = {'source_dir': str(base), 'pages': [page_map[k] for k in sorted(page_map.keys())]}
    (base / args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(base / args.output)


if __name__ == '__main__':
    main()
