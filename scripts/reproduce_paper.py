"""Reproduce synthetic/analytical paper artifacts; no LLM calls are made."""
from pathlib import Path
import sys, json, hashlib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from fdar import evaluate_runs
from fdar.metrics import composite_score, DIMENSION_KEYS

def main():
    for sub in ['results', 'paper/tables', 'paper/figures']:
        (ROOT/sub).mkdir(parents=True, exist_ok=True)
    source = ROOT/'data/synthetic_reference_runs.jsonl'
    rows = [json.loads(x) for x in source.read_text().splitlines()]
    assert len(rows) == 720 and all(r['synthetic'] is True for r in rows)
    scored = evaluate_runs(pd.DataFrame(rows))
    assert set(scored.observed_dimension_count) == {4, 5}
    scored.to_csv(ROOT/'results/scored_synthetic_records.csv', index=False)
    complete = scored.loc[scored.observed_dimension_count == 5]
    cols = DIMENSION_KEYS + ['reliability_score']
    means = complete.groupby('architecture')[cols].mean()
    counts = scored.groupby(['architecture','observed_dimension_count']).size()
    means.to_csv(ROOT/'results/synthetic_complete_case_summary.csv')
    counts.to_csv(ROOT/'results/observation_counts.csv', header=['records'])
    names = {'direct_agent':'Direct profile', 'planner_executor':'Planner--executor profile',
             'guarded_recovery_agent':'Guarded-recovery profile'}
    table = [r'\begin{tabular}{lrrrrrr}', r'\toprule',
             r'Reference profile & $F$ & $R$ & $S$ & $C$ & $E$ & $Q$ \\', r'\midrule']
    for key in names:
        table.append(names[key]+' & '+' & '.join(f'{means.loc[key,c]:.3f}' for c in cols)+r' \\')
    table += [r'\bottomrule',r'\end{tabular}']
    (ROOT/'paper/tables/summary.tex').write_text('\n'.join(table)+'\n')
    xs=[i/100 for i in range(101)]
    ys=[composite_score(dict(dict.fromkeys(DIMENSION_KEYS,.8),recovery=x)) for x in xs]
    pd.DataFrame({'observed_recovery':xs,'five_dimension_score':ys,'missing_recovery_score':.8}).to_csv(ROOT/'results/analytical_sensitivity.csv',index=False)
    fig,ax=plt.subplots(figsize=(6.2,3.1),layout='constrained')
    ax.plot(xs,ys,color='#195c84',lw=2,label='Recovery observed (5 dimensions)')
    ax.axhline(.8,color='#b15e20',ls='--',label='Recovery unobserved (4 dimensions)')
    ax.set(xlabel='Observed recovery score',ylabel='Composite score',xlim=(0,1),ylim=(0,1))
    ax.legend(frameon=False,fontsize=9,loc='lower right'); ax.grid(alpha=.2)
    fig.savefig(ROOT/'paper/figures/sensitivity.pdf',metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)
    (ROOT/'results/input_hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data').glob('*.jsonl'))},indent=2)+'\n')
    print(means.to_string()); print(counts.to_string())

if __name__ == '__main__': main()
