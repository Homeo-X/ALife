"""Ω World — the research engine as a persistent, watchable living world.

`World` (runtime) runs the engine forever at flat memory; `checkpoint` lets a world survive
restarts; `observe.world_snapshot` makes it legible; `dashboard` lets you watch it live.
"""
from omega.world.runtime import World
from omega.world import checkpoint

__all__ = ["World", "checkpoint"]
