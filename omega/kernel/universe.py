"""The Universe — the mutable world state and the only place reactions land.

The universe is a *soup*, not a grid: an unordered collection of organizations
plus a reservoir of free distinguishability and a registry of currently-valid
transforms. There is no space. If spatial structure ever matters it must arise
as a constraint a Physics imposes on which organizations may react — it is never
assumed here.

Responsibilities:

* hold organizations, their per-instance stats, and the reservoir;
* enact reactions atomically and conservatively (the *only* mutation path);
* keep a class registry so persistence and novelty can be measured over
  *classes* (continued recognizability) rather than instances;
* hold the mutable transform registry that Physics plugins grow at runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from omega.kernel.conservation import verify_conservation
from omega.kernel.organization import Organization, State, distinguishability
from omega.kernel.relation import Relation
from omega.kernel.transform import Reaction, Transform


@dataclass(slots=True)
class OrgStats:
    """Per-instance history — kept off the frozen Organization for cleanliness."""

    birth_tick: int
    age: int = 0
    reproductions: int = 0       # how many reactions used this org as an input
    recent_activity: float = 0.0  # leaky count of recent participations (function)


@dataclass
class ClassRecord:
    """Aggregate history of a *class* (an equivalence set of recognizable states)."""

    cls: str
    first_seen: int
    last_seen: int
    peak_population: int = 0
    total_observations: int = 0  # summed population over ticks it was present
    ticks_present: int = 0
    births: int = 0               # times an instance of this class was (re)created
    depth: int = 0                # compositional depth of the arrangement
    size: int = 0                 # distinguishability (atomic differences bound)
    kind: str = ""                # representative kind tag
    rep_state: tuple = ()         # a representative state (for reification etc.)


class Universe:
    """The world. Constructed empty; a Physics seeds it from the reservoir."""

    def __init__(self, total_quanta: int) -> None:
        self.total_quanta: int = total_quanta
        self.reservoir: int = total_quanta
        self.tick: int = 0

        self.organizations: dict[int, Organization] = {}
        self.stats: dict[int, OrgStats] = {}
        self.transforms: list[Transform] = []
        self.class_registry: dict[str, ClassRecord] = {}
        # Monotonic count of *distinct classes ever seen*. Equals len(class_registry)
        # exactly while nothing is evicted, but survives eviction — so novelty (which is
        # this count differenced over ticks) stays exact even when the registry is bounded
        # for a very long run. This decoupling is what lets the registry shrink.
        self.classes_ever_seen: int = 0
        # Optional eviction-robust GLOBAL novelty estimator (a scalable Bloom "ever-seen" set).
        # Off (None) by default => never touched => every experiment byte-identical. When the harness
        # attaches one (global_novelty=True), a class is counted here only the FIRST time it is ever
        # seen — an evicted class that reappears is recognized as old, stripping the windowed-novelty
        # inflation that bounded memory otherwise introduces (see omega/emergence/global_novelty.py).
        self.novelty_sketch = None
        self.classes_ever_seen_global: int = 0
        self.class_births: dict[str, int] = {}  # lifetime (re)creation count per class
        self.class_fed: dict[str, int] = {}      # births from the reservoir (feed)
        self.class_constructed: dict[str, int] = {}  # births from other organizations
        self.relations: list[Relation] = []
        # Runtime-minted primitives (Axiom 1 + Axiom 5): new atomic *kinds of
        # difference* that did not exist when the universe began. An empty set is
        # the norm; only a Physis that reifies persistent structure grows it.
        self.emergent_primitives: set = set()
        # Free-form scalar observables a Physics may publish each tick (e.g. the
        # reification lineage depth). Copied into every metrics snapshot. Keeps
        # experiment-specific instrumentation out of the kernel's fixed schema.
        self.gauges: dict[str, float] = {}

        self._next_uid: int = 0
        # counters, reset each tick, surfaced in the tick report
        self.reactions_committed: int = 0
        self.reactions_blocked: int = 0
        self.decayed: int = 0

        # Long-run (bounded-memory) mode. Both 0 by default => nothing is ever evicted and
        # every existing experiment is byte-identical. When a Physics/harness sets a
        # positive horizon, cold class records (and, past a cap, old provenance relations)
        # are evicted each tick so memory stays flat over 10^6+ ticks. classes_ever_seen
        # is never decremented, so the novelty *count* stays exact (see bound_memory).
        self.memory_horizon: int = 0
        self.relation_cap: int = 0
        # Eviction is amortized: the O(registry) cold-scan runs every N ticks, not every
        # tick (which would roughly double per-tick cost at a large horizon). Between scans
        # the registry overshoots by ~N×(new/tick) — negligible vs the horizon.
        self.memory_evict_interval: int = 512

    # ---- identity minting -------------------------------------------------
    def mint_uid(self) -> int:
        uid = self._next_uid
        self._next_uid += 1
        return uid

    # ---- construction / destruction of organizations ----------------------
    def spawn(self, state: State, kind: str, parents: tuple[int, ...] = ()) -> Organization | None:
        """Bind ``distinguishability(state)`` quanta from the reservoir into a new
        organization. Returns None (and does nothing) if the reservoir cannot
        cover it — conservation is never violated to force a birth.
        """
        need = distinguishability(state)
        if need > self.reservoir:
            return None
        uid = self.mint_uid()
        org = Organization(uid=uid, state=state, kind=kind,
                           birth_tick=self.tick, lineage=parents)
        self.organizations[uid] = org
        self.stats[uid] = OrgStats(birth_tick=self.tick)
        self.reservoir -= need
        cls = org.cls
        self.class_births[cls] = self.class_births.get(cls, 0) + 1
        return org

    def dissolve(self, uid: int) -> None:
        """Remove an organization and return its quanta to the reservoir."""
        org = self.organizations.pop(uid, None)
        if org is None:
            return
        self.stats.pop(uid, None)
        self.reservoir += org.distinguishability

    # ---- the single causal path -------------------------------------------
    def apply_reaction(self, reaction: Reaction) -> bool:
        """Attempt a reaction atomically and conservatively.

        Net quanta needed = (quanta in outputs) - (quanta freed by consumed
        inputs). If the reservoir cannot cover a positive net, the reaction is
        blocked and the world is left untouched. Otherwise inputs in ``consume``
        are dissolved, outputs are spawned, and provenance relations recorded.
        """
        # inputs must still exist (a prior reaction this tick may have eaten them)
        for uid in reaction.inputs:
            if uid not in self.organizations:
                self.reactions_blocked += 1
                return False

        freed = sum(self.organizations[u].distinguishability for u in reaction.consume)
        needed = sum(distinguishability(s) for s, _ in reaction.outputs)
        available = self.reservoir + freed  # freed quanta become available too
        if needed > available:
            self.reactions_blocked += 1
            return False

        # credit inputs' reproduction count and recent activity (they participated;
        # activity is what a Physics can couple persistence to, i.e. *function*)
        for uid in reaction.inputs:
            st = self.stats.get(uid)
            if st is not None:
                st.reproductions += 1
                st.recent_activity += 1.0

        parents = tuple(reaction.inputs)
        spontaneous = reaction.is_spontaneous
        for uid in reaction.consume:
            self.dissolve(uid)
        for state, kind in reaction.outputs:
            child = self.spawn(state, kind, parents=parents)
            if child is not None:
                # amplification bookkeeping: was this output conjured from the
                # reservoir (a "feed") or *constructed* by other organizations? A
                # class constructed far more than it is fed is being amplified by
                # the soup — the signature of an emergent replicator.
                if spontaneous:
                    self.class_fed[child.cls] = self.class_fed.get(child.cls, 0) + 1
                else:
                    self.class_constructed[child.cls] = self.class_constructed.get(child.cls, 0) + 1
                for p in parents:
                    self.relations.append(
                        Relation(source=p, target=child.uid, via=reaction.via, tick=self.tick)
                    )
        self.reactions_committed += 1
        return True

    def amplification(self) -> tuple[float, str | None]:
        """Max over classes of constructed/(fed+1) — the top self-amplification,
        and the class achieving it. >>1 means a class the soup keeps rebuilding
        far beyond what the feed supplies: an emergent replicator."""
        best, who = 0.0, None
        for cls, c in self.class_constructed.items():
            amp = c / (self.class_fed.get(cls, 0) + 1)
            if amp > best:
                best, who = amp, cls
        return best, who

    # ---- transform registry (constructed laws) ----------------------------
    def register_transform(self, transform: Transform) -> None:
        self.transforms.append(transform)

    def discovered_transforms(self) -> list[Transform]:
        return [t for t in self.transforms if t.discovered]

    def register_primitive(self, symbol) -> None:
        """Mint a new atomic kind of difference discovered at runtime."""
        self.emergent_primitives.add(symbol)

    # ---- census -----------------------------------------------------------
    def _bound(self) -> int:
        return sum(o.distinguishability for o in self.organizations.values())

    def class_population(self) -> dict[str, int]:
        pop: dict[str, int] = {}
        for org in self.organizations.values():
            pop[org.cls] = pop.get(org.cls, 0) + 1
        return pop

    def observe_classes(self) -> dict[str, int]:
        """Update the class registry from the current population and return the
        current per-class population. This is how *continued recognizability*
        (persistence) is accumulated over time.
        """
        pop: dict[str, int] = {}
        rep: dict[str, Organization] = {}
        for org in self.organizations.values():
            pop[org.cls] = pop.get(org.cls, 0) + 1
            rep.setdefault(org.cls, org)
        for cls, n in pop.items():
            rec = self.class_registry.get(cls)
            if rec is None:
                example = rep[cls]
                rec = ClassRecord(cls=cls, first_seen=self.tick, last_seen=self.tick,
                                  depth=example.depth, size=example.distinguishability,
                                  kind=example.kind, rep_state=example.state)
                self.class_registry[cls] = rec
                self.classes_ever_seen += 1
                if self.novelty_sketch is not None and self.novelty_sketch.add_if_new(cls):
                    self.classes_ever_seen_global += 1
            rec.last_seen = self.tick
            rec.peak_population = max(rec.peak_population, n)
            rec.total_observations += n
            rec.ticks_present += 1
            rec.births = self.class_births.get(cls, rec.births)
        if (self.memory_horizon or self.relation_cap) and \
                self.tick % self.memory_evict_interval == 0:
            self.bound_memory()
        return pop

    def bound_memory(self) -> None:
        """Long-run mode: evict cold state so memory stays bounded over 10^6+ ticks.

        A class not seen for ``memory_horizon`` ticks is dropped from the registry and
        from the per-class amplification tallies — so ``amplification()``'s scan (over
        ``class_constructed``) stays bounded too, with no need for incremental tracking.
        ``classes_ever_seen`` is *not* decremented, so the novelty **count** stays exact;
        a class that reappears after eviction is counted as a fresh discovery (a
        horizon-windowed novelty). Lifetime-aggregate readers (persistence spectrum,
        amplification) thereby become horizon-windowed — the price of a bounded registry.
        Old provenance ``relations`` past ``relation_cap`` are trimmed (only exp011 reads
        them, and never in this mode). Both knobs 0 => this method is never called.
        """
        h = self.memory_horizon
        if h > 0:
            cutoff = self.tick - h
            if cutoff > 0:
                cold = [c for c, r in self.class_registry.items() if r.last_seen < cutoff]
                for c in cold:
                    del self.class_registry[c]
                    self.class_births.pop(c, None)
                    self.class_fed.pop(c, None)
                    self.class_constructed.pop(c, None)
        cap = self.relation_cap
        if cap > 0 and len(self.relations) > cap:
            del self.relations[:-cap]

    def verify(self) -> int:
        return verify_conservation(self)
