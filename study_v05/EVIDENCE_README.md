# Anonymous reliability review evidence

Contains 768 completed records for this study, unchanged frozen source files, selected tasks, and reference results. The full frozen manifest includes the related protocol and disjoint task cohorts to preserve provenance; only this study's model records are packaged. Historical development notes describe status at freeze, not the current completion state. No GPU rerun is needed to analyze these records.

Install dependencies from requirements-lock.txt in a separate environment. Run:

    python -m pytest test_research.py test_analysis.py
    python analysis.py --study reliability

Results are written to results/reliability/. Compare against reference_results/. The analysis verifies frozen hashes and exact study record keys before calculating results. Floating-point environment changes can affect last-digit precision.

Inference replication: in a fresh copy, archive the supplied runs directory before starting an independent replication. Resolve local checkpoint paths with `python setup_replication.py --cache-dir YOUR_CACHE --output local_assets.json`, then `python run_studies.py --run --study reliability`. Never overwrite the supplied evidence or run two GPU jobs simultaneously. No paid service is required. Preserve interruptions and failures.

One unexplained interruption and one author-requested pause occurred in the combined program; all saved records were retained and resumed without repeating keys. Unknown unsaved compute is not included in completed-record accounting. The two studies share software and development ancestry, not primary evaluation questions. Public benchmark contamination is possible.

Generative AI assisted code development, drafting, editing and internal validation. Human author responsibility remains. This is not independent human peer review. Files are supplied for review; third-party notices remain intact. No author-identifying repository links are included.
