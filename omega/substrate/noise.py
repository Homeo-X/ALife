"""Deterministic noise — the origin of difference and of every random choice.

Axiom 1 says existence begins with distinguishable configurations. Something has
to *supply* that initial distinguishability; in Ω it is a seeded PRNG. The same
object also drives decay, reaction ordering, and operator sampling, so a run is a
pure function of its seed: deterministic replay comes for free.

We wrap :class:`random.Random` rather than exposing it so that the substrate has
a single, auditable entropy source and so we can add domain vocabulary
(``symbol``, ``weighted_choice``) without leaking implementation.
"""
from __future__ import annotations

import random
from typing import Sequence, TypeVar

T = TypeVar("T")


class Noise:
    def __init__(self, seed: int) -> None:
        self.seed = seed
        self._r = random.Random(seed)

    def random(self) -> float:
        return self._r.random()

    def randint(self, a: int, b: int) -> int:
        return self._r.randint(a, b)

    def choice(self, seq: Sequence[T]) -> T:
        return self._r.choice(seq)

    def sample(self, seq: Sequence[T], k: int) -> list[T]:
        k = min(k, len(seq))
        return self._r.sample(list(seq), k)

    def shuffle(self, seq: list) -> None:
        self._r.shuffle(seq)

    def weighted_choice(self, items: Sequence[T], weights: Sequence[float]) -> T:
        return self._r.choices(list(items), weights=list(weights), k=1)[0]

    def symbol(self, alphabet: str) -> str:
        """Draw one atomic difference from an alphabet of symbols."""
        return self._r.choice(alphabet)

    def fork(self, tag: int) -> "Noise":
        """A derived stream — still deterministic, decorrelated from the parent."""
        return Noise((self.seed * 1_000_003) ^ (tag * 2_654_435_761) & 0xFFFFFFFF)
