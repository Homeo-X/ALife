"""Novelty index — instantaneous discovery pressure.

A single scalar in [0, ~] combining how fast genuinely new classes are appearing
with how much of the current population is *recently* new. Used both as a live
signal and as an input to the aggregate open-endedness index.
"""
from __future__ import annotations

from omega.emergence.novelty import NoveltyTracker


def novelty_index(tracker: NoveltyTracker, window: int = 50) -> float:
    """Recent new-class rate, normalized to be comparable across run lengths.

    Returns new classes per tick averaged over ``window``. Zero means closure.
    """
    return tracker.recent_rate(window)
