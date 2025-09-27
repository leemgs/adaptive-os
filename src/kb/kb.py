import csv
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

@dataclass
class Tunable:
    name: str
    subsystem: str
    default: str
    range: str
    description: str

class SemanticKB:
    def __init__(self, root: str):
        self.root = Path(root)
        self.tunables: List[Tunable] = []
        self.outcomes: List[Dict[str, str]] = []
        self._load()

    def _load(self):
        with open(self.root/'seed'/'tunables.csv') as f:
            for row in csv.DictReader(f):
                self.tunables.append(Tunable(**row))
        with open(self.root/'seed'/'outcomes.csv') as f:
            for row in csv.DictReader(f):
                self.outcomes.append(row)

    def retrieve(self, workload: str) -> List[Dict[str, Any]]:
        hits = []
        for o in self.outcomes:
            score = 0.0
            if workload == o['workload']:
                score += 1.0
            if 'dirty' in o['actions']:
                score += 0.1
            hits.append((score, o))
        hits.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in hits[:3]]
