"""Render completed, integrity-checked observations; never generate outcomes."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'empirical/results'
ARCHS=['single_agent','single_agent_tools','planner_executor_verifier','hierarchical_multi_agent']
LABELS=dict(zip(ARCHS,['SA','SAT','PEV','HMA']))
MODELS=['Qwen/Qwen3-0.6B','HuggingFaceTB/SmolLM2-360M-Instruct']
NAMES=dict(zip(MODELS,['Qwen','SmolLM2']))

def write_table(path,header,rows,cols):
    path.write_text('\\begin{tabular}{'+cols+'}\n\\toprule\n'+header+r' \\'+'\n\\midrule\n'+
                    '\n'.join(' & '.join(row)+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n')

def main():
    episodes=pd.read_csv(RESULTS/'episodes.csv')
    assert len(episodes)==720
    summary=pd.read_csv(RESULTS/'condition_summary.csv')
    policy=pd.read_csv(RESULTS/'selector_policy_evaluation.csv')
    for folder in ['.']:
        paper=ROOT/'paper'
        tables=paper/'tables'
        rows=[]
        for m in MODELS:
            for a in ARCHS:
                r=summary[(summary.model==m)&(summary.architecture==a)&(summary.condition=='clean')].iloc[0]
                parsed=episodes[(episodes.model==m)&(episodes.architecture==a)&(episodes.condition=='clean')].parsed_answer.notna().sum()
                rows.append([NAMES[m],LABELS[a],str(parsed),f'{int(r.correct)}/36',
                    f'[{r.accuracy_ci_low:.2f}, {r.accuracy_ci_high:.2f}]',
                    f'{r.median_output_tokens:.0f}',f'{r.median_elapsed_seconds:.1f}'])
        write_table(tables/'empirical_clean.tex',r'Model & Arch. & Parsed & Correct & 95\% CI & Tokens & Seconds',rows,'llrrrrr')
        rows=[]
        for condition in ['timeout','injection']:
            for m in MODELS:
                for a in ARCHS[1:]:
                    r=summary[(summary.model==m)&(summary.architecture==a)&(summary.condition==condition)].iloc[0]
                    exposure=int(r.exposed)
                    post=f'{int(r.correct_after_exposure)}/{exposure}' if exposure else '--'
                    extra=str(int(r.successful_tool_retries)) if condition=='timeout' else (str(int(r.injection_sentinel_adoptions)) if exposure else '--')
                    rows.append([condition.title(),NAMES[m],LABELS[a],f'{int(r.correct)}/36',str(exposure),post,extra])
        write_table(tables/'empirical_faults.tex',r'Condition & Model & Arch. & Correct & Exposed & Post-success & Later/adopt',rows,'lllrrrr')
        rows=[]
        for m in MODELS:
            for a in ARCHS+['frozen_proxy_selector']:
                r=policy[(policy.model==m)&(policy.policy==a)].iloc[0]
                rows.append([NAMES[m],LABELS.get(a,'Fixed selector'),f'{r.mean_utility:.3f}',
                    f'[{r.ci_low:.3f}, {r.ci_high:.3f}]',f'{r.mean_observed_regret:.3f}'])
        write_table(tables/'empirical_policy.tex',r'Model & Policy & Utility & 95\% CI & Regret',rows,'llrrr')
        fig,ax=plt.subplots(figsize=(6.7,3.1),layout='constrained')
        for i,m in enumerate(MODELS):
            s=summary[(summary.model==m)&(summary.condition=='clean')].set_index('architecture').loc[ARCHS]
            y=np.arange(4)+(i-.5)*.16
            ax.errorbar(s.accuracy,y,xerr=np.vstack([s.accuracy-s.accuracy_ci_low,s.accuracy_ci_high-s.accuracy]),
                        fmt='o',capsize=3,label=NAMES[m],color=['#165B8E','#B35728'][i])
        ax.set(yticks=np.arange(4),yticklabels=[LABELS[a] for a in ARCHS],xlim=(-.025,1.025),
               xlabel='Exact-answer accuracy (12 tasks, 3 seeds each)')
        ax.grid(axis='x',alpha=.2); ax.legend(loc='upper right',frameon=False)
        fig.savefig(paper/'figures/empirical_clean.pdf'); plt.close(fig)
    print('Rendered tables and figures from all 720 recorded episodes.')

if __name__=='__main__': main()
