"""The immutable kernel.

Only four things are fixed in Ω and they all live here:

* **Identity**        — an organization is recognizable by the canonical form of
                        its state (``Organization.cls``).
* **Consistency**     — the same state always yields the same identity and the
                        same distinguishability.
* **Causality**       — the universe only changes through ``Reaction`` objects
                        applied by the ``Scheduler``; nothing mutates in place.
* **Conservation of distinguishability** — total distinguishability (bound in
                        organizations + free in the reservoir) is invariant.

Everything else — space, decay rules, interaction operators, even the laws
themselves — is supplied by a ``Physics`` plugin and may be discovered,
rewritten, or abandoned.
"""
from __future__ import annotations

from omega.kernel.organization import Organization, distinguishability, canonical_cls
from omega.kernel.relation import Relation
from omega.kernel.transform import Transform, Reaction, Physics
from omega.kernel.conservation import ConservationError, verify_conservation
from omega.kernel.universe import Universe, OrgStats
from omega.kernel.scheduler import Scheduler, TickReport

__all__ = [
    "Organization",
    "distinguishability",
    "canonical_cls",
    "Relation",
    "Transform",
    "Reaction",
    "Physics",
    "ConservationError",
    "verify_conservation",
    "Universe",
    "OrgStats",
    "Scheduler",
    "TickReport",
]
