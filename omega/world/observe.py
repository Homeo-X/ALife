"""Observability — making the living world legible.

The engine's state is dicts of hashes and counts. A *world* is something you can watch: a
pulse of never-ending novelty, a roster of named living individuals born and dying, cultures
spreading, an alphabet of constructed primitives growing. ``Observer`` turns the live
``World`` state into that picture each time it is called — all from state the engine already
keeps (``NoveltyTracker``, ``physics._deme_signature``/``_deme_edges``, ``physics._reified``,
``universe.class_registry``, the culture counters) — and diffs consecutive snapshots into a
rolling **event feed** (a lifeform appears, a lifeform is gone, a new primitive is reified).

Names are deterministic functions of identity (a signature's edge-set, a class hash), so the
same lifeform keeps the same name across snapshots and across a checkpoint/resume.
"""
from __future__ import annotations

from collections import deque

_CONS = "bdfgklmnprstvz"
_VOWL = "aeiou"


def _name(key: str) -> str:
    """A stable, pronounceable name derived deterministically from an identity string."""
    h = 1469598103934665603
    for ch in key:                       # FNV-1a — stdlib-only, deterministic
        h = ((h ^ ord(ch)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    syl = 3 if (h & 1) else 2
    out = []
    for _ in range(syl):
        out.append(_CONS[h % len(_CONS)]); h //= len(_CONS)
        out.append(_VOWL[h % len(_VOWL)]); h //= len(_VOWL)
    return "".join(out).capitalize()


class Observer:
    """Rolling observer: call :meth:`snapshot` each chunk to get the world's live picture."""

    def __init__(self, pulse_len: int = 120, event_len: int = 60) -> None:
        self._pulse: deque = deque(maxlen=pulse_len)   # novelty-rate history (the "pulse")
        self._events: deque = deque(maxlen=event_len)
        self._reified_seen: int = 0
        self._known_lifeforms: set[str] = set()        # class-names ever notable

    def _collectives(self, world) -> list[dict]:
        """Live **collectives** — demes carrying a non-trivial cross-production network
        signature. These are the research's collective individuals; they are genuinely
        *transient communities* (networks reconfigure each generation), so we report the
        current roster, not ages."""
        p = world.physics
        seen: dict[str, dict] = {}
        for pi in list(getattr(p, "_deme_edges", {}) or {}):
            sig = p._deme_signature(pi)
            if not sig:
                continue
            name = _name(repr(sorted(sig)))
            if name not in seen:                 # dedupe identical signatures (same community)
                seen[name] = {"name": name, "size": len(sig), "patches": 1}
            else:
                seen[name]["patches"] += 1
        return sorted(seen.values(), key=lambda d: (-d["size"], d["name"]))

    def _lifeforms(self, universe) -> list[dict]:
        """Stable, named **lifeforms** — the persistent organizational classes, with real
        ages (``ticks_present``). These are the characters a viewer follows over time."""
        forms = sorted(universe.class_registry.values(),
                       key=lambda r: (r.ticks_present, r.peak_population), reverse=True)[:10]
        return [{"name": _name(r.cls), "age": r.ticks_present, "peak": r.peak_population,
                 "depth": r.depth, "size": r.size} for r in forms]

    def snapshot(self, world) -> dict:
        u, p = world.universe, world.physics
        nov_rate = world.novelty.recent_rate(window=min(2000, max(50, u.tick // 10 or 50)))
        self._pulse.append(round(nov_rate, 4))

        collectives = self._collectives(world)
        lifeforms = self._lifeforms(u)

        # events (meaningful, not per-frame churn): a new lifeform reaches the roster, and a
        # persistent motif is reified into a new primitive (a real construction event).
        for lf in lifeforms:
            if lf["age"] >= 200 and lf["name"] not in self._known_lifeforms:
                self._known_lifeforms.add(lf["name"])
                self._events.appendleft({"tick": u.tick, "kind": "lifeform",
                                         "text": f"lifeform {lf['name']} endures "
                                                 f"(age {lf['age']}, depth {lf['depth']})"})
        reified = len(getattr(p, "_reified", {}))
        if reified > self._reified_seen:
            self._events.appendleft({"tick": u.tick, "kind": "reify",
                                     "text": f"a persistent motif became a new primitive "
                                             f"(alphabet now {len(p.atoms)})"})
            self._reified_seen = reified

        meme_h = int(getattr(p, "_meme_horizontal", 0))
        meme_v = int(getattr(p, "_meme_vertical", 0))
        return {
            "tick": u.tick,
            "population": len(u.organizations),
            "reservoir": u.reservoir,
            "novelty_rate": round(nov_rate, 4),
            "novelty_pulse": list(self._pulse),
            "classes_ever": u.classes_ever_seen,
            "registry_size": len(u.class_registry),      # bounded (windowed)
            "alphabet": len(p.atoms),
            "reified": reified,
            "culture": {"horizontal": meme_h, "vertical": meme_v,
                        "ratio": round(meme_h / meme_v, 3) if meme_v else 0.0},
            "collectives": collectives,
            "n_collectives": len(collectives),
            "lifeforms": lifeforms,
            "events": list(self._events),
        }
