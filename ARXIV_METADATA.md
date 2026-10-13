# arXiv submission metadata

Title: Five-Dimensional Reliability Evaluation for AI Agents: A Reproducible Framework, Synthetic Demonstrations, and a Local Model Case Study

Author: Goutham Siripuram

Affiliation: Independent Researcher (author to confirm at submission).

Suggested primary category: cs.AI (Artificial Intelligence).

Suggested secondary category: none. This manuscript presents agent evaluation/decision methodology, not a trained learning algorithm; cs.LG is not necessary for the current scope.

## Abstract

This paper proposes a five-dimensional reliability scoring specification for AI agents, covering task fidelity, recovery, action safety, resource efficiency, and evidence-observability. The reference implementation has explicit finite-input and missing-recovery handling. We retain 48 synthetic task specifications and 720 supplied synthetic demonstration records, and separately report 720 actual local model episodes using two small Hugging Face checkpoints, four concrete agent configurations, and 12 GSM8K test questions with three seeds and controlled tool faults. Across the eight clean model–configuration cells, exact-answer success ranges from 0/36 to 13/36 attempts. Fault exposure is recorded rather than treating untested recovery as success. The empirical case study supplies partial operational measurements; it neither validates every dimension nor calibrates the proposed aggregate. We release the frozen protocol, traces, analysis, uncertainty estimates, and limitations. The contribution is an inspectable methodology with synthetic illustrations and a bounded empirical case study, without deployment guarantees or a general model-superiority claim.

## Comments

Methodology preprint with synthetic demonstrations and a local model case study; software v0.4.0. 9 pages including references. Shared empirical data and source code are available in the repository.

## License recommendation

Recommend arXiv's non-exclusive distribution license for this submission, subject to the author's choice and any future venue requirements. The repository retains its existing license. No license selection has been submitted on the author's behalf. Review https://info.arxiv.org/help/license/index.html before choosing.

Keywords: LLM agents; reliability evaluation; recovery; safety; observability; synthetic stress tests.

GitHub repository: https://github.com/GouthamSiripuram/agent-reliability-evaluation

## AI-assistance disclosure recommendation

Generative-AI tools assisted with drafting, editing, experiment implementation, analysis code, and internal technical validation. Goutham Siripuram is the sole human author and is responsible for the manuscript, software, references, and scientific claims. AI assistance and the internal review do not constitute independent peer review.

Status: prepared for author review and manual submission. Not submitted to arXiv; no arXiv identifier or project DOI exists in this release metadata. Moderation and endorsement, if requested, remain arXiv decisions.
