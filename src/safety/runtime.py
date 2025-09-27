from typing import Dict, Any, List
import random

class SafetyRuntime:
    def __init__(self, slo_latency_ms: int = 15, max_anomaly_rate: float = 0.02):
        self.slo_latency_ms = slo_latency_ms
        self.max_anomaly_rate = max_anomaly_rate

    def canary_and_apply(self, workload: str, recs: List[Dict[str, Any]]):
        trials = 5
        improvements = 0
        for _ in range(trials):
            delta = random.uniform(-2.0, 4.0)  # ms
            if delta < 0:
                improvements += 1
        anomalies = random.uniform(0.0, 0.03)
        decision = 'commit' if (improvements >= (trials // 2) and anomalies <= self.max_anomaly_rate) else 'rollback'
        return {'decision': decision, 'anomaly_rate': round(anomalies, 3), 'improved_trials': improvements, 'trials': trials}
