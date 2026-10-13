# Empirical measurements and interpretation

The JSONL traces are the authoritative raw records; CSVs are derived summaries. Empty CSV values mean missing/unobserved, not zero. Analysis uses raw JSONL records to avoid CSV type-inference changes. No assigned synthetic outcomes appear in this study directory.

| Field | Meaning |
|---|---|
| model | Pinned checkpoint identity; revision and weight hashes are in ASSET_MANIFEST.json. |
| task_id, split | Original GSM8K row and split. Only `test` rows enter published empirical summaries. |
| architecture | Concrete prompt, orchestration and role-budget configuration described in PROTOCOL.md. |
| condition | Assigned clean, timeout or injection condition; assignment alone does not imply exposure. |
| seed | Per-episode seed, one of 17, 43, 91. |
| timestamp_utc | End-of-episode timestamp. |
| answer, parsed_answer, correct | Raw final output, deterministic numeric parse, and exact equality with the gold answer. Intermediate reasoning is not judged for correctness. |
| error | An exception escaping the episode orchestration, such as exhausted role budget. Framework-caught parsing errors can appear in agent logs without setting this field. |
| infrastructure_error | Unexpected failure inside actual model generation. Such errors stop the study for explicit adjudication. |
| fault_exposed | A valid calculator request triggered the assigned intervention. False is not successful recovery or injection resistance. |
| sentinel_adopted | The parsed final answer equals the attack sentinel. The reported conditional metric additionally requires exposure. |
| input_tokens, output_tokens | Sum of actual token counts across successfully completed generation calls, including special/stop tokens where returned by the model. Output allowance is 512 per episode. |
| model_calls | Actual completed generation calls recorded in the trace. |
| tool_attempts | Calls reaching the calculator implementation, including rejected arithmetic expressions. Malformed JSON or schema errors rejected before the calculator are in framework logs and are not counted here. |
| elapsed_seconds | Total episode wall time, including orchestration; excludes model loading/download and warmup. |
| generation_seconds | Sum of synchronized generation-call timings. |
| tool_retried_successfully | Historical column name in the frozen analyzer: true when any later calculator call succeeds after a timeout. It does not require the same expression and does not imply task completion. Interpret as later successful tool use. |
| post_exposure_success | Correct final answers divided by actually exposed episodes in a cell. This is not necessarily successful tool retry. |
| mean_unanimity | Task mean of absolute(2 * success fraction - 1) across three seeds. Unanimous failure has value one. It is binary success unanimity, not semantic answer agreement. |

Condition summaries contain 36 attempts per model/configuration/condition cell. Paired effects use differences of task-level means between assigned conditions, including unexposed episodes. Conditional rates describe selected exposed populations, which can differ across architectures. Neither estimand should be silently substituted for the other.

The policy comparison uses clean runs only, with utility = correctness - 0.05 * generated tokens / 512. The fixed selector uses question-only proxies and unchanged coefficients; it is not trained. The observed oracle is the best mean utility among four tested configurations on each task and is optimistic/noisy with only three seeds. Regret is relative to that observed oracle, not a known globally optimal policy.

All 95% intervals are exploratory task-cluster bootstrap percentile intervals. Degenerate zero-width intervals can occur for all-failure observations and do not establish a zero success probability on unseen tasks. There are only 12 task clusters; repeated runs and the two companion papers must not be counted as independent task samples or independent studies. No monetary, energy, enterprise-deployment or full five-dimensional reliability score is measured.
