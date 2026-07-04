"""Construction quality — novelty you cannot fake by relabelling.

Ω-0.4 exposed a hole in the scorecard: a permissive reification bar mints a flood
of *shallow* primitives (9990 of them) that inflates every count-based metric while
producing almost no hierarchy. Raw primitive count, and even the operator-discovery
rate, are therefore gameable by relabelling.

This metric closes the hole by weighting novelty by **depth**. It reads the
reification depth distribution a Physics publishes into ``universe.gauges`` and
returns:

* ``mean_depth``      — how deep the *typical* primitive is. A shallow flood scores
                        ~1–2 no matter how many primitives it mints; a true ratchet
                        scores high. This is the single best quality scalar.
* ``depth_weighted``  — Σ depth over all primitives. Rewards count *and* depth, so
                        it rises only when you add primitives that are actually deep.
* ``deep_fraction``   — share of primitives at depth ≥ 5. Directly the "is this
                        cumulative construction or churn" question.

A physics that does not reify simply reports zeros — the metric is meaningful
wherever the gauges exist and inert elsewhere.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True)
class ConstructionQuality:
    n_primitives: int
    max_depth: float
    mean_depth: float
    depth_weighted: float
    deep_primitives: int
    deep_fraction: float

    def summary(self) -> str:
        return (
            f"primitives={self.n_primitives} max_depth={self.max_depth:.0f} "
            f"mean_depth={self.mean_depth:.2f} depth_weighted={self.depth_weighted:.0f} "
            f"deep(>=5)={self.deep_primitives} ({self.deep_fraction:.2f})"
        )


def construction_quality(final_gauges: Mapping[str, float], n_primitives: int) -> ConstructionQuality:
    """Build the quality summary from a run's final gauge dict and primitive count."""
    max_depth = float(final_gauges.get("reify_depth", 0.0))
    mean_depth = float(final_gauges.get("reify_depth_mean", 0.0))
    depth_weighted = float(final_gauges.get("reify_depth_weighted", 0.0))
    deep = int(final_gauges.get("deep_primitives", 0.0))
    frac = (deep / n_primitives) if n_primitives else 0.0
    return ConstructionQuality(
        n_primitives=n_primitives,
        max_depth=max_depth,
        mean_depth=mean_depth,
        depth_weighted=depth_weighted,
        deep_primitives=deep,
        deep_fraction=frac,
    )
