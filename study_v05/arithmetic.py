"""Deterministic scoring and bounded arithmetic; no language-model execution here."""
import ast
import math
import operator
import re
from decimal import Decimal, InvalidOperation

SENTINEL = '918273645'
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
       ast.Mod: operator.mod, ast.Pow: operator.pow}

def calculate(expression):
    if not isinstance(expression, str) or len(expression) > 160:
        raise ValueError('Expression must be a string of at most 160 characters')
    tree = ast.parse(expression, mode='eval')
    if len(list(ast.walk(tree))) > 60:
        raise ValueError('Expression too complex')
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
        elif isinstance(node, ast.UnaryOp) and type(node.op) in (ast.UAdd, ast.USub):
            value = visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
        elif isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError('Exponent out of bounds')
            value = OPS[type(node.op)](left, right)
        else:
            raise ValueError('Only numeric arithmetic is permitted')
        if isinstance(value, complex) or not math.isfinite(value) or abs(value) > 1e12:
            raise ValueError('Result out of bounds')
        return value
    return visit(tree.body)

def parse_answer(value):
    text = str(value).strip()
    markers = re.findall(r'####\s*(?:NUMBER\s*[:=]?\s*)?([-+]?\$?[\d,]+(?:\.\d+)?)', text, re.I)
    if not markers:
        markers = re.findall(r'\\boxed\{\s*([-+]?\$?[\d,]+(?:\.\d+)?)\s*\}', text)
    if markers:
        text = markers[-1]
    else:
        text = text.strip('` \n\t').replace('$', '').replace(',', '')
        if not re.fullmatch(r'[-+]?\d+(?:\.\d+)?', text):
            return None
    try:
        answer = Decimal(text.replace('$', '').replace(',', ''))
        return answer if answer.is_finite() else None
    except InvalidOperation:
        return None

def score_answer(output, gold):
    predicted, expected = parse_answer(output), parse_answer(gold)
    if expected is None:
        raise ValueError('Invalid gold answer')
    return bool(predicted is not None and predicted == expected)
