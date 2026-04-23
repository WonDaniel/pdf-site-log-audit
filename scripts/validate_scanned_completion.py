from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_STATUSES = [
    'pending',
    'prepared',
    'ocr_done',
    'mapping_done',
    'candidate_done',
    'review_done',
    'report_done',
    'completed',
    'failed',
]


def nonempty_dir(path: Path) -> bool:
    return path.exists() and path.is_dir() and any(path.iterdir())


def find_ocr_dir(task_dir: Path) -> Path | None:
    for name in ('ocr_text', 'ocr'):
        p = task_dir / name
        if nonempty_dir(p):
            return p
    return None


def find_candidate_artifact(task_dir: Path) -> Path | None:
    for name in ('duplicate_candidates.json', 'candidate_review.json'):
        p = task_dir / name
        if p.exists():
            return p
    return None


def find_review_artifact(task_dir: Path) -> Path | None:
    for name in ('duplicate_review.json', 'duplicate_review_manual.json', 'final_review.json', 'run_summary.json'):
        p = task_dir / name
        if p.exists():
            return p
    return None


def validate(task_dir: Path, source_pdf: Path):
    local_pdf = task_dir / source_pdf.name
    report = source_pdf.with_name(source_pdf.stem + ' 分析报告.docx')
    mapping = task_dir / 'page_image_text_mapping.json'

    checks = {
        'task_dir_exists': task_dir.exists() and task_dir.is_dir(),
        'local_pdf_copy_exists': local_pdf.exists(),
        'ocr_artifact_dir_exists': find_ocr_dir(task_dir) is not None,
        'page_image_text_mapping_exists': mapping.exists(),
        'duplicate_candidate_artifact_exists': find_candidate_artifact(task_dir) is not None,
        'final_review_artifact_exists': find_review_artifact(task_dir) is not None,
        'final_report_exists': report.exists(),
    }
    ok = all(checks.values())
    return {
        'ok': ok,
        'task_dir': str(task_dir),
        'source_pdf': str(source_pdf),
        'local_pdf': str(local_pdf),
        'report': str(report),
        'checks': checks,
        'ocr_dir': str(find_ocr_dir(task_dir)) if find_ocr_dir(task_dir) else None,
        'candidate_artifact': str(find_candidate_artifact(task_dir)) if find_candidate_artifact(task_dir) else None,
        'review_artifact': str(find_review_artifact(task_dir)) if find_review_artifact(task_dir) else None,
    }


def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: python validate_scanned_completion.py <task_dir> <source_pdf>')
    task_dir = Path(sys.argv[1])
    source_pdf = Path(sys.argv[2])
    print(json.dumps(validate(task_dir, source_pdf), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
