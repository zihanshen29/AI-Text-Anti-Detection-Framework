# English Tell-Tale Phrases — AI Vocabulary Signatures

> **Consumed by:** Layer 0 (Discovery) during Step 4 pattern scanning.
> **Complements:** `sentence_patterns.md` (syntactic signals). This file is the vocabulary counterpart.
> **Not to be read by:** Layer 2 (Execution).

## Scope and relation to sentence_patterns.md

`sentence_patterns.md` catches AI signals at the **sentence level** — rhythm, structure, parallelism, opener patterns. This file catches signals at the **word and short-phrase level** — individual tokens and 2-4 word expressions that are diagnostic on their own.

There is deliberate overlap: P-16 in `sentence_patterns.md` lists a handful of headline vocabulary items (`delve`, `nuanced`, `multifaceted`) at a glance. This file is the canonical, organized vocabulary library. If a word appears in both, prefer this file for detect rules.

Why vocabulary gets its own file in English: modern detectors (GPTZero, Pangram, Originality) maintain explicit AI-vocabulary dictionaries. A single instance of the wrong word can move their score by 5-10 percentage points. The cost of scanning is low, the false-positive rate is moderate (technical-use exceptions exist), and the fix is usually a single-word replacement — which makes these Tier A fixes in Layer 1.

## How to read this file

Each entry has:

- **ID** — stable identifier `V-NN` (V for Vocabulary).
- **Triggers** — the exact strings to grep.
- **Why flagged** — one-sentence explanation.
- **Technical exceptions** — genres or contexts where the word is legitimate.
- **Replacement candidates** — a short list of less-detectable alternatives. Layer 1 picks the context-appropriate one; this is guidance, not a mandate.
- **Density threshold** — when the pattern becomes a strong signal.

---

## 1. The "elevated academic" vocabulary cluster

This is the single most detector-weighted category. These words are diagnostic because LLMs use them as "sound smart" filler — human academic writers use more neutral vocabulary unless the word's specific meaning is required.

### V-01: delve (and morphs)

- **Triggers:** `delve into`, `delving into`, `delve deeper`, `delved into`.
- **Why flagged:** The single most diagnostic word in current English AI detectors. `delve` appeared in GPT-3.5 era output at ~50× human baseline frequency; detectors are trained on this.
- **Technical exceptions:** none in modern academic prose. If your document is on archaeology or mining, the literal sense might appear — still rare.
- **Replacement candidates:** `examine`, `investigate`, `analyse`, `look at`, `study`, `work through`.
- **Density threshold:** **any single instance** in an academic document is a strong signal. Treat this as hit-count matters, not density.

### V-02: nuanced

- **Triggers:** `nuanced`, `nuance` (as a standalone intensifier), `a more nuanced`.
- **Why flagged:** LLMs use `nuanced` as a hedge that sounds thoughtful without committing to specifics. Real academic writing says *what* the nuance is.
- **Technical exceptions:** legitimate in philosophy, linguistics, literary criticism where the word has technical content.
- **Replacement candidates:** delete and state the actual distinction (`distinctions between X and Y are important`); `complex`; `not straightforward`; `context-dependent`.
- **Density threshold:** any instance in technical writing; 2+ in any document.

### V-03: multifaceted

- **Triggers:** `multifaceted`, `many-faceted`, `multi-faceted`.
- **Why flagged:** Pure filler. If there are multiple facets, list them; the word itself commits to nothing.
- **Technical exceptions:** almost none.
- **Replacement candidates:** delete and enumerate the facets (`affects performance, cost, and reliability`); `complex`; `has several aspects`.
- **Density threshold:** any single instance.

### V-04: tapestry

- **Triggers:** `tapestry of`, `rich tapestry`, `woven into the tapestry`.
- **Why flagged:** Metaphor that appears in ~zero human academic prose and in overwhelming AI output. Near-deterministic signal.
- **Technical exceptions:** textile studies; some literary criticism.
- **Replacement candidates:** `range of`, `collection of`, `set of`, delete.
- **Density threshold:** any single instance.

### V-05: intricate

- **Triggers:** `intricate`, `intricacy`, `intricately`.
- **Why flagged:** Like `nuanced`, it's a hedge-adjective for "complex" that commits to nothing. LLMs over-use it.
- **Technical exceptions:** mechanical engineering (literal intricate mechanisms), biology (intricate signaling cascades) — narrow literal uses.
- **Replacement candidates:** `complex`, `detailed`, `fine-grained`, or describe the specific complexity.
- **Density threshold:** 2+ in any document; any use in a short document (< 2000 words).

