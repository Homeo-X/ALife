"""The recursive level stack.

A single major transition (exp017–030) turns a collection of level-N individuals into a
level-(N+1) individual: a deme whose cross-production **network signature** is heritable
(exp030) is a reproducible collective. This module makes that transition **recurse**.

Each tier runs the exp030 ``typed_path`` substrate (open-ended AND modular) whose base
atoms are the tier's *alphabet*. After the run, the tier's stable collectives — live
demes carrying a non-trivial, heritable network signature — are **promoted**: each
becomes a single fresh symbol, and the set of those symbols is the *next* tier's
alphabet. So a tier-(N+1) atom literally **is** a tier-N collective; a tier-(N+1) path is
a sequence of tier-N collectives; and physics → chemistry → biology → culture emerge as
successive tiers of one engine. The tower stops when a tier yields < 2 stable collectives
(a real possible outcome — transitions need not recurse).

The reusable engine (no kernel changes): ``get_experiment('exp030')`` for the per-tier
physics, ``omega.experiments.harness.run`` for the run, and the physics object's
``_deme_edges`` / ``_deme_signature`` / ``_hered_edge_self|null`` for collective
detection. Reification (promoting a persistent higher-order structure to a new primitive,
Axiom 5 / exp004) is the promotion primitive, here applied *across tiers of individuality*
rather than within one level.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run as _harness_run

# what the individuals AT tier i are analogues of (physics is the kernel beneath tier 0)
LEVEL_NAMES = ["chemistry", "biology", "culture", "meta-culture", "meta²-culture"]


@dataclass
class TierResult:
    tier: int
    level: str                 # the analogue for individuals at this tier
    alphabet_size: int         # how many atoms (= lower-tier collectives) this tier had
    n_collectives: int         # stable heritable collectives formed (→ next alphabet)
    hered_self: float
    hered_null: float
    novelty: float
    classes_ever: int
    heritable: bool            # self > null: the tier supports heritable collectives
    physics: str = "exp030"    # which registered engine ran this tier (exp033: may vary)
    competence: float = 0.0    # exp055: mean achieved competence of this tier's live demes
    catalyst_period: int = 0   # exp055: the (competence-derived) law strength granted to this tier


@dataclass
class StackResult:
    tiers: list                # list[TierResult]
    unfold: dict = field(default_factory=dict)  # tier-(N+1) symbol -> (tier N, signature)

    @property
    def tower_depth(self) -> int:
        """Number of tiers that formed >=2 stable heritable collectives — the new
        open-endedness axis: open-endedness *of levels*, not just within a level."""
        return sum(1 for t in self.tiers if t.heritable and t.n_collectives >= 2)


def _stable_collectives(physics) -> list:
    """Signatures of live demes that carry a non-trivial network (the tier's collectives).
    Reads the physics' end-of-run per-patch edge tallies (``_deme_edges``)."""
    sigs = []
    for pi in list(physics._deme_edges):
        s = physics._deme_signature(pi)
        if s:
            sigs.append(s)
    return sigs


def _tier_competence(physics) -> float:
    """exp055: mean achieved competence (closure + breed-true + network breadth, exp042) of this tier's
    live demes — the quantity a rule-changing transition reads to grant the NEXT tier its law."""
    live = [pi for pi in list(physics._deme_edges) if physics._deme_edges.get(pi)]
    if not live:
        return 0.0
    return mean(physics._deme_competence(pi) for pi in live)


def run_stack(max_tiers: int = 4, seed: int = 0, ticks: int = 3000,
              base_n_types: int = 32, resolution: int = 3,
              min_collectives: int = 2, levels: tuple | None = None,
              builder: str = "exp030", law_from_competence: bool = False,
              catalyst_period: int = 400, competence_pressure: float = 1.0) -> StackResult:
    """Run the recursive tower; return per-tier results and the unfold map.

    ``levels`` makes the per-tier physics **first-class** (exp033): a sequence of
    registered builder names, one per tier (cycled if shorter than ``max_tiers``), so
    different levels can run *different composition laws* — e.g. ``('exp029','exp030',
    'exp031_culture')`` is a closed→open→culture tower rather than the self-similar
    ``exp030`` engine climbing itself. All three share the type-atom interface (each
    ingests the promoted alphabet via ``explicit_atoms`` and exposes deme signatures),
    so the promotion bridge is physics-agnostic. ``levels=None`` (default) runs
    ``exp030`` at every tier — byte-identical to the pre-exp033 tower.

    exp055 TRANSITION-AS-RULE-CHANGE: ``builder`` sets a single per-tier engine for all
    tiers (default ``exp030``; ``exp053`` runs the competence-compounding Catalytic-Law +
    Red-Queen physics at every level). ``law_from_competence`` makes the transition itself
    change the law: the NEXT tier's Catalytic-Law strength (``catalyst_period``) is DERIVED
    from THIS tier's achieved competence — a more competent level grants its successor a
    faster-harvesting (stronger) law, ``period = base / (1 + competence)``. Unlike exp054's
    (failed) *deeper* law, the richness added here is a **new kind** — the higher tier
    composes lower-tier *collectives* — so cross-production stays viable. Off ⇒ the exact
    pre-exp055 tower (``law_from_competence`` False and ``builder='exp030'`` ⇒ byte-identical)."""
    alphabet = [f"y{i}" for i in range(base_n_types)]          # tier-0 base types
    tiers: list = []
    unfold: dict = {}
    period = catalyst_period                                    # law strength granted to the current tier
    for tier in range(max_tiers):
        b = builder if not levels else levels[tier % len(levels)]
        physics, cfg = get_experiment(b)(
            seed=seed, ticks=ticks, n_patches=24, propagule_mode='source',
            explicit_atoms=tuple(alphabet), n_types=len(alphabet),
            type_resolution=resolution, catalyst_period=period,
            competence_pressure=competence_pressure)
        res = _harness_run(physics, cfg)
        collectives = _stable_collectives(physics)
        comp = _tier_competence(physics)
        hs = mean(physics._hered_edge_self) if physics._hered_edge_self else 0.0
        hn = mean(physics._hered_edge_null) if physics._hered_edge_null else 0.0
        tiers.append(TierResult(
            tier=tier, level=LEVEL_NAMES[min(tier, len(LEVEL_NAMES) - 1)],
            alphabet_size=len(alphabet), n_collectives=len(collectives),
            hered_self=hs, hered_null=hn, novelty=res.open_endedness["novelty_rate"],
            classes_ever=res.final_classes_total, heritable=hs > hn, physics=b,
            competence=comp, catalyst_period=period))
        # exp055: the transition GRANTS the next tier a law derived from this tier's competence —
        # a competent level earns its successor a stronger (faster-harvesting) Catalytic Law.
        if law_from_competence:
            period = max(50, int(catalyst_period / (1.0 + comp)))
        # promote this tier's collectives to the next tier's alphabet (reification)
        if len(collectives) < min_collectives or hs <= hn:
            break
        new_alphabet = [f"L{tier + 1}_{i}" for i in range(len(collectives))]
        for sym, sig in zip(new_alphabet, collectives):
            unfold[sym] = (tier, sig)                          # nesting: symbol IS a collective
        alphabet = new_alphabet
    return StackResult(tiers=tiers, unfold=unfold)


# convenience aliases for the package API
Level = TierResult
LevelStack = StackResult
