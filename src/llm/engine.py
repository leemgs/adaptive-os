import os
from typing import Dict, Any, List
from .prompts import format_rationale

DIRTY_BUDGET_DEFAULT = 18

def _rule_based_policy(workload: str, telem: Dict[str, Any], retrieved: List[Dict[str, str]]):
    recs = []
    runq = telem['runqueue_depth']
    lat = telem['latency_ms']
    iow = telem['io_wait_ms']
    if iow > 8 or workload in ('oltp','streaming'):
        recs.append(dict(param='vm.dirty_budget_ratio', from_=None, to=DIRTY_BUDGET_DEFAULT, effect='stabilize writeback; fewer oscillations'))
    if runq > 4 or lat > 12:
        recs.append(dict(param='kernel.sched_latency_ns', delta='-20%', effect='lower tail at risk of fairness'))
        recs.append(dict(param='kernel.sched_min_granularity_ns', delta='-10%', effect='tighter slices for bursts'))
    if workload in ('web','streaming'):
        recs.append(dict(param='kernel.sched_wake_affine', to=1, effect='localize cache; reduce tail spikes'))
    recs.append(dict(param='kernel.sched_child_runs_first', to=0, effect='neutralize legacy bias under PELT'))
    return recs

def recommend(workload: str, latest_telem: Dict[str, Any], retrieved: List[Dict[str, str]]):
    # Hook for real LLMs (set KGPT_USE_OPENAI=1)
    if os.getenv('KGPT_USE_OPENAI') == '1':
        # Implement your provider call here.
        pass
    recs = _rule_based_policy(workload, latest_telem, retrieved)
    rationale = format_rationale(workload, latest_telem, recs, retrieved)
    return {'recommendations': recs, 'rationale': rationale, 'confidence': 0.72}
