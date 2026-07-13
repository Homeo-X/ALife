# exp037 — Per-collective evolvable internal state: architecture *can* now evolve

exp036 (Ω-0.24) hit the third wall: a collective could not be selected for anticipation because
it had **no internal state to represent** it. exp037 supplies the missing engine piece — a
**per-collective genome** — and asks whether a collective's architecture can now evolve under
selection at all.

## Mechanism

Each deme carries a **heritable, mutable construction rule of its own**: its `type_resolution`,
made first-class *per collective* (exp033 made physics first-class per *level*). It is used in that
deme's own compositions (`compose_path(..., res)`), and when a deme founds another it **transmits
its rule** to the child, with a `genome_mut` chance of a ±1 mutation. Demes start with resolutions
drawn uniformly (1..6). Gated: `deme_genome=False` (default) ⇒ exp001–035 byte-identical.

## Result (6000 ticks, 3 seeds)

Mean per-deme resolution over the run (start = 3.5):

| | early → late |
| --- | --- |
| **treat** (network selection) | 3.1 · 2.7 · 3.3 · 3.5 · 3.7 · 3.5 · 4.1 · 4.3 · 3.7 · 3.5 · **4.1** |
| **control** (no selection channel) | 3.1 · 3.0 · 3.0 · 3.0 · 3.0 · 3.0 · 3.0 · 3.0 · 3.0 · 3.0 · **3.0** |

**Final resolution: treatment 4.14 vs control 3.03 — a +1.11 selection gap.** With a selection
channel, the per-collective genome **moves**; without one it stays put. So the mechanism the third
wall demanded works: **a collective can now carry heritable internal state that selection acts on**
— exactly what exp036 could not do.

## Interpretation — engine piece #2 works, with two honest edges

This is a **positive result**: representation enables selection. But it is a *weak* positive, and
the two edges are as important as the result:

1. **The selection signal on architecture is weak and noisy** — a ~1-point drift over 6000 ticks,
   not a sharp convergence to a fixed optimum. This is consistent with the **exp028 heredity
   ceiling**: the collective level transmits traits only moderately faithfully, so selection on a
   collective-level trait moves it slowly. Better heredity (the amplifier layer) would sharpen it.

2. **It evolves toward the fitness proxy's extreme, not the "good" architecture** — network
   selection drives resolution *up* (toward 4–5: runaway openness, high novelty), away from the
   exp030 heredity "both corner". Evolvable architecture faithfully **amplifies whatever is
   selected** — a Goodhart outcome. The lesson: giving collectives a knob to turn is only as good
   as the target you select for.

Together these say: engine piece #2 (per-collective internal state) is **necessary and now
present**, but two things gate it into something like self-improvement — **stronger collective
heredity** (so selection bites) and **a better-aligned selection target** (so it improves toward
coherence, not just toward gaming the proxy). Both are the next rung: **exp038 — coherence /
autocatalytic closure as an emergent, selectable, better-aligned trait.**

## Reproduce
`PYTHONPATH=. python3 studies/exp037_genome.py 6000 3` → the trajectory above; committed as
`studies/exp037_results.json` / `_console.txt`. Mechanism pinned by `test_exp037_*` in
`omega/tests/test_experiments.py`; `deme_genome` off ⇒ exp001–035 byte-identical.