### V-06: pivotal

- **Triggers:** `pivotal`, `plays a pivotal role`, `pivotal moment`.
- **Why flagged:** LLM's preferred alternative to `important` or `central`. Appears at elevated frequency in LLM output across all domains.
- **Technical exceptions:** medicine (pivotal trial — a specific regulatory term), mechanical engineering (pivot as literal joint).
- **Replacement candidates:** `central`, `decisive`, `key`, `critical`, or describe what specific role the thing plays.
- **Density threshold:** 2+ in any document.

### V-07: paramount

- **Triggers:** `paramount`, `of paramount importance`, `paramount concern`.
- **Why flagged:** Archaic elevated register that LLMs default to. Human writers mostly use `most important` or concrete comparatives.
- **Technical exceptions:** legal writing (paramount clause, paramount title are legal terms).
- **Replacement candidates:** `most important`, `the main`, `central`, `critical`.
- **Density threshold:** any single instance in non-legal contexts.

### V-08: realm

- **Triggers:** `realm of`, `in the realm of`, `within the realm`.
- **Why flagged:** Metaphorical-kingdom framing for abstract domains. Strongly LLM-preferred.
- **Technical exceptions:** fantasy writing; biology (phylogenetic realms are a technical term in some classifications).
- **Replacement candidates:** `area of`, `field of`, `domain of`, delete the phrase entirely if it's scaffolding.
- **Density threshold:** 2+ in any document.

### V-09: landscape (metaphorical)

- **Triggers:** `landscape of`, `the X landscape`, `changing landscape`, `current landscape`.
- **Why flagged:** Over-used metaphor for "state of a field". LLMs reach for it constantly.
- **Technical exceptions:** literal geography; ML literature (loss landscape, optimization landscape) where it's a specific technical term.
- **Replacement candidates:** `state of`, `field of`, `current approaches to`, delete the metaphorical frame.
- **Density threshold:** 2+ in any document outside geography/ML-theory contexts.

### V-10: robust (outside statistical contexts)

- **Triggers:** `robust`, `robustly`, `robustness`.
- **Why flagged:** LLMs apply `robust` to everything: "robust framework", "robust methodology", "robust results". Human writers reserve it for specific technical meaning.
- **Technical exceptions:** legitimate in statistics (robust estimator), ML (robustness to adversarial inputs), engineering (robust control). **This word has a real technical home.** Only flag when used loosely as a synonym for "good" or "strong".
- **Replacement candidates:** `reliable`, `stable`, `effective`, or specify what makes it robust (`tolerates X`, `works under condition Y`).
- **Density threshold:** `robust` outside its technical home, 2+ instances.

### V-11: leverage (as a verb)

- **Triggers:** `leverage`, `leveraging`, `leverages`, `leveraged`.
- **Why flagged:** Business-speak verb that LLMs apply indiscriminately. Human academic writers use `use`, `apply`, `exploit`.
- **Technical exceptions:** finance (literal leverage); physics (lever arm / mechanical leverage).
- **Replacement candidates:** `use`, `apply`, `build on`, `exploit`, `take advantage of`.
- **Density threshold:** any instance in academic/technical prose outside finance/physics.

### V-12: underscore (as a verb)

- **Triggers:** `underscore`, `underscores`, `underscored`, `underscoring`.
- **Why flagged:** LLMs default to `underscore` where humans write `emphasize`, `confirm`, `show`. Elevated register flag.
- **Technical exceptions:** typography (literal underscore character).
- **Replacement candidates:** `emphasize`, `confirm`, `show`, `highlight`, `support`.
- **Density threshold:** 2+ instances.

### V-13: crucial

- **Triggers:** `crucial`, `crucially`.
- **Why flagged:** LLMs' default word for "important". Ubiquitous in AI output, elevated frequency vs human baseline.
- **Technical exceptions:** logic and epistemology (crucial experiment is a technical term).
- **Replacement candidates:** `important`, `essential`, `necessary`, `key`, or describe why.
- **Density threshold:** 3+ instances in any document; any instance in a short document.

### V-14: comprehensive

- **Triggers:** `comprehensive`, `comprehensively`, `comprehensive understanding`.
- **Why flagged:** LLM's claim-everything word. Human academic writers scope their claims narrowly.
- **Technical exceptions:** legitimate in review articles, surveys, and explicit comprehensive tests (`comprehensive benchmark`).
- **Replacement candidates:** `thorough`, `complete`, `broad`, or narrow the claim (`systematic on X; partial on Y`).
- **Density threshold:** 2+ instances outside survey/review contexts.

