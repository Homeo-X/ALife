"""Experiment 004 — Reification. *Can promoting persistent structure to new
primitives defeat the closure that killed exp003?*

Ω-0.2 established (honestly, against my earlier claim) that exp003 is **not**
open-ended: with a fixed finite alphabet and a length ceiling, the set of possible
operators is finite, so the universe discovers a finite burst of them and freezes.
Closure is not an accident there; it is forced by a bounded possibility space.

The only way a *finite-material* universe can keep discovering genuinely new
organization is for its **space of possibilities to keep enlarging**. This
experiment tests one concrete mechanism for that, and it is exactly Axiom 5
("organizations may create organizations that were impossible before"):

    **Reification.** When a composed organization becomes reliably persistent
    (re-formed many times), mint a brand-new atomic symbol that *names* it and add
    that symbol to the alphabet. Every later feed and operator may now use the new
    primitive — so structures and operators that were literally unconstructible
    before now exist. A reified symbol can itself appear inside a later reified
    structure, giving an unbounded ladder of primitives (atoms -> motifs -> motifs
    of motifs -> ...).

Reification is also *conservation-efficient*: folding a k-symbol structure into a
single symbol returns k-1 quanta to the reservoir, so compressing a common motif
relieves scarcity and funds further construction. Self-maintenance advantage falls
out of the resource gradient rather than being programmed.

**Design as a controlled test.** ``reify=True`` is the treatment; ``reify=False``
is a matched control that is exactly exp003's dynamics (it should freeze). The
prediction under test: the treatment keeps ``operator_rate`` above zero and grows
its alphabet without bound over long horizons, while the control freezes. This
file does not assume that outcome — it is what the study is run to find out.
"""
from __future__ import annotations

from typing import Sequence

from omega.config import Config
from omega.experiments.registry import register
from omega.experiments.exp003_construction import (
    apply_rewrite, is_operator, make_transform, split_operator, _kind_of, _DELIM,
)
from omega.kernel.organization import canonical_cls
from omega.kernel.transform import Physics, Reaction, Transform
from omega.kernel.universe import Universe
from omega.substrate.gradient import reservoir_pressure
from omega.substrate.noise import Noise

_BASE_ALPHABET = "abc"


