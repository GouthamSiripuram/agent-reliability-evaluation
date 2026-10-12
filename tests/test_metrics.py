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
