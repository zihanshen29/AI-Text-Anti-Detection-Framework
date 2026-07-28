# Reliability Optimization Task Card Rev 2 - 2026-07-28

**Status:** preregistered for a new, independent Terra execution task
**Target release:** v1.3.0 reliability release candidate
**Planner/reviewer:** Sol (`gpt-5.6-sol`, max reasoning)
**Executor:** Terra (`gpt-5.6-terra`, max reasoning)
**Repository base:** `1f962b5e311d167597a4572dac6048b0b8f86adb`
**Base tree:** `a44d54e7637613f76c6e3df29c6abf2af02700c8`
**Base tag:** `v1.2.0`
**Sol branch:** `sol/optimization-plan-rev2-20260728`
**Sol worktree:** `E:\app\.worktrees\ai-text-antidetection-v1.3.0-sol-rev2`
**Card path:** `ai-detection-workflow/meta/proposals/optimization_plan_rev2_20260728.md`

This card is a new durable authorization boundary. It is self-contained. The
executor must not read, amend, continue, or treat any earlier optimization card
or failed execution as authority.

## 1. Objective

Produce a finite v1.3.0 reliability upgrade that makes the existing offline
workflow deterministic enough to serve as an auditable gate. Correctness,
stable provenance, and reproducible evidence take priority over adding detector
rules.

The release must:

1. Correct Chinese rule-machine semantics, including placeholder patterns,
   malformed C-08 entries, context whitelist application, and cross-rule span
   deduplication.
2. Wire deterministic tools into Layer 0, Layer 1, and Layer 2 as mandatory
   evidence gates.
3. Make plan preflight round-aware and multi-file-aware.
4. Replace conflicting prose contracts with one machine-readable workflow
   contract and enforce it at runtime and in CI.
5. Remove survivorship bias from batch aggregation.
6. Expand fidelity coverage, remove unconditional all-window overlap
   comparison, and add stdlib-only regression tests plus CI.

Success means that command-line behavior, active workflow documentation,
templates, tests, and machine-readable contracts agree. Success does not mean
that any external AI detector score is predicted or improved.

## 2. Non-goals

- No external detector integration, calls, score simulation, or claimed
  correlation to GPTZero, Turnitin, CNKI, Wanfang, VIP, or similar services.
- No new detector-rule families or broad expansion of phrase lists.
- No rewriting, regeneration, deletion, renaming, normalization, or cleanup
  under `meta/provider_articles/**` or `meta/generated_articles/**`.
- No modification of historical evaluation reports or existing task cards.
- No continuation, amendment, cherry-pick, or repair of a previous Sol/Terra
  run.
- No BrainMem operation.
- No push, pull request, release publication, or tag.
- No broad README marketing rewrite. Root `README.md` is protected.
- No non-stdlib Python runtime dependency. PyYAML, pandas, numpy, rapidfuzz,
  and similar packages are prohibited.
- No global Git configuration writes. Ownership handling is command-local
  `git -c safe.directory=<repo> ...` only.

## 3. Frozen read-only evidence

The following defects exist at the exact base and define the implementation
target:

- `随着人工智能的发展` does not match C-02 because
  `随着...的发展` is treated as a literal.
- C-08 stores `最后；第一` and `第四；一是` as single literals, so `最后`,
  `第一`, `第四`, and `一是` are missed.
- `生态环境`, `数字化转型`, and `控制闭环` are counted as actionable even
  though the prose whitelist protects them.
- Exact cross-rule duplicate literals such as `但是`, `此外`, and `然而`
  inflate summed totals.
- The five offline tools are described but are not mandatory Layer 0/1/2
  gates; plan preflight is single-document and cannot select a round.
- Active workflow contracts disagree about round counts, D/A+D tier handling,
  anti-regression thresholds, audit optionality, and rollback granularity.
- Batch evaluation excludes low-quality valid outputs from its primary mean.
- Guardrail extraction misses common numeric, citation, heading, and label
  forms.
- Overlap comparison performs an unconditional current-window by prior-window
  scan and scales quadratically in ordinary cases.
- No tracked CI workflow or stdlib unittest suite exists.

The previous failed preregistration established one additional planning fact:
cross-worktree frozen hashes must not be calculated from checkout bytes when
Git EOL conversion is possible. Rev 2 therefore uses only canonical Git blob
payloads for tracked frozen inputs.

## 4. Hash protocol

### 4.1 Hash domains

Three hash kinds are defined. They are not interchangeable.

1. `git_blob_sha256`
   - Use only for tracked files frozen at a named Git revision.
   - Resolve the object with
     `git rev-parse <source_revision>:<path>`.
   - Read bytes only with `git cat-file blob <git_blob_oid>`.
   - Calculate SHA-256 directly over those bytes.
   - Never read the checkout file to generate or verify this value.

2. `worktree_raw_sha256`
   - Use for snapshots or generated artifacts created inside one Terra run.
   - Calculate SHA-256 over `Path.read_bytes()` in that same worktree.
   - Never compare this value across Sol and Terra worktrees.
   - Runtime plan/post-round manifests must label these hashes explicitly.

