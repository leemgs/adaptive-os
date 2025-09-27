# AdaptiveOS — Prototype
This repository provides a runnable prototype of **AdaptiveOS**, mapping to the paper’s architecture: Telemetry → Semantic KB → LLM Reasoning → Safety Runtime → Interfaces (CLI/REST).  
It defaults to **simulation mode** (no root) and includes **optional eBPF stubs** for ctx‑switch sampling (root + bcc).

## Install
```bash
pip install -r requirements.txt
```

## Simulated end‑to‑end
```bash
python main.py --workload web --trials 5
```

## REST API
```bash
uvicorn src.api.app:app --reload --port 8080
curl -X POST localhost:8080/recommend -H "Content-Type: application/json" -d '{"workload":"oltp"}'
```

## CLI
```bash
python src/cli/kgpt_cli.py recommend --workload streaming
```

## Tree
```
AdaptiveOS/
├── LICENSE.md                # Apache-2.0
├── README.md                 # 실행/구성/주의사항
├── requirements.txt          # 경량 의존성(오프라인에서도 설치 가능)
├── main.py                   # 시뮬레이션 E2E 오케스트레이터
├── data/samples/telemetry_log.csv
├── patches/
│   ├── merge_writeback.patch             # vm.dirty_* → vm.dirty_budget_ratio 통합
│   └── sched_child_runs_first.patch      # CFS 레거시 knob 중립화
└── src/
    ├── api/app.py            # FastAPI 엔드포인트(/recommend)
    ├── cli/kgpt_cli.py       # 개발자 CLI
    ├── kb/kb.py              # 시맨틱 KB + 간단 검색
    │   └── seed/{tunables.csv,outcomes.csv}
    ├── llm/{engine.py,prompts.py}  # 규칙기반 LLM 대체 + 플러그인 훅
    ├── safety/runtime.py     # 카나리/롤백/SLO 가드레일
    └── telemetry/
        ├── simulate_telemetry.py         # 루트 불필요 시뮬레이션
        └── ebpf/{ctxswitch.c,loader.py}  # 선택: bcc 필요(루트)

```

### Notes
- Patches correspond to the **configuration simplification** case studies in the paper (merge `dirty_*` knobs; neutralize `sched_child_runs_first`).  
- The LLM engine defaults to a **rule‑based fallback**; plug in your provider by setting env `KGPT_USE_OPENAI=1` and implementing the call in `src/llm/engine.py`.

