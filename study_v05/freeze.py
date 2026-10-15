"""Freeze only after completed development review; never overwrite an existing freeze."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    if (ROOT/'FREEZE.json').exists():
        raise RuntimeError('Freeze already exists')
    if not (ROOT/'development/COMPLETE.json').exists():
        raise RuntimeError('Development has not completed')
    review=json.loads((ROOT/'DEVELOPMENT_REVIEW.json').read_text(encoding='utf-8'))
    if not review.get('ready_to_freeze'):
        raise RuntimeError('Development review not approved by the technical audit')
    if (ROOT/'runs').exists():
        raise RuntimeError('Evaluation directory exists before freeze; investigate')
    local=json.loads((ROOT/'local_assets.json').read_text(encoding='utf-8'))
    public={'models':[]}
    for model in local['models']:
        hashes={}
        for p in Path(model['local_path']).glob('*'):
            if p.is_file():
                h=hashlib.sha256()
                with p.open('rb') as f:
                    for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
                hashes[p.name]=h.hexdigest()
        public['models'].append({k:v for k,v in model.items() if k not in ['local_path','files']}|{'files':hashes})
    (ROOT/'MODEL_MANIFEST.json').write_text(json.dumps(public,indent=2),encoding='utf-8')
    (ROOT/'requirements-lock.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True),encoding='utf-8')
    files=[*ROOT.glob('*.py'),ROOT/'tasks.json',ROOT/'MODEL_MANIFEST.json',ROOT/'DATA_PROVENANCE.json',
           ROOT/'PROTOCOL_RELIABILITY.md',ROOT/'PROTOCOL_ARCHITECTURE.md',ROOT/'requirements-lock.txt',
           ROOT/'DEVELOPMENT_REVIEW.json',ROOT/'DEVELOPMENT_LOG.md']
    manifest={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'status':'Local protocol/code freeze before evaluation; not independent public preregistration',
        'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    with (ROOT/'FREEZE.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2)
    print('Frozen',len(files),'files at',manifest['timestamp_utc'])


if __name__=='__main__':main()
