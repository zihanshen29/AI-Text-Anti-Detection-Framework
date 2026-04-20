# English Sentence Patterns — AI Detection Signatures

> **Consumed by:** Layer 0 (Discovery) during Step 4 pattern scanning.
> **Not to be read by:** Layer 2 (Execution) — executors take exact before/after pairs from `plan.md`, not rules.

## How to read this file

Each pattern entry has the same structure:

- **ID** — stable identifier, used by `discovery.md` and `plan.md` to cross-reference hits.
- **Detect** — a grep-able rule or structural check the discovery scanner runs against the document. If a pattern cannot be reduced to something mechanically detectable, it does not belong here.
- **Why flagged** — one-sentence explanation of what AI writing habit this captures.
- **Strongest detectors** — which AI detection tools give this pattern the most weight.
- **False-positive contexts** — genres where this pattern is legitimate and should not be flagged.
- **Fix direction** — general guidance for Layer 1, NOT exact rewrites. Layer 1 writes the actual before/after against the real document.

The rules are candidates, not verdicts. Layer 0 must verify each one against the actual document before including it in `discovery.md`. Patterns with zero hits should never be forwarded to planning.

---

## Discourse markers and metalinguistic openers

### P-01: Transitional adverb overuse

- **Detect:** Count paragraph-initial or sentence-initial occurrences of `Moreover`, `Furthermore`, `Additionally`, `Consequently`, `Notably`, `Importantly`, `In addition`, `In particular`, `Indeed`. Flag if the density exceeds 1 per 250 words across the document, or if any three consecutive paragraphs each begin with one of these.
- **Why flagged:** LLMs over-rely on explicit discourse markers where human writers use implicit sequencing or varied connectors. GPTZero and Pangram both train on this density.
- **Strongest detectors:** GPTZero, Pangram, Originality.
- **False-positive contexts:** formal legal writing; graduate-level philosophy; texts translated from German.
- **Fix direction:** Delete outright (usually the sentence reads fine without), or replace with a content-bearing connector that ties to the previous idea specifically (`This result also shows…`, `A related finding…`).

### P-02: Metalinguistic filler

- **Detect:** Case-insensitive search for `it is important to note that`, `it should be noted that`, `it is worth noting`, `it is worth mentioning`, `it bears emphasizing`, `note that`, `as previously mentioned`, `as discussed above`, `needless to say`. Any occurrence is a candidate; three or more in a document is a strong signal.
- **Why flagged:** These phrases carry no content; they mark the writer's act of communicating rather than the content being communicated. Human academic writers use them sparingly; LLMs use them as default hedges.
- **Strongest detectors:** GPTZero, Copyleaks.
- **False-positive contexts:** almost none in academic prose. Possibly legitimate in legal drafting where precise signposting has legal function.
- **Fix direction:** Delete the filler and start the sentence with its actual content. Rarely requires any replacement.

### P-03: Establishing opener

- **Detect:** Document-opening or section-opening matches for `In today's rapidly evolving`, `In recent years`, `With the rise of`, `As technology advances`, `In the modern era`, `In an age where`, `The field of X has seen`, `The world of X`. Also flag any opening sentence longer than 25 words whose first half is a time/trend clause.
- **Why flagged:** These are textbook LLM essay openers. They do not commit to any specific claim and serve only to delay the substance.
- **Strongest detectors:** GPTZero, ZeroGPT, Originality.
- **False-positive contexts:** genuine trend pieces where the temporal framing is the argument.
- **Fix direction:** Replace with a sentence that commits to the document's specific claim or scope. For a thesis: state the problem, not the era.

---

## Rhythmic and structural tells

### P-04: Em-dash overuse

- **Detect:** Count em-dashes (`—`, Unicode U+2014). Flag if density exceeds 3 per 300 words in academic prose or 2 per 300 words in short-form writing. Also flag any paragraph containing more than one em-dash.
- **Why flagged:** LLMs trained on Internet English over-use em-dash as a rhythmic device. Human academic writers prefer commas, semicolons, or parenthetical structure. Pangram specifically weights this.
- **Strongest detectors:** Pangram, GPTZero.
- **False-positive contexts:** creative nonfiction, fiction, personal essays — em-dash is legitimately common here.
- **Fix direction:** Replace with commas for parenthetical asides, semicolons for independent-clause joins, or period + new sentence for emphasis. Aim for fewer than one per 500 words in academic prose.

### P-05: Tricolon overuse (triple parallel structure)

