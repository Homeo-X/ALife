"""Detecting persistence — Axiom 3, made measurable (and de-confounded).

Identity is *continued recognizability*. The naive reading — "a class was present
for many ticks" — is a trap: with a decay hazard *h*, every organization, even a
random one, survives ~1/h ticks, so its class looks present for ~1/h ticks
without anything being maintained. That measures the decay constant, not
organization.

The de-confounded signal is **re-formation**: how many times a class was
independently (re)created (``ClassRecord.births``). A one-off noise string is born
once and never returns (births == 1). A composite that the dynamics keep
regenerating from a feed is born again and again (births >> 1), *even as its
individual instances decay*. Re-formation is exactly persistence-through-flux, and
it is immune to the 1/h artefact.

We further separate **composed** persistence (classes that bind >= 2 atomic
differences and re-form) from flat persistence (single-difference monomers that
re-form). A lone difference is not yet an *arrangement*; it is composed
persistence — a maintained arrangement of interacting differences — that answers
"can stable organizations emerge?".
"""
from __future__ import annotations

from dataclasses import dataclass

from omega.kernel.universe import Universe


@dataclass
class PersistenceSpectrum:
    lifespans: list[int]              # last_seen - first_seen, per class
    reformations: list[int]           # births, per class
    max_lifespan: int
    mean_lifespan: float
    max_reformations: int
    reformed_fraction: float          # fraction of classes with births >= threshold
    composed_persistent: int          # count of depth>=1 classes with births >= threshold
    reform_threshold: int

    def summary(self) -> str:
        return (
            f"classes={len(self.lifespans)} max_life={self.max_lifespan} "
            f"max_reform={self.max_reformations} "
            f"reformed(>={self.reform_threshold})={self.reformed_fraction:.3f} "
            f"composed_persistent={self.composed_persistent}"
        )


class PersistenceTracker:
    """Computes the (re-formation-based) persistence spectrum."""

    def __init__(self, reform_threshold: int = 3) -> None:
        self.threshold = reform_threshold

    def spectrum(self, universe: Universe) -> PersistenceSpectrum:
        records = list(universe.class_registry.values())
        if not records:
            return PersistenceSpectrum([], [], 0, 0.0, 0, 0.0, 0, self.threshold)
        lifespans = [r.last_seen - r.first_seen for r in records]
        reformations = [r.births for r in records]
        reformed = sum(1 for r in records if r.births >= self.threshold)
        composed_persistent = sum(
            1 for r in records if r.size >= 2 and r.births >= self.threshold
        )
        return PersistenceSpectrum(
            lifespans=lifespans,
            reformations=reformations,
            max_lifespan=max(lifespans),
            mean_lifespan=sum(lifespans) / len(lifespans),
            max_reformations=max(reformations),
            reformed_fraction=reformed / len(records),
            composed_persistent=composed_persistent,
            reform_threshold=self.threshold,
        )
