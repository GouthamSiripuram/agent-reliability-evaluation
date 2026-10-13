"""Post-run integrity audit; does not alter the frozen primary analysis."""
from pathlib import Path
from datetime import datetime
import sys,json,hashlib,re,collections

ROOT=Path(__file__).resolve().parents[1]
EMP=ROOT/'empirical'
sys.path.insert(0,str(EMP))
from measurement import calculate,parse_answer,score_answer

def main():
    freeze=json.loads((EMP/'FREEZE.json').read_text())
    for name,digest in freeze['files'].items():
        assert hashlib.sha256((EMP/name).read_bytes()).hexdigest()==digest,name
    frozen=datetime.fromisoformat(freeze['frozen_at_utc'])
    checkpoints_match=None
    if (EMP/'local_assets.json').exists():
        local=json.loads((EMP/'local_assets.json').read_text())
        public=json.loads((EMP/'ASSET_MANIFEST.json').read_text())
        for local_model,expected_model in zip(local['models'],public['models']):
            assert local_model['id']==expected_model['id']
            for name,digest in expected_model['weight_sha256'].items():
                h=hashlib.sha256()
                with (Path(local_model['local_path'])/name).open('rb') as f:
                    for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
                assert h.hexdigest()==digest, 'Checkpoint weight file changed'
        checkpoints_match=True
    records=[]
    for path in sorted((EMP/'runs').glob('model_*.jsonl')):
        records.extend(json.loads(line) for line in path.read_text(encoding='utf-8').splitlines())
    assert len(records)==720
    flagged=[]; calls=0; tool_events=0
    tasks={t['task_id']:t for t in json.loads((EMP/'tasks.json').read_text(encoding='utf-8'))}
    for r in records:
        assert datetime.fromisoformat(r['timestamp_utc'])>frozen
        assert r['split']=='test' and not r['infrastructure_error']
        assert r['correct']==score_answer(r['answer'],tasks[r['task_id']]['gold_answer'])
        trace=r['trace']['model_calls']; calls+=len(trace)
        assert sum(c['output_tokens'] for c in trace)==r['output_tokens']<=512
        assert sum(c['input_tokens'] for c in trace)==r['input_tokens']
        assert r['elapsed_seconds']+.001>=sum(c['generation_seconds'] for c in trace)
        assert all(c['input_tokens']<=4096 and c['output_tokens']<=c['token_limit'] for c in trace)
        assert tasks[r['task_id']]['gold_answer'] not in trace[0]['rendered_prompt'], 'Full reference solution in first prompt'
        events=r['trace']['tool_events']; tool_events+=len(events)
        faults=[e for e in events if e.get('fault')]
        assert len(faults)==int(r['fault_exposed'])
        if faults: assert faults[0]['fault']==r['condition']
        for e in events:
            if 'output' in e:
                assert e['output'].split('\n')[0]==str(calculate(e['expression']))
        answer=r['answer'] or ''
        for match in re.finditer(r'####\s*(?:NUMBER\s*[:=]?\s*)?([-+]?\$?[\d,]+(?:\.\d+)?)',answer,re.I):
            if re.match(r'\s*(?:[/+*=]|-\s*\d|[eE][+-]?\d)',answer[match.end():]):
                flagged.append({'task_id':r['task_id'],'model':r['model'],'architecture':r['architecture'],
                    'condition':r['condition'],'seed':r['seed'],'answer':answer,'primary_correct':r['correct']})
                break
    result={'episodes':len(records),'model_calls':calls,'calculator_attempts':tool_events,
        'frozen_files_unchanged':True,'complete_reference_solution_absent_from_first_prompts':True,
        'local_checkpoint_weights_match_manifest':checkpoints_match,
        'token_totals_and_bounds_verified':True,'tool_outputs_recomputed':True,
        'infrastructure_errors':sum(bool(r['infrastructure_error']) for r in records),
        'run_errors':sum(bool(r['error']) for r in records),
        'counts_by_model':dict(collections.Counter(r['model'] for r in records)),
        'counts_by_condition':dict(collections.Counter(r['condition'] for r in records)),
        'ambiguous_marked_answers':flagged,
        'note':'Post-run integrity checks; no observations or frozen primary analyses modified.'}
    (EMP/'results/INTEGRITY_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
