# v0.3.0 publication validation

Audit date: 2026-10-12. Base repository commit: `f4627f08ea2bad1f6546db88afaa2eabebfc8a7f`.

## Inspected material

Inspected the current GitHub file tree and local README, CITATION.cff, LICENSE, paper sources and bibliography, original diagrams, all source modules, tests, data schemas/records, generators, notebooks, submission notes, and historical validation/internal-review documentation. Original data files and SVG diagrams remain preserved. The v0.2 NaN/range checks, unobserved-recovery handling, and independent architecture-scenario generation are present in implementation, not just README claims.

## Corrections and remaining limits

The old PDF had unresolved citations; the current bibliography and references compile cleanly. Manuscripts now state their formulas, assumptions, synthetic evidence, limitations, related work, and generative-AI assistance. No real-agent experiment or human peer review was performed. The original internal review remains unchanged.

Fixed truncation of fractional binary outcomes, validation of missing-policy values even without missing components, and overflowing weight sums. Added observed_dimension_count and stratified notebook summaries. The consistency helper measures unanimity, including repeated failure; the manuscript explicitly distinguishes this from success. The run-observation generator remains unavailable; only scoring and task-catalog generation are reproducible.

The supplied MIT notice had a truncated disclaimer; the full standard disclaimer is restored and the original is archived. No license change to a different license family was made.

## Executed checks

```text
................                                                         [100%]
16 passed in 2.28s
```

- Notebook: both code cells executed successfully in an in-process IPython interpreter. A separate Jupyter kernel was not launched. Reliability notebook re-executed after adding coverage stratification.
- Paper reproduction script: generated the tables, PDF figure, input hashes and row-level summaries from supplied data/reference code.
- Generator: generated records exactly equal the supplied task catalog.
- CITATION.cff: validated against the CFF 1.2.0 schema with cffconvert 2.0.0.
- Bibliography: 10 used entries verified against primary records. Every cited key has exactly one bibliography entry and rendered item. See BIBLIOGRAPHY_AUDIT.md for source/version decisions.
- Source package: extracted into a new temporary directory, compiled with Tectonic 0.17.0 using cached standard TeX resources and automatic BibTeX/reruns. Only packaged manuscript inputs were used. The dependency manifest listed main.tex, references.bib, required tables and the required PDF figure.
- Final build: no LaTeX warnings, undefined citations/references, missing characters or overfull boxes in the final log; no fatal errors. A local font-configuration warning on an earlier verification run was resolved before final builds.
- Final PDF: 6 pages, all visually inspected. Tables, plot, equations, author, links, bibliography and page numbers render correctly; extracted text contains no `??` or `[?]` markers.
- ZIP contents: only `main.tex`, `references.bib`, `main.bbl`, `tables/summary.tex`, `figures/sensitivity.pdf`. No raw dataset, notebook, code, review notes, git history, environment, credentials, or strategy material is packaged.

## Environment

Python 3.12.14; Windows-11-10.0.26200-SP0. Direct dependency pins are in requirements-reproduction.txt; this is not a complete transitive environment lock. Package versions and machine-readable outcomes are in results/validation.json. No clean-machine portability claim is made for Python notebooks; independent clean-folder LaTeX compilation was verified.

## Final quality gate

- [x] Every citation resolves and bibliography renders.
- [x] No unresolved LaTeX references or missing figures.
- [x] Author is Goutham Siripuram; no institutional affiliation invented.
- [x] Synthetic calculations explicitly identified; no fabricated empirical results.
- [x] References audited; no fabricated project DOI or arXiv identifier.
- [x] No claim of independent human peer review.
- [x] Correct GitHub repository URL and AI-assistance disclosure.
- [x] Source ZIP independently compiles; final PDF visually inspected.
- [x] Exact source ZIP supplied in submission/.

ZIP SHA-256: `b7e8440259ec910a723d531d4235b481d78ccd39d3d7be3fcf09114c9e16f963`

PDF SHA-256: `93b2a8d8439f026d2ae70a277fde0ba5bb4fc15e67d0774815bdc448d94beadd`

Status: technically ready for author inspection and manual arXiv submission. This is not a statement of arXiv acceptance or empirical scientific validation. Goutham must review and approve all claims and confirm the affiliation/license before submitting. No arXiv submission was attempted. GitHub release notes are prepared; no tag or release was created by this workflow.
