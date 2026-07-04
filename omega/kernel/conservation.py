"""Conservation of distinguishability — the one law that never bends.

The universe holds a fixed total of atomic differences, ``total_quanta``. At
every instant each quantum is either *bound* inside an organization or *free* in
the reservoir:

    reservoir + sum(org.distinguishability for org in universe) == total_quanta

Novelty in Ω is therefore always *recombination*, never inflation — you cannot
conjure organization from nothing, only rearrange what exists. This is what
makes the reservoir a genuine resource gradient: when it empties, construction
stalls and organizations must compete for the bound quanta, and *that* pressure
(not a hand-coded fitness) is where selection comes from.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omega.kernel.universe import Universe


class ConservationError(RuntimeError):
    """Raised when the distinguishability books do not balance — a kernel bug."""


def verify_conservation(universe: "Universe") -> int:
    """Assert the invariant and return the (constant) total.

    Called every tick by the scheduler. A violation means a reaction or decay
    path failed to account for quanta — it is never an emergent phenomenon, it is
    always a defect, so we raise rather than warn.
    """
    bound = sum(org.distinguishability for org in universe.organizations.values())
    total = universe.reservoir + bound
    if total != universe.total_quanta:
        raise ConservationError(
            f"distinguishability not conserved at tick {universe.tick}: "
            f"reservoir={universe.reservoir} + bound={bound} = {total} "
            f"!= total_quanta={universe.total_quanta}"
        )
    return total
