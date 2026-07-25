# exp068 — The ~1.9 tower plateau is a HARD expressivity ceiling, not a satisficing one: a rising cross-tier target does not lift competence — it starves selection and collapses the tower (Ω-0.57)

exp067 (Ω-0.56) showed *transparent* promotion does not raise the across-tier competence slope — the cap is
the per-tier substrate's optimal-richness ceiling, not the promotion boundary. exp068 asks the sharp
follow-on: **is that ~1.9 plateau a *satisficing* plateau (selection relaxing once "good enough" — a rising
target would push higher) or a *hard* expressivity ceiling (the substrate cannot build more, whatever the
target)?** The answer is unambiguous: **a hard ceiling.** Carrying a rising competence target across the
tower boundary does not make competence climb — it makes it *fall*, and collapses more towers.

## Lever (gated `carry_ratchet_bar` + `ratchet_seed`, off ⇒ byte-identical)

The tower runs the exp053 network-visible Catalytic Law but with `deme_fitness="ratchet"` (exp042: reward =
`0.05 + max(0, competence − _ratchet_bar)`, the bar chasing the achieved frontier and never lowering). A
gated physics `ratchet_seed` pre-loads `_ratchet_bar` at construction; `run_stack(carry_ratchet_bar=True)`
seeds tier N+1's bar from the level tier N reached (`physics._ratchet_bar`), so **each tier must EXCEED the
last to score above the floor**. Three arms: **ratchet_reset** (bar resets per tier — the within-tier
ratchet at tower scale, exp042's known plateau), **ratchet_carry** (H2 — differs ONLY by the carry),
**census_ref** (the exp053 + `law_from_competence` census tower — anchors the ~1.9 plateau).

## Result (5 tiers, 6000 ticks/tier, 5 seeds; per-tier competence on full-depth towers)

| arm | tier0 | tier1 | tier2 | tier3 | tier4 | across-tier slope | collapse | mean depth |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ratchet_reset | 1.773 | 1.746 | 1.878 | 1.790 | 1.803 | +0.0104 | 0.40 | 3.40 |
| **ratchet_carry** | 1.805 | **1.906** | **1.468** | 1.857 | **1.651** | **−0.0357** | **0.60** | **2.80** |
| census_ref | 1.830 | 1.865 | 1.923 | 1.958 | 1.903 | +0.0240 | 0.40 | 3.20 |

**A hard ceiling.** The carried rising target makes the across-tier slope **negative** (**−0.036** vs
ratchet_reset's +0.010 and census_ref's +0.024) — competence *drops* at deeper tiers (tier 2 = 1.468, tier 4
= 1.651, well below the ~1.9 plateau) — and it **raises the collapse rate** (0.60 vs 0.40) and **shrinks the
tower** (mean depth 2.8 vs 3.4). Carrying the bar is *actively harmful*, the opposite of a climb.

## Interpretation — the plateau is set by what each tier can EXPRESS, and locating that precisely

The mechanism is exactly the predicted hard-ceiling failure. When tier N reaches ~1.9 (the substrate's
optimal richness) and seeds tier N+1's bar there, tier N+1 **cannot build a network more competent than
~1.9** — so *no deme clears the seeded bar*, every deme collapses to the `0.05` floor, selection goes
**uniform (drift)**, and competence *erodes* while the diversity the tower needs thins (hence the higher
collapse and shallower depth). A rising target cannot extract competence the substrate cannot express; it
only removes the selection signal that was holding competence *at* the ceiling.

This **tightens the exp067 bound into a precise, two-experiment triangulation of the limit.** Cross-level
competence is capped by **what each tier can express** — the per-tier construction law — and it is:
- **not** the promotion boundary's opacity (exp067: transparent carry-over doesn't lift the slope), and
- **not** the selection target (exp068: a rising target doesn't lift it — it starves selection).

Two of the three candidate levers are now ruled out. The remaining one is **H3 — a genuinely richer per-tier
construction law** (change what a tier *can build*, not what it carries across or what it is selected toward).
That is the next, and now sharply-motivated, rung. It also re-frames the whole plateau: the ~1.9 ceiling is a
property of the *substrate's expressivity*, exactly as the within-level exp053/054 "rate up to optimal
richness, then a stock" law predicted — and it holds at tower scale against both a transparent boundary and a
rising target.

## Is / is not
- **Is:** a clean, decisive negative that resolves the satisficing-vs-hard-ceiling question (hard ceiling: a
  rising target makes competence *fall* and towers collapse), with a diagnosed mechanism (the seeded bar
  starves selection when it exceeds the substrate's expressivity). Together with exp067 it triangulates the
  limit to the per-tier law.
- **Is not:** a claim that competence can *never* climb across levels — only that neither carrying structure
  (exp067) nor raising the target (exp068) does it; a richer per-tier law (H3) is untested. Reused the
  ratchet-fitness platform (a possible Red-Queen-floor variant is a follow-on). 5 seeds; the negative
  (slope down, collapse up) is clear and directionally consistent with the probe. `carry_ratchet_bar=False`
  / `ratchet_seed` absent ⇒ byte-identical.

## Reproduce
`PYTHONPATH=. python3 studies/exp068_ratchet.py 5 6000 5` → the table above; committed as
`studies/exp068_results.json` / `_console.txt`. Pinned by
`test_exp068_cross_tier_ratchet_seeds_the_bar_and_gates` (`ratchet_seed` pre-loads the bar and changes
selection; `ratchet_seed=0.0` / `carry_ratchet_bar=False` ⇒ byte-identical; on, tier 0 is unchanged and
tier 1+ differ).