3. `normalized_lf_utf8_sha256`
   - Optional and unused by the frozen input manifest below.
   - Allowed only for an explicitly declared text-comparison purpose.
   - Read bytes, remove one leading UTF-8 BOM if present, decode strict UTF-8,
     replace CRLF with LF, then replace remaining CR with LF, encode UTF-8
     without BOM, and hash the resulting bytes.
   - Invalid UTF-8 is a protocol error; no replacement decoding is allowed.

`core.autocrlf`, checkout EOLs, and local Git conversion settings must not
affect `git_blob_sha256`. `Get-FileHash` on a checkout path, `Get-Content`,
PowerShell text pipelines, or `Path.read_bytes()` on a checkout file are
forbidden for cross-worktree frozen-input verification.

### 4.2 Canonical algorithm

For every manifest entry, verification must perform these exact logical steps:

```python
oid = subprocess.run(
    ["git", "-c", f"safe.directory={repo}", "-C", repo,
     "rev-parse", f"{source_revision}:{path}"],
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
).stdout.decode("ascii").strip()

blob_bytes = subprocess.run(
    ["git", "-c", f"safe.directory={repo}", "-C", repo,
     "cat-file", "blob", oid],
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
).stdout

digest = hashlib.sha256(blob_bytes).hexdigest()
```

The verifier must compare both `git_blob_oid` and `sha256`. The Git object ID
is the repository's object-format identifier; `sha256` is explicitly the
SHA-256 of the blob payload.

### 4.3 Frozen canonical blob manifest

This manifest was recomputed from the exact base revision using
`git rev-parse <base>:<path>` followed by `git cat-file blob <oid>`. No value
was copied from an earlier task card and no checkout file was hashed.

<!-- FROZEN_BLOB_MANIFEST_BEGIN
[
  {
    "path": "ai-detection-workflow/rules/zh/rules.yaml",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "285e652c223468b3944e982a7576a76a2d923cda",
    "sha256": "48275d8bab4b9066f38fcfd3e3a512f146176b290eaaf3392a7f2f918ddfbb1b",
    "blob_size": 11898
  },
  {
    "path": "ai-detection-workflow/rules/zh/context_whitelist.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "ca6f649c161be07dfceb09f8a8c2d8062b0c5dbb",
    "sha256": "f8445b9620659751d83d1f5f1a259ebb3e6040a200f18490f332781028ed6ee2",
    "blob_size": 4198
  },
  {
    "path": "ai-detection-workflow/tools/tool_common.py",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "12a7f1aa42f1194486aaf20d34fb31c24cab0681",
    "sha256": "4d7167a444ad837b266993696578ccbbebf017d40020b927ada7148d051804d9",
    "blob_size": 4320
  },
  {
    "path": "ai-detection-workflow/tools/scan_rules.py",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "15c5d439f9e2126f4de220ea30e18be55903f1f8",
    "sha256": "e060257592a281497a5c056a48c9acafd2eaa09a43a8e133771d06a7feea156e",
    "blob_size": 7565
  },
  {
    "path": "ai-detection-workflow/tools/preflight_plan.py",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "c4dcb73c6102d2861511b9f3a706cbc0271aa1b7",
    "sha256": "09c855c6a171df3e54df82ec14303274170cedefbac8788b4d0108b9a64fac14",
    "blob_size": 3500
  },
  {
    "path": "ai-detection-workflow/tools/guardrails_diff.py",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "8eef2a2c29a3173bb037df586a3293f1c97123e6",
    "sha256": "1be89ef946b88e01fba987e6f20eea96c604f8447169e81c87de4520d5dc2aec",
    "blob_size": 4168
  },
  {
    "path": "ai-detection-workflow/tools/overlap_check.py",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "0f5857daa88d09d27b7f39842e23a69015f2f9c2",
    "sha256": "84da69c2db54603bd15f4e9a25035fd4e15a692bdac74b4b6afe2185ed15ada3",
    "blob_size": 5236
  },
  {
    "path": "ai-detection-workflow/workflow/discovery.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "2e4f4ec044b2faa05e614757e3d160eb5294eab2",
    "sha256": "03a4c6cf1467f4ee9103a766cb60515fae93b175c29e491d8649bcaa6f0d84f1",
    "blob_size": 13769
  },
  {
    "path": "ai-detection-workflow/workflow/planning.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "c1a5b06720c162489309cec0661c7d7fef7a1fc5",
    "sha256": "c107e5ba1b7137ed0dc69d11ce93c0facddae648e1623cc68c6e2d2c0d042b9d",
    "blob_size": 17536
  },
  {
    "path": "ai-detection-workflow/workflow/execution.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "5991101ed16db86c2ec20cdd112b5585223126dd",
    "sha256": "c0821db43aaa63bf061b1a62c662671e844a28071c8ca6b157c35e843dbda86b",
    "blob_size": 14481
  },
  {
    "path": "ai-detection-workflow/templates/plan_output.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "5c61af3eb480bf58e8fc6194e37172c7f36bc9c6",
    "sha256": "7ded1c4797ddcbfd242125fc1024cbcd008aec66df19bf80147b6cd167ddd1e6",
    "blob_size": 11811
  },
  {
    "path": "ai-detection-workflow/templates/batch_eval_output.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "0fcce89151c9c3abf24630512e7e623d89c77e34",
    "sha256": "94fdae90134efc1006ca5960c71d806815db5048d7354f39056899d498de83c4",
    "blob_size": 4725
  },
  {
    "path": "ai-detection-workflow/meta/prompts/eval_prompt.md",
    "source_revision": "1f962b5e311d167597a4572dac6048b0b8f86adb",
    "hash_kind": "git_blob_sha256",
    "git_blob_oid": "87fa02371a421df3a6576304e914b090c96b749a",
    "sha256": "20c74f9f462d25d4930cc7595b5f95883d994ae23fee81ad4ac16d0c337e9482",
    "blob_size": 3056
  }
]
FROZEN_BLOB_MANIFEST_END -->

