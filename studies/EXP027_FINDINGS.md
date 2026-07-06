# exp027 — How far does the substrate dial go? A dose-response of individuation vs basis richness

exp026 turned exp024's substrate wall into a **dial**: enriching the combinator basis
with interacting combinators (SKI → BCW) lifted a deme's network-signature heredity
from weak (1.6×) toward moderate (2.4×). This experiment sweeps the dial — the
interacting basis from **3 to 11 combinators** — to answer whether collective
individuation keeps climbing toward *strong* (self ≫ null) or plateaus.

**Mechanism (gated; exp012–026 byte-identical; determinism preserved; 31/31 tests
pass, incl. per-combinator reducer correctness tests).** Extended `_step` with five
more standard, terminating combinators — thrush `T a b→b a`, vireo `V a b c→c a b`,
and the primed `B'/C'/S'` (arity-4) — each inert unless its atom appears. `exp027`
exposes the full basis `S,K,I,B,C,W,T,V,B',C',S'`; the study sweeps it. A secondary
`expr_size` dial enlarges feed expressions. Reproduce with `studies/exp027_*.py`.

## Result: the dial has an optimum (~3.3×), not an unbounded climb

`source`, 4000 ticks, 5 seeds. Edge-set heredity = self/null Jaccard of a founded
deme's cross-production network signature:

| basis | combinators | distinct types | top-9 cover | edge-set heredity | n_sigs | novelty |
|-------|:-----------:|:--------------:|:-----------:|:-----------------:|:------:|:-------:|
| SKI       | 3  | 204  | 0.72 | 1.59 ± 0.09 | 18.7 | 1.86 |
| +B        | 4  | 598  | 0.48 | 2.18 ± 0.33 | 15.7 | 3.93 |
| +BC       | 5  | 969  | 0.38 | 2.60 ± 0.39 | 12.6 | 3.84 |
| +BCW      | 6  | 1144 | 0.34 | 2.42 ± 0.87 | 12.2 | 2.90 |
| **+T**    | 7  | 1261 | 0.32 | **3.27 ± 1.92** | 10.3 | 4.65 |
| **+V**    | 8  | 1625 | 0.30 | **3.27 ± 0.89** | 7.5  | 4.53 |
| +primed   | 11 | 2307 | 0.21 | 2.43 ± 0.67 | 10.7 | 4.57 |

Three findings:

**1. Individuation climbs to an arc-high, then declines — a Goldilocks basis.** Edge
heredity rises from **1.6× (SKI) to ~3.3× at 7–8 combinators** (S,K,I,B,C,W,T,V), the
strongest emergent collective-level heredity anywhere in the exp017–027 arc, then
**falls back to ~2.4×** at 11 combinators. Past the optimum the type space is *too*
rich (2307 forms, top-9 only 21%): demes can no longer consolidate a stable network,
so signatures stop breeding true. There is an optimal amount of interacting-type
diversity for collective identity — enough to make demes distinct, not so much that
their networks can't reproduce.

**2. The type space enriches monotonically** with basis size (204 → 2307 distinct
forms; top-9 coverage 0.72 → 0.21), confirming the dial does what it should to the
substrate; the *individuation* response to it is what peaks.

**3. Richness improves open-endedness too.** Novelty rate rises from 1.86 (SKI) to
~4.5 across the richer bases — the enriched substrate is both more individuating and
more open-ended, up to the optimum. The secondary `expr_size` dial (BCW basis) is
weaker: 2.42 → 2.87 → 2.72 across sizes 5/8/12, a mild bump then flat.

## Interpretation — moderate-strong, and now fully characterized

Collective individuation in this substrate is **real, emergent, and tunable, but
bounded**. Pushing the interacting basis takes network-signature heredity from weak
(1.6×) to **moderate-strong (~3.3×)** at the optimum — a founded deme's cross-
production network is >3× more similar to its parent than to a random deme, the
clearest sign yet of demes as heritable collective individuals. But it does **not**
cross into *strong* (≫, e.g. 5×+): the response to substrate richness is peaked, not
monotone, because type diversity and network reproducibility trade off.

This completes the diagnosis the arc has been building:

| lever | best network heredity | shape |
|-------|:---------------------:|-------|
| collective machinery only (exp017–022) | ~1× (inert / imposed traits aside) | flat |
| network-signature *representation* (exp025) | 1.6× | — |
| richer interacting basis (exp026) | 2.4–2.65× | rising |
| **full basis sweep (exp027)** | **~3.3×** | **peaked at 7–8 combinators** |

## Status and the remaining path

- Multi-level machinery: works (exp021/022).
- Emergent, heritable collective identity: **present and moderate-strong** (~3.3×),
  maximized at a Goldilocks interacting-basis richness, with novelty intact.
- A *completed* (strong, discrete) transition: **not reached** in the SKI-family
  substrate; the response to enrichment peaks at ~3.3×.

The evidence now points past combinator bases: because individuation peaks and then
falls as combinator diversity grows, the ceiling is not "too few types" but the
**reproducibility** of networks built from a fixed reduction dynamics. The clearest
remaining hypothesis is a substrate whose types are diverse *and* whose interactions
compose modularly enough that large networks still breed true — e.g. **typed** or
**lambda-term** substrates where a deme's network can be a stable, modular circuit
rather than a fragile combinator tangle. exp027 leaves the transition to collective
individuality demonstrated in miniature (~3.3× heritable collective identity) and its
governing trade-off — type diversity vs network reproducibility — precisely located.

---

**Follow-up (see `EXP028_FINDINGS.md`).** exp028 tested whether the ~3.3× ceiling is
fixable by better *transmission* (a network-biased propagule; up to copying the whole
source deme) before pivoting substrates. It is not: even perfect member-set transmission
leaves the signature heritable-but-thin (self Jaccard ~0.06, 0/30 runs strong), and
network-biased propagules don't help while costing novelty. The ceiling is
substrate-limited — the reduction dynamics don't re-form a deme's network even from
identical members — which conclusively motivates the typed/lambda substrate pivot
(exp029).
