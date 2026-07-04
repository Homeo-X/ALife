"""The Organization — the only primitive in Ω.

An Organization is *a persistent arrangement of interacting differences*. We
represent that arrangement as a nested tuple of atomic symbols (``state``).
Atomic symbols are the irreducible "differences" of Axiom 1; a tuple groups them
into a distinguishable, recognizable whole.

Two design commitments encode the immutable kernel:

* **Identity is continued recognizability, not an object.** An organization's
  *class* is the canonical hash of its state (:func:`canonical_cls`). Two
  instances with the same state are the same *kind* of organization even if they
  have different histories. Persistence is measured over classes, not uids.

* **Distinguishability is conserved.** :func:`distinguishability` counts the
  atomic differences an organization binds up. The universe may rearrange them
  but never create or destroy them (see :mod:`omega.kernel.conservation`).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Iterable

# An atomic difference is any hashable, non-tuple value (int, str, ...).
Atom = Any
# A state is a (possibly nested) tuple of atoms — the "arrangement".
State = tuple


def _iter_atoms(state: Any) -> Iterable[Atom]:
    if isinstance(state, tuple):
        for part in state:
            yield from _iter_atoms(part)
    else:
        yield state


def distinguishability(state: Any) -> int:
    """Number of atomic differences bound up in ``state``.

    This is the conserved quantity of the universe. An atom contributes 1; a
    tuple contributes the sum of its parts. The empty tuple contributes 0.
    """
    return sum(1 for _ in _iter_atoms(state))


def canonical_cls(state: Any) -> str:
    """Stable class identity for a state — its *continued recognizability*.

    Uses a canonical textual encoding so that structurally identical states map
    to the same class regardless of how or when they were constructed.
    """
    encoded = repr(state).encode("utf-8")
    return hashlib.sha1(encoded).hexdigest()[:16]


@dataclass(frozen=True, slots=True)
class Organization:
    """A persistent arrangement of interacting differences.

    Instances are immutable (causality flows only through new instances). The
    dynamic bookkeeping — age, reproduction count, persistence score — lives in
    :class:`omega.kernel.universe.OrgStats`, keyed by ``uid``, so that identity
    (the state) stays cleanly separated from history.
    """

    uid: int
    state: State
    kind: str = "organization"
    birth_tick: int = 0
    lineage: tuple[int, ...] = field(default=())

    @property
    def cls(self) -> str:
        """Class identity — what makes this organization *recognizable*."""
        return canonical_cls(self.state)

    @property
    def distinguishability(self) -> int:
        """Atomic differences this organization binds (its conserved 'mass')."""
        return distinguishability(self.state)

    @property
    def depth(self) -> int:
        """Structural (compositional) depth of the arrangement."""
        return _depth(self.state)

    def relabelled(self, uid: int, tick: int, parents: tuple[int, ...]) -> "Organization":
        """Return a copy stamped with a new identity/history (same state)."""
        return Organization(
            uid=uid, state=self.state, kind=self.kind,
            birth_tick=tick, lineage=parents,
        )


def _depth(state: Any) -> int:
    if not isinstance(state, tuple) or not state:
        return 0
    return 1 + max(_depth(part) for part in state)
