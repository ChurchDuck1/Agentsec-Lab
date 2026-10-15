import json
import time
from pathlib import Path

class AuditLog:
    def __init__(self, path: Path, clock=time.time):
        self.path = Path(path)
        self.clock = clock   
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: str, **fields):
        entry = {"ts": self.clock(), "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read_all(self) -> list[dict]:
        return [json.loads(line) for line in self.path.read_text().splitlines() if line]