# v0.4.0 publication validation

Audit date: 2026-10-13. The v0.3.0 methodology sources and validation records are preserved under validation/v0.3.0/; earlier v0.2.0 material and the original internal review remain unchanged.

## Scope and implementation

Inspected the original research source, tests, data, notebooks, figures, manuscript and metadata in the preceding publication audit. The NaN, untested-recovery, finite/range, input-validation and independent-scenario-generation fixes remain present. The 26 existing framework tests passed again in the empirical environment (16 reliability and 10 architecture tests).

The new work adds actual local Hugging Face model execution, a bounded calculator, four concrete configurations, controlled faults, deterministic scoring, and a frozen analysis. Development used only two training examples. It corrected message formatting, explicit final-answer parsing, conflicting final-answer instructions, and the framework's blanket prohibition on repeating tool calls. These fixes preceded held-out execution. Thirteen study tests passed, including arithmetic bounds, parsing, zero-exposure handling, bootstrap denominators, and scripted timeout/retry/tool-call integration.

## Empirical evidence

- Exactly 720 unique planned test episodes: 360 per checkpoint; 288 clean, 216 timeout-assigned and 216 injection-assigned.
- Two checkpoints, 12 GSM8K test questions, three seeds, and four concrete configurations. All inference was local; no paid compute.
- 2837 actual completed model-generation calls and 538 calls reaching the calculator implementation.
- 178 episode-level agent exceptions remain in the outcome denominator; no infrastructure errors occurred.
- Exact task/model/configuration/condition/seed set verified, frozen files unchanged, timestamps after local freeze, token totals/bounds checked, and recorded calculator outputs recomputed.
- No complete reference solution appeared in the first model prompt. Public-benchmark training contamination remains possible and is disclosed.
- Primary answers were rescored against dataset labels. One marked arithmetic expression exposed a numeric-prefix parser limitation; adjudication confirmed it was already incorrect against the gold answer and all reported outcomes remain unchanged. The flag and adjudication are retained; see empirical/SCORING_AUDIT.md. No run was discarded or rerun.
- Task-cluster intervals and frozen proxy-policy comparisons were computed without fitting to test outcomes. Zero exposure remains unobserved. No full FDAR aggregate or broad enterprise-validation claim is made.
- The two companion papers use the same shared observations, not independent replications.

Exact raw traces, episode CSV, summary tables, provenance, licenses and checksums are in empirical/. The post-run integrity audit is recorded separately from the frozen primary analysis. The original synthetic records remain synthetic and unchanged.

## Publication checks

- Original synthetic notebooks and generators passed in v0.3.0; their scope is recorded in the preserved validation history. The new empirical notebook executed all 4 code cells in-process with IPython, with its plot embedded. No separate Jupyter kernel was launched.
- CITATION.cff passed the CFF 1.2.0 schema check.
- 11 used bibliography items have matching rendered entries. The GSM8K reference and official model/framework footnotes were verified against primary sources; prior unchanged references retain their documented audit.
- Independent ZIP extraction and compilation with Tectonic 0.17.0 passed, using only packaged manuscript inputs and standard cached TeX resources.
- No unresolved citations/references, missing bibliography/images, fatal errors, LaTeX warnings, missing characters, or overfull boxes in the final build. PDF text has no unresolved `??` or `[?]` markers.
- All 9 pages were visually inspected. The author, tables, figures, references and links render correctly.
- Source ZIP contains only: `main.tex`, `references.bib`, `main.bbl`, `tables/summary.tex`, `figures/sensitivity.pdf`, `tables/empirical_clean.tex`, `tables/empirical_faults.tex`. It excludes datasets, traces, model weights, notebooks, code, internal reviews, credentials, strategy material and Git history.

## Final gate

- [x] Cited works and bibliography resolve; figures and references render.
- [x] Goutham Siripuram is the sole named author; no institutional affiliation invented.
- [x] Actual local observations are separated from preserved synthetic demonstrations.
- [x] No fabricated experiment, citation, DOI, arXiv identifier, or peer-review status.
- [x] Correct repository URL and explicit generative-AI assistance disclosure.
- [x] Independent source ZIP compilation and visual PDF inspection completed.
- [x] Exact source ZIP and corresponding PDF supplied.

ZIP SHA-256: `13260d94bccbb0c106b2b5691d1fd052461fe9fd5f2672ac372b2a4bc496dcd8`

PDF SHA-256: `0276bfb862d49a50ef9b7e529c313db7551e07ad51a166f492b90bb0dfc6bfca`

Status: technically ready for author review and manual arXiv submission. This is a bounded empirical case study, not validation of every methodological assumption or an acceptance claim. No arXiv submission was attempted. Goutham must inspect the final claims and choose the submission license/category; any endorsement or moderation remains with arXiv. GitHub release notes are prepared; no tag, release or Zenodo DOI is claimed here.
