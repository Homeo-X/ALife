"""Experiment 011 — Function. *If organizations are selected for what they DO, does
a functional ecology emerge?*

Ω-0.7 found the substrate's wall: it selects on *form* (re-formation of a shape),
never on *function* (behaviour). Both the deep-reuse and copying walls trace to
that absence. This experiment introduces function in the least-committal way the
manifesto allows — not a fitness target, but a *condition*:

    **Use it or lose it.** An operator's decay hazard falls with its recent
    activity (successful participations). Operators that find substrate to act on
    persist; idle operators decay at the base rate. Data still decays uniformly.

No goal is imposed. Selection is purely for *doing something with what is
available*. Because operators also *produce* the substrate other operators feed
on, the pressure is frequency-dependent and can coevolve — the substrate selects
operator function, and operator function reshapes the substrate.

This is enabled by a kernel generalisation: decay was never part of the immutable
kernel (Identity / Consistency / Causality / Conservation are), so a Physics may
make it depend on the organization. ``FunctionalConstructionPhysics.hazard`` is
that dependence.

Questions (with a matched ``functional=False`` control that reverts to uniform
decay): does the surviving operator population become *enriched for activity*
(selection working)? Does it *specialise* to the available substrate (shorter,
more-often-matching patterns)? And does functional selection help or hurt
open-endedness? Built to measure.
"""
from __future__ import annotations

import math

from omega.config import Config
from omega.experiments.exp003_construction import ConstructionPhysics, _DATA_ALPHABET
from omega.experiments.exp003_construction import split_operator
from omega.experiments.registry import register
from omega.kernel.transform import Physics


class FunctionalConstructionPhysics(ConstructionPhysics):
    """Operator persistence coupled to function. Two definitions of "function":

    * ``mode="participation"`` — activity = you matched some substrate. Ω-0.8 showed
      this selects for promiscuous generalists, not usefulness.
    * ``mode="value"`` — an operator earns *value* only when its product is **novel
      and survives** (it generated lasting new structure). Value decays, so an
      operator must keep being generative to persist. This is function as
      *contribution to persistent novelty*, not mere activity.
    """

    def __init__(self, functional: bool = True, mode: str = "value",
                 activity_gain: float = 1.5, value_gain: float = 1.5,
                 min_hazard_frac: float = 0.05, value_decay: float = 0.9, **kw) -> None:
        super().__init__(**kw)
        self.functional = functional
        self.mode = mode
        self.activity_gain = activity_gain
        self.value_gain = value_gain
        self.min_hazard_frac = min_hazard_frac
        self.value_decay = value_decay
        self._value: dict[int, float] = {}   # per-operator generativity value
        self._seen: set = set()              # product classes ever seen
        self._rel_mark: int = 0              # relations processed watermark

    def _credit_generativity(self, universe) -> None:
        """Reward operators whose recent products were novel and still survive."""
        rels = universe.relations
        for rel in rels[self._rel_mark:]:
            if not rel.via.startswith("apply:"):
                continue
            src = universe.organizations.get(rel.source)
            tgt = universe.organizations.get(rel.target)
            if src is None or src.kind != "operator" or tgt is None:
                continue  # operator gone, or product already decayed (no value)
            cls = tgt.cls
            if cls not in self._seen:            # a *novel* surviving product
                self._seen.add(cls)
                self._value[rel.source] = self._value.get(rel.source, 0.0) + 1.0
        self._rel_mark = len(rels)

    def hazard(self, org, stats, base: float) -> float:
        if not self.functional or org.kind != "operator":
            return base
        if self.mode == "value":
            v = self._value.get(org.uid, 0.0)
            return max(base * self.min_hazard_frac, base * math.exp(-self.value_gain * v))
        act = stats.recent_activity if stats is not None else 0.0
        return max(base * self.min_hazard_frac, base * math.exp(-self.activity_gain * act))

    def propose(self, universe, rng):
        # value mode: credit generativity from last tick's surviving novel products,
        # then leak values (a operator must keep generating to stay valuable)
        if self.functional and self.mode == "value":
            self._credit_generativity(universe)
            live = universe.organizations
            self._value = {u: v * self.value_decay for u, v in self._value.items()
                           if u in live and v * self.value_decay > 1e-3}
        reactions = super().propose(universe, rng)
        # publish a functional-selection read-out: mean activity & mean pattern
        # length of the surviving operators (specialisation signal)
        ops = [(o, universe.stats.get(o.uid)) for o in universe.organizations.values()
               if o.kind == "operator"]
        if ops:
            acts = [st.recent_activity for _, st in ops if st is not None]
            plens = []
            for o, _ in ops:
                try:
                    plens.append(len(split_operator(o.state)[0]))
                except ValueError:
                    pass
            universe.gauges["op_mean_activity"] = sum(acts) / len(acts) if acts else 0.0
            universe.gauges["op_mean_pattern_len"] = sum(plens) / len(plens) if plens else 0.0
            universe.gauges["op_count"] = float(len(ops))
            # fraction of the operator population that is currently *functional*
            # (has acted recently). Functional selection should keep this high by
            # pruning the idle; the control lets idle operators accumulate.
            universe.gauges["op_active_fraction"] = (
                sum(1 for a in acts if a > 0.5) / len(acts)) if acts else 0.0
            universe.gauges["op_valued_fraction"] = (
                sum(1 for o, _ in ops if self._value.get(o.uid, 0) > 0.5) / len(ops))
        return reactions


@register("exp011")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    functional = bool(overrides.get("functional", True))
    physics = FunctionalConstructionPhysics(
        functional=functional,
        mode=str(overrides.get("mode", "value")),
        activity_gain=float(overrides.get("activity_gain", 1.5)),
        meta_prob=float(overrides.get("meta_prob", 0.4)),
        max_len=int(overrides.get("max_len", 14)),
        op_feed_rate=int(overrides.get("op_feed_rate", 6)),
        n_seed_operators=int(overrides.get("n_seed_operators", 20)),
    )
    cfg = Config(
        experiment="exp011",
        seed=seed,
        ticks=int(overrides.get("ticks", 1500)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.05)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 150)),
        params={"functional": functional, "activity_gain": 0.6},
    )
    return physics, cfg
