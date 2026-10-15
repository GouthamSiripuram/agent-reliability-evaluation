"""Local Hugging Face inference with explicit call-level accounting."""
from pathlib import Path
import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

ROOT = Path(__file__).resolve().parent
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


class LocalModel:
    def __init__(self, asset):
        self.model_id = asset['id']
        self.tokenizer = AutoTokenizer.from_pretrained(asset['local_path'], local_files_only=True, trust_remote_code=False)
        self.network = AutoModelForCausalLM.from_pretrained(asset['local_path'], local_files_only=True,
            trust_remote_code=False, dtype=torch.float16, attn_implementation='sdpa').to('cuda').eval()

    def call(self, messages, limit, seed, role, stop_line=False):
        if not 0 < limit <= 1024:
            raise ValueError('Invalid call budget')
        set_seed(seed)
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False,
            add_generation_prompt=True, enable_thinking=False)
        tokens = self.tokenizer(prompt, return_tensors='pt').to('cuda')
        if tokens.input_ids.shape[1] > 4096:
            raise ValueError('Context limit exceeded; no truncation')
        torch.cuda.synchronize(); start = time.perf_counter()
        with torch.inference_mode():
            output = self.network.generate(**tokens, max_new_tokens=limit, do_sample=True,
                temperature=.7, top_p=.9, top_k=50, max_time=120,
                pad_token_id=self.tokenizer.eos_token_id,
                **({'stop_strings':['\n'],'tokenizer':self.tokenizer} if stop_line else {}))
        torch.cuda.synchronize()
        ids = output[0, tokens.input_ids.shape[1]:]
        return {'role': role, 'seed': seed, 'messages': messages, 'rendered_prompt': prompt,
            'response': self.tokenizer.decode(ids, skip_special_tokens=True),
            'input_tokens': int(tokens.input_ids.shape[1]), 'output_tokens': int(len(ids)),
            'limit': limit, 'hit_token_limit': len(ids) == limit, 'stop_at_newline':stop_line,
            'seconds': time.perf_counter() - start}
