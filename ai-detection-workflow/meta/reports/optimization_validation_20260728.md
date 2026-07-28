# v1.3.0 Reliability Validation Evidence (Rev 2)

## Identity and Scope

- Base: `1f962b5e311d167597a4572dac6048b0b8f86adb`
- Rev 2 preregistration: `058f9bd99a3fadd474073759b7ec9a63e97f4838`
- Parent base tree: `a44d54e7637613f76c6e3df29c6abf2af02700c8`
- Rung 4 implementation commit: `06cfbae5d6dc99567c7df7f6f439731d08d63a8f`
- Terra branch/worktree: `terra/optimization-v1.3.0-rev2` at
  `E:\app\.worktrees\ai-text-antidetection-v1.3.0-terra-rev2`
- Report commit resolution: after this file is committed, resolve its commit
  with `git log -1 --format=%H -- ai-detection-workflow/meta/reports/optimization_validation_20260728.md`.

No external detector was called, simulated, or used to make a score claim.
All detector-like names in historical material remained untouched.

## Canonical Frozen Inputs

Rung 0 used Appendix A verbatim. Each frozen item was resolved with
`git rev-parse <source_revision>:<path>`, read only with `git cat-file blob
<oid>`, and hashed with SHA-256 over raw blob bytes. No checkout bytes,
PowerShell text pipeline, or EOL-normalized bytes participated.

Result: `canonical_manifest_status: pass`, source revision
`1f962b5e311d167597a4572dac6048b0b8f86adb`, 13 entries, hash kind
`git_blob_sha256`. This remains independent of `core.autocrlf`.

## Ordered Commit Chain

1. `3c28612b25e3c239e7f4a1fef1f9464ba7547aa6` - `fix(scanner): make Chinese rule hits context-aware and span-unique`
2. `d107f733c3bbda9750ba4c20b1090fffd25dfa12` - `fix(contract): centralize workflow and batch evaluation policy`
3. `356d61beb72587ca24adffdacd20c0046835a35b` - `feat(workflow): enforce deterministic layer gates`
4. `06cfbae5d6dc99567c7df7f6f439731d08d63a8f` - `test(tools): expand fidelity checks and optimize overlap`
5. This report is the required fifth `docs(validation)` commit.

## Sealed Validation Evidence

All commands below exited 0 unless an explicit expected tool finding was being
tested inside a unittest fixture. No sealed gate was rerun after a failure.

### Rung 0

- `git -c safe.directory=$Repo -C $Repo status --porcelain=v1 --branch`:
  pass; clean branch `terra/optimization-v1.3.0-rev2`.
- `git -c safe.directory=$Repo -C $Repo branch --show-current`: pass; exact
  Terra branch.
- `git -c safe.directory=$Repo -C $Repo rev-list --parents -n 1 HEAD`: pass;
  `058f9bd...` had exactly one parent, `1f962b...`.
- `git -c safe.directory=$Repo -C $Repo rev-parse HEAD^`: pass; exact base.
- `git -c safe.directory=$Repo -C $Repo rev-parse 'HEAD^^{tree}'`: pass;
  `a44d54e7637613f76c6e3df29c6abf2af02700c8`.
- `git -c safe.directory=$Repo -C $Repo diff-tree --no-commit-id --name-status -r HEAD`:
  pass; exactly `A ai-detection-workflow/meta/proposals/optimization_plan_rev2_20260728.md`.
- `python --version`: pass; Python 3.11.6.
- Appendix A canonical verifier: pass; 13 raw Git blobs matched object ID,
  SHA-256 payload digest, and byte size.

### Rung 1

- `python -m unittest discover -s .../tools/tests -p test_scan_rules.py -v`:
  pass; 8 tests.
- `python -m unittest discover -s .../tools/tests -p test_rule_config.py -v`:
  pass; 6 tests.
- `python .../tools/lint_repository.py rules`: pass.
- `git -c safe.directory=$Repo -C $Repo diff --check HEAD^..HEAD`: pass.

Scanner fixture evidence: C-02 matched two bounded positive placeholders and
rejected sentence-crossing and overlong variants; C-08 found `最后`, `第一`,
`第四`, and `一是` separately. `生态环境`, `数字化转型`, and `控制闭环`
produced three whitelisted unique spans and zero actionable spans. `但是`,
`此外`, and `然而` produced six raw rule hits but three exact unique actionable
spans, each merged across C-12/S-13.

