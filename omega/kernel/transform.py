"""Transforms, Reactions, and the Physics plugin interface.

Axiom 4 (Constraint) and Axiom 5 (Novel Construction) live here.

A **Transform** is a partial, constrained rule that turns input organizations
into output states. Crucially the set of transforms is *not* fixed: it lives in
the ``Universe`` and a ``Physics`` plugin may add operators that organizations
themselves have discovered (constructed laws). This is the mechanism by which
the universe enlarges its own possibility space.

A **Reaction** is a concrete, proposed event: "consume these organizations,
produce these states, via this transform." The scheduler is the only thing that
may enact a reaction, and only if it conserves distinguishability. Nothing
mutates in place — causality flows exclusively through reactions.

A **Physics** is the pluggable law-set for an experiment. It seeds the universe
and, each tick, proposes reactions. Dependency inversion: the kernel knows the
``Physics`` protocol, never a concrete physics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Protocol, Sequence, runtime_checkable

from omega.kernel.organization import Organization, State

if TYPE_CHECKING:  # avoid import cycle; Universe imports Transform types
    from omega.kernel.universe import Universe
    from omega.substrate.noise import Noise


@dataclass(frozen=True, slots=True)
class Reaction:
    """A proposed causal event.

    ``inputs`` are the uids consulted. ``consume`` lists the subset actually
    destroyed (catalysts appear in ``inputs`` but not in ``consume``).
    ``outputs`` are the (state, kind) pairs to create. ``via`` names the
    transform, for provenance and the interaction graph.
    """

    inputs: tuple[int, ...]
    consume: tuple[int, ...]
    outputs: tuple[tuple[State, str], ...]
    via: str = "?"

    @property
    def is_spontaneous(self) -> bool:
        """A reaction with no inputs draws novelty straight from the reservoir."""
        return not self.inputs


# A transform's callable form: given the input organizations and an RNG, return
# the output states (or None if it declines to fire on these inputs).
TransformFn = Callable[
    [Sequence[Organization], "Noise"],
    "Sequence[tuple[State, str]] | None",
]


@dataclass(frozen=True, slots=True)
class Transform:
    """A named, arity-typed interaction rule.

    ``catalytic`` transforms do not consume their inputs (they act like enzymes),
    which is what lets an operator drive construction repeatedly. ``discovered``
    marks transforms that were *invented* by organizations at runtime rather than
    seeded — the population of discovered transforms is a direct open-endedness
    signal.
    """

    name: str
    arity: int
    fn: TransformFn
    catalytic: bool = False
    discovered: bool = False
    origin_cls: str | None = None  # class of the organization that authored it


@runtime_checkable
class Physics(Protocol):
    """The pluggable law-set for an experiment (dependency-inversion boundary)."""

    name: str

    def seed(self, universe: "Universe", rng: "Noise") -> None:
        """Populate the fresh universe (draws its material from the reservoir)."""
        ...

    def propose(self, universe: "Universe", rng: "Noise") -> Sequence[Reaction]:
        """Return the reactions to attempt this tick (may consult transforms)."""
        ...
