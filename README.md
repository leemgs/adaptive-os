# KernelGPT — Prototype (AAAI Adaptive OS)

This repository provides a runnable prototype of **KernelGPT**, mapping to the paper’s architecture: Telemetry → Semantic KB → LLM Reasoning → Safety Runtime → Interfaces (CLI/REST).  
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
kernelgpt/
├── LICENSE.md
├── README.md
├── requirements.txt
├── main.py
├── data/samples/telemetry_log.csv
├── patches/
│   ├── merge_writeback.patch
│   └── sched_child_runs_first.patch
└── src/
    ├── api/app.py
    ├── cli/kgpt_cli.py
    ├── kb/kb.py
    │   └── seed/{tunables.csv,outcomes.csv}
    ├── llm/{engine.py,prompts.py}
    ├── safety/runtime.py
    └── telemetry/{simulate_telemetry.py, ebpf/{ctxswitch.c,loader.py}}
```

### Notes
- Patches correspond to the **configuration simplification** case studies in the paper (merge `dirty_*` knobs; neutralize `sched_child_runs_first`).  
- The LLM engine defaults to a **rule‑based fallback**; plug in your provider by setting env `KGPT_USE_OPENAI=1` and implementing the call in `src/llm/engine.py`.