### Rung 2

- `python -m unittest discover -s .../tools/tests -p test_workflow_contract.py -v`:
  pass; 4 tests.
- `python -m unittest discover -s .../tools/tests -p test_docs_contract.py -v`:
  pass; 5 tests.
- `python .../tools/lint_repository.py contract`: pass.
- `git -c safe.directory=$Repo -C $Repo diff --check HEAD^..HEAD`: pass.

Contract evidence: exact JSON schema version 1, release 1.3.0, 3/5/7 rounds,
A/B/C editing tiers, ten-token 0.70 threshold, whole-round rollback, and
all-valid batch primary population were asserted. Active consumer lint excludes
historical/protected locations. Batch templates and prompt now report valid and
input-invalid counts, all-valid mean/median, below-25/35 count/rate, and
hard-fail count/rate; only input-invalid cases leave the primary population.

### Rung 3

- `python -m unittest discover -s .../tools/tests -p test_preflight_plan.py -v`:
  pass; 5 tests.
- `python -m unittest discover -s .../tools/tests -p test_workflow_check.py -v`:
  pass; 5 tests.
- `python .../tools/lint_repository.py gates`: pass.
- `git -c safe.directory=$Repo -C $Repo diff --check HEAD^..HEAD`: pass.

Multi-file/round evidence: a three-round fixture has two editing rounds, two
targets, and a final audit-only round. `--round 1` selects only fix 1.1;
path escape, zero/multiple BEFORE matches, unacknowledged AFTER hits, mixed
plan language omissions, and guardrail number changes are blocking. Snapshot
manifests preserve bytes and record absolute/relative target paths, languages,
rounds, fixes, prior paths, overlap settings, snapshot paths, and labeled
`worktree_raw_sha256` values. A modified number produces
`whole_round_rollback_required`; rule or structure deltas produce
`review_required`, without detector calls.

### Rung 4

- `python -m unittest discover -s .../tools/tests -p test_guardrails_diff.py -v`:
  pass; 4 tests.
- `python -m unittest discover -s .../tools/tests -p test_overlap_check.py -v`:
  pass; 4 tests.
- `python -m unittest discover -s .../tools/tests -p test_*.py -v`:
  pass; 45 tests.
- `python .../tools/lint_repository.py all`: pass.
- `git -c safe.directory=$Repo -C $Repo diff --check HEAD^..HEAD`: pass.
- Every executable tool's `--help` command passed for `scan_rules.py`,
  `structure_metrics.py`, `preflight_plan.py`, `guardrails_diff.py`,
  `overlap_check.py`, `workflow_check.py`, and `lint_repository.py`.

Guardrail fixtures cover signed and Unicode-minus values, scientific notation,
comma-grouped values, percentages, dotted versions, numeric citations,
optional-argument `cite`/`citep`/`citet`, Pandoc citations, Markdown headings,
LaTeX labels/headings, Figure/Fig./Table/Equation/Eq., and Chinese 图/表/式
labels. Entity multiset/order/heading-scope changes are hard failures. Changed
normalized local context produces a review warning with fingerprints and
excerpts, not an automatic semantic claim.

Overlap evidence: seeded English and Chinese cases matched a naive reference
exactly. On the deterministic 2,000-token benchmark (1,991 current windows),
the naive reference took 21.643503 seconds and the token-postings accumulator
took 0.243101 seconds; findings were equivalent. The implementation documents
that a repeated-token corpus can still approach quadratic candidate work.

CI evidence: `.github/workflows/ci.yml` runs Windows and Ubuntu with Python
3.11, actions/checkout and actions/setup-python as bootstrap only, repository
lint, all stdlib unittests, every tool help command, and `git diff --check`.

## Canonical Tracked Artifact Hashes

The following values are `git_blob_sha256`, calculated from raw
`git cat-file blob` payloads at Rung 4 revision
`06cfbae5d6dc99567c7df7f6f439731d08d63a8f`.

