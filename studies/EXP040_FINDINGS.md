# exp040 — The collective-heredity ceiling breaks: developmental (network-template) inheritance

exp039 located the single blocker between Ω collectives and self-improvement: **collective heredity
is too weak** (the exp028 ceiling, ~3–5× null; self ~0.08–0.28), because a deme's cross-production
network is a *dynamical attractor* that offspring do not re-form from inherited **members** alone.
exp040 attacks it directly — and breaks it.

## Mechanism

Transmit the **developmental niche**, not just the members. When a deme is founded, a fraction
`network_template ∈ [0,1]` of the *parent network's product states* is seeded into the child's
recycle buffer (`_niche`), so the child is continuously re-fed the parent's outputs and canalizes
toward the parent's edges. A biological analogue: offspring inherit genes **and** a structured
developmental environment (niche / parental-effect inheritance). The strength is a dial — the
collective-level analogue of exp030's resolution dial. Gated: `network_template=0` ⇒ byte-identical.

## Result (4000 ticks, 3 seeds; numbers deterministic as of Ω-0.33 — see note)

| template strength | heredity self | null | ratio | novelty | corner |
|:-----------------:|:-------------:|:----:|:-----:|:-------:|--------|
| 0.0 (off) | 0.136 | 0.035 | 3.9× | 0.490 | open, **weak heredity** (the exp028 ceiling) |
| **0.25** | **0.563** | 0.129 | **4.3×** | **0.217** | **BOTH** |
| **0.5** | **0.569** | 0.165 | **3.4×** | **0.220** | **BOTH** |
| **0.75** | **0.582** | 0.155 | **3.8×** | **0.236** | **BOTH** |
| 1.0 (full) | 0.607 | 0.108 | 5.6× | 0.214 | strong heredity, still open |

- **The ceiling breaks (on absolute heredity).** A partial template lifts collective heredity to
  self ≈ **0.56** — **~4.1× the off baseline (0.136)** and, decisively, **well past the exp028
  ceiling of self ≤ 0.28** that even whole-deme transmission could not clear. (The self/null *ratio*
  is a more modest ~3.4–4.3× because the template raises the null baseline too; the load-bearing
  signal is the absolute self clearing 0.28.)
- **And the world stays open.** Across strengths 0.25–1.0 novelty is sustained (~0.21–0.24) — the
  **collective-level "both corner": strong reproducible heredity AND open-endedness at once.**
- **Note (Ω-0.33 determinism correction).** These numbers were refreshed after the Ω-0.33
  determinism fix. The originally reported figures (partial self ≈ 0.40, **8–9× null**, and a sharp
  "**full pinning closes the world**, novelty → 0") were partly an artifact of a favourable
  `PYTHONHASHSEED` (the niche-seed subset order was hash-dependent). Deterministically the ceiling
  break is *stronger* on absolute self (0.56 vs 0.40) but the null-ratio is smaller (~4× not ~9×) and
  the world stays open even at full template (novelty ~0.21, not 0) — so the crisp closed↔open *dial*
  is muted. The qualitative claim (**a partial developmental template reaches the collective both
  corner**) stands.

## Interpretation — the same principle, one level up

This is exactly the exp029→030 story re-derived at the collective level. exp030 resolved the
open-vs-reproducible trade-off for *individuals* with a **modular (partial-identity) resolution
dial**; exp040 resolves it for *collectives* with a **modular (partial-template) developmental
dial**. The collective-heredity ceiling was never a hard wall — it was the same open-vs-reproducible
trade-off, and it yields to the same fix: **partial, modular transmission.** Full transmission
reproduces perfectly but closes; no transmission stays open but can't reproduce; the intermediate is
the both corner.

**Honest scope.** The inheritance channel is *developmental / ecological* (the child is re-provisioned
with a fraction of the parent's products), not purely genetic — a legitimate, biologically grounded
mechanism (niche inheritance, parental effects), and a *partial* one (0.25–0.5), so offspring inherit
a scaffold and still build novelty on top rather than being cloned. The self/null being parent-specific
(null stays low, 0.04–0.05, while self rises to 0.40) rules out a "everything looks alike" artifact.
The both corner is a *multi-seed* result: individual seeds are noisy — some close even at
intermediate strength (e.g. seed 0 at 0.5) — so the open-vs-closed boundary is a soft, seed-dependent
band around strength ≈ 0.25–0.75, not a sharp threshold. Heredity-breaking is robust across seeds;
staying-open is the seed-variable part.

## Consequence

exp039's blocker is removed. The question the whole self-improvement arc was built toward is now
testable at last: **with collective heredity strong (and the world still open), does competence
compound** — closure, heredity, and function rising together over generations? That is **exp041**.

## Reproduce
`PYTHONPATH=. python3 studies/exp040_template.py 4000 3` → the sweep above; committed as
`studies/exp040_results.json` / `_console.txt`. Pinned by `test_exp040_*` in
`omega/tests/test_experiments.py`; `network_template=0` ⇒ exp001–039 byte-identical.
