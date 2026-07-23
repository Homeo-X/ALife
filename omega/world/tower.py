"""The live recursive tower — levels that emerge over wall-clock time, watchable.

``omega/levels/stack.py:run_stack`` builds the physics→chemistry→biology→culture tower in *batch*:
run a tier to completion, promote its stable collectives to the next tier's alphabet, recurse. A
**world** wants that same recursion to happen *live* — you watch tier 0 develop, a level is *born*
(a promotion event), tier 1 develops on top of it, and so on — at flat memory, checkpointable.

``TowerWorld`` wraps the ``World`` runtime (``runtime.py``) around ``run_stack``'s promotion logic.
It runs the current top tier as a persistent, chunk-advanced ``World``; once that tier has matured
(``tier_ticks``) it reads the tier's stable collectives (``stack._stable_collectives``) and achieved
competence (``stack._tier_competence``), records a ``TierResult``, and — if the tier formed ≥
``min_collectives`` heritable collectives — **promotes** them to the next tier's alphabet and spins
up the next tier live. With ``law_from_competence`` (exp055) the new tier's Catalytic-Law strength is
*derived* from the competence achieved below, so each emergent level plays by rules the level below
earned.

Faithfulness: each tier is constructed exactly as ``run_stack`` constructs it (same builder, same
per-tier overrides, the *same* seed), and a ``World`` with no eviction (``memory_horizon=0``) is the
same deterministic function of its seed as the equivalent batch run — so an un-evicted ``TowerWorld``
reproduces ``run_stack`` tier-for-tier (pinned by ``test_world``). Run it bounded (a positive horizon)
for an indefinite, watchable tower; run it un-evicted to compare against batch.
"""
from __future__ import annotations

from statistics import mean

from omega.levels.stack import (LEVEL_NAMES, TierResult, _stable_collectives,
                                _tier_competence)
from omega.world.runtime import World, DEFAULT_MEMORY_HORIZON, DEFAULT_RELATION_CAP


