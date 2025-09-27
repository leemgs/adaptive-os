import time, random, json
from typing import Dict

def stream(workload: str, steps: int = 30):
    rng = random.Random(42)
    for t in range(steps):
        runq = max(1, int(rng.gauss(3 if workload!='streaming' else 5, 1)))
        ctx = max(200, int(rng.gauss(900 if workload=='web' else 750, 80)))
        lat = max(3, int(rng.gauss(9 if workload=='web' else 13, 2)))
        numa = max(0.0, round(rng.random()*0.5, 2))
        iow = max(2, int(rng.gauss(6 if workload!='oltp' else 9, 2)))
        yield {
            "runqueue_depth": runq,
            "ctx_switches": ctx,
            "latency_ms": lat,
            "numa_imbalance": numa,
            "io_wait_ms": iow
        }
        time.sleep(0.02)

if __name__ == '__main__':
    for x in stream('web', 3):
        print(json.dumps(x))
