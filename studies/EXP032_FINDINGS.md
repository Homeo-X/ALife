# exp032 — Unboundedness: does the tower keep climbing, and does each level stay alive?

Every prior findings doc — and the program's *original* goal (Ω-0.1/0.10/0.14) — hands
forward one frontier: **unboundedness**. Every headline before this was a bounded-horizon
burst (400–4000 ticks). exp032 tests the two unboundedness questions the arc sharpened, at
real scale, with the mandatory guardrails (rates in temporal **windows**, not cumulatives;
**matched controls**; honest verdict either way — the program has two metric-artefact false
positives on record, so this is deliberately conservative). It is analysis-only on the
existing engine (no new registered physics); the sole code was the gated `record_stride`
harness hook to bound memory on long runs.

## Part A — within-level persistence (40k ticks × 3 seeds, plus one 120k stretch)

Run the exp030 "both corner" (open-ended AND modular, `typed_path` n_types=32 res=3) long,
against a matched **closed** control (exp029, modular-only, novelty→0). Novelty rate per
window comes from the per-tick `novelty_new_per_tick`; collective heredity per window from
the physics' `_hered_edge_self` / `_hered_edge_null` (event-ordered — these are
**event-count windows**, an approximate temporal alignment, not exact tick windows).

**40 000 ticks, 3 seeds, 8 windows:**

| window | w0 | w1 | w2 | w3 | w4 | w5 | w6 | w7 |
|--------|----|----|----|----|----|----|----|----|
| novelty rate (open, exp030) | 0.389 | 0.575 | 0.364 | 0.308 | 0.287 | 0.268 | 0.315 | 0.359 |
| novelty rate (closed, exp029) | 0.028 | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** |
| heredity self (open) | 0.150 | 0.083 | 0.089 | 0.090 | 0.087 | 0.087 | 0.089 | 0.084 |
| heredity null (open) | 0.038 | 0.019 | 0.016 | 0.019 | 0.018 | 0.017 | 0.018 | 0.018 |

The open corner keeps novelty rate **> 0 in every window** (0.27–0.58, no downward trend at
40k) and collective heredity **self > null in every window** (self ≈ 4–5× null, flat),
while the closed control's novelty **collapses to exactly 0.000** from window 1 on. The
population is stable throughout (final 197±9, range [158, 229] over the run, reservoir
pressure 0.147 — no collapse, no runaway). **Verdict: SUSTAINED — the "both corner" is not
a startup transient.**

**The 120k stretch (seed 0, 39 788 heredity events, 34 274 classes discovered):**

| window | w0 | w1 | w2 | w3 | w4 | w5 | w6 | w7 |
|--------|----|----|----|----|----|----|----|----|
| novelty rate | 0.454 | 0.276 | 0.389 | 0.353 | 0.268 | 0.207 | 0.175 | 0.164 |
| heredity self | 0.113 | 0.093 | 0.077 | 0.096 | 0.087 | 0.091 | 0.085 | 0.085 |
| heredity null | 0.027 | 0.020 | 0.013 | 0.020 | 0.018 | 0.020 | 0.019 | 0.018 |

Both stay alive to 120k: novelty > 0 in every window, heredity self > null (≈ 4–5×) in
every window, and the class registry keeps growing (34 274 distinct classes ever — novelty
is genuine construction, not a counter artefact).

**Honest caveats.** (i) **Heredity is the robust half** — flat, self ≈ 4–5× null, no
erosion across either horizon. (ii) **Novelty is sustained but not perfectly stationary at
120k**: the rate drifts down over the stretch (~0.45 → ~0.16, roughly halving). It stays
firmly above the closed control's exact zero — the *open-vs-closed* distinction is
decisive — but whether the rate asymptotes to a **positive floor** or is a very slow
dilution toward zero is **not settled even at 120k** (the same honest limit flagged in
Ω-0.2). (iii) The absolute self-Jaccard in the sustained regime (~0.085) is **lower** than
the short-horizon burst (~0.25 in exp030): as deme networks grow, a fixed amount of shared
structure is a smaller Jaccard fraction, so absolute overlap falls even as the heritability
*signal* (self ≫ null) persists.

## Part B — tower-depth scaling (2500 ticks/tier)

Does the recursive level tower (`omega/levels/stack.py`) have an intrinsic depth ceiling,
or is depth limited only by compute? Lift the cap and measure.

**Deep tower, `max_tiers=15`, base 32, 2 seeds** — per-seed depth **[15, 0]**. When the
tower survives its (stochastic) early tiers it climbs to the **full cap of 15**, with a
**self-sustaining ~fixed-point alphabet**: collectives/tier ≈ 23–24 *undiminished from tier
1 to tier 14*, heredity self (0.11–0.16) > null (0.02–0.04) at every tier, novelty
0.49–0.60 at every tier. The promoted alphabet does not starve with depth — no intrinsic
ceiling appears up to 15.

**Base-alphabet sweep, `max_tiers=8`, 3 seeds/base** — per-seed depth:

| base | depths | reaches cap? |
|-----:|--------|:------------:|
| 16 | [8, 8, 8] | 3/3 |
| 32 | [8, 0, 8] | 2/3 |
| 64 | [8, 8, 8] | 3/3 |

**8 of 9 seeds reach the `max_tiers` cap regardless of base size.** Depth is set by the cap
(compute), not by the base alphabet — a bigger base buys no more depth because each tier
regenerates a ~constant collective count anyway. **Verdict: depth is compute/cap-limited,
not ceiling-limited** — the tower's promotion map has an attractor (~23 collectives/tier)
that sustains the alphabet indefinitely.

**Honest caveat.** There is a **stochastic early-tier failure mode**: ~1 seed in 3 (deep
[15,**0**]; base-32 [8,**0**,8]) fails to form ≥2 heritable collectives at tier 0 and the
tower never starts (depth 0), mirroring exp031's 1/5 failed seed. Conditional on surviving
tier 0, the tower climbs to whatever cap it is given; unconditionally, tower formation is
not guaranteed on every seed.

## Interpretation — the unboundedness verdict

- **Within a level:** at the both corner, **collective heredity persists robustly** (self ≫
  null, flat, to 120k) and **novelty stays open** (> 0 every window, vs the closed control's
  exact zero) — the transition to collective individuality is *sustained*, not transient.
  The one unsettled question is whether the novelty **rate** holds a positive floor or dilutes
  very slowly; heredity has no such caveat.
- **Of levels:** the recursive tower shows **no intrinsic depth ceiling up to 15** — a
  self-sustaining fixed-point alphabet makes depth compute-limited, the strongest
  open-endedness-*of-levels* evidence in the program — tempered by a stochastic early-tier
  failure that can abort a tower before it starts.

Net: on both axes the evidence is **affirmative for unboundedness in miniature**, with the
honest edges named (novelty-rate asymptote not settled at 120k; tower formation is
per-seed stochastic). This is the sustained-horizon test the log said had never been run.

## Reproduce
`PYTHONPATH=. python3 studies/exp032_longhorizon.py 40000 3 120000` and
`PYTHONPATH=. python3 studies/exp032_towerscaling.py 2500 2 3` print the tables above;
committed as `studies/exp032_longhorizon_results.json` / `_towerscaling_results.json` (+
`_console.txt`). Claims pinned by `test_exp032_both_corner_persists_across_windows` and
`test_exp032_tower_depth_not_ceiling_limited` in `omega/tests/test_experiments.py`.
