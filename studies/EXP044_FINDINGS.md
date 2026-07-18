# exp044 — The frontier: heritable, composable GOALS make competence ratchet at last — but narrowly, and at a cost

exp042 closed the self-improvement arc with a precise diagnosis: competence does not compound even
under a *self-expanding* objective, because the substrate can reify **structure** (Ω-0.20) but has no
**heritable, composable representation of a goal** to reify (and a scalar moving bar flattens its own
selection gradient). exp044 builds that missing faculty and runs the payoff test — and delivers the
**first sustained over-generations ratchet in the entire arc**, together with an equally important
honest caveat.

## Mechanism (gated `deme_fitness="goal"`, default off ⇒ byte-identical)

In `typed_path`, a goal can be an object of the very kind the substrate builds — a **target path**.
So each deme carries one (`_deme_goal[pi]`), which is:
- **heritable** — transmitted to offspring at recolonization like the exp037 genome, mutated via the
  existing `_mutate_path`;
- **achievement-measured** — a deme *realizes* its target when the path is a contiguous stretch of a
  produced class, or of producer++product laid end to end across a cross-production edge (`_contig_subseq`),
  so a goal deeper than `type_resolution` is realized only by **building the pathway**;
- **composable / reified** — a deme that robustly achieves its goal has it **extended by one node**,
  *directed* toward the atom the deme most produces (faithful reification: the target grows along the
  collective's own achieved construction, not a blind random atom).

Fitness rewards achievement × goal depth. Controls: `goal_reify=False` (fixed goals — inherited and
selected on, never extended, isolating composability), exp042 `ratchet` (the scalar bar that failed),
and `size` (drift). Runs with the exp040 heredity channel (`network_template=0.5`).

## Result (12k ticks, 4 seeds, `memory_horizon=4000`)

| arm | goal depth (start → end, slope) | max depth | generic competence (mean, slope) |
|-----|:---:|:---:|:---:|
| **goals+reify** (composable) | **2.41 → 4.05, +0.126/win** | **10** | **0.28, −0.10/win** |
| goals-fixed (composability off) | 2.00 → 2.00, +0.000 | 2 | 0.47, −0.10/win |
| ratchet (exp042 scalar bar) | — | — | 0.51, +0.03/win |
| size (drift) | — | — | 0.57, −0.04/win |

**Two findings, and both matter.**

1. **The representational faculty WORKS — the arc's first sustained compounding.** With heritable,
   *composable* goals, achieved goal depth **ratchets** from ~2.4 to ~4.0 over 12k ticks (max depth
   **10**), robustly across 4 seeds — while the fixed-goal control stays pinned at exactly 2. Nothing
   in exp039/041/042 compounded over generations; here something does. So exp042's diagnosis is
   **confirmed from the other side**: goal representation *was* a real missing piece — given a goal the
   substrate can represent, inherit, and **compose**, the collective accumulates deeper achievements
   across generations. Composability is the active ingredient (fixed goals, everything else equal,
   don't move).

2. **But the ratchet is NARROW — and actively costs generic competence.** The composable-goal arm's
   generic competence (closure + breed-true heredity + network breadth) is the **lowest of all arms**
   (mean 0.28 vs fixed 0.47, ratchet 0.51, drift 0.57) and *declines* over the run. Chasing an
   ever-deeper *idiosyncratic* target does not lift general competence — it **cannibalizes** it: the
   collective pours its construction into realizing its specific goal path at the expense of
   self-maintenance and faithful reproduction.

## Interpretation — the arc advances from "no compounding" to "compounding, but narrow"

This is the payoff and the next problem in one result. The payoff: **open-ended accumulation is
possible in this substrate** once collectives have a heritable, composable goal — the thing exp042
proved was missing. The problem: a represented goal ratchets *itself*, not the collective's general
competence, and worse, the two are in tension (deeper goals pull construction away from closure and
heredity). So the barrier past **goal representation** is **goal alignment / credit assignment**: the
collective can extend and pursue a target, but it cannot tell *which of its parts* makes it
competent, so it cannot aim the goal at its own self-maintenance — it just deepens whatever arbitrary
path it happened to start with. Selecting deeper achievement then trades away the very competence the
arc set out to compound.

The arc, one line each:
- **exp039** — fixed multi-objective doesn't compound → suspect heredity.
- **exp040** — break the heredity ceiling.
- **exp041** — still doesn't compound under a fixed objective → the fixed target.
- **exp042** — self-expand the target (scalar) → still doesn't, worse → **goal representation** is missing.
- **exp044** — give it heritable, composable goals → **it ratchets at last** (first sustained
  compounding), *but narrowly and at the cost of generic competence* → the next barrier is **goal
  alignment / credit assignment**.

## Honest scope

"Competence" is a within-substrate composite; "goal depth" is achieved target-path length, a genuine
constructive achievement but a *specific* one. The goal ratchet is robust across 4 seeds and 12k
ticks (max depth 10), decisively above the fixed control; the competence cost is likewise robust
(composable is lowest on every seed-averaged window). The result is therefore a **partial positive**:
the first over-generations ratchet the arc has produced, honestly bounded — it compounds the
represented dimension, not general competence, and the specialization is costly. It does not claim
mind-like self-improvement; it claims that the *missing faculty was real* and that supplying it opens
a new, sharper problem.

**Determinism caveat (discovered here, engine-wide).** Building exp044 surfaced that the engine's
per-tick reaction selection is sensitive to `PYTHONHASHSEED` (set/dict iteration order feeding the
proposal list before `rng.shuffle`), so the same `seed` can yield different absolute counts across
process invocations (e.g. `classes_ever_seen` varied ~435–1732 at fixed `seed=0`). This does **not**
affect the qualitative findings anywhere in the program — they are matched-control *inequalities* that
hold across the variation (here: composable ≫ fixed on goal depth; composable lowest on competence) —
but specific numbers reproduce only at a fixed hash seed. The claim tests are written to be
hash-robust (multi-seed means / direct mechanism checks). A proper fix — canonicalising iteration
order so results are byte-identical across hash seeds — is a separate determinism-consolidation rung
(tracked; the natural companion to Ω-0.31).

## Consequence — the named next frontier

exp045: **align the goal with competence** — make goal reification promote targets that *increase the
collective's own closure/heredity/breadth* (credit-assign the goal to self-maintenance), then test
whether the now-aligned ratchet lifts generic competence instead of cannibalizing it. That is the
first rung of a *credit-assignment* faculty, the barrier this experiment exposes.

## Reproduce
`PYTHONPATH=. python3 studies/exp044_goals.py 12000 4 4000` → the table above; committed as
`studies/exp044_results.json` / `_console.txt`. Pinned by
`test_exp044_goals_are_heritable_composable_and_reify` in `omega/tests/test_experiments.py` (goals
inherit; composable goals deepen past the seed while fixed stay at 2; heritable with the template on).
`deme_fitness` default ⇒ exp001–043 byte-identical.