| Path | Git blob OID | SHA-256 |
| --- | --- | --- |
| `.github/workflows/ci.yml` | `3e6e7b07acb1d3875b301b657ce0331a9b3cb645` | `7e7b839ca51acd851998518a547d2af05e7e44d26b65f862116e607161197b09` |
| `ai-detection-workflow/rules/zh/context_whitelist.json` | `e700c73003a8fd46a0771f9938de6c0851d0210b` | `ddd203f31f5b8c2e77a9d550e5dc4a7adfda52e7be00ee9ed758f46a2c97d7d2` |
| `ai-detection-workflow/rules/zh/rules.yaml` | `baed91775174bf32bbce3f47d0d699cd62bf398a` | `297670e4ff2ce921f62c13c20b341587e689179877e77d2028cf96064056db3d` |
| `ai-detection-workflow/workflow/contract.json` | `590a1f693fe1f9ac0cf6a48ff599bdff3050f820` | `56e9ba45a1b75e58c342226179f4cd234e915007830ac96f791d878818ce582a` |
| `ai-detection-workflow/tools/tool_common.py` | `390093e2ed03e868a216b1a667e233378235a6b3` | `0e74b5c2a8306d7e98a80ecb384859e8b4019fd3ee44c16674ee07227db0c65c` |
| `ai-detection-workflow/tools/scan_rules.py` | `7cefb1210d12138b2dbde9017dda1fdfea756140` | `30ef579c19d4c25cacd36828e379d1f1b9005b77a66cde8b196fb22d68f337d4` |
| `ai-detection-workflow/tools/preflight_plan.py` | `1ba21101cd25f7a94748ff6bc50aed80eb9258c8` | `6d0e609000b46b993504b2379da304a3deafcce3c86cc231046534c8442b9796` |
| `ai-detection-workflow/tools/workflow_check.py` | `178bb9ba38291c78d911ff200bcc7c49b4bc6b70` | `a4237819c7577223801fcc97292d75c95471c068916890cb1fa3183ed97a150f` |
| `ai-detection-workflow/tools/lint_repository.py` | `49a112c7cc6ed83e12670c7965aaaa4b287b16f9` | `55ae6194d0d5d32d2b947460602c03e1a9cfe11671e7678976215a2b16e8f853` |
| `ai-detection-workflow/tools/guardrails_diff.py` | `90c77bb741d2c2bef875b82f5bd461a616916f47` | `00a2d147518610132fac0c4d83cda2e15db38602d7488bc4082ab8a467374522` |
| `ai-detection-workflow/tools/overlap_check.py` | `551ce553043bab98ed4532cb9b36b5352480a567` | `461f7735e5c0fa048e5035a251198cd53fbc670f3f20b44eb1e6dc07e3916fab` |
| `ai-detection-workflow/tools/tests/test_scan_rules.py` | `90793984c26f513e4c8acc47157514ada3b9a416` | `5d275a4987d6c9cf8c6590e79f66e0e66c4b397fe2f85505c87d6b230934b470` |
| `ai-detection-workflow/tools/tests/test_workflow_check.py` | `176640bbb7aee389a8860a7a9d4031ce9d8989fa` | `c718c6a395933ebfad7efbb63cf55b42ef859ba3314ceca22f259aade333e2e7` |
| `ai-detection-workflow/tools/tests/test_guardrails_diff.py` | `c3da16ba412e6f5f79236b352061b5aaed48c5df` | `217e6f4ded32cb4a89da6e1fa867242699d355379176178e7389598ebbc1214d` |
| `ai-detection-workflow/tools/tests/test_overlap_check.py` | `15b944bfd6cf2b43260f2111d517d65b7b06b4a5` | `8a60e464c28c98dd5a42425b803ed72c6d7e33009c9c4f652b4ebf949d2c257c` |

Supplemental complete ledger, same revision and hash domain:

