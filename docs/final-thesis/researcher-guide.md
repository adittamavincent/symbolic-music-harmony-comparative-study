# Getting final thesis v3 ready

This guide is for the researcher writing their first thesis. It applies to this repository's Indonesian undergraduate manuscript. The sequence below is my recommendation after inspecting the draft and code; it is not a department regulation.

v1 and v2 were proposals. v3 continues the same project as the final thesis. A final-thesis phase can contain unfinished drafts. Calling it v3 does not imply that the experiments, conclusions, or approval are complete.

Read [PROGRESS.md](PROGRESS.md) for current evidence and [feedback.md](feedback.md) for the lecturer-review record.

## What you are trying to produce

Your thesis should let another reader follow a research question through a justified method, inspect the evidence, and judge your answer. You need to explain why you chose the method and what the evidence cannot establish.

For this project, the chain is:

```text
Research question
  → published musical rule and stated exceptions
  → operational definition and validated detector
  → supported model task and recorded generation settings
  → preserved raw samples, failures, and exclusions
  → reproducible measurements and analysis
  → musical interpretation and bounded conclusion
```

Writing code supplies part of that chain. You also need to justify the choices that the code makes.

Suppose you want to measure parallel fifths. You must first decide which two voices and which sounding events are compared, what counts as a fifth, and which musical situations are eligible. Then you can compare the detector with labeled examples. Until then, a number called `parallel_fifths` is a software output whose musical meaning still needs checking.

## The terms you need first

| Term | Meaning in this project |
| --- | --- |
| Research problem | A specific unanswered question about assessing generated symbolic music |
| Literature gap | What your documented search did not find, within its stated scope |
| Research question | A question your available outputs and instrument can answer |
| Theory | The musical account you use to define rules and their contexts |
| Operational definition | The exact musical event, condition, and counting procedure used to measure a rule |
| Instrument | The parser, voice/key assignment, rule detector, and scoring procedure together |
| Software test | A known input and expected output used to check code behavior |
| Instrument validation | Evidence that those outputs measure the intended musical property |
| Pilot | A small trial used to find problems before freezing the main procedure |
| Main data | Samples collected under the agreed procedure used for the thesis answers |
| Unit of analysis | What counts as one observation, including dependence on a shared seed/input |
| Result | What was measured, with its source, counts, and uncertainty |
| Discussion | Your supported interpretation, competing explanations, and musical examples |
| Limitation | A boundary that restricts the answer or its generalization |

## What each chapter must do

| Chapter | Reader's question | What you need to supply |
| --- | --- | --- |
| I. Pendahuluan | What is the question and why study it? | Specific problem, supported gap, bounded questions, objectives, scope |
| II. Tinjauan Pustaka | What prior work and musical theory justify the choices? | Accurate summaries, source pages, model/task differences, Strube rules and exceptions |
| III. Metodologi | How could someone repeat and check this work? | Executed protocol, instrument definitions, validation, model identities, samples, exclusions, analysis |
| IV. Hasil dan Pembahasan | What happened and how do you interpret it? | Actual counts, quality failures, rule-level results, analysis, score excerpts, competing explanations |
| V. Kesimpulan dan Saran | What answers can the evidence support? | Answer each question using chapter IV; state limits and specific next work |

The abstract comes after the results and conclusions are settled. It should state the actual method and findings. Department rules determine its language, length, and required front matter.

Write the parts you can substantiate now. For this project, it is practical to settle chapter III first, then write IV and V from the data, reconcile I and II with the final scope, and finish the abstracts. This is a workflow suggestion, not a required chapter-writing order.

## The missing research work

The proposal's 120-file plan has not been demonstrated by local main data. The inspected output folder contained dry-run metadata only. Existing tests check four cases, and the manuscript's earlier validation table contradicted those outputs.

Resolve these issues before the main run:

