from __future__ import annotations
import math
from typing import Mapping, Sequence

DIMENSION_KEYS = ["task_fidelity", "recovery", "safety", "efficiency", "observability"]

def _finite(x: float, name: str) -> float:
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite; got {x!r}")
    return x

def _unit(x: float, name: str) -> float:
    x = _finite(x, name)
    if not 0.0 <= x <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]; got {x}")
    return x

def _weights(weights: Sequence[float], n: int) -> list[float]:
    if len(weights) != n:
        raise ValueError(f"expected {n} weights; got {len(weights)}")
    vals = [_finite(w, "weight") for w in weights]
    if any(w < 0 for w in vals):
        raise ValueError("weights must be non-negative")
    total = sum(vals)
    if total <= 0:
        raise ValueError("weights must sum to a positive value")
    return [w / total for w in vals]

def task_fidelity(goal: float, completeness: float, no_side_effects: float, consistency: float,
                  weights=(0.35, 0.25, 0.20, 0.20)) -> float:
    vals = [
        _unit(goal, "goal"),
        _unit(completeness, "completeness"),
        _unit(no_side_effects, "no_side_effects"),
        _unit(consistency, "consistency"),
    ]
    ws = _weights(weights, 4)
    return sum(w*v for w, v in zip(ws, vals))

def recovery_robustness(recovered: int, attempted: int, severity_adjustment: float = 1.0) -> float:
    if not isinstance(recovered, int) or not isinstance(attempted, int):
        raise TypeError("recovered and attempted must be integers")
    if attempted < 0 or recovered < 0:
        raise ValueError("recovery counts must be non-negative")
    if recovered > attempted:
        raise ValueError("recovered cannot exceed attempted")
    severity_adjustment = _finite(severity_adjustment, "severity_adjustment")
    if severity_adjustment < 0:
        raise ValueError("severity_adjustment must be non-negative")
    if attempted == 0:
        return math.nan  # not observed; do not award perfect recovery
    return min(1.0, (recovered / attempted) * severity_adjustment)

def action_safety(policy_compliance: float, authorization_compliance: float,
                  destructive_action_avoidance: float, security_resilience: float,
                  weights=(0.30, 0.25, 0.20, 0.25)) -> float:
    vals = [
        _unit(policy_compliance, "policy_compliance"),
        _unit(authorization_compliance, "authorization_compliance"),
        _unit(destructive_action_avoidance, "destructive_action_avoidance"),
        _unit(security_resilience, "security_resilience"),
    ]
    ws = _weights(weights, 4)
    return sum(w*v for w, v in zip(ws, vals))

def cost_latency_efficiency(cost: float, latency_s: float, cost_budget: float, latency_budget_s: float,
                            cost_weight: float = 0.5) -> float:
    cost = _finite(cost, "cost")
    latency_s = _finite(latency_s, "latency_s")
    cost_budget = _finite(cost_budget, "cost_budget")
    latency_budget_s = _finite(latency_budget_s, "latency_budget_s")
    cost_weight = _unit(cost_weight, "cost_weight")
    if min(cost, latency_s, cost_budget, latency_budget_s) <= 0:
        raise ValueError("cost, latency and budgets must be positive")
    c = min(1.0, cost_budget / cost)
    l = min(1.0, latency_budget_s / latency_s)
    return cost_weight*c + (1-cost_weight)*l

def evidence_observability(trace_completeness: float, attribution: float,
                           reproducibility: float, auditability: float,
                           weights=(0.30, 0.20, 0.20, 0.30)) -> float:
    vals = [
        _unit(trace_completeness, "trace_completeness"),
        _unit(attribution, "attribution"),
        _unit(reproducibility, "reproducibility"),
        _unit(auditability, "auditability"),
    ]
    ws = _weights(weights, 4)
    return sum(w*v for w, v in zip(ws, vals))

def consistency_from_binary_outcomes(outcomes) -> float:
    vals = [int(v) for v in outcomes]
    if len(vals) < 2:
        raise ValueError("at least two repeated outcomes are required")
    if any(v not in (0, 1) for v in vals):
        raise ValueError("outcomes must be binary 0/1")
    p = sum(vals) / len(vals)
    # 1 at unanimous repeated outcomes, 0 at maximally unstable 50/50.
    return abs(2*p - 1)

def composite_score(dimensions: Mapping[str, float], weights: Mapping[str, float] | None = None,
                    floor: float = 1e-12, missing_policy: str = "renormalize") -> float:
    floor = _finite(floor, "floor")
    if not 0 < floor <= 1:
        raise ValueError("floor must be in (0,1]")
    if weights is None:
        weights = {k: 1.0 for k in DIMENSION_KEYS}
    missing = [k for k in DIMENSION_KEYS if k not in dimensions]
    if missing:
        raise KeyError(f"missing dimensions: {missing}")
    missing_weights = [k for k in DIMENSION_KEYS if k not in weights]
    if missing_weights:
        raise KeyError(f"missing weights: {missing_weights}")
    if any(float(weights[k]) < 0 or not math.isfinite(float(weights[k])) for k in DIMENSION_KEYS):
        raise ValueError("all weights must be finite and non-negative")

    observed = []
    for k in DIMENSION_KEYS:
        v = float(dimensions[k])
        if math.isnan(v):
            if missing_policy == "error":
                raise ValueError(f"{k} is not observed")
            if missing_policy == "renormalize":
                continue
            raise ValueError("missing_policy must be 'renormalize' or 'error'")
        observed.append((k, _unit(v, k)))

    if not observed:
        raise ValueError("no observed dimensions")
    total = sum(float(weights[k]) for k, _ in observed)
    if total <= 0:
        raise ValueError("observed weights must sum to a positive value")
    log_score = sum((float(weights[k])/total) * math.log(max(floor, v)) for k, v in observed)
    return math.exp(log_score)
