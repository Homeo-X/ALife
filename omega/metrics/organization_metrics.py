"""A single-tick snapshot of the whole organizational state.

Bundles the cheap-to-compute readings into one dataclass so recorders can append
a time series without recomputing or re-walking the population several times.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from omega.kernel.universe import Universe
from omega.metrics.complexity import shannon_entropy, class_diversity, hierarchy_index
from omega.substrate.gradient import reservoir_pressure


@dataclass(slots=True)
class OrganizationMetrics:
    tick: int
    population: int
    distinct_classes: int
    entropy_bits: float
    hierarchy_index: float
    reservoir_pressure: float
    discovered_transforms: int
    primitive_count: int
    gauges: dict[str, float]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def snapshot_metrics(universe: Universe) -> OrganizationMetrics:
    pop = universe.class_population()
    return OrganizationMetrics(
        tick=universe.tick,
        population=len(universe.organizations),
        distinct_classes=len(pop),
        entropy_bits=shannon_entropy(pop.values()),
        hierarchy_index=hierarchy_index(universe),
        reservoir_pressure=reservoir_pressure(universe),
        discovered_transforms=len(universe.discovered_transforms()),
        primitive_count=len(universe.emergent_primitives),
        gauges=dict(universe.gauges),
    )
