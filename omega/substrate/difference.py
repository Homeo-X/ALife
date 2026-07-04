"""Minting atomic differences.

A ``DifferenceSource`` hands out atoms drawn from an alphabet. It exists so that
experiments do not each reinvent "make me a random symbol / a random short
string", and so the alphabet (the size of the space of primitive differences) is
an explicit, logged parameter of a universe rather than a magic constant.
"""
from __future__ import annotations

from dataclasses import dataclass

from omega.substrate.noise import Noise


@dataclass(slots=True)
class DifferenceSource:
    alphabet: str

    def atom(self, rng: Noise) -> str:
        return rng.symbol(self.alphabet)

    def string(self, rng: Noise, length: int) -> tuple[str, ...]:
        """A short arrangement of atoms — the seed material for construction."""
        return tuple(rng.symbol(self.alphabet) for _ in range(length))

    @property
    def space_size(self) -> int:
        return len(self.alphabet)