| Path | SHA-256 |
| --- | --- |
| `ai-detection-workflow/SKILL.md` | `4912c4e83f2288ad6c7cec1a1ae18f8e6fa84a10eb7457c868a8965e325c81cd` |
| `ai-detection-workflow/meta/prompts/eval_prompt.md` | `a33431c9192a47f19b2f8394d5af6fcfd9e5b6aba6025c582a6502e870adfa31` |
| `ai-detection-workflow/rules/zh/context_whitelist.md` | `184b82930d2f5275f99167be86ff1777aa2037ff92a2abb11c79d93f0b419a73` |
| `ai-detection-workflow/templates/batch_eval_output.md` | `ce3db58b6fa5b3abcf9836f6dd1740c3316c7a23ff788874d0ccaf5ff58e9a1e` |
| `ai-detection-workflow/templates/changes_log.md` | `337a130aee2b26454076ad4b5513b152057c05a814103e807f4737dfdc61ac13` |
| `ai-detection-workflow/templates/discovery_output.md` | `22572a77127d66ca7a778402b9b6c9482bf545d3345c11ee482520d1c81c933b` |
| `ai-detection-workflow/templates/plan_output.md` | `a3ffeb084ea849b6066cde323887be2193275bf96576ba1cebfe8e259909e079` |
| `ai-detection-workflow/tools/README.md` | `7a128d6af235914cea4dd724a39adf364b599b666b44d0aa6b3e51f7ecaa6c93` |
| `ai-detection-workflow/tools/testdata/workflow_plan_two_targets.md` | `2d4f0fea5b2390abed603ccd929130e88058f0d4550ab2f8373bdbcc01141bae` |
| `ai-detection-workflow/tools/testdata/workflow_prior_one.md` | `85c0948970a2d612602aa3731de321990c7710c4702ba867c599f69c22e0417a` |
| `ai-detection-workflow/tools/testdata/workflow_target_one.md` | `2db65515d4577997351479292271e694cd272caa5256e03cc48ff6f56e798765` |
| `ai-detection-workflow/tools/testdata/workflow_target_two.md` | `950b4aefeec5caee1b2ab1c77be434b57501a18ee78083f38ae0abbef4179cd7` |
| `ai-detection-workflow/tools/tests/test_docs_contract.py` | `8ad311b1e4dbae56ea9f82cebf18689a10089c80e65753bbb780fa80fd5a94dd` |
| `ai-detection-workflow/tools/tests/test_lint_repository.py` | `404800f8c46014c482192419b33512d490b26a2836394583a61c570e154898aa` |
| `ai-detection-workflow/tools/tests/test_preflight_plan.py` | `adf882a2a7a7ec99133c10a5d379a12c91cde421c7d0fc9647b0e100271b841a` |
| `ai-detection-workflow/tools/tests/test_rule_config.py` | `bab696f90c5adbaa916122bdf495d3a676a0b3a54cca67d11ea66994fe336ed0` |
| `ai-detection-workflow/tools/tests/test_structure_metrics.py` | `911e78bf6ef0ee8829033f1fe6f1a638203f294940e4a854a2864f031238579c` |
| `ai-detection-workflow/tools/tests/test_tool_help.py` | `60903f8e292c8885595adc2f02e52a57ec9800936c56a03b6ad1de45626f254b` |
| `ai-detection-workflow/tools/tests/test_workflow_contract.py` | `ffd3ffb7125704a9bae528b427a1a973727d4313cc2c9c6f00f247c970e38902` |
| `ai-detection-workflow/workflow/discovery.md` | `a77a3b76e71b210e5a784a6a8e1cc3f13e1319bb40c64d76fe2610d382697df1` |
| `ai-detection-workflow/workflow/execution.md` | `eb30b984a93f8cbfd3d4028da48b1f8ba51135796555eba57ac3d7e98747c330` |
| `ai-detection-workflow/workflow/planning.md` | `9fb2e6b185ee9eea8583b46eb0ac16d47d36f10fefd285cbd54c59f61d7856df` |

## Report Snapshot and Scope Audit

The following hash is explicitly a `worktree_raw_sha256`, calculated with
`Path.read_bytes()` on this generated report's pre-commit snapshot immediately
before the placeholder in this evidence line was finalized. It is local-run
evidence only and must not be compared across worktrees:

`22dde58189e0141d6d01c066f6334172310548ab7d8b7e69678252ab3122a1fa`

Protected-path audit before the report commit found 36 changed paths from the
preregistration through Rung 4, all inside Section 6. No root README, LICENSE,
historical corpus/report/card, English rules, or other protected path changed.
The sole Rung 5 path is the explicitly authorized report itself. Rung 5's
post-commit sealed status and changed-file audit are recorded in the final
executor evidence packet because the report must be committed before that seal
can run.

## Residual Risks

- The candidate accumulator remains exact but repeated-token inputs can be
  expensive in the documented degenerate case.
- Offline rule, structure, overlap, and fidelity evidence is not a proxy for
  an external detector score.
- Workflow plan parsing is intentionally constrained to the documented
  Markdown format; unstructured plans correctly require review rather than
  inference.
