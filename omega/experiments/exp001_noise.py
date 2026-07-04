"""Experiment 001 — Pure noise. *Can persistence emerge?*

The null control for the entire program. The universe is fed a steady stream of
random, high-entropy organizations (short strings over a large alphabet) drawn
from the reservoir, and nothing else happens: no interaction, no binding, no
operators. Organizations appear, sit, and decay under the uniform hazard.

Prediction (and the point of running it): persistence does **not** emerge. Because
the space of possible strings is enormous, essentially every class is seen in a
single tick and never again — the persistence spectrum piles up at lifespan 0.

The instructive twist: the *novelty rate* here is enormous (every tick is full of
never-seen classes). That is exactly why raw novelty is a trap and the
Open-Endedness Index is multi-factor: noise maximises novelty while producing
zero persistence, zero hierarchy, and zero operators. Verdict should read ACTIVE
(novelty without hierarchy), i.e. not open-ended.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.registry import register
from omega.kernel.transform import Physics, Reaction
from omega.kernel.universe import Universe
from omega.substrate.difference import DifferenceSource
from omega.substrate.gradient import reservoir_pressure
from omega.substrate.noise import Noise

_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class NoisePhysics:
    name = "exp001_noise"

    def __init__(self, alphabet: str = _ALPHABET, min_len: int = 4, max_len: int = 6,
                 feed_rate: int = 40) -> None:
        self.src = DifferenceSource(alphabet)
        self.min_len = min_len
        self.max_len = max_len
        self.feed_rate = feed_rate

    def seed(self, universe: Universe, rng: Noise) -> None:
        for _ in range(self.feed_rate):
            self._inject(universe, rng)

    def propose(self, universe: Universe, rng: Noise):
        # Feed random organizations from the reservoir; throttle as it empties.
        reactions = []
        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        for _ in range(max(budget, 1)):
            length = rng.randint(self.min_len, self.max_len)
            state = self.src.string(rng, length)
            reactions.append(Reaction(inputs=(), consume=(), outputs=((state, "noise"),), via="feed"))
        return reactions

    def _inject(self, universe: Universe, rng: Noise) -> None:
        length = rng.randint(self.min_len, self.max_len)
        universe.spawn(self.src.string(rng, length), kind="noise")


@register("exp001")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    cfg = Config(
        experiment="exp001",
        seed=seed,
        ticks=overrides.get("ticks", 300),
        total_quanta=overrides.get("total_quanta", 6000),
        decay_hazard=overrides.get("decay_hazard", 0.05),
        max_reactions_per_tick=overrides.get("max_reactions_per_tick", 80),
        params={"alphabet_size": len(_ALPHABET), "feed_rate": 40},
    )
    return NoisePhysics(), cfg