### V-15: showcase (as a verb)

- **Triggers:** `showcase`, `showcases`, `showcasing`, `showcased`.
- **Why flagged:** Marketing register. Almost never appears in human academic writing; ubiquitous in LLM output.
- **Technical exceptions:** none in academic prose.
- **Replacement candidates:** `demonstrate`, `present`, `show`, `illustrate`.
- **Density threshold:** any single instance.

### V-16: embark (on/upon)

- **Triggers:** `embark on`, `embark upon`, `embarking on`.
- **Why flagged:** Narrative-voice elevation. Nobody "embarks on a literature review".
- **Technical exceptions:** literal travel/maritime contexts.
- **Replacement candidates:** `begin`, `start`, `undertake`, `carry out`.
- **Density threshold:** any single instance.

### V-17: foster

- **Triggers:** `foster`, `fosters`, `fostering`, `foster collaboration`.
- **Why flagged:** LLM's default verb for "encourage" or "support". Over-used.
- **Technical exceptions:** foster care (legal term).
- **Replacement candidates:** `encourage`, `support`, `promote`, `help`.
- **Density threshold:** 2+ instances.

### V-18: navigate (metaphorical)

- **Triggers:** `navigate the`, `navigating the`, `navigate through`, `navigate this`.
- **Why flagged:** LLMs use `navigate` for any decision or process. Human writers use `handle`, `manage`, or `work through`.
- **Technical exceptions:** literal navigation (aerospace, maritime, robotics — in robotics, this is a technical term, not a flag).
- **Replacement candidates:** `work through`, `handle`, `deal with`, `manage`, `approach`.
- **Density threshold:** 2+ metaphorical instances in non-robotics contexts.

---

## 2. Latinate vs Germanic verb preference

LLMs systematically prefer Latinate verbs over their Germanic counterparts. Academic English tolerates some Latinate register but not the consistent preference LLMs show. Detecting this cluster is harder than a word-list scan because context matters — you have to check whether the simpler verb would fit.

### V-19: utilize / utilise

- **Triggers:** `utilize`, `utilise`, `utilization`, `utilised`, `utilizing`.
- **Why flagged:** The classic. `Use` is almost always correct; `utilize` appears at 10-20× human baseline in LLM output.
- **Technical exceptions:** extremely rare. Some engineering contexts have "utilization rate" as a fixed term (CPU utilization, bandwidth utilization) — fine. Everywhere else, read aloud: if "use" fits, use "use".
- **Replacement candidates:** `use` (almost always).
- **Density threshold:** any single instance in non-utilization-rate context.

### V-20: facilitate

- **Triggers:** `facilitate`, `facilitates`, `facilitating`, `facilitated`.
- **Why flagged:** LLM substitute for `enable`, `help`, `allow`, `make possible`.
- **Technical exceptions:** legitimate when the subject is literally a facilitator (HR, meetings). In technical writing, usually replaceable.
- **Replacement candidates:** `enable`, `help`, `allow`, `support`, `make easier`.
- **Density threshold:** 2+ instances.

### V-21: endeavor / endeavour

- **Triggers:** `endeavor`, `endeavour`, `endeavored`, `endeavouring`.
- **Why flagged:** Archaic register for `try`, `attempt`, `work`.
- **Technical exceptions:** none in modern prose.
- **Replacement candidates:** `try`, `attempt`, `work on`, `aim`.
- **Density threshold:** any single instance.

### V-22: implement (non-technical)

- **Triggers:** `implement`, `implementation`, `implementing`.
- **Why flagged:** In software/engineering contexts, `implement` is a correct technical term and should not be flagged. Outside technical contexts (policy, business, education), LLMs use it where `apply`, `use`, `carry out` fits.
- **Technical exceptions:** software/hardware implementation is **not** a flag. Policy-implementation in public-administration contexts is borderline acceptable.
- **Replacement candidates (only in non-technical contexts):** `apply`, `use`, `put in place`, `carry out`.
- **Density threshold:** only evaluate in non-technical contexts; 2+ instances.

### V-23: conceptualize

