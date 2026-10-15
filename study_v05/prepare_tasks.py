"""Select tasks without reading model outcomes; never overwrite a frozen split."""
from pathlib import Path
import hashlib
import json
import random
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
GSM_REV = '740312add88f781978c0658806c59bc2815b9866'
SVAMP_REV = '78e727689e1c1bebfc4be39c446898e8e10b0518'


def normalize(text):
    return re.sub(r'\W+', '', text.lower())


def main():
    if (ROOT/'FREEZE.json').exists():
        raise RuntimeError('Do not overwrite frozen tasks')
    gsm_root = ROOT.parent/'.hf-cache/hub/datasets--openai--gsm8k/snapshots'/GSM_REV/'main'
    frames = {s:pd.read_parquet(gsm_root/f'{s}-00000-of-00001.parquet') for s in ['train','test']}
    pilot = json.loads((ROOT.parent/'empirical/tasks.json').read_text(encoding='utf-8'))
    excluded = {normalize(t['question']) for t in pilot}
    used = set(excluded); tasks = []
    rng = random.Random(2026101401)
    assignments = [('development','train',8), ('architecture_train','train',64),
                   ('reliability_test','test',64), ('architecture_test','test',64)]
    for cohort, split, count in assignments:
        indices = list(range(len(frames[split]))); rng.shuffle(indices)
        chosen = 0
        for index in indices:
            row = frames[split].iloc[index]; key = normalize(row.question)
            if key in used:
                continue
            used.add(key)
            gold = row.answer.rsplit('####',1)[1].strip().replace(',','')
            tasks.append({'task_id':f'gsm8k-{split}-{index:04d}','dataset':'gsm8k',
                'source_split':split,'cohort':cohort,'row_index':index,
                'question':row.question,'gold':gold})
            chosen += 1
            if chosen == count:
                break
        assert chosen == count
    svamp = json.loads((ROOT/'assets/SVAMP.json').read_text(encoding='utf-8'))
    indices = list(range(len(svamp))); rng.shuffle(indices)
    bodies = set(); chosen = 0
    for index in indices:
        row = svamp[index]; question = row['Body'].strip()+' '+row['Question'].strip()
        # Avoid repeated numeric variants of the same body within the transfer sample.
        group = normalize(re.sub(r'\d+(?:\.\d+)?','NUM',row['Body']))
        key = normalize(question)
        if key in used or group in bodies:
            continue
        used.add(key); bodies.add(group)
        tasks.append({'task_id':'svamp-'+row['ID'],'dataset':'svamp','source_split':'challenge',
            'cohort':'architecture_transfer','row_index':index,'question':question,'gold':str(row['Answer'])})
        chosen += 1
        if chosen == 64:
            break
    assert chosen == 64
    (ROOT/'tasks.json').write_text(json.dumps(tasks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    provenance = {'selection_seed':2026101401,'gsm8k_revision':GSM_REV,'svamp_revision':SVAMP_REV,
        'svamp_url':f'https://github.com/arkilpatel/SVAMP/tree/{SVAMP_REV}',
        'sources':{}, 'cohorts':{c:sum(t['cohort']==c for t in tasks) for c in sorted(set(t['cohort'] for t in tasks))},
        'pilot_questions_excluded':len(excluded),'all_question_texts_unique':True,
        'svamp_selection':'one example per normalized numeric-masked body, then 64 sampled groups',
        'public_benchmark_contamination_possible':True}
    for p in [*gsm_root.glob('*.parquet'),ROOT/'assets/SVAMP.json',ROOT/'assets/SVAMP_LICENSE']:
        provenance['sources'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    (ROOT/'DATA_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    print(provenance['cohorts'])


if __name__ == '__main__':
    main()
