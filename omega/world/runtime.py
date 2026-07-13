"""The persistent world runtime.

Every experiment runs the engine as a *batch*: build a universe, run a fixed number of
ticks, package a ``RunResult``, exit. A **world** is different — it runs *forever*, at flat
memory, and is meant to be *watched* and *checkpointed* rather than measured to a horizon.

``World`` owns the same live state the harness builds — ``(Noise, Universe,
CombinatorPhysics, NoveltyTracker, ConstructionTracker)`` — but advances in **chunks** and
keeps that state addressable so it can be observed (``omega.world.observe``) and pickled
(``omega.world.checkpoint``). Bounded-memory mode (Ω-0.21) is always on, which is exactly
what makes an indefinite run feasible. Chunking is transparent to the dynamics: running the
scheduler ``k`` ticks at a time is identical to running it ``n·k`` ticks at once, so a world
is the same deterministic function of its seed as the equivalent batch run.
"""
from __future__ import annotations

from omega.config import Config
from omega.emergence.construction import ConstructionTracker
from omega.emergence.novelty import NoveltyTracker
from omega.experiments.registry import get_experiment
from omega.kernel.scheduler import Scheduler
from omega.kernel.universe import Universe
from omega.substrate.noise import Noise

# a world runs at flat memory: keep only a window of recent classes / relations
DEFAULT_MEMORY_HORIZON = 20_000
DEFAULT_RELATION_CAP = 80_000


class World:
    """A living Ω world: a persistent, chunk-advanced run with addressable live state."""

    def __init__(self, physics, config: Config, *,
                 memory_horizon: int = DEFAULT_MEMORY_HORIZON,
                 relation_cap: int = DEFAULT_RELATION_CAP,
                 _bundle: dict | None = None) -> None:
        self.config = config
        self.memory_horizon = memory_horizon
        self.relation_cap = relation_cap
        if _bundle is None:                     # a fresh world
            self.rng = Noise(config.seed)
            self.universe = Universe(total_quanta=config.total_quanta)
            self.physics = physics
            self.novelty = NoveltyTracker()
            self.construction = ConstructionTracker()
            self.universe.memory_horizon = memory_horizon
            self.universe.relation_cap = relation_cap
            self.physics.seed(self.universe, self.rng)
        else:                                    # a resumed world (checkpoint.load)
            self.rng = _bundle["rng"]
            self.universe = _bundle["universe"]
            self.physics = _bundle["physics"]
            self.novelty = _bundle["novelty"]
            self.construction = _bundle["construction"]
        self._build_scheduler()

    # ---- construction --------------------------------------------------
    @classmethod
    def create(cls, experiment: str = "world", seed: int = 0, *,
               memory_horizon: int = DEFAULT_MEMORY_HORIZON,
               relation_cap: int = DEFAULT_RELATION_CAP, **overrides) -> "World":
        """Build a fresh world from a registered physics (default the ``world`` builder)."""
        physics, config = get_experiment(experiment)(seed=seed, **overrides)
        return cls(physics, config, memory_horizon=memory_horizon,
                   relation_cap=relation_cap)

    @classmethod
    def from_bundle(cls, bundle: dict) -> "World":
        """Rebuild a world from a checkpoint bundle (the scheduler is rebuilt, not pickled)."""
        return cls(None, bundle["config"], memory_horizon=bundle["memory_horizon"],
                   relation_cap=bundle["relation_cap"], _bundle=bundle)

    def _build_scheduler(self) -> None:
        # the scheduler is stateless-but-for-config, so it is rebuilt (not pickled) on resume.
        self.universe.memory_horizon = self.memory_horizon
        self.universe.relation_cap = self.relation_cap
        self.scheduler = Scheduler(
            self.universe, self.physics, self.rng,
            decay_hazard=self.config.decay_hazard,
            max_reactions_per_tick=self.config.max_reactions_per_tick,
        )
        self.scheduler.add_recorder(self._record)

    def _record(self, universe: Universe, report) -> None:
        # per-tick rate trackers only (no heavy metrics_series — a world runs forever).
        self.novelty.record(universe)
        self.construction.record(universe)

    # ---- advancing -----------------------------------------------------
    def step(self, ticks: int) -> None:
        """Advance the world ``ticks`` ticks (chunk-transparent to the dynamics)."""
        self.scheduler.run(ticks)

    @property
    def tick(self) -> int:
        return self.universe.tick

    def bundle(self) -> dict:
        """The picklable state bundle (everything except the rebuildable scheduler)."""
        return {
            "config": self.config,
            "memory_horizon": self.memory_horizon,
            "relation_cap": self.relation_cap,
            "rng": self.rng,
            "universe": self.universe,
            "physics": self.physics,
            "novelty": self.novelty,
            "construction": self.construction,
        }
