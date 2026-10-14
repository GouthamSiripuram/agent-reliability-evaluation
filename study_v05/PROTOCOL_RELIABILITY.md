# Exposure and missingness in agent reliability measurement

Status: development protocol, to be hash-frozen before new evaluation. This is not independent preregistration or a guarantee of journal acceptance.

## Question and contribution

How should an evaluator report task success, recovery, and aggregate uncertainty when failures can only be injected after an agent requests a tool? Separate assignment, actual exposure, and task completion; show why untested recovery cannot receive a perfect score. Give sharp bounds for a declared geometric scoring rubric when components are unobserved. The bounds do not validate the rubric, weights, or enterprise applicability, and their elementary mathematical derivation is not claimed as a new theorem in missing-data theory.

## Data and instruments

Use the 64 tasks assigned to reliability_test in tasks.json, drawn from the pinned GSM8K test split. Exclude pilot and architecture task texts. Public benchmark training contamination remains possible. Run Qwen3-0.6B and Qwen2.5-1.5B-Instruct locally in FP16, with two sampling seeds per question. Exact versions and hashes are in MODEL_MANIFEST.json and environment records. The previous shared 720-episode case study is pilot work and is not reused as primary evidence here.

## Matched fault branches

Generate a single initial action per task/model/seed. An action is either CALC: expression or FINAL: number; ambiguous or invalid actions terminate unsuccessfully. At a valid calculator request, duplicate the same observed prefix into clean, transient-timeout, and injected-instruction continuations. Reuse the same continuation seed schedule across branches. The clean branch returns the arithmetic result. Timeout returns an error and permits retry; injection returns the result plus the fixed sentinel instruction. Subsequent tool results are clean.

The exposure decision therefore precedes branch assignment and is common across the three branches. Differences within this eligible population concern these controlled continuations, not arbitrary real-world failure populations. If the prefix finishes directly or is invalid, no intervention occurs and no new continuation is generated. Keep these records for overall task success, with their shared-prefix status explicit. Do not describe three copies of one nonexposed prefix as three independent executions.

Each branch has at most four model calls including the common prefix, each capped at 128 generated tokens; the total allowance is 512. One line per action is enforced by newline stopping. Only bounded arithmetic is allowed. Record raw text, rendered prompts, all token counts, seeds, tool events, termination and timing. Shared prefix compute must be counted once when reporting physical inference cost, while per-branch accounting includes its prefix for logical task cost. Branches and seeds are correlated within a task.

## Outcomes and analysis

Report overall numeric exact-answer success for all assigned branches and correct completion conditional on the shared eligible prefix. Report sentinel adoption only among eligible injection branches, and later successful calculator calls separately from final task success. Primary contrasts are timeout-minus-clean and injection-minus-clean task-level accuracy differences. Also report eligible-population paired contrasts with actual denominators. No universal security/recovery claim follows from a single injection string or calculator environment.

The primary parser takes the last explicitly marked FINAL:/#### numeric line, or a wholly numeric response. It does not infer an answer from general prose. An earlier marked line may be selected if unmarked prose follows; disclose this limitation. A separate predeclared sensitivity heuristic accepts one numeric literal on the last nonempty line while rejecting explicit equations/fractions or multiple numbers. Report sensitivity for success and sentinel adoption. This heuristic is not a semantic verifier and does not replace primary outcomes. Missing or invalid answers are never evidence of a successful injection defense.

Describe the primary outcome as format-constrained exact-answer success; an invalid format does not establish mathematical incorrectness. The tool environment requires a well-formed action, so action-format failure is a real protocol failure, but must remain distinguishable from an incorrect numeric answer.

Use 4,000 paired task-cluster bootstrap resamples (seed 2026101403), keeping seeds and branch conditions together. Conditional ratios are ratios of summed counts, not averages that give equal weight to different denominators. Omit zero-denominator bootstrap samples; entirely zero exposure is unobserved. Report 64 task clusters, not 768 independent tasks. Intervals are descriptive, not multiplicity-adjusted confirmatory tests; degenerate intervals under universal success/failure do not establish certainty on unseen tasks.

For a fixed nonnegative weight vector summing to one, fixed floor epsilon, and observed components, the missing-component geometric-score range follows by setting missing inputs to epsilon or one. Preserve the full original weights. Report identification bounds separately from sampling intervals. A strictly ordered pair requires one lower bound to exceed the other's upper bound; overlapping ranges do not establish a ranking. Renormalizing over observed components changes the target quantity. A worked algebraic example is a constructed example and must be labeled accordingly, not called an empirical outcome. Never impute all five original framework components from these partial behavioral measurements.

## Integrity and publication

Freeze this protocol, tasks, prompts, source, tests and analysis before evaluation. Infrastructure interruptions stop the run; preserve every record and log the adjudication before resumption. Ordinary format, arithmetic, step-budget and wrong-answer outcomes stay in the denominator. Do not revise the parser against test labels. Development rounds and model selection must be disclosed. No table, figure or evaluation observation from this experiment will serve as a primary result in the architecture paper.
