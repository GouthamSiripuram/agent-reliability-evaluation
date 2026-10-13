# Bibliography verification

Checked 2026-10-12 against primary proceedings or versioned arXiv records. Each retained reference has a verified title, author list, year and canonical identifier/URL. Venue is supplied only where verified; versioned arXiv citations do not imply a proceedings publication. No DOI is assigned to this project.

## yao2023react

[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

Supported use: Interleaving reasoning and actions; ICLR camera-ready version identified by the arXiv record.

## shinn2023reflexion

[Reflexion: Language Agents with Verbal Reinforcement Learning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)

Supported use: Language feedback and episodic memory. Five authors match the conference record; later arXiv authorship differs.

## schick2023toolformer

[Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html)

Supported use: Learning API use. Conference author list includes Eric Hambro; the older arXiv list differs.

## liu2024agentbench

[AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688)

Supported use: Interactive agent evaluation in multiple environments; ICLR 2024 identified in the source record.

## zhou2024webarena

[WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)

Supported use: Web interaction and task evaluation; does not validate the present metrics.

## mialon2024gaia

[GAIA: A Benchmark for General AI Assistants](https://proceedings.iclr.cc/paper_files/paper/2024/hash/25ae35b5b1738d80f1f03a8713e405ec-Abstract-Conference.html)

Supported use: General-assistant tasks involving reasoning and tool use. Five authors follow the official proceedings metadata; some PDF/arXiv versions include Craig Swift. Version difference retained here explicitly.

## drouin2024workarena

[WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?](https://proceedings.mlr.press/v235/drouin24a.html)

Supported use: Enterprise web workflows; not evidence for the proposed coefficients.

## xie2024osworld

[OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html)

Supported use: Real computer environment tasks and execution-based evaluation.

## rabanser2026reliability

[Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666v3)

Supported use: Multidimensional reliability profile: consistency, robustness, predictability and safety. Cited version is arXiv v3; its record states acceptance at ICML 2026. No unverified proceedings pagination supplied.

## debenedetti2024agentdojo

[AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)

Supported use: Prompt-injection evaluation in tool-using agents; motivates separate security measures.

## Original bibliography disposition

All eight original works exist. Expanded abbreviated author lists, supplied canonical links, and corrected the IJCAI survey entry type where retained. Original entries not cited in this manuscript were omitted from its submission bibliography, not treated as nonexistent. Added only directly relevant sources. Version-dependent author lists are documented above; metadata is not combined across editions. Claims of metric novelty, empirical calibration or architecture superiority are not supported by these citations and are not made. This is a targeted citation audit, not a systematic literature review.


## v0.4.0 empirical extension (checked 2026-10-13)

- `cobbe2021gsm8k`: [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168v2), Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman (2021). Title, complete authorship and versioned identifier verified against the primary arXiv record. Used only for GSM8K provenance and task type; upstream model results are not substituted for our measurements. No unverified venue supplied.
- Official [Qwen3-0.6B card](https://huggingface.co/Qwen/Qwen3-0.6B) verifies checkpoint identity, Apache-2.0 license, and non-thinking configuration. Official [SmolLM2-360M-Instruct card](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) verifies its identity and Apache-2.0 declaration. Cited as source footnotes, not invented scholarly papers. Exact revisions are in ASSET_MANIFEST.json.
- Versioned [smolagents model documentation](https://huggingface.co/docs/smolagents/v1.21.2/en/reference/models) supports the local model-adapter interface. The actual adapter and agent behavior were checked in installed source and development tests.
- [Dataset card](https://huggingface.co/datasets/openai/gsm8k) and [original MIT notice](https://github.com/openai/grade-school-math/blob/master/LICENSE) support provenance/licensing. The original notice is retained in empirical/THIRD_PARTY_NOTICES.md.

The earlier bibliography audit remains applicable to unchanged background claims. No new project DOI, arXiv identifier, peer-review status or citation count is claimed. This remains a targeted reference audit, not a systematic review.
