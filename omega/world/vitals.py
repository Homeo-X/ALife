"""Vital signs — making OEE and *life* legible in a running world.

``Observer`` (``observe.py``) shows what a world *is* (a novelty pulse, named lifeforms, collectives,
culture). ``WorldVitals`` shows whether it is *alive and getting better* — the signals the
self-improvement arc (Ω-0.24–0.47) proved matter but the exp030-era world never surfaced:

* **Competence trajectory** — mean collective competence (closure + breed-true + network breadth,
  exp042) and its rolling *slope*. A positive slope is the arc's headline made live: the world is
  getting better at building, not just building more (Ω-0.42, the Catalytic Law).
* **Autocatalytic closure — the life signal** — mean deme closure (exp038: producers∩products /
  producers∪products, →1 for a set that rebuilds its own parts) and the count of collectives above a
  closure threshold that also breed true. These are self-maintaining, heritable individuals — the
  substrate-native definition of *life*.
* **Genuine novelty** — the eviction-robust global rate (Ω-0.39), read off the universe's
  ``classes_ever_seen_global`` (populated when a ``GlobalNoveltySketch`` is attached), so the pulse
  distinguishes *genuinely* new organization from windowed recycling.
* **Ecology** — a Shannon diversity of the live class populations, and the live-collective count.

Like every ``metrics``/``emergence`` reader, this is **strictly observational** — it never mutates
the universe, so a positive reading is evidence about the substrate, not about the instrument
(``ARCHITECTURE.md``). It reads only state the physics/universe already keep.
"""
from __future__ import annotations

import math
from collections import Counter, deque
from statistics import mean


def _slope(points) -> float:
    """Least-squares slope of ``y`` vs ``x`` over ``(x, y)`` points (0 if < 2 or degenerate)."""
    n = len(points)
    if n < 2:
        return 0.0
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


class WorldVitals:
    """Rolling vital-signs reader: call :meth:`sample` each chunk to get the world's live health."""

    def __init__(self, window: int = 120, closure_threshold: float = 0.3) -> None:
        self.closure_threshold = closure_threshold
        self._competence: deque = deque(maxlen=window)   # (tick, mean competence) — for the slope
        self._closure_pulse: deque = deque(maxlen=window)
        self._competence_pulse: deque = deque(maxlen=window)
        self._genuine: deque = deque(maxlen=window)       # (tick, classes_ever_seen_global)

    # ---- read-only helpers ------------------------------------------------
    def _live_demes(self, physics) -> list:
        edges = getattr(physics, "_deme_edges", {}) or {}
        return [pi for pi in list(edges) if edges.get(pi)]

    def _diversity(self, universe) -> float:
        """Shannon diversity (nats) of the live class populations — ecological richness×evenness."""
        pops = Counter(o.cls for o in universe.organizations.values())
        total = sum(pops.values())
        if total <= 0:
            return 0.0
        return -sum((c / total) * math.log(c / total) for c in pops.values() if c)

    # ---- the sample -------------------------------------------------------
    def sample(self, world) -> dict:
        """A snapshot of the world's vital signs (never mutates the world)."""
        p, u = world.physics, world.universe
        tick = u.tick
        live = self._live_demes(p)

        competence = mean(p._deme_competence(pi) for pi in live) if live else 0.0
        closure = mean(p._deme_closure(pi) for pi in live) if live else 0.0

        # "lifeforms": distinct collective signatures that are self-maintaining (closure over
        # threshold). Dedupe by signature so the same community across patches counts once.
        alive_sigs = set()
        breed_true = []
        for pi in live:
            if p._deme_closure(pi) >= self.closure_threshold:
                sig = p._deme_signature(pi)
                if sig:
                    alive_sigs.add(sig)
            bt = getattr(p, "_breedtrue", {}).get(pi)
            if bt is not None:
                breed_true.append(bt)

        # genuine (eviction-robust) novelty rate, if a sketch is attached to the universe
        genuine_distinct = getattr(u, "classes_ever_seen_global", 0)
        self._genuine.append((tick, genuine_distinct))
        genuine_rate = _slope(self._genuine) if len(self._genuine) >= 2 else 0.0

        self._competence.append((tick, competence))
        self._competence_pulse.append(competence)
        self._closure_pulse.append(closure)

        return {
            "tick": tick,
            "competence": competence,
            "competence_slope": _slope(self._competence),
            "closure": closure,
            "lifeforms": len(alive_sigs),               # self-maintaining, distinct collectives
            "breeding_true": mean(breed_true) if breed_true else 0.0,
            "collectives": sum(1 for pi in live if p._deme_signature(pi)),
            "genuine_distinct": genuine_distinct,
            "genuine_novelty_rate": genuine_rate,
            "windowed_novelty_rate": world.novelty.recent_rate(50),
            "diversity": self._diversity(u),
            "competence_pulse": list(self._competence_pulse),
            "closure_pulse": list(self._closure_pulse),
        }
