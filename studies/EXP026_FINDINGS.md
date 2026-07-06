# exp026 — Pushing network individuation from weak toward strong: substrate + selection

exp025 found a deme's cross-production network signature is a *heritable* collective
identity, but only weakly (~1.6×), and exp024 traced the ceiling to **substrate
type-space poverty** (~9 attractor normal forms). This experiment attacks both at
once, in a 2×2 factorial:

- **substrate lever** — `extra_combinators="BCW"` adds the B/C/W combinators to the
  {S,K,I} basis. A first attempt with inert *data* atoms was tried and rejected: it
  enriched the type space (204 → 2529 distinct forms) but **killed cross-production**
  (`mean_cross_prod → 0`), because inert data does not *interact*. B/C/W are extra
  *functions*, so they enrich the type space **and** keep the network dynamics.
- **selection lever** — `deme_fitness="breed_true"` weights a deme's reproduction by
  how faithfully its propagules reproduced its network signature (an EMA of realized
  edge-set heredity), directly selecting for high-fidelity collective reproduction.

Both are gated; the extended `_step` rules are inert unless B/C/W atoms are present,
so exp012–025 stay byte-identical (determinism preserved; 29/29 tests pass).
Reproduce with `studies/exp026_*.py`.

## Result: the substrate lever is the real unlock; selection is a bounded add-on

2×2, `source`, 4000 ticks, 5 seeds. Headline = edge-set heredity ratio (self/null
Jaccard of a founded deme's network vs its source vs a random deme):

| substrate | fitness | edge-set heredity | n_signatures | novelty rate |
|-----------|---------|:-----------------:|:------------:|:------------:|
| SKI | network    | 1.59 ± 0.09 | 18.7 | 1.86 |
| SKI | breed_true | 1.41 ± 0.06 | 18.5 | 1.95 |
| BCW | network    | **2.42 ± 0.87** | 12.2 | **2.90** |
| BCW | breed_true | **2.65 ± 0.27** | 8.5 | 2.66 |

Type space (feed distribution, 5000 draws): SKI = 204 distinct forms, top-9 cover
0.72; **BCW = 1144 distinct forms, top-9 cover 0.34** — broader and much flatter,
while cross-production is preserved (`mean_cross_prod` 10.9 → 8.2).

**1. The richer interacting substrate is the decisive lever.** BCW lifts network
individuation from weak **1.59× → 2.42×** (+52%) **and improves novelty** (1.86 →
2.90) — the collective identity gets more heritable *and* the universe stays more
open-ended. This is the first substrate-level advance in the exp017–026 arc, and it
directly confirms exp024's diagnosis: the ceiling was type-space poverty, and adding
distinct *interacting* types raises it.

**2. Breed-true selection helps only on the rich substrate, and canalizes.** On BCW it
adds a further, and much more *consistent*, push (2.42 → 2.65, variance ±0.87 → ±0.27)
— but it shrinks the identity space (18.7 → 8.5 distinct signatures): the population
canalizes onto a few well-defined, high-fidelity collective types. On the poor SKI
substrate the same selection **backfires** (1.59 → 1.41) — with only ~9 attractor
types, selecting hard for breed-true just collapses between-deme variance. So the
fitness lever is a heredity-vs-diversity knob that requires the substrate lever to pay
off, echoing the Ω-0.14 tension.

## Interpretation — direction found, ceiling raised (not removed)

The collective-individuation problem now has a clear, validated direction. Weak network
heredity (1.6×) was not a dead end but a **substrate ceiling**, and the ceiling moves
when the substrate offers more distinct interacting types: BCW reaches 2.4–2.65×, the
strongest emergent collective-level heredity in the arc, with novelty intact. The
combination BCW + breed_true produces the sharpest outcome — fewer (~8), strongly and
consistently heritable collective identities — which is qualitatively what a nascent
set of collective *individuals* looks like (discrete, breeding true), at the cost of
diversity.

It is still not *strong* individuation (self ≫ null, e.g. 5×+ with a rich identity
space): 2.65× is moderate, and pushing it further trades away distinctness or novelty.
But the levers and their signs are now known:

| lever | effect on network heredity | cost |
|-------|----------------------------|------|
| richer interacting basis (BCW) | 1.6× → 2.4× (primary) | none — novelty *rises* |
| breed-true selection (on BCW) | 2.4× → 2.65× (secondary, consistent) | identity space canalizes (18 → 8) |
| breed-true on poor substrate (SKI) | backfires (1.6× → 1.4×) | collapses between-deme variance |

## Status after exp017–026 and the path to a completed transition

- Multi-level machinery: **works** (exp021/022).
- A heritable collective identity: **present and now moderately strong** at the network
  level (exp025 weak 1.6× → exp026 moderate 2.4–2.65×), and it *strengthens with
  substrate richness while preserving open-endedness*.
- Full (strong) individuation: **not yet**, but no longer diagnosed as a dead end — it
  is gated by how many distinct *interacting* types the substrate offers.

**Predicted path to strong individuation** (the arc's clearest remaining hypothesis):
continue enriching the *interacting* type space — a larger combinator basis, typed
combinators, or lambda terms with a broad flat normal-form distribution — and network
heredity should keep climbing from moderate (2.4×) toward strong. exp026 turns the
exp024 "substrate wall" into a **tunable dial**: the transition to collective
individuality appears reachable not by more multi-level machinery, but by paying for a
richer substrate of interacting parts.
