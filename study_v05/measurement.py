"""Measurements for the new study; the frozen v0.4 scorer is unchanged."""
import math
import re
from decimal import Decimal, InvalidOperation

NUMBER = r'[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'


def parse_answer(value):
    if value is None:
        return None
    text = str(value).strip()
    marked = re.findall(r'(?im)^\s*(?:FINAL\s*:\s*|####\s*)([^\n]+)', text)
    candidate = marked[-1].strip() if marked else text
    if not re.fullmatch(NUMBER, candidate):
        return None
    try:
        result = Decimal(candidate.replace(',', ''))
        return result if result.is_finite() else None
    except InvalidOperation:
        return None


def correct(answer, gold):
    expected = parse_answer(gold)
    if expected is None:
        raise ValueError('Invalid gold label')
    return parse_answer(answer) == expected


def final_line_number(value):
    """Sensitivity heuristic, not the primary scorer or a semantic verifier.

    Accept one numeric literal on the final nonempty line, allowing surrounding
    prose/units/markup. Reject multiple numbers or explicit arithmetic operators.
    This can still mistake a lone unrelated number for an answer; report as a
    sensitivity analysis, never silently substitute it for the primary outcome.
    """
    lines=[s.strip() for s in str(value or '').splitlines() if s.strip()]
    if not lines:
        return None
    line=lines[-1].replace('**','').replace('####','').replace('$','')
    if any(op in line for op in ['=','/','*','\\times','\\frac']):
        return None
    numbers=re.findall(NUMBER,line)
    return parse_answer(numbers[0]) if len(numbers)==1 else None


def geometric_bounds(values, weights=None, floor=1e-12):
    """Sharp box bounds for a fixed-weight floored geometric mean.

    Missing components range independently over [0, 1]. These are identification
    bounds under the stated rubric, not statistical confidence intervals.
    """
    if not values or not 0 < floor <= 1 or not math.isfinite(floor):
        raise ValueError('Nonempty values and finite floor in (0,1] required')
    weights = [1.] * len(values) if weights is None else list(weights)
    if len(weights) != len(values):
        raise ValueError('Weight length mismatch')
    if any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError('Invalid weight')
    total = sum(weights)
    if not math.isfinite(total) or total <= 0:
        raise ValueError('Invalid total weight')
    observed_log = 0.; missing_weight = 0.
    for value, weight in zip(values, weights):
        if value is None:
            missing_weight += weight / total
        else:
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError('Invalid component')
            observed_log += weight / total * math.log(max(floor, value))
    return (math.exp(observed_log + missing_weight * math.log(floor)),
            math.exp(observed_log))


def conditional_rate(successes, exposures):
    if not 0 <= successes <= exposures:
        raise ValueError('Successes must be within exposure denominator')
    return successes / exposures if exposures else None
