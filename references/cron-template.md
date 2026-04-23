# PDF Site Log Audit Cron Template

Use this pattern when running scanned-PDF rework as a background batch.

## 1. Prepare batch task file

Create a JSON file such as:
- `tmp/<batch_name>_tasks.json`

Each entry should contain at least:

```json
{
  "source_pdf": "/absolute/path/to/source.pdf",
  "task_dir": "/absolute/path/to/task_dir",
  "status": "pending",
  "notes": ""
}
```

## 2. Recommended cron cadence

Default:
- every 10 minutes
- one file per run
- isolated session target

## 3. Required cron message shape

The cron message should explicitly instruct the agent to:
- read the batch task JSON
- select exactly one pending file
- copy source PDF into task_dir
- run `scripts/ocr_extract.py` for scanned PDFs
- run `scripts/build_page_mapping.py`
- run `scripts/find_duplicate_candidates.py`
- perform agent duplicate confirmation and severe mismatch review
- write/update final `分析报告.docx`
- update task status stage-by-stage
- stop after one file

## 4. Example cron command

```bash
openclaw cron add \
  --name '<batch-name>' \
  --cron '*/10 * * * *' \
  --tz 'Asia/Shanghai' \
  --session isolated \
  --message '[cron:<batch-name>] Use the pdf-site-log-audit skill. Read <batch-task-json>. Pick exactly one pending file. For scanned PDFs, copy the source PDF into task_dir, run scripts/ocr_extract.py on the local copy, then run scripts/build_page_mapping.py, then scripts/find_duplicate_candidates.py, then perform agent review, write the final 分析报告.docx, update task status, and stop after one file.'
```

## 5. Completion gate reminder

A scanned PDF is not complete unless all of these exist:
- local PDF copy in task_dir
- OCR artifact directory with non-empty outputs
- `page_image_text_mapping.json`
- duplicate candidate artifact
- final review artifact
- final `分析报告.docx`

Do not mark a task `completed` without these artifacts.
