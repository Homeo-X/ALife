"""Experiment 006 — What sets the hierarchy-depth ceiling?

exp005's cumulative ratchet reached reification lineage depth ~13 and then
plateaued. Ω-0.3 attributed the plateau to a **structure-length ceiling**
(``reify_max_len=4``, ``max_len=10``). This experiment tests that attribution
directly by sweeping the length caps and measuring where depth plateaus.

Two hypotheses:

* **H-length (the Ω-0.3 guess).** Depth is bounded by how long structures may be.
  Raising ``reify_max_len`` should raise the depth plateau roughly in step.
* **H-rarity (the structural counter-argument).** A length-L structure needs only
  *one* deep child to increment depth, so length does not directly cap depth. The
  real throttle is that the deepest primitives become *rare* in the data pool, so
  motifs that contain them cross the recurrence bar ever less often, and depth
  saturates almost regardless of the length cap.

The prediction of H-rarity is uncomfortable but sharp: raising the caps will
*not* buy much depth. If the sweep shows the plateau roughly flat across
``reify_max_len``, the length-ceiling story is wrong and unbounded hierarchy needs
a mechanism that keeps deep primitives abundant — motivating exp007.

``max_len`` is scaled with ``reify_max_len`` so that string length is never the
binding constraint, isolating the reified-structure cap as the variable under
study.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.exp004_reification import ReificationPhysics, _BASE_ALPHABET
from omega.experiments.registry import register
from omega.kernel.transform import Physics


@register("exp006")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    # Canonical settings are exp005's winning ratchet; the swept variable is the
    # reified-structure length cap. max_len is kept generously above it so raw
    # string length is not the binding constraint.
    reify_max_len = int(overrides.get("reify_max_len", 8))
    max_len = int(overrides.get("max_len", 2 * reify_max_len + 8))
    physics = ReificationPhysics(
        reify=True,
        feed_reified=True,
        reify_threshold_nested=int(overrides.get("reify_threshold_nested", 2)),
        reify_threshold=int(overrides.get("reify_threshold", 4)),
        reify_max_len=reify_max_len,
        max_len=max_len,
        meta_prob=float(overrides.get("meta_prob", 0.5)),
        depth_discount=bool(overrides.get("depth_discount", False)),
    )
    cfg = Config(
        experiment="exp006",
        seed=seed,
        ticks=int(overrides.get("ticks", 4000)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"reify_max_len": reify_max_len, "max_len": max_len,
                "reify_threshold_nested": 2},
    )
    return physics, cfg
