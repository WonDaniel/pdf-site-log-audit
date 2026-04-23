# pdf-site-log-audit

A project for auditing site-log style PDF / DOCX documents and generating structured Word analysis reports.

It is suitable for engineering, maintenance, landscaping, greening, municipal, patrol, and similar ledger-style documents, especially when pages contain both:
- date
- weather
- work location
- work description
- construction / maintenance photos

## What this project does

This is not a single script. It is a complete workflow.

The goal is to turn raw documents into a reviewable, traceable, batch-friendly audit flow, and finally generate one `分析报告.docx` per source document.

Typical outputs include:
1. OCR or extracted text layer
2. image layer plus page mapping
3. duplicate-image findings
4. clear text-image mismatch findings
5. final `分析报告.docx`

## What it can do

This project mainly handles two classes of problems:

### 1. Duplicate-image review
Detect whether construction / maintenance photos were reused across different pages, then group and report them.

### 2. Text-image mismatch review
Combine page text and page images to identify clear, severe, and not reasonably explainable contradictions.

The project uses a "script normalization + agent final judgment" model:
- scripts handle OCR, mapping, candidate generation, and status persistence
- the agent handles final review and judgment

## Supported documents

Typical examples:
- engineering logs
- maintenance logs
- construction logs
- patrol / inspection logs
- landscaping / greening / municipal ledgers

Supported inputs:
- PDF
- DOCX

The real branching point is:
- digital-native documents
- scanned / image-based documents

## Workflow overview

### Phase 1: document normalization

For digital-native documents:
- extract text directly
- extract embedded images
- build page / image mapping

For scanned documents:
- run OCR first
- generate text, image, and layout intermediate layers
- build `page-image-text mapping`
- generate duplicate-image candidates

### Phase 2: audit judgment

#### Duplicate-image review
- scripts generate candidates first
- the agent then performs visual review and final grouping

#### Text-image mismatch review
- scripts perform rule-based checks first
- the agent then performs page-by-page multimodal judgment

## Final report rules

Each source document should end with one `分析报告.docx`.

By default the report contains only two sections:
1. `重复图片问题`
2. `明确的图文不符问题`

Principles:
- write `未发现...` when no issue exists
- do not write speculative conclusions
- do not present sampling as full-document review
- when date/weather contradiction is caused only by the same duplicated photo being reused, record it under `重复图片问题` by default

## How to use it

This project is intended to be used through an agent workflow.

In normal use, a human does not need to run every script manually. The agent should follow the skill instructions, call the scripts, advance the workflow, and produce the final reports.

For long or batch tasks, the recommended mode is:
- background async execution
- OpenClaw cron continuation

## Deployment / runtime requirements

### 1. OCR token
Running OCR requires a valid token.

If the current environment does not already have one, obtain the required OCR credential from Paddle.

Do not hardcode it in code and do not commit it to Git. Provide it at runtime through environment variables.

### 2. Python environment
The project scripts are intended to run with Python.

### 3. Agent environment
The recommended deployment model is to let an agent orchestrate the workflow, rather than treating the project as a one-shot single-script tool.

## Directory structure

```text
pdf-site-log-audit/
├── SKILL.md
├── SKILL_zh.md
├── README.md
├── README_en.md
├── LICENSE
├── references/
└── scripts/
```

## Key files

- `SKILL.md`: English skill definition and execution rules
- `SKILL_zh.md`: Chinese description
- `references/`: templates, cron references, execution constraints
- `scripts/`: OCR, mapping, candidate generation, batch progression, and validation scripts

## Project positioning

This is a workflow-oriented project, not a "one script solves everything" tool.

Its priorities are:
- reviewability
- durable batch execution
- agent-driven orchestration
- keeping the final judgment layer in human / multimodal review