### 4.4 Failure classification

Use these definitions before any write:

- `STOP_BASE_DRIFT`: the preregistration parent, base tree, clean status,
  manifest path existence, canonical blob OID, canonical blob payload size, or
  canonical blob SHA-256 differs from this card.
- `STOP_HASH_PROTOCOL`: the manifest cannot be parsed; a hash kind is unknown;
  the exact `rev-parse` plus `cat-file blob` algorithm cannot run; output is
  passed through a text transcoder; or an executor attempts to substitute
  checkout-byte hashing for `git_blob_sha256`.
- `STOP_ENVIRONMENT`: Python 3.11+, Git, or the declared worktree is unavailable
  for reasons unrelated to repository identity or the hash protocol.

A difference between checkout bytes caused only by `core.autocrlf` is not
`STOP_BASE_DRIFT`. Rung 0 must not compare Sol and Terra checkout bytes.

## 5. Branch and worktree choice

Sol preregisters this card on:

```text
branch: sol/optimization-plan-rev2-20260728
worktree: E:\app\.worktrees\ai-text-antidetection-v1.3.0-sol-rev2
```

Terra must use a new branch and worktree:

```text
branch: terra/optimization-v1.3.0-rev2
worktree: E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2
```

After Sol commits this card, create the Terra worktree with command-local
ownership handling only:

```powershell
$env:GIT_CONFIG_GLOBAL = 'NUL'
$SolRepo = 'E:/app/.worktrees/ai-text-antidetection-v1.3.0-sol-rev2'
$Card = 'ai-detection-workflow/meta/proposals/optimization_plan_rev2_20260728.md'
$Prereg = git -c safe.directory=$SolRepo -C $SolRepo log -1 --format=%H -- $Card
git -c safe.directory=$SolRepo -C $SolRepo worktree add -b terra/optimization-v1.3.0-rev2 E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2 $Prereg
```

The preregistration commit is the commit that first introduces this card. It
must have exactly one parent, the exact base commit. Terra must not write in the
Sol worktree, and no second writer may use the Terra worktree.

## 6. Allowed Terra write scope

Terra may create or modify only:

- `.github/workflows/ci.yml`
- `ai-detection-workflow/SKILL.md`
- `ai-detection-workflow/workflow/contract.json` (new)
- `ai-detection-workflow/workflow/discovery.md`
- `ai-detection-workflow/workflow/planning.md`
- `ai-detection-workflow/workflow/execution.md`
- `ai-detection-workflow/templates/discovery_output.md`
- `ai-detection-workflow/templates/plan_output.md`
- `ai-detection-workflow/templates/changes_log.md`
- `ai-detection-workflow/templates/batch_eval_output.md`
- `ai-detection-workflow/meta/prompts/eval_prompt.md`
- `ai-detection-workflow/meta/reports/optimization_validation_20260728.md` (new)
- `ai-detection-workflow/rules/zh/rules.yaml`
- `ai-detection-workflow/rules/zh/context_whitelist.md`
- `ai-detection-workflow/rules/zh/context_whitelist.json` (new)
- `ai-detection-workflow/tools/README.md`
- `ai-detection-workflow/tools/tool_common.py`
- `ai-detection-workflow/tools/scan_rules.py`
- `ai-detection-workflow/tools/preflight_plan.py`
- `ai-detection-workflow/tools/guardrails_diff.py`
- `ai-detection-workflow/tools/overlap_check.py`
- `ai-detection-workflow/tools/workflow_check.py` (new)
- `ai-detection-workflow/tools/lint_repository.py` (new)
- `ai-detection-workflow/tools/testdata/**`
- `ai-detection-workflow/tools/tests/**` (new)

If implementation requires any other tracked path, Terra must stop with
`STOP_SCOPE` and request a new Sol card.

## 7. Protected files and state

The following are read-only:

- this Rev 2 task card and all existing files under
  `ai-detection-workflow/meta/proposals/**`;
- `README.md`;
- `LICENSE`;
- all existing files under `ai-detection-workflow/meta/provider_articles/**`;
- all existing files under `ai-detection-workflow/meta/generated_articles/**`;
- all existing files under `ai-detection-workflow/meta/reports/**`, except the
  one new validation report authorized in Section 6;