1. **Scope.** Compare the selected model/checkpoint pipelines. The present setup cannot separate architecture from training data, task, sampling, checkpoint, or parser differences.
2. **Controls.** NotaGen C and D currently use identical metadata. Its B metadata does not specify C major. A choir style tag does not demonstrate preservation of a particular soprano or bass.
3. **Musical measurement.** The evaluator's quantization collapses timing in a small probe. It also treats fourths as fifth candidates, checks shared onsets rather than complete sounding sonorities, and assumes parsed-part order identifies SATB.
4. **Scoring.** The current clipped count-per-soprano-event index is described as a proportion of clean moments. Those are different quantities. Choose a definition and denominator before comparing scores.
5. **Validation.** Read the actual rule passages and annotate examples. A positive Bach score does not identify the detector's false positives or missed violations. The test also forces tonic C, so its leading-tone output needs contextual checking.
6. **Data integrity.** Batch evaluation currently drops parse-quality flags/errors from summaries. Shared output folders can include stale files. MIDI conversion can change Coconet timing. Fix these paths and record attempts and actual usable counts.
7. **Analysis.** Choose comparisons and independent units before main collection. Repeating generation from one seed gives multiple files, but does not give multiple independent source chorales.

Detailed repairs remain in [maintenance.md](../maintenance.md). Musical and design choices belong in [research/protocol.md](../../research/protocol.md), not hidden in scripts.

## Your next seven work sessions

Work through these in order. Their duration depends on your deadline, access to books, and tutor availability.

| Session | Your task | Concrete deliverable |
| --- | --- | --- |
| 1 | Paste the lecturer's v2 notes; get the current department guide; write the question in your own words | Feedback record, requirements list, one paragraph explaining the study |
| 2 | Read the two thesis-writing selections below; identify problem, question, evidence, and contribution | A one-page research outline and a list of what remains undecided |
| 3 | Read Strube's relevant passages; work through examples at a keyboard/score; discuss exceptions with a tutor | Three rule-definition sheets with edition/pages, examples, exceptions, and expected labels |
| 4 | Read the original model and evaluation papers; compare their actual tasks and controls | Completed core-source notes and a supported comparison matrix |
| 5 | Agree the protocol, annotation procedure, score denominator, sample rationale, and analysis plan | Dated protocol decision record; method revisions with reasons |
| 6 | Run and inspect a small pilot after the measurement/pipeline fixes | Raw pilot artifacts, all attempts, labeled checks, and a decision to revise or freeze the protocol |
| 7 | Freeze the procedure, collect main data, analyze it, and draft IV/V | Evidence bundle and conclusions that answer the agreed questions |

Submission layout, front matter, bibliography checks, supervisor review, and defense preparation follow once the evidence is available. Use the gates in PROGRESS.md to identify what is ready, rather than counting completed pages.

After each work session, write four short lines: what I did, what I found, what I changed and why, and what I must resolve next. Link source pages or artifact paths. Use dated entries in [the research log](research-log.md); do not edit old findings to match a later explanation.

## Read in this order

Borrow through your library or use institutional access where possible. Start with the named sections and a written task; you do not need to read every book cover to cover before making progress.

