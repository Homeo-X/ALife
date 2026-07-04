"""Property tests for conservation of distinguishability.

Conservation is the one immutable law; if any code path leaks quanta the whole
substrate is meaningless. We hammer it two ways: a randomized spawn/dissolve/react
stress test, and an every-tick check while running each real experiment.
"""
from __future__ import annotations

import unittest

from omega.experiments.registry import get_experiment
from omega.kernel.scheduler import Scheduler
from omega.kernel.transform import Reaction
from omega.kernel.universe import Universe
from omega.substrate.noise import Noise


class TestConservationProperty(unittest.TestCase):
    def test_random_operations_conserve(self):
        rng = Noise(1234)
        u = Universe(total_quanta=500)
        for _ in range(2000):
            roll = rng.random()
            if roll < 0.45:  # spawn
                length = rng.randint(1, 4)
                u.spawn(tuple(rng.symbol("abcd") for _ in range(length)), kind="x")
            elif roll < 0.7 and u.organizations:  # dissolve
                uid = rng.choice(list(u.organizations))
                u.dissolve(uid)
            elif len(u.organizations) >= 2:  # react two into one
                a, b = rng.sample(list(u.organizations), 2)
                sa = u.organizations[a].state
                r = Reaction(inputs=(a, b), consume=(a, b),
                             outputs=((sa + ("+",), "x"),), via="merge")
                u.apply_reaction(r)
            self.assertEqual(u.verify(), 500)


class TestExperimentsConserve(unittest.TestCase):
    def test_every_tick_conserves(self):
        for name in ("exp001", "exp002", "exp003"):
            physics, cfg = get_experiment(name)(seed=7)
            rng = Noise(cfg.seed)
            u = Universe(total_quanta=cfg.total_quanta)
            physics.seed(u, rng)
            sched = Scheduler(u, physics, rng, decay_hazard=cfg.decay_hazard,
                              max_reactions_per_tick=cfg.max_reactions_per_tick)
            for _ in range(40):
                sched.step()  # scheduler asserts conservation internally each tick
            self.assertEqual(u.reservoir + sum(o.distinguishability
                             for o in u.organizations.values()), cfg.total_quanta)


if __name__ == "__main__":
    unittest.main()
