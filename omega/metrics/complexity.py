"""Complexity primitives — diversity, disorder, and hierarchy.

Kept as pure functions so they can be unit-tested against hand-computed values
and reused by the higher-level indices.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, Sequence

from omega.kernel.universe import Universe


def shannon_entropy(counts: Iterable[int]) -> float:
    """Shannon entropy (bits) of a population distribution over classes.

    Low when one class dominates, high when many classes coexist evenly. This is
    the substrate's "recoverable organization" read the information-theoretic way.
    """
    counts = [c for c in counts if c > 0]
    total = sum(counts)
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts:
        p = c / total
        h -= p * math.log2(p)
    return h


def class_diversity(universe: Universe) -> int:
    """Number of distinct organizational classes currently present."""
    return len(universe.class_population())


def hierarchy_index(universe: Universe) -> float:
    """Mean compositional depth over the living population.

    A flat soup of atoms scores ~0. A soup where organizations nest inside
    organizations scores higher — this is the signal that *organizational
    classes*, not just organizations, are proliferating.
    """
    depths = [o.depth for o in universe.organizations.values()]
    if not depths:
        return 0.0
    return sum(depths) / len(depths)
