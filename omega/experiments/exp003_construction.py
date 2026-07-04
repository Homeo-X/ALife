"""Experiment 003 — Organizations construct organizations. *Can novelty be
self-amplifying, and can the universe enlarge its own law set?*

This is the first experiment that reaches for Axiom 5 in earnest. The substrate
is a *constructive rewriting soup*:

* An organization is a string of atomic symbols. A string containing the
  delimiter ``>`` is an **operator**: the symbols before ``>`` are a pattern, the
  symbols after are a replacement. Everything else is **data**.
* The only interaction is *catalytic application*: an operator whose pattern
  occurs in a data string rewrites that string. The operator is not consumed (it
  is a catalyst); the data string is; the product is new.
* Crucially, an operator's replacement may itself contain ``>``. Applying such an
  operator to data yields a string that contains ``>`` — i.e. **a brand-new
  operator whose content was determined by the data it acted on.** The set of
  laws is not fixed; it is authored, at runtime, by the population.

A steady feed of random data keeps substrate available (a chemostat). Conservation
still binds: a rewrite that lengthens a string must pay for the extra
distinguishability out of the reservoir, so growth competes for a finite budget.

Predicted readings, in contrast to exp001's noise: novelty stays positive *and*
is accompanied by a growing count of **discovered operators** (new organizational
laws). That operator growth is the open-endedness signal exp001 cannot fake —
verdict OPEN-ENDED (law set growing). What this experiment does *not* yet produce
is deep compositional hierarchy (strings stay shallow); that gap is the explicit
motivation for exp004+.
"""
from __future__ import annotations

from typing import Sequence

from omega.config import Config
from omega.experiments.registry import register
from omega.kernel.organization import Organization, State
from omega.kernel.transform import Physics, Reaction, Transform
from omega.kernel.universe import Universe
from omega.substrate.gradient import reservoir_pressure
from omega.substrate.noise import Noise

_DELIM = ">"
_DATA_ALPHABET = "abcd"


# ---- operator utilities ---------------------------------------------------
def is_operator(state: State) -> bool:
    return _DELIM in state


def split_operator(state: State) -> tuple[tuple, tuple]:
    idx = state.index(_DELIM)
    return state[:idx], state[idx + 1:]


def _find(pattern: tuple, data: tuple) -> int:
    n, m = len(data), len(pattern)
    if m == 0 or m > n:
        return -1
    for i in range(n - m + 1):
        if data[i:i + m] == pattern:
            return i
    return -1


def apply_rewrite(pattern: tuple, replacement: tuple, data: tuple) -> tuple | None:
    i = _find(pattern, data)
    if i < 0:
        return None
    return data[:i] + tuple(replacement) + data[i + len(pattern):]


def _kind_of(state: State) -> str:
    return "operator" if is_operator(state) else "data"


def make_transform(op_state: State) -> Transform:
    """Turn an operator organization into a genuine, usable Transform.

    These populate the universe's discovered-law registry: each distinct operator
    class that appears becomes a first-class law, documenting the universe
    enlarging its own possibility space.
    """
    pattern, replacement = split_operator(op_state)

    def fn(inputs: Sequence[Organization], rng: Noise):
        if len(inputs) != 1:
            return None
        product = apply_rewrite(pattern, replacement, inputs[0].state)
        if product is None:
            return None
        return ((product, _kind_of(product)),)

    from omega.kernel.organization import canonical_cls
    return Transform(name=f"op:{''.join(map(str, op_state))}", arity=1, fn=fn,
                     catalytic=True, discovered=True, origin_cls=canonical_cls(op_state))


