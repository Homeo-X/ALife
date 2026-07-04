"""Experiment 005 — The cumulative nesting ratchet.

This experiment started from a hypothesis that turned out to be **wrong**, and the
falsification is the interesting part. Ω-0.2 saw exp004's discovery rate decline
mildly over long horizons and blamed *dilution*: a random feed over a growing
alphabet makes any given motif recur less often. The proposed fix was to feed only
base symbols (``feed_reified=False``), so reified symbols would enter data only via
construction.

A 2x2 factorial over the two knobs (``feed_reified`` x ``reify_threshold_nested``)
at 4000 ticks demolished that hypothesis:

    feedR=T, nest=4 (exp004):  ops/1k = [193, 64, 58, 58]     depth  6   OPEN-ENDED
    feedR=T, nest=2:           ops/1k = [424,194,190,174]     depth 12   OPEN-ENDED
    feedR=F, nest=4:           ops/1k = [324,  0,  0,  0]     depth  1   CONVERGED
    feedR=F, nest=2:           ops/1k = [346,  0,  0,  0]     depth  2   CONVERGED

The "fix" (``feed_reified=False``) **froze the universe completely** after the
first window. Feeding reified symbols back into the data pool is not the *cause* of
dilution — it is the *essential fuel* for the ratchet: a higher-order motif can
only recur (and thus be reified) if its reified components are abundant in the data,
and construction alone does not keep them abundant enough.

The real lever is the **nesting ratchet**: lowering the recurrence bar for motifs
that already contain a reified symbol (``reify_threshold_nested`` < base). That one
change roughly triples the sustained discovery rate and doubles lineage depth,
because it lets primitives-built-from-primitives form freely. Over 8000 ticks the
winning config sustains ~150 new operators / 1000 ticks with a stable reservoir
and a lineage depth that ratchets to ~13 (then plateaus at a structure-length
ceiling while breadth keeps growing) — the most sustained open-endedness in the
program, and the first with demonstrably *cumulative* (deeply nested) structure.

So exp005's canonical form IS the winning arm (``feed_reified=True``,
``reify_threshold_nested=2``); the frozen ``feed_reified=False`` arm is retained as
a runnable control that documents the falsified hypothesis.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp004_reification import ReificationPhysics, _BASE_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp005")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    reify = bool(overrides.get("reify", True))
    meta_prob = float(overrides.get("meta_prob", 0.5))
    # canonical exp005 = the winning arm of the factorial. Feeding reified symbols
    # back (feed_reified=True) fuels the ratchet; the low nested bar drives it.
    feed_reified = bool(overrides.get("feed_reified", True))
    reify_threshold = int(overrides.get("reify_threshold", 4))
    reify_threshold_nested = int(overrides.get("reify_threshold_nested", 2))
    cfg = Config(
        experiment="exp005",
        seed=seed,
        ticks=int(overrides.get("ticks", 2000)),
        total_quanta=int(overrides.get("total_quanta", 3000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={
            "base_alphabet": _BASE_ALPHABET,
            "reify": reify,
            "meta_prob": meta_prob,
            "feed_reified": feed_reified,
            "reify_threshold": reify_threshold,
            "reify_threshold_nested": reify_threshold_nested,
        },
    )
    physics = ReificationPhysics(
        reify=reify, meta_prob=meta_prob, feed_reified=feed_reified,
        reify_threshold=reify_threshold, reify_threshold_nested=reify_threshold_nested,
    )
    return physics, cfg
