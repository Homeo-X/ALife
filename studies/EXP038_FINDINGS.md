# exp038 — Coherence is selectable and emergent — but single-objective selection trades off

exp037 (Ω-0.25) showed evolvable architecture amplifies *whatever* is selected, and that a network
proxy drives runaway openness (Goodhart). exp038 tries a **better-aligned, emergent** target:
**autocatalytic closure** — the fraction of a deme's cross-production network that is
self-producing (a class both *produced by* a member and *itself a producer*: a self-maintaining
loop), read straight off the real network (`_deme_closure`), not imposed like exp021's coop bit.

## Result (6000 ticks, 3 seeds)

| selection target | mean closure | heredity self | null | self/null |
|------------------|:------------:|:-------------:|:----:|:---------:|
| **closure** | **0.064** | 0.102 | 0.025 | 4.12 |
| network | 0.046 | **0.209** | 0.050 | 4.21 |
| size (no network sel) | 0.028 | 0.117 | 0.023 | 5.02 |

**Two findings, one positive and one honest negative:**

1. **Coherence is an emergent, selectable trait (positive).** Selecting for closure raises it —
   0.064 (closure) > 0.046 (network) > 0.028 (size), a clean ordering, +0.018 over the network
   control. Unlike exp021's *imposed* cooperation bit, closure is *read off the real
   cross-production network* — a genuinely emergent collective property that selection can grip.
   This is what the roadmap asked for: internal coordination made selectable without hand-installing
   it.

2. **But it does not strengthen individuality — it trades off against it (honest negative).**
   Selecting closure *lowers* collective heredity (self 0.102) vs selecting the network directly
   (self 0.209). Closure and heredity are **competing axes** under a single-objective fitness:
   pushing self-maintenance (short internal loops) is not the same as pushing faithful reproduction
   of the whole network, and rewarding one costs the other. The hoped-for "closure → self-
   maintaining → longer-lived / breeds truer" payoff **does not appear** under closure selection
   alone.

## Interpretation — the Goodhart theme, sharpened into a design constraint

exp037 said evolvable architecture amplifies whatever you select; exp038 shows that *even a
well-motivated emergent target* (closure) optimizes itself at the expense of the other properties
you actually want (heredity). A collective made of intrinsically-functional, self-improving parts
needs **closure AND heredity AND function at once** — and every single-objective proxy tried so
far (network → openness; closure → low heredity) buys one by spending another. The lesson is not
"closure is wrong" but "**alignment is multi-objective**": there is no scalar fitness whose
maximization yields the whole package. That is the real obstacle between here and self-improving
collectives — and it is the question the capstone (exp039/040) must confront directly: whether a
*combined* objective (closure + heredity + intrinsic function), with the per-collective evolvable
state of exp037, produces collectives that compound rather than trade off.

## Status against the roadmap
- **Selectable coherence: achieved** (emergent, not imposed).
- **Coherence → stability/longevity: not achieved** — closure trades off against heredity under
  single-objective selection. The churn/short-life problem is *not* fixed by closure selection
  alone; it needs multi-objective, aligned selection (the capstone).

## Reproduce
`PYTHONPATH=. python3 studies/exp038_closure.py 6000 3` → the table above; committed as
`studies/exp038_results.json` / `_console.txt`. Mechanism pinned by `test_exp038_*` in
`omega/tests/test_experiments.py`; `deme_fitness != "closure"` leaves exp001–035 byte-identical.
