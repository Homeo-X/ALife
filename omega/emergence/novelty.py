"""Detecting novelty — the anti-closure signal.

Closure, not entropy, is the failure mode this whole project is organized
against. So the central time series is the *novel class discovery rate*: how many
never-before-seen organizational classes appear per tick. A universe that has
exhausted its search space drives this toward zero; an open-ended one keeps it
positive indefinitely.

The tracker is stateful across ticks because "never before seen" is a claim about
the whole history, which the universe's ``class_registry`` already keeps (a class
whose ``first_seen == current tick`` is new). We snapshot the registry size each
tick and difference it — cheap and exact.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from omega.kernel.universe import Universe


@dataclass
class NoveltyTracker:
    #: per-tick count of classes whose first_seen == that tick
    new_per_tick: list[int] = field(default_factory=list)
    cumulative: list[int] = field(default_factory=list)
    #: per-tick GLOBAL (eviction-robust) novelty — only populated when a novelty_sketch is
    #: attached to the universe (harness global_novelty=True); empty otherwise.
    new_per_tick_global: list[int] = field(default_factory=list)
    cumulative_global: list[int] = field(default_factory=list)
    _last_total: int = 0
    _last_total_global: int = 0

    def record(self, universe: Universe) -> int:
        """Call once per tick (after observe_classes). Returns new classes this tick.

        Counts against ``classes_ever_seen`` (a monotonic counter) rather than
        ``len(class_registry)`` so novelty stays exact even when the registry is bounded
        (evicted) on a very long run. The two are identical while nothing is evicted, so
        every existing experiment is byte-identical; under eviction this becomes a
        horizon-windowed novelty (a class absent longer than the horizon and reappearing
        counts as newly discovered — a conservative, memory-bounded rate).

        When the universe carries a ``novelty_sketch`` (an eviction-robust global "ever-seen"
        set), a second, *deduplicated* series is recorded from ``classes_ever_seen_global`` — a
        class that was evicted and reappears is NOT re-counted, so this series strips the
        windowing inflation and measures whether novelty has a genuine positive floor.
        """
        total = universe.classes_ever_seen
        new = total - self._last_total
        self._last_total = total
        self.new_per_tick.append(new)
        self.cumulative.append(total)
        if universe.novelty_sketch is not None:
            tg = universe.classes_ever_seen_global
            self.new_per_tick_global.append(tg - self._last_total_global)
            self._last_total_global = tg
            self.cumulative_global.append(tg)
        return new

    def recent_rate(self, window: int = 50) -> float:
        """Mean new-classes-per-tick over the last ``window`` ticks."""
        if not self.new_per_tick:
            return 0.0
        w = self.new_per_tick[-window:]
        return sum(w) / len(w)

    def is_converging(self, window: int = 50, eps: float = 1e-3) -> bool:
        """True if novelty has effectively stopped — the universe is closing."""
        return self.recent_rate(window) < eps
