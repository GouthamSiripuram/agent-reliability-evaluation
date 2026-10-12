# Five-Dimensional Reliability Evaluation for Enterprise AI Agents

**Author:** Goutham Siripuram  
**Version:** 0.2.0

This repository accompanies the methodology preprint **Five-Dimensional Reliability Evaluation for Enterprise AI Agents: A Reproducible Framework and Synthetic Stress-Test Suite**.

## Scope
The framework evaluates five dimensions: task fidelity, recovery robustness, action safety, cost-latency efficiency, and evidence-observability.

## Scientific status
The bundled demonstration data are **synthetic**. They are not measurements of commercial or open-source LLMs. Real-agent experiments are required before making empirical comparative claims.

## Contents
- `src/fdar/` â€” v0.2 reference implementation with finite/range validation and missing-recovery handling.
- `scripts/generate_synthetic_data.py` â€” deterministic task-catalog generator.
- `data/` â€” synthetic task catalog and demonstration runs.
- `notebooks/reproduce_results.ipynb` â€” reproducibility notebook.
- `paper/` â€” LaTeX preprint source, BibTeX, and compiled PDF.
- `tests/` â€” adversarial unit tests.
- `CITATION.cff`, `LICENSE`, and submission notes.

## Run
```bash
python -m pip install -e ".[validation]"
python -m pytest -q
jupyter notebook notebooks/reproduce_results.ipynb
```

## Integrity note
Do not represent synthetic data as real model measurements. An internal AI-assisted seven-role review identified and corrected edge cases in v0.2; it is not independent human peer review.

## Publication status and limitations

Repository: https://github.com/GouthamSiripuram/agent-reliability-evaluation

This is an AI-assisted methodology and synthetic demonstration release, not a peer-reviewed or empirically validated model benchmark. See `SEVEN_ROLE_INTERNAL_REVIEW.md` for the internal review and `VALIDATION.md` for release checks.

The supplied `paper/main.pdf` is preserved, but its original build has unresolved citations because BibTeX was unavailable. Treat it as a draft. Rebuild from `paper/main.tex` and `paper/references.bib` with `pdflatex main`, `bibtex main`, then `pdflatex main` twice before paper submission.

The generation script reproduces the task catalog only. It does not regenerate `synthetic_reference_runs.jsonl`; those supplied synthetic runs remain available for reproducing scoring. No claim of complete run-data generation reproducibility is made.

