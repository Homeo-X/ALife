# exp045 — Goal alignment / credit assignment: aiming the goal at the closure core does NOT make competence compound (a clean negative)

exp044 gave collectives heritable, composable goals and got the arc's first over-generations
*deepening* — but the ratchet was transient and did **not** lift generic competence: goals grew toward
an *arbitrary* achievable path, so chasing a deeper target cannibalised self-maintenance. The
diagnosis was **credit assignment** — the collective cannot attribute its competence to its parts.
exp045 tests the most direct fix and finds it insufficient.

## Mechanism (gated `goal_align`, default off ⇒ exp001–044 byte-identical)

When a deme robustly achieves its goal, exp044 extends the target toward the atom the deme most
produces. exp045 instead aims the extension at the deme's **autocatalytic closure core** — the classes
that are both *producers* and *products* (the self-maintaining loop that *is* its competence): the
extension-atom vote is restricted to members whose class sits in that loop (falling back to any member
when the loop is momentarily empty). The hypothesis: if the goal grows along the competence-bearing
core, pursuing it should reinforce closure rather than pull away from it. Register `exp045` = exp044 +
`goal_align=True`; the matched control is exactly exp044 (`goal_align=False`).

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (start → end, mean) | closure (mean) | goal depth (start → max) |
|-----|:---:|:---:|:---:|
| **aligned** (exp045) | 0.62 → 0.10, **mean 0.38** | 0.047 | 2.7 → 3.5 |
| unaligned (exp044) | 0.63 → 0.24, mean 0.41 | 0.053 | 2.6 → 3.9 |
| size (drift) | 0.64 → 0.55, **mean 0.63** | **0.097** | — |

**Verdict: still does not compound — and alignment made it slightly *worse*.**

- **Aligning the goal to the closure core did not lift competence.** The aligned arm's generic
  competence (mean 0.38, steady slope **−0.083/win**) is *below* the unaligned exp044 control (0.41),
  and **both goal arms are far below the drift floor (0.63)**. Selecting on goal achievement — aligned
  or not — *degrades* competence relative to doing nothing.
- **It did not even raise closure — the axis it targets.** Aligned closure (0.047) is *below*
  unaligned (0.053) and less than half the drift arm's (0.097). Aiming goal growth at the closure core
  did not make the collective more self-maintaining; if anything the narrower, sometimes-empty target
  made goals deepen *less* (max 3.5 vs 3.9) with no competence return.

## Interpretation — the fix was aimed at the wrong thing: direction, not pressure

exp044's diagnosis (credit assignment) points the right way, but exp045 shows the naive implementation
is insufficient — and *why*. Alignment changed the goal's **direction** (grow it along the closure
core) but not the **selection pressure**, which is still `achievement × depth`. Selection therefore
still rewards *building the goal path*, regardless of whether doing so maintains closure — so the deme
keeps sacrificing self-maintenance to chase depth, and merely pointing the target at the closure core
does not change that trade. Worse, restricting goal growth to a small, often-empty core narrows what
the deme can pursue without giving selection any reason to preserve the core.

The lesson sharpens the frontier: **credit assignment is not a targeting problem, it is a
representation problem.** For competence to compound, the collective needs an *explicit, heritable
model of which parts cause its competence* that **selection itself acts on** — not a goal merely aimed
at those parts. The substrate currently transmits a goal *path* and a developmental *niche*, but it has
no transmissible per-part *contribution* signal; without one, selection on any single achievement
scalar (goal depth, competence bar, closure) reverts to the same trade-off the whole arc has hit.

The arc, one line each:
- **exp039** fixed multi-objective doesn't compound → suspect heredity.
- **exp040** break the heredity ceiling.
- **exp041** still doesn't compound under a fixed objective → the fixed target.
- **exp042** self-expand the target (scalar) → still doesn't → **goal representation** missing.
- **exp044** heritable, composable goals → deeper goals accumulate but transiently, no competence lift.
- **exp045** aim the goal at the closure core (credit assignment, v1) → **still no compounding**, and
  slightly worse → credit assignment needs an *explicit, heritable, selectable contribution
  representation*, not just an aimed goal.

## Honest scope

"Competence"/"closure"/"goal depth" are within-substrate measures; the closure-core target is one
concrete alignment rule (aim goal growth at producers ∩ products). The negative is robust across 6
seeds and 12k ticks (aligned ≤ unaligned ≤ drift on competence, every seed-averaged window past the
transient). It does **not** prove no alignment can work — it shows *this* direct one does not, and
diagnoses why (it moves the target, not the selection pressure), which is what makes it a signpost:
the next rung must put credit into the *fitness*, not the *goal*.

## Consequence — the named next frontier

exp046: **represent the credit in selection.** Give each deme a heritable per-part (per-class or
per-edge) *contribution* score that is itself transmitted and mutated, and make deme fitness reward
demes whose high-contribution parts persist — so selection directly rewards keeping the parts that
cause competence. Then test whether competence finally rises with construction. That is credit
assignment as a *representational* faculty, the barrier exp045 isolates.

## Reproduce
`PYTHONPATH=. python3 studies/exp045_align.py 12000 6 4000` → the table above; committed as
`studies/exp045_results.json` / `_console.txt`. Pinned by
`test_exp045_goal_alignment_targets_the_closure_core` (aligned reification deepens goals toward the
closure core; `goal_align=False` ⇒ exp044 byte-identical). Deterministic across `PYTHONHASHSEED`.
