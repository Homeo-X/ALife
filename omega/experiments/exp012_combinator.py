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


def compose(fs, xs, max_size):
    """exp029 typed-morphism substrate. A morphism is a 2-tuple ``(in_type, out_type)``
    and interaction is **modular composition**: ``(a->b) ∘ (b->c) = (a->c)`` iff the
    types match. Unlike combinator reduction, the product is a deterministic function
    of the two members' types — so a deme's cross-production network is reproducible
    from its member set (the property exp028 showed the combinator dynamics lack)."""
    if not (isinstance(fs, tuple) and isinstance(xs, tuple)
            and len(fs) == 2 and len(xs) == 2):
        return None
    if fs[1] == xs[0]:
        return (fs[0], xs[1])
    return None


def _path_nodes(state) -> list:
    """Flatten a typed-path morphism (right-nested tuple of type atoms) to a list."""
    nodes = []
    cur = state
    while isinstance(cur, tuple) and len(cur) == 2:
        nodes.append(cur[0])
        cur = cur[1]
    nodes.append(cur)
    return nodes


def _path_build(nodes: list):
    """Build a right-nested tuple morphism from a list of >=2 type nodes."""
    state = nodes[-1]
    for n in reversed(nodes[:-1]):
        state = (n, state)
    return state


def compose_path(fs, xs, max_size, resolution=0):
    """exp030 open-ended AND modular substrate. A morphism is a variable-length type
    *path* (t0->t1->...->tk). Composition is concatenation when endpoints match:
    (a..b) ∘ (b..c) = (a..b..c) — deterministic in the members (modular, reproducible),
    yet the path (and its class) grows unboundedly (open-ended). ``resolution`` truncates
    the product to its last N nodes (0 = unbounded): the dial between the exp029 closed/
    reproducible corner (small N) and the combinator open-but-unreproducible corner."""
    fn, xn = _path_nodes(fs), _path_nodes(xs)
    if fn[-1] != xn[0]:
        return None
    nodes = fn + xn[1:]
    if resolution and len(nodes) > resolution:
        nodes = nodes[-resolution:]
    if len(nodes) > max_size:
        return None
    return _path_build(nodes)


def _mutate_path(state, rng, atoms):
    """Point-mutation for a typed path: change / insert / delete one node (keeping
    length >= 2). Heritable variation for the typed_path substrate."""
    nodes = _path_nodes(state)
    roll = rng.random()
    i = rng.randint(0, len(nodes) - 1)
    if roll < 0.7 or len(nodes) <= 2:
        nodes[i] = rng.choice(atoms)                 # substitute
    elif roll < 0.85:
        nodes.insert(i, rng.choice(atoms))           # grow
    else:
        del nodes[i]                                 # shrink
    return _path_build(nodes)


def _tree_leftmost(t):
    while isinstance(t, tuple):
        t = t[0]
    return t


def _tree_truncate(t, depth):
    """Bound a tree's identity: collapse subtrees deeper than ``depth`` to their leftmost
    atom. The branching analogue of ``compose_path``'s node truncation."""
    if isinstance(t, str):
        return t
    if depth <= 1:
        return _tree_leftmost(t)
    return (_tree_truncate(t[0], depth - 1), _tree_truncate(t[1], depth - 1))


def graft(fs, xs, max_size, resolution=0):
    """exp035 tree substrate — a genuinely NEW composition law (not a type substrate).
    Organizations are binary trees; composition **grafts** them into a new node ``(f, x)``
    (a non-associative, non-commutative branching combination), then caps depth to
    ``resolution`` (collapsing subtrees deeper than the cap to their leftmost atom).
    Deterministic in the two parts (modular → a deme's cross-production network is
    reproducible) yet trees grow (open-ended); the depth cap bounds identity so products
    fall back into existing classes (closed loops → heredity). The branching analogue of
    typed_path's path-length truncation, and distinct from both linear concatenation
    (associative) and morphism composition (endpoint-matched)."""
    result = (fs, xs)
    if resolution:
        result = _tree_truncate(result, resolution)
    if _size(result) > max_size:
        return None
    return result


