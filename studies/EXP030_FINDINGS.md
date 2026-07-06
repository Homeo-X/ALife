# exp030 — The capstone: an open-ended AND modular substrate completes the transition

exp029 localized the transition to collective individuality to a single trade-off: the
**combinator** substrate is open-ended (novelty ~4.5) but its networks don't breed true
(self ~0.10); the **typed** substrate composes modularly so networks breed true (self
~0.24) but is closed (novelty ~0). A completed transition needs a substrate that is
**both** open-ended **and** modular. This experiment builds one and finds the regime
where both hold at once.

**Mechanism (gated by `substrate="typed_path"`; exp012–029 byte-identical; determinism
preserved; 35/35 tests pass).** A morphism is now a variable-length **type path**
(`t0→t1→…→tk`, a kernel-compatible right-nested tuple). Interaction is **modular
composition by concatenation** — `compose_path`: `(a..b) ∘ (b..c) = (a..b..c)` iff the
endpoints match. Composition is deterministic in the members (modular → networks
reproducible), yet paths grow unboundedly (open-ended → novelty can stay > 0). A
`type_resolution` dial truncates products to their last N nodes — the knob between the
two exp029 corners: small N → few types, closed/reproducible (≈ typed); large/0 → many
types, open/unreproducible (≈ combinator). Registered as `exp030`. Reproduce with
`studies/exp030_*.py`.

## Result: the "both" corner exists — a completed transition in miniature

`source`, 4000 ticks, 5 seeds. The two baselines are the corners; the typed_path grid
sweeps `n_types × type_resolution`:

| substrate | edge self | self/null | x-prod | novelty |
|-----------|:---------:|:---------:|:------:|:-------:|
| combinator (exp027, open) | 0.099 | 3.27 | 2.6 | **4.53** |
| typed (exp029, modular)   | 0.241 | 5.34 | 1.0 | **0.00** |
| **typed_path n=32, res=2** | **0.246** | 3.23 | 4.6 | **0.10** |
| **typed_path n=32, res=3** | **0.224** | 5.28 | 6.7 | **0.41** |
| **typed_path n=64, res=2** | **0.281** | 3.78 | 3.9 | **0.18** |

At the **both corner** (`n_types` 32–64, `resolution` 2–3), the substrate simultaneously
delivers all three things neither pure substrate could:

- **Strong, reproducible collective heredity:** self Jaccard 0.22–0.28 — matching or
  *exceeding* the modular typed substrate (0.24), and ~2.5× the combinator ceiling (0.10).
  A founded deme re-forms its parent's cross-production network faithfully.
- **Sustained open-endedness:** novelty rate 0.1–0.41 — genuinely positive, unlike the
  closed typed substrate's 0.00. The universe keeps discovering new morphism types while
  demes breed true.
- **Richer networks than either baseline:** cross-production 4–7 (vs combinator 2.6,
  typed 1.0), with signatures of 1–1.4 edges — the collectives are more, not less,
  structured.

The `resolution` dial cleanly maps the frontier: increasing it trades heredity for
novelty (res 2→4: self 0.25→0.10, novelty 0.10→0.94), and the **intermediate** resolution
is exactly where both are satisfied. Larger `n_types` widens the "both" window (its
`res=2` cell stays reproducible while the bigger type space keeps novelty alive).

## Interpretation — the transition, completed in miniature

This is the resolution the whole exp017–030 arc was built to reach. A major transition to
collective individuality requires collectives that are (i) heritable and selectable and
(ii) discrete/reproducible, *in an open-ended world*. exp029 proved the two requirements
pull against each other at the substrate level; exp030 shows they are **jointly
satisfiable** — on a substrate that is modular (composition is deterministic in the parts)
*and* open-ended (the parts, and their compositions, grow unboundedly). Path-morphisms
with a bounded identity resolution are the minimal such substrate: modularity makes deme
networks reproducible (self ≫ combinator), the growing path space keeps novelty alive
(novelty > 0, unlike closed typed), and an intermediate resolution holds both at once.

It remains "in miniature" — as the whole program's results are (Ω-0.1, Ω-0.10, Ω-0.14):
novelty at the both corner (~0.4) is lower than the pure combinator's (~4.5), so there is
a residual, now-*graded* rather than *absolute* trade-off — you can have more of one by
accepting less of the other, but a healthy amount of both is reachable. That is precisely
what a completed transition looks like at this scale: not the abolition of the
heredity-vs-diversity tension, but a regime where a heritable collective individual and an
open-ended world coexist.

## Where the arc ends, and what remains

exp017 → exp030 has carried the collective-individuation question from "does selection
act on the collective?" to a working answer:

- **Yes, given a heritable group trait** (exp021 imposed, exp022 emergent) — the
  machinery is sound.
- The **binding constraint** is substrate network reproducibility (exp024–028), not the
  machinery or transmission.
- **Modular composition removes it** (exp029), and a substrate that is **both modular and
  open-ended** (exp030, typed_path) achieves strong, reproducible, open-ended collective
  individuality — a completed transition in miniature.

What remains is the same frontier the whole program shares: showing it **unbounded** —
that at the both corner the collective heredity *and* the novelty rate both stay alive
over 10⁵⁺ ticks and across many seeds, and that collective individuals themselves begin to
compose into a further level (a transition *of* transitions). exp030 turns the collective
individuality question from open to answered-in-miniature, and hands the unboundedness
question — the program's original and ultimate one — forward.
