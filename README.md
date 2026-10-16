# Reporting Agent Reliability under Partial Observation: Exposure-Matched Fault Tests and Score Bounds

Authors: Goutham Siripuram and Akshitha Mulastam (equal contribution). Research revision **0.5.0**. Prepared preprint and submission materials; **not submitted to arXiv or TMLR**, and not peer reviewed.

Fault tests can produce misleading reliability summaries when task completion, actual exposure, and recovery are treated as interchangeable observations. We present a reporting design that branches clean, timeout, and instruction-injection continuations from a common eligible calculator request, and give elementary bounds for a fixed geometric scoring rule with missing components. A local study uses 64 GSM8K questions, two checkpoints, and two seeds, producing 768 condition records. Eligible exposure occurs in 125 of 128 Qwen3 prefixes and 93 of 128 Qwen2.5 prefixes. Injection reduces overall format-constrained success by 21.88 and 24.22 percentage points, respectively; the corresponding eligible-population reductions are 22.40 and 33.33 points. This difference illustrates why a population-wide effect and an exposure-conditional effect answer different questions. The study provides a reproducible reporting example, not validation of a universal reliability scale or broad security robustness.

## Evidence and limits

This revision uses actual local Qwen3-0.6B and Qwen2.5-1.5B-Instruct executions on public arithmetic benchmark questions. It is a bounded case study, not production or enterprise validation. Earlier synthetic demonstrations remain synthetic and are preserved in the original directories and Git history. The v0.4 pilot is historical and is not pooled into v0.5 primary results. The related paper shares research ancestry and software but has different primary tasks and interventions.

## Files and reproduction

- [Preprint PDF](submission/v0.5.0/agent_reliability_preprint.pdf)
- [Self-contained arXiv source](submission/v0.5.0/agent_reliability_arxiv_submission.zip)
- [Execution evidence and frozen code](submission/v0.5.0/agent_reliability_tmlr_supplement.zip)
- [Validation report](study_v05/FINAL_VALIDATION.md)
- [arXiv metadata](ARXIV_METADATA.md)

Extract the evidence ZIP into a separate directory. It contains completed records, unchanged source hashes, task data, dependency versions, provenance and notices. Install requirements-lock.txt in an isolated environment. Run `python -m pytest test_research.py test_analysis.py`, then `python analysis.py --study reliability`. This recomputes results without inference. Full local-inference instructions are in its README. Never overwrite supplied records or run duplicate GPU jobs.

The published source ZIP compiled independently. Identified and anonymous PDFs have been visually checked. An anonymous review PDF is supplied separately to the author; the public preprint is not the anonymous upload. Author review and submission declarations remain required. Technical checks do not guarantee acceptance.

## Citation and authorship

Cite Goutham Siripuram and Akshitha Mulastam, *Reporting Agent Reliability under Partial Observation: Exposure-Matched Fault Tests and Score Bounds*, research software/preprint revision 0.5.0, 2026, this repository. See CITATION.cff. No DOI or arXiv ID has been assigned.

Goutham Siripuram and Akshitha Mulastam contributed equally to this work. Generative AI assisted drafting, code development, editing and internal technical validation; the human authors are responsible for the manuscript and its scientific claims. The historical seven-role AI review was not independent human peer review. Original code remains under the repository MIT license; third-party material retains its notices. Manuscript licensing is an author submission decision; CC BY 4.0 is recommended for TMLR compatibility.
