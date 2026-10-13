import math, pytest
from fdar.metrics import (
    task_fidelity, recovery_robustness, composite_score,
    cost_latency_efficiency, consistency_from_binary_outcomes
)

def test_nan_rejected_in_metric():
    with pytest.raises(ValueError):
        task_fidelity(float("nan"), .8, .9, .8)

def test_no_recovery_test_is_not_perfect():
    assert math.isnan(recovery_robustness(0, 0))

def test_invalid_counts_rejected():
    with pytest.raises(ValueError):
        recovery_robustness(2, 1)

def test_invalid_cost_weight_rejected():
    with pytest.raises(ValueError):
        cost_latency_efficiency(.1, 1, .1, 1, cost_weight=1.5)

def test_composite_renormalizes_missing_recovery():
    s = composite_score({
        "task_fidelity":.8, "recovery":float("nan"), "safety":.9,
        "efficiency":.7, "observability":.8
    })
    assert 0 < s <= 1

def test_bad_dimension_weight_rejected():
    with pytest.raises(ValueError):
        composite_score(
            {"task_fidelity":.8,"recovery":.8,"safety":.8,"efficiency":.8,"observability":.8},
            weights={"task_fidelity":1,"recovery":1,"safety":-1,"efficiency":1,"observability":1}
        )

def test_consistency_helper():
    assert consistency_from_binary_outcomes([1,1,1,1]) == 1
    assert consistency_from_binary_outcomes([1,0,1,0]) == 0

@pytest.mark.parametrize("value", [.5, -.5, 1.5, float("nan"), float("inf")])
def test_consistency_rejects_nonbinary(value):
    with pytest.raises(ValueError):
        consistency_from_binary_outcomes([0, value])

def test_unknown_missing_policy_rejected_without_missing_values():
    from fdar.metrics import DIMENSION_KEYS
    with pytest.raises(ValueError):
        composite_score(dict.fromkeys(DIMENSION_KEYS, .8), missing_policy="typo")

def test_overflowing_weights_rejected():
    with pytest.raises(ValueError):
        task_fidelity(1, 1, 1, 1, weights=[1e308]*4)

def test_missing_recovery_is_reported_separately_from_observed_zero():
    import pandas as pd
    from fdar.evaluator import REQUIRED, evaluate_runs
    row = dict.fromkeys(REQUIRED, 1.0)
    row.update(recovered_failures=0, attempted_failures=0)
    observed = dict(row, attempted_failures=1)
    scored = evaluate_runs(pd.DataFrame([row, observed]))
    assert list(scored.observed_dimension_count) == [4, 5]
    assert math.isnan(scored.recovery.iloc[0])
    assert scored.recovery.iloc[1] == 0
    assert scored.reliability_score.iloc[0] == pytest.approx(1)
    assert scored.reliability_score.iloc[1] == pytest.approx(10**(-12/5))

def test_strict_missing_policy_rejects_unobserved_recovery():
    from fdar.metrics import DIMENSION_KEYS
    dims = dict.fromkeys(DIMENSION_KEYS, .8)
    dims['recovery'] = math.nan
    with pytest.raises(ValueError, match='not observed'):
        composite_score(dims, missing_policy='error')
