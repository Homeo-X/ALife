"""The Open-Endedness Index — the project's top-line falsifiable metric.

**Revised in Ω-0.2 after the v0.1 index gave a false positive.** The original
index gated on *cumulative* operator growth, so a universe that discovered a
finite burst of operators and then froze scored as OPEN-ENDED. It was not: over
long horizons its novelty collapsed and its operator set never grew again. The
lesson: open-endedness is a statement about *rates that persist*, never about
totals accumulated.

Two more hard-won points shape this version:

* **Novelty alone is not trustworthy here.** Every experiment with a random feed
  (001 and 003 both have one) shows a positive new-class rate forever, because the
  feed keeps injecting never-seen noise. So a nonzero novelty rate does *not*
  imply open-endedness — noise fakes it (exp001 is the proof). Novelty is kept
  only as a *necessary* condition (zero novelty ⇒ dead), not a sufficient one.

* **The trustworthy signal is a sustained rate of new organizational laws.**
  ``ConstructionTracker.recent_operator_rate`` measures whether the universe is
  *still* authoring operators at the end of the run. That is the thing that must
  not decay for the possibility space to keep enlarging.

The index therefore gates on the recent operator-discovery rate, uses recent
novelty only as a liveness floor, and treats depth as a bonus.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from omega.emergence.construction import ConstructionTracker
from omega.emergence.novelty import NoveltyTracker


@dataclass
class OpenEndednessReport:
    novelty_rate: float
    operator_rate: float          # NEW: sustained operator-discovery rate (the gate)
    operator_growth: int          # cumulative, kept for context only
    typical_depth: float
    index: float
    verdict: str

    def summary(self) -> str:
        return (
            f"OEI={self.index:.4f} [{self.verdict}]  "
            f"op_rate={self.operator_rate:.4f} "
            f"novelty_rate={self.novelty_rate:.4f} "
            f"depth={self.typical_depth:.2f} op_total={self.operator_growth}"
        )


def _saturate(x: float, scale: float) -> float:
    """Map [0, inf) -> [0, 1) smoothly; keeps the index bounded and comparable."""
    return 1.0 - math.exp(-x / scale)


def open_endedness_index(
    novelty: NoveltyTracker,
    construction: ConstructionTracker,
    *,
    window: int = 50,
    op_rate_scale: float = 0.05,
    depth_scale: float = 3.0,
    novelty_floor: float = 1e-2,
    op_rate_dead: float = 5e-3,  # > ~3 new laws per (scaled) window ⇒ still growing
) -> OpenEndednessReport:
    nr = novelty.recent_rate(window)
    op_rate = construction.recent_operator_rate(window)
    op_total = construction.operator_growth
    depth = construction.depth_per_tick[-1] if construction.depth_per_tick else 0

    # Gate on sustained operator discovery; require novelty to be alive at all;
    # let depth add a bonus. If either gate fails the index collapses.
    alive = 1.0 if nr >= novelty_floor else 0.0
    f_ops = _saturate(op_rate, op_rate_scale)
    f_depth = 0.5 + 0.5 * _saturate(depth, depth_scale)
    index = alive * f_ops * f_depth

    if op_rate >= op_rate_dead:
        verdict = "OPEN-ENDED (law set still growing)"
    elif nr < novelty_floor:
        verdict = "CONVERGED (finite class set, novelty extinguished)"
    elif op_total > 0:
        verdict = "CLOSED (law set froze after a finite burst)"
    else:
        verdict = "CHURNING (novelty is noise; no laws discovered)"

    return OpenEndednessReport(
        novelty_rate=nr,
        operator_rate=op_rate,
        operator_growth=op_total,
        typical_depth=float(depth),
        index=index,
        verdict=verdict,
    )
