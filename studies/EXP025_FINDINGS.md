# exp025 — Combinatorial deme identity: is a deme's network signature a heritable collective phenotype?

exp024 localized the individuation blocker to a **substrate type-space wall**: a deme's
identity was its single dominant class, and small SKI expressions reduce to only ~9
attractor normal forms, so 24 demes collapse onto ~13 shared identities. This
experiment sidesteps the wall without a substrate pivot: **redefine a deme's identity
combinatorially** as its internal cross-production **network signature** — the set of
active producer→product class edges. Even with ~9 member types the edge-set space is
combinatorially large, so demes *can* hold distinct identities. Decisive question:
**is that signature heritable through the propagule, and more so than the dominant
class?**

**Mechanism (gated by `track_signature`; exp012–024 byte-identical; determinism
preserved; 28/28 tests pass).** Per deme, accumulate the multiset of cross-production
edges `(producer_cls → product_cls)` this generation; the deme's **signature** is the
set of edges seen ≥ `edge_threshold` (=2) times. Heredity of the signature is measured
exactly like the existing class-set heredity (`_pending`/`_hered_self`/`_hered_null`):
does a founded deme's signature resemble its source's (Jaccard) more than a random
deme's? Registered as `exp025` (= exp022 network experiment + recycle feed + signature
tracking). Reproduce with `studies/exp025_*.py`.

## Result: the network signature is a *more heritable, richer* deme identity — modestly

Source vs mixed, 4000 ticks, 5 seeds. Headline is *within* source runs — network
(edge-set) heredity vs class-set heredity, both self/null Jaccard ratios:

| identity representation | heredity ratio (self / null) |
|-------------------------|:----------------------------:|
| **network signature (edge-set)** | **1.59 ± 0.09** |
| dominant class (exp024 baseline) | 1.47 ± 0.12 |

- edge-set heredity **> class-set heredity in 4/5 seeds**; raw edge Jaccard
  self 0.178 vs null 0.112 — a founded deme's cross-production network is ~1.6× more
  similar to its source than to a random deme. **The signature is genuinely heritable.**
- **Identity space is richer at the network level:** `n_deme_signatures` 18.7 vs
  `n_deme_types` 16.2 (source), and source 18.7 > mixed 16.8 — more distinct demes are
  resolved by their networks than by their dominant class, and `source` resolves more
  than the well-mixed null (a mild network-level individuation signal). Signatures are
  small (~2.3 edges each) and novelty is reduced by the recycle feed (~1.9 vs 2.1).

## Interpretation — the wall is *partly* representational, but only partly

exp024's conclusion is **softened, not overturned**. Two things are now clear:

1. **Part of the missing individuation was a measurement artefact.** Scoring identity
   as a single dominant class undercounts how distinct demes actually are: at the
   network level demes are measurably more distinct (18.7 vs 16.2) and their identity
   is measurably more heritable (1.59× vs 1.47×). The combinatorial representation
   recovers real collective structure the class metric could not resolve.

2. **But the effect is bounded, so the substrate limit is real.** Even the richer
   network identity reaches only ~1.6× heredity — a genuine but weak heritable
   collective phenotype, nowhere near the self ≫ null (discrete, high-fidelity
   identity) that a *completed* transition to collective individuality would show.
   The ~9-attractor type space still constrains how distinct and how heritable the
   networks built from those types can be; combinatorial identity widens the ceiling
   but does not remove it.

## Status of the collective-individuation problem after exp017–025

| ingredient | status |
|------------|--------|
| multi-level selection machinery | **works** (exp021 imposed, exp022 emergent trait) |
| within-deme dominance | liftable to ~0.33 via environmental heredity (exp023), not into distinct demes |
| collective identity that is heritable | **weakly present** at the *network* level (exp025, ~1.6×) — richer and more heritable than the class level, but bounded |
| full individuation (discrete, high-fidelity collective individuals) | **not reached** — capped by substrate type-space poverty (exp024) |

**Where this leaves the program.** exp025 shows the right *representation* of a
collective phenotype (a cross-production network, not a dominant class) recovers a
real, heritable, richer collective identity — the strongest emergent collective-level
heredity in the arc so far, on a par with exp022's selection signal. But it confirms
that a *complete* major transition needs what exp024 already indicated: a substrate
with a broader space of stable types, so networks built on them can be strongly (not
weakly) distinct and heritable. The two clean next moves remain:
- **cheap, in-substrate:** make *deme fitness itself* the network signature's
  distinctness/heredity (select for demes whose networks breed true), pushing the ~1.6×
  heredity higher — a direct extension of exp025;
- **the real unlock:** a richer-type-space substrate (larger/typed combinators or
  lambda terms with a broad, flat normal-form distribution), then re-run the exp022–025
  machinery to test whether network individuation crosses from weak (~1.6×) to strong.
