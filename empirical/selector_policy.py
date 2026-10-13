"""Predeclared question-only proxies for testing the existing, unfitted selector.

These proxies are not validated construct measurements. No answers or run outcomes
are used to derive them. Their limitations must accompany any policy evaluation.
"""
import re

COEFFICIENTS={
    'single_agent':(.05,.05,.02,.05,.06,.05),
    'single_agent_tools':(.10,.30,.08,.08,.08,.12),
    'planner_executor_verifier':(.45,.35,.70,.35,.25,.35),
    'hierarchical_multi_agent':(.85,.80,.65,.75,.55,.70),
}

def descriptors(question):
    sentences=len(re.findall(r'[.!?](?:\s|$)',question))
    numeric_mentions=len(re.findall(r'\b\d+(?:\.\d+)?\b',question))
    return {'decomposability':min(max(sentences-1,0)/4,1),
            'specialization_need':0.,'verification_value':1.,
            'coordination_burden':.25,'error_propagation_risk':min(numeric_mentions/12,1),
            'resource_sensitivity':.5}

def select(question):
    x=list(descriptors(question).values())
    utilities={a:sum(c[i]*x[i]*(1 if i<3 else -1) for i in range(6)) for a,c in COEFFICIENTS.items()}
    best=max(utilities.values()); winners=[a for a,v in utilities.items() if abs(v-best)<=1e-12]
    if len(winners)!=1: raise ValueError('Explicit policy tie requires resolution')
    return winners[0],utilities
