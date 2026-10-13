import unittest
from pathlib import Path
import json
import numpy as np
import pandas as pd
from analyze import mean_ci, conditional_ci
from selector_policy import descriptors, select


class AnalysisTests(unittest.TestCase):
    def test_constant_task_bootstrap(self):
        self.assertEqual(mean_ci([0]*12), (0., 0., 0.))
        self.assertEqual(mean_ci([1]*12), (1., 1., 1.))

    def test_unexposed_not_perfect_recovery(self):
        frame = pd.DataFrame({'task_id':['a','b'], 'success':[0,0], 'exposed':[0,0]})
        self.assertEqual(conditional_ci(frame,'success','exposed'), (None,None,None))

    def test_conditional_denominator(self):
        frame = pd.DataFrame({'task_id':['a','a','b','b'], 'success':[1,0,0,0], 'exposed':[1,1,0,0]})
        self.assertEqual(conditional_ci(frame,'success','exposed')[0], .5)

    def test_fixed_proxy_bounds_and_determinism(self):
        for q in ['', 'One question?', '1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13?']:
            self.assertTrue(all(0 <= v <= 1 for v in descriptors(q).values()))
            self.assertEqual(select(q), select(q))

    def test_selected_task_provenance(self):
        records = json.loads((Path(__file__).parent/'tasks.json').read_text(encoding='utf-8'))
        rows = [r['row_index'] for r in records if r['split']=='test']
        self.assertEqual(rows, [32,55,301,413,438,441,467,605,618,954,1023,1255])
        self.assertEqual(len(set(r['task_id'] for r in records)), 14)


if __name__ == '__main__':
    unittest.main()
