#!/usr/bin/env python3
"""OCR extraction helper for scanned PDF/DOCX audit workflow.

This script is intentionally workflow-oriented, not a final one-shot auditor.
It normalizes one scanned source into text/image/layout artifacts that later
steps can consume.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

API_URL = "https://pbu2m0bfy5rez5l6.aistudio-app.com/layout-parsing"
ROOT = Path(__file__).resolve().parents[1]
LOCAL_ENV = ROOT / '.env.local'


def load_local_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def post_ocr(api_url: str, token: str, file_path: Path, file_type: int) -> dict:
    body = json.dumps({
        "file": base64.b64encode(file_path.read_bytes()).decode("ascii"),
        "fileType": file_type,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }).encode("utf-8")
    req = Request(api_url, data=body, headers={
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }, method="POST")
    with urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str) -> bytes:
    with urlopen(url, timeout=120) as resp:
        return resp.read()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--token")
    ap.add_argument("--token-env", default="PDF_OCR_TOKEN")
    ap.add_argument("--file-type", type=int, choices=[0, 1], default=0)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--api-url", default=API_URL)
    args = ap.parse_args()

    src = Path(args.input).expanduser().resolve()
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    imgs = out / "imgs"
    imgs.mkdir(exist_ok=True)

    load_local_env(LOCAL_ENV)
    token = args.token or os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"Missing OCR token. Pass --token or set environment variable {args.token_env}.")
    data = post_ocr(args.api_url, token, src, args.file_type)
    (out / "raw_ocr_response.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    result = data["result"]
    for i, res in enumerate(result.get("layoutParsingResults", [])):
        (out / f"doc_{i}.md").write_text(res["markdown"]["text"], encoding="utf-8")
        for img_path, img_url in res["markdown"].get("images", {}).items():
            dst = out / img_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(download(img_url))
        for img_name, img_url in res.get("outputImages", {}).items():
            (out / f"{img_name}_{i}.jpg").write_bytes(download(img_url))

    print(out)


if __name__ == "__main__":
    main()