- **Detect:** Search for patterns of the form `A, B, and C` where A, B, C are short noun phrases or verb phrases of similar length. Flag if more than 4 such constructions appear per 1000 words.
- **Why flagged:** The rule of three is a legitimate rhetorical device, but LLMs apply it compulsively, creating a telltale rhythm. Low burstiness in the resulting sentence lengths.
- **Strongest detectors:** GPTZero, Pangram.
- **False-positive contexts:** genuine technical enumerations (an API with three endpoints, a device with three modes) should not be flagged — these are facts, not stylistic choices.
- **Fix direction:** Break some tricolons into two-item lists or expanded prose. Avoid using three consecutive tricolons in the same paragraph.

### P-06: Uniform sentence length

- **Detect:** Compute per-sentence word counts across any 500-word window. Flag if the standard deviation is below 6 words and the mean is between 15 and 25 words.
- **Why flagged:** Human writing has burstiness — long sentences followed by short ones, parenthetical interruptions, emphatic fragments. LLMs produce medium-length sentences clustered tightly around a mean. This is the single most-weighted feature in perplexity-based detectors.
- **Strongest detectors:** GPTZero (burstiness is a named feature in their model), ZeroGPT.
- **False-positive contexts:** highly formalized writing (patents, legal contracts, technical specifications) genuinely exhibits uniform sentence length.
- **Fix direction:** Inject burstiness deliberately. Merge two short sentences into a longer compound; split one long sentence into a brief assertion plus a longer elaboration. Do not do this with fragments (`Feet leave. Feet return.`) — that is a different pattern (P-09) that moves the document away from academic register.

### P-07: Cross-sentence paragraph symmetry

- **Detect:** Within a single paragraph of 4+ sentences, flag if consecutive sentences use the same opening part-of-speech pattern (three paragraphs in a row starting with a demonstrative + noun, or an -ing participle, or a prepositional phrase). Manual scan; grep cannot easily catch this.
- **Why flagged:** LLMs produce locally-coherent paragraphs by anchoring each sentence on a similar structural template. Human writers vary.
- **Strongest detectors:** Pangram, Originality.
- **False-positive contexts:** bullet lists rendered as prose; step-by-step procedural writing.
- **Fix direction:** Reorder clauses or vary sentence openings. Break one sentence into two with different openers, or merge two sentences with a subordinating conjunction.

---

## Content-level tells

### P-08: Balanced parallel construction with repeated stem

- **Detect:** Patterns of the form `X enough to A and X enough to B`, `not just X but also Y`, `both X and Y`, `neither X nor Y` where X repeats or the two halves are conspicuously symmetric in length. Flag all occurrences in a document with more than 2 such constructions per 500 words.
- **Why flagged:** LLMs gravitate toward rhetorically balanced pairs as a polish move. Human academic writers use them more sparingly and more purposefully. The giveaway is density, not presence.
- **Strongest detectors:** Pangram, GPTZero.
- **False-positive contexts:** argumentative essays where balance-against-contrast is the thesis structure; oratorical transcripts.
- **Fix direction:** Break one half into an independent sentence; or remove one half if it was only added for symmetry. If the balance is substantive, keep one and convert the second into prose.

### P-09: Emphatic fragment clusters

- **Detect:** Any sequence of two or more sentences each under 10 words, appearing consecutively. Flag the whole sequence.
- **Why flagged:** Paradoxically, both heavy use and zero use of short sentences are signals — but the specific failure mode is the cluster: three fragments in a row (`Attitude moved first. Roll went first. Pitch followed.`). LLMs produce these when prompted to "add punch" or in outputs that have been run through a "humanize" pass that injects fragments mechanically. Human academic writers use a single emphatic short sentence surrounded by normal-length sentences.
- **Strongest detectors:** Pangram specifically flags this after it became a common humanizer output. GPTZero also catches it via low burstiness in the short-sentence direction.
- **False-positive contexts:** dialogue in fiction; sports commentary; deliberate stylistic choice in creative nonfiction.
- **Fix direction:** Merge at least two of the fragments into one compound sentence. Keep at most one short sentence in the cluster as the emphatic note.

### P-10: Hedging stack

- **Detect:** Search for co-occurring hedges within a single sentence: `may potentially`, `could possibly`, `might arguably`, `seems to suggest that`, `appears to indicate that`, `tends to generally`. Flag any single-sentence stack of two hedges.
- **Why flagged:** LLMs double-hedge from RLHF training that rewards uncertainty expression. Human academic writers hedge once per claim, not twice.
- **Strongest detectors:** GPTZero, Originality.
- **False-positive contexts:** rare — this is almost always excessive.
- **Fix direction:** Delete one hedge. Prefer the more specific one (`may` over `could possibly`).

### P-11: Filler intensifiers

