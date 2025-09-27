from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ..kb.kb import SemanticKB
from ..llm.engine import recommend
from ..safety.runtime import SafetyRuntime

app = FastAPI(title='KernelGPT API')

class Req(BaseModel):
    workload: str
    runqueue_depth: Optional[int] = 4
    ctx_switches: Optional[int] = 800
    latency_ms: Optional[int] = 12
    numa_imbalance: Optional[float] = 0.2
    io_wait_ms: Optional[int] = 6

@app.post('/recommend')
def do_recommend(req: Req):
    kb = SemanticKB('src/kb')
    retrieved = kb.retrieve(req.workload)
    out = recommend(req.workload, req.dict(), retrieved)
    guard = SafetyRuntime().canary_and_apply(req.workload, out['recommendations'])
    return {'advice': out, 'guardrails': guard}
