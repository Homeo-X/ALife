"""Experiment configuration — everything a run needs to be reproduced.

A ``Config`` is a plain, serializable record. Given a config and the code, a run
is bit-for-bit reproducible (the seed drives the single ``Noise`` source). Configs
round-trip through JSON so experiments can be checked into ``configs/`` and
results traced back to exactly what produced them.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class Config:
    experiment: str
    seed: int = 0
    ticks: int = 400
    total_quanta: int = 4000
    decay_hazard: float = 0.02
    max_reactions_per_tick: int | None = 200
    # experiment-specific knobs (alphabet size, binding rules, ...)
    params: dict[str, Any] = field(default_factory=dict)

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def from_json(cls, path: str | Path) -> "Config":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)

    def get(self, key: str, default: Any = None) -> Any:
        return self.params.get(key, default)
