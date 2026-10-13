# v0.4.0 — local empirical case study

Prepared for a versioned release; this file alone does not create a GitHub tag or release.

- Added 720 actual local model episodes from two pinned Hugging Face checkpoints, four concrete configurations, three seeds, 12 GSM8K test questions, and controlled tool conditions.
- Preserved the original synthetic demonstrations and historical validation records.
- Added frozen protocol/code hashes, dependency and checkpoint provenance, complete compressed traces, exact-key checks, task-cluster uncertainty and fixed-policy comparisons.
- Kept all agent failures and distinguished fault assignment from actual exposure. No full FDAR score is imputed and no coefficient calibration is claimed.
- Updated the manuscripts, metadata, citation files and reproducibility instructions to distinguish the bounded empirical evidence from proposed methodology.
- Rebuilt self-contained source packages; see VALIDATION.md for final tests, compilation and visual checks.

Both companion papers share this study. No paid compute, independent human peer review, arXiv submission or project DOI is claimed.

## Manual release and optional Zenodo archive

1. After inspecting the final files, open this repository's Releases page and choose **Draft a new release**.
2. Create tag `v0.4.0` at the publication commit listed in the handoff. Use the title above and the change list from this file.
3. Attach `agent_reliability_arxiv_submission.zip` and `agent_reliability_preprint.pdf`; publish the release if satisfied.
4. For a Zenodo DOI, first sign in to Zenodo, link the GitHub account under account settings, open the GitHub integration page, and enable this existing repository. Enable it **before** publishing the GitHub release to trigger archiving.
5. After archiving completes, inspect the Zenodo record's author, title, version, license and files. Copy the actual assigned DOI into citation metadata only after verification. No DOI has been reserved or fabricated here.

Official instructions: https://help.zenodo.org/docs/profile/linking-accounts/ ; https://help.zenodo.org/docs/github/enable-repository/ ; https://help.zenodo.org/docs/github/archive-software/github-upload/ .
