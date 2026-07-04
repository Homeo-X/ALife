"""The Scheduler — the universe loop.

Deliberately *not* ``for particle in particles``. Each tick:

1. **Observe**    — snapshot the class census (accumulate recognizability).
2. **Propose**    — ask the Physics for candidate reactions.
3. **Constrain**  — enact them in a randomized order, each conservation-checked;
                    order-dependent conflicts (an input already consumed) simply
                    fail closed.
4. **Decay**      — every organization faces the same baseline dissolution
                    hazard. Persistence is therefore *never granted*; a class
                    only survives if its production keeps pace with this uniform
                    entropy. That is the whole point — persistence must emerge.
5. **Measure**    — hand the tick to any metric recorders.
6. **Verify**     — assert conservation. A failure is a kernel bug, not physics.

The loop is fully deterministic given the seed, so any run replays exactly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from omega.kernel.transform import Physics
from omega.kernel.universe import Universe
from omega.substrate.noise import Noise

# A recorder is called once per tick with the universe and the report.
Recorder = Callable[[Universe, "TickReport"], None]


@dataclass(slots=True)
class TickReport:
    tick: int
    population: int
    distinct_classes: int
    reservoir: int
    committed: int
    blocked: int
    decayed: int
    discovered_transforms: int


class Scheduler:
    def __init__(
        self,
        universe: Universe,
        physics: Physics,
        rng: Noise,
        *,
        decay_hazard: float = 0.02,
        max_reactions_per_tick: int | None = None,
    ) -> None:
        self.universe = universe
        self.physics = physics
        self.rng = rng
        self.decay_hazard = decay_hazard
        self.max_reactions_per_tick = max_reactions_per_tick
        self.recorders: list[Recorder] = []
        # activity leak per tick, and whether the physics defines a per-org hazard.
        # Decay was never part of the immutable kernel (Identity/Consistency/
        # Causality/Conservation are) — so a Physics may make it depend on the
        # organization, which is how functional selection enters.
        self.activity_decay = 0.85
        self._physics_hazard = getattr(physics, "hazard", None)

    def add_recorder(self, recorder: Recorder) -> None:
        self.recorders.append(recorder)

    def step(self) -> TickReport:
        u = self.universe
        u.reactions_committed = u.reactions_blocked = u.decayed = 0

        # 1. Observe — accumulate continued recognizability over classes.
        u.observe_classes()

        # 2. Propose.
        reactions = list(self.physics.propose(u, self.rng))

        # 3. Constrain — randomized enactment, each conservation-checked.
        self.rng.shuffle(reactions)
        if self.max_reactions_per_tick is not None:
            reactions = reactions[: self.max_reactions_per_tick]
        for reaction in reactions:
            u.apply_reaction(reaction)

        # 4. Decay — uniform entropy pressure; age the survivors.
        self._decay_pass()

        # advance time; age survivors and leak their recent-activity
        u.tick += 1
        for st in u.stats.values():
            st.age += 1
            st.recent_activity *= self.activity_decay

        # 5/6. Measure and verify.
        report = TickReport(
            tick=u.tick,
            population=len(u.organizations),
            distinct_classes=len(u.class_population()),
            reservoir=u.reservoir,
            committed=u.reactions_committed,
            blocked=u.reactions_blocked,
            decayed=u.decayed,
            discovered_transforms=len(u.discovered_transforms()),
        )
        for rec in self.recorders:
            rec(u, report)
        u.verify()
        return report

    def run(self, ticks: int) -> list[TickReport]:
        return [self.step() for _ in range(ticks)]

    # ----------------------------------------------------------------------
    def _decay_pass(self) -> None:
        u = self.universe
        if self._physics_hazard is None:
            doomed = [uid for uid in list(u.organizations)
                      if self.rng.random() < self.decay_hazard]
        else:
            # per-organization hazard: the Physics couples persistence to whatever
            # it deems functional (e.g. recent activity). Uniform decay is the
            # default the physics can fall back to.
            hz = self._physics_hazard
            doomed = [uid for uid, org in list(u.organizations.items())
                      if self.rng.random() < hz(org, u.stats.get(uid), self.decay_hazard)]
        for uid in doomed:
            u.dissolve(uid)
        u.decayed = len(doomed)
