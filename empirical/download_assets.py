from pathlib import Path
import os, json, random, hashlib, platform, subprocess
ROOT=Path(__file__).resolve().parent
os.environ['HF_HOME']=str(ROOT.parent/'.hf-cache')
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
os.environ['HF_HUB_DISABLE_XET']='1'
from huggingface_hub import HfApi, snapshot_download, hf_hub_download
import pandas as pd
import torch

api=HfApi(token=False)
pinned=json.loads((ROOT/'ASSET_MANIFEST.json').read_text()) if (ROOT/'ASSET_MANIFEST.json').exists() else None
manifest={'models':[], 'dataset':{}, 'platform':platform.platform(),
          'torch':torch.__version__, 'cuda_available':torch.cuda.is_available()}
if not torch.cuda.is_available(): raise RuntimeError('CUDA unavailable; stop before study')
manifest['gpu']=torch.cuda.get_device_name(0)
manifest['gpu_total_bytes']=torch.cuda.get_device_properties(0).total_memory
for name in ['Qwen/Qwen3-0.6B','HuggingFaceTB/SmolLM2-360M-Instruct']:
    revision=next(m['revision'] for m in pinned['models'] if m['id']==name) if pinned else None
    info=api.model_info(name,revision=revision)
    print('Downloading pinned model',name,info.sha,flush=True)
    kwargs={'local_dir':str(ROOT.parent/'.hf-models'/name.replace('/','--'))} if name.startswith('HuggingFaceTB/') else {}
    path=snapshot_download(name,revision=info.sha,token=False,max_workers=1,
        allow_patterns=['config.json','generation_config.json','tokenizer*','special_tokens_map.json',
                        'vocab.json','merges.txt','*.safetensors','README.md','LICENSE*'],**kwargs)
    manifest['models'].append({'id':name,'revision':info.sha,'local_path':str(path),
        'license':getattr(info.card_data,'license',None),
        'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(path).glob('*') if p.is_file() and p.suffix!='.safetensors'}})
dataset='openai/gsm8k'; info=api.dataset_info(dataset,revision=pinned['dataset']['revision'] if pinned else None)
paths=api.list_repo_files(dataset,repo_type='dataset',revision=info.sha)
data={}
for split in ['train','test']:
    name=next(p for p in paths if p.startswith('main/'+split+'-') and p.endswith('.parquet'))
    path=hf_hub_download(dataset,name,repo_type='dataset',revision=info.sha,token=False)
    data[split]=pd.read_parquet(path)
    manifest['dataset'][split]={'file':name,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'rows':len(data[split])}
manifest['dataset'].update(id=dataset,revision=info.sha,configuration='main',license='mit')
indices=sorted(random.Random(104729).sample(range(len(data['test'])),12))
records=[]
for split,ids in [('train',[0,1]),('test',indices)]:
    for index in ids:
        row=data[split].iloc[index]
        records.append({'task_id':f'gsm8k-{split}-{index:04d}','split':split,'row_index':index,
            'question':row.question,'gold_answer':row.answer})
tasks_text=json.dumps(records,indent=2,ensure_ascii=False)+'\n'
if (ROOT/'FREEZE.json').exists():
    assert json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))==records, 'Pinned dataset task mismatch'
else:
    (ROOT/'tasks.json').write_text(tasks_text,encoding='utf-8')
(ROOT/'local_assets.json').write_text(json.dumps(manifest,indent=2)+'\n')
public={**manifest,'models':[{k:v for k,v in m.items() if k!='local_path'} for m in manifest['models']]}
if not (ROOT/'FREEZE.json').exists():
    (ROOT/'ASSET_MANIFEST.json').write_text(json.dumps(public,indent=2)+'\n')
    (ROOT/'requirements-lock.txt').write_text(subprocess.check_output([os.sys.executable,'-m','pip','freeze'],text=True))
print('Assets pinned; test indices:',indices,flush=True)