- **Triggers:** `conceptualize`, `conceptualise`, `conceptualization`.
- **Why flagged:** LLM substitute for `think about`, `define`, `frame`.
- **Technical exceptions:** cognitive science and some philosophy contexts where the word has specific meaning.
- **Replacement candidates:** `think of as`, `define`, `frame`, `view as`.
- **Density threshold:** any single instance outside cognitive-science contexts.

### V-24: operationalize

- **Triggers:** `operationalize`, `operationalise`, `operationalization`.
- **Why flagged:** Social-science jargon over-used by LLMs in contexts where it doesn't belong.
- **Technical exceptions:** legitimate in social science methodology (operationalizing a construct into measurable variables).
- **Replacement candidates:** `put into practice`, `measure`, `implement`.
- **Density threshold:** any instance outside explicit social-science methodology sections.

### V-25: streamline

- **Triggers:** `streamline`, `streamlined`, `streamlining`.
- **Why flagged:** Management-speak. LLMs apply it to any process.
- **Technical exceptions:** aerodynamics (literal streamlining).
- **Replacement candidates:** `simplify`, `speed up`, `make more efficient`, `remove steps from`.
- **Density threshold:** 2+ instances outside aerodynamics.

---

## 3. Hedge words (beyond the stack in P-10)

`sentence_patterns.md` P-10 catches hedge stacks (two hedges in one sentence). This section catches individual hedge vocabulary that's over-used.

### V-26: arguably

- **Triggers:** `arguably`.
- **Why flagged:** LLM insertion for plausibility. Appears at elevated frequency; academic writing either commits to a claim with citations or states the disagreement explicitly.
- **Technical exceptions:** acceptable when followed by `arguably the most X, though Y would also qualify` — actual acknowledgment of alternatives.
- **Replacement candidates:** delete, or replace with explicit comparison.
- **Density threshold:** 2+ instances.

### V-27: seemingly

- **Triggers:** `seemingly`, `seemed to`, `appears to`.
- **Why flagged:** Double-hedging. If you're reporting a result, commit; if you're reporting an impression, say whose impression.
- **Technical exceptions:** legitimate in phenomenology or perception-related research.
- **Replacement candidates:** commit to the claim if the data supports it; specify the observer if not.
- **Density threshold:** 3+ instances.

### V-28: essentially / basically / fundamentally

- **Triggers:** `essentially`, `basically`, `fundamentally`.
- **Why flagged:** LLMs use these as confidence-builders that commit to nothing. Academic writing states the actual thing.
- **Technical exceptions:** mathematics/physics (`fundamental` as a technical adjective is fine — `fundamental theorem`, `fundamental frequency`).
- **Replacement candidates:** delete (usually the sentence works fine); or state the specific claim.
- **Density threshold:** 2+ instances per 1000 words.

### V-29: relatively

- **Triggers:** `relatively`.
- **Why flagged:** Used without specifying what the comparison is. "Relatively efficient" compared to what?
- **Technical exceptions:** when the comparison is explicit (`relatively to baseline X`, `relatively to v10`).
- **Replacement candidates:** specify the comparison, or delete if not needed.
- **Density threshold:** 3+ instances without explicit comparisons.

### V-30: largely / mostly / primarily

- **Triggers:** `largely`, `mostly`, `primarily`, `predominantly`.
- **Why flagged:** Hedging quantifiers. LLMs use these to avoid precise percentages.
- **Technical exceptions:** legitimate when the exact number isn't known and the approximation matters.
- **Replacement candidates:** give the percentage if known (`72% of cases`); if unknown, consider whether the hedge is even necessary.
- **Density threshold:** 3+ instances.

---

## 4. Opening-sentence and section-opening vocabulary

`sentence_patterns.md` P-03 catches establishing-opener sentences structurally. This catches the specific vocabulary LLMs favor in that position.

### V-31: "In today's / In the modern / In recent years"

- **Triggers:** `In today's`, `In the modern age`, `In the modern era`, `In recent years`, `In the current era`, `In an era`.
- **Why flagged:** Default LLM opener. Strongly detector-weighted.
- **Technical exceptions:** genuinely trend-focused articles.
- **Replacement candidates:** delete and start with the specific topic.
- **Density threshold:** any document-opening or section-opening occurrence.

### V-32: "The advent of / With the rise of / The emergence of"

- **Triggers:** `the advent of`, `with the rise of`, `the emergence of`, `the proliferation of`.
- **Why flagged:** LLM setup for "thing X has changed the world" style intros.
- **Technical exceptions:** genuinely historical writing about technology adoption.
- **Replacement candidates:** drop the framing, state the specific claim.
- **Density threshold:** any occurrence as a section opener.