- `ai-detection-workflow/meta/rubric/offline_rubric.md`;
- `ai-detection-workflow/rules/en/**`;
- `ai-detection-workflow/rules/zh/ai_cliches.md`;
- `ai-detection-workflow/rules/zh/sentence_patterns.md`;
- `ai-detection-workflow/rules/zh/replacement_blacklist.md`;
- `ai-detection-workflow/rules/zh/detector_profiles.md`;
- every prior Sol/Terra branch, card, worktree, and execution artifact.

Do not delete or clean unrelated ignored files, including existing
`__pycache__` directories. Preserve unrelated changes if any appear.

## 8. Frozen workflow contract decisions

The release must create
`ai-detection-workflow/workflow/contract.json` with these exact values and make
runtime gates consume it:

```json
{
  "schema_version": 1,
  "release": "1.3.0",
  "rounds": {
    "allowed_total_round_counts": [3, 5, 7],
    "zero_round_discovery_allowed": true,
    "final_audit_required_when_layer2_runs": true
  },
  "editing": {
    "risk_tiers": ["A", "B", "C"],
    "sweep_is_a_tier": false,
    "tier_mixing_allowed": false,
    "exact_before_after_required": true
  },
  "anti_regression": {
    "window_tokens": 10,
    "overlap_threshold": 0.7
  },
  "rollback": {
    "unit": "whole_round",
    "continue_after_fix_failure": false
  },
  "batch_evaluation": {
    "primary_population": "all_valid_inputs",
    "quality_failure_threshold": 25,
    "hard_fail_excluded_from_primary": false,
    "only_input_invalid_excluded": true
  }
}
```

Interpretation:

- Discovery may recommend zero edits. Once Layer 2 runs, the full plan has 3,
  5, or 7 total rounds and its final round is always audit-only.
- D is not a risk tier. A sweep is a discovery/planning method. Every sweep hit
  must become an enumerated A, B, or C exact fix before approval.
- No edit round mixes A, B, and C.
- Anti-regression uses a ten-token window and 0.70 everywhere.
- An application, parse, encoding, or guardrail failure rolls back the whole
  round and stops it. Later fixes do not continue after one failed fix.
- Low-quality outputs and hard fails remain in the primary batch aggregate.
  Only invalid inputs are excluded.

## 9. Ordered implementation rungs

Each rung has a sealed validation gate. Terra may use normal red/green
development checks before committing a rung. Once the rung commit exists,
Terra runs that rung's sealed validation once. The first unexpected failure
ends the execution. Do not patch, amend, or rerun after failed sealed evidence.

All Git commands must include command-local
`-c safe.directory=E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2`.
Do not run `git config --global` or alter persistent Git configuration.

### Rung 0 - Executor preflight

**Writes:** none.

1. Read `E:\app\AGENTS.md` and this complete card.
2. Verify branch `terra/optimization-v1.3.0-rev2`, clean status, and that HEAD
   is the preregistration commit.
3. Verify HEAD has exactly one parent and that parent is
   `1f962b5e311d167597a4572dac6048b0b8f86adb`.
4. Verify the parent's tree is
   `a44d54e7637613f76c6e3df29c6abf2af02700c8`.
5. Verify the preregistration commit changes exactly one path with status `A`:
   `ai-detection-workflow/meta/proposals/optimization_plan_rev2_20260728.md`.
6. Run the canonical verifier in Appendix A. Do not hash checkout copies of
   frozen inputs.
7. Confirm Python 3.11 or newer.

**Sealed validation:**

```powershell
$env:GIT_CONFIG_GLOBAL = 'NUL'
$Repo = 'E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2'
git -c safe.directory=$Repo -C $Repo status --porcelain=v1 --branch
git -c safe.directory=$Repo -C $Repo branch --show-current
git -c safe.directory=$Repo -C $Repo rev-list --parents -n 1 HEAD
git -c safe.directory=$Repo -C $Repo rev-parse HEAD^
git -c safe.directory=$Repo -C $Repo rev-parse 'HEAD^^{tree}'
git -c safe.directory=$Repo -C $Repo diff-tree --no-commit-id --name-status -r HEAD
python --version
```

Then run Appendix A verbatim with `REV2_REPO` and `REV2_CARD` set to the Terra
worktree and card path.

**PASS condition:** clean status, exact branch, one parent, exact base/tree,
exact one-file preregistration diff, Python 3.11+, and Appendix A returns
`canonical_manifest_status: pass`.

**First-failure verdict:** `STOP_BASE_DRIFT`, `STOP_HASH_PROTOCOL`, or
`STOP_ENVIRONMENT` according to Section 4.4.

### Rung 1 - Correct rule semantics and aggregate accounting

**Commit subject:**

```text
fix(scanner): make Chinese rule hits context-aware and span-unique
```

**Required implementation:**

1. Extend the constrained rule loader without a YAML dependency. Auto rules may
   contain direct `literals`, one legacy `pattern`, and an optional `patterns`
   JSON-style list. Reject auto rules with no executable matcher.
