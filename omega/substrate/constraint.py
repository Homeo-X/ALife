"""Constraints — Axiom 4. Not every interaction is possible.

A ``Constraint`` is just a predicate over a tuple of candidate input
organizations: it returns True if the interaction is *permitted*. Constraints
are the vocabulary a Physics uses to carve its lawful reactions out of the space
of all conceivable ones. Keeping them as small composable objects means a
Physics can build complex admissibility rules — and, later, organizations could
in principle author their own.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from omega.kernel.organization import Organization

Predicate = Callable[[Sequence[Organization]], bool]


@dataclass(frozen=True, slots=True)
class Constraint:
    name: str
    predicate: Predicate

    def __call__(self, inputs: Sequence[Organization]) -> bool:
        return self.predicate(inputs)


def all_of(*constraints: Constraint) -> Constraint:
    return Constraint(
        name="all(" + ",".join(c.name for c in constraints) + ")",
        predicate=lambda inputs: all(c(inputs) for c in constraints),
    )


def any_of(*constraints: Constraint) -> Constraint:
    return Constraint(
        name="any(" + ",".join(c.name for c in constraints) + ")",
        predicate=lambda inputs: any(c(inputs) for c in constraints),
    )
