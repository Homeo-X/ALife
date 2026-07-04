"""Resource gradient — reading the reservoir as a scarcity signal.

We never implement metabolism. Instead we expose the reservoir as a gradient:
when it is full, construction is cheap; as organizations bind up quanta it
empties, and further construction competes for what remains. Self-maintaining
organizations — ones that keep recreating themselves faster than they decay —
are simply the ones that win that competition. Metabolism, if it appears, is a
strategy discovered against this gradient, not a primitive.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omega.kernel.universe import Universe


def reservoir_pressure(universe: "Universe") -> float:
    """Fraction of total distinguishability currently *bound* in organizations.

    0.0 means everything is free (no scarcity); 1.0 means the reservoir is empty
    and no net-positive construction can occur without something decaying first.
    """
    if universe.total_quanta == 0:
        return 0.0
    return 1.0 - universe.reservoir / universe.total_quanta
