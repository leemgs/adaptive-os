import argparse, json
from ..kb.kb import SemanticKB
from ..llm.engine import recommend
from ..safety.runtime import SafetyRuntime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['recommend'])
    ap.add_argument('--workload', required=True, choices=['web','oltp','streaming','sensor'])
    args = ap.parse_args()

    kb = SemanticKB('src/kb')
    retrieved = kb.retrieve(args.workload)
    telem = dict(runqueue_depth=5, ctx_switches=900, latency_ms=14, numa_imbalance=0.3, io_wait_ms=8)
    out = recommend(args.workload, telem, retrieved)
    guard = SafetyRuntime().canary_and_apply(args.workload, out['recommendations'])
    print(json.dumps({'advice': out, 'guardrails': guard}, indent=2))

if __name__ == '__main__':
    main()
