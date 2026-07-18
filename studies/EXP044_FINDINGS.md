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

Goal-depth trajectory (composable, per generation-window): **2.6 → 3.3 → 3.4 → 4.1 → 4.3 → 3.4 →
3.7 → 3.3** — a **hump**: it climbs well above the fixed control, peaks near window 4, then partially
falls back.

| arm | goal depth (start → peak → end) | max depth | generic competence (mean) |
|-----|:---:|:---:|:---:|
| **goals+reify** (composable) | **2.6 → 4.3 → 3.3** | **7** | 0.46 |
| goals-fixed (composability off) | 2.00 → 2.00 → 2.00 | 2 | 0.39 |
| ratchet (exp042 scalar bar) | — | — | 0.30 |
| size (drift) | — | — | 0.60 |

**Two findings, and both matter.**

1. **The representational faculty has a real effect — the arc's first over-generations *deepening*.**
   With heritable, *composable* goals, achieved goal depth climbs far above the fixed-goal control
   (peak **~4.3**, max **7**, mean well above 2) while the fixed control stays pinned at exactly 2.
   Nothing in exp039/041/042 deepened over generations; here composability does. So exp042's diagnosis
   holds: goal representation *was* a real missing piece — given a goal the substrate can represent,
   inherit, and **compose**, the collective accumulates deeper achievements. Composability is the
   active ingredient (fixed goals, everything else equal, don't move).

2. **But the ratchet is NOT sustained, and it does not lift generic competence.** Goal depth is
   *hump-shaped* — it overshoots to ~4.3 then **partially collapses** to ~3.3: deeper goals outrun the
   collective's ability to keep achieving them, so the deepest-goal demes stop scoring and are
   replaced. And generic competence (closure + breed-true heredity + breadth) is middling — composable
   0.46 beats fixed 0.39 and the exp042 ratchet 0.30 but **loses to drift (0.60)** — so pursuing deeper
   idiosyncratic targets does not translate into general competence. The faculty helps; it does not
   deliver *sustained* compounding.

*(Determinism note, Ω-0.33: an earlier hash-seed run reported a cleaner monotonic ratchet 2.4→4.0,
max 10, "the arc's first sustained compounding". Under the deterministic engine the ratchet is real
but **transient** (peaks then partially collapses) — the "sustained" framing was partly a favourable
`PYTHONHASHSEED`. The direction of every arm is unchanged; the magnitude and the "sustained" qualifier
are corrected. This is exactly why the determinism fix matters.)*

## Interpretation — the arc advances from "no compounding" to "transient deepening, not sustained"

This is a real effect and its limit in one result. The effect: **deeper achievements can accumulate
over generations** once collectives have a heritable, composable goal — the thing exp042 proved was
missing (composable reaches depth ~4–7; fixed stays at 2). The limit: that accumulation is **not
sustained** (the depth hump peaks then partially collapses) and it does **not** transfer to general
competence (composable competence beats fixed and the exp042 ratchet, but not drift). So the barrier
past **goal representation** is **goal alignment / credit assignment**: the collective can extend and
pursue a target, but it cannot tell *which of its parts* makes it competent, so it can neither aim the
goal at its own self-maintenance nor keep achieving a target that has grown past what its network can
build — it just deepens whatever arbitrary path it started with until that path outruns it.

The arc, one line each:
- **exp039** — fixed multi-objective doesn't compound → suspect heredity.
- **exp040** — break the heredity ceiling.
- **exp041** — still doesn't compound under a fixed objective → the fixed target.
- **exp042** — self-expand the target (scalar) → still doesn't, worse → **goal representation** is missing.
- **exp044** — give it heritable, composable goals → **deeper goals do accumulate** (composable ≫
  fixed), the arc's first over-generations deepening — *but the ratchet is transient (peaks then
  collapses) and doesn't lift generic competence* → the next barrier is **goal alignment / credit
  assignment**.

## Honest scope

"Competence" is a within-substrate composite; "goal depth" is achieved target-path length, a genuine
constructive achievement but a *specific* one. The goal *deepening* is robust across 4 seeds and 12k
ticks (peak ~4.3, max 7), decisively above the fixed control; the non-sustained (hump) shape and the
failure to beat drift on generic competence are likewise consistent across the seed-averaged windows.
The result is therefore a **mixed / partial positive**: composability produces the first
over-generations deepening the arc has seen (real, and absent in every prior rung), honestly bounded —
it is transient, confined to the represented dimension, and does not lift general competence. It does
not claim mind-like self-improvement; it claims the *missing faculty was real* and that supplying it
opens a new, sharper problem (keep achieving a growing target — credit assignment).

**Determinism caveat (discovered here, engine-wide — now FIXED in Ω-0.33).** Building exp044 surfaced
that the engine's per-tick reaction selection was sensitive to `PYTHONHASHSEED` (set/dict iteration
order feeding the niche-seed subset before it is recycled), so the same `seed` yielded different
absolute counts across process invocations (e.g. `classes_ever_seen` varied ~435–1732 at fixed
`seed=0`). The **directions** of every matched-control comparison were robust (composable ≫ fixed on
goal depth; composable doesn't beat drift on competence), but specific magnitudes reproduced only at a
fixed hash seed — and, as the table's determinism note records, the "sustained ratchet 2.4→4.0"
reading was one such favourable-seed magnitude. **Ω-0.33 fixed this at the source** (draw the niche
subset with `rng.sample` over a canonically-sorted candidate list); the numbers above are now
byte-identical across hash seeds, and a `test_deterministic_across_hash_seeds` guard prevents
regression.

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