class ReificationPhysics:
    name = "exp004_reification"

    def __init__(self, reify: bool = True, feed_rate: int = 12, apply_attempts: int = 60,
                 n_seed_operators: int = 10, meta_prob: float = 0.5, max_len: int = 10,
                 reify_threshold: int = 4, reify_max_len: int = 4,
                 reify_per_tick: int = 2, feed_reified: bool = True,
                 reify_threshold_nested: int | None = None,
                 depth_discount: bool = False,
                 frontier_prob: float = 0.0, frontier_band: int = 2,
                 library_prob: float = 0.0, library_size: int = 16,
                 module_prob: float = 0.0, module_min_depth: int = 5,
                 module_size: int = 32) -> None:
        self.reify = reify
        self.feed_rate = feed_rate
        self.apply_attempts = apply_attempts
        self.n_seed_operators = n_seed_operators
        self.meta_prob = meta_prob
        self.max_len = max_len
        self.reify_threshold = reify_threshold
        self.reify_max_len = reify_max_len
        self.reify_per_tick = reify_per_tick
        # exp006 knob: counteract deep-symbol rarity by lowering the recurrence bar
        # for deeper motifs (bar shrinks by one per level of child depth). Tests
        # whether the depth plateau is a rarity equilibrium — if so this lifts it.
        self.depth_discount = depth_discount
        # exp005 knobs (behavior-preserving defaults keep exp004 exactly as-was):
        #   feed_reified=False   -> random feed uses only base symbols, so reified
        #                           symbols enter data only via construction (this
        #                           decouples reification from feed dilution).
        #   reify_threshold_nested -> a (usually lower) recurrence bar for motifs
        #                           that already contain a reified symbol, to
        #                           actively drive cumulative nesting (ratcheting).
        self.feed_reified = feed_reified
        self.reify_threshold_nested = (reify_threshold if reify_threshold_nested is None
                                       else reify_threshold_nested)
        # exp007 knobs: keep the DEEPEST primitives abundant in the feed so the top
        # of the hierarchy can keep advancing. frontier_prob is the chance a fed
        # symbol is drawn from the frontier (the top `frontier_band` depth levels)
        # instead of uniformly. This concentrates recurrence on the frontier rather
        # than loosening the bar globally (which Ω-0.4 showed just floods breadth).
        self.frontier_prob = frontier_prob
        self.frontier_band = frontier_band
        # exp008 knob: keep the most-REUSED primitives (an emergent "toolkit")
        # abundant, so useful building blocks get recombined more — a positive
        # feedback aimed at a rich, heavily-reused DAG rather than a deep-but-thin
        # one. Selects by reuse, where frontier_prob selects by depth.
        self.library_prob = library_prob
        self.library_size = library_size
        self._library: list[str] = []
        # exp009 knob: a persistent "deep-module pool" — keep the most-reused
        # *deep* primitives (depth >= module_min_depth) abundant in the feed so a
        # complex primitive can accumulate reuse instead of being minted at the
        # frontier and immediately superseded (which leaves deep primitives
        # terminal). Aims at reusable deep modules, the Ω-0.6 apex gap.
        self.module_prob = module_prob
        self.module_min_depth = module_min_depth
        self.module_size = module_size
        self._modules: list[str] = []

        self.base_alphabet: list[str] = list(_BASE_ALPHABET)
        self.alphabet: list[str] = list(_BASE_ALPHABET)  # grows via reification
        self._known_ops: set[str] = set()
        self._reified: dict[str, str] = {}               # class hash -> new symbol
        self._reify_depth: dict[str, int] = {}           # symbol -> lineage depth
        self._next_reified: int = 0
        self.max_reify_depth: int = 0
        self._frontier: list[str] = []                   # refreshed each tick
        # reification-DAG structure (Ω-0.6 instrumentation): reuse[c] = how many
        # reified structures use primitive c as a component; combinatorial_count =
        # reifications that combine >=2 reified components (recombination, not mere
        # extension). These separate a *rich* DAG from a deep-but-thin ladder.
        self._reify_structure: dict[str, tuple] = {}
        self._reuse: dict[str, int] = {}
        self._combinatorial_count: int = 0

    # -- material --
    def _feed_alphabet(self) -> list[str]:
        return self.alphabet if self.feed_reified else self.base_alphabet

    def _random_data(self, rng: Noise, lo: int = 2, hi: int = 5) -> tuple:
        length = rng.randint(lo, hi)
        alpha = self._feed_alphabet()
        if ((self.frontier_prob > 0.0 and self._frontier) or
                (self.library_prob > 0.0 and self._library) or
                (self.module_prob > 0.0 and self._modules)):
            fp, lp, mp = self.frontier_prob, self.library_prob, self.module_prob
            out = []
            for _ in range(length):
                roll = rng.random()
                if self._frontier and roll < fp:
                    out.append(rng.choice(self._frontier))
                elif self._library and roll < fp + lp:
                    out.append(rng.choice(self._library))
                elif self._modules and roll < fp + lp + mp:
                    out.append(rng.choice(self._modules))
                else:
                    out.append(rng.choice(alpha))
            return tuple(out)
        return tuple(rng.choice(alpha) for _ in range(length))

    def _random_operator(self, rng: Noise) -> tuple:
        p_len, r_len = rng.randint(1, 2), rng.randint(1, 3)
        pattern = [rng.choice(self.alphabet) for _ in range(p_len)]
        replacement = [rng.choice(self.alphabet) for _ in range(r_len)]
        if rng.random() < self.meta_prob:
            pos = rng.randint(0, len(replacement))
            replacement = replacement[:pos] + [_DELIM] + replacement[pos:]
        return tuple(pattern) + (_DELIM,) + tuple(replacement)

    def seed(self, universe: Universe, rng: Noise) -> None:
        for _ in range(self.n_seed_operators):
            universe.spawn(self._random_operator(rng), kind="operator")
        for _ in range(self.feed_rate * 3):
            universe.spawn(self._random_data(rng), kind="data")
        for op in universe.organizations.values():
            if op.kind == "operator":
                self._known_ops.add(op.cls)

    # -- per tick --
    def propose(self, universe: Universe, rng: Noise):
        reactions: list[Reaction] = []

        # refresh the frontier (deepest `frontier_band` levels) used by the feed
        if self.frontier_prob > 0.0 and self.max_reify_depth >= 1:
            cutoff = self.max_reify_depth - self.frontier_band + 1
            self._frontier = [s for s, d in self._reify_depth.items() if d >= cutoff]
        # refresh the library (the most-reused primitives) used by the feed
        if self.library_prob > 0.0 and self._reuse:
            import heapq
            self._library = heapq.nlargest(self.library_size, self._reuse,
                                           key=self._reuse.get)
        # refresh the deep-module pool (most-reused primitives at depth >= min)
        if self.module_prob > 0.0:
            import heapq
            deep = [s for s, d in self._reify_depth.items() if d >= self.module_min_depth]
            self._modules = heapq.nlargest(self.module_size, deep,
                                           key=lambda s: self._reuse.get(s, 0))

        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        for _ in range(max(budget, 1)):
            reactions.append(Reaction(inputs=(), consume=(),
                                      outputs=((self._random_data(rng), "data"),), via="feed"))

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
                    inputs=(op.uid, d.uid), consume=(d.uid,),
                    outputs=((product, _kind_of(product)),),
                    via=f"apply:{''.join(map(str, op.state))}"))

        # register newly-appeared operator classes as discovered laws
        for o in operators:
            if o.cls not in self._known_ops:
                self._known_ops.add(o.cls)
                universe.register_transform(make_transform(o.state))

        # THE MECHANISM UNDER TEST: promote persistent structure to a new primitive
        if self.reify:
            self._reify_step(universe, rng)

        # publish reification-lineage observables for the metrics stream. The
        # depth *distribution* (mean depth, depth-weighted total) is the quality
        # signal: a shallow breadth-flood scores low mean depth even with a huge
        # primitive count, so it cannot masquerade as deep construction.
        depths = list(self._reify_depth.values())
        universe.gauges["reify_depth"] = float(self.max_reify_depth)
        universe.gauges["reify_depth_mean"] = float(sum(depths) / len(depths)) if depths else 0.0
        universe.gauges["reify_depth_weighted"] = float(sum(depths))  # Σ depth over primitives
        universe.gauges["nested_primitives"] = float(sum(1 for d in depths if d >= 2))
        universe.gauges["deep_primitives"] = float(sum(1 for d in depths if d >= 5))
        # DAG richness: mean/max reuse of a primitive as a component, and the
        # fraction of reifications that recombine >=2 primitives (vs mere extension)
        n = len(self._reify_depth)
        universe.gauges["mean_reuse"] = float(sum(self._reuse.values()) / n) if n else 0.0
        universe.gauges["max_reuse"] = float(max(self._reuse.values())) if self._reuse else 0.0
        universe.gauges["combinatorial_fraction"] = float(self._combinatorial_count / n) if n else 0.0
        # reuse restricted to *deep* primitives — the Ω-0.6 apex gap. If reusable
        # deep modules emerge, deep_mean_reuse rises well above the ~2.6 baseline.
        deep_reuse = [self._reuse.get(s, 0) for s, d in self._reify_depth.items() if d >= 5]
        universe.gauges["deep_mean_reuse"] = float(sum(deep_reuse) / len(deep_reuse)) if deep_reuse else 0.0
        universe.gauges["deep_max_reuse"] = float(max(deep_reuse)) if deep_reuse else 0.0

        return reactions

    def _reify_step(self, universe: Universe, rng: Noise) -> None:
        minted = 0
        # scan persistent, composed, data-kind classes not yet reified
        for rec in list(universe.class_registry.values()):
            if minted >= self.reify_per_tick:
                break
            if not (rec.kind == "data" and rec.size >= 2
                    and 2 <= len(rec.rep_state) <= self.reify_max_len
                    and rec.cls not in self._reified and _DELIM not in rec.rep_state):
                continue
            structure = tuple(rec.rep_state)
            # depth of the components already reified inside this structure; a
            # motif built from reified symbols is a *nested* (higher-order) one and
            # is held to the nested recurrence bar, which drives ratcheting.
            reified_components = [s for s in structure if s in self._reify_depth]
            child_depths = [self._reify_depth[s] for s in reified_components]
            nested = bool(child_depths)
            bar = self.reify_threshold_nested if nested else self.reify_threshold
            if nested and self.depth_discount:
                # deeper motifs are rarer, so give them a proportionally lower bar
                bar = max(1, bar - (max(child_depths) - 1))
            if rec.births < bar:
                continue

            symbol = f"R{self._next_reified}"
            # a fold operator (structure -> symbol) must be affordable; the
            # reservoir thus gates how fast the universe can enlarge itself
            fold_state = structure + (_DELIM, symbol)
            expand_state = (symbol, _DELIM) + structure
            if universe.spawn(fold_state, kind="operator") is None:
                continue
            universe.spawn(expand_state, kind="operator")  # best-effort inverse
            self._reified[rec.cls] = symbol
            depth = 1 + (max(child_depths) if child_depths else 0)
            self._reify_depth[symbol] = depth
            self.max_reify_depth = max(self.max_reify_depth, depth)
            # DAG bookkeeping: record structure, credit reuse of each reified
            # component, and count this as recombination if it fuses >=2 of them.
            self._reify_structure[symbol] = structure
            for c in set(reified_components):
                self._reuse[c] = self._reuse.get(c, 0) + 1
            if len(set(reified_components)) >= 2:
                self._combinatorial_count += 1
            self._next_reified += 1
            self.alphabet.append(symbol)
            universe.register_primitive(symbol)
            # register both directions as discovered laws
            for st in (fold_state, expand_state):
                if canonical_cls(st) not in self._known_ops:
                    self._known_ops.add(canonical_cls(st))
                    universe.register_transform(make_transform(st))
            minted += 1


@register("exp004")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    reify = bool(overrides.get("reify", True))
    meta_prob = float(overrides.get("meta_prob", 0.5))
    cfg = Config(
        experiment="exp004",
        seed=seed,
        ticks=int(overrides.get("ticks", 400)),
        total_quanta=int(overrides.get("total_quanta", 3000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.04)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 120)),
        params={"base_alphabet": _BASE_ALPHABET, "reify": reify, "meta_prob": meta_prob},
    )
    return ReificationPhysics(reify=reify, meta_prob=meta_prob), cfg