2. Convert C-02 placeholders into bounded regex patterns. At minimum cover
   `随着...的发展`, `随着...的不断深入`, `随着...的日益普及`, and
   `在...的推动下`. Quantifiers must not cross a sentence or newline and must
   have a documented maximum span.
3. Split malformed C-08 entries so `最后`, `第一`, `第四`, and `一是` are
   independent. Lint must reject placeholder ellipses in auto literals and
   suspicious delimiter-concatenated entries.
4. Add `rules/zh/context_whitelist.json` as the machine source. Keep the
   Markdown file as human guidance pointing to the JSON source. Every JSON
   entry has an ID, rule IDs, trigger, context matcher, and disposition
   `whitelisted` or `review`.
5. Make `whitelist_ref` operational and resolve it relative to the workflow
   root. Longest containing context wins. Conflicting equal-length
   dispositions are configuration errors.
6. Collect match spans before counting. Merge exact `(start, end)` duplicates
   across rules into one hit with multiple `rule_ids`. Nested non-identical
   spans remain distinct.
7. Replace ambiguous aggregate `total_hits` with:
   `raw_rule_hits`, `raw_unique_spans`, `whitelisted_unique_spans`,
   `review_unique_spans`, and `actionable_unique_spans`. Only
   `actionable_unique_spans` is the primary before/after aggregate.
8. Per-rule output shows raw, whitelisted, review, and actionable counts. JSON
   hits include start, end, exact text, rule IDs, disposition, and whitelist
   entry IDs.
9. Whitelist-only input exits 0; actionable or review hits exit 1;
   configuration, encoding, and runtime errors exit 2.
10. Preserve the offline-only disclaimer.

**Required tests:**

- C-02 positive cases and overlong/cross-sentence negatives.
- Correct C-08 individual terms.
- Definite whitelist cases `生态环境`, `数字化转型`, and `控制闭环`.
- One review context and one isolated actionable trigger.
- C-12/S-13 exact-span deduplication.
- Baseline comparison based on `actionable_unique_spans`.
- Invalid whitelist reference and conflicting entry errors.
- Existing English behavior, without modifying English rules.

**Sealed validation:**

```powershell
$Repo = 'E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2'
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_scan_rules.py" -v
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_rule_config.py" -v
python "$Repo\ai-detection-workflow\tools\lint_repository.py" rules
git -c safe.directory='E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2' -C $Repo diff --check HEAD^..HEAD
```

**PASS condition:** all commands exit 0 and tests assert exact counts,
dispositions, and exit codes.

**First-failure verdict:** `STOP_VALIDATION`.

### Rung 2 - Centralize workflow and batch contracts

**Commit subject:**

```text
fix(contract): centralize workflow and batch evaluation policy
```

**Required implementation:**

1. Add `workflow/contract.json` with the exact Section 8 values.
2. Synchronize SKILL, discovery, planning, execution, and templates:
   - use 3/5/7, not `3-6` or `3–6`;
   - remove D as a risk tier and convert sweeps to enumerated A/B/C fixes;
   - use 0.70 for ten-token anti-regression;
   - require final audit whenever Layer 2 runs;
   - use whole-round rollback and stop after the first fix/guardrail failure.
3. Remove informal-document audit skipping and single-fix rollback-and-continue.
4. Correct `batch_eval_output.md` and `eval_prompt.md`:
   - primary mean/median include every valid input, including `<25/35` and hard
     fails;
   - exclude only input-invalid cases with reasons;
   - report valid/invalid counts, all-valid mean, median, `<25/35` count/rate,
     and hard-fail count/rate;
   - any success-only mean is labeled diagnostic and is never headline data.
5. Add contract-aware lint for stale round, tier, threshold, audit, rollback,
   and batch-exclusion forms. Historical/protected files are outside that lint.

**Required tests:**

- Contract schema and all frozen decisions.
- Every active workflow/template consumer references the contract.
- Known contradictory forms are absent from active files.
- Historical/protected files are excluded from contract lint.

**Sealed validation:**

```powershell
$Repo = 'E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2'
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_workflow_contract.py" -v
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_docs_contract.py" -v
python "$Repo\ai-detection-workflow\tools\lint_repository.py" contract
git -c safe.directory='E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2' -C $Repo diff --check HEAD^..HEAD
```

**PASS condition:** all commands exit 0 and protected historical files are
unchanged.

**First-failure verdict:** `STOP_VALIDATION`.

### Rung 3 - Make deterministic checks mandatory workflow gates

**Commit subject:**

```text
feat(workflow): enforce deterministic layer gates
```

**Required implementation:**

1. Upgrade `preflight_plan.py` to parse round headings, fix IDs, required target
   file, per-fix language for mixed plans, exact BEFORE/AFTER quote blocks, and
   secondary-scan disposition.
2. Add `--round <N|all>` and `--project-root <path>`. Resolve targets under the
   project root and reject path escape. Preserve `--doc` as documented
   backward-compatible single-file mode.
3. Preflight multiple target files. Report target, round, fix ID, BEFORE count,
   guardrail preservation, AFTER actionable hits, and disposition. Missing
   fields, path escape, zero/multiple BEFORE matches, or unacknowledged AFTER
   hits are blocking.
