import json, os, time
from typing import Any, Dict

class TraceLogger:
    def __init__(self, out_dir="runs"):
        os.makedirs(out_dir, exist_ok=True)
        ts = time.strftime("%Y%m%d-%H%M%S")
        self.path = os.path.join(out_dir, f"trace-{ts}.jsonl")
        self.f = open(self.path, "a", encoding="utf-8")

    def log(self, **payload: Dict[str,Any]):
        self.f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.f.flush()

    def close(self):
        try: self.f.close()
        except: pass