def _mutate_tree(state, rng, atoms):
    """Point-mutation for a tree: descend one random root-to-leaf path, substitute that
    leaf with a random atom. Heritable variation for the tree substrate."""
    if isinstance(state, str):
        return rng.choice(atoms)
    if rng.random() < 0.5:
        return (_mutate_tree(state[0], rng, atoms), state[1])
    return (state[0], _mutate_tree(state[1], rng, atoms))


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
    # exp027 further-extended basis (T/V + primed B'/C'/S'), same gating: inert unless
    # the atom is present, so exp012-026 stay byte-identical. Standard, terminating,
    # non-self-applying combinators — a bigger dial of distinct *interacting* types.
    if isinstance(f, tuple) and f[0] == "T":
        return (x, f[1]), True                     # T a b -> b a
    if isinstance(f, tuple) and isinstance(f[0], tuple) and f[0][0] == "V":
        return ((x, f[0][1]), f[1]), True          # V a b c -> c a b
    if isinstance(f, tuple) and isinstance(f[0], tuple) and isinstance(f[0][0], tuple):
        if f[0][0][0] == "B1":                     # B' k a b c -> k a (b c)
            return ((f[0][0][1], f[0][1]), (f[1], x)), True
        if f[0][0][0] == "C1":                     # C' k a b c -> k (a c) b
            return ((f[0][0][1], (f[0][1], x)), f[1]), True
        if f[0][0][0] == "S1":                     # S' k a b c -> k (a c) (b c)
            return ((f[0][0][1], (f[0][1], x)), (f[1], x)), True
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
        # world: SPACE. The kernel stays spaceless; space is a *constraint a Physics imposes
        # on which organizations may react* (the README's rule). When ``space`` is on, the
        # n_patches demes are laid out on a W×H torus and locality becomes geography:
        # migration hops only to a neighbouring patch, and an extinct patch is recolonized
        # preferentially from a *nearby* survivor — so lineages spread locally
        # (isolation-by-distance, biogeography). Off (default) = the well-mixed uniform-random
        # behaviour of every prior experiment → byte-identical.
        self.space = False
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
        # exp028 network-biased propagule: when "network", found a deme preferentially
        # from the source's *network-participant* members (classes in its cross-
        # production signature) rather than random members — transmit the network, not
        # a random sample. Tests whether the ~3.3x heredity ceiling (exp027) is limited
        # by member-set reproducibility (fixable here) or by the substrate itself.
        # "random" (default) leaves every prior experiment byte-identical.
        self.propagule_bias = "random"
        # exp040 DEVELOPMENTAL (network-template) inheritance: exp028 showed a deme's
        # cross-production network is a dynamical attractor that offspring do NOT re-form from
        # inherited *members* alone (the ~3-5x heredity ceiling). This transmits the developmental
        # *niche* too: when a deme is founded, its recycle buffer (self._niche) is seeded with the
        # PARENT network's product states, so the child is re-fed the parent's outputs and
        # canalizes back to the same edges. A biological analogue: inheriting genes AND a
        # structured developmental environment. It is a STRENGTH dial in [0,1] (the fraction of
        # the parent network's products seeded) — the collective-level analogue of exp030's
        # resolution dial: 0 = off (byte-identical); 1 = full pinning (strong heredity but closes
        # the world); intermediate = the target both corner (strong heredity AND sustained novelty).
        self.network_template = 0.0
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
        # exp027 secondary dial: max size of random feed expressions (default 5).
        self.expr_size = 5
        # exp029 substrate pivot: "combinator" (default, byte-identical) vs "typed" —
        # morphisms (in_type,out_type) that interact by modular composition, so a
        # deme's network is reproducible from its members. n_types base types.
        self.substrate = "combinator"
        self.n_types = 12
        # exp030 typed_path: morphisms are variable-length type paths, composed by
        # concatenation (modular + open-ended). type_resolution truncates products to
        # their last N nodes (0 = unbounded) — the dial between reproducible/closed and
        # open/unreproducible.
        self.type_resolution = 0
        # exp031 level stack: seed_states seeds a tier from a promoted set of lower-tier
        # collectives (instead of random); horizontal_transfer is the CULTURE mechanism —
        # a deme imports a high-value motif from a fitter deme within its lifetime
        # (horizontal, Lamarckian), decoupled from vertical propagule reproduction.
        # Both default off => exp012-030 byte-identical.
        self.seed_states: list | None = None
        self.horizontal_transfer = 0.0
        self._meme_horizontal = 0      # motifs acquired horizontally (culture)
        self._meme_vertical = 0        # motifs inherited vertically (propagule)
        # exp034 in-level reification (the constructibility lever at the collective level):
        # every reify_period ticks, promote the most common recent non-trivial product to a
        # NEW atom appended to self.atoms — growing the generative base *during* the run.
        # Tests whether growing constructibility (not space) keeps the novelty RATE from
        # decaying at long horizon. reify_period=0 (default) => exp012-033 byte-identical.
        self.reify_period = 0
        self.reify_max_atoms = 0       # cap on grown alphabet (0 = uncapped)
        self._reified: dict = {}       # new atom symbol -> the state it stands for
        self._reify_seen: dict = {}    # product class -> [count, state] this period
        self._reified_cls: set = set()
        self._reify_next = 0
        # exp035 tree substrate: a new composition law (graft at leftmost leaf, depth-capped
        # by tree_resolution). substrate != "tree" => byte-identical.
        self.tree_resolution = 0
        # exp036 INTRINSIC FUNCTION: give the environment structure worth predicting, and
        # select for predicting it. feed_pattern="cyclic" makes the feed favour a rotating
        # BAND of atoms (a "season" that changes every feed_period ticks); deme_fitness=
        # "anticipation" rewards a deme whose recent products already match the *next* band —
        # i.e. it has internalized the environment's regularity and pre-builds for it. This
        # is the engine piece exp011 said was missing (function must be intrinsic, selected,
        # not bolted on). feed_pattern="random" / other deme_fitness => byte-identical.
        self.feed_pattern = "random"
        self.feed_period = 0
        self.feed_bands = 4
        self._cur_band: list = []      # atoms favoured by the feed this tick (cyclic)
        self._next_band: set = set()   # atoms the NEXT season will favour (what to anticipate)
        self._deme_atoms: dict[int, dict] = {}   # per-patch recent product-atom tally
        # exp037 PER-COLLECTIVE EVOLVABLE INTERNAL STATE (meta-reification): a deme carries a
        # heritable, mutable *construction rule* of its own — its own type_resolution — used in
        # its own compositions and transmitted (with mutation) to the demes it founds. exp033
        # made physics first-class per LEVEL; this makes a slice of it first-class per
        # COLLECTIVE, so a collective can evolve and improve its own "architecture" under
        # selection (proto self-improvement). deme_genome=False (default) => byte-identical.
        self.deme_genome = False
        self.genome_mut = 0.3
        self.genome_res_range = (1, 5)   # initial per-deme resolution drawn uniformly here
        self._deme_res: dict[int, int] = {}   # per-patch resolution (the heritable genome)
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

    def _feed_choice(self, rng: Noise):
        """Draw a feed atom. exp036 cyclic feed favours the current season's band; otherwise
        (default) it is exactly ``rng.choice(self.atoms)`` with no extra draw => byte-identical."""
        if self.feed_pattern == "cyclic" and self._cur_band and rng.random() < 0.75:
            return rng.choice(self._cur_band)
        return rng.choice(self.atoms)

    def _random_normal(self, rng: Noise):
        """A random behaviour to feed. Combinator: a random expression's normal form.
        Typed (exp029): a random morphism ``(in_type, out_type)``."""
        if self.substrate == "typed":
            return (self._feed_choice(rng), self._feed_choice(rng))
        if self.substrate == "typed_path":
            L = rng.randint(2, max(2, self.expr_size))
            return _path_build([self._feed_choice(rng) for _ in range(L)])
        if self.substrate == "tree":
            return self._random_expr(rng, rng.randint(2, max(2, self.expr_size)))
        e = self._random_expr(rng, rng.randint(1, self.expr_size))
        nf = normalize(e, self.fuel, self.max_size)
        return nf if nf is not None else rng.choice(self.atoms)

    def _seed_coop(self, org, rng: Noise) -> None:
        # exp021: only the founding population carries cooperators; the feed is all
        # defectors, so cooperation must be sustained by heredity+selection.
        if self.coop and org is not None:
            self._coop[org.uid] = 1.0 if rng.random() < self.coop_init else 0.0

    def seed(self, universe: Universe, rng: Noise) -> None:
        if self.seed_states:
            # exp031: seed a tier from a promoted set of lower-tier collectives.
            for _ in range(self.seed_pop):
                org = universe.spawn(rng.choice(self.seed_states), kind="expr")
                self._seed_coop(org, rng)
            return
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

    # ---- geography (world SPACE) --------------------------------------
    def _grid_dims(self) -> tuple[int, int]:
        """Lay the n_patches demes on the most-square W×H torus that tiles them exactly."""
        n = max(1, self.n_patches)
        w = int(n ** 0.5)
        while w > 1 and n % w:
            w -= 1
        return w, n // w

    def patch_pos(self, p: int) -> tuple[int, int]:
        w, _ = self._grid_dims()
        return p % w, p // w

    def _neighbors(self, p: int) -> list:
        w, h = self._grid_dims()
        x, y = p % w, p // w
        return [((y + dy) % h) * w + ((x + dx) % w)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]

    def _patch_dist(self, a: int, b: int) -> int:
        w, h = self._grid_dims()
        ax, ay, bx, by = a % w, a // w, b % w, b // w
        return min((ax - bx) % w, (bx - ax) % w) + min((ay - by) % h, (by - ay) % h)

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
                if self.space:                       # geography: hop to a neighbour only
                    p = rng.choice(self._neighbors(p))
                else:
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

    def _deme_closure(self, pi: int) -> float:
        """exp038 AUTOCATALYTIC CLOSURE: an *emergent* coherence measure. From the deme's
        cross-production edges (producer_cls -> product_cls), a class that is both **produced
        by** a member and **itself a producer** sits inside a self-maintaining loop. Closure
        = |producers ∩ products| / |producers ∪ products| — 0 for a feed-forward chain (every
        product is a dead end), →1 for a fully self-producing set (a collective that rebuilds
        its own parts). Unlike exp021's imposed coop bit, this is read off the real network."""
        edges = self._deme_edges.get(pi)
        if not edges:
            return 0.0
        producers = {f for (f, _p) in edges}
        products = {p for (_f, p) in edges}
        union = producers | products
        return len(producers & products) / len(union) if union else 0.0

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
                elif self.deme_fitness == "anticipation":
                    # exp036: reward a deme whose recent products already match the atoms the
                    # NEXT season will favour — it has internalized the environment's rhythm.
                    nb = self._next_band
                    weights = [1.0 + sum(n for a, n in self._deme_atoms.get(s, {}).items()
                                         if a in nb) for s in survivors]
                elif self.deme_fitness == "closure":
                    # exp038: reward autocatalytic CLOSURE — a deme that rebuilds its own parts
                    # (a self-maintaining loop), an emergent coherence read off the network.
                    weights = [0.05 + self._deme_closure(s) for s in survivors]
                elif self.deme_fitness == "composite":
                    # exp039 capstone: MULTI-OBJECTIVE alignment — reward demes good at BOTH
                    # self-maintenance (closure) AND faithful reproduction (breed_true heredity).
                    # Each objective is normalized to the survivor-set mean (so neither's raw
                    # scale/variance dominates), then multiplied — a deme must be above-average on
                    # *both* to win. Tests whether combining independent objectives beats exp038's
                    # single-objective trade-off (compound) or hits a real Pareto frontier.
                    cl = [self._deme_closure(s) for s in survivors]
                    bt = [self._breedtrue.get(s, 0.1) for s in survivors]
                    mcl = (sum(cl) / len(cl)) or 1.0
                    mbt = (sum(bt) / len(bt)) or 1.0
                    # maximin: reward the deme whose *weaker* (mean-normalized) objective is
                    # strongest — forces both high, penalizing single-objective specialists.
                    weights = [0.05 + min(c / mcl, b / mbt) for c, b in zip(cl, bt)]
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
                if self.space:                       # geography: recolonize from nearby
                    weights = [w * (0.25 ** self._patch_dist(s, kp))
                               for w, s in zip(weights, survivors)]
                src = rng.weighted_choice(survivors, weights)
                pool = by_patch[src]
                if self.deme_genome:   # exp037: the founded deme inherits src's rule (+ mut)
                    lo, hi = self.genome_res_range
                    r = self._deme_res.get(src, self.type_resolution)
                    if rng.random() < self.genome_mut:
                        r = max(lo, min(hi, r + rng.choice((-1, 1))))
                    self._deme_res[kp] = r
            else:  # "mixed" null — propagule from the whole survivor pool
                pool = [o for s in survivors for o in by_patch[s]]
            k = min(self.propagule_size, len(pool))
            if (self.propagule_bias == "network" and self.propagule_mode == "source"
                    and self.track_signature):
                # prioritize members whose class participates in the source deme's
                # cross-production signature, so the network (not a random sample) is
                # what founds the child deme.
                parts = {c for e in self._deme_signature(src) for c in e}
                participants = [o for o in pool if o.cls in parts]
                others = [o for o in pool if o.cls not in parts]
                rng.shuffle(participants)
                rng.shuffle(others)
                propagule = (participants + others)[:k]
            else:
                propagule = rng.sample(pool, k)
            for o in propagule:
                child = universe.spawn(o.state, "expr")
                if child is not None:
                    self._patch[child.uid] = kp
                    if self.coop:  # propagule carries its source org's coop bit
                        self._coop[child.uid] = self._coop.get(o.uid, 0.0)
            if self.propagule_mode == "source":  # remember source for heredity check
                self._pending[kp] = frozenset(o.cls for o in by_patch[src])
                self._meme_vertical += 1          # a vertical (reproductive) transmission
                if self.track_signature:
                    self._pending_edges[kp] = self._deme_signature(src)
                    self._pending_src[kp] = src
                    if self.network_template > 0.0:
                        # exp040: seed a FRACTION (network_template) of the PARENT network's
                        # product states into the child's developmental niche, so recycle-feed
                        # re-primes the producing reactions and the child canalizes toward the
                        # parent's edges. A partial template (< 1) is the dial between the
                        # reproducible-but-closed corner (full) and the open-but-weak corner (off).
                        cls_state = {o.cls: o.state for o in by_patch[src]}
                        seed = [cls_state[p] for (_f, p) in self._deme_signature(src)
                                if p in cls_state]
                        if seed:
                            keep = max(1, int(self.network_template * len(seed)))
                            self._niche[kp] = seed[:keep][-self.niche_window:]
        # exp031 CULTURE: horizontal, Lamarckian transfer between *surviving* demes — a
        # deme imitates a fitter deme's top motif within its lifetime (not via
        # reproduction), injecting that motif's product into its own recycle buffer.
        if self.horizontal_transfer > 0.0:
            rep_state: dict = {}
            for m in by_patch.values():
                for o in m:
                    rep_state.setdefault(o.cls, o.state)
            live = [p for p in survivors if by_patch.get(p)]
            for rp in live:
                if rng.random() >= self.horizontal_transfer:
                    continue
                donors = [p for p in live if p != rp and self._deme_edges.get(p)]
                if not donors:
                    continue
                w = [len(self._deme_edges[p]) + self._breedtrue.get(p, 0.0) + 0.1
                     for p in donors]
                dp = rng.weighted_choice(donors, w)
                (_f, p_cls), _ = max(self._deme_edges[dp].items(), key=lambda kv: kv[1])
                if p_cls in rep_state:
                    self._niche.setdefault(rp, []).append(rep_state[p_cls])
                    self._meme_horizontal += 1
        self._deme_prod.clear()  # start a fresh productivity window for next gen
        self._xprod.clear()
        self._deme_edges.clear()
        self._deme_atoms.clear()  # exp036: fresh product-atom window each generation

    def _reify_promote(self) -> None:
        """exp034: promote the most common recent non-trivial product to a NEW atom,
        appended to ``self.atoms`` (an opaque primitive standing for that motif — Axiom-5
        reification, applied *within* a level and *during* the run). Deterministic (no
        RNG): the constructive base grows, so novelty need not dilute. The per-period
        tally is cleared so it tracks the *moving* frontier of common motifs."""
        if self.reify_max_atoms and len(self.atoms) >= self.reify_max_atoms:
            self._reify_seen = {}
            return
        best, best_n = None, self.edge_threshold
        for pc, (n, st) in self._reify_seen.items():
            if pc in self._reified_cls or not isinstance(st, tuple):
                continue                       # only composites (non-atomic) are reifiable
            if n > best_n:
                best_n, best = n, (pc, st)
        self._reify_seen = {}
        if best is None:
            return
        sym = f"R{self._reify_next}"
        self._reify_next += 1
        self.atoms = tuple(self.atoms) + (sym,)
        self._reified[sym] = best[1]
        self._reified_cls.add(best[0])

    def propose(self, universe: Universe, rng: Noise):
        reactions: list[Reaction] = []

        # exp036: the environment's "season" — which band of atoms the feed favours now, and
        # which it will favour next (what a deme must anticipate). Deterministic in the tick,
        # so feed_pattern != "cyclic" consumes no state and stays byte-identical.
        if self.feed_pattern == "cyclic" and self.feed_period > 0 and self.atoms:
            k = max(1, self.feed_bands)
            w = max(1, len(self.atoms) // k)
            cur = (universe.tick // self.feed_period) % k
            self._cur_band = list(self.atoms[cur * w: cur * w + w]) or list(self.atoms)
            nb = ((universe.tick // self.feed_period) + 1) % k
            self._next_band = set(self.atoms[nb * w: nb * w + w]) or set(self.atoms)

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

        # exp034 in-level reification: on its own cadence, promote a persistent motif to a
        # new primitive (grows self.atoms). No RNG consumed => reify_period=0 byte-identical.
        if (self.reify_period and universe.tick > 0
                and universe.tick % self.reify_period == 0):
            self._reify_promote()

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
        # exp037: give every live deme a construction-rule genome (its own resolution) and a
        # fast id->patch-index map so a composition can use its deme's rule. Gated => off is
        # byte-identical (no map built, global type_resolution used).
        genome_ix = None
        if self.deme_genome and patches is not None:
            lo, hi = self.genome_res_range
            for pi in range(len(patches)):
                if patches[pi] and pi not in self._deme_res:
                    self._deme_res[pi] = rng.randint(lo, hi)
            genome_ix = {id(m): i for i, m in enumerate(patches)}
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
                res = self.type_resolution
                if genome_ix is not None:
                    res = self._deme_res.get(genome_ix.get(id(members), -1), res)
                if self.substrate == "typed":
                    product = compose(f.state, x.state, self.max_size)
                elif self.substrate == "typed_path":
                    product = compose_path(f.state, x.state, self.max_size, res)
                elif self.substrate == "tree":
                    product = graft(f.state, x.state, self.max_size, self.tree_resolution)
                else:
                    product = normalize((f.state, x.state), self.fuel, self.max_size)
                if product is None:
                    continue
                if self.reify_period:            # exp034: tally products for reification
                    pc = canonical_cls(product)
                    seen = self._reify_seen.get(pc)
                    if seen is None:
                        self._reify_seen[pc] = [1, product]
                    else:
                        seen[0] += 1
                if patches is not None and (self.measure_xprod or self.track_signature
                        or self.deme_fitness in ("productivity", "network", "anticipation",
                                                 "closure", "composite")):
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
                            if self.deme_fitness == "anticipation":
                                # exp036: tally which atoms this deme is currently producing,
                                # so anticipation fitness can reward matching the NEXT season.
                                d = self._deme_atoms.setdefault(pi, {})
                                for a in _path_nodes(product):
                                    d[a] = d.get(a, 0) + 1
                            break
                if self.mut_prob > 0.0 and rng.random() < self.mut_prob:
                    if self.substrate == "typed_path":
                        product = _mutate_path(product, rng, self.atoms)
                    elif self.substrate == "tree":
                        product = _mutate_tree(product, rng, self.atoms)
                    elif self.substrate == "typed":
                        product = mutate(product, rng, self.atoms)
                    else:
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
        if self.horizontal_transfer > 0.0:
            universe.gauges["meme_horizontal"] = float(self._meme_horizontal)
            universe.gauges["meme_vertical"] = float(self._meme_vertical)
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
    physics.propagule_bias = str(overrides.get("propagule_bias", "random"))
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
    # richer type space (exp026/027): SKI + extra *interacting* combinators. Tokens
    # are comma/space-separated (multi-char primed combinators need this); the legacy
    # concatenated "BCW" form is still accepted for the single-char B/C/W.
    raw = str(overrides.get("extra_combinators", ""))
    tokens = [t for t in raw.replace(" ", ",").split(",") if t]
    if len(tokens) == 1 and "," not in raw and all(ch in "BCW" for ch in tokens[0]):
        tokens = list(tokens[0])  # "BCW" -> ["B","C","W"]
    known = ("B", "C", "W", "T", "V", "B1", "C1", "S1")
    physics.atoms = _ATOMS + tuple(t for t in known if t in tokens)
    physics.expr_size = int(overrides.get("expr_size", 5))
    physics.substrate = str(overrides.get("substrate", "combinator"))
    physics.n_types = int(overrides.get("n_types", 12))
    physics.type_resolution = int(overrides.get("type_resolution", 0))
    physics.tree_resolution = int(overrides.get("tree_resolution", 0))
    physics.space = bool(overrides.get("space", False))     # world geography (gated)
    physics.feed_pattern = str(overrides.get("feed_pattern", "random"))  # exp036 environment
    physics.feed_period = int(overrides.get("feed_period", 0))
    physics.feed_bands = int(overrides.get("feed_bands", 4))
    physics.deme_genome = bool(overrides.get("deme_genome", False))   # exp037 evolvable rule
    physics.genome_mut = float(overrides.get("genome_mut", 0.3))
    physics.network_template = float(overrides.get("network_template", 0.0))  # exp040 strength
    physics.reify_period = int(overrides.get("reify_period", 0))
    physics.reify_max_atoms = int(overrides.get("reify_max_atoms", 0))
    if physics.substrate in ("typed", "typed_path", "tree"):  # atoms over n_types base types
        physics.atoms = tuple(f"y{i}" for i in range(physics.n_types))
    # exp031 level stack: an explicit promoted alphabet (a tier's atoms ARE the lower
    # tier's collectives), a seed set of promoted states, and the culture channel.
    if overrides.get("explicit_atoms"):
        physics.atoms = tuple(overrides["explicit_atoms"])
    physics.seed_states = overrides.get("seed_states")
    physics.horizontal_transfer = float(overrides.get("horizontal_transfer", 0.0))
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


@register("exp027")
def build_substrate_dial(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp027 — how far does the substrate dial go? exp026 showed enriching the basis
    with interacting combinators lifts network-signature heredity (1.6x -> 2.4x). This
    exposes the *full* extended basis (S,K,I,B,C,W,T,V + primed B'/C'/S') so a study
    can sweep basis richness (3 -> 11 combinators) and see whether collective
    individuation keeps climbing toward strong (self >> null) or plateaus. Same exp025/
    026 collective machinery (network signature + heredity, recycle feed, network
    fitness, isolation); a secondary `expr_size` dial enlarges feed expressions."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("extra_combinators", "B,C,W,T,V,B1,C1,S1")
    return _make(seed, "exp027", **overrides)


@register("exp028")
def build_reproducible(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp028 — is the ~3.3x individuation ceiling reproducibility-limited or
    substrate-limited? exp027 found network-signature heredity peaks at ~3.3x (basis
    S,K,I,B,C,W,T,V) then falls as the type space grows too rich for a random propagule
    to re-sample the deme's network. This tests the fix: `propagule_bias="network"`
    founds a child deme from the source's *network-participant* members (transmit the
    network, not random members), at the exp027 optimum basis with breed-true
    selection. The study sweeps bias x propagule_size. If edge-set heredity crosses
    from ~3.3x toward strong, the ceiling was reproducibility (fixable in-substrate);
    if it plateaus, the ceiling is the substrate itself (motivating a typed/lambda
    pivot)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 16)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "breed_true")
    overrides.setdefault("extra_combinators", "B,C,W,T,V")
    overrides.setdefault("propagule_bias", "network")
    return _make(seed, "exp028", **overrides)


@register("exp029")
def build_typed_substrate(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp029 — the substrate pivot. exp028 proved the ~3.3x individuation ceiling is
    substrate-limited: the combinator reduction dynamics do not re-form a deme's
    cross-production network even from identical members. This pivots to a **typed
    substrate** (`substrate="typed"`): organizations are morphisms (in_type,out_type)
    and interaction is modular composition ((a->b)∘(b->c)=(a->c)), so a deme's network
    is a deterministic function of its member set — reproducible by construction. Runs
    the exp025-027 collective machinery (network signature + heredity, recycle feed,
    network fitness, isolation) on the new substrate. Prediction: network-signature
    heredity crosses from thin/weak (~3x ratio, self~0.06) into strong (self >> null
    with substantial overlap) — a completed transition to collective individuality."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed")
    overrides.setdefault("n_types", 12)
    return _make(seed, "exp029", **overrides)


@register("exp030")
def build_openended_modular(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp030 — the capstone: an OPEN-ENDED *and* MODULAR substrate. exp029 found the
    two substrates are opposite corners of one trade-off (combinator: open-ended but
    networks unreproducible; typed: modular/reproducible but closed). This uses
    variable-length type PATHS composed by concatenation (`substrate="typed_path"`):
    composition is deterministic (modular → networks reproducible) yet paths grow
    unboundedly (open-ended → novelty > 0). `type_resolution` truncates products to
    their last N nodes — the dial between the two corners. The study sweeps it to test
    whether an intermediate regime gives BOTH strong network heredity AND sustained
    novelty (a completed transition to collective individuality) or whether the
    frontier is a strict trade-off."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)      # the "both" corner: strong heredity AND
    overrides.setdefault("type_resolution", 3)  # open-ended novelty AND rich networks
    return _make(seed, "exp030", **overrides)


@register("exp031_culture")
def build_culture(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp031 (culture level) — a qualitatively distinct top tier on the exp030 base.
    Biology transmits *vertically* (propagule → offspring deme). Culture is *horizontal
    and Lamarckian*: `horizontal_transfer` lets a deme imitate a fitter deme's top
    network motif within its lifetime, decoupled from reproduction. The study contrasts
    a motif's spread with vs without transfer, and horizontal vs vertical rate."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("horizontal_transfer", 0.3)
    return _make(seed, "exp031_culture", **overrides)


@register("exp034")
def build_reification(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp034 — sustained novelty via in-level REIFICATION (the constructibility lever).
    exp032 found the both-corner's novelty *rate* drifts down over 120k ticks (its atom
    alphabet is fixed). This turns the constructibility lever back on *within* a level:
    every `reify_period` ticks the most common recent product motif is promoted to a new
    atom (grows `self.atoms` during the run), testing the program's core thesis — that
    growing constructibility (not space) keeps the novelty rate from decaying. Same
    exp030 both-corner base; `reify_period=0` recovers exp030 exactly."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("reify_period", 500)
    overrides.setdefault("reify_max_atoms", 256)
    return _make(seed, "exp034", **overrides)


@register("exp035")
def build_tree(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp035 — a genuinely NEW level law (not a type substrate). Organizations are binary
    TREES; composition grafts x at f's leftmost leaf, depth-capped by `tree_resolution`
    (the branching analogue of typed_path's path truncation). Tests whether a law unlike
    all three type substrates still reaches the exp030 "both corner" (strong reproducible
    heredity AND sustained novelty) — i.e. whether the both-corner condition, not the
    specific concatenation law, is what makes a level work. Runs the same collective
    machinery as exp030."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "tree")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("tree_resolution", 2)
    return _make(seed, "exp035", **overrides)


@register("world")
def build_world(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """The **living world** — the most-alive single-tier configuration, meant to be run
    *persistently* (forever, bounded memory) and *watched* rather than measured to a fixed
    horizon. It composes the program's confirmed ingredients on one substrate:
      - the exp030 **both corner** (`typed_path`, n_types 32, resolution 3): modular AND
        open-ended, so collectives are heritable *and* the world stays open (Ω-0.15);
      - **collective individuals** (`track_signature` + `deme_fitness="network"` + demes):
        reproducing network-signature lifeforms with heredity (Ω-0.15);
      - **reification** (`reify_period`): continuing construction, so the novelty rate does
        not decay over a long life (Ω-0.20);
      - **culture** (`horizontal_transfer`): horizontal, Lamarckian motif spread between
        lifeforms (Ω-0.16).
    Every knob already exists and is gated, so exp001–035 stay byte-identical. This is not a
    new experiment; it is the world runtime's default physics (see `omega/world/`)."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("reify_period", 500)
    overrides.setdefault("reify_max_atoms", 0)      # keep constructing (persistent world)
    overrides.setdefault("horizontal_transfer", 0.3)
    overrides.setdefault("space", True)             # geography: a torus of patches
    overrides.setdefault("mig_rate", 0.06)          # local diffusion (neighbours only)
    return _make(seed, "world", **overrides)


@register("exp036")
def build_anticipation(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp036 — INTRINSIC FUNCTION: the engine piece exp011 said was missing (function must
    be intrinsic and *selected*, not bolted on). The environment is given a regularity worth
    predicting — the feed favours a **rotating band of atoms** (a "season" that turns every
    `feed_period` ticks) — and demes are selected for **anticipation**: a deme whose recent
    products already match the *next* season is fitter. Prediction: with a predictable feed,
    collectives evolve to produce the next season's atoms above chance (intrinsic function);
    the matched control (random feed) has nothing to anticipate, so no such structure forms.
    Runs the exp030 both-corner collective machinery."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "anticipation")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("feed_pattern", "cyclic")
    overrides.setdefault("feed_period", 300)
    overrides.setdefault("feed_bands", 4)
    return _make(seed, "exp036", **overrides)


@register("exp037")
def build_genome(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp037 — PER-COLLECTIVE EVOLVABLE INTERNAL STATE (meta-reification): the engine piece
    exp036 showed is required (you cannot select for what a collective cannot represent). Each
    deme carries a heritable, mutable **construction rule of its own** — its `type_resolution`,
    made first-class per COLLECTIVE (exp033 made it per LEVEL) — used in its own compositions
    and transmitted (with `genome_mut` mutation) to the demes it founds. Demes start with
    resolutions drawn uniformly from `genome_res_range`; under network selection the population's
    rule should **evolve toward the exp027 fitness optimum** (~2–3) — a collective improving its
    own architecture. Prediction: treatment (network selection) converges toward the optimum
    from a random start; a matched control (mixed/random founding) drifts. Runs the exp030
    both-corner machinery."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("deme_genome", True)
    overrides.setdefault("genome_mut", 0.3)
    return _make(seed, "exp037", **overrides)


@register("exp038")
def build_closure(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp038 — COHERENCE as an emergent, better-aligned selection target. exp037 showed
    evolvable architecture amplifies whatever is selected (Goodhart), and that network fitness
    drives runaway openness. This selects for **autocatalytic closure** instead — the fraction
    of a deme's cross-production network that is self-producing (a class both produced by and
    itself a producer: a self-maintaining loop). Unlike exp021's *imposed* cooperation bit,
    closure is *emergent* — read off the real network. Prediction: `deme_fitness="closure"`
    raises closure above a matched network-selection control (an emergent coherence trait can
    be selected), and self-maintaining demes are **longer-lived** (attacking the churn/short-
    life problem). Runs the exp030 both-corner machinery."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "closure")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    return _make(seed, "exp038", **overrides)


@register("exp040")
def build_network_template(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp040 — DEVELOPMENTAL (network-template) inheritance: a direct assault on the collective-
    heredity ceiling (exp028: ~3-5x null, substrate-limited because *identical members ⇏ the same
    network* — the network is a dynamical attractor, not a stored structure). Hypothesis: offspring
    fail to breed the network true because they inherit only members and must re-derive the
    attractor. This transmits the developmental *niche* too — the child's recycle buffer is seeded
    with the parent network's product states (`network_template`), re-priming the producing
    reactions so it canalizes back to the parent edges. Base is the exp030 both corner with a
    network-biased propagule (exp028); the matched control is the same with `network_template=False`
    (i.e. exp028's members-only transmission, which capped at ~3x). Prediction: template inheritance
    lifts self-vs-null heredity past the ceiling; falsification (also a real result): it does not,
    and collective identity is intrinsically non-reproducible."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "network")
    overrides.setdefault("propagule_bias", "network")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    overrides.setdefault("network_template", 0.5)   # partial template — the both-corner target
    return _make(seed, "exp040", **overrides)


@register("exp039")
def build_composite(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    """exp039 — the CAPSTONE of the self-improvement arc. exp036–038 showed every *single*
    selection proxy Goodharts: network → runaway openness (exp037), closure → low heredity
    (exp038). The design constraint they exposed is that **alignment is multi-objective**. This
    tests it directly: `deme_fitness="composite"` rewards demes good at BOTH self-maintenance
    (autocatalytic closure) AND faithful reproduction (breed_true heredity), multiplicatively
    (a deme must satisfy both). Question: does combining objectives **compound** — reaching high
    closure AND high heredity at once, beating the single-objective trade-off — or does it land
    in the **middle** (a genuine Pareto frontier: the two are fundamentally in tension)? Either
    is a real capstone result. Runs the exp030 both-corner machinery."""
    overrides.setdefault("mut_prob", 0.05)
    overrides.setdefault("track_ecology", True)
    overrides.setdefault("n_patches", 24)
    overrides.setdefault("deme_gen", 20)
    overrides.setdefault("mig_rate", 0.0)
    overrides.setdefault("propagule_size", 8)
    overrides.setdefault("feed_mode", "recycle")
    overrides.setdefault("track_signature", True)
    overrides.setdefault("deme_fitness", "composite")
    overrides.setdefault("substrate", "typed_path")
    overrides.setdefault("n_types", 32)
    overrides.setdefault("type_resolution", 3)
    return _make(seed, "exp039", **overrides)