4. Add `workflow_check.py` with exactly:

```text
workflow_check.py discovery --text PATH --lang {en,zh,auto} --output JSON
workflow_check.py plan --plan PATH --round {N,all} --project-root PATH [--snapshot-dir PATH] --output JSON
workflow_check.py post-round --manifest JSON --output JSON
```

5. `discovery` runs encoding/language preflight, rule scan, and structural
   metrics. Hits are evidence, not a failed discovery. Complete is exit 0;
   tool/configuration error is exit 2.
6. `plan` enforces the contract and multi-file preflight. With
   `--snapshot-dir`, copy each target and write a manifest containing absolute
   and relative target paths, language, round, fixes, prior paths, overlap
   settings, snapshot paths, and explicitly labeled `worktree_raw_sha256`
   values. Exit 0 only when executable, 1 for blocking review, and 2 for error.
7. `post-round` consumes only a plan-generated manifest. It verifies target
   identity and runs guardrail, rule, structure, and configured prior-overlap
   checks. Hard fidelity/encoding/path/identity failure requires whole-round
   rollback. Rule regressions, context warnings, or overlap findings require
   review before the next round.
8. JSON evidence includes tool version, command type, contract version, UTC
   timestamp, normalized paths, explicitly labeled hash kind and values,
   component results, and result status. It must not claim detector evidence.
9. Wire commands into active workflow and templates:
   - Layer 0 cannot hand off without discovery JSON;
   - Layer 1 cannot request approval until `plan --round all` exits 0;
   - Layer 2 cannot edit until snapshot preflight exits 0;
   - Layer 2 cannot hand off until `post-round` completes;
   - CHANGES records evidence paths, hashes, outcomes, and disposition.
10. Examples use Windows PowerShell and paths anchored at the workflow root.

**Required tests:**

- Two rounds and two target files.
- Round selection.
- Path-escape rejection.
- Snapshot bytes and `worktree_raw_sha256` provenance.
- Modified-number rollback.
- Rule/structure deltas without detector calls.
- Mixed plan per-fix language requirement.
- Legacy single-file fixture.

**Sealed validation:**

```powershell
$Repo = 'E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2'
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_preflight_plan.py" -v
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_workflow_check.py" -v
python "$Repo\ai-detection-workflow\tools\lint_repository.py" gates
git -c safe.directory='E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2' -C $Repo diff --check HEAD^..HEAD
```

**PASS condition:** all commands exit 0 and tests cover multi-file, round,
snapshot provenance, and hard-failure behavior.

**First-failure verdict:** `STOP_VALIDATION`.

### Rung 4 - Strengthen fidelity, overlap performance, and CI

**Commit subject:**

```text
test(tools): expand fidelity checks and optimize overlap
```

**Required implementation:**

1. Expand guardrails for signed and Unicode-minus values, scientific notation,
   comma-grouped values, percentages, dotted versions, numeric citation
   lists/ranges, `\cite`/`\citep`/`\citet` with optional arguments, Pandoc
   citations, Markdown/LaTeX headings, and Figure/Fig./Table/Equation/Eq./
   `图`/`表`/`式` labels with dotted or hyphenated numbers.
2. Compare entity multiset, occurrence order, and nearest heading scope.
   Multiset/order/scope changes are hard failures. Emit normalized local
   context fingerprints and excerpts; changed local context is a review
   warning, not an automatic semantic claim.
3. Keep JSON and Markdown explicit about hard failure versus review warning.
4. Replace unconditional all-window comparison with an exact token-postings
   candidate accumulator. Preserve Counter-based overlap semantics and output.
   An exact-signature fast path is permitted. Document degenerate worst-case
   behavior rather than claim guaranteed linear complexity.
5. Prove equivalence to a naive reference on fixed seeded English and Chinese
   cases.
6. Add a deterministic 2000-token performance regression below eight seconds,
   with enough margin for GitHub-hosted Windows.
7. Add stdlib unittest coverage for all tools and exit codes.
8. Add `.github/workflows/ci.yml` with Windows and Ubuntu on Python 3.11.
   `actions/checkout` and `actions/setup-python` are CI bootstrap only; project
   runtime remains stdlib-only.
9. CI runs repository lint, all tests, every tool's `--help`, and diff checks.

**Sealed validation:**

```powershell
$Repo = 'E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2'
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_guardrails_diff.py" -v
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_overlap_check.py" -v
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_*.py" -v
python "$Repo\ai-detection-workflow\tools\lint_repository.py" all
git -c safe.directory='E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2' -C $Repo diff --check HEAD^..HEAD
```

Then every executable tool must return 0 for `--help`:

```powershell
$Repo = 'E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2'
$Tools = @(
  'scan_rules.py',
  'structure_metrics.py',
  'preflight_plan.py',
  'guardrails_diff.py',
  'overlap_check.py',
  'workflow_check.py',
  'lint_repository.py'
)
foreach ($Tool in $Tools) {
  & python (Join-Path "$Repo\ai-detection-workflow\tools" $Tool) --help
  if ($LASTEXITCODE -ne 0) { throw "$Tool --help failed with $LASTEXITCODE" }
}
```