- **Detect:** Search for `very`, `really`, `quite`, `rather`, `fairly`, `pretty`, `somewhat`, `highly`, `significantly` in any context where they modify adjectives that already carry the degree (`very unique`, `highly critical`, `significantly important`). Flag density > 1 per 150 words.
- **Why flagged:** LLMs pad prose with empty intensifiers. Academic writing is expected to be quantitatively precise (`48% higher`, `within the 2-sigma band`) rather than vaguely intensified.
- **Strongest detectors:** Turnitin AI, Originality (vocabulary-feature models).
- **False-positive contexts:** informal prose, blog writing.
- **Fix direction:** Delete the intensifier entirely, or replace with a measurable claim if one is available.

---

## Formulaic sentence skeletons

### P-12: "Not just X but Y" / "Not only X but also Y"

- **Detect:** Literal search for `not just`, `not only`, combined with a following `but`. Flag density > 2 per 1000 words.
- **Why flagged:** The phrase is so overused in LLM output that its presence alone moves the probability estimate. GPTZero's training data is saturated with it.
- **Strongest detectors:** GPTZero.
- **False-positive contexts:** rhetorical essays; political speeches.
- **Fix direction:** Split into two sentences (`It did X. It also did Y.`), or compress into a compound predicate (`It did both X and Y`).

### P-13: "It is worth/useful/important to..."

- **Detect:** Search for `it is worth`, `it is useful to`, `it is important to`, `it is essential to`, `it is critical to`, `it is necessary to` as sentence openers.
- **Why flagged:** Dummy-subject opener with no content. Humans usually move the point to the grammatical subject.
- **Strongest detectors:** GPTZero, Copyleaks.
- **False-positive contexts:** none at scale in academic writing.
- **Fix direction:** Rewrite with the concept as the subject: `Noting X is important` → `X matters because…`.

### P-14: "X, which Y, Z" nested relative clauses

- **Detect:** Sentences containing two or more `, which` or `, that` clauses. Flag if any sentence has three+ embedded clauses.
- **Why flagged:** LLMs nest relative clauses to avoid period decisions. Human writers break them.
- **Strongest detectors:** Originality, Turnitin AI.
- **False-positive contexts:** legal writing (which is supposed to nest).
- **Fix direction:** Break at the second `, which` and start a new sentence.

### P-15: "From X to Y" frame

- **Detect:** Phrases of the form `from X to Y`, `from X through Y to Z`, `ranging from X to Y`, especially when X and Y are abstract nouns (`from policy to implementation`, `from theory to practice`).
- **Why flagged:** LLMs use this frame as a pseudo-comprehensive gesture without committing to specifics.
- **Strongest detectors:** GPTZero, Pangram.
- **False-positive contexts:** genuinely spatial or temporal ranges (`from 2018 to 2022`, `from the kitchen to the garden`).
- **Fix direction:** Replace with a specific enumeration or a concrete case study.

---

## Tell-tale vocabulary (pattern-level, not word-list)

### P-16: Academic vocabulary over-reaching

- **Detect:** Search for `delve`, `nuanced`, `multifaceted`, `tapestry`, `intricate`, `pivotal`, `paramount`, `robust` (outside of statistical contexts), `leverage` (as a verb outside finance), `realm`, `landscape` (metaphorical), `crucial`, `comprehensive` (outside review contexts), `underscore` (as a verb). Flag density > 1 per 500 words.
- **Why flagged:** These words are almost diagnostic. `Delve` and `tapestry` alone can move GPTZero's estimate by 10+ percentage points in a short document.
- **Strongest detectors:** GPTZero, Pangram, ZeroGPT. This is the single most-weighted lexical signal in current detectors.
- **False-positive contexts:** some terms have legitimate technical meaning (`robust` in ML; `pivotal` in medicine; `leverage` in finance and physics). The rule lists these — do not blindly flag technical uses.
- **Fix direction:** Replace with more specific or more ordinary vocabulary. `delve into` → `examine` / `investigate`. `nuanced` → `specific` or delete. `multifaceted` → list the facets. `pivotal` → `decisive` or `central`.

### P-17: Verb–noun pretension

- **Detect:** Search for `utilize` (almost always `use`), `facilitate` (often `enable` or `help`), `endeavor` (often `try`), `implement` in non-code contexts (often `use` or `apply`), `conceptualize` (often `think of` or `define`), `operationalize` (rarely needed).
- **Why flagged:** LLMs prefer Latinate verbs over Germanic. Academic writing does not require it.
- **Strongest detectors:** Turnitin AI, Originality.
- **False-positive contexts:** legitimate technical verbs (`implement` when discussing software is correct).
- **Fix direction:** Use the shorter Germanic verb where the meaning is identical.

---

## Meta-patterns: detector-awareness signals

### P-18: Overused "This/That" sentence starts

