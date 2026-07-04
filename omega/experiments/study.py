"""Multi-seed studies — turning single runs into evidence.

A single deterministic run tells a story; a *study* tells you whether the story
holds. This module runs an experiment across many seeds, aggregates the
open-endedness signals with mean +/- std, and adds two diagnostics the
single-run harness cannot give:

* **saturation** — comparing the novel-class rate in an early window vs a late
  window of the *same* run. A universe that is genuinely open-ended keeps the
  late rate up; one that is merely exploring a finite set has late << early.
* **operator plateau** — whether the discovered-operator count is still climbing
  at the end of the run or has flattened.

These are exactly what the falsification conditions in the research log require.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from statistics import fmean, pstdev
from typing import Any

from omega.experiments.harness import RunResult, run
from omega.experiments.registry import get_experiment


def _window_rate(series: list[int], lo_frac: float, hi_frac: float) -> float:
    """Mean of ``series`` over the fractional window [lo_frac, hi_frac)."""
    if not series:
        return 0.0
    n = len(series)
    lo, hi = int(lo_frac * n), max(int(hi_frac * n), int(lo_frac * n) + 1)
    seg = series[lo:hi]
    return fmean(seg) if seg else 0.0


@dataclass
class RunSummary:
    seed: int
    oei_index: float
    verdict: str
    operator_growth: int              # cumulative (context only)
    operator_rate: float              # sustained discovery rate (the real signal)
    novelty_rate_late: float          # mean new classes/tick, last 10% of run
    novelty_rate_early: float         # mean new classes/tick, 10-20% of run
    saturation: float                 # late/early in (0,1]; ~1 sustained, ~0 closed
    operator_plateaued: bool          # operator count flat over final third
    composed_persistent: int
    classes_ever: int

    @classmethod
    def from_result(cls, seed: int, r: RunResult) -> "RunSummary":
        oe = r.open_endedness
        early = _window_rate(r.novelty_new_per_tick, 0.1, 0.2)
        late = _window_rate(r.novelty_new_per_tick, 0.9, 1.0)
        sat = (late / early) if early > 1e-9 else 0.0
        ops = r.discovered_per_tick
        if ops:
            mid = ops[len(ops) * 2 // 3]
            plateaued = (ops[-1] - mid) <= 0
        else:
            plateaued = True
        return cls(
            seed=seed,
            oei_index=oe["index"],
            verdict=oe["verdict"],
            operator_growth=oe["operator_growth"],
            operator_rate=oe.get("operator_rate", 0.0),
            novelty_rate_late=late,
            novelty_rate_early=early,
            saturation=min(sat, 1.0),
            operator_plateaued=plateaued,
            composed_persistent=r.persistence["composed_persistent"],
            classes_ever=r.final_classes_total,
        )


@dataclass
class StudyReport:
    experiment: str
    overrides: dict[str, Any]
    n_seeds: int
    runs: list[RunSummary]

    def _agg(self, attr: str) -> tuple[float, float]:
        vals = [getattr(s, attr) for s in self.runs]
        return (fmean(vals), pstdev(vals) if len(vals) > 1 else 0.0)

    def summary(self) -> str:
        oei_m, oei_s = self._agg("oei_index")
        og_m, og_s = self._agg("operator_growth")
        or_m, or_s = self._agg("operator_rate")
        sat_m, sat_s = self._agg("saturation")
        early_m, _ = self._agg("novelty_rate_early")
        late_m, _ = self._agg("novelty_rate_late")
        cp_m, cp_s = self._agg("composed_persistent")
        verdicts = {}
        for s in self.runs:
            key = s.verdict.split(" (")[0]
            verdicts[key] = verdicts.get(key, 0) + 1
        plateau = sum(s.operator_plateaued for s in self.runs)
        ov = ", ".join(f"{k}={v}" for k, v in self.overrides.items()) or "(defaults)"
        lines = [
            f"[{self.experiment}] {ov}  n={self.n_seeds}",
            f"  OEI                 {oei_m:.4f} +/- {oei_s:.4f}",
            f"  operator_rate(late) {or_m:.4f} +/- {or_s:.4f}   <-- open-endedness gate",
            f"  operator_total      {og_m:.1f} +/- {og_s:.1f}   (plateaued in {plateau}/{self.n_seeds})",
            f"  novelty early->late {early_m:.3f} -> {late_m:.3f}   saturation={sat_m:.3f} +/- {sat_s:.3f}",
            f"  composed_persistent {cp_m:.1f} +/- {cp_s:.1f}",
            f"  verdicts            {verdicts}",
        ]
        return "\n".join(lines)


def run_study(experiment: str, seeds: list[int], **overrides) -> StudyReport:
    runs: list[RunSummary] = []
    for seed in seeds:
        physics, cfg = get_experiment(experiment)(seed=seed, **overrides)
        result = run(physics, cfg)
        runs.append(RunSummary.from_result(seed, result))
    return StudyReport(experiment=experiment, overrides=dict(overrides),
                       n_seeds=len(seeds), runs=runs)
