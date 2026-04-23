#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import argparse


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('base_dir', help='Directory containing source PDFs')
    ap.add_argument('output_json', help='Where to write the batch task list JSON')
    ap.add_argument('--task-root', default='tmp/pdf_audit_batch', help='Root directory for per-PDF task dirs')
    ap.add_argument('--skip', action='append', default=[], help='PDF filename to skip, repeatable')
    args = ap.parse_args()

    base = Path(args.base_dir).expanduser().resolve()
    out = Path(args.output_json).expanduser().resolve()
    task_root = Path(args.task_root).expanduser().resolve()
    skip = set(args.skip)

    rows = []
    for pdf in sorted(base.glob('*.pdf')):
        if pdf.name in skip:
            continue
        task_dir = task_root / pdf.stem
        rows.append({
            'pdf': str(pdf),
            'name': pdf.name,
            'task_dir': str(task_dir),
            'status': 'pending'
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)
    print('count', len(rows))


if __name__ == '__main__':
    main()
