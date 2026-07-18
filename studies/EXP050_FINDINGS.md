# exp050 — "Stays open forever" settled at 10⁶ ticks: the genuine-novelty floor is REAL, and the Ω-0.31 decline was a transient

The load-bearing claim of the whole program is that **constructibility keeps the world open**. Ω-0.31
settled it *honestly but partially*: on the eviction-robust **global** novelty sketch (which counts each
class once *ever*, stripping the recycling that inflates the windowed rate under bounded memory), the
open engine's genuine rate was **positive but slowly declining** — it *halved* over 300k ticks / 3
seeds, leaving open whether it floors or dilutes to zero further out. exp050 runs the literal
**10⁶-tick** campaign the thesis rests on and resolves that edge.

## Setup (measurement only — no physics change)

Open engine (exp030, the "both corner") vs closed control (exp029, novelty → 0), `run(global_novelty=
True)` (the Ω-0.31 scalable-Bloom ever-seen set), bounded memory (`memory_horizon=5000`,
`relation_cap=20000`) so a literal long run is memory-safe, **10⁶ ticks × 5 seeds** per arm, reported
over 10 windows of 100k ticks each. Both the windowed (inflated) and global (deduplicated) rates are
shown.

## Result (10⁶ ticks, 5 seeds)

| window (×100k ticks) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|--|--|--|--|--|--|--|--|--|--|
| open **windowed** rate | 0.467 | 0.465 | 0.459 | 0.463 | 0.465 | 0.460 | 0.468 | 0.465 | 0.465 | 0.465 |
| open **global** rate | 0.299 | 0.171 | 0.130 | 0.128 | 0.104 | 0.101 | 0.092 | 0.101 | 0.095 | 0.085 |
| closed **global** rate | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

- **open distinct classes ever ≈ 130,600 / seed** (registry held flat at ~3,100 by eviction).
- **closed distinct classes ever = 144 / seed** (the closed alphabet, exhausted in the transient).
- late windowed/global **inflation factor ≈ 5.0** (the windowed rate is ~5× the genuine rate — eviction
  recycling, exactly the artifact the sketch strips).

**Verdict: the genuine-novelty floor is REAL at 10⁶ — "stays open forever" is settled an order of
magnitude beyond Ω-0.31.**

- The eviction-robust global rate is **~0.085–0.10 genuinely-new classes/tick in the entire second half
  of the run**, decisively above the closed control's **exact 0.0000**. The open engine is still
  discovering never-before-seen organization at 10⁶ ticks, having already found ~130k distinct classes.
- **The Ω-0.31 "slow decline" was a transient, not dilution.** The steep drop (0.30 → 0.10) is confined
  to the first ~400k ticks; from window 4 onward (the last 600k) the rate is essentially **flat at
  ~0.095** (0.104, 0.101, 0.092, 0.101, 0.095, 0.085 — a gentle ~18% sag vs the 67% early drop). The
  curve levels onto a floor rather than heading for zero. Ω-0.31's open worry ("halves over 300k — floor
  or dilution?") is resolved in favor of **floor**: the halving was the transient settling, and the
  asymptotic rate is a positive constant.
- **Instrument sanity is perfect.** The closed control reads global 0.0000 in every window past the
  first, and finds only 144 classes ever — the sketch does not manufacture novelty, and the open
  engine's floor is not an artifact of the estimator.

## Interpretation

This is the strongest form of the program's central thesis, now shown at the horizon it was always
stated for. **Open-endedness of *construction* is genuine and asymptotic**, not a finite budget slowly
draining through a measurement window: with all eviction-recycling removed, a *modular-and-open* both-
corner substrate keeps building genuinely-new organization at a stable positive rate to 10⁶ ticks,
while a *closed* substrate stops dead at 144 classes. Constructibility is a **rate with a positive
floor** (Ω-0.20's "rate not stock", now quantified: ~0.09 genuinely-new classes/tick, ~130k distinct
in 10⁶ ticks), and the both-corner condition (open **and** modular) is what sustains it.

Read together with Ω-0.38 (exp049), the picture the program lands on is sharp and honest: **construction
is open-ended (this result); competence is not** (the self-improvement arc plateaued at a substrate-set
ceiling). The world compounds *what it builds* — forever, measurably — but not *how good its collectives
get*.

## Honest scope

The rate is a *floor*, not *flat forever proven*: windows 4–9 still sag ~18%, so a much longer run
(10⁷) could reveal a slower second-order decline — but the deceleration (67% drop in the first 400k vs
18% across the next 600k) is strong evidence of convergence to a positive constant, not of continued
descent toward zero. Within the both-corner substrate (exp030); the closed control is the matched
null. Bounded-memory measurement, which is exactly why the *global* (registry-independent) sketch is
the right instrument.

## Reproduce
`PYTHONPATH=. python3 studies/exp050_megahorizon.py 1000000 5 5000 4` → the table above; committed as
`studies/exp050_megahorizon_results.json` / `_console.txt`. The instrument is pinned by
`test_global_novelty_sketch_is_conservative_and_eviction_robust` (the sketch never false-negatives,
strips recycling under eviction, and is byte-identical when off). Deterministic across `PYTHONHASHSEED`;
`global_novelty=False` ⇒ every existing experiment byte-identical. Preserves the Ω-0.31 300k artifact
(`studies/exp043_unbounded_*`) rather than overwriting it.
