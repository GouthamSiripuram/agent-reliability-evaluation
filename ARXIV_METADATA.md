# arXiv submission metadata

Title: Five-Dimensional Reliability Evaluation for Enterprise AI Agents: A Reproducible Framework and Synthetic Stress-Test Suite

Author: Goutham Siripuram

Affiliation: Independent Researcher (author to confirm at submission).

Suggested primary category: cs.AI (Artificial Intelligence).

Suggested secondary category: none. This manuscript presents agent evaluation/decision methodology, not a trained learning algorithm; cs.LG is not necessary for the current scope.

## Abstract

Evaluation of an AI agent requires explicit choices about task completion, recovery, safety, resource use, and the evidence retained for inspection. This paper proposes a five-dimensional scoring specification and a small executable reference implementation. It defines task fidelity, recovery robustness, action safety, cost-latency efficiency, and evidence-observability, with a weighted geometric summary and explicit handling of unobserved recovery. The release includes 48 synthetic task specifications and 720 supplied synthetic records; none are measurements of deployed agents or language models. We reproduce descriptive summaries and an analytical sensitivity example, document missing-data and aggregation limitations, and specify a protocol for future real-agent validation. The contribution is an auditable operationalization and software artifact, not a new general theory of reliability, an empirically calibrated metric, or evidence of model superiority.

## Comments

6 pages, including references; methodology preprint with reproducible synthetic demonstrations; software v0.3.0. No real-agent empirical validation. Source code and data available at the repository below.

## License recommendation

Recommend arXiv's non-exclusive distribution license for this submission, subject to the author's choice and any future venue requirements. The repository retains its existing license. No license selection has been submitted on the author's behalf. Review https://info.arxiv.org/help/license/index.html before choosing.

Keywords: LLM agents; reliability evaluation; recovery; safety; observability; synthetic stress tests.

GitHub repository: https://github.com/GouthamSiripuram/agent-reliability-evaluation

## AI-assistance disclosure recommendation

Generative-AI tools assisted with drafting, editing, code review, and internal technical validation. Goutham Siripuram is the sole human author and is responsible for the manuscript, software, references, and scientific claims. AI assistance and the internal review do not constitute independent peer review.

Status: prepared for author review and manual submission. Not submitted to arXiv; no arXiv identifier or project DOI exists in this release metadata. Moderation and endorsement, if requested, remain arXiv decisions.
