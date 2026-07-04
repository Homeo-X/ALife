"""Experiment 010 — Copying capstone. *Can self-replication emerge, and what does
it do to open-endedness?*

The manifesto's central discipline: never implement a capability you can make
*emerge*. For reproduction that means — do not build a replicator; build a soup in
which duplication is a *possible move*, and ask whether a self-amplifying lineage
gets discovered.

The enabling condition (in the exp003 rewriting soup): with probability
``dup_prob`` a generated operator is a **template** whose replacement repeats its
pattern (p → p p). Applying it grows a copy of the matched unit. That is not a
replicator — a replicator is a *class the soup keeps rebuilding far faster than the
feed supplies it*. To detect exactly that, the kernel now separates each class's
births into **fed** (conjured from the reservoir) and **constructed** (built by
other organizations); ``Universe.amplification`` reports the maximum
constructed/(fed+1) — the top self-amplification.

Two questions, both interesting either way:

1. **Does amplification rise** when duplication is possible (`dup_prob > 0`) versus
   a matched control (`dup_prob = 0`)? Rising ⇒ the soup discovered a way to get
   itself rebuilt — the seed of copying.
2. **What does it cost open-endedness?** A replicator that takes over concentrates
   the population on itself (population *dominance* up, class diversity down). This
   experiment can therefore expose the tension the manifesto hints at: reproduction
   and open-ended novelty may pull against each other.

A negative result — amplification flat even with duplication enabled — is itself a
finding: this substrate does not spontaneously breed replicators, and reproduction
would have to be scaffolded rather than discovered.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp003_construction import ConstructionPhysics, _DATA_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp010")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    dup_prob = float(overrides.get("dup_prob", 0.3))
    op_feed_rate = int(overrides.get("op_feed_rate", 3))
    physics = ConstructionPhysics(
        meta_prob=float(overrides.get("meta_prob", 0.3)),
        max_len=int(overrides.get("max_len", 16)),
        dup_prob=dup_prob,
        op_feed_rate=op_feed_rate,
    )
    cfg = Config(
        experiment="exp010",
        seed=seed,
        ticks=int(overrides.get("ticks", 1500)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 150)),
        params={"dup_prob": dup_prob, "op_feed_rate": op_feed_rate},
    )
    return physics, cfg
