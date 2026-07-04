"""Metrics — the only scorecard that matters.

The manifesto forbids the usual ALife vanity metrics (population, fitness,
species count) because they all saturate. We measure the things that *should not*
saturate in an open-ended universe:

* novel organization discovery rate      (:mod:`novelty_index`)
* rate of new organizational classes      (:mod:`novelty_index`)
* organizational depth / hierarchy         (:mod:`complexity`)
* persistence spectrum                      (:mod:`organization_metrics`)
* recursive innovation / meta-operators     (:mod:`openendedness`)
* an aggregate Open-Endedness Index         (:mod:`openendedness`)

If the Open-Endedness Index trends to zero, the universe has failed — that is the
falsification condition for the whole program.
"""
from __future__ import annotations

from omega.metrics.organization_metrics import OrganizationMetrics, snapshot_metrics
from omega.metrics.complexity import shannon_entropy, class_diversity, hierarchy_index
from omega.metrics.novelty_index import novelty_index
from omega.metrics.openendedness import OpenEndednessReport, open_endedness_index
from omega.metrics.construction_quality import ConstructionQuality, construction_quality
from omega.metrics.ecology import EcologyReport, analyze as analyze_ecology

__all__ = [
    "EcologyReport",
    "analyze_ecology",
    "OrganizationMetrics",
    "snapshot_metrics",
    "shannon_entropy",
    "class_diversity",
    "hierarchy_index",
    "novelty_index",
    "OpenEndednessReport",
    "open_endedness_index",
    "ConstructionQuality",
    "construction_quality",
]
