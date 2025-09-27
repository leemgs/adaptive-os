import argparse, json
from src.telemetry.simulate_telemetry import stream
from src.kb.kb import SemanticKB
from src.llm.engine import recommend
from src.safety.runtime import SafetyRuntime

def run(workload: str, trials: int):
    kb = SemanticKB('src/kb')
    retrieved = kb.retrieve(workload)
    latest = None
    for _i, snap in enumerate(stream(workload, steps=trials)):
        latest = snap
    out = recommend(workload, latest, retrieved)
    guard = SafetyRuntime().canary_and_apply(workload, out['recommendations'])
    print(json.dumps({'telemetry': latest, 'advice': out, 'guardrails': guard}, indent=2))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--workload', default='web', choices=['web','oltp','streaming','sensor'])
    ap.add_argument('--trials', type=int, default=5)
    args = ap.parse_args()
    run(args.workload, args.trials)
