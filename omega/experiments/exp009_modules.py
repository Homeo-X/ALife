"""Experiment 009 — Reusable deep modules. *Can a complex primitive become a
widely-reused building block, closing the pyramid's apex gap?*

Ω-0.6 found reuse forms a pyramid: shallow primitives are reused heavily (~18×)
while deep primitives stay **terminal** (~2.6×). The suspected cause is a
chicken-and-egg: a deep primitive must be abundant in the data pool to get reused,
but the toolkit (which selects by *current* reuse) is dominated by shallow
primitives, and the depth frontier feeds a deep symbol only briefly before moving
on. So deep primitives never get the exposure that would let them accumulate reuse.

exp009 breaks the loop with a **persistent deep-module pool**: the most-reused
primitives at depth ≥ ``module_min_depth`` are kept abundant in the feed
(``module_prob``), and — unlike the frontier — they are *not* superseded as depth
grows. A deep primitive thus gets sustained exposure and a fair chance to be reused
across many structures, with a positive feedback (reused → stays in the pool →
reused more).

Success criterion, read straight off the gauges: ``deep_mean_reuse`` (reuse of
depth-≥5 primitives) rises well above the ~2.6 baseline, i.e. genuinely reusable
deep modules emerge. A negative result — deep reuse stubbornly flat despite the
pool — would say the terminal-apex property is intrinsic to this substrate, not a
mere exposure artefact. This file measures which.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp004_reification import ReificationPhysics, _BASE_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp009")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    module_prob = float(overrides.get("module_prob", 0.5))
    module_min_depth = int(overrides.get("module_min_depth", 5))
    module_size = int(overrides.get("module_size", 32))
    # a little frontier feeding so deep primitives exist to be promoted at all
    frontier_prob = float(overrides.get("frontier_prob", 0.2))
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
        library_prob=float(overrides.get("library_prob", 0.0)),
        module_prob=module_prob,
        module_min_depth=module_min_depth,
        module_size=module_size,
    )
    cfg = Config(
        experiment="exp009",
        seed=seed,
        ticks=int(overrides.get("ticks", 3000)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"module_prob": module_prob, "module_min_depth": module_min_depth,
                "module_size": module_size, "frontier_prob": frontier_prob},
    )
    return physics, cfg
