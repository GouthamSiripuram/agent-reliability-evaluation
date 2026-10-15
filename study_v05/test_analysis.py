import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import json
import numpy as np
import pandas as pd
from analysis import features, fit_router, route, mean_interval, ratio_interval, ARCHITECTURES


class AnalysisTests(unittest.TestCase):
    def training(self):
        rows=[]
        for i in range(10):
            for architecture in ARCHITECTURES:
                for seed in [137,271]:
                    rows.append({'task_id':str(i),'cohort':'architecture_train','budget':512,
                        'workflow':architecture,'seed':seed,'correct':architecture=='direct','output_tokens':100})
        return pd.DataFrame(rows)

    def test_router_rejects_heldout_cohort(self):
        frame=self.training();frame.loc[0,'cohort']='architecture_test'
        with self.assertRaises(ValueError):fit_router(frame,{str(i):f'{i} apples?' for i in range(10)})

    def test_router_fit_and_constant_baseline_use_training_only(self):
        frame=self.training();questions={str(i):f'{i} apples and 3 pears. How many total?' for i in range(10)}
        model=fit_router(frame,questions)
        self.assertEqual(model['best_training_constant'],'direct')
        self.assertEqual(route(model,'12 apples and 4 pears. How many total?'),'direct')
        self.assertEqual(len(model['training_task_ids']),10)

    def test_missing_workflow_training_cell_rejected(self):
        frame=self.training();frame=frame[~((frame.task_id=='1') & (frame.workflow=='direct'))]
        with self.assertRaises(ValueError):fit_router(frame,{str(i):str(i) for i in range(10)})

    def test_bootstrap_resamples_task_values(self):
        self.assertEqual(mean_interval([1,1,1]),[1.,1.,1.])
        mean,lo,hi=mean_interval([0,1]*32)
        self.assertEqual(mean,.5);self.assertLess(lo,.5);self.assertGreater(hi,.5)

    def test_zero_exposure_and_count_validation(self):
        self.assertEqual(ratio_interval([0,0],[0,0]),[None,None,None])
        self.assertEqual(ratio_interval([1,0],[1,1])[0],.5)
        with self.assertRaises(ValueError):ratio_interval([2],[1])

    def test_features_finite_without_dataset_labels(self):
        np.testing.assert_array_equal(features(''),np.zeros(6))
        self.assertTrue(np.isfinite(features('Each of 3 people has 2 apples. How many total?')).all())
        self.assertEqual(features('').shape,(6,))

    def test_complete_analysis_with_explicit_test_fixtures(self):
        # No model calls and no real evaluation files: this checks full analysis
        # wiring using a temporary, explicitly artificial unit-test dataset.
        import analysis
        from run_studies import jobs
        tasks=[]
        for cohort in ['reliability_test','architecture_train','architecture_test','architecture_transfer']:
            for i in range(2):
                tasks.append({'task_id':cohort+str(i),'cohort':cohort,'dataset':'test-fixture',
                              'question':f'{i} test items and 42 others. Total?','gold':'42'})
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'runs').mkdir()
            (root/'tasks.json').write_text(json.dumps(tasks),encoding='utf-8')
            (root/'MODEL_MANIFEST.json').write_text(json.dumps({'models':[{'id':'scripted-unit-fixture'}]}),encoding='utf-8')
            records=[]
            for task,workflow,seed,budget in jobs(tasks,False):
                for condition in (['clean','timeout','injection'] if workflow=='reliability' else ['clean']):
                    right=workflow in ['direct','reliability'] and condition!='injection'
                    answer='FINAL: 42' if right else 'FINAL: 1'
                    trace={'response':answer,'hit_token_limit':False}
                    records.append({'model':'scripted-unit-fixture','task_id':task['task_id'],'cohort':task['cohort'],
                        'dataset':'test-fixture','workflow':workflow,'condition':condition,'seed':seed,'budget':budget,
                        'answer':answer,'parsed_answer':'42' if right else '1','correct':right,
                        'output_tokens':20,'input_tokens':30,'generation_seconds':.1,
                        'branch_eligible':workflow=='reliability','sentinel_adopted':False,'trace':[trace,trace]})
            (root/'runs/model_0.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf-8')
            with patch.object(analysis,'ROOT',root),patch('run_studies.verify_freeze',return_value={}):
                analysis.analyze()
                analysis.analyze('reliability')
                analysis.analyze('architecture')
            policy=pd.read_csv(root/'results/architecture_policies.csv')
            selected=policy[policy.policy=='ridge_router']
            self.assertTrue(np.allclose(selected.delta_train_constant,0))
            self.assertTrue(np.allclose(selected.same_policy_heuristic_delta,0))
            self.assertTrue((root/'results/reliability_paired_effects.csv').exists())
            self.assertEqual(len(pd.read_csv(root/'results/reliability/episodes.csv')),12)
            self.assertEqual(len(pd.read_csv(root/'results/architecture/episodes.csv')),64)


if __name__=='__main__':unittest.main()
