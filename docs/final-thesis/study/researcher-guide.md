# Getting final thesis v3 ready

This guide is for the researcher writing their first thesis. It applies to this repository's Indonesian undergraduate manuscript. The sequence below is my recommendation after inspecting the draft and code; it is not a department regulation.

v1 and v2 were proposals. v3 continues the same project as the final thesis. A final-thesis phase can contain unfinished drafts. Calling it v3 does not imply that the experiments, conclusions, or approval are complete.

The current design is a machine-only continuation of Huang et al. (2019) with DeepBach and Coconet. Read [PROGRESS.md](../PROGRESS.md) for the current status, [research/protocol.md](../../../research/protocol.md) for the design, and [feedback.md](../supervision/feedback.md) for the lecturer-review record. Practise with [defense-qa.md](defense-qa.md).

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
| Instrument | The parser, voice mapping, rule detector, and rate calculation together |
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
| III. Metode Penelitian | How could someone repeat and check this work? | Executed protocol, instrument definitions, validation, model identities, samples, exclusions, analysis |
| IV. Hasil dan Pembahasan | What happened and how do you interpret it? | Actual counts, quality failures, rule-level results, analysis, score excerpts, competing explanations |
| V. Kesimpulan dan Saran | What answers can the evidence support? | Answer each question using chapter IV; state limits and specific next work |

The abstract comes after the results and conclusions are settled. It should state the actual method and findings. Department rules determine its language, length, and required front matter.

Write the parts you can substantiate now. For this project, it is practical to settle chapter III first, then write IV and V from the data, reconcile I and II with the final scope, and finish the abstracts. This is a workflow suggestion, not a required chapter-writing order.

## Where the work stands

Open work is tracked in one place: the completion gates and open items in [PROGRESS.md](../PROGRESS.md). Design decisions belong in [research/protocol.md](../../../research/protocol.md), and technical defects and repairs in [maintenance.md](../../maintenance.md). Before the next supervisor meeting, follow the study order in [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md).

After each work session, write four short lines: what I did, what I found, what I changed and why, and what I must resolve next. Link source pages or artifact paths. Use dated entries in [the research log](../records/research-log.md); do not edit old findings to match a later explanation.

## Read in this order

Borrow through your library or use institutional access where possible. Start with the named sections and a written task; you do not need to read every book cover to cover before making progress.

