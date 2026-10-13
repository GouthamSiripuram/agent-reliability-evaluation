# Five-Dimensional Reliability Evaluation for AI Agents: A Reproducible Framework, Synthetic Demonstrations, and a Local Model Case Study

**Author: Goutham Siripuram | Version: 0.4.0**

**Scientific status: proposed methodology, preserved synthetic demonstrations, and a separate local empirical case study.** The original data remain synthetic. `empirical/results/` contains measurements from 720 actual local model episodes on 12 GSM8K tasks, with two small checkpoints, three seeds, four configurations, and controlled tool faults. This is limited empirical evidence, not enterprise validation or calibrated methodology. The current preprint is prepared for author review and manual arXiv submission; it has not been submitted to arXiv, and no arXiv ID or DOI is claimed.

The five dimensions are task fidelity, recovery, action safety, cost-latency efficiency, and evidence-observability. Aggregation and weights are proposed conventions, not empirically validated measures. Always report dimension coverage; a four-dimension score is not directly comparable to a five-dimension score.

## Paper and submission files

- [Compiled preprint](paper/main.pdf)
- [Self-contained arXiv source ZIP](submission/agent_reliability_arxiv_submission.zip)
- [arXiv metadata](ARXIV_METADATA.md)
- [Bibliography verification](BIBLIOGRAPHY_AUDIT.md) and [claim audit](CLAIM_AUDIT.md)
- [Validation record](VALIDATION.md) and [release notes](RELEASE_NOTES.md)

Suggested category: **cs.AI**. The author must review the manuscript and arXiv-generated PDF before manually submitting. Technical readiness does not imply acceptance or validation of every methodological assumption.

## Reproduce the calculations

Use Python 3.12 for the recorded environment (the package supports Python >=3.10). From the repository root:

```bash
python -m venv .venv
# Activate .venv using your platform's activation command.
python -m pip install -r requirements-reproduction.txt
python -m pip install -e .
python -m pytest -q
python scripts/reproduce_paper.py
```

The last command regenerates the manuscript tables, sensitivity figure, and machine-readable summaries in `results/`. Direct reproduction dependencies are version-pinned; this is not a full transitive lockfile. Optional interactive notebook support is available with `python -m pip install -e ".[validation]"`, then `jupyter notebook notebooks/reproduce_results.ipynb`.

Run `python scripts/generate_synthetic_data.py` to regenerate the 48 task descriptions. It does not regenerate the 720 supplied synthetic observation records. Their original generation process is unavailable; scoring from the checked-in file is reproducible. The catalog is deterministic without a random seed.

## Real local-agent study

See [the empirical protocol and reproduction instructions](empirical/README.md). The study uses Qwen3-0.6B and SmolLM2-360M-Instruct through Hugging Face smolagents, running locally on a 4 GB GPU. No paid inference was used. Failed attempts remain in the results; unexposed tool faults do not count as successful recovery. The two companion repositories contain the **same shared study**, not independent replications.

- [Frozen protocol](empirical/PROTOCOL.md) and [hash manifest](empirical/FREEZE.json)
- [Episode measurements](empirical/results/episodes.csv) and [condition summaries](empirical/results/condition_summary.csv)
- [Fixed-selector comparison](empirical/results/selector_policy_evaluation.csv)
- Full compressed traces and checksums are in `empirical/results/`.

The study observes only part of the reliability framework, so no complete five-dimensional score is imputed. The architecture selector uses unvalidated question-only proxies and unchanged coefficients; it has not been calibrated. Exact-answer parsing, small models, limited role budgets, public-data contamination, and only 12 task clusters limit interpretation. Results do not establish a general advantage for additional agents.

Run `python scripts/reproduce_empirical_paper.py` to regenerate empirical tables/figures from released summaries. Run the frozen analysis and inference separately as documented in `empirical/README.md`. Core-package tests use `tests/`; empirical tests require the separate model environment and are invoked explicitly with `python -m pytest empirical -q`.

## Build the paper

From `paper/`, use a standard LaTeX installation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The release uses Tectonic 0.17.0 (automatic bibliography and LaTeX reruns): `tectonic --untrusted --keep-logs --keep-intermediates main.tex`. The source uses standard article/LaTeX packages and PDF figures. Submission ZIPs include `main.bbl` as well as `references.bib`.

## How to cite

Use [CITATION.cff](CITATION.cff) or cite: Goutham Siripuram (2026), *Five-Dimensional Reliability Evaluation for AI Agents: A Reproducible Framework, Synthetic Demonstrations, and a Local Model Case Study*, methodology preprint and software, version 0.4.0, https://github.com/GouthamSiripuram/agent-reliability-evaluation. Cite the exact commit used when no release tag is available. No DOI should be added until one is actually issued.

## Provenance and limitations

Generative-AI tools assisted with drafting, editing, code review, and internal technical validation. Goutham Siripuram is the sole human author and is responsible for the claims and artifacts. The seven-role AI-assisted internal review is **not independent human peer review**.

The original [internal review](SEVEN_ROLE_INTERNAL_REVIEW.md) remains unchanged. Earlier build warnings, draft sources/PDF, and validation records are preserved in `validation/v0.2.0/`; their historical status does not describe the current paper. The v0.3.0 manuscript and validation records are preserved in `validation/v0.3.0/`. Real local-agent runs are now included; full construct validation, coefficient calibration, and independent evaluation remain outstanding.
