"""Development-only GPU/runtime check for the predeclared larger budget."""
from pathlib import Path
import json
import gc
import torch
from local_model import LocalModel
from workflows import ARCHITECTURES, architecture_episode
from run_studies import make_record, append, load_records

ROOT=Path(__file__).resolve().parent
if (ROOT/'FREEZE.json').exists():
    raise RuntimeError('This development check must precede freeze')
if (ROOT/'development/RUNNING.lock').exists():
    raise RuntimeError('Other development GPU job still running')
assets=json.loads((ROOT/'local_assets.json').read_text(encoding='utf-8'))
tasks=[t for t in json.loads((ROOT/'tasks.json').read_text(encoding='utf-8')) if t['cohort']=='development'][:2]
out=ROOT/'development_budget';out.mkdir(exist_ok=True)
torch.set_num_threads(4)
for i,asset in enumerate(assets['models']):
    path=out/f'model_{i}.jsonl'
    done={(r['task_id'],r['workflow']) for r in load_records(path)}
    if len(done)==8:continue
    print('Loading budget-check model',asset['id'],flush=True)
    model=LocalModel(asset)
    for task in tasks:
        for workflow in ARCHITECTURES:
            if (task['task_id'],workflow) in done:continue
            answer,traces=architecture_episode(model,task['question'],workflow,1024,137)
            record=make_record(task,model,workflow,'clean',137,1024,answer,traces,
                {'development_check':'1024-token budget; excluded from evaluation'})
            append(path,record)
            print(i,task['task_id'],workflow,'tokens',record['output_tokens'],'correct',record['correct'],flush=True)
    del model;gc.collect();torch.cuda.empty_cache()
(out/'COMPLETE.json').write_text(json.dumps({'completed':True,'episodes':16}),encoding='utf-8')