| Priority | Reading | What to do with it |
| --- | --- | --- |
| 1 | Booth et al., [The Craft of Research, 5th edition](https://press.uchicago.edu/ucp/books/book/chicago/C/bo215874008) | Read the parts on research questions/problems, sources, claims, and evidence. Write your own question, claim boundary, and the evidence required to answer it. |
| 2 | Evans, Gruba, and Zobel, [How to Write a Better Thesis, 3rd edition](https://link.springer.com/book/10.1007/978-3-319-04286-2) | Start with “What Is a Thesis?”, “Thesis Structure”, and “Establishing Your Contribution”; use “Outcomes and Results”, “The Discussion or Interpretation”, and “Before You Submit” during drafting. |
| 3 | Strube, *The Theory and Use of Chords* (1928), and its Indonesian translation *Teori dan Penggunaan Akor (I)* by A. Gathut Bintarto T. (2015), who is Pembimbing I ([ISI library catalog](https://opac.isi.ac.id/index.php?id=29353&p=show_detail)) | Read the rule passages, exceptions, and printed examples in both editions. The page map and three wording differences are in [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md), section 1. |
| 4 | Huang et al. (2019) §6.3 and Yan et al. (2018) §4 with its supplementary rubric | The study's design, measure, and rule categories come from these two papers. Sections to read and what to explain are listed in [persiapan-pembimbing-1.md](persiapan-pembimbing-1.md), section 5. |
| 5 | Hadjeres et al., [DeepBach](https://proceedings.mlr.press/v70/hadjeres17a.html), and Huang et al., [Counterpoint by Convolution](https://archives.ismir.net/ismir2017/paper/000187.pdf) | Write down representation, training data, supported controls, and sampling. DeepBach uses pseudo-Gibbs sampling; describing its generation as ordinary left-to-right LSTM generation is inaccurate. |
| 6 | Wang et al., [NotaGen](https://arxiv.org/html/2502.18008v5), and Fang et al., [Bach or Mock?](https://arxiv.org/html/2006.13329v3) | Explain why NotaGen was excluded (its official interface takes period, composer, and instrumentation prompts, not a melody to preserve) and why Fang's weighted Wasserstein score measures closeness to Bach's style rather than rule violations. |
| 7 | [NeurIPS reproducibility checklist](https://neurips.cc/public/guides/PaperChecklist) and Pineau et al.'s [reproducibility report](https://www.jmlr.org/papers/v22/20-303.html) | Use the reporting questions to check your evidence bundle: exact methods, environment, data, uncertainty, and reproducible commands. They are research guidance, not your university's submission rules. |

For code work, consult the official [music21 voice-leading documentation](https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html), [stream/quantization documentation](https://music21.org/music21docs/moduleReference/moduleStreamBase.html), and the SciPy documentation for the [Wilcoxon signed-rank test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html) and the [Mann–Whitney U test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html). Software APIs can implement your decisions; they do not determine which musical interpretation you should adopt.

## Forums and community reading

I searched for concrete discussions rather than treating forum advice as a university rule.

- [Academia Stack Exchange: how much implementation detail belongs in a thesis?](https://academia.stackexchange.com/questions/40820/how-detailed-should-i-be-about-my-implemented-system-while-writing-a-ph-d-thesi) Compare the answers with your chapter III: can another reader reconstruct the measurements? Use the discussion to identify missing explanation, not to set an arbitrary page count.
- [Academia Stack Exchange: keeping information gathered during research](https://academia.stackexchange.com/questions/108625/how-to-store-incidental-information-gleaned-in-the-course-of-conducting-research) Consider which note-taking habits help you recover source context and decisions. For this repo, use the reading ledger and dated research log.
- [University of Victoria Graduate Writers Community: review of How to Write a Better Thesis](https://onlineacademiccommunity.uvic.ca/gradwriters/2019/03/01/seeing-the-big-picture-a-review-of-how-to-write-a-better-thesis/) Read alongside the book if you need orientation before choosing chapters.

These discussions concern broader graduate research. Adapt their practical advice to your undergraduate scope and supervisor's requirements. Musical definitions should be grounded in the chosen theory source and expert review; empirical claims need the actual papers or your data.

## Read and record, then write

The [reading ledger](../records/reading-notes.csv) distinguishes assistant source verification from your own reading. For each core source, record the relevant page/section, the claim it supports, what it does not establish, and how it affects your design.

For a literature search, record the date, index/site, exact query, results screened, and reasons for keeping sources. Start with phrases such as `symbolic music generation voice leading evaluation`, `parallel fifths chorale generation`, and `automatic harmonization evaluation rubric`, and keep the tracked query plan in `research/literature/openalex_queries.json`; follow references and papers citing the core work. Search Scholar and the ISMIR archive as discovery tools, then read the original publications. Ask a librarian for help retrieving inaccessible material. State what your search covered before claiming novelty.

A safe gap statement can describe the comparison your reviewed sources did not address. “No one has ever tested this” requires much broader evidence. Do not cite a source merely because it mentions music generation; find the passage supporting the specific sentence.

## Your responsibility and the help available

You need to understand and defend the research question, musical rules, operational definitions, selection/exclusion decisions, and interpretation. Read the sources you cite and review the scores behind important results. Agree any required human-participant or AI-assistance procedure with the supervisor if it applies to the final design.

I can help repair the pipeline, translate agreed definitions into tests/code, build reproducible tables and figures, audit citations, edit the Indonesian manuscript, and prepare defense questions. Your observations, tutor judgments, and supervisor decisions supply information that code and prose generation cannot infer.
