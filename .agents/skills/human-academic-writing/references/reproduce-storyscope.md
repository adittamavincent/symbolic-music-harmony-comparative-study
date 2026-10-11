# Separate the reproduction tasks

## Three different outcomes

| Task | Evidence needed | Scope of this skill |
| --- | --- | --- |
| Repeat the editing procedure | Same input/source packet, skill revision, model/settings, and recorded output | Supported by the paragraph workflow. Exact wording from a generative model is not guaranteed. |
| Show that the adapted skill helps this thesis | Actual paired outputs, source-fidelity review, and reader judgments | Proposed in [evaluation.md](evaluation.md); not yet measured. |
| Reproduce StoryScope's experimental results | Released artifacts, pinned code, feature encoding, splits, evaluation and bootstrap settings, plus the necessary data/models | A separate experiment. No classifier, dataset download, story generation, or paid API pipeline was run in creating this skill. |

## If the paper experiment is explicitly requested

Start with the [authors' repository](https://github.com/jenna-russell/storyscope) and its data documentation. Record an exact commit, license, artifact checksums, dependencies, and the paper revision. Inspect executable arguments at that commit before constructing commands; a mutable README is not proof that its commands reproduce the supplied PDF.

Prefer the released feature matrix for a classification-only reproduction. It can avoid rerunning story generation and feature extraction. Verify that labels, prompt IDs, feature types, splits, missing-value treatment, and style exclusions match the selected experimental revision. Keep outputs in a separate research run directory and preserve failed attempts.

The paper's stages are:

1. Construct prompts with Gemini 2.5 Flash and generate stories with the five specified source models (§2; Appendix J).
2. Extract ten-dimension structured templates using GPT-5.1 (§2.1; Figure 8).
3. Compare blinded templates in randomized order for 100 discovery prompts, with prompt-group batching (Appendix B).
4. Run feature discovery three times; deduplicate 408 candidates with F2LLM-4B and single-link clustering at cosine threshold 0.85 (§2.1; Appendix B).
5. Assign features from full stories using Gemini 3 Flash with minimal thinking, grouped by dimension; preserve missing assignments and exclusions (§2.2; Appendix C).
6. Encode feature types and train XGBoost with prompt-level grouping, validation selection, the applicable class weighting, and fixed settings (§3; Appendix D).
7. Reproduce the 47-feature style exclusion, reported variants, bootstrap SHAP analysis with 50 iterations, core/fingerprint definitions, and reported evaluation subsets (§3; Appendices D–H).

Keep discovery prompts apart from evaluation. Keep every source version of the same prompt in the same split. Report binary macro-F1 and AUPRC, and six-way macro-F1 and accuracy. Never equate the 5:1 class-imbalanced binary accuracy with the paper's macro-F1.

The human story texts are not released with the public dataset; the authors describe copyright constraints. A feature-only classifier reproduction and a new raw-text pipeline run are therefore different scopes. Do not promise a complete raw-text replication from the release alone or retrieve Books3 as a side effect of using this writing skill.

## Reconcile discrepancies before claiming replication

The supplied PDF contains differing count descriptions:

- Main §3, p. 5: 8,739 training prompts / 52,434 stories and 1,377 test prompts / 8,262 stories.
- Appendix D, p. 20: 7,383 train / 1,405 validation / 1,384 test prompts, refit on 8,788 prompts / 52,707 stories, test on 8,301 stories.
- Nominal corpus: 61,608 stories; footnote 8 mentions 24 generation refusals. Table 5, p. 17, shows generation coverage missing 11 Gemini and 13 Claude stories.
- The [repository README](https://github.com/jenna-russell/storyscope#data) inspected on 11 October 2026 lists a released feature matrix of 61,575 stories.

Do not silently choose one count or assume all artifacts have complete six-source groups. Trace the actual exclusions, prompt IDs, artifact revision, and evaluation script; report the selected configuration and unresolved differences. A differing count is not by itself proof of an invalid result.

Fresh generation can incur costs and depend on model availability or changed provider behavior. Check the requested experimental scope before launching it. A successful run proves only the stages actually executed; compare reproduced numbers with the paper and retain discrepancies rather than describing approximate agreement as exact reproduction.
