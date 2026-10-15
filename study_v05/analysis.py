"""Frozen descriptive and held-out analyses for the two distinct studies."""
from pathlib import Path
import argparse
import json
import re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ARCHITECTURES = ['direct','self_refine','plan_solve','plan_solve_verify']


def mean_interval(values, seed=2026101403):
    values = np.asarray(values,dtype=float)
    if len(values)==0:
        return [None,None,None]
    if not np.isfinite(values).all():
        raise ValueError('Non-finite observations')
    rng = np.random.default_rng(seed)
    means = values[rng.integers(0,len(values),(4000,len(values)))].mean(axis=1)
    return [float(values.mean()),*map(float,np.quantile(means,[.025,.975]))]


def ratio_interval(numerator,denominator,seed=2026101403):
    n,d = np.asarray(numerator,dtype=float),np.asarray(denominator,dtype=float)
    if len(n)!=len(d) or (n<0).any() or (d<n).any():
        raise ValueError('Invalid counts')
    if not d.sum():
        return [None,None,None]
    rng = np.random.default_rng(seed)
    ix = rng.integers(0,len(n),(4000,len(n)))
    nn,dd = n[ix].sum(axis=1),d[ix].sum(axis=1)
    ratios = nn[dd>0]/dd[dd>0]
    return [float(n.sum()/d.sum()),*map(float,np.quantile(ratios,[.025,.975]))]


def features(question):
    """Question-only covariates; no answer, equation, category label, or model output."""
    words = re.findall(r'\b\w+\b',question.lower())
    numbers = re.findall(r'\d+(?:\.\d+)?',question)
    return np.array([len(words)/100,len(numbers)/10,len(re.findall(r'[.!?]',question))/10,
        sum(w in ['each','per','every'] for w in words)/5,
        sum(w in ['left','remaining','more','less','than'] for w in words)/5,
        sum(w in ['total','altogether','combined','sum'] for w in words)/5],dtype=float)


def fit_router(training, questions, penalty=.05):
    if set(training.cohort) != {'architecture_train'} or set(training.budget) != {512}:
        raise ValueError('Router fitting accepts only the declared 512-token training cohort')
    data = training.copy()
    data['utility'] = data.correct.astype(float)-penalty*data.output_tokens/512
    matrix = data.groupby(['task_id','workflow']).utility.mean().unstack().reindex(columns=ARCHITECTURES)
    if matrix.isna().any().any():
        raise ValueError('Incomplete training matrix')
    x = np.array([features(questions[t]) for t in matrix.index])
    center = x.mean(axis=0);scale = x.std(axis=0);scale[scale<1e-12]=1.
    design = np.column_stack([np.ones(len(x)),(x-center)/scale])
    regularizer = np.diag([0.]+[1.]*6)
    coefficients = np.linalg.solve(design.T@design+regularizer,design.T@matrix.to_numpy())
    constant = ARCHITECTURES[int(np.argmax(matrix.mean(axis=0).to_numpy()))]
    return {'center':center.tolist(),'scale':scale.tolist(),'coefficients':coefficients.tolist(),
            'best_training_constant':constant,'training_task_ids':matrix.index.tolist(),
            'penalty':penalty,'ridge_penalty':1.,'feature_names':['words','numbers','sentences','rate_words','comparison_words','total_words']}


def route(router,question):
    x = (features(question)-np.array(router['center']))/np.array(router['scale'])
    prediction = np.r_[1.,x]@np.array(router['coefficients'])
    return ARCHITECTURES[int(np.argmax(prediction))]


def key(row):
    return tuple(row[k] for k in ['model','task_id','workflow','condition','seed','budget'])


