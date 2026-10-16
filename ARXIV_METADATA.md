# arXiv metadata — author review required

Title: Reporting Agent Reliability under Partial Observation: Exposure-Matched Fault Tests and Score Bounds

Authors: Goutham Siripuram; Akshitha Mulastam

Author contributions: Both authors contributed equally to this work.

Suggested primary category: cs.AI
Suggested secondary category: cs.SE (subject to arXiv classification)

Abstract:
Fault tests can produce misleading reliability summaries when task completion, actual exposure, and recovery are treated as interchangeable observations. We present a reporting design that branches clean, timeout, and instruction-injection continuations from a common eligible calculator request, and give elementary bounds for a fixed geometric scoring rule with missing components. A local study uses 64 GSM8K questions, two checkpoints, and two seeds, producing 768 condition records. Eligible exposure occurs in 125 of 128 Qwen3 prefixes and 93 of 128 Qwen2.5 prefixes. Injection reduces overall format-constrained success by 21.88 and 24.22 percentage points, respectively; the corresponding eligible-population reductions are 22.40 and 33.33 points. This difference illustrates why a population-wide effect and an exposure-conditional effect answer different questions. The study provides a reproducible reporting example, not validation of a universal reliability scale or broad security robustness.

Comments: 6 pages, 1 figure. Local benchmark evaluation; code and execution records accompany the research release.

License recommendation: CC BY 4.0 for the manuscript, consistent with TMLR submission licensing. Author must select the license. Third-party assets retain their upstream licenses.

Keywords: agent evaluation; fault injection; partial observation; reliability measurement

GitHub repository: https://github.com/GouthamSiripuram/agent-reliability-evaluation

AI-assistance disclosure: Generative AI assisted drafting, code development, editing, and internal technical validation. The human authors are responsible for the manuscript and its scientific claims. This assistance is not independent peer review.

Status: prepared preprint; not submitted to arXiv or TMLR. No arXiv ID or DOI has been assigned. The anonymous review template's standard header does not mean a submission has occurred.