### V-33: "It is well known that / It is widely accepted that"

- **Triggers:** `it is well known`, `it is widely accepted`, `it is common knowledge`, `as is well known`, `as is widely understood`.
- **Why flagged:** Appeal to consensus without citation. Academic writing cites or narrows the claim.
- **Technical exceptions:** almost none.
- **Replacement candidates:** cite the source (`Smith [1] showed...`) or narrow (`in the ML literature...`).
- **Density threshold:** any occurrence.

---

## 5. Closing-sentence vocabulary

Companions to `sentence_patterns.md` P-19 (summary clichés) and P-20 (future-work clichés) at the word level.

### V-34: "This paper / This work / This study" as opener

- **Triggers:** sentences beginning with `This paper`, `This work`, `This study`, `This dissertation`, `This research`.
- **Why flagged:** Over-used self-reference opener. LLMs use it to pad. Human academic writers use it sparingly — usually once in the abstract, once in the introduction, once in the conclusion.
- **Technical exceptions:** one appearance in each major structural position (abstract / intro / conclusion) is fine.
- **Replacement candidates:** let the sentence stand on its own content, or vary (`The present work`, `The results reported here`, direct topic opener).
- **Density threshold:** 4+ instances across a document; 2+ in a single section.

### V-35: "In conclusion" family

- **Triggers:** `in conclusion`, `to conclude`, `in summary`, `to summarize`, `to summarise`, `ultimately`, `overall`, `all in all`, `taken together`.
- **Why flagged:** Explicit discourse signaling. LLMs over-mark section boundaries.
- **Technical exceptions:** formal technical reports where labeled conclusion markers are expected. Even there, use at most once per major section.
- **Replacement candidates:** delete the signaling word; the content sentence usually stands fine on its own.
- **Density threshold:** 2+ instances in any document.

### V-36: "In light of" / "Given that"

- **Triggers:** `in light of`, `given that`, `in view of the fact that`, `considering that`.
- **Why flagged:** Formal-register causal connectors that LLMs over-use.
- **Technical exceptions:** legitimate when the cause-effect reasoning genuinely needs the setup.
- **Replacement candidates:** `because`, `since`, or restructure so the cause leads the sentence.
- **Density threshold:** 3+ instances.

---

## 6. Euphemism / indirection

### V-37: "The fact that"

- **Triggers:** `the fact that`, `despite the fact that`, `due to the fact that`, `owing to the fact that`.
- **Why flagged:** Padding. Academic writers say `that`, `although`, `because`.
- **Technical exceptions:** almost none.
- **Replacement candidates:** `that` (`the fact that X is true` → `that X is true`); `although`; `because`.
- **Density threshold:** 2+ instances.

### V-38: "A number of / a variety of"

- **Triggers:** `a number of`, `a variety of`, `an array of`, `a host of`, `a plethora of`, `a myriad of`.
- **Why flagged:** Vague quantifiers. LLMs reach for these instead of giving specifics.
- **Technical exceptions:** when the exact count is genuinely irrelevant and `several` reads wrong.
- **Replacement candidates:** give the count (`three approaches`); `several`; `many`; or just `some`.
- **Density threshold:** 3+ instances.

### V-39: "In order to"

- **Triggers:** `in order to`.
- **Why flagged:** Padding. `To` alone carries the same meaning.
- **Technical exceptions:** rare — when dropping `in order` would genuinely shift emphasis. Not common.
- **Replacement candidates:** `to`.
- **Density threshold:** 3+ instances.

### V-40: "Play a role in"

- **Triggers:** `plays a role in`, `play a role in`, `plays a significant role`, `plays a key role`.
- **Why flagged:** Scaffolded way to say X affects Y. Human writers just say what the role is.
- **Technical exceptions:** acting, theater (literal roles).
- **Replacement candidates:** state the specific effect (`X affects Y by Z`); `affects`; `influences`; `determines`.
- **Density threshold:** 2+ instances.

---

## 7. The "thought-leader" cluster

Vocabulary that makes the text sound like a TED talk rather than academic writing.

### V-41: "Game-changer / paradigm shift / disruptive"

- **Triggers:** `game-changer`, `game changer`, `paradigm shift`, `disruptive`, `revolutionary`, `groundbreaking`.
- **Why flagged:** LLMs learned these from business journalism. They rarely belong in academic writing.
- **Technical exceptions:** quoting someone who used the term; some business/strategy writing.
- **Replacement candidates:** describe the specific change (`reduces training time by 40%`); `significant`; `important`.
- **Density threshold:** any single instance in academic prose.