class TowerWorld:
    """A live, watchable recursive tower: tiers emerge and promote over wall-clock time."""

    def __init__(self, builder: str = "exp053", seed: int = 0, tier_ticks: int = 3500,
                 base_n_types: int = 32, resolution: int = 3, min_collectives: int = 2,
                 law_from_competence: bool = True, catalyst_period: int = 400,
                 competence_pressure: float = 1.0, max_tiers: int = 8,
                 memory_horizon: int = DEFAULT_MEMORY_HORIZON,
                 relation_cap: int = DEFAULT_RELATION_CAP,
                 genuine_novelty: bool = False, _bundle: dict | None = None) -> None:
        self.builder = builder
        self.seed = seed
        self.tier_ticks = tier_ticks
        self.base_n_types = base_n_types
        self.resolution = resolution
        self.min_collectives = min_collectives
        self.law_from_competence = law_from_competence
        self.catalyst_period = catalyst_period
        self.competence_pressure = competence_pressure
        self.max_tiers = max_tiers
        self.memory_horizon = memory_horizon
        self.relation_cap = relation_cap
        self.genuine_novelty = genuine_novelty
        if _bundle is None:                                  # a fresh tower
            self.alphabet = [f"y{i}" for i in range(base_n_types)]
            self.period = catalyst_period                    # law strength granted to the current tier
            self.tiers: list = []                            # completed TierResults (bottom-up)
            self.unfold: dict = {}                           # tier-(N+1) symbol -> (tier N, signature)
            self.tier_index = 0
            self.tier_elapsed = 0
            self.total_ticks = 0
            self.events: list = []                           # level-birth events (for the watcher)
            self.done = False
            self._start_tier()
        else:                                                # a resumed tower (checkpoint.load)
            self.alphabet = _bundle["alphabet"]
            self.period = _bundle["period"]
            self.tiers = _bundle["tiers"]
            self.unfold = _bundle["unfold"]
            self.tier_index = _bundle["tier_index"]
            self.tier_elapsed = _bundle["tier_elapsed"]
            self.total_ticks = _bundle["total_ticks"]
            self.events = _bundle["events"]
            self.done = _bundle["done"]
            self.current = World.from_bundle(_bundle["current"])

    # ---- tier construction (mirrors run_stack's per-tier build exactly) ---
    def _tier_overrides(self) -> dict:
        return dict(n_patches=24, propagule_mode="source", explicit_atoms=tuple(self.alphabet),
                    n_types=len(self.alphabet), type_resolution=self.resolution,
                    catalyst_period=self.period, competence_pressure=self.competence_pressure)

    def _start_tier(self) -> None:
        self.current = World.create(self.builder, seed=self.seed,
                                    memory_horizon=self.memory_horizon,
                                    relation_cap=self.relation_cap,
                                    genuine_novelty=self.genuine_novelty,
                                    **self._tier_overrides())
        self.tier_elapsed = 0

    # ---- advancing -------------------------------------------------------
    def step(self, ticks: int) -> None:
        """Advance the live tower ``ticks`` ticks; promote a matured tier when it is ready."""
        if self.done:
            return
        self.current.step(ticks)
        self.tier_elapsed += ticks
        self.total_ticks += ticks
        if self.tier_elapsed >= self.tier_ticks:
            self._finalize_tier()

    def _finalize_tier(self) -> None:
        p = self.current.physics
        collectives = _stable_collectives(p)
        comp = _tier_competence(p)
        hs = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
        hn = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
        self.tiers.append(TierResult(
            tier=self.tier_index,
            level=LEVEL_NAMES[min(self.tier_index, len(LEVEL_NAMES) - 1)],
            alphabet_size=len(self.alphabet), n_collectives=len(collectives),
            hered_self=hs, hered_null=hn,
            novelty=self.current.novelty.recent_rate(max(50, self.tier_ticks // 10)),
            classes_ever=self.current.universe.classes_ever_seen,
            heritable=hs > hn, physics=self.builder, competence=comp,
            catalyst_period=self.period))
        # exp055: the transition GRANTS the next tier a law derived from this tier's competence.
        if self.law_from_competence:
            self.period = max(50, int(self.catalyst_period / (1.0 + comp)))
        # promote this tier's collectives to the next tier's alphabet (reification across tiers)
        if (len(collectives) < self.min_collectives or hs <= hn
                or self.tier_index + 1 >= self.max_tiers):
            self.done = True
            return
        new_alphabet = [f"L{self.tier_index + 1}_{i}" for i in range(len(collectives))]
        for sym, sig in zip(new_alphabet, collectives):
            self.unfold[sym] = (self.tier_index, sig)
        nxt = self.tier_index + 1
        self.events.insert(0, {
            "tick": self.total_ticks, "kind": "level",
            "text": f"a new level was born — tier {nxt} ({LEVEL_NAMES[min(nxt, len(LEVEL_NAMES) - 1)]}), "
                    f"{len(collectives)} collectives promoted (competence {comp:.2f})"})
        self.alphabet = new_alphabet
        self.tier_index = nxt
        self._start_tier()

    # ---- observation -----------------------------------------------------
    @property
    def tick(self) -> int:
        return self.total_ticks

    @property
    def tower_depth(self) -> int:
        """Tiers that formed >= 2 stable heritable collectives — the emergent level count."""
        return sum(1 for t in self.tiers if t.heritable and t.n_collectives >= 2)

    def status(self) -> dict:
        """A compact live picture of the emergent tower (for the watcher / vitals)."""
        return {
            "total_ticks": self.total_ticks,
            "active_tier": self.tier_index,
            "tier_elapsed": self.tier_elapsed,
            "tower_depth": self.tower_depth,
            "done": self.done,
            "per_tier": [{"tier": t.tier, "level": t.level, "competence": round(t.competence, 4),
                          "collectives": t.n_collectives, "heritable": t.heritable,
                          "catalyst_period": t.catalyst_period} for t in self.tiers],
            "events": list(self.events[:12]),
        }

    # ---- checkpoint ------------------------------------------------------
    def bundle(self) -> dict:
        """The picklable state bundle (the current tier's World + the tower accumulators)."""
        return {
            "kind": "tower",
            "builder": self.builder, "seed": self.seed, "tier_ticks": self.tier_ticks,
            "base_n_types": self.base_n_types, "resolution": self.resolution,
            "min_collectives": self.min_collectives, "law_from_competence": self.law_from_competence,
            "catalyst_period": self.catalyst_period, "competence_pressure": self.competence_pressure,
            "max_tiers": self.max_tiers, "memory_horizon": self.memory_horizon,
            "relation_cap": self.relation_cap, "genuine_novelty": self.genuine_novelty,
            "alphabet": self.alphabet, "period": self.period, "tiers": self.tiers,
            "unfold": self.unfold, "tier_index": self.tier_index, "tier_elapsed": self.tier_elapsed,
            "total_ticks": self.total_ticks, "events": self.events, "done": self.done,
            "current": self.current.bundle(),
        }

    @classmethod
    def from_bundle(cls, bundle: dict) -> "TowerWorld":
        return cls(builder=bundle["builder"], seed=bundle["seed"], tier_ticks=bundle["tier_ticks"],
                   base_n_types=bundle["base_n_types"], resolution=bundle["resolution"],
                   min_collectives=bundle["min_collectives"],
                   law_from_competence=bundle["law_from_competence"],
                   catalyst_period=bundle["catalyst_period"],
                   competence_pressure=bundle["competence_pressure"], max_tiers=bundle["max_tiers"],
                   memory_horizon=bundle["memory_horizon"], relation_cap=bundle["relation_cap"],
                   genuine_novelty=bundle["genuine_novelty"], _bundle=bundle)
