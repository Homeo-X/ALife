# exp029 — The substrate pivot: does modular composition break the individuation ceiling?

exp028 proved the ~3.3× network-individuation ceiling is **substrate-limited**: the
combinator reduction dynamics do not re-form a deme's cross-production network even from
an identical member set. The evidenced next step is a substrate whose interactions
compose *modularly*, so a deme's network is reproducible from its members. exp029 builds
one and runs the exp025–027 collective machinery on it.

**Mechanism (gated by `substrate="typed"`; exp012–028 byte-identical; determinism
preserved; 33/33 tests pass).** A **typed substrate**: an organization is a *morphism*
`(in_type, out_type)` over `n_types` base types, and interaction is **modular
composition** — `(a→b) ∘ (b→c) = (a→c)` iff the types match (`compose()` in
`exp012_combinator.py`). Unlike combinator reduction, the product is a deterministic
function of the two members' types, so a deme's cross-production network is reproducible
by construction. Everything else (network signature + heredity, recycle feed, network
fitness, isolation) is reused unchanged. Reproduce with `studies/exp029_*.py`.

## Result: modularity breaks the reproducibility ceiling — but the substrate closes

Combinator (exp027, optimum BCWTV basis) vs typed (exp029), `source`, 4000 ticks, 5 seeds:

| substrate | edge self | edge null | self/null | x-prod | sig_size | novelty |
|-----------|:---------:|:---------:|:---------:|:------:|:--------:|:-------:|
| combinator | 0.099 | 0.033 | 3.27 | 2.6 | 0.54 | **4.53** |
| **typed**  | **0.241** | 0.050 | **5.34** | 1.0 | 0.20 | **0.00** |

**1. Modular composition makes networks reproducible — the ceiling breaks.** The
child-source network overlap **roughly triples** (self Jaccard 0.099 → 0.241) and the
heredity ratio climbs past the combinator ceiling (3.27× → 5.34×). This directly
confirms exp028's diagnosis: the combinator limit was network *reproducibility*, and a
substrate where the product is a deterministic function of member types removes it. A
founded deme now re-forms its parent's network far more faithfully.

**2. But the typed substrate is closed — open-endedness collapses.** Novelty rate falls
to **0.00** (vs 4.53 on the combinator substrate): the morphism type space is finite
(`n_types²` signatures), composition stays within it, and the population saturates to a
few types with no ongoing class discovery. An `n_types` sweep (6 → 48) shows the same
pattern everywhere — the heredity ratio rises (partly as the null falls) but novelty
stays ~0 and the networks stay **thin** (sig_size 0.06–0.39, x-prod 0.4–1.9): reproducible
but nearly empty circuits in a frozen system.

## Interpretation — the two substrates are opposite corners of one trade-off

exp029 completes the diagnosis the whole exp017–029 arc has been converging on. The two
substrates sit at opposite ends of a single fundamental tension:

| substrate | open-ended? | networks breed true? |
|-----------|:-----------:|:--------------------:|
| combinator (reduction) | **yes** (novelty ~4.5) | **no** (self ~0.10, ceiling ~3×) |
| typed (modular composition) | **no** (novelty ~0) | **yes** (self ~0.24, ratio ~5×) |

- The **combinator** substrate is open-ended — it keeps constructing genuinely new
  types — but its reduction dynamics make networks *unreproducible*, so collectives can
  only ever be weakly heritable (the exp024–028 wall).
- The **typed** substrate composes modularly, so networks *are* reproducible — but its
  closed, finite type space kills open-endedness, and the reproducible networks are thin.

This is the program's deepest tension (Ω-0.14, "collective heredity vs the feed that
sustains diversity") reappearing at the substrate level as **open-endedness vs
modular reproducibility**. A *completed* transition to collective individuality — rich,
reproducible collective individuals in an open-ended world — requires a substrate that is
**both** open-ended **and** modularly composable. Neither pure substrate is.

## Status after exp017–029: the transition, fully localized

- Multi-level machinery: **works** given a heritable group trait (exp021/022).
- Collective identity as a network signature: **heritable**, tunable to a ~3.3× peak on
  a rich interacting combinator basis (exp025–027).
- The ceiling: **network reproducibility of the substrate**, not transmission (exp028).
- Modularity **removes** the reproducibility limit (exp029, self ~0.24, ratio ~5×) — but
  only by sacrificing open-endedness.

**The final frontier (concrete and evidenced).** Build a substrate that is *both*
open-ended and modular — the clearest candidate is **typed combinators / typed lambda
terms**: a type discipline makes well-typed composition modular and reproducible, while
terms still grow unboundedly (types can be reified, à la exp004) so novelty does not
close. The prediction the whole arc now sharpens to a single testable claim: on such a
substrate the exp025–029 machinery should yield network-signature heredity that is
**both strong (self ≫ null) and open-ended (novelty > 0)** — a completed major transition
to collective individuality. exp029 turns that from an aspiration into the one remaining
engineering problem, with the trade-off it must resolve precisely measured.

---

**Follow-up (see `EXP030_FINDINGS.md`).** exp030 built that substrate — variable-length
type **paths** composed by concatenation (modular *and* open-ended), with a
`type_resolution` dial between the two corners. At the "both" corner (n_types 32–64,
resolution 2–3) it delivers all three at once: strong reproducible collective heredity
(self 0.22–0.28, matching/exceeding the typed substrate), sustained novelty (0.1–0.4 > 0,
unlike closed typed), and richer networks than either baseline (x-prod 4–7). The
open-ended-vs-modular trade-off, absolute in exp029, becomes *graded* — a completed
transition to collective individuality in miniature.
