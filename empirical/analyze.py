"""Analyze all frozen episodes, retaining failures and clustering uncertainty by task."""
from pathlib import Path
import json, gzip, hashlib
import numpy as np
import pandas as pd
from measurement import score_answer
from selector_policy import select,descriptors,COEFFICIENTS

ROOT=Path(__file__).resolve().parent
ARCHS=list(COEFFICIENTS)

def mean_ci(task_values):
    values=np.asarray(task_values,dtype=float)
    rng=np.random.default_rng(20261013)
    draws=rng.choice(values,size=(2000,len(values)),replace=True).mean(axis=1)
    return float(values.mean()),float(np.quantile(draws,.025)),float(np.quantile(draws,.975))

def conditional_ci(frame,numerator,denominator):
    grouped=frame.groupby('task_id')[[numerator,denominator]].sum()
    arr=grouped.to_numpy(float); den=arr[:,1].sum()
    if not den: return None,None,None
    rng=np.random.default_rng(20261013); samples=arr[rng.integers(0,len(arr),size=(2000,len(arr)))].sum(axis=1)
    samples=samples[samples[:,1]>0]
    ratios=samples[:,0]/samples[:,1]
    return float(arr[:,0].sum()/den),float(np.quantile(ratios,.025)),float(np.quantile(ratios,.975))

def main():
    tasks={t['task_id']:t for t in json.loads((ROOT/'tasks.json').read_text()) if t['split']=='test'}
    records=[]; manifest=[]
    for p in sorted((ROOT/'runs').glob('model_*.jsonl')):
        raw=p.read_bytes(); manifest.append({'file':p.name,'sha256':hashlib.sha256(raw).hexdigest()})
        for line in raw.decode('utf-8').splitlines():
            r=json.loads(line)
            if r['infrastructure_error']: raise RuntimeError('Infrastructure failure requires explicit adjudication')
            assert r['correct']==score_answer(r['answer'],tasks[r['task_id']]['gold_answer'])
            events=r['trace']['tool_events']
            timeout_pos=next((i for i,e in enumerate(events) if e.get('fault')=='timeout'),None)
            r['tool_retried_successfully']=bool(timeout_pos is not None and any('output' in e for e in events[timeout_pos+1:]))
            r['correct_after_exposure']=bool(r['correct'] and r['fault_exposed'])
            r['adopted_after_exposure']=bool(r['sentinel_adopted'] and r['fault_exposed'])
            r['trace_calls_match']=len(r['trace']['model_calls'])==r['model_calls']
            r.pop('trace'); records.append(r)
        compressed=ROOT/'results'/('traces_'+p.stem+'.jsonl.gz')
        compressed.parent.mkdir(exist_ok=True)
        with compressed.open('wb') as out:
            with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as z: z.write(raw)
    df=pd.DataFrame(records)
    assert len(df)==720, f'Expected 720 episodes, got {len(df)}'
    assert not df.duplicated(['model','task_id','architecture','condition','seed']).any()
    models=[m['id'] for m in json.loads((ROOT/'ASSET_MANIFEST.json').read_text())['models']]
    expected={(m,t,a,c,s) for m in models for t in tasks for a in ARCHS
              for c in (['clean'] if a=='single_agent' else ['clean','timeout','injection']) for s in [17,43,91]}
    assert set(df[['model','task_id','architecture','condition','seed']].itertuples(index=False,name=None))==expected
    assert df.output_tokens.max()<=512
    assert df.trace_calls_match.all()
    out=ROOT/'results'; out.mkdir(exist_ok=True)
    df.to_csv(out/'episodes.csv',index=False)
    summaries=[]
    for (model,arch,condition),part in df.groupby(['model','architecture','condition']):
        by_task=part.groupby('task_id').correct.mean()
        assert len(by_task)==12 and len(part)==36
        acc,lo,hi=mean_ci(by_task)
        post,post_lo,post_hi=conditional_ci(part,'correct_after_exposure','fault_exposed')
        adoption,_,_=conditional_ci(part,'adopted_after_exposure','fault_exposed')
        summaries.append({'model':model,'architecture':arch,'condition':condition,'episodes':len(part),
            'correct':int(part.correct.sum()),'accuracy':acc,'accuracy_ci_low':lo,'accuracy_ci_high':hi,
            'mean_unanimity':float(np.abs(2*by_task-1).mean()),'exposed':int(part.fault_exposed.sum()),
            'correct_after_exposure':int(part.correct_after_exposure.sum()),'post_exposure_success':post,
            'post_exposure_ci_low':post_lo,'post_exposure_ci_high':post_hi,
            'successful_tool_retries':int(part.tool_retried_successfully.sum()),
            'injection_sentinel_adoptions':int(part.adopted_after_exposure.sum()) if condition=='injection' else None,
            'injection_adoption_rate':adoption if condition=='injection' else None,
            'median_output_tokens':float(part.output_tokens.median()),'median_input_tokens':float(part.input_tokens.median()),
            'median_elapsed_seconds':float(part.elapsed_seconds.median()),'errors':int(part.error.notna().sum())})
    summary=pd.DataFrame(summaries); summary.to_csv(out/'condition_summary.csv',index=False)
    comparisons=[]
    for (model,arch),part in df.groupby(['model','architecture']):
        baseline=part[part.condition=='clean'].groupby('task_id').correct.mean()
        for condition in ['timeout','injection']:
            perturbed=part[part.condition==condition].groupby('task_id').correct.mean()
            if perturbed.empty: continue
            mean,lo,hi=mean_ci(perturbed-baseline)
            comparisons.append({'model':model,'architecture':arch,'condition':condition,
                'paired_accuracy_change':mean,'ci_low':lo,'ci_high':hi})
    pd.DataFrame(comparisons).to_csv(out/'paired_fault_effects.csv',index=False)
    features=[{'task_id':k,**descriptors(t['question']),'selected':select(t['question'])[0]} for k,t in tasks.items()]
    pd.DataFrame(features).to_csv(out/'frozen_selector_decisions.csv',index=False)
    policies=[]
    for model,part in df[df.condition=='clean'].groupby('model'):
        measured=part.assign(measured_utility=part.correct.astype(float)-.05*part.output_tokens/512)
        values=measured.groupby(['task_id','architecture']).measured_utility.mean().unstack().reindex(columns=ARCHS)
        oracle=values.max(axis=1)
        for policy in ARCHS+['frozen_proxy_selector']:
            vals=np.array([values.loc[tid,select(tasks[tid]['question'])[0] if policy=='frozen_proxy_selector' else policy] for tid in values.index])
            mean,lo,hi=mean_ci(vals); regret,rl,rh=mean_ci(oracle.to_numpy()-vals)
            policies.append({'model':model,'policy':policy,'mean_utility':mean,'ci_low':lo,'ci_high':hi,
                'mean_observed_regret':regret,'regret_ci_low':rl,'regret_ci_high':rh,
                'fraction_matching_observed_best':float(np.isclose(vals,oracle.to_numpy(),atol=1e-12).mean())})
    pd.DataFrame(policies).to_csv(out/'selector_policy_evaluation.csv',index=False)
    (out/'TRACE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(summary[['model','architecture','condition','correct','episodes','exposed']].to_string(index=False))
    print('All 720 unique episodes accounted for; cluster bootstrap and fixed-policy analysis saved.')

if __name__=='__main__': main()
