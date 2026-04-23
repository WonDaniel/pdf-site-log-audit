# Scanned PDF Execution Contract

This document turns the skill guidance into an operational contract.

## Required scanned-PDF chain

For any scanned PDF, the agent must execute the following chain in order:

1. Create/select task_dir
2. Copy source PDF into task_dir
3. Run `scripts/ocr_extract.py` against the local task copy
4. Persist non-empty OCR artifacts under task_dir
5. Run `scripts/build_page_mapping.py`
6. Produce `page_image_text_mapping.json`
7. Run `scripts/find_duplicate_candidates.py`
8. Persist duplicate candidate artifacts
9. Perform agent review using OCR + mapping + candidate artifacts
10. Write final `分析报告.docx`
11. Update task status to `completed` only after completion gate passes

## Explicitly forbidden shortcuts

The following do not satisfy the scanned-PDF OCR requirement on their own:
- direct `pdf` tool prompting against the source PDF
- ad-hoc vision/model OCR in chat
- direct jump from rendered pages to final report without OCR artifacts
- manual conclusion with no persisted OCR layer

## Minimum artifact checklist

A scanned PDF is only validly completed if these exist:
- task_dir
- local PDF copy in task_dir
- non-empty OCR artifact directory
- `page_image_text_mapping.json`
- duplicate candidate artifact
- final review artifact
- final `分析报告.docx`

## Task status discipline

Recommended states:
- `pending`
- `prepared`
- `ocr_done`
- `mapping_done`
- `candidate_done`
- `review_done`
- `report_done`
- `completed`
- `failed`

Avoid vague long-lived `running` states when a concrete stage is known.
