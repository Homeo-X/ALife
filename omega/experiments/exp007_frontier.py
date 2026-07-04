"""Experiment 007 — Frontier-focused reification. *Can concentrating recurrence on
the deepest primitives lift the depth ceiling without a breadth explosion?*

Ω-0.4 pinned down why hierarchy depth saturates (~12): the deepest primitives are
too **rare** in the data pool for the next level to recur and reify, and the naive
counter — lowering the recurrence bar — backfires, flooding the pool with *shallow*
primitives that make deep chains even rarer (a breadth/depth trade-off).

exp007 tries the mechanism Ω-0.4 pointed to instead: **keep the frontier abundant.**
A fraction ``frontier_prob`` of every fed symbol is drawn from the *frontier* — the
top ``frontier_band`` reification-depth levels — rather than uniformly over the
alphabet. This concentrates recurrence exactly where depth needs to grow, without
touching the recurrence bar, so it should deepen the hierarchy *without* the
shallow flood.

Judged fairly. Because Ω-0.4 showed count-based metrics are gameable by
relabelling, exp007 is scored with :mod:`omega.metrics.construction_quality`
(mean reification depth, depth-weighted total, deep-primitive fraction), not raw
primitive count. The prediction under test: versus the exp005 baseline, exp007
raises **max and mean depth** and the deep-primitive fraction, while *not* blowing
up primitive count the way ``depth_discount`` did. This file assumes none of that —
it is built to measure it.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp004_reification import ReificationPhysics, _BASE_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp007")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    # exp005's winning ratchet, plus frontier feeding. frontier_prob=0 recovers the
    # exp005 baseline exactly (the natural matched control).
    frontier_prob = float(overrides.get("frontier_prob", 0.5))
    frontier_band = int(overrides.get("frontier_band", 2))
    reify_max_len = int(overrides.get("reify_max_len", 6))
    physics = ReificationPhysics(
        reify=True,
        feed_reified=True,
        reify_threshold_nested=int(overrides.get("reify_threshold_nested", 2)),
        reify_threshold=int(overrides.get("reify_threshold", 4)),
        reify_max_len=reify_max_len,
        max_len=int(overrides.get("max_len", 2 * reify_max_len + 8)),
        meta_prob=float(overrides.get("meta_prob", 0.5)),
        frontier_prob=frontier_prob,
        frontier_band=frontier_band,
    )
    cfg = Config(
        experiment="exp007",
        seed=seed,
        ticks=int(overrides.get("ticks", 4000)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"frontier_prob": frontier_prob, "frontier_band": frontier_band,
                "reify_max_len": reify_max_len},
    )
    return physics, cfg
