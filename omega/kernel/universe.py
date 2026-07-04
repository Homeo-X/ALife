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
            rec.last_seen = self.tick
            rec.peak_population = max(rec.peak_population, n)
            rec.total_observations += n
            rec.ticks_present += 1
            rec.births = self.class_births.get(cls, rec.births)
        return pop

    def verify(self) -> int:
        return verify_conservation(self)
