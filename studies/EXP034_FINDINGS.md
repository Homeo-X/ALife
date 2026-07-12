# exp034 — Sustained novelty via in-level reification (the constructibility lever)

exp032 (Ω-0.17) left one honest edge: at the both corner, collective heredity is flat and
robust, but the novelty **rate** drifts down over a long horizon (~0.45→0.16 across 120k
ticks). The both-corner substrate has a **fixed** atom alphabet — so as the accessible
type-space around current structures gets explored, the rate of genuinely-new discovery
slows. The program's founding thesis (Ω-0.1) is that open-ended complexity needs infinite
**constructibility**, not infinite space: reification (exp004) — promoting a persistent
motif to a *new primitive* — was the mechanism that kept an individual-level world open.
This applies that lever *inside* the collective both-corner substrate.

## Mechanism

Every `reify_period` ticks (default 500), the most common recent product motif is promoted
to a **new atom** appended to `self.atoms` — an opaque primitive standing for that motif
(Axiom-5 reification, applied within a level and *during* the run). The per-period tally is
cleared so it tracks the *moving frontier* of common motifs. It consumes no RNG, so
`reify_period=0` recovers exp030 byte-identically. Same both-corner base otherwise
(`typed_path`, n_types 32, resolution 3).

## Result — the novelty-rate decay is not just slowed, it is eliminated

30 000 ticks, 3 seeds, 8 temporal windows (rate per window, not cumulative):

| window | w0 | w1 | w2 | w3 | w4 | w5 | w6 | w7 |
|--------|----|----|----|----|----|----|----|----|
| novelty rate — **baseline** (exp030, fixed alphabet) | 0.418 | 0.523 | 0.496 | 0.334 | 0.302 | 0.306 | 0.282 | 0.262 |
| novelty rate — **reify** (exp034) | 0.475 | 0.528 | 0.635 | 0.539 | 0.543 | 0.525 | 0.626 | **0.668** |
| reify heredity self | 0.195 | 0.097 | 0.085 | 0.091 | 0.089 | 0.088 | 0.086 | 0.080 |
| reify heredity null | 0.057 | 0.023 | 0.017 | 0.017 | 0.014 | 0.016 | 0.018 | 0.016 |

- **Baseline** novelty rate decays from ~0.52 (w1) to **0.27** (w7) — a late/early ratio of
  **0.53** (it roughly halves), exactly the drift exp032 flagged.
- **Reify** novelty rate goes from ~0.53 (w1) to **0.67** (w7) — a late/early ratio of
  **1.11**: *flat to slightly rising*, no decay at all. The late-window rate is **2.38× the
  baseline**.
- The alphabet grew **32 → 91 atoms** (59 motifs reified), and collective **heredity stayed
  alive every window** (self ≈ 4–5× null throughout) — reification sustains novelty *without*
  eroding the reproducibility that makes collectives individuals.

## Interpretation — constructibility, not space

This is the program's founding hypothesis, confirmed at the collective level and at the
place it was most in doubt. The both-corner's novelty decay was **not** an intrinsic limit
of the deme dynamics; it was the fixed alphabet. Feeding persistent structure back as new
primitives — growing *constructibility*, while the material/space is unchanged — turns a
decaying novelty rate into a sustained (here, non-decaying) one. "Infinite constructibility,
not infinite space" is the lever, exactly as Ω-0.1 conjectured and exp004 first showed for
individuals.

## Honest scope
- **Horizon.** 30k ticks — long enough that the baseline clearly decays (0.53×) and reify
  clearly does not (1.11×). It is not a proof of *forever*: it shows reification removes the
  decay over the horizon where the fixed-alphabet baseline exhibits it. Whether the rate
  holds across 10⁶⁺ ticks (and whether unbounded alphabet growth has its own late cost) is
  the next horizon; `reify_max_atoms` caps growth at 256 here.
- **What it is not.** Not a new substrate — it is exp030 plus a periodic reification hook.
  The reified atom is opaque during composition (its motif is recorded but not re-expanded),
  which is the point (a promoted primitive), not a limitation.

## Follow-up (250k ticks) — sustained novelty needs *continuing* construction

The 30k result leaves a sharper question: is it a **one-time** alphabet enlargement that
sustains novelty, or **ongoing** construction? A three-arm run separates them — baseline
(never constructs), **capped** (constructs then *stops*: a low cap of 64 atoms, filled by
~16k ticks), **uncapped** (keeps constructing). 250k ticks, seed 0, 10 windows of 25k (so
windows 1–9 are all *post-cap* for the capped arm):

| window | w0 | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | late/early |
|--------|----|----|----|----|----|----|----|----|----|----|:---------:|
| **baseline** (never constructs) | 0.391 | 0.327 | 0.325 | 0.192 | 0.167 | 0.199 | 0.195 | 0.162 | 0.185 | 0.152 | **0.51** |
| **capped** (constructs, stops ~16k) | 0.562 | 0.420 | 0.331 | 0.315 | 0.294 | 0.262 | 0.267 | 0.265 | 0.248 | 0.247 | **0.67** |
| **uncapped** (keeps constructing) | 0.554 | 0.637 | 0.690 | 0.700 | 0.781 | 0.779 | 0.645 | 0.739 | 0.763 | 0.803 | **1.16** |

- **Baseline** halves (ratio 0.51), as before.
- **Capped** — once its alphabet freezes at 64 atoms (32 reified), its novelty rate **resumes
  decaying** (0.42 → 0.25, ratio 0.67): a one-time construction bump *delays* but does **not**
  stop the decay.
- **Uncapped** — growing to **531 atoms (499 reified)** — the novelty rate is **flat to
  rising** (0.64 → 0.80, ratio 1.16) across all 10 windows, with collective heredity alive
  throughout (self ≈ 0.085 ≫ null ≈ 0.015).

**So sustained novelty requires *continuing* construction, not a larger fixed alphabet.** This
is the sharpest form of the Ω-0.1 thesis: what keeps a world open is not a bigger fixed space
(the capped arm has a permanently enlarged one and still closes) but the **ongoing act of
construction itself** — reification must keep running. Constructibility is a *rate*, not a
*stock*.

*(A literal 10⁶-tick run is memory-bound on a 16 GB box — genuinely open-ended novelty grows
the class registry with cumulative new classes, ~GB/arm — so this uses an early-filling cap to
put the decisive post-cap regime inside a feasible 250k horizon. Single seed: one deep
trajectory, not a distribution.)*

## Reproduce
`PYTHONPATH=. python3 studies/exp034_reification.py 30000 3` → the 30k table; and
`PYTHONPATH=. python3 studies/exp034_megatick.py 250000 64` → the three-arm continuing-vs-
one-time table (committed as `studies/exp034_megatick_results.json` / `_console.txt`).
Claim pinned by `test_exp034_reification_grows_the_alphabet_and_keeps_novelty` in
`omega/tests/test_experiments.py`.
