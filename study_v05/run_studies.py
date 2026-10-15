"""Resumable local experiments. Evaluation is prohibited until code is frozen."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import gc
import hashlib
import json
import random
import time
import torch
from local_model import LocalModel
from measurement import correct, parse_answer
from workflows import (ARCHITECTURES, CONDITIONS, SENTINEL, architecture_episode,
                       reliability_prefix, reliability_branch)

ROOT = Path(__file__).resolve().parent
SEEDS = [137, 271]


def now():
    return datetime.now(timezone.utc).isoformat()


def verify_freeze():
    freeze = json.loads((ROOT/'FREEZE.json').read_text(encoding='utf-8'))
    for name,digest in freeze['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Frozen input changed: '+name)
    return freeze


def append(path, record):
    with path.open('a',encoding='utf-8') as stream:
        stream.write(json.dumps(record,ensure_ascii=False,allow_nan=False)+'\n')
        stream.flush()


def load_records(path):
    if not path.exists():
        return []
    records = []
    for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        try: records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f'Incomplete record at {path}:{number}; preserve and adjudicate before resuming') from exc
    return records


def make_record(task, model, workflow, condition, seed, budget, output, traces, extra=None):
    parsed = parse_answer(output)
    record = {'task_id':task['task_id'],'cohort':task['cohort'],'dataset':task['dataset'],
        'model':model.model_id,'workflow':workflow,'condition':condition,'seed':seed,
        'budget':budget,'timestamp_utc':now(),'answer':output,
        'parsed_answer':str(parsed) if parsed is not None else None,'correct':correct(output,task['gold']),
        'output_tokens':sum(t['output_tokens'] for t in traces),
        'input_tokens':sum(t['input_tokens'] for t in traces),
        'generation_seconds':sum(t['seconds'] for t in traces),'trace':traces}
    if record['output_tokens'] > budget:
        raise RuntimeError('Token budget exceeded')
    if extra:
        record.update(extra)
    return record


def key(record):
    return tuple(record[x] for x in ['task_id','workflow','condition','seed','budget'])


def jobs(tasks, smoke):
    planned = []
    for task in tasks:
        for seed in ([137] if smoke else SEEDS):
            if task['cohort'] in ['development','reliability_test']:
                planned.append((task,'reliability',seed,512))
            if task['cohort'] != 'reliability_test':
                for workflow in ARCHITECTURES:
                    planned.append((task,workflow,seed,512))
                    if task['cohort'] == 'architecture_test':
                        planned.append((task,workflow,seed,1024))
    random.Random(2026101402).shuffle(planned)
    return planned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--model',type=int,choices=[0,1])
    parser.add_argument('--study',choices=['both','reliability','architecture'],default='both')
    args = parser.parse_args()
    if args.smoke == args.run:
        parser.error('Choose --smoke or --run')
    if args.run:
        verify_freeze()
    tasks = json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))
    tasks = [t for t in tasks if (t['cohort']=='development') == args.smoke]
    assets = json.loads((ROOT/'local_assets.json').read_text(encoding='utf-8'))
    public = json.loads((ROOT/'MODEL_MANIFEST.json').read_text(encoding='utf-8'))
    if [(m['id'],m['revision']) for m in assets['models']] != [(m['id'],m['revision']) for m in public['models']]:
        raise RuntimeError('Local model identities differ from public manifest')
    directory = ROOT/('development' if args.smoke else 'runs'); directory.mkdir(exist_ok=True)
    lock = directory/'RUNNING.lock'
    try:
        handle = lock.open('x',encoding='utf-8')
    except FileExistsError:
        raise RuntimeError('Study lock exists; check process before resuming')
    import os
    handle.write(json.dumps({'pid':os.getpid(),'start_utc':now()}));handle.close()
    try:
        torch.set_num_threads(4)
        for mi,asset in enumerate(assets['models']):
            if args.model is not None and mi != args.model:
                continue
            path = directory/f'model_{mi}.jsonl'; prefix_path = directory/f'prefixes_{mi}.jsonl'
            existing = load_records(path); done = {key(r) for r in existing}
            if any(r['model']!=asset['id'] for r in existing):
                raise RuntimeError('Existing records belong to another model; preserve separately')
            if len(done) != len(existing):
                raise RuntimeError('Duplicate episode keys')
            prefixes = {(r['task_id'],r['seed']):r['prefix'] for r in load_records(prefix_path)}
            planned = [j for j in jobs(tasks,args.smoke) if args.study=='both' or (j[1]=='reliability')==(args.study=='reliability')]
            valid_keys={(t['task_id'],w,c,s,b) for t,w,s,b in planned for c in (CONDITIONS if w=='reliability' else ['clean'])}
            done=done & valid_keys
            expected = sum(3 if j[1]=='reliability' else 1 for j in planned)
            if len(done) == expected:
                continue
            if args.run:
                for name,digest in public['models'][mi]['files'].items():
                    h=hashlib.sha256()
                    with (Path(asset['local_path'])/name).open('rb') as f:
                        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
                    if h.hexdigest()!=digest:
                        raise RuntimeError('Checkpoint file changed: '+name)
            print('Loading',asset['id'],flush=True); model = LocalModel(asset)
            model.call([{'role':'user','content':'Say hello briefly.'}],16,0,'warmup')
            for task,workflow,seed,budget in planned:
                conditions = CONDITIONS if workflow=='reliability' else ['clean']
                if all((task['task_id'],workflow,c,seed,budget) in done for c in conditions):
                    continue
                prefix = None
                if workflow == 'reliability':
                    pk = (task['task_id'],seed)
                    if pk not in prefixes:
                        prefix = reliability_prefix(model,task['question'],seed)
                        append(prefix_path,{'task_id':task['task_id'],'model':model.model_id,'seed':seed,
                                            'timestamp_utc':now(),'prefix':prefix})
                        prefixes[pk] = prefix
                    prefix = prefixes[pk]
                for condition in conditions:
                    episode_key = (task['task_id'],workflow,condition,seed,budget)
                    if episode_key in done:
                        continue
                    if workflow == 'reliability':
                        output,traces,events,termination = reliability_branch(model,prefix,condition,seed)
                        extra = {'fault_exposed':bool(prefix['valid_request'] and condition!='clean'),
                            'branch_eligible':prefix['valid_request'],'termination':termination,
                            'tool_events':events,'sentinel_adopted':parse_answer(output)==parse_answer(SENTINEL),
                            'prefix_shared_across_conditions':True}
                    else:
                        output,traces = architecture_episode(model,task['question'],workflow,budget,seed)
                        extra = {'termination':'completed','fault_exposed':False}
                    record = make_record(task,model,workflow,condition,seed,budget,output,traces,extra)
                    append(path,record);done.add(episode_key)
                    progress = {'model':model.model_id,'model_index':mi,'completed_in_model':len(done),
                        'planned_in_model':expected,'latest_timestamp':now(),'latest_task':task['task_id'],
                        'latest_cohort':task['cohort'],'status':'running'}
                    (directory/'progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8')
                    print(f"{mi} {len(done)}/{expected} {task['cohort']} {workflow} {condition} correct={record['correct']}",flush=True)
            del model; gc.collect(); torch.cuda.empty_cache()
        per_model_expected=len(valid_keys)
        all_complete=all(len({key(r) for r in load_records(directory/f'model_{i}.jsonl')} & valid_keys)==per_model_expected for i in range(len(assets['models'])))
        if all_complete:
            marker='COMPLETE.json' if args.study=='both' else f'COMPLETE_{args.study}.json'
            (directory/marker).write_text(json.dumps({'finished_utc':now(),'study':args.study,'mode':'development' if args.smoke else 'evaluation'}),encoding='utf-8')
    except BaseException as exc:
        append(directory/'INFRASTRUCTURE_ERRORS.jsonl',{'timestamp_utc':now(),'type':type(exc).__name__,'message':str(exc)})
        raise
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
