# Evaluate edits without an authorship score

## Delivery checks

Apply `docs/final-thesis/eval.md` first. Then inspect original and revised text with its source context:

| Check | Observable acceptance condition |
| --- | --- |
| Meaning and evidence | Every revised claim remains supported at the same strength; any authorized substantive correction is explained with evidence. |
| Research status | Plans, implementation checks, validation, pilot, main data, and listening remain distinguishable. |
| Argument | Each paragraph contributes to the section; connections are justified; genuine exceptions remain visible. |
| Explanation | Necessary definitions, inferential steps, and measurement details survive; repetitive importance labels do not. |
| Specificity | Names and numbers come from evidence; no experiences, pages, or observations were invented. |
| Grammar | Subjects, predicates, referents, punctuation, and conjunctions make the intended relation clear. |
| Voice | Useful vocabulary and cadence survive; no forced informality, random variation, or systematic new template appears. |
| Continuity | Terms, scope, units, tense, and references fit adjacent paragraphs and the applicable protocol. |
| Markup | Citation keys and pages, formulas, labels, references, and unaffected LaTeX remain intact. |
| Task boundary | Audit mode does not rewrite; a local edit does not rewrite the chapter, front matter, or protocol. |

Fix a failed check within the authorized scope and reread. If a missing fact prevents a defensible claim, report the gap outside the manuscript. Do not invent the fact to pass the check.

## Reusable behavioral cases

When changing this skill, try the fixtures in [academic-editing.md](academic-editing.md), without treating the given wording as the only acceptable answer:

1. Edit a redundant significance sentence. The output removes empty emphasis without inventing a replacement claim.
2. Edit the denominator definition. The output preserves what is counted and the difference from the bar denominator.
3. Supply the attribution fixture with and without its evidence. The agent names the source only when supplied or verified; otherwise it flags the missing evidence.
4. Edit the model-comparison limitation. The agent retains the causal boundary and specific differences.
5. Edit the planned-generation fixture. The agent does not claim that the planned outputs exist.
6. Repair the dangling fragment. The agent fixes syntax without claiming identical controls.
7. Edit the clear Bach-reference sentence. No edit is acceptable and often preferable.
8. Request detection only. The agent reports an observed pattern without rewriting or labeling authorship.
9. Supply a paragraph plus neighbors using `pelanggaran per birama` and `pelanggaran per kesempatan`. The edit preserves the applicable denominator and does not rotate the terms as synonyms.
10. Supply a cited LaTeX passage. Check preserved tokens and the source support of the surrounding claim, not just whether the passage compiles.

Record actual outcomes, model/settings, skill revision, input, output, and failures when running a behavioral comparison. A self-check can catch mistakes; it is weaker evidence than an independent reader or a blinded comparison. File/frontmatter validators verify packaging, not writing behavior.

## Test whether the adaptation helps this researcher

This is a proposed local evaluation, not a study already run and not a reproduction of StoryScope's authorship experiments.

Use the same source packet and task for two editing conditions: the existing no-AI-slop instructions alone, and those instructions plus this skill. Choose a small set of real passages representing the researcher's common tasks: background, literature comparison, definitions, methods, limitations, and transitions. Use authentic researcher-written samples for voice comparison only if available and identified by the researcher; agent-written passages cannot establish the researcher's personal voice.

Record model version, settings, prompts, source packet, skill commit or file hash, and raw outputs. Keep claim requirements and allowed edits equal. If possible, repeat across passages or outputs; one favorable example cannot establish a general effect.

Present alternatives with randomized anonymous labels, counterbalancing order across passages. Have the researcher and, if available, another reader compare clarity, accuracy, voice, continuity, necessary explanation, and concision. Verify scientific fidelity against source material separately. Readers must be able to choose a tie or reject both.

Retain original wording when it is better. Report preferences and failures with their actual passage counts and reasons. State who reviewed and what was blinded. Do not call ordinal reader ratings validated scales or infer significance from a small convenience set.

Do not use detector scores, perplexity, sentence-length variance, or “burstiness” as the objective. Do not ask the rewriter to certify its own prose as human. The practical outcome is a passage the researcher prefers and can defend, with no unsupported changes in meaning.

## Current verification boundary

Reading the source, checking the adaptation map, validating skill packaging, and examining example edits do not establish that this skill improves real thesis prose. The paired reader evaluation above remains unrun until actual outputs and judgments are recorded. The main music research protocol is unaffected by this proposed editorial comparison.
