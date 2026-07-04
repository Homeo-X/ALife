"""Experiment 002 — Local interaction. *Can stable organizations emerge?*

We add exactly one thing to the null: a *constraint-gated binding interaction*.
The alphabet is now small (a handful of complementary types). Two free monomers
of complementary type may bind into a composite ``('bond', x, y)`` — a genuine
multi-difference arrangement. Nothing gives composites a survival bonus; they
decay under the same uniform hazard as everything else.

Persistence of composites is therefore *emergent flux balance*: composites are
continually re-formed from the monomer feed as fast as they decay, so a small set
of composite classes stays present across the whole run. A correlation between
two differences persists longer than either difference is individually injected —
that is stable organization, arising without being implemented.

Matched control (``bind=False``): identical small-alphabet monomer feed, binding
disabled. Monomers (depth 0) still recur, but **no depth-1 organization ever
persists**. So the discriminator is not "does anything persist" but "does a
*composed* organization persist" — read off ``hierarchy_index`` and the lifespan
of depth>=1 classes.
"""
from __future__ import annotations

from omega.config import Config
from omega.experiments.registry import register
from omega.kernel.organization import Organization
from omega.kernel.transform import Physics, Reaction
from omega.kernel.universe import Universe
from omega.substrate.gradient import reservoir_pressure
from omega.substrate.noise import Noise

# A small set of types with a fixed complementary pairing (Axiom 4 constraint):
#   A binds B, C binds D. Nothing else binds.
_TYPES = ("A", "B", "C", "D")
_COMPLEMENT = {"A": "B", "B": "A", "C": "D", "D": "C"}


class BindingPhysics:
    name = "exp002_persistence"

    def __init__(self, bind: bool = True, feed_rate: int = 30,
                 bind_attempts: int = 40) -> None:
        self.bind = bind
        self.feed_rate = feed_rate
        self.bind_attempts = bind_attempts

    def seed(self, universe: Universe, rng: Noise) -> None:
        for _ in range(self.feed_rate * 2):
            universe.spawn((rng.choice(_TYPES),), kind="monomer")

    def propose(self, universe: Universe, rng: Noise):
        reactions = []
        # 1) steady monomer feed from the reservoir (throttled by scarcity)
        budget = int(self.feed_rate * (1.0 - reservoir_pressure(universe)))
        for _ in range(max(budget, 1)):
            t = rng.choice(_TYPES)
            reactions.append(Reaction(inputs=(), consume=(),
                                      outputs=(((t,), "monomer"),), via="feed"))

        # 2) constraint-gated binding: complementary monomers form a composite
        if self.bind:
            monomers = [o for o in universe.organizations.values() if o.kind == "monomer"]
            rng.shuffle(monomers)
            paired: set[int] = set()
            for i in range(0, len(monomers) - 1, 2):
                if len([r for r in reactions if r.via == "bind"]) >= self.bind_attempts:
                    break
                a, b = monomers[i], monomers[i + 1]
                if a.uid in paired or b.uid in paired:
                    continue
                ta, tb = a.state[0], b.state[0]
                if _COMPLEMENT.get(ta) == tb:  # only complementary pairs bind
                    composite = ("bond", ta, tb)
                    reactions.append(Reaction(
                        inputs=(a.uid, b.uid), consume=(a.uid, b.uid),
                        outputs=((composite, "composite"),), via="bind"))
                    paired.add(a.uid); paired.add(b.uid)
        return reactions


@register("exp002")
def build(seed: int = 0, **overrides) -> tuple[Physics, Config]:
    bind = overrides.get("bind", True)
    cfg = Config(
        experiment="exp002",
        seed=seed,
        ticks=overrides.get("ticks", 400),
        total_quanta=overrides.get("total_quanta", 4000),
        decay_hazard=overrides.get("decay_hazard", 0.04),
        max_reactions_per_tick=overrides.get("max_reactions_per_tick", 120),
        params={"types": list(_TYPES), "bind": bind},
    )
    return BindingPhysics(bind=bind), cfg
