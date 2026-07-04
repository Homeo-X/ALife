"""Detecting construction — Axiom 5, the engine of open-endedness.

Two things are worth watching:

* **Compositional depth.** Organizations built out of other organizations are
  structurally deeper. A rising maximum/typical depth means the universe is
  building *hierarchy*, not just churning flat strings.

* **Discovered operators.** The sharpest open-endedness signal: transforms that
  organizations authored at runtime and added to the law registry. Each one
  literally enlarges the set of reachable states. We track how many exist and how
  many are *meta* — operators whose action can, in turn, mint operators.

This detector is observational; the actual authoring of operators is done by the
Physics for the experiment that permits it (exp003).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from omega.kernel.universe import Universe


@dataclass
class ConstructionTracker:
    max_depth_seen: int = 0
    depth_per_tick: list[int] = field(default_factory=list)
    discovered_per_tick: list[int] = field(default_factory=list)

    def record(self, universe: Universe) -> None:
        depths = [o.depth for o in universe.organizations.values()]
        cur_max = max(depths) if depths else 0
        self.max_depth_seen = max(self.max_depth_seen, cur_max)
        self.depth_per_tick.append(cur_max)
        self.discovered_per_tick.append(len(universe.discovered_transforms()))

    @property
    def operator_growth(self) -> int:
        """Net discovered operators over the *whole* run (final minus initial).

        WARNING: this is cumulative. A universe that discovers a finite burst of
        operators and then freezes has a large positive ``operator_growth`` yet is
        completely closed. Do **not** use this as an open-endedness gate — use
        :meth:`recent_operator_rate`, which measures whether discovery is *still
        happening*. (This lesson cost us the v0.1 headline; see RESEARCH_LOG.)
        """
        if not self.discovered_per_tick:
            return 0
        return self.discovered_per_tick[-1] - self.discovered_per_tick[0]

    def recent_operator_rate(self, window: int = 50) -> float:
        """New operators discovered per tick over the last ``window`` ticks.

        This is the honest open-endedness signal for the law set: if it decays to
        ~0 the universe has stopped enlarging its own possibility space, no matter
        how many operators it discovered earlier.
        """
        series = self.discovered_per_tick
        if len(series) < 2:
            return 0.0
        w = min(window, len(series) - 1)
        return (series[-1] - series[-1 - w]) / w
