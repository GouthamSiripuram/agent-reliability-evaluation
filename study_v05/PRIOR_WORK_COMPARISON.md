# Focused method comparison after completed evaluation

Primary method sections inspected 2026-10-15 UTC. This comparison narrows publication claims; it changes no frozen experimental input and is not an independent reproduction of the cited systems.

## Reliability: SSCBench

Source: https://arxiv.org/html/2610.11514v1, sections III-A through III-C and IV-A. Authors: Xincheng He, Wanli Dong, Zhaoqiang Guo, Yan Liu, Lei Xu.

SSCBench specifies fault assertions, authoritative refutations, and their timing relative to dependent use. Admission requires a legal continuation that could expose refutation before use; execution reconstruction then distinguishes realized early, late, or absent evidence. Its fault contracts include corrupted reads and suppressed state updates in retail/airline environments.

Our eligibility is narrower: a valid first calculator request determines whether a shared prefix can receive one of three continuations. We compare clean, timeout, and instruction-injection outcomes within that common population. We do not reconstruct semantic counterevidence arrival, first faulty reliance, or state-update correctness. Our elementary geometric-score interval is a separate scoring-rubric calculation.

Shared concern: an outcome's interpretation depends on the population and observations that support it. Distinction: pre-intervention exposure matching versus post-intervention evidential timing. That distinction does not establish priority or a major new framework. Position the paper as a bounded reporting case study; do not claim to replace or outperform SSCBench.

## Architecture: CB-Orchestrator

Source: https://arxiv.org/html/2610.13064v1, sections 3.2--3.3 and the ablation discussion. Authors: Jiahang Sun, Zhiwei Shang, Zhipiao Liu, Hongwei Yang, Guoqing Xie, Shuang Qiu, Zhongxiang Dai.

CB-Orchestrator separates evolutionary construction of candidate workflows from contextual-bandit selection. Its representation combines embeddings of query text and workflow code; a neural reward predictor and linear exploration bonus select training interactions. Its ablations include a static workflow pool and linear/neural bandit variants.

Our study uses four manually fixed workflows, six lexical counts, exhaustive two-seed training observations, and separate ridge predictors. There is no workflow evolution, embedding model, bandit exploration, or adaptive feedback collection. Our evaluation concerns transfer of a fixed policy under changed output allowances and benchmark data, with a separate parsing sensitivity.

Shared concern: query-dependent choice among workflows. The simpler training and representation are not novel algorithms. The negative findings cannot refute CB-Orchestrator because we did not implement or compare its method under shared conditions. Position the paper as a constrained baseline evaluation, and make the absence of stronger learned-selector comparisons explicit.

## Editorial consequence

Both manuscripts must acknowledge the close work and avoid first-in-field claims. Completed execution records establish that observations were collected, not that either paper makes a sufficient journal contribution. The reliability study can document the magnitude of an exposure-denominator distinction; the architecture study can document failure of this baseline and scorer-dependent interpretation. Whether these lessons are sufficient for TMLR remains unresolved pending the full manuscript and author review. No retrospective tuning, extra model selection, or silent replacement of primary outcomes is authorized by this comparison.
