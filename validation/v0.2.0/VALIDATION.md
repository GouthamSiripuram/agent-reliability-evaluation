# Publication validation

Python 3.12.14 on Windows.

## Tests

```text
.......                                                                  [100%]
7 passed in 1.87s
```

## Notebook

All 2 code cells in `notebooks/reproduce_results.ipynb` executed successfully using an in-process IPython interpreter; outputs saved. A separate Jupyter kernel was not launched. Results describe synthetic demonstrations only.

## Data generation

`generate_synthetic_data.py` executed successfully. Generated `task_catalog.jsonl` matches the supplied records: True. A description-only mismatch was corrected in the generator to preserve the supplied task catalog.

## Limits

The supplied paper PDF has unresolved citations; original PDF and source are preserved. No empirical model experiments or independent human peer review were performed.

The supplied generator does not regenerate the synthetic run observations.

## Environment

- pandas: 3.0.1
- pytest: 9.1.1
- nbformat: 5.11.1
- IPython: 9.17.1
