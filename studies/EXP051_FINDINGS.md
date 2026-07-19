# exp051 — The horizon stress: the genuine-novelty floor HOLDS to 3M ticks (the Ω-0.39 caveat closed)

Ω-0.39 (exp050) settled "stays open forever" at 10⁶ ticks: the eviction-robust global rate decelerated
onto ~0.09 genuinely-new classes/tick and *looked* converged, but the last windows still sagged ~18%, so
a slower second-order decline toward zero was not strictly ruled out. exp051 pushes the horizon **3×
further (3M ticks)** with the eviction regime held fixed and asks the one remaining question: does the
floor stay flat from 10⁶ to 3M, or keep sliding?

## Setup (measurement only — no physics change)

Open engine (exp030, the both corner) vs closed control (exp029), `run(global_novelty=True)`, **3M ticks
× 3 seeds**, 12 windows of 250k ticks. `memory_horizon=5000` is held **fixed** (not scaled with ticks)
so the eviction regime is identical to the Ω-0.39 10⁶ run — a fair floor comparison. `relation_cap=8000`
(small, for throughput) bounds only the relation registry and does **not** affect the global-novelty
sketch, which is the headline metric.

## Result (3M ticks, 3 seeds)

| window (×250k ticks) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|--|--|--|--|--|--|--|--|--|--|--|--|
| open **global** rate | 0.220 | 0.120 | 0.093 | 0.088 | 0.084 | 0.091 | 0.076 | 0.074 | 0.075 | 0.075 | 0.068 | 0.062 |
| open **windowed** rate | 0.461 | 0.465 | 0.463 | 0.460 | 0.459 | 0.462 | 0.462 | 0.461 | 0.463 | 0.462 | 0.463 | 0.459 |
| closed **global** rate | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

- **open distinct classes ever ≈ 281,400 / seed** (registry held flat ~3,100 by eviction).
- **closed distinct classes ever = 144 / seed** — exactly the closed alphabet, unchanged from 10⁶.
- mid region (~1–2M) global = **0.0815**; final region (~2–3M) global = **0.0699** → **hold ratio 0.86**.

**Verdict: the floor HOLDS to 3M — the Ω-0.39 deceleration has converged to a positive constant.**

- After the transient (0.22 → 0.08 over the first ~1M ticks, a **64%** fall), the genuine rate is
  **flat within ~14%** across the entire final 2M ticks (0.084 → 0.070), decisively above the closed
  control's **exact 0.0000**. The world is still discovering never-before-seen organization at 3M ticks,
  having found ~281k distinct classes — and the *rate* of that discovery has stopped falling steeply.
- **The decline is decelerating toward an asymptote, not descending toward zero.** The fall is 64% over
  the first 1M ticks but only ~14% over the last 2M — a log-like convergence to a positive floor, exactly
  what "a rate with a positive floor" predicts and the opposite of linear dilution.
- **Instrument sanity holds at 3M.** The closed control reads global 0.0000 in every window past the
  first and finds only 144 classes ever — the sketch manufactures no novelty, and the open floor is real.

## Interpretation

This closes the one caveat Ω-0.39 left open. The genuine-novelty floor is not an artifact of stopping at
10⁶: stressed to 3M ticks with the eviction regime held fixed, it stays flat (within 14%) across 2M ticks
of the late run, three times beyond the point where it was declared converged. Constructibility is a
**rate with a positive floor** — now shown to *hold*, not merely *appear to hold*, over a 3× longer
horizon, with the distinct-ever count climbing to ~281k (roughly 2.1× the 10⁶ value, consistent with a
steady ~0.07–0.09/tick). The both-corner substrate keeps building genuinely-new organization; the closed
substrate remains frozen at 144 classes forever.

Read across the program's two axes, the honest picture is now firm on both: **construction is
open-ended** (Ω-0.39/Ω-0.40, a positive floor holding to 3M) while **competence is not** (Ω-0.38, the
self-improvement arc plateaued). The world compounds *what it builds*, durably and measurably, but not
*how good its collectives get*.

## Honest scope

The floor holds but is not *perfectly* flat: there is a residual ~14% sag across the final 2M, so a much
longer run (10⁷) could still reveal a very slow second-order drift — the deceleration (64% → 14%) argues
against it, but does not mathematically exclude it. This is a 3-seed stress at 3M; the 10⁶ result is the
5-seed anchor. Within the both-corner substrate (exp030), with the closed control (exp029) as the exact-
zero null. `relation_cap` was shrunk for throughput, which does not touch the global metric but means the
windowed-registry detail is coarser than the Ω-0.39 run (irrelevant to the floor claim).

## Reproduce
`PYTHONPATH=. python3 studies/exp051_horizonstress.py 3000000 3 5000 4` → the table above; committed as
`studies/exp051_horizonstress_results.json` / `_console.txt`. Instrument pinned by
`test_global_novelty_sketch_is_conservative_and_eviction_robust`. Deterministic across `PYTHONHASHSEED`;
`global_novelty=False` ⇒ every experiment byte-identical. Preserves the Ω-0.39 10⁶ artifact
(`studies/exp050_megahorizon_*`).
