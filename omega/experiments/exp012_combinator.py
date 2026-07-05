"""Experiment 012 — Behavior-first substrate (SKI combinator soup).

Three form-based experiments hit walls (deep-reuse, copying, functional selection),
all second-order add-ons to a substrate where behaviour is optional. Ω authorises
abandoning an approach when the evidence says so. This experiment changes the
*substrate*, not an add-on.

Here an organization **is a function**: an SKI-combinator expression. Its identity
is its **behaviour** — the normal form it reduces to — not its written form.
Interaction is **application**: organization *f* applied to organization *x*
produces ``normalize(f x)``. The three combinators are the whole of physics:

    I x        → x
    K x y      → x            (discard — erasure)
    S x y z    → x z (y z)    (duplicate x's argument — the seed of copying)

The S rule *duplicates* ``z``; that is exactly why copying can be an *attractor*
here and was an impossible quine in the string soup. Conservation is untouched:
a reduction that grows the expression must pay the extra distinguishability out of
the reservoir, so **reproduction is resource-limited** — replicators compete for
free quanta, which is where selection comes from.

Representation (chosen so distinguishability counts only atoms, conserving cleanly):
a str ``'S'|'K'|'I'`` is an atom; a 2-tuple ``(f, x)`` is an application.

The question three form-based experiments could not answer: **does a self-amplifying
replicator emerge?** Measured with the kernel's fed/constructed split
(``amplification``) and population ``dominance`` — the same gauges exp010 used, so
the two substrates are directly comparable.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.registry import register
from omega.kernel.organization import canonical_cls
from omega.kernel.transform import Physics, Reaction
from omega.kernel.universe import Universe
from omega.substrate.gradient import reservoir_pressure
from omega.substrate.noise import Noise

_ATOMS = ("S", "K", "I")


def _size(e) -> int:
    if isinstance(e, str):
        return 1
    return _size(e[0]) + _size(e[1])


def _step(e):
    """One leftmost-outermost reduction; returns (expr, changed)."""
    if isinstance(e, str):
        return e, False
    f, x = e
    if f == "I":                                   # I x -> x
        return x, True
    if isinstance(f, tuple) and f[0] == "K":       # (K a) x -> a
        return f[1], True
    if isinstance(f, tuple) and isinstance(f[0], tuple) and f[0][0] == "S":
        a, b, c = f[0][1], f[1], x                 # S a b c -> (a c)(b c)
        return ((a, c), (b, c)), True
    f2, ch = _step(f)
    if ch:
        return (f2, x), True
    x2, ch = _step(x)
    if ch:
        return (f, x2), True
    return e, False


def normalize(e, fuel: int, max_size: int):
    """Reduce to normal form. Returns the NF, or None if it runs away / diverges."""
    for _ in range(fuel):
        if _size(e) > max_size:
            return None
        e2, ch = _step(e)
        if not ch:
            return e
        e = e2
    return None


def _atoms_positions(e, path=()):
    if isinstance(e, str):
        yield path
    else:
        yield from _atoms_positions(e[0], path + (0,))
        yield from _atoms_positions(e[1], path + (1,))


def _set_at(e, path, val):
    if not path:
        return val
    f, x = e
    if path[0] == 0:
        return (_set_at(f, path[1:], val), x)
    return (f, _set_at(x, path[1:], val))


def mutate(e, rng):
    """Point-mutation: change one random atom to a different combinator. Heritable
    variation without which selection can only converge, never evolve open-endedly."""
    positions = list(_atoms_positions(e))
    if not positions:
        return e
    p = rng.choice(positions)
    cur = e if isinstance(e, str) else None
    new_atom = rng.choice(_ATOMS)
    return _set_at(e, p, new_atom) if p else new_atom


class CombinatorPhysics:
    name = "exp012_combinator"

    def __init__(self, feed_rate: int = 14, apply_attempts: int = 80,
                 fuel: int = 120, max_size: int = 24, seed_pop: int = 60,
                 mut_prob: float = 0.0, track_ecology: bool = False,
        n_patches: int = 0, mig_rate: float = 0.02) -> None:
        self.feed_rate = feed_rate
        self.apply_attempts = apply_attempts
        self.fuel = fuel
        self.max_size = max_size
        self.seed_pop = seed_pop
        # exp013 knob: imperfect reduction. With probability mut_prob a product is
        # point-mutated (one atom changed) then re-normalized — heritable variation.
        # Without it, selection can only converge (replicator takeover, Ω-0.9). The
        # question: does mutation turn takeover into open-ended *evolution*?
        self.mut_prob = mut_prob
        # self-catalysis: a class C is a genuine replicator (not just a convergence
        # attractor) if applying C to something reproduces C: (C x) -> C. We count
        # such events per class to tell replication from mere normal-form pile-up.
        self._selfcat: dict[str, int] = {}
        # exp014 ecology: the cross-production graph. _cross[(f_cls, p_cls)] counts
        # reactions where function class f produced product class p. From it we read
        # mutualism (reciprocal production), hypercycles (longer cycles), and
        # parasitism (produced a lot, produces little). _size_of caches class sizes.
        self.track_ecology = track_ecology
        self._cross: dict[tuple, int] = {}
        self._produces: dict[str, int] = {}
        self._produced: dict[str, int] = {}
        self._size_of: dict[str, int] = {}
        # exp015 knockout: classes to suppress (dissolved every tick). Used to test
        # whether a topological hypercycle is *functionally* self-sustaining —
        # remove one member and see if its partners' production collapses.
        self.suppress: set = set()
        # exp016 locality: partition the soup into n_patches demes; application only
        # happens *within* a patch, so each product has few local producers (low
        # redundancy) — the condition Ω-0.12 flagged as required for *obligate*
        # hypercycles. A product inherits its function-parent's patch; feed lands
        # randomly; mig_rate orgs hop patches per tick (keeps demes coupled).
        self.n_patches = n_patches
        self.mig_rate = mig_rate
        self._patch: dict[int, int] = {}
        # exp017 multi-level selection: demes themselves reproduce. Every deme_gen
        # ticks a fraction of demes go extinct and are recolonized by a *propagule*
        # copied from a surviving deme (chosen by productivity, so fitter collectives
        # found more demes). propagule_mode="mixed" is the null: recolonize from a
        # well-mixed pool, destroying collective heredity. If selection acts on the
        # collective, the between-deme diversity of "deme types" should winnow under
        # "source" but not under "mixed".
        self.deme_gen = 0
        self.deme_death_frac = 0.3
        self.propagule_size = 4
        self.propagule_mode = "source"
        # exp018 collective fitness: how a surviving deme's chance of founding a
        # propagule is set. "size" (the exp017 default) weights by deme headcount —
        # but the global reservoir cap pins every deme to ~the same size, so
        # deme-level selection is near-neutral (drift). "productivity" instead
        # weights by the deme's *construction throughput* (viable applications it
        # produced this generation), a heritable, composition-derived trait — the
        # heritable between-deme fitness variance exp017 lacked. _deme_prod tallies
        # it per patch, reset each deme generation.
        self.deme_fitness = "size"
        self._deme_prod: dict[int, int] = {}
        # direct collective-heredity measure: after a deme is founded from a source,
        # does it resemble that source (class-set Jaccard) more than a random deme?
        self._pending: dict[int, frozenset] = {}
        self._hered_self: list = []
        self._hered_null: list = []

    def _random_expr(self, rng: Noise, size: int) -> object:
        if size <= 1:
            return rng.choice(_ATOMS)
        left = rng.randint(1, size - 1)
        return (self._random_expr(rng, left), self._random_expr(rng, size - left))

    def _random_normal(self, rng: Noise):
        """A random expression, reduced to normal form (so the feed is behavioural)."""
        e = self._random_expr(rng, rng.randint(1, 5))
        nf = normalize(e, self.fuel, self.max_size)
        return nf if nf is not None else rng.choice(_ATOMS)

    def seed(self, universe: Universe, rng: Noise) -> None:
        for _ in range(self.seed_pop):
            universe.spawn(self._random_normal(rng), kind="expr")

    def _build_patches(self, pop, rng: Noise) -> list:
        """Assign each org to a patch (inheriting its function-parent's patch, else
        random), apply migration, and return the per-patch member lists."""
        live = {o.uid for o in pop}
        for u in [u for u in self._patch if u not in live]:
            del self._patch[u]
        buckets = [[] for _ in range(self.n_patches)]
        for o in pop:
            p = self._patch.get(o.uid)
            if p is None:
                for parent in o.lineage:            # inherit function-parent's patch
                    if parent in self._patch:
                        p = self._patch[parent]
                        break
                if p is None:
                    p = rng.randint(0, self.n_patches - 1)
                self._patch[o.uid] = p
            if rng.random() < self.mig_rate:         # migration couples the demes
                p = rng.randint(0, self.n_patches - 1)
                self._patch[o.uid] = p
            buckets[p].append(o)
        return buckets

    def _deme_reproduction(self, universe: Universe, rng: Noise) -> None:
        """Kill a fraction of demes and recolonize each from a propagule copied out
        of a surviving deme (productivity-weighted) — deme-level reproduction."""
        pop = list(universe.organizations.values())
        by_patch: dict[int, list] = {}
        for o in pop:
            p = self._patch.get(o.uid)
            if p is not None:
                by_patch.setdefault(p, []).append(o)
        # measure heredity of demes founded in the previous round: does a child
        # deme resemble its source (class-set Jaccard) more than a random deme?
        def jac(a, b):
            return len(a & b) / len(a | b) if (a or b) else 0.0
        for child_p, src_set in list(self._pending.items()):
            child_set = frozenset(o.cls for o in by_patch.get(child_p, []))
            if child_set:
                others = [p for p in by_patch if p != child_p and by_patch[p]]
                if others:
                    r = rng.choice(others)
                    self._hered_self.append(jac(child_set, src_set))
                    self._hered_null.append(jac(child_set, frozenset(o.cls for o in by_patch[r])))
        self._pending.clear()

        alive = [p for p, m in by_patch.items() if m]
        if len(alive) < 2:
            return
        n_kill = min(int(self.deme_death_frac * self.n_patches), len(alive) - 1)
        if n_kill <= 0:
            return
        rng.shuffle(alive)
        kill, survivors = alive[:n_kill], alive[n_kill:]
        for kp in kill:
            for o in by_patch[kp]:
                universe.dissolve(o.uid)
            if self.propagule_mode == "source":
                if self.deme_fitness == "productivity":
                    weights = [self._deme_prod.get(s, 0) + 1 for s in survivors]
                else:
                    weights = [len(by_patch[s]) for s in survivors]
                src = rng.weighted_choice(survivors, weights)
                pool = by_patch[src]
            else:  # "mixed" null — propagule from the whole survivor pool
                pool = [o for s in survivors for o in by_patch[s]]
            for o in rng.sample(pool, min(self.propagule_size, len(pool))):
                child = universe.spawn(o.state, "expr")
                if child is not None:
                    self._patch[child.uid] = kp
            if self.propagule_mode == "source":  # remember source for heredity check
                self._pending[kp] = frozenset(o.cls for o in by_patch[src])
        self._deme_prod.clear()  # start a fresh productivity window for next gen

    def propose(self, universe: Universe, rng: Noise):
        reactions: list[Reaction] = []

        # knockout: continuously remove suppressed classes so they cannot act
        if self.suppress:
            for uid in [u for u, o in universe.organizations.items()
                        if o.cls in self.suppress]:
                universe.dissolve(uid)

        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        for _ in range(max(budget, 1)):
            nf = self._random_normal(rng)
            if self.suppress and canonical_cls(nf) in self.suppress:
                continue  # never (re)introduce a knocked-out class
            reactions.append(Reaction(inputs=(), consume=(),
                                      outputs=((nf, "expr"),), via="feed"))

        # deme-level reproduction round (multi-level selection)
        if (self.deme_gen and self.n_patches > 0 and universe.tick > 0
                and universe.tick % self.deme_gen == 0):
            self._deme_reproduction(universe, rng)

        pop = list(universe.organizations.values())
        patches = self._build_patches(pop, rng) if self.n_patches > 0 else None
        if self.n_patches > 0 and patches is not None:
            # publish between-deme collective diversity: distinct deme "types"
            # (each deme's most-abundant class). Winnowing => collective selection.
            types = set()
            for members in patches:
                if members:
                    from collections import Counter
                    types.add(Counter(o.cls for o in members).most_common(1)[0][0])
            universe.gauges["n_deme_types"] = float(len(types))
            universe.gauges["n_live_demes"] = float(sum(1 for m in patches if m))
        if len(pop) >= 2:
            for _ in range(self.apply_attempts):
                if patches is not None:
                    members = rng.choice(patches) if patches else None
                    if not members or len(members) < 2:
                        continue
                    f, x = rng.choice(members), rng.choice(members)
                else:
                    f = rng.choice(pop)
                    x = rng.choice(pop)
                if f.uid == x.uid:
                    continue
                product = normalize((f.state, x.state), self.fuel, self.max_size)
                if product is None:
                    continue
                if self.deme_fitness == "productivity" and patches is not None:
                    # credit this deme with a viable construction event (its fitness).
                    # identity lookup consumes no RNG, so non-productivity runs and
                    # every other experiment stay byte-identical.
                    for pi in range(len(patches)):
                        if patches[pi] is members:
                            self._deme_prod[pi] = self._deme_prod.get(pi, 0) + 1
                            break
                if self.mut_prob > 0.0 and rng.random() < self.mut_prob:
                    m = normalize(mutate(product, rng), self.fuel, self.max_size)
                    if m is not None:
                        product = m
                if self.suppress and canonical_cls(product) in self.suppress:
                    continue  # never (re)construct a knocked-out class
                # f is catalytic (a function keeps acting); x (the argument) is
                # consumed into the product. A function that keeps yielding copies
                # of itself is thus a replicator — resource-limited by the reservoir.
                if product == f.state:                 # (f x) -> f : self-catalysis
                    fc = f.cls
                    self._selfcat[fc] = self._selfcat.get(fc, 0) + 1
                if self.track_ecology:
                    fcls, pcls = f.cls, canonical_cls(product)
                    key = (fcls, pcls)
                    self._cross[key] = self._cross.get(key, 0) + 1
                    self._produces[fcls] = self._produces.get(fcls, 0) + 1
                    self._produced[pcls] = self._produced.get(pcls, 0) + 1
                    if pcls not in self._size_of:
                        self._size_of[pcls] = _size(product)
                reactions.append(Reaction(
                    inputs=(f.uid, x.uid), consume=(x.uid,),
                    outputs=((product, "expr"),), via="apply"))

        amp, _ = universe.amplification()
        universe.gauges["amplification"] = amp
        popc = universe.class_population()
        total = sum(popc.values())
        universe.gauges["dominance"] = (max(popc.values()) / total) if total else 0.0
        universe.gauges["max_selfcat"] = float(max(self._selfcat.values())) if self._selfcat else 0.0
        universe.gauges["n_selfcat_classes"] = float(len(self._selfcat))
        return reactions


def _make(seed, experiment, **overrides):
    physics = CombinatorPhysics(
        fuel=int(overrides.get("fuel", 120)),
        max_size=int(overrides.get("max_size", 24)),
        apply_attempts=int(overrides.get("apply_attempts", 80)),
        mut_prob=float(overrides.get("mut_prob", 0.0)),
        track_ecology=bool(overrides.get("track_ecology", False)),
        n_patches=int(overrides.get("n_patches", 0)),
        mig_rate=float(overrides.get("mig_rate", 0.02)),
    )
    physics.deme_gen = int(overrides.get("deme_gen", 0))
    physics.deme_death_frac = float(overrides.get("deme_death_frac", 0.3))
    physics.propagule_size = int(overrides.get("propagule_size", 4))
    physics.propagule_mode = str(overrides.get("propagule_mode", "source"))
    physics.deme_fitness = str(overrides.get("deme_fitness", "size"))
    cfg = Config(
        experiment=experiment,
        seed=seed,
        ticks=int(overrides.get("ticks", 1500)),
        total_quanta=int(overrides.get("total_quanta", 4000)),
        decay_hazard=float(overrides.get("decay_hazard", 0.05)),
        max_reactions_per_tick=int(overrides.get("max_reactions_per_tick", 150)),
        params={"fuel": 120, "max_size": 24, "mut_prob": float(overrides.get("mut_prob", 0.0))},
    )
    return physics, cfg


@register("exp012")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    return _make(seed, "exp012", **overrides)


@register("exp013")
def build_evolution(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp013 — the synthesis: reproduction + heritable variation. Defaults turn on
    mutation; ``mut_prob=0`` recovers the exp012 (pure-takeover) control."""
    overrides.setdefault("mut_prob", 0.05)
    return _make(seed, "exp013", **overrides)


