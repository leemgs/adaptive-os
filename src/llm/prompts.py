from typing import List, Dict, Any

def format_rationale(workload: str, telem: Dict[str, Any], recs: List[Dict[str, Any]], retrieved: List[Dict[str, str]]):
    reasons = [f"workload={workload}", f"runqueue={telem['runqueue_depth']}", f"latency_ms={telem['latency_ms']}", f"io_wait_ms={telem['io_wait_ms']}"]
    bullets = []
    for r in recs:
        tgt = r.get('to', r.get('delta','proposal'))
        bullets.append(f"- {r['param']} → {tgt} ({r['effect']})")
    cite = '; '.join([o['actions'] for o in retrieved])
    return "Inputs: " + ', '.join(reasons) + "\n" + "\n".join(bullets) + f"\nKB: {cite}\nGuardrails: canary, rollback, monitoring"