| Priority | Reading | What to do with it |
| --- | --- | --- |
| 1 | Booth et al., [The Craft of Research, 5th edition](https://press.uchicago.edu/ucp/books/book/chicago/C/bo215874008) | Read the parts on research questions/problems, sources, claims, and evidence. Write your own question, claim boundary, and the evidence required to answer it. |
| 2 | Evans, Gruba, and Zobel, [How to Write a Better Thesis, 3rd edition](https://link.springer.com/book/10.1007/978-3-319-04286-2) | Start with “What Is a Thesis?”, “Thesis Structure”, and “Establishing Your Contribution”; use “Outcomes and Results”, “The Discussion or Interpretation”, and “Before You Submit” during drafting. |
| 3 | Strube, the edition of *The Theory and Use of Chords* you actually consult | Find the relevant voice-leading passages and exercises. Record their pages. The [ISI library catalog](https://opac.isi.ac.id/index.php?id=29353&p=show_detail) lists an Indonesian translation, *Teori dan Penggunaan Akor (I)*, translated by A. Gathut Bintarto T., published in 2015. Confirm whether that volume covers all your rules. A catalog listing does not verify the manuscript's 1928 edition or the rule wording. |
| 4 | Hadjeres et al., [DeepBach](https://proceedings.mlr.press/v70/hadjeres17a.html), and Huang et al., [Counterpoint by Convolution](https://archives.ismir.net/ismir2017/paper/000187.pdf) | Write down representation, training data, supported controls, and sampling. DeepBach uses pseudo-Gibbs sampling; describing its generation as ordinary left-to-right LSTM generation is inaccurate. |
| 5 | Wang et al., [NotaGen](https://arxiv.org/html/2502.18008v5), and Fang et al., [Bach or Mock?](https://arxiv.org/html/2006.13329v3) | Separate paper claims from your interpretations. NotaGen includes pretraining, fine-tuning, and CLaMP-DPO. Fang's score uses weighted Wasserstein distances between feature distributions; it is not this repo's clipped violation ratio. |
| 6 | [NeurIPS reproducibility checklist](https://neurips.cc/public/guides/PaperChecklist) and Pineau et al.'s [reproducibility report](https://www.jmlr.org/papers/v22/20-303.html) | Use the reporting questions to check your evidence bundle: exact methods, environment, data, uncertainty, and reproducible commands. They are research guidance, not your university's submission rules. |

For code work, consult the official [music21 voice-leading documentation](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html), [stream/quantization documentation](https://music21.org/music21docs/moduleReference/moduleStreamBase.html), and [SciPy Kruskal–Wallis documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html). Software APIs can implement your decisions; they do not determine which musical interpretation you should adopt.

## Forums and community reading

I searched for concrete discussions rather than treating forum advice as a university rule.

- [Academia Stack Exchange: how much implementation detail belongs in a thesis?](https://academia.stackexchange.com/questions/40820/how-detailed-should-i-be-about-my-implemented-system-while-writing-a-ph-d-thesi) Compare the answers with your chapter III: can another reader reconstruct the measurements? Use the discussion to identify missing explanation, not to set an arbitrary page count.
- [Academia Stack Exchange: keeping information gathered during research](https://academia.stackexchange.com/questions/108625/how-to-store-incidental-information-gleaned-in-the-course-of-conducting-research) Consider which note-taking habits help you recover source context and decisions. For this repo, use the reading ledger and dated research log.
- [University of Victoria Graduate Writers Community: review of How to Write a Better Thesis](https://onlineacademiccommunity.uvic.ca/gradwriters/2019/03/01/seeing-the-big-picture-a-review-of-how-to-write-a-better-thesis/) Read alongside the book if you need orientation before choosing chapters.

These discussions concern broader graduate research. Adapt their practical advice to your undergraduate scope and supervisor's requirements. Musical definitions should be grounded in the chosen theory source and expert review; empirical claims need the actual papers or your data.

## Read and record, then write

The [reading ledger](reading-notes.csv) distinguishes assistant source verification from your own reading. For each core source, record the relevant page/section, the claim it supports, what it does not establish, and how it affects your design.

For a literature search, record the date, index/site, exact query, results screened, and reasons for keeping sources. Start with phrases such as `symbolic music generation voice leading evaluation`, `parallel fifths chorale generation`, and `NotaGen harmony evaluation`; follow references and papers citing the core work. Search Scholar and the ISMIR archive as discovery tools, then read the original publications. Ask a librarian for help retrieving inaccessible material. State what your search covered before claiming novelty.

A safe gap statement can describe the comparison your reviewed sources did not address. “No one has ever tested this” requires much broader evidence. Do not cite a source merely because it mentions music generation; find the passage supporting the specific sentence.

## Your responsibility and the help available

You need to understand and defend the research question, musical rules, annotations, selection/exclusion decisions, and interpretation. Read the sources you cite and review the scores behind important results. Agree any required human-participant or AI-assistance procedure with the supervisor if it applies to the final design.

I can help repair the pipeline, translate agreed definitions into tests/code, build reproducible tables and figures, audit citations, edit the Indonesian manuscript, and prepare defense questions. Your observations, tutor judgments, and supervisor decisions supply information that code and prose generation cannot infer.

Start with session 1: put the v2 review notes into `feedback.md` and write one paragraph explaining what you want the research to find out.