@register("exp014")
def build_ecology(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp014 — ecology: the evolving replicator soup with cross-production tracking
    on, so mutualism / hypercycles / parasites can be measured."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    return _make(seed, "exp014", **overrides)


@register("exp016")
def build_spatial(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp016 — locality: the evolving/ecology soup partitioned into demes, so each
    product has few local producers. Tests whether reducing redundancy lets
    *obligate* (knockout-sensitive) hypercycles form."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 12)
    return _make(seed, "exp016", **overrides)


@register("exp017")
def build_multilevel(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp017 — multi-level selection: demes reproduce (extinction + propagule
    recolonization). Tests whether selection acts on the *collective* — whether
    between-deme collective diversity winnows under propagule heredity (`source`)
    but not under a well-mixed null (`propagule_mode="mixed"`)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 40)
    return _make(seed, "exp017", **overrides)


@register("exp018")
def build_collective_fitness(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp018 — collective fitness: exp017's long-run study found real collective
    *heredity* but no collective *selection*, because the global reservoir cap
    equalizes deme size and makes size-weighted deme reproduction near-neutral.
    This turns on both missing ingredients: heritable between-deme fitness variance
    (``deme_fitness="productivity"`` — reproduce fitter/more-constructive demes)
    and strong collective heredity (isolated demes + a deme-dominating propagule +
    fast turnover). Tests whether *then* the collective actually outcompetes:
    whether ``n_deme_types`` winnows below the exp017 controls."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 16)
    overrides.setdefault("deme_fitness", "productivity")
    return _make(seed, "exp018", **overrides)
