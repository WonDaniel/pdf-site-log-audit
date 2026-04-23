#!/bin/zsh
# Example only. Replace batch name and task JSON path before use.

openclaw cron add \
  --name '扫描件PDF批处理推进' \
  --cron '*/10 * * * *' \
  --tz 'Asia/Shanghai' \
  --session isolated \
  --message "$(cat <<'EOF'
[cron:<batch-name>] Use the pdf-site-log-audit skill. Read <batch-task-json>. Pick exactly one pending file. Determine whether it is digital-native or scanned. If scanned: copy the source PDF into task_dir, run scripts/prepare_scanned_pdf.py first, then run scripts/ocr_extract.py on the local task copy, then run scripts/build_page_mapping.py (or scripts/build_page_mapping_local.py when folding local OCR artifacts into the canonical mapping), then run scripts/find_duplicate_candidates.py (or scripts/find_duplicate_candidates_local.py when running from local cropped artifacts), then perform agent duplicate confirmation and severe text-image mismatch review, then write/update the final 分析报告.docx beside the source PDF using the approved template. Before setting the task to completed, run scripts/validate_scanned_completion.py against task_dir and source_pdf; only if validation passes may the task be marked completed. Update the task status stage-by-stage and stop after exactly one file.
EOF
)"
