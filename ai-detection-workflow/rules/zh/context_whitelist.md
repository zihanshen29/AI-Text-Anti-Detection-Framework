# Chinese Context Whitelist

The machine-readable source for this policy is
[`context_whitelist.json`](context_whitelist.json). `scan_rules.py` loads that
JSON through each rule's `whitelist_ref`; this Markdown file is guidance for
reviewers and plan authors only.

## Dispositions

- `whitelisted`: a fixed or technical context. Do not create a mechanical fix.
- `review`: context is plausible but needs sentence-level human review.
- no matching entry: the hit remains actionable evidence.

The scanner evaluates every configured matcher that contains the rule hit. The
longest containing context wins. If equal-length matches disagree on the
disposition, the JSON configuration is invalid and scanning stops with exit
code 2.

## Review Guidance

`生态环境`, `数字化转型`, and `控制闭环` are protected technical or fixed
terms. `业务闭环`, concrete `痛点`, and genre-dependent `赋能` contexts need
review rather than mechanical synonym replacement. Paired forms such as
`不仅……而且……` must be evaluated as a whole; never edit only one side.

When a valid context requires a new policy, add a JSON entry with an ID, the
applicable rule IDs, trigger, context matcher, and disposition. Do not use this
document as a second machine source.
