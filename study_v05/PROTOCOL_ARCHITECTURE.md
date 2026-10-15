# Selecting bounded reasoning workflows using question-only features

Status: development protocol, to be hash-frozen before new evaluation. This is not independent preregistration.

## Question and limits

Can a small question-only routing model improve observed accuracy/cost utility over a single workflow chosen using training results? Evaluate whether planning and verification help under limited output allowances and whether a router transfers to different math-word-problem data. The workflows use the same checkpoint in all roles; roles are prompt and information-flow choices, not independent human experts. No blanket superiority of multiple agents or novel general scaling law is claimed. Existing related work already examines matched-budget comparisons and strong single-agent baselines.

## Separate cohorts

tasks.json fixes 64 GSM8K training questions, 64 distinct GSM8K test questions, and 64 SVAMP transfer questions. Eight other GSM8K training questions are reserved for implementation development; the pilot and reliability-study task texts are excluded. SVAMP sampling takes at most one question per numeric-masked body group. These public datasets may have appeared in model pretraining and both involve arithmetic word problems, so this is not broad cross-domain validation. No SVAMP answers or outcomes are used for fitting the router.

## Workflows and budgets

Use Qwen3-0.6B and Qwen2.5-1.5B-Instruct locally, with seeds 137 and 271. Four workflows use no external tools: direct solution; solution followed by self-refinement; a separate plan followed by solution; plan, solution, then a verifier response. These are concrete bounded inference workflows, not every implementation of the old architecture taxonomy.

All cohorts use an allowance of 512 generated tokens. Direct receives 512. Self-refinement receives 256+256. Plan/solve receives 96+416. Plan/solve/verify receives 96+288+128. Unused role allowances are not redistributed. The GSM8K test cohort also receives a predeclared 1024-token ablation with proportional allowances. This larger allowance was chosen during development because intermediate role truncation and absent final answers were common at 512 total tokens; no held-out result informed the change. Prompts and decoding are frozen in code. These are equal maximum output allowances, not equal realized tokens, FLOPs, money, latency or input-token costs. Report actual input/output tokens, generation time and limit hits. Compare role decomposition with self-refinement before attributing differences to additional agents.

## Routing and baselines

For each checkpoint, fit four ridge regressions to training-task mean utility, one per workflow. Predict from six question-only counts: words, numeric mentions, sentence punctuation, rate words, comparison words, and total words. Standardize using training means/standard deviations only, with unit scale for constant features; include an unpenalized intercept. Ridge penalty is fixed at one, with no held-out tuning. Each task's target averages its two seeds. Choose the largest predicted utility; ties use the declared workflow order. The baseline chooses the best mean-utility constant workflow using the same training cohort, with the same tie order. Also report all four fixed workflows, and the best observed test workflow only as an explicitly optimistic retrospective oracle.

Utility is correctness minus lambda times generated-token usage divided by the assigned episode allowance. Primary lambda=0.05; predeclared sensitivity values 0, 0.02 and 0.1 each refit on training results only. This exchange rate is a convention, not measured monetary cost. Compare router-minus-training-selected-constant utility on each evaluation cohort/budget. No retraining occurs on GSM8K test, its 1024-token ablation, or SVAMP. The 1024-token comparison is a transfer of the 512-token-trained router, not budget-specific calibration. The previous hand-specified architecture coefficients remain historical hypotheses; do not call them fitted by this study.

## Scoring and uncertainty

Use the strict documented parser: take the last explicit FINAL:/#### line, requiring its payload to be solely numeric, or accept an entirely numeric response. Equations, units and absent marked answers are invalid, not partially correct. An earlier marked line can be selected if unmarked prose follows; this is a parser limitation. Report format compliance as well as accuracy. Keep all outcomes. Use 4,000 task-cluster bootstrap resamples (seed 2026101403), retaining both seeds and all workflows/budgets for each sampled task. Main uncertainty conditions on the fitted router; it does not quantify variation from collecting a different training set. Report 64 distinct evaluation tasks per dataset, descriptive confidence intervals and paired differences, not just point estimates or a cherry-picked winning architecture. No significance claim follows from selecting the largest observed mean.

Predeclared format sensitivity: also report success under a separate heuristic accepting exactly one numeric literal on the final nonempty response line, allowing surrounding words/units/markup but rejecting multiple numeric literals or explicit equations/fractions. This heuristic can select an unrelated number and is not a semantic verifier. It never replaces primary scoring or the routing targets. This check was added during development after observing correct arithmetic expressed without the requested marker, before any held-out evaluation. Conclusions dependent on scorer choice must be qualified.

In the manuscript, call the primary outcome **format-constrained exact-answer success**. Do not equate a missing marker with proven mathematical incorrectness. Development showed a substantial scorer discrepancy for Qwen2.5; therefore any architecture-selection interpretation must discuss both scoring views. The primary routing target remains a protocol-compliant numerical response, not latent reasoning ability. If this distinction prevents a useful supported result, report that limitation instead of claiming broad architecture quality.

For the scoring sensitivity, keep the primary router's and primary training-constant's choices unchanged and compare their utilities under the heuristic scorer. Do not refit or pick a new best constant using test outcomes. Also report last-call budget saturation and candidate-to-revised-answer transitions for self-refinement and verification, under both scorers. These diagnostics are specified before evaluation and are descriptive explanations, not extra confirmatory hypotheses.

## Separation and integrity

The reliability paper uses a different GSM8K cohort and fault experiment; this paper will not reuse its result tables, figures or experimental observations. Common inference software and conceptual ancestry remain acknowledged. Freeze inputs, analysis and prompts before evaluating either held-out cohort. Save raw generations, task IDs, checkpoint hashes, code hashes and terminations. The human author must review claims and the accurate AI-assistance disclosure. Do not imply independent human review or guaranteed journal acceptance.