- **Detect:** Flag any three consecutive sentences within a paragraph that begin with `This`, `That`, or `It`.
- **Why flagged:** LLMs use demonstrative subjects for cross-sentence cohesion instead of varying sentence openers.
- **Strongest detectors:** Pangram, GPTZero.
- **False-positive contexts:** spoken transcripts; children's writing.
- **Fix direction:** Replace one demonstrative with a content noun phrase or relocate it later in the sentence.

### P-19: Summary sentence clichés

- **Detect:** Phrases `in conclusion`, `in summary`, `to sum up`, `overall`, `taken together`, `all in all`, `ultimately` as paragraph or section closers. Flag any appearance in short-form writing (< 2000 words); flag density > 2 per major section in long-form.
- **Why flagged:** LLMs signal discourse structure explicitly. Humans trust the reader to follow.
- **Strongest detectors:** GPTZero, Copyleaks.
- **False-positive contexts:** formal oratory; structured technical reports that name their summary sections.
- **Fix direction:** Delete the signaling phrase. The summary sentence usually works without it.

### P-20: Future-work framing clichés

- **Detect:** `further research is needed`, `more work is required`, `future studies should`, `an interesting avenue for future research`, `promising direction`, `remains an open question` clustered in a concluding section.
- **Why flagged:** LLMs produce template conclusions. Real research future-work sections are specific ("add friction-cone slack at horizon steps 20–35"), not generic.
- **Strongest detectors:** GPTZero, ZeroGPT.
- **False-positive contexts:** writing aimed at general audiences where specifics are inappropriate.
- **Fix direction:** Replace generic future-work sentences with specific ones taken from the document's actual technical content. If no specifics are available, that is itself a problem for Layer 1 to flag back to the author.

---

## Novel-pattern slot

If Layer 0 encounters a pattern that reads AI-generated but does not match P-01 through P-20, record it under "Novel patterns" in `discovery.md` with a verbatim quote and a location. After the project concludes, consider adding it to this rule file with a new P-NN identifier. LLM writing styles evolve; this rule library must evolve with them.

## Detector cross-reference (summary)

| Pattern | GPTZero | Pangram | Originality | Turnitin | Copyleaks | ZeroGPT |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P-01 transitional adverb | ●●● | ●●● | ●●○ | ●○○ | ●●○ | ●●○ |
| P-02 metalinguistic filler | ●●● | ●○○ | ○○○ | ●○○ | ●●● | ○○○ |
| P-03 establishing opener | ●●● | ●●○ | ●●○ | ○○○ | ●○○ | ●●● |
| P-04 em-dash overuse | ●●○ | ●●● | ●○○ | ○○○ | ○○○ | ●○○ |
| P-05 tricolon | ●●● | ●●● | ●○○ | ○○○ | ●○○ | ●●○ |
| P-06 uniform length | ●●● | ●●○ | ●●● | ●●○ | ●●○ | ●●● |
| P-07 paragraph symmetry | ●○○ | ●●● | ●●○ | ○○○ | ○○○ | ●○○ |
| P-08 balanced parallel | ●●● | ●●● | ●○○ | ○○○ | ●○○ | ●●○ |
| P-09 fragment cluster | ●●○ | ●●● | ●○○ | ○○○ | ○○○ | ●●○ |
| P-10 hedging stack | ●●● | ●○○ | ●●● | ●○○ | ●○○ | ●●○ |
| P-11 filler intensifiers | ●●○ | ●●○ | ●●● | ●●● | ●●○ | ●●○ |
| P-12 not-just-X-but-Y | ●●● | ●●○ | ●○○ | ○○○ | ○○○ | ●●○ |
| P-13 dummy-subject opener | ●●● | ●●○ | ○○○ | ●○○ | ●●● | ●●○ |
| P-14 nested relatives | ●○○ | ●○○ | ●●● | ●●● | ●●○ | ●○○ |
| P-15 from-X-to-Y | ●●○ | ●●● | ●●○ | ●○○ | ●○○ | ●●○ |
| P-16 vocabulary (delve etc.) | ●●● | ●●● | ●●● | ●●○ | ●●● | ●●● |
| P-17 Latinate verbs | ●●○ | ●●○ | ●●● | ●●● | ●●○ | ●●○ |
| P-18 This/That starts | ●●○ | ●●● | ●●○ | ○○○ | ●○○ | ●●○ |
| P-19 summary cliché | ●●● | ●●○ | ●○○ | ●○○ | ●●● | ●●○ |
| P-20 future-work cliché | ●●● | ●●○ | ●○○ | ●○○ | ●○○ | ●●● |

Legend: ●●● strongly weighted / ●●○ moderate / ●○○ mild / ○○○ not a primary signal.

Use this table in Layer 1 when the user has a specific target detector — prioritize patterns with ●●● against that detector; deprioritize ○○○ ones. If the user's target is unknown, P-06 (uniform length) and P-16 (vocabulary) are universally weighted and safe to prioritize first.