**PASS condition:** all commands exit 0, equivalence and performance tests
pass, and CI contains both operating systems.

**First-failure verdict:** `STOP_VALIDATION`.

### Rung 5 - Final evidence and scope audit

**Commit subject:**

```text
docs(validation): record v1.3.0 reliability evidence
```

Create `meta/reports/optimization_validation_20260728.md` containing:

- base, Rev 2 preregistration, and Rung 4 implementation commit IDs;
- a note that the report commit is resolved after creation with
  `git log -1 --format=%H -- <report-path>`;
- ordered commit chain and every sealed command/outcome;
- canonical Rung 0 manifest result and hash protocol used;
- scanner fixture totals, whitelist, and duplicate-span evidence;
- contract and lint results;
- multi-file/round preflight evidence;
- batch primary-population evidence;
- guardrail fixtures;
- overlap equivalence and before/after timing;
- CI matrix summary;
- canonical Git blob SHA-256 for tracked changed artifacts after commit where
  applicable, and clearly labeled `worktree_raw_sha256` for pre-commit
  generated report evidence;
- protected-path audit and final status;
- the disclaimer that no external detector ran.

The report records sealed evidence. Do not rerun a failed gate to make the
report appear clean.

**Sealed validation:**

```powershell
$env:GIT_CONFIG_GLOBAL = 'NUL'
$Repo = 'E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2'
python -m unittest discover -s "$Repo\ai-detection-workflow\tools\tests" -p "test_*.py" -v
python "$Repo\ai-detection-workflow\tools\lint_repository.py" all
git -c safe.directory=$Repo -C $Repo diff --check HEAD~5..HEAD
git -c safe.directory=$Repo -C $Repo diff --name-only HEAD~5..HEAD
git -c safe.directory=$Repo -C $Repo status --porcelain=v1 --branch
```

Verify the changed-file list is a subset of Section 6 and contains no Section
7 protected path.

**PASS condition:** commands pass, only authorized files changed, the report is
complete, and the worktree is clean after the report commit.

**First-failure verdict:** `STOP_VALIDATION` or `STOP_SCOPE`.

## 10. Explicit Terra commit sequence

The Terra branch must contain exactly these five commits after the Rev 2
preregistration commit:

1. `fix(scanner): make Chinese rule hits context-aware and span-unique`
2. `fix(contract): centralize workflow and batch evaluation policy`
3. `feat(workflow): enforce deterministic layer gates`
4. `test(tools): expand fidelity checks and optimize overlap`
5. `docs(validation): record v1.3.0 reliability evidence`

Stage explicit authorized paths only. Do not use `git add -A`, `git add .`,
amend, squash, rebase, reset, or force operations. Do not modify the
preregistration commit.

## 11. Expected artifacts and generated-file policy

Expected tracked artifacts:

- `workflow/contract.json`;
- `rules/zh/context_whitelist.json`;
- `tools/workflow_check.py`;
- `tools/lint_repository.py`;
- stdlib tests under `tools/tests/` and required fixtures under
  `tools/testdata/`;
- `.github/workflows/ci.yml`;
- synchronized active files from Section 6;
- `meta/reports/optimization_validation_20260728.md`;
- five ordered Terra commits and a clean worktree.

Generated-file rules:

- The one validation report above is the only tracked generated evidence.
- Runtime JSON, snapshots, benchmarks, coverage, and test temporary files stay
  under `tempfile.TemporaryDirectory` or
  `$env:TEMP\ai-detection-workflow-v130-rev2-*`.
- Do not commit `__pycache__`, `.pyc`, logs, timing dumps, snapshots, or local
  detector output.
- Do not delete pre-existing ignored files.
- Every persisted hash states `hash_kind`; an unlabeled SHA-256 is invalid
  evidence.

## 12. Permitted executor verdicts

Terra returns exactly one:

- `READY_FOR_SOL_REVIEW`: every rung passed and the worktree is clean.
- `STOP_BASE_DRIFT`: canonical repository identity differs.
- `STOP_HASH_PROTOCOL`: canonical hash protocol or manifest is invalid or
  cannot be executed exactly.
- `STOP_SCOPE`: required work exceeds allowed paths or touches protected state.
- `STOP_ENVIRONMENT`: required runtime/worktree capability is unavailable.
- `STOP_VALIDATION`: first sealed validation failure.

Terra does not issue ACCEPT/REJECT/AMBER. Sol assigns that final review verdict.

## 13. Final executor report format

Return:

```text
Execution task: <thread id>
Verdict: <one permitted verdict>
Branch/worktree: terra/optimization-v1.3.0-rev2 at E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2
Base/prereg/final HEAD: <three SHAs>
Commits: <ordered SHAs and subjects>
Last completed rung: <0-5>
Validation: <each sealed command and outcome>
Canonical manifest: <pass or failure evidence>
Report: <absolute path or not created due to STOP>
Evidence hashes: <hash kind, path, revision/snapshot, digest>
Protected-path audit: pass/fail
Remaining worktree state: <git status summary>
Review request: verify scope, chronology, STOP discipline, provenance, hash domains, and claims.
```

