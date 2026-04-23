#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def ahash(img: Image.Image) -> str:
    small = img.convert('RGB').resize((8, 8))
    vals = [sum(px)/3 for px in list(small.getdata())]
    avg = sum(vals) / len(vals)
    bits = ''.join('1' if v >= avg else '0' for v in vals)
    return hex(int(bits, 2))[2:].zfill(16)


def hamming_hex(a: str, b: str) -> int:
    return bin(int(a, 16) ^ int(b, 16)).count('1')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('mapping_json')
    ap.add_argument('--output', default='duplicate_candidates.json')
    ap.add_argument('--max-distance', type=int, default=6)
    args = ap.parse_args()

    mp = json.loads(Path(args.mapping_json).read_text(encoding='utf-8'))
    items = []
    for page in mp['pages']:
        for img_path in page.get('image_paths', []):
            p = Path(img_path)
            if not p.exists():
                continue
            img = Image.open(p).convert('RGB')
            items.append({
                'page': page['page_number_1_based'],
                'file': p.name,
                'path': str(p),
                'md5': hashlib.md5(p.read_bytes()).hexdigest(),
                'ahash': ahash(img),
                'size': img.size,
            })

    exact = {}
    for it in items:
        exact.setdefault(it['md5'], []).append(it)
    exact_cross = []
    for md5, group in exact.items():
        pages = sorted(set(x['page'] for x in group))
        if len(pages) > 1:
            exact_cross.append({'type': 'exact', 'md5': md5, 'pages': pages, 'items': group})

    near = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a['page'] == b['page']:
                continue
            d = hamming_hex(a['ahash'], b['ahash'])
            if d <= args.max_distance and abs(a['size'][0] - b['size'][0]) <= 40 and abs(a['size'][1] - b['size'][1]) <= 40:
                near.append({
                    'page_a': a['page'], 'file_a': a['file'],
                    'page_b': b['page'], 'file_b': b['file'],
                    'distance': d,
                    'size_a': a['size'], 'size_b': b['size'],
                })

    out = {
        'image_count': len(items),
        'exact_cross_page_duplicates': exact_cross,
        'near_duplicate_candidates': sorted(near, key=lambda x: (x['distance'], x['page_a'], x['page_b']))
    }
    dst = Path(args.mapping_json).resolve().parent / args.output
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(dst)


if __name__ == '__main__':
    main()
