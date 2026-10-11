# StoryScope: evidence and transfer map

## Source identity

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John Wieting, *StoryScope: Investigating idiosyncrasies in AI fiction*.
- Supplied source: `/Users/vincent/Downloads/2604.03136v6.pdf`, 30 PDF pages; arXiv identifier printed in it: `2604.03136v6`, 10 August 2026. The PDF identifies itself as a COLM 2026 conference paper.
- SHA-256 of the supplied file: `929fd1add912dc030ed280451ab4f9a70378e2ded5d255aadad8012521c0643a`.
- [Versioned arXiv record](https://arxiv.org/abs/2604.03136v6), [authors' code](https://github.com/jenna-russell/storyscope).
- Read on 11 October 2026: complete local PDF text; Tables 14–16 also checked visually. Page numbers below are printed PDF pages, which match the file's page sequence.

The local PDF is the source for the findings recorded here. Web metadata and repository contents can change. Do not assume the web abstract, repository `main`, and this file are byte-identical or infer an experiment revision from the filename alone.

## What the experiment establishes

The authors compare published short stories from Books3 with stories generated from reverse-engineered prompts by five specified model versions: Claude Sonnet 4.6, DeepSeek V3.2, Gemini 3 Flash, GPT-5.4, and Kimi K2.5. The paper describes 10,272 prompt groups and a nominal 61,608 stories, averaging 4,753 words (§2, pp. 3–5). Missing generations and differing final artifact counts need to be reconciled for replication; see the reproduction reference.

StoryScope extracts structured representations, compares anonymized sources sharing prompts, discovers a feature taxonomy, and assigns features to full stories (§2; Appendix B, pp. 17–18; Appendix J, pp. 28–30). Its 304 semantic features span ten dimensions. The narrative-only classifier excludes 47 features judged dependent on surface style, leaving 257 (§3, p. 6). Style is therefore audited, not perfectly separated by an independently proved boundary.

Reported binary macro-F1 is 93.2% for narrative features and 96.0% for narrative plus style. Core-only performance is 84.8%. Six-way attribution is 68.4% using narrative features and 77.3% including style (Tables 2–3, pp. 6, 8). These measure classification on this benchmark, not grammatical correctness, literary quality, human authorship probability for one passage, or the benefit of a writing intervention.

The span-editing experiment uses 278 Gemini stories. Narrative classification changes from 95.5% on the original subset to 93.9% on edited stories (§4.2, p. 8). That supports a narrow finding: this surface-editing intervention did little to erase the classifier's narrative signal. It does not show that editing failed to improve prose, or that a particular prompt can make academic writing human.

Extractor reliability is reported as nominal Krippendorff's alpha 0.90 across repeated runs. A small validation uses 12 stories and 240 story-feature items per annotator, with mean human-model Cohen's kappa 0.84 (Appendix C, p. 19). This checks feature assignment within the fiction task; it does not validate the adapted academic checks in this skill.

## Findings to editorial adaptations

The source column describes fiction. The next column is our editorial adaptation for this project. Every adaptation requires the academic justification in the last column; none inherits the paper's classifier performance.

| Source observation and locator | Adaptation for academic prose | Boundary or counterargument |
| --- | --- | --- |
| Explicit narrator commentary on themes: AI 77%, human 52%; thematic explicitness means 3.94 vs. 3.28 on a 1–5 scale (§4.1, p. 7; Table 16, p. 26). | Remove sentences that only announce importance or repeat an already explained conclusion. Replace an unclear inference with its actual reasoning. | A thesis must explain definitions and inferential steps. Explanation becomes excess when it adds no information, not merely because it is explicit. |
| Explicit named references: human 47%, AI 24%; diffuse references more common in AI (§4.1; Table 16). | Name the actual study, author, model, musical rule, page, or data artifact that supports a claim. | Specificity is useful only if verified. Do not add names, citations, brands, or page numbers to imitate the fiction distribution. |
| AI favors a continuous causal chain, no subplots, and internal resolution; humans have more mixed structures (§4.1, pp. 7–8; Tables 14–16). | Check for a conclusion that makes mixed evidence look settled. Retain exceptions, incompatible measurements, and alternative explanations where supported. | Logical order, thematic unity, and a decisive conclusion can be correct academic choices. Do not create digressions or weaken a supported result to seem human. |
| Human stories are more dispersed and rarer in narrative feature space (§5, p. 9; Appendix H, pp. 22–23). | Avoid giving every paragraph the same rhetorical job or every section the same stock ending. Preserve useful variation already serving the argument. | Statistical rarity is not quality or authenticity. Do not randomize grammar, sentence lengths, or paragraph order, and do not optimize a rarity score. |
| AI uses bodily metaphors for emotion more often: 81% vs. 38%; humans use explicit emotion labels more often: 29% vs. 8% (§4.1; Table 16). | Prefer an accurate direct statement over ornament when describing the method or a limitation. | “Show, don't tell” is not an absolute instruction to add physical or sensory descriptions. Musical listening observations require actual observation. |
| Surface rewriting largely preserves narrative classification (§4.2, p. 8). | Inspect claims, relationships, and closure before fixing diction and punctuation. | This justifies examining two levels; it does not prove that this skill reproduces the authors' intervention or improves academic writing. |
| Structured templates discover more structure-oriented features than direct raw-text comparison (Appendix B, p. 17). | Make a brief internal map of paragraph purpose, evidence, boundaries, and connection when the argument is unclear. | The academic paragraph map is ours. It is not a StoryScope feature extractor or validated narrative representation. Do not expose a rigid template in the manuscript. |

## Findings that stay in fiction

Do not prescribe these as academic virtues merely because they lean human in Tables 15–16:

- Flashbacks, time jumps, delayed revelations, and nonlinear framing. Thesis methods should remain easy to reconstruct.
- Fourth-wall breaking and direct reader address. Explain terms for the intended reader without changing the department's academic register.
- More dialogue, locations, subplots, or morally ambivalent protagonists. These describe stories, not a thesis's argument.
- Ambiguous endings as a stylistic goal. State the supported answer clearly and preserve only genuine uncertainty.
- Model fingerprints such as gossip, epilogues, or restrained escalation (§5; Table 17). They describe the tested generations and do not diagnose the agent writing this paragraph.

Tables 14 and 15 contain 20 AI-leaning and 13 human-leaning directional entries. Some entries are different options of the same base feature, such as emotional expression and subplot integration. Do not treat 33 directional rows as 33 independent base features or recreate a universal human-writing checklist from their frequencies.

## Limits of the claim

This is an observational comparison of fiction produced under particular prompts and model settings, with LLM-derived annotations. The prompt examples are in English. The experiment does not test Indonesian thesis paragraphs, grammatical acceptability, retention of academic meaning, or readers' preference for edits made with this skill. Reverse-engineered prompts, corpus selection, model versions, annotation choices, and correlated features limit transfer.

We adopt evidence-conscious editorial practices and test them separately. We have not established “what makes all human writing human,” reproduced the authors' reported metrics, validated a new instrument, or shown improved writing quality. The actual researcher still supplies decisions, observations, and judgments; an agent cannot synthesize those from stylistic markers.
