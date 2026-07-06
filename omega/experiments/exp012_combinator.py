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
    # exp026 extended basis: B/C/W combinators — richer *interacting* types (they are
    # functions, unlike inert data). Inert unless an expression contains these atoms,
    # so every prior experiment (alphabet S/K/I) is byte-identical.
    if isinstance(f, tuple) and isinstance(f[0], tuple) and f[0][0] == "B":
        return (f[0][1], (f[1], x)), True          # B a b c -> a (b c)
    if isinstance(f, tuple) and isinstance(f[0], tuple) and f[0][0] == "C":
        return ((f[0][1], x), f[1]), True          # C a b c -> a c b
    if isinstance(f, tuple) and f[0] == "W":
        return ((f[1], x), x), True                # W a b -> a b b
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


def mutate(e, rng, atoms=_ATOMS):
    """Point-mutation: change one random atom to another symbol from ``atoms``.
    Heritable variation without which selection can only converge, never evolve
    open-endedly. ``atoms`` may include exp026 inert data symbols."""
    positions = list(_atoms_positions(e))
    if not positions:
        return e
    p = rng.choice(positions)
    cur = e if isinstance(e, str) else None
    new_atom = rng.choice(atoms)
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
        # exp022 emergent-collective trait: internal cross-production per deme (a
        # member producing a *different* member). Tallied in _xprod, separate from
        # productivity so it can be *measured* (measure_xprod) even when demes are
        # selected by another rule — isolating selection-for from mere preservation.
        self._xprod: dict[int, int] = {}
        self.measure_xprod = False
        # exp019 local feed: direct the random feed to under-full patches (local
        # carrying capacity) instead of uniformly, so a local replicator can take
        # over its deme (raise within-deme dominance) without starving the whole
        # soup. Tests whether within-deme dominance is what unlocks collective
        # selection — the missing upstream ingredient exp018 identified.
        self.local_feed = False
        # exp023 niche construction: with feed_mode="recycle" a deme is fed a resample
        # of ITS OWN recent products (self._niche) rather than fresh random forms, so
        # the deme's environment becomes a second, heritable inheritance channel — a
        # positive feedback meant to lift within-deme dominance past the ~0.37 ceiling
        # that blocked exp017-022. "random" (default) leaves every prior experiment
        # untouched. _niche is a per-patch rolling buffer of recent product states.
        self.feed_mode = "random"
        self._niche: dict[int, list] = {}
        self.niche_window = 64
        # exp024 founder divergence: with founder_mode="monoculture" each patch is
        # seeded as a distinct monoculture (its own founder class), so demes start in
        # different basins. exp023 showed recycle feed raises dominance but converges
        # every deme on the same global winner; forcing initial divergence is the
        # missing ingredient for recycle to lock *distinct* types into *distinct*
        # demes (individuation). "random" (default) leaves prior experiments untouched.
        self.founder_mode = "random"
        # exp025 combinatorial identity: a deme's phenotype is its internal cross-
        # production NETWORK SIGNATURE (the set of active producer->product class
        # edges), not a single dominant class. Even with few member types the edge-set
        # space is combinatorially large, so demes can hold distinct heritable
        # identities that the class metric (exp024) could not resolve. _deme_edges is
        # a per-patch {(f_cls, prod_cls): count} this generation; heredity of the
        # signature is measured like the class-set heredity but on edge-sets.
        self.track_signature = False
        self.edge_threshold = 2
        self._deme_edges: dict[int, dict] = {}
        self._pending_edges: dict[int, frozenset] = {}
        self._pending_src: dict[int, int] = {}
        self._hered_edge_self: list = []
        self._hered_edge_null: list = []
        # exp026 breed-true fitness: per-patch EMA of realized signature heredity —
        # how faithfully a deme's propagules reproduced its network signature. Used
        # to *select* demes whose collective identity breeds true (deme_fitness=
        # "breed_true"), directly pushing the weak (~1.6x) signature heredity higher.
        self._breedtrue: dict[int, float] = {}
        # exp026 richer type space: the alphabet random expressions are built from.
        # Default is the 3 SKI combinators; adding inert "data" atoms (which no
        # reduction rule touches) makes normal forms carry distinguishable content,
        # broadening/flattening the type distribution beyond the ~9 attractors that
        # capped individuation in exp024. Inert *data* atoms enrich types but kill
        # cross-production (they don't interact); exp026 instead adds extra
        # *combinators* (B/C/W) — richer types that still act as functions. Kept as
        # ("S","K","I") => byte-identical.
        self.atoms = _ATOMS
        # exp020 replicase: strength/fidelity of the explicit template-copy channel.
        # copy_rate=0 (default) leaves every earlier experiment untouched.
        self.copy_rate = 0.0
        self.copy_mut = 0.0
        # exp021 cooperation: a genuine group-beneficial, individually-costly trait —
        # the missing ingredient exp017-020 lacked. Each org carries a heritable coop
        # bit (self._coop). A cooperator replicates slower (pays coop_cost on each
        # copy) but raises its *deme's* reproduction weight (coop_benefit x cooperator
        # fraction). Within-deme selection erodes cooperation; between-deme selection
        # (source propagules) can maintain it. coop=False leaves exp012-020 untouched.
        self.coop = False
        self.coop_cost = 0.0
        self.coop_benefit = 0.0
        self.coop_mut = 0.0
        self.coop_init = 0.5
        self._coop: dict[int, float] = {}
        # direct collective-heredity measure: after a deme is founded from a source,
        # does it resemble that source (class-set Jaccard) more than a random deme?
        self._pending: dict[int, frozenset] = {}
        self._hered_self: list = []
        self._hered_null: list = []

    def _random_expr(self, rng: Noise, size: int) -> object:
        if size <= 1:
            return rng.choice(self.atoms)
        left = rng.randint(1, size - 1)
        return (self._random_expr(rng, left), self._random_expr(rng, size - left))

    def _random_normal(self, rng: Noise):
        """A random expression, reduced to normal form (so the feed is behavioural)."""
        e = self._random_expr(rng, rng.randint(1, 5))
        nf = normalize(e, self.fuel, self.max_size)
        return nf if nf is not None else rng.choice(self.atoms)

    def _seed_coop(self, org, rng: Noise) -> None:
        # exp021: only the founding population carries cooperators; the feed is all
        # defectors, so cooperation must be sustained by heredity+selection.
        if self.coop and org is not None:
            self._coop[org.uid] = 1.0 if rng.random() < self.coop_init else 0.0

    def seed(self, universe: Universe, rng: Noise) -> None:
        if self.founder_mode == "monoculture" and self.n_patches > 0:
            # each patch = a distinct monoculture (its own founder class), pinned to
            # that patch, so demes begin in different basins (exp024 divergence).
            per = max(1, self.seed_pop // self.n_patches)
            for p in range(self.n_patches):
                founder = self._random_normal(rng)
                for _ in range(per):
                    org = universe.spawn(founder, kind="expr")
                    if org is not None:
                        self._patch[org.uid] = p
                        self._seed_coop(org, rng)
            return
        for _ in range(self.seed_pop):
            org = universe.spawn(self._random_normal(rng), kind="expr")
            self._seed_coop(org, rng)

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
                    # rootless orgs are the feed. Default: land in a uniformly random
                    # patch (global feed — dilutes every deme equally). exp019 local
                    # feed instead directs each fed org to a patch with probability
                    # proportional to its local vacancy (target - occupancy), so a
                    # deme a replicator has filled stops receiving diluting feed and
                    # can consolidate a heritable type — without cutting total feed.
                    if self.local_feed:
                        target = max(1.0, len(pop) / self.n_patches)
                        weights = [max(1e-3, target - len(buckets[i]))
                                   for i in range(self.n_patches)]
                        p = rng.weighted_choice(range(self.n_patches), weights)
                    else:
                        p = rng.randint(0, self.n_patches - 1)
                self._patch[o.uid] = p
            if rng.random() < self.mig_rate:         # migration couples the demes
                p = rng.randint(0, self.n_patches - 1)
                self._patch[o.uid] = p
            buckets[p].append(o)
        return buckets

    def _ensure_coop(self, pop, rng: Noise) -> None:
        """Assign each org a heritable cooperation bit, inheriting from its lineage
        (with coop_mut flips) exactly as patches are inherited; feed/seed orgs draw
        one at rate coop_init. This is the group-beneficial trait exp021 selects on."""
        live = {o.uid for o in pop}
        for u in [u for u in self._coop if u not in live]:
            del self._coop[u]
        for o in pop:
            if o.uid in self._coop:
                continue
            c = None
            for parent in o.lineage:
                if parent in self._coop:
                    c = self._coop[parent]
                    break
            if c is None:
                c = 0.0                           # feed organisms are defectors
            elif self.coop_mut > 0.0 and rng.random() < self.coop_mut:
                c = 1.0 - c                       # heritable variation (rare flip)
            self._coop[o.uid] = c

    def _deme_signature(self, pi: int) -> frozenset:
        """The deme's cross-production network signature: edges seen at least
        edge_threshold times this generation (noise-filtered). exp025 uses this as
        the deme's combinatorial identity in place of its single dominant class."""
        return frozenset(e for e, n in self._deme_edges.get(pi, {}).items()
                         if n >= self.edge_threshold)

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
        # exp025: the same heredity test on the deme's NETWORK SIGNATURE (edge-set)
        # rather than its class-set — does a founded deme inherit its source's
        # cross-production network more than a random deme?
        if self.track_signature:
            for child_p, src_sig in list(self._pending_edges.items()):
                child_sig = self._deme_signature(child_p)
                if child_sig:
                    others = [p for p in by_patch if p != child_p and by_patch[p]]
                    if others:
                        r = rng.choice(others)
                        js = jac(child_sig, src_sig)
                        self._hered_edge_self.append(js)
                        self._hered_edge_null.append(jac(child_sig, self._deme_signature(r)))
                        # exp026 breed-true: credit the SOURCE deme with how faithfully
                        # this child reproduced its signature (EMA), so demes whose
                        # networks breed true are selected to reproduce more.
                        sp = self._pending_src.get(child_p)
                        if sp is not None:
                            prev = self._breedtrue.get(sp, js)
                            self._breedtrue[sp] = 0.7 * prev + 0.3 * js
            self._pending_edges.clear()
            self._pending_src.clear()

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
                elif self.deme_fitness == "network":
                    weights = [self._xprod.get(s, 0) + 1 for s in survivors]
                elif self.deme_fitness == "breed_true":
                    # select demes whose network signature reproduces faithfully
                    weights = [self._breedtrue.get(s, 0.2) + 0.05 for s in survivors]
                else:
                    weights = [len(by_patch[s]) for s in survivors]
                if self.coop:
                    # group benefit: a deme founds propagules in proportion to its
                    # cooperator fraction — the collective phenotype selection acts on.
                    boosted = []
                    for w, s in zip(weights, survivors):
                        m = by_patch[s]
                        frac = (sum(1 for o in m if self._coop.get(o.uid, 0.0) >= 1.0)
                                / len(m)) if m else 0.0
                        boosted.append(w * (1.0 + self.coop_benefit * frac))
                    weights = boosted
                src = rng.weighted_choice(survivors, weights)
                pool = by_patch[src]
            else:  # "mixed" null — propagule from the whole survivor pool
                pool = [o for s in survivors for o in by_patch[s]]
            for o in rng.sample(pool, min(self.propagule_size, len(pool))):
                child = universe.spawn(o.state, "expr")
                if child is not None:
                    self._patch[child.uid] = kp
                    if self.coop:  # propagule carries its source org's coop bit
                        self._coop[child.uid] = self._coop.get(o.uid, 0.0)
            if self.propagule_mode == "source":  # remember source for heredity check
                self._pending[kp] = frozenset(o.cls for o in by_patch[src])
                if self.track_signature:
                    self._pending_edges[kp] = self._deme_signature(src)
                    self._pending_src[kp] = src
        self._deme_prod.clear()  # start a fresh productivity window for next gen
        self._xprod.clear()
        self._deme_edges.clear()

    def propose(self, universe: Universe, rng: Noise):
        reactions: list[Reaction] = []

        # knockout: continuously remove suppressed classes so they cannot act
        if self.suppress:
            for uid in [u for u, o in universe.organizations.items()
                        if o.cls in self.suppress]:
                universe.dissolve(uid)

        # exp021: refresh the heritable coop trait before deme reproduction reads it
        if self.coop:
            self._ensure_coop(list(universe.organizations.values()), rng)

        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        if self.feed_mode == "recycle" and self.n_patches > 0:
            # niche construction: feed each deme a resample of its own recent products,
            # anchored on a resident (catalyst) so the new org inherits that deme's
            # patch via lineage. Uses last tick's persistent patch map (self._patch).
            members_by_patch: dict[int, list] = {}
            for o in universe.organizations.values():
                p = self._patch.get(o.uid)
                if p is not None:
                    members_by_patch.setdefault(p, []).append(o)
            patched = [p for p in members_by_patch if members_by_patch[p]]
            for _ in range(max(budget, 1)):
                if not patched:                       # warmup / no patch map yet
                    nf = self._random_normal(rng)
                    reactions.append(Reaction(inputs=(), consume=(),
                                              outputs=((nf, "expr"),), via="feed"))
                    continue
                p = rng.choice(patched)
                buf = self._niche.get(p)
                state = rng.choice(buf) if buf else self._random_normal(rng)
                if self.suppress and canonical_cls(state) in self.suppress:
                    continue
                anchor = rng.choice(members_by_patch[p])
                reactions.append(Reaction(inputs=(anchor.uid,), consume=(),
                                          outputs=((state, "expr"),), via="recycle"))
        else:
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
        # exp022 "network" fitness needs each patch's class set to detect cross-
        # production (a member producing another member) — the collective, non-self
        # metabolic activity that no single replicator can maximize.
        patch_classes = ([set(o.cls for o in m) for m in patches]
                         if (patches is not None
                             and (self.deme_fitness == "network" or self.measure_xprod
                                  or self.track_signature))
                         else None)
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
                if patches is not None and (self.measure_xprod or self.track_signature
                        or self.deme_fitness in ("productivity", "network")):
                    # credit this deme's fitness. identity lookup consumes no RNG, so
                    # non-collective runs and every other experiment stay identical.
                    # "productivity": any viable construction. cross-production
                    # (_xprod): a member making a *different* member already in the
                    # deme — irreducibly collective, measured whenever needed for
                    # selection ("network"), the gauge (measure_xprod), or the deme
                    # network signature (track_signature, exp025).
                    for pi in range(len(patches)):
                        if patches[pi] is members:
                            if self.deme_fitness == "productivity":
                                self._deme_prod[pi] = self._deme_prod.get(pi, 0) + 1
                            if (self.deme_fitness == "network" or self.measure_xprod
                                    or self.track_signature):
                                pcls = canonical_cls(product)
                                if pcls != f.cls and patch_classes is not None \
                                        and pcls in patch_classes[pi]:
                                    if self.deme_fitness == "network" or self.measure_xprod:
                                        self._xprod[pi] = self._xprod.get(pi, 0) + 1
                                    if self.track_signature:
                                        edges = self._deme_edges.setdefault(pi, {})
                                        edges[(f.cls, pcls)] = edges.get((f.cls, pcls), 0) + 1
                            break
                if self.mut_prob > 0.0 and rng.random() < self.mut_prob:
                    m = normalize(mutate(product, rng, self.atoms), self.fuel, self.max_size)
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
                if self.feed_mode == "recycle" and patches is not None:
                    # remember this deme's product so it can be recycled as its feed
                    for pi in range(len(patches)):
                        if patches[pi] is members:
                            buf = self._niche.setdefault(pi, [])
                            buf.append(product)
                            if len(buf) > self.niche_window:
                                del buf[0]
                            break

        # exp020 replicase: an explicit template-copy channel. exp017-019 showed the
        # combinator soup never produces a replicator strong enough to sweep a patch
        # (within-deme dominance caps ~0.37) because self-catalysis (f x)->f is rare
        # and fragile. A copy reaction T -> T + T (template catalytic, cost paid from
        # the reservoir so it stays resource-limited) is a *strong* replicator: it
        # competes for free quanta, cheaper/compact templates win, and a class can
        # sweep its deme. copy_mut gives it heritable variation. The copy inherits
        # the template's patch (via lineage), so replication is local.
        if self.copy_rate > 0.0 and pop:
            for _ in range(int(self.copy_rate * len(pop))):
                if patches is not None:
                    members = rng.choice(patches)
                    if not members:
                        continue
                    t = rng.choice(members)
                else:
                    t = rng.choice(pop)
                if self.coop and self._coop.get(t.uid, 0.0) >= 1.0 \
                        and rng.random() < self.coop_cost:
                    continue                       # cooperators replicate slower
                state = t.state
                if self.copy_mut > 0.0 and rng.random() < self.copy_mut:
                    m = normalize(mutate(state, rng, self.atoms), self.fuel, self.max_size)
                    if m is not None:
                        state = m
                if self.suppress and canonical_cls(state) in self.suppress:
                    continue
                reactions.append(Reaction(inputs=(t.uid,), consume=(),
                                          outputs=((state, "expr"),), via="copy"))

        amp, _ = universe.amplification()
        universe.gauges["amplification"] = amp
        popc = universe.class_population()
        total = sum(popc.values())
        universe.gauges["dominance"] = (max(popc.values()) / total) if total else 0.0
        universe.gauges["max_selfcat"] = float(max(self._selfcat.values())) if self._selfcat else 0.0
        universe.gauges["n_selfcat_classes"] = float(len(self._selfcat))
        if self.coop and pop:
            universe.gauges["coop_frac"] = (
                sum(1 for o in pop if self._coop.get(o.uid, 0.0) >= 1.0) / len(pop))
        if patches is not None and (self.deme_fitness == "network" or self.measure_xprod):
            # mean internal cross-production per live deme — the emergent collective
            # metabolism group selection is being asked to favor.
            live = [self._xprod.get(i, 0) for i, m in enumerate(patches) if m]
            universe.gauges["mean_cross_prod"] = (sum(live) / len(live)) if live else 0.0
        if self.track_signature and patches is not None:
            # combinatorial deme identity: distinct network signatures across live
            # demes, and their mean size. n_deme_signatures >> n_deme_types would mean
            # the edge-set identity space is far richer than the dominant-class one.
            sigs, sizes = [], []
            for i, m in enumerate(patches):
                if m:
                    s = self._deme_signature(i)
                    sigs.append(s); sizes.append(len(s))
            universe.gauges["n_deme_signatures"] = float(len(set(sigs)))
            universe.gauges["mean_signature_size"] = (sum(sizes) / len(sizes)) if sizes else 0.0
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
    physics.local_feed = bool(overrides.get("local_feed", False))
    physics.copy_rate = float(overrides.get("copy_rate", 0.0))
    physics.copy_mut = float(overrides.get("copy_mut", 0.0))
    physics.coop = bool(overrides.get("coop", False))
    physics.coop_cost = float(overrides.get("coop_cost", 0.0))
    physics.coop_benefit = float(overrides.get("coop_benefit", 0.0))
    physics.coop_mut = float(overrides.get("coop_mut", 0.0))
    physics.coop_init = float(overrides.get("coop_init", 0.5))
    physics.measure_xprod = bool(overrides.get("measure_xprod", False))
    physics.feed_mode = str(overrides.get("feed_mode", "random"))
    physics.niche_window = int(overrides.get("niche_window", 64))
    physics.founder_mode = str(overrides.get("founder_mode", "random"))
    physics.track_signature = bool(overrides.get("track_signature", False))
    physics.edge_threshold = int(overrides.get("edge_threshold", 2))
    extra = str(overrides.get("extra_combinators", ""))
    if extra:  # exp026 richer type space: SKI + extra *interacting* combinators (BCW)
        physics.atoms = _ATOMS + tuple(a for a in ("B", "C", "W") if a in extra)
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


@register("exp019")
def build_local_feed(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp019 — patch-local feed: exp018 found collectives cannot be selected
    because demes never crystallize a heritable *type* (within-deme dominance
    stays ≤0.35), and the global feed's constant injection of random forms is the
    churn that prevents local replicator takeover. This directs the feed to
    under-full patches (`local_feed=True`) — local carrying capacity — so a deme a
    replicator fills stops being diluted, without cutting total feed (no
    starvation). All exp018 collective ingredients stay on. Tests whether local
    feed raises within-deme dominance and *then* lets the collective winnow
    (`n_deme_types` / types-per-live-deme below the well-mixed null)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 16)
    overrides.setdefault("deme_fitness", "productivity")
    overrides.setdefault("local_feed", True)
    return _make(seed, "exp019", **overrides)


@register("exp020")
def build_replicase(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp020 — explicit replicase: exp017-019 hit the same wall — the combinator
    soup never makes a replicator strong enough to sweep a patch (within-deme
    dominance ≤0.37), so multi-level selection has no heritable collective unit.
    This adds a strong copy channel (T -> T + T, template catalytic, reservoir-
    limited, `copy_mut` fidelity) on top of exp019's local feed + collective
    machinery. Tests whether local dominance now clears ~0.5 and whether the
    collective *then* winnows (`source` types-per-live-deme below the mixed null)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 16)
    overrides.setdefault("deme_fitness", "productivity")
    overrides.setdefault("local_feed", True)
    overrides.setdefault("copy_rate", 0.5)
    overrides.setdefault("copy_mut", 0.02)
    return _make(seed, "exp020", **overrides)


@register("exp021")
def build_cooperation(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp021 — group-beneficial trait: exp017-020 found the multi-level structure
    inert because nothing coupled a deme's composition to its reproduction in a way
    individual selection wouldn't already produce. This adds the canonical missing
    ingredient — a cooperation trait that is individually costly (`coop_cost`:
    cooperators replicate slower) but collectively beneficial (`coop_benefit`: a
    deme founds propagules in proportion to its cooperator fraction). Within-deme
    selection erodes cooperation; between-deme selection (source propagules) can
    maintain it. Decisive test: does global cooperator fraction stay > 0 under
    `source` but collapse to 0 under the well-mixed `mixed` null?"""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 16)
    overrides.setdefault("deme_fitness", "productivity")
    overrides.setdefault("local_feed", True)
    # strong-relatedness regime: a single-founder propagule bottleneck + fast, strong
    # deme turnover is what gives group selection any purchase (Hamilton/Price).
    overrides.setdefault("total_quanta", 1200)
    overrides.setdefault("copy_rate", 0.3)
    overrides.setdefault("copy_mut", 0.02)
    overrides.setdefault("propagule_size", 1)
    overrides.setdefault("deme_gen", 5)
    overrides.setdefault("deme_death_frac", 0.5)
    overrides.setdefault("coop", True)
    overrides.setdefault("coop_cost", 0.05)
    overrides.setdefault("coop_benefit", 10.0)
    overrides.setdefault("coop_mut", 0.02)
    overrides.setdefault("coop_init", 0.7)
    return _make(seed, "exp021", **overrides)


@register("exp022")
def build_network(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp022 — emergent collective (open problem). exp021's group trait was imposed;
    here it must *emerge*. Deme fitness is `network`: a deme reproduces in proportion
    to its internal *cross*-production — members producing *other* members (a class
    making a different class already present). That is irreducibly collective: a
    monoculture self-catalyst scores ~0; only a mutualistic/autocatalytic set scores
    high, and no single replicator can maximize it. No copy channel, no coop bit —
    the 'cooperation' is emergent membership in a cross-producing network.

    Novel prediction (opposite of exp021's single-locus trait, which wanted *small*
    propagules): a multi-member collective can only be inherited if the propagule
    carries enough of the network, so there should be an *intermediate* propagule-size
    optimum — a transmission threshold below which the collective cannot be passed on."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("local_feed", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("propagule_size", 8)
    return _make(seed, "exp022", **overrides)


@register("exp023")
def build_niche(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp023 — niche construction / environmental heredity (open-problem track A1).
    The wall behind exp017-022: within-deme dominance never clears ~0.37 because the
    random global feed constantly dilutes every deme, so no local type crystallizes.
    Here `feed_mode="recycle"` feeds each deme a resample of ITS OWN recent products
    instead of fresh random forms — the deme's environment becomes a second, heritable
    inheritance channel and a positive feedback on its own composition. Tests whether
    this lifts within-deme dominance and lets demes individuate (n_deme_types winnow
    under `source` vs the `mixed` null) — without collapsing open-ended novelty."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    return _make(seed, "exp023", **overrides)


@register("exp024")
def build_individuation(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp024 — the combination (open-problem track). exp021/022/023 each supplied
    *part* of a major transition: collective selection, an emergent group trait, and
    within-deme dominance — but none individuated demes. This combines all three plus
    the ingredient exp023 exposed as missing: forced founder divergence.
      - founder_mode="monoculture": each deme starts as a distinct monoculture;
      - feed_mode="recycle" (exp023): each deme reinforces its own composition;
      - deme_fitness="network" (exp022): collective selection favors cross-producers;
      - mig_rate=0: isolation preserves the divergence.
    Tests whether demes now become discrete, heritable collective individuals — high
    within-deme dominance AND strong collective heredity (self≫null) that persists,
    rather than all demes collapsing onto one global winner."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("founder_mode", "monoculture")
    return _make(seed, "exp024", **overrides)


@register("exp025")
def build_network_identity(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp025 — combinatorial deme identity (open-problem track). exp024 showed
    individuation is blocked because a deme's identity (its dominant class) draws
    from only ~9 attractor types. This redefines identity as the deme's cross-
    production NETWORK SIGNATURE (`track_signature`) — the set of active
    producer->product edges — so a small member-type space still yields a
    combinatorially large identity space. Decisive test: is that signature heritable
    through the propagule (edge-set Jaccard self >> null, and >> the class-set
    heredity), revealing collective individuation the class metric missed?"""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    return _make(seed, "exp025", **overrides)


@register("exp026")
def build_strong_individuation(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp026 — push weak (~1.6x) network individuation toward strong, via two levers
    at once. (1) Richer type space: `extra_combinators="BCW"` adds B/C/W combinators —
    more distinct types that still *interact* (inert data atoms enrich types but kill
    cross-production). (2) Selection for high-fidelity collective reproduction:
    `deme_fitness="breed_true"` weights a deme's reproduction by how faithfully its
    propagules reproduced its network signature. Built on exp025 (signature identity +
    recycle feed). The study runs the 2x2 {SKI,BCW} x {network,breed_true} to isolate
    each lever and their combination; success = edge-set heredity crossing from weak
    (~1.6x) toward strong (self >> null)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("extra_combinators", "BCW")
    overrides.setdefault("deme_fitness", "breed_true")
    return _make(seed, "exp026", **overrides)
