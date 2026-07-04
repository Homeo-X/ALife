"""The shared run harness — identical instrumentation for every experiment.

Builds the universe and scheduler from a ``Config`` and a ``Physics``, attaches
the standard emergence trackers as recorders, runs the loop, and packages a
fully-serializable :class:`RunResult`. Determinism is preserved end to end: the
same config yields the same result.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from omega.config import Config
from omega.emergence.construction import ConstructionTracker
from omega.emergence.novelty import NoveltyTracker
from omega.emergence.persistence import PersistenceTracker
from omega.kernel.scheduler import Scheduler, TickReport
from omega.kernel.transform import Physics
from omega.kernel.universe import Universe
from omega.metrics.openendedness import open_endedness_index
from omega.metrics.organization_metrics import snapshot_metrics
from omega.substrate.noise import Noise


@dataclass
class RunResult:
    config: Config
    metrics: list[dict[str, Any]]        # per-tick OrganizationMetrics
    novelty_new_per_tick: list[int]
    novelty_cumulative: list[int]
    depth_per_tick: list[int]
    discovered_per_tick: list[int]
    persistence: dict[str, Any]
    open_endedness: dict[str, Any]
    final_population: int
    final_classes_total: int

    def to_json(self, path: str | Path) -> None:
        payload = asdict(self)
        payload["config"] = asdict(self.config)
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def headline(self) -> str:
        oe = self.open_endedness
        p = self.persistence
        return (
            f"[{self.config.experiment}] ticks={self.config.ticks} "
            f"pop={self.final_population} classes_ever={self.final_classes_total} | "
            f"persist: max_reform={p['max_reformations']} "
            f"reformed={p['reformed_fraction']:.3f} "
            f"composed_persistent={p['composed_persistent']} | "
            f"OEI={oe['index']:.4f} [{oe['verdict']}]"
        )


def run(physics: Physics, config: Config, *, novelty_window: int | None = None) -> RunResult:
    # The rate-measurement window must be long enough to *resolve* a slow but
    # sustained discovery rate. A fixed 50-tick window quantizes a ~0.05/tick rate
    # to zero over long runs and reports a spurious CLOSED verdict (the mirror of
    # the v0.1 false positive). Scale it with the horizon.
    if novelty_window is None:
        novelty_window = max(50, config.ticks // 10)
    rng = Noise(config.seed)
    universe = Universe(total_quanta=config.total_quanta)
    physics.seed(universe, rng)

    scheduler = Scheduler(
        universe, physics, rng,
        decay_hazard=config.decay_hazard,
        max_reactions_per_tick=config.max_reactions_per_tick,
    )

    novelty = NoveltyTracker()
    construction = ConstructionTracker()
    metrics_series: list[dict[str, Any]] = []

    def recorder(u: Universe, report: TickReport) -> None:
        novelty.record(u)
        construction.record(u)
        metrics_series.append(snapshot_metrics(u).as_dict())

    scheduler.add_recorder(recorder)
    scheduler.run(config.ticks)

    persistence = PersistenceTracker().spectrum(universe)
    oe = open_endedness_index(novelty, construction, window=novelty_window)

    return RunResult(
        config=config,
        metrics=metrics_series,
        novelty_new_per_tick=novelty.new_per_tick,
        novelty_cumulative=novelty.cumulative,
        depth_per_tick=construction.depth_per_tick,
        discovered_per_tick=construction.discovered_per_tick,
        persistence={
            "max_lifespan": persistence.max_lifespan,
            "mean_lifespan": persistence.mean_lifespan,
            "max_reformations": persistence.max_reformations,
            "reformed_fraction": persistence.reformed_fraction,
            "composed_persistent": persistence.composed_persistent,
            "reform_threshold": persistence.reform_threshold,
            "n_classes": len(persistence.lifespans),
        },
        open_endedness={
            "index": oe.index,
            "verdict": oe.verdict,
            "novelty_rate": oe.novelty_rate,
            "operator_rate": oe.operator_rate,
            "typical_depth": oe.typical_depth,
            "operator_growth": oe.operator_growth,
        },
        final_population=len(universe.organizations),
        final_classes_total=len(universe.class_registry),
    )
