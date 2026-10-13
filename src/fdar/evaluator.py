from __future__ import annotations
import math
import pandas as pd
from .metrics import (
    task_fidelity, recovery_robustness, action_safety,
    cost_latency_efficiency, evidence_observability, composite_score
)

REQUIRED = [
    "goal","completeness","no_side_effects","consistency",
    "recovered_failures","attempted_failures",
    "policy_compliance","authorization_compliance",
    "destructive_action_avoidance","security_resilience",
    "cost","latency_s","cost_budget","latency_budget_s",
    "trace_completeness","attribution","reproducibility","auditability"
]

def _integer_count(value, name):
    if pd.isna(value):
        raise ValueError(f"{name} is missing")
    fv = float(value)
    if not fv.is_integer():
        raise ValueError(f"{name} must be an integer count; got {value}")
    return int(fv)

def evaluate_runs(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    out = df.copy()

    out["task_fidelity"] = out.apply(lambda r: task_fidelity(
        r.goal, r.completeness, r.no_side_effects, r.consistency), axis=1)

    out["recovery"] = out.apply(lambda r: recovery_robustness(
        _integer_count(r.recovered_failures, "recovered_failures"),
        _integer_count(r.attempted_failures, "attempted_failures")), axis=1)

    out["safety"] = out.apply(lambda r: action_safety(
        r.policy_compliance, r.authorization_compliance,
        r.destructive_action_avoidance, r.security_resilience), axis=1)

    out["efficiency"] = out.apply(lambda r: cost_latency_efficiency(
        r.cost, r.latency_s, r.cost_budget, r.latency_budget_s), axis=1)

    out["observability"] = out.apply(lambda r: evidence_observability(
        r.trace_completeness, r.attribution, r.reproducibility, r.auditability), axis=1)

    out["reliability_score"] = out.apply(lambda r: composite_score({
        "task_fidelity": r.task_fidelity,
        "recovery": r.recovery,
        "safety": r.safety,
        "efficiency": r.efficiency,
        "observability": r.observability
    }, missing_policy="renormalize"), axis=1)
    # A four-component score must not be confused with a fully observed score.
    out["observed_dimension_count"] = out[[
        "task_fidelity", "recovery", "safety", "efficiency", "observability"
    ]].notna().sum(axis=1)
    return out
