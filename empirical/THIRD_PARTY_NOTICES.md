# Third-party provenance

The study downloads checkpoints from Qwen/Qwen3-0.6B and HuggingFaceTB/SmolLM2-360M-Instruct. Their pinned model cards specify Apache-2.0. Checkpoint weights are not redistributed in these research repositories. smolagents, Transformers and PyTorch retain their upstream licenses. Exact revisions and package versions are recorded in ASSET_MANIFEST.json and requirements-lock.txt.

The 14 question/answer records in tasks.json (two development and twelve test examples) come from the main configuration of openai/gsm8k, revision 740312add88f781978c0658806c59bc2815b9866. They are existing benchmark examples, not newly fabricated data. Model traces reproduce these questions as inputs. Source: https://huggingface.co/datasets/openai/gsm8k. Original dataset paper: Karl Cobbe et al., Training Verifiers to Solve Math Word Problems (2021), https://arxiv.org/abs/2110.14168.

The dataset's MIT notice follows, from https://github.com/openai/grade-school-math/blob/master/LICENSE:

MIT License

Copyright (c) 2021 OpenAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
