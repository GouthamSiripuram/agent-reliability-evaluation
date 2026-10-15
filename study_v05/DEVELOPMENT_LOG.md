# Development record

No new held-out evaluation has run. All rounds below use the same eight designated GSM8K training questions; their outputs are excluded from final evaluation. The published v0.4 pilot remains unchanged.

## Round 1

112 logical episode records across Qwen3-0.6B and SmolLM2-360M-Instruct. Raw records and a source snapshot are preserved in development_round1/. All final scored answers were incorrect, including a mixture of genuine math errors and invalid final-answer formats. No result was reclassified as correct merely to improve accuracy.

Observed interface problem: models sometimes emitted CALC and FINAL in one response without waiting for a calculator result. The environment rejected this ambiguity. Tool turns now stop at the first newline, enforcing the documented one-action interaction rather than allowing the model to invent a tool result. Original raw responses remain preserved.

Architecture prompts had encouraged concise answers so strongly that Qwen often skipped working through the arithmetic. The development revision requests intermediate calculations and a separate explicit numeric final line. The strict scorer still rejects a marked equation instead of accepting its first number. Planning uses a separate system instruction, without a contradictory demand for a final numeric solution.

The pilot and round-1 development show that SmolLM2 is a poor primary instrument for these tasks and interfaces. A larger public checkpoint, Qwen2.5-1.5B-Instruct, is being downloaded and tested for local GPU fit. Model selection happens before any new held-out outcome is observed. This is development selection, not an independent test of model superiority. Round-1 SmolLM2 outcomes will remain documented.

## Round 2

Round 2 is running with Qwen3-0.6B and the downloaded Qwen2.5-1.5B-Instruct. The latter fits locally at approximately 3301 MiB GPU memory. The Qwen3 portion completed 56 logical records, with 14 primary successes and 46 numeric parses. All eight initial requests were valid calculator requests. These are development observations only.

Development review found correct arithmetic expressed in prose without the requested marker. Before evaluation, a separate last-line single-number sensitivity heuristic was added to the analysis. The primary scorer and existing recorded outcomes are unchanged. The heuristic rejects explicit equations/fractions and multiple numbers but is not a semantic verifier. Report dependence on scoring choice rather than selecting the favorable score.

Orchestration was also hardened to reject mismatched model identities, verify checkpoint file hashes before evaluation, and avoid declaring the entire study complete after a single-model run. These changes do not alter already executed development prompts or primary outcomes. Full evaluation remains prohibited until development completes and the reviewed source/analysis are frozen.

Before freeze, the planned GSM8K budget-transfer comparison was changed from 256 to 1024 tokens. Development showed many truncated intermediate/verifier outputs at 512, so an even lower budget would mostly worsen a known interface/budget limitation. The larger allowance tests whether this limitation eases; it is not selected from test outcomes. Call generation timeout increases from 60 to 120 seconds, context cap stays 4096. All fixed allocations scale proportionally. A separate development smoke check will test the larger allowance.

Round 2 completed 112 records with a passing integrity audit. Qwen3: 14 primary successes; Qwen2.5: 5 primary successes. The separately reported last-line sensitivity gives 14 and 21 respectively, reinforcing that primary format-constrained success is not a pure mathematical-ability metric. The 1024-token development check completed 16 additional records on the first two designated development tasks with no infrastructure failures. Both checkpoints fit the GPU. Twenty-one new tests passed, including full analysis on artificial unit fixtures and independent per-study analysis. No artificial unit fixture is included in experimental results.
