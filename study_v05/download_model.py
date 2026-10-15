"""Download one public checkpoint; inference remains entirely local."""
from pathlib import Path
import hashlib
import json
import os
ROOT = Path(__file__).resolve().parent
os.environ['HF_HOME']=str(ROOT.parent/'.hf-cache')
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
os.environ['HF_HUB_DISABLE_XET']='1'
from huggingface_hub import HfApi, snapshot_download

if (ROOT/'FREEZE.json').exists():
    raise RuntimeError('Do not replace frozen model manifest')
name='Qwen/Qwen2.5-1.5B-Instruct'
api=HfApi(token=False)
info=api.model_info(name)
path=snapshot_download(name,revision=info.sha,token=False,max_workers=1,
    allow_patterns=['config.json','generation_config.json','tokenizer*','vocab.json','merges.txt',
                    '*.safetensors','README.md','LICENSE*'])
previous=json.loads((ROOT.parent/'empirical/local_assets.json').read_text(encoding='utf-8'))['models'][0]
model={'id':name,'revision':info.sha,'local_path':path,'license':'apache-2.0',
    'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(path).glob('*') if p.is_file()}}
local={'models':[previous,model]}
(ROOT/'local_assets.json').write_text(json.dumps(local,indent=2),encoding='utf-8')
public={'models':[{k:v for k,v in m.items() if k!='local_path'} for m in local['models']]}
(ROOT/'MODEL_MANIFEST.json').write_text(json.dumps(public,indent=2),encoding='utf-8')
print('Downloaded pinned checkpoint',name,info.sha,flush=True)