## 14. Appendix A - Canonical frozen-input verifier

Set the environment values to the Terra worktree, then run this code verbatim.
It writes no file and hashes only `git cat-file blob` output for frozen inputs.

```powershell
$env:GIT_CONFIG_GLOBAL = 'NUL'
$env:REV2_REPO = 'E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2'
$env:REV2_CARD = 'E:/app/.worktrees/ai-text-antidetection-v1.3.0-terra-rev2/ai-detection-workflow/meta/proposals/optimization_plan_rev2_20260728.md'
@'
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = "1f962b5e311d167597a4572dac6048b0b8f86adb"
repo = os.environ["REV2_REPO"]
card = Path(os.environ["REV2_CARD"])


class ProtocolError(Exception):
    pass


def git_bytes(*args: str) -> bytes:
    command = [
        "git",
        "-c",
        f"safe.directory={repo}",
        "-C",
        repo,
        *args,
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise ProtocolError(f"git command failed: {args!r}: {message}")
    return result.stdout


try:
    source = card.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- FROZEN_BLOB_MANIFEST_BEGIN\s*(\[.*?\])\s*"
        r"FROZEN_BLOB_MANIFEST_END -->",
        source,
        flags=re.DOTALL,
    )
    if not match:
        raise ProtocolError("canonical manifest markers not found")
    manifest = json.loads(match.group(1))
    if not isinstance(manifest, list) or not manifest:
        raise ProtocolError("canonical manifest must be a non-empty list")

    failures = []
    for item in manifest:
        required = {
            "path",
            "source_revision",
            "hash_kind",
            "git_blob_oid",
            "sha256",
            "blob_size",
        }
        missing = sorted(required - set(item))
        if missing:
            raise ProtocolError(f"manifest entry missing fields: {missing}")
        if item["source_revision"] != BASE:
            raise ProtocolError(
                f"unexpected source_revision for {item['path']}"
            )
        if item["hash_kind"] != "git_blob_sha256":
            raise ProtocolError(f"unexpected hash_kind for {item['path']}")

        spec = f"{item['source_revision']}:{item['path']}"
        oid = git_bytes("rev-parse", spec).decode("ascii").strip()
        blob = git_bytes("cat-file", "blob", oid)
        observed = {
            "git_blob_oid": oid,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "blob_size": len(blob),
        }
        expected = {
            "git_blob_oid": item["git_blob_oid"],
            "sha256": item["sha256"],
            "blob_size": item["blob_size"],
        }
        if observed != expected:
            failures.append(
                {
                    "path": item["path"],
                    "expected": expected,
                    "observed": observed,
                }
            )

    if failures:
        print(
            json.dumps(
                {
                    "canonical_manifest_status": "base_drift",
                    "failures": failures,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    print(
        json.dumps(
            {
                "canonical_manifest_status": "pass",
                "source_revision": BASE,
                "entry_count": len(manifest),
                "hash_kind": "git_blob_sha256",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
except (OSError, UnicodeError, json.JSONDecodeError, ProtocolError) as exc:
    print(
        json.dumps(
            {
                "canonical_manifest_status": "protocol_error",
                "error": str(exc),
            },
            ensure_ascii=False,
            indent=2,
        ),
        file=sys.stderr,
    )
    sys.exit(2)
'@ | python -
```

Exit interpretation:

- `0`: canonical manifest passed.
- `1`: `STOP_BASE_DRIFT`.
- `2`: `STOP_HASH_PROTOCOL`.

## 15. Concise Terra executor prompt

```text
You are the Terra executor in a new Sol-Terra review loop. Use gpt-5.6-terra
with max reasoning. This is Rev 2, not a continuation or repair of any earlier
run.

Use only:
branch: terra/optimization-v1.3.0-rev2
worktree: E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2
task card: E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2\ai-detection-workflow\meta\proposals\optimization_plan_rev2_20260728.md
base: 1f962b5e311d167597a4572dac6048b0b8f86adb

Read E:\app\AGENTS.md and this complete card first. Run Rung 0 read-only.
Verify the sole parent, base tree, exact one-card preregistration diff, and the
canonical manifest with Appendix A. For tracked frozen inputs, use only
git rev-parse base:path plus raw git cat-file blob bytes. Never hash checkout
files across worktrees. core.autocrlf must not affect the verdict. Distinguish
STOP_BASE_DRIFT from STOP_HASH_PROTOCOL exactly as defined.

If Rung 0 passes, implement only the Section 6 scope in Rung order. Preserve
all protected and unrelated files. Use Python 3.11+ standard library only.
Make the five exact commits in Section 10, staging explicit paths only. Use
command-local safe.directory for every Git command; do not modify global Git
configuration.

Development checks may run before a rung commit. After committing a rung, run
its sealed validation once. Stop at the first declared failure and do not
patch, amend, or rerun after failed sealed evidence. Keep transient evidence
untracked except for the authorized final report. Do not modify BrainMem,
historical corpora/reports/cards, root README, remotes, tags, or prior
branches/worktrees.

Return one Section 12 verdict and the exact Section 13 evidence packet.
```