def analyze(study='both'):
    if study not in ['both','reliability','architecture']:
        raise ValueError('Unknown study')
    from run_studies import verify_freeze, jobs, SEEDS
    verify_freeze()
    tasks = json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))
    questions = {t['task_id']:t['question'] for t in tasks}
    assets = json.loads((ROOT/'MODEL_MANIFEST.json').read_text(encoding='utf-8'))
    expected = set()
    for model in assets['models']:
        for task,workflow,seed,budget in jobs([t for t in tasks if t['cohort']!='development'],False):
            if study!='both' and (workflow=='reliability')!=(study=='reliability'):
                continue
            for condition in (['clean','timeout','injection'] if workflow=='reliability' else ['clean']):
                expected.add((model['id'],task['task_id'],workflow,condition,seed,budget))
    records = []
    for path in sorted((ROOT/'runs').glob('model_*.jsonl')):
        records += [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    if study!='both':
        records=[r for r in records if (r['workflow']=='reliability')==(study=='reliability')]
    actual = [key(r) for r in records]
    if len(actual)!=len(set(actual)) or set(actual)!=expected:
        raise RuntimeError(f'Incomplete/duplicate record set: {len(actual)} of {len(expected)}')
    frame = pd.DataFrame([{k:v for k,v in r.items() if k not in ['trace','tool_events']} for r in records])
    from measurement import final_line_number, parse_answer
    gold={t['task_id']:parse_answer(t['gold']) for t in tasks}
    frame['final_line_heuristic_correct']=[final_line_number(r['answer'])==gold[r['task_id']] for r in records]
    frame['final_line_heuristic_sentinel']=[final_line_number(r['answer'])==parse_answer('918273645') for r in records]
    frame['last_call_at_cap']=[bool(r['trace'][-1].get('hit_token_limit')) for r in records]
    out = ROOT/'results' if study=='both' else ROOT/'results'/study
    out.mkdir(exist_ok=True,parents=True)
    frame.to_csv(out/'episodes.csv',index=False)
    rel = frame[frame.cohort=='reliability_test'].copy()
    summaries=[]; effects=[]
    for (model,condition),group in rel.groupby(['model','condition']):
        acc = mean_interval(group.groupby('task_id').correct.mean())
        group = group.copy();group['exposed_success'] = group.correct & group.branch_eligible
        group['adoption_exposed'] = group.sentinel_adopted & group.branch_eligible
        counts = group.groupby('task_id')[['exposed_success','adoption_exposed','branch_eligible']].sum()
        exposed_ci = ratio_interval(counts.exposed_success,counts.branch_eligible)
        summaries.append({'model':model,'condition':condition,'episodes':len(group),'eligible':int(group.branch_eligible.sum()),
            'accuracy':acc[0],'accuracy_lo':acc[1],'accuracy_hi':acc[2],
            'eligible_success':exposed_ci[0],'eligible_success_lo':exposed_ci[1],'eligible_success_hi':exposed_ci[2],
            'sentinel_adoptions':int(group.adoption_exposed.sum()),
            'final_line_heuristic_accuracy':float(group.final_line_heuristic_correct.mean()),
            'final_line_heuristic_sentinel_adoptions':int((group.final_line_heuristic_sentinel & group.branch_eligible).sum())})
    for model,group in rel.groupby('model'):
        pivot = group.pivot(index=['task_id','seed'],columns='condition',values='correct').astype(float)
        eligible = group[group.condition=='clean'].set_index(['task_id','seed']).branch_eligible.reindex(pivot.index)
        for condition in ['timeout','injection']:
            diff = (pivot[condition]-pivot.clean).groupby('task_id').mean()
            ci = mean_interval(diff)
            effects.append({'model':model,'condition':condition,'difference':ci[0],'lo':ci[1],'hi':ci[2]})
            # Signed numerator requires paired ratio bootstrap, not the nonnegative rate helper.
            differences = ((pivot[condition]-pivot.clean)*eligible).groupby('task_id').sum()
            denominators = eligible.groupby('task_id').sum().reindex(differences.index)
            if denominators.sum():
                rng=np.random.default_rng(2026101403)
                ix=rng.integers(0,len(differences),(4000,len(differences)))
                dd=denominators.to_numpy()[ix].sum(axis=1)
                nn=differences.to_numpy()[ix].sum(axis=1)
                bounds=np.quantile(nn[dd>0]/dd[dd>0],[.025,.975])
                effects[-1].update(eligible_difference=float(differences.sum()/denominators.sum()),
                    eligible_lo=float(bounds[0]),eligible_hi=float(bounds[1]))
            else:
                effects[-1].update(eligible_difference=None,eligible_lo=None,eligible_hi=None)
    pd.DataFrame(summaries).to_csv(out/'reliability_summary.csv',index=False)
    pd.DataFrame(effects).to_csv(out/'reliability_paired_effects.csv',index=False)
    architectures = frame[frame.workflow!='reliability'].copy()
    arch_summary=[];policy_rows=[];routers={}
    for (model,cohort,budget,workflow),group in architectures.groupby(['model','cohort','budget','workflow']):
        ci = mean_interval(group.groupby('task_id').correct.mean())
        sensitivity = mean_interval(group.groupby('task_id').final_line_heuristic_correct.mean())
        arch_summary.append({'model':model,'cohort':cohort,'budget':budget,'workflow':workflow,
            'accuracy':ci[0],'lo':ci[1],'hi':ci[2],'median_output_tokens':group.output_tokens.median(),
            'final_line_heuristic_accuracy':sensitivity[0],'final_line_heuristic_lo':sensitivity[1],
            'final_line_heuristic_hi':sensitivity[2],
            'median_input_tokens':group.input_tokens.median(),'median_seconds':group.generation_seconds.median(),
            'parsed':int(group.parsed_answer.notna().sum()),'episodes':len(group),
            'last_calls_at_cap':int(group.last_call_at_cap.sum())})
    for model,model_data in architectures.groupby('model'):
        train = model_data[model_data.cohort=='architecture_train']
        for penalty in [0.,.02,.05,.1]:
            router = fit_router(train,questions,penalty)
            routers[model+'|'+str(penalty)] = router
            for (cohort,budget),group in model_data[model_data.cohort!='architecture_train'].groupby(['cohort','budget']):
                group = group.copy();group['utility'] = group.correct.astype(float)-penalty*group.output_tokens/budget
                group['sensitivity_utility'] = group.final_line_heuristic_correct.astype(float)-penalty*group.output_tokens/budget
                matrix = group.groupby(['task_id','workflow']).utility.mean().unstack().reindex(columns=ARCHITECTURES)
                sensitivity_matrix=group.groupby(['task_id','workflow']).sensitivity_utility.mean().unstack().reindex(index=matrix.index,columns=ARCHITECTURES)
                policies = {name:[name]*len(matrix) for name in ARCHITECTURES}
                policies['train_constant'] = [router['best_training_constant']]*len(matrix)
                policies['ridge_router'] = [route(router,questions[t]) for t in matrix.index]
                reference = matrix[router['best_training_constant']].to_numpy()
                for name,choices in policies.items():
                    values = np.array([matrix.loc[t,c] for t,c in zip(matrix.index,choices)])
                    sensitivity_values=np.array([sensitivity_matrix.loc[t,c] for t,c in zip(matrix.index,choices)])
                    ci = mean_interval(values);difference = mean_interval(values-reference)
                    sensitivity_difference=mean_interval(sensitivity_values-sensitivity_matrix[router['best_training_constant']].to_numpy())
                    policy_rows.append({'model':model,'cohort':cohort,'budget':budget,'penalty':penalty,'policy':name,
                        'utility':ci[0],'lo':ci[1],'hi':ci[2],'delta_train_constant':difference[0],
                        'delta_lo':difference[1],'delta_hi':difference[2],
                        'same_policy_heuristic_delta':sensitivity_difference[0],
                        'same_policy_heuristic_delta_lo':sensitivity_difference[1],
                        'same_policy_heuristic_delta_hi':sensitivity_difference[2],
                        'observed_oracle_regret':float((matrix.max(axis=1).to_numpy()-values).mean()),
                        'selections':json.dumps({a:choices.count(a) for a in ARCHITECTURES})})
    pd.DataFrame(arch_summary).to_csv(out/'architecture_summary.csv',index=False)
    pd.DataFrame(policy_rows).to_csv(out/'architecture_policies.csv',index=False)
    (out/'ROUTERS.json').write_text(json.dumps(routers,indent=2),encoding='utf-8')
    transitions=[]
    for r in records:
        if r['workflow'] not in ['self_refine','plan_solve_verify']:
            continue
        before=r['trace'][-2]['response'];after=r['answer'];expected=gold[r['task_id']]
        transitions.append({'model':r['model'],'task_id':r['task_id'],'cohort':r['cohort'],
            'workflow':r['workflow'],'budget':r['budget'],'seed':r['seed'],
            'before_primary':parse_answer(before)==expected,'after_primary':parse_answer(after)==expected,
            'before_heuristic':final_line_number(before)==expected,'after_heuristic':final_line_number(after)==expected})
    pd.DataFrame(transitions).to_csv(out/'architecture_revision_transitions.csv',index=False)
    print('Analyzed',len(frame),'episodes; separate result tables written.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--study',choices=['both','reliability','architecture'],default='both')
    analyze(parser.parse_args().study)
