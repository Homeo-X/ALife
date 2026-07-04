"""Emergence detectors — read-only analyses over an evolving universe.

These never *drive* the dynamics; they only look. The distinction matters: if a
capability (memory, self-maintenance, copying) had to be detected by machinery
that also produced it, we would be measuring our own code. Detectors here are
strictly observational so that a positive reading is evidence about the
substrate, not about the detector.
"""
from __future__ import annotations

from omega.emergence.persistence import PersistenceTracker, PersistenceSpectrum
from omega.emergence.novelty import NoveltyTracker
from omega.emergence.construction import ConstructionTracker

__all__ = [
    "PersistenceTracker",
    "PersistenceSpectrum",
    "NoveltyTracker",
    "ConstructionTracker",
]
