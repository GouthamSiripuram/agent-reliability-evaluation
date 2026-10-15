"""Independent post-run consistency checks; does not alter experiment outputs."""
from pathlib import Path
import hashlib
import json
from measurement import correct, parse_answer
from arithmetic import calculate

ROOT=Path(__file__).resolve().parent


def audit(directory='runs'):
    tasks={t['task_id']:t for t in json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))}
    paths=sorted((ROOT/directory).glob('model_*.jsonl'))
    records=[json.loads(line) for p in paths for line in p.read_text(encoding='utf-8').splitlines()]
    keys=set();unique_calls={};prefixes={};later_success={}
    for r in records:
        key=tuple(r[k] for k in ['model','task_id','workflow','condition','seed','budget'])
        assert key not in keys;keys.add(key)
        task=tasks[r['task_id']]
        assert r['cohort']==task['cohort']
        assert r['correct']==correct(r['answer'],task['gold'])
        parsed=parse_answer(r['answer'])
        assert r['parsed_answer']==(str(parsed) if parsed is not None else None)
        assert r['output_tokens']==sum(t['output_tokens'] for t in r['trace'])<=r['budget']
        assert r['input_tokens']==sum(t['input_tokens'] for t in r['trace'])
        for index,t in enumerate(r['trace']):
            assert 0<t['output_tokens']<=t['limit']
            # Reference answer values can legitimately occur in a question/calculation;
            # verify prompt construction from question-only inputs in tests, not by
            # declaring every occurrence of a small numeric gold value a leakage.
            call_key=key+(index,)
            if r['workflow']=='reliability' and index==0:
                call_key=(r['model'],r['task_id'],r['seed'],'shared_prefix')
            if call_key in unique_calls:
                assert unique_calls[call_key]==t
            unique_calls[call_key]=t
        if r['workflow']=='reliability':
            pk=(r['model'],r['task_id'],r['seed'])
            prior=prefixes.setdefault(pk,r['trace'][0])
            assert prior==r['trace'][0]
            assert r['fault_exposed']==(r['branch_eligible'] and r['condition']!='clean')
            if not r['branch_eligible']:
                assert len(r['trace'])==1 and not r['tool_events']
            successes=0
            for event in r['tool_events']:
                if not event.get('first_request') and event.get('error') is None:
                    assert event['output']=='Calculator result: '+str(calculate(event['expression']))
                    successes+=1
            later_success[str(key)]=successes
    summary={'records':len(records),'unique_keys':len(keys),'actual_completed_model_calls':len(unique_calls),
        'physical_generated_tokens':sum(t['output_tokens'] for t in unique_calls.values()),
        'shared_prefixes':len(prefixes),'development_only':directory!='runs',
        'source_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'checks':'key uniqueness, rescore, token accounting, identical branch prefixes, exposure, calculator outputs',
        'later_successful_calculator_calls_by_episode':later_success}
    target=ROOT/directory/'INTEGRITY_AUDIT.json'
    target.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print({k:v for k,v in summary.items() if k not in ['later_successful_calculator_calls_by_episode','source_files']})
    return summary


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--directory',default='runs')
    audit(parser.parse_args().directory)
