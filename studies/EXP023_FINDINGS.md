# exp023 — Niche construction: can environmental heredity break the within-deme-dominance wall?

The recurring wall behind exp017–022: **within-deme dominance never clears ~0.37** —
no local replicator ever takes over a patch, so demes never crystallize a heritable
"type" for collective selection to grip. exp022's roadmap flagged the most promising
lever as a *second inheritance channel*: **niche construction**. This tests it.

**Mechanism (gated; exp012–022 byte-identical; determinism preserved; 26/26 tests
pass).** `feed_mode="recycle"`: instead of feeding each deme fresh random normal
forms, feed it a **resample of its own recent products** (a per-patch rolling buffer,
`self._niche`), anchored on a resident so the new organism inherits that deme's patch.
The deme's environment becomes a heritable phenotype and a positive feedback on its
own composition. Registered as `exp023`. Reproduce with `studies/exp023_*.py`.

## Result: it moves the wall, but does not break through — and it costs novelty

2×2, `feed_mode {random, recycle}` × `propagule {source, mixed}`, 5000 ticks, 5 seeds:

| feed | mode | within-deme dom | n_deme_types | types/live | novelty rate | classes ever |
|------|------|:---------------:|:------------:|:----------:|:------------:|:------------:|
| random  | source | 0.245 | 18.9 | 0.791 | 6.35 | 35,806 |
| random  | mixed  | 0.243 | 19.0 | 0.793 | 6.60 | 36,359 |
| recycle | source | **0.325** | 15.4 | 0.650 | **2.34** | 10,818 |
| recycle | mixed  | 0.318 | 15.8 | 0.668 | 1.84 | 13,007 |

Three findings:

**1. Niche construction genuinely lifts within-deme dominance — the first lever to
do so.** Recycle raises it 0.245 → 0.322 (robust across 5 seeds), where local feed
(exp019) and even an explicit replicase (exp020) could not move it via feed geometry
alone. The environmental-heredity channel is real. But it plateaus at ~0.32 — it
does **not** clear the ~0.37–0.5 threshold that would mark a crisp deme type.

**2. It does not individuate.** The deme-type consolidation (19 → ~15.5) happens
essentially *equally* in `source` and `mixed` (ndt diff −0.4; types/live diff −0.018
— within seed noise), so it is **not** collective winnowing. A strong founder
bottleneck does not rescue it: recycle × propagule ∈ {1, 2, 8} gives inconsistent
source−mixed signs (−1.0, +2.3, +0.3). The mechanism is global, not collective:
recycling reinforces whichever replicators are *globally* fittest, in every deme
identically — so demes become more dominated but by the **same** classes (lower
`n_deme_types`) rather than diverging into deme-specific types. It is individual-level
rich-get-richer routed through the environment, the same failure mode as exp020.

**3. It costs open-ended novelty.** The novelty rate roughly **halves** (6.5 → 2.0)
and lifetime classes fall ~3× (36k → 11k). Feeding a deme its own past output instead
of fresh forms trades away exactly the novelty the feed was supplying. This is the
Ω-0.14 heredity-vs-diversity tension — *"collective heredity requires high-fidelity
reproduction (low feed), which trades against the feed that sustains diversity"* —
reappearing, now localized to the feed channel itself. (OEI reads 0 throughout, as
for all combinator experiments — the SKI soup does not build the form-substrate's
runtime operators; novelty rate is the informative signal here.)

## Interpretation — a partial step, and the chicken-and-egg it exposes

Niche construction is the first intervention to move the within-deme-dominance number
at all, confirming environmental heredity is a real second channel. But on its own it
raises dominance *globally without differentiation*: the environment amplifies the
shared global winners in every deme, so no between-deme variance is created for
collective selection to act on, and open-ended novelty pays the bill.

The exposed obstacle is a **chicken-and-egg**: recycling can *lock in* a deme's
composition, but only if demes have *already diverged*; it does not, by itself, create
the initial divergence. So the environmental channel amplifies whatever composition
exists rather than differentiating it.

**Where this points (next experiment).** Pair niche construction with a mechanism that
*forces initial between-deme divergence*, so recycling then locks distinct types into
distinct demes:
- **seed demes with different founder compositions** (distinct local alphabets/biases
  per patch), so each deme starts in a different basin and recycling keeps it there; or
- **combine recycle feed with exp022 network fitness**, so collective selection favors
  deme-specific cross-producing networks while recycling gives them the within-deme
  dominance to persist — the two half-mechanisms (022 selects but does not dominate;
  023 dominates but does not differentiate) may be complementary.

The updated status of the collective-individuation problem: three levers now each
supply *part* of what a major transition needs — collective selection (exp022),
within-deme dominance (exp023), and heredity+relatedness (exp021) — but no single
experiment yet supplies all at once. The next step is their **combination**, not
another isolated lever.