### V-42: "Unlock / unleash / harness"

- **Triggers:** `unlock`, `unleash`, `harness the power of`.
- **Why flagged:** Marketing copy register.
- **Technical exceptions:** literal unlocking (cryptographic, physical locks).
- **Replacement candidates:** `use`, `apply`, `enable`, `exploit`.
- **Density threshold:** any single instance in academic prose.

### V-43: "Cutting-edge / state-of-the-art"

- **Triggers:** `cutting-edge`, `cutting edge`, `state-of-the-art`, `state of the art`, `bleeding-edge`.
- **Why flagged:** In ML/AI papers, "state-of-the-art" (SOTA) is a technical term. Everywhere else it's marketing.
- **Technical exceptions:** ML/CV/NLP papers comparing to SOTA benchmarks — **this is a real technical term in those fields, don't flag it.**
- **Replacement candidates (outside ML contexts):** `current`, `recent`, `modern`, `best available`, or give the specific benchmark.
- **Density threshold:** any instance outside ML-benchmark contexts.

---

## 8. Sentence transitions (single-word)

### V-44: "Moreover / Furthermore / Additionally"

See P-01 in `sentence_patterns.md` — syntactic pattern already covers this. Listed here for cross-reference only; do not double-count hits.

### V-45: "Thus / Hence / Therefore"

- **Triggers:** `thus`, `hence`, `therefore`.
- **Why flagged:** LLMs over-use logical connectors. `Thus` especially is over-indexed in AI output.
- **Technical exceptions:** formal mathematical proofs (`thus, we have shown`) — legitimate and common.
- **Replacement candidates:** `so`, `which means`, drop it entirely, or restructure.
- **Density threshold:** 3+ in any document outside proof contexts; 2+ consecutively.

---

## 9. How to combine with sentence_patterns.md in Layer 0

When Layer 0 scans:

1. Run all V-NN pattern searches (this file) as grep operations. Cheap, fast, high-recall.
2. Run all P-NN pattern searches (`sentence_patterns.md`) — some are grep-able, some require structural checks.
3. For each hit, look up the detector sensitivity in the relevant detector-profile file and in the V-NN entry above.
4. In `discovery.md` §3, group by pattern ID (V-NN or P-NN). If a passage triggers both V-NN and P-NN (common for P-16 ↔ V-01 through V-18), record it under P-NN (higher structural level) and note the V-NN cross-reference.
5. **Do not report V-NN entries with zero hits.** Absence is information for internal round-count estimation only.

## Detector cross-reference (summary)

| Cluster | GPTZero | Pangram | Originality | Turnitin AI | Copyleaks | ZeroGPT |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Elevated academic (V-01–V-18) | ●●● | ●●● | ●●● | ●●○ | ●●● | ●●● |
| Latinate verbs (V-19–V-25) | ●●○ | ●●○ | ●●● | ●●● | ●●○ | ●●○ |
| Hedges (V-26–V-30) | ●●● | ●○○ | ●●● | ●●○ | ●●○ | ●●○ |
| Openers (V-31–V-33) | ●●● | ●●○ | ●●○ | ○○○ | ●●○ | ●●● |
| Closers (V-34–V-36) | ●●● | ●●○ | ●○○ | ●○○ | ●●● | ●●○ |
| Padding (V-37–V-40) | ●●○ | ●●● | ●●● | ●●● | ●●○ | ●●○ |
| Thought-leader (V-41–V-43) | ●●● | ●●● | ●●○ | ●●○ | ●●● | ●●● |
| Connectives (V-44–V-45) | ●●● | ●●● | ●●○ | ●○○ | ●●○ | ●●○ |

Legend: ●●● strongly weighted / ●●○ moderate / ●○○ mild.

## Novel-word slot

If Layer 0 finds an AI-sounding word or short phrase not in V-01 through V-45, record it under "Novel patterns" in `discovery.md` with a verbatim quote. LLM vocabulary preferences shift with each model generation; this file must evolve. Candidate additions from Claude 3.5+ era outputs include: `testament to`, `the intersection of`, `serves as a reminder`, `at the heart of`, `cornerstone`, `hallmark`, `inflection point`, `mosaic`, `orchestrate` (as a verb). Evaluate each for density and detector weight before adding as a canonical V-NN entry.
