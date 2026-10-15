import itertools
import json
import math
from pathlib import Path
import unittest
from measurement import parse_answer, correct, geometric_bounds, conditional_rate, final_line_number
from workflows import architecture_episode, reliability_prefix, reliability_branch, request, ARCHITECTURES


class ScriptedModel:
    model_id = 'scripted-test-double-not-an-experiment'
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.calls = []
    def call(self,messages,limit,seed,role,stop_line=False):
        trace = {'messages':messages,'limit':limit,'seed':seed,'role':role,
                 'response':next(self.outputs),'input_tokens':1,'output_tokens':limit,'seconds':0.}
        self.calls.append(trace)
        return trace


class MeasurementTests(unittest.TestCase):
    def test_expression_is_not_numeric_prefix(self):
        for value in ['FINAL: 2 + 12 = 14','#### 2 + 12 = 14','FINAL: 14 apples','FINAL: NaN',None]:
            self.assertIsNone(parse_answer(value))
        self.assertTrue(correct('Reasoning\nFINAL: 1,234.50','1234.5'))

    def test_gold_must_be_valid(self):
        with self.assertRaises(ValueError):correct('FINAL: 1','unavailable')

    def test_sensitivity_parser_is_separate_and_rejects_arithmetic(self):
        self.assertIsNone(parse_answer('The answer is **21** blocks.'))
        self.assertEqual(str(final_line_number('The answer is **21** blocks.')),'21')
        self.assertIsNone(final_line_number('2 + 12 = 14'))
        self.assertIsNone(final_line_number('2/3'))
        self.assertIsNone(final_line_number('between 21 and 22'))

    def test_no_exposure_is_missing(self):
        self.assertIsNone(conditional_rate(0,0))
        self.assertEqual(conditional_rate(1,4),.25)
        with self.assertRaises(ValueError):conditional_rate(1,0)

    def test_bounds_are_sharp_over_missing_box_corners(self):
        lo,hi = geometric_bounds([.8,None,.3,None],[1,2,3,4],floor=.01)
        corners = []
        for a,b in itertools.product([0.,1.],repeat=2):
            vals = [.8,a,.3,b]
            corners.append(math.exp(sum(w/10*math.log(max(.01,v)) for v,w in zip(vals,[1,2,3,4]))))
        self.assertAlmostEqual(lo,min(corners)); self.assertAlmostEqual(hi,max(corners))

    def test_observing_component_cannot_widen_bounds(self):
        lo,hi = geometric_bounds([.7,None,None])
        for value in [0.,.1,.8,1.]:
            a,b = geometric_bounds([.7,value,None])
            self.assertGreaterEqual(a+1e-15,lo);self.assertLessEqual(b,hi+1e-15)

    def test_no_missing_collapses_interval(self):
        lo,hi = geometric_bounds([.25,1])
        self.assertAlmostEqual(lo,.5);self.assertAlmostEqual(hi,.5)
        self.assertEqual(geometric_bounds([None,None])[1],1.)

    def test_invalid_scientific_inputs_rejected(self):
        for values,weights in [([float('nan')],None),([2],None),([.5],[0]),([.5],[float('inf')]),([.5],[-1])]:
            with self.assertRaises(ValueError):geometric_bounds(values,weights)


class WorkflowTests(unittest.TestCase):
    def test_ambiguous_actions_rejected(self):
        self.assertEqual(request('CALC: 2+2\nFINAL: 4')[0],'invalid')

    def test_same_prefix_branches_timeout_retry(self):
        model = ScriptedModel(['CALC: 6*7','CALC: 6*7','FINAL: 42'])
        prefix = reliability_prefix(model,'Six times seven?',137)
        answer,traces,events,termination = reliability_branch(model,prefix,'timeout',137)
        self.assertEqual(answer,'FINAL: 42');self.assertEqual(termination,'final')
        self.assertIn('timeout',events[0]['output']);self.assertEqual(events[1]['output'],'Calculator result: 42')
        self.assertIs(traces[0],prefix['trace'])

    def test_unexposed_branch_generates_no_fake_calls(self):
        model = ScriptedModel(['FINAL: 42'])
        prefix = reliability_prefix(model,'Six times seven?',137)
        for condition in ['clean','timeout','injection']:
            answer,traces,events,_ = reliability_branch(model,prefix,condition,137)
            self.assertEqual(answer,'FINAL: 42');self.assertFalse(events)
            self.assertEqual(len(traces),1)
        self.assertEqual(len(model.calls),1)

    def test_unsafe_calculation_never_executed(self):
        model = ScriptedModel(['CALC: __import__("os").getcwd()'])
        prefix = reliability_prefix(model,'test',137)
        self.assertFalse(prefix['valid_request'])

    def test_all_workflows_obey_budget_without_gold_prompt(self):
        for budget in [512,1024]:
            for architecture in ARCHITECTURES:
                model = ScriptedModel(['FINAL: 123']*3)
                _,traces = architecture_episode(model,'QUESTION ONLY',architecture,budget,137)
                self.assertEqual(sum(t['output_tokens'] for t in traces),budget)
                if any(t['role']=='planner' for t in traces):
                    self.assertNotIn('Finish with FINAL:',traces[0]['messages'][0]['content'])

    def test_cohorts_and_pilot_do_not_share_questions(self):
        root = Path(__file__).parent
        tasks = json.loads((root/'tasks.json').read_text(encoding='utf-8'))
        self.assertEqual(len(tasks),264)
        from prepare_tasks import normalize
        self.assertEqual(len({normalize(t['question']) for t in tasks}),264)
        pilot = json.loads((root.parent/'empirical/tasks.json').read_text(encoding='utf-8'))
        self.assertFalse({normalize(t['question']) for t in tasks}&{normalize(t['question']) for t in pilot})


if __name__ == '__main__':
    unittest.main()
