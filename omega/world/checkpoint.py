"""Checkpoint / resume — how a world survives restarts and accretes history.

A world is meant to run for millions of ticks across many sessions (and this environment
reclaims its container when idle), so a world must be able to **snapshot its exact live
state and resume byte-identically**. The single entropy source is the RNG, so capturing its
internal state (``Noise.getstate``) plus the universe, the physics (whose large mutable state
lives *outside* the universe — ``_deme_edges``, ``_hered_*``, ``_reified``, ``atoms`` …), and
the trackers is necessary and sufficient. The scheduler is rebuilt on load, not pickled.

Determinism contract (pinned by ``test_world``): resume-then-continue N ticks is identical
to run-through N ticks. Bounded memory keeps the pickle small even after millions of ticks.
"""
from __future__ import annotations

import os
import pickle
import tempfile
from pathlib import Path

from omega.world.runtime import World

FORMAT = 1


def save(world: World, path: str | Path) -> None:
    """Atomically pickle the world's state bundle to ``path``."""
    payload = {"format": FORMAT, "tick": world.tick, "bundle": world.bundle()}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # atomic write: a mid-write crash must never corrupt an existing good checkpoint.
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def load(path: str | Path) -> World:
    """Rebuild a world from a checkpoint written by :func:`save`."""
    with open(path, "rb") as f:
        payload = pickle.load(f)
    if payload.get("format") != FORMAT:
        raise ValueError(f"unsupported checkpoint format {payload.get('format')!r}")
    return World.from_bundle(payload["bundle"])


def exists(path: str | Path) -> bool:
    return Path(path).is_file()
