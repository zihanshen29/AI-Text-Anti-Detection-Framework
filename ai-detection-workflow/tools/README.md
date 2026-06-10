# Offline Tooling

These tools provide deterministic offline checks for the workflow. They do not call external AI detectors, do not estimate detector scores, and use only the Python standard library.

## Exit Codes

- `0`: check completed with no findings, or metric-only output completed.
- `1`: check completed and found rule hits or guardrail/overlap findings.
- `2`: runtime or preflight error, including unreadable files, invalid UTF-8, or encoding/language anomalies.

## Paths and Encoding

- Relative input paths resolve against the `ai-detection-workflow/` root (the directory containing `tools/`), not the caller's working directory. `meta/...` and `tools/testdata/...` therefore work from any cwd; cwd-relative shortcuts like `testdata/...` from inside `tools/` do not.
- stdout/stderr are forced to UTF-8, so the tools always emit UTF-8 bytes regardless of console codepage. Redirection is byte-clean in cmd.exe, Git Bash, and PowerShell 7+. Windows PowerShell 5.1 re-encodes `>` output with the console codepage and will mangle Chinese rule names; there, run `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` first, or redirect via cmd/bash.

## `scan_rules.py`

Counts machine-readable `rules/<lang>/rules.yaml` literal and regex hits in one file or a source/rewrite pair. Manual structural rules are listed but not counted.

```powershell
python tools\scan_rules.py --baseline meta\provider_articles\run_20260520\deepseek\topic_05.md --text meta\provider_articles\run_20260520_rewritten_zh\deepseek\topic_05.md --lang zh
```

Negative regression fixture: this sample is intentionally invalid for English scanning and should exit `2`.

```powershell
python tools\scan_rules.py --text meta\provider_articles\run_20260520\gemini\topic_04.md --lang en
```

Disclaimer: Offline literal hits only; not a detector score.

## `structure_metrics.py`

Reports deterministic structural proxies such as sentence-length CV, paragraph-length CV, punctuation diversity, em-dash count, spaced-hyphen count, 500-token type-token ratio, and adjacent paragraph prefix repetition.

```powershell
python tools\structure_metrics.py --baseline meta\provider_articles\run_20260520\deepseek\topic_01.md --text meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_01.md --lang en
```

Disclaimer: Structural proxies only; no validated correlation to any external detector.

## `preflight_plan.py`

Parses `plan.md` fix blocks and checks that every `BEFORE` string appears exactly once in the target document.

```powershell
python tools\preflight_plan.py --plan tools\testdata\preflight_plan_sample.md --doc tools\testdata\preflight_doc_once.md
```

## `guardrails_diff.py`

Compares source/rewrite guardrails: number tokens, citation keys, Markdown headings, formula/figure/table labels, and English rewrite CJK residuals.

```powershell
python tools\guardrails_diff.py --source meta\provider_articles\run_20260520\deepseek\topic_01.md --rewrite meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_01.md --lang en
```

## `overlap_check.py`

Checks sliding-window overlap against a prior version. English uses word tokens; Chinese uses overlapping CJK character bigrams.

```powershell
python tools\overlap_check.py --current tools\testdata\overlap_a.md --prior tools\testdata\overlap_a.md --window 5 --threshold 0.7
```

## `tool_common.py`

Shared helper module for UTF-8/mojibake preflight, constrained YAML loading, language inference, and Markdown table rendering. It is imported by the command-line tools and is not intended to be run directly.

## Test Data

`tools/testdata/` contains deterministic fixtures used by the self-checks:

- `preflight_plan_sample.md`
- `preflight_doc_once.md`
- `preflight_doc_zero.md`
- `preflight_doc_multi.md`
- `guardrails_source.md`
- `guardrails_rewrite_pass.md`
- `guardrails_rewrite_number_fail.md`
- `overlap_a.md`
- `overlap_unrelated.md`
