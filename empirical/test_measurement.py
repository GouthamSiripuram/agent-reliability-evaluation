import unittest
from decimal import Decimal
from measurement import calculate, parse_answer, score_answer

class MeasurementTests(unittest.TestCase):
    def test_real_arithmetic(self):
        self.assertEqual(calculate('(48+24)/3'), 24)
        self.assertEqual(calculate('-2+3*4'), 10)
    def test_no_code_execution(self):
        for expression in ['__import__("os")', '(1).__class__', '[1,2]', '2**100000', '1/0']:
            with self.assertRaises(Exception): calculate(expression)
    def test_final_marker_not_intermediate_reasoning(self):
        self.assertEqual(parse_answer('First 5 then 7. #### 12'), Decimal(12))
        self.assertIsNone(parse_answer('First 5 then 7.'))
    def test_numeric_normalization(self):
        self.assertTrue(score_answer('#### $1,200.00', 'reasoning #### 1200'))
        self.assertFalse(score_answer('1201', '#### 1200'))
        self.assertTrue(score_answer('#### NUMBER\n72', '#### 72'))
        self.assertTrue(score_answer(r'Final: \boxed{72}', '#### 72'))
    def test_invalid_answer_is_failure(self):
        for answer in [None, 'nan', 'inf', 'no answer', '{}']:
            self.assertFalse(score_answer(answer, '#### 42'))

if __name__ == '__main__': unittest.main()
