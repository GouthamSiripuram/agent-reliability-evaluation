# Local model case study

Author: Goutham Siripuram. Local inference only; no paid/cloud inference.

This directory specifies actual model executions on a small public benchmark sample. It is separate from the original synthetic demonstration files. The exact study status is determined by the run records and analysis integrity checks; the protocol's planned count is not a completed-result claim.

- Read PROTOCOL.md before interpreting results.
- FREEZE.json records the local pre-evaluation protocol/code hashes; it is not an independent public preregistration.
- ASSET_MANIFEST.json pins model/dataset revisions and records the original hardware.
- tasks.json contains development and held-out task IDs, questions and scoring answers. Gold answers are never passed to the models.
- results/episodes.csv contains actual episode measurements once the complete analysis passes.
- results/traces_model_*.jsonl.gz retains raw prompts, responses, tool events and framework traces.
- Original synthetic files elsewhere in the repository remain synthetic.

Both companion repositories contain the same empirical study. These are shared observations, not independent experiments or replications.

## Reproduce

The recorded environment is Python 3.12 on Windows with an NVIDIA 4 GB GPU. Create a separate virtual environment. Install the CUDA build of PyTorch first from its official index, then the pinned requirements:

```bash
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
python -m pip install -r empirical/requirements-lock.txt
python empirical/download_assets.py
python -m pytest empirical -q
python empirical/run_study.py --run
python empirical/analyze.py
```

The download step requires internet access and several GB of disk space. It downloads pinned assets and writes a machine-local local_assets.json; that file is intentionally not published. All subsequent inference is offline, with no remote model code. Set up a fresh runs/ directory for a new replication; the runner resumes existing records and does not overwrite them. Do not merge new runs into the released result set. The frozen source files must remain unchanged for the runner's integrity check. A different environment can change timings and sampled outputs even with identical seeds.

For analysis of the released traces without rerunning inference, extract each results/traces_model_N.jsonl.gz to runs/model_N.jsonl using a gzip tool, then run analyze.py with NumPy/pandas installed. Keep the released results separate if comparing replications. The analyzer requires all 720 unique planned keys, including unsuccessful runs, and stops on infrastructure errors or inconsistent scoring.

## Interpretation

Twelve math tasks and two small checkpoints do not establish enterprise reliability. The benchmark may overlap model training. Numerical exact-answer success and limited injected tool faults observe only part of the proposed reliability framework. No complete five-dimensional score is manufactured. Architecture comparisons include differences in prompts, interface compliance and role budget allocation. The fixed selector's task descriptors are unvalidated proxies, its coefficients are not fitted, and its observed oracle is uncertain. No dollar or energy costs are measured.

See THIRD_PARTY_NOTICES.md for dataset provenance and licensing. Generative-AI tools assisted with implementation, analysis and technical review; Goutham Siripuram remains the responsible human author. This is not independent human peer review.
