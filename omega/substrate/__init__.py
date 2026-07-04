"""The substrate — the raw materials a universe is stirred out of.

Nothing here is alive or organized; these are the pre-conditions the axioms
require:

* :mod:`omega.substrate.noise`      — a deterministic source of difference
                                       (Axiom 1) that also drives all stochastic
                                       choices, so every run replays exactly.
* :mod:`omega.substrate.difference`  — minting fresh atomic differences.
* :mod:`omega.substrate.constraint`  — reusable predicates that forbid
                                       interactions (Axiom 4).
* :mod:`omega.substrate.gradient`    — reading the reservoir as a resource
                                       gradient that construction draws down.
"""
from __future__ import annotations

from omega.substrate.noise import Noise
from omega.substrate.difference import DifferenceSource
from omega.substrate.constraint import Constraint, all_of, any_of
from omega.substrate.gradient import reservoir_pressure

__all__ = [
    "Noise",
    "DifferenceSource",
    "Constraint",
    "all_of",
    "any_of",
    "reservoir_pressure",
]