# ---- the physics ----------------------------------------------------------
class ConstructionPhysics:
    name = "exp003_construction"

    def __init__(self, data_alphabet: str = _DATA_ALPHABET, feed_rate: int = 12,
                 apply_attempts: int = 60, n_seed_operators: int = 12,
                 meta_prob: float = 0.5, max_len: int = 10, dup_prob: float = 0.0,
                 op_feed_rate: int = 0) -> None:
        self.data_alphabet = data_alphabet
        self.feed_rate = feed_rate
        self.apply_attempts = apply_attempts
        self.n_seed_operators = n_seed_operators
        self.meta_prob = meta_prob
        self.max_len = max_len
        self.op_feed_rate = op_feed_rate  # fresh operators fed per tick (keeps
        #                                   duplicators available against decay)
        # Copying capstone (exp010) enabling condition: with probability dup_prob a
        # generated operator is a *template* whose replacement DUPLICATES its
        # pattern (p -> p p). This does not implement self-replication — it only
        # makes duplication a *possible* move the soup may or may not exploit. The
        # question is whether an actual self-amplifying replicator gets discovered.
        self.dup_prob = dup_prob
        self._known_ops: set[str] = set()  # operator classes already registered

    # -- seeding --
    def _random_data(self, rng: Noise, lo: int = 2, hi: int = 5) -> tuple:
        length = rng.randint(lo, hi)
        return tuple(rng.symbol(self.data_alphabet) for _ in range(length))

    def _random_operator(self, rng: Noise) -> tuple:
        p_len = rng.randint(1, 2)
        pattern = [rng.symbol(self.data_alphabet) for _ in range(p_len)]
        # duplication (template) operator: replacement repeats the pattern -> the
        # applied string grows a copy of the matched unit. A possible move, not a
        # replicator by itself.
        if rng.random() < self.dup_prob:
            return tuple(pattern) + (_DELIM,) + tuple(pattern) + tuple(pattern)
        r_len = rng.randint(1, 3)
        replacement = [rng.symbol(self.data_alphabet) for _ in range(r_len)]
        # with probability meta_prob, make this a *meta* operator whose products
        # will themselves be operators (embed a delimiter in the replacement)
        if rng.random() < self.meta_prob:
            pos = rng.randint(0, len(replacement))
            replacement = replacement[:pos] + [_DELIM] + replacement[pos:]
        return tuple(pattern) + (_DELIM,) + tuple(replacement)

    def seed(self, universe: Universe, rng: Noise) -> None:
        for _ in range(self.n_seed_operators):
            universe.spawn(self._random_operator(rng), kind="operator")
        for _ in range(self.feed_rate * 3):
            universe.spawn(self._random_data(rng), kind="data")
        # seed operators are the baseline law set — not counted as "discovered"
        for op in universe.organizations.values():
            if op.kind == "operator":
                self._known_ops.add(op.cls)

    # -- per-tick proposal --
    def propose(self, universe: Universe, rng: Noise):
        reactions: list[Reaction] = []

        # 1) chemostat: feed random data, throttled by scarcity
        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        for _ in range(max(budget, 1)):
            reactions.append(Reaction(inputs=(), consume=(),
                                      outputs=((self._random_data(rng), "data"),), via="feed"))
        # optional operator feed (keeps duplication operators available)
        for _ in range(self.op_feed_rate):
            reactions.append(Reaction(inputs=(), consume=(),
                                      outputs=((self._random_operator(rng), "operator"),), via="feed"))

        # 2) catalytic application of operators to data
        operators = [o for o in universe.organizations.values() if o.kind == "operator"]
        data = [o for o in universe.organizations.values() if o.kind == "data"]
        if operators and data:
            for _ in range(self.apply_attempts):
                op = rng.choice(operators)
                d = rng.choice(data)
                pattern, replacement = split_operator(op.state)
                product = apply_rewrite(pattern, replacement, d.state)
                if product is None or len(product) > self.max_len:
                    continue
                reactions.append(Reaction(
                    inputs=(op.uid, d.uid), consume=(d.uid,),  # operator is catalytic
                    outputs=((product, _kind_of(product)),),
                    via=f"apply:{''.join(map(str, op.state))}"))

        # 3) register any newly-appeared operator class as a discovered law
        for o in operators:
            if o.cls not in self._known_ops:
                self._known_ops.add(o.cls)
                universe.register_transform(make_transform(o.state))

        # 4) publish the top self-amplification and population dominance (copying
        #    capstone signals): dominance = largest class's share of the population,
        #    which rises if a replicator takes the soup over.
        amp, _ = universe.amplification()
        universe.gauges["amplification"] = amp
        pop = universe.class_population()
        total = sum(pop.values())
        universe.gauges["dominance"] = (max(pop.values()) / total) if total else 0.0

        return reactions


@register("exp003")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    # meta_prob is the operative knob: with meta_prob=0 no operator can ever
    # author an operator, so the law set is frozen at the seeds (the matched
    # control that tests whether meta-operator authoring is the mechanism).
    meta_prob = float(overrides.get("meta_prob", 0.5))
    max_len = int(overrides.get("max_len", 10))
    cfg = Config(
        experiment="exp003",
        seed=seed,
        ticks=int(overrides.get("ticks", 400)),
        total_quanta=int(overrides.get("total_quanta", 3000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"data_alphabet": _DATA_ALPHABET, "meta_prob": meta_prob, "max_len": max_len},
    )
    return ConstructionPhysics(meta_prob=meta_prob, max_len=max_len), cfg
