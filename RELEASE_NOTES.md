# v0.3.0 — methodology preprint and reproducibility update

Prepared for a versioned release; this file alone does not mean a GitHub tag or release has been created.

- Expanded the manuscript with explicit assumptions, synthetic demonstrations, limitations, related work, and AI-assistance disclosure.
- Audited all retained references against primary records and qualified novelty claims.
- Generated paper tables and sensitivity figures directly from the reference implementation.
- Fixed fractional binary-outcome acceptance, invalid missing-data policies, and weight-sum overflow; added dimension coverage reporting.
- Tests: 16 passed in 2.28s. Both notebook code cells executed in-process using IPython; data-generation record comparison and CFF validation passed.
- Preserved v0.2.0 draft and validation history. Restored the complete standard MIT disclaimer (the supplied LICENSE was truncated); the original notice remains archived. Standard text: https://opensource.org/license/mit.

No real-agent empirical results, independent human peer review, arXiv identifier, or project DOI are claimed.

## Manual release and optional Zenodo archive

1. After inspecting the final files, open this repository's Releases page and choose **Draft a new release**.
2. Create tag `v0.3.0` at the publication commit listed in the handoff. Use the title above and the change list from this file.
3. Attach `agent_reliability_arxiv_submission.zip` and `agent_reliability_preprint.pdf`; publish the release if satisfied.
4. For a Zenodo DOI, first sign in to Zenodo, link the GitHub account under account settings, open the GitHub integration page, and enable this existing repository. Enable it **before** publishing the GitHub release to trigger archiving.
5. After archiving completes, inspect the Zenodo record's author, title, version, license and files. Copy the actual assigned DOI into citation metadata only after verification. No DOI has been reserved or fabricated here.

Official instructions: https://help.zenodo.org/docs/profile/linking-accounts/ ; https://help.zenodo.org/docs/github/enable-repository/ ; https://help.zenodo.org/docs/github/archive-software/github-upload/ .
