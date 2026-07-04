"""Experiment 008 — Toolkit feeding for a *rich* (heavily-reused) hierarchy.

exp007 gave depth. Measuring the reification DAG then showed something more subtle:
the DAG is *already* highly combinatorial (82-99% of reifications fuse >=2 reified
primitives — recombination, not a thin ladder), but **reuse is modest** (a primitive
is reused as a component only ~2.4 times on average), and frontier feeding actually
*lowers* peak reuse: racing depth-ward, it uses each primitive a few times before
the frontier moves on, so no stable, heavily-reused core forms.

Rich cumulative systems — technology, biology, language — are not just deep; they
reuse a *core toolkit* of primitives thousands of times. exp008 tests a mechanism
aimed at that: keep the **most-reused** primitives abundant in the feed (the
emergent toolkit), by analogy to how exp007 kept the *deepest* abundant. This sets
up a positive feedback — a useful primitive is fed more, so it is recombined more,
so it is reused more — that should thicken the DAG.

Knobs: ``library_prob`` (chance a fed symbol is drawn from the toolkit) and
``library_size`` (how many top-reuse primitives count as the toolkit). It composes
with ``frontier_prob``, so depth and reuse can be pursued together.

Scored on the DAG-richness gauges (``mean_reuse``, ``max_reuse``,
``combinatorial_fraction``) alongside depth quality. The prediction under test:
toolkit feeding raises mean/peak reuse over both the baseline and pure-frontier
runs — a richer DAG — ideally without sacrificing all the depth. Built to measure,
not to assume.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp004_reification import ReificationPhysics, _BASE_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp008")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    library_prob = float(overrides.get("library_prob", 0.5))
    library_size = int(overrides.get("library_size", 16))
    frontier_prob = float(overrides.get("frontier_prob", 0.0))
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
        frontier_band=int(overrides.get("frontier_band", 2)),
        library_prob=library_prob,
        library_size=library_size,
    )
    cfg = Config(
        experiment="exp008",
        seed=seed,
        ticks=int(overrides.get("ticks", 4000)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"library_prob": library_prob, "library_size": library_size,
                "frontier_prob": frontier_prob, "reify_max_len": reify_max_len},
    )
    return physics, cfg
