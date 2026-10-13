"""Freeze once, after development checks and before any held-out execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT=Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
    return h.hexdigest()

if __name__=='__main__':
    assert not (ROOT/'FREEZE.json').exists(), 'Freeze already exists'
    assert not list((ROOT/'runs').glob('*.jsonl')), 'Held-out execution already started'
    development=[]
    for i in range(2):
        p=ROOT/'smoke'/f'model_{i}.jsonl'
        records=[json.loads(line) for line in p.read_text(encoding='utf-8').splitlines()]
        assert len(records)==20 and all(r['split']=='train' and not r['infrastructure_error'] for r in records)
        development.append({'model_index':i,'episodes':20,'trace_sha256':sha(p)})
    assets=json.loads((ROOT/'local_assets.json').read_text())
    public=json.loads((ROOT/'ASSET_MANIFEST.json').read_text())
    for local,published in zip(assets['models'],public['models']):
        assert local['id']==published['id'] and local['revision']==published['revision']
        published['weight_sha256']={p.name:sha(p) for p in Path(local['local_path']).glob('*.safetensors')}
        assert published['weight_sha256']
    (ROOT/'ASSET_MANIFEST.json').write_text(json.dumps(public,indent=2)+'\n')
    files=['PROTOCOL.md','run_study.py','measurement.py','selector_policy.py','analyze.py',
           'download_assets.py','freeze_study.py','tasks.json','ASSET_MANIFEST.json','requirements-lock.txt',
           'test_measurement.py','test_analysis.py','test_harness.py']
    result={'frozen_at_utc':datetime.now(timezone.utc).isoformat(),
            'status':'local protocol freeze before held-out evaluation; not public preregistration',
            'planned_episodes':720,'development':development,
            'files':{name:sha(ROOT/name) for name in files}}
    (ROOT/'FREEZE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['frozen_at_utc'], 'Frozen',len(files),'files; 720 episodes planned.')
