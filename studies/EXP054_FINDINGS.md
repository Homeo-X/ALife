# exp054 — The Earned Law: expanding *construction depth* does not break exp053's saturation (an honest negative that locates the real limit)

exp053 (Ω-0.42) broke the competence-flat wall — a Catalytic Law that promotes competent closure loops to
shared, network-visible *reactions* makes competence compound — but it **saturates** (~1.45 by ~8k ticks).
exp054 asked whether an *expanding* competence-dependent law (growing the composition law itself, not a
bounded reaction repertoire) sustains the rise. It does **not** — and the negative pins *why* competence
saturates.

## What the diagnostic established (why this mechanism, and its controls)

- **exp053's saturation is not the catalyst cap.** At 16k ticks, catalyst_max 16 / 80 / 400 give
  **byte-identical** trajectories (only ~10 distinct closure-core edges ever qualify to harvest). At fixed
  resolution the constructible space is finite, so competent structure exhausts.
- **`type_resolution` is the binding construction lever** (it sets the type-path length: res3→len-3,
  res5→len-5). From a cold start res5 slightly *beats* res3, but res8 (isolated) collapses, and raising
  resolution *mid-life* re-classifies products and orphans the network.
- So exp054 climbs resolution **gradually, at birth, per lineage** (`earned_law`): a deme earns +1 reach
  (added to type_resolution/max_size) iff its parent achieved enough closure at its current reach — fixed
  for the deme's life (non-destructive), self-limited by a rising closure threshold. Hypothesis: earning
  your way up reaches deep regimes a cold start can't.

## Result (20k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (mean, late-slope) | end-survival | mean reach |
|-----|:---:|:---:|:---:|
| catalytic (exp053, fixed richness) | **1.224**, +0.0036 | **0.79** | 0 |
| fixed-law (res3 baseline) | 0.800, +0.0123 | 0.73 | 0 |
| fixed-high (cold res8) | 0.742, +0.0102 | 0.60 | 0 |
| **earned** (climb resolution with closure) | **0.577**, −0.0032 | 0.46 | 3.67 |

**Verdict: the Earned Law fails — expanding construction depth is the *wrong* kind of law expansion.**

- **Earned competence is the *lowest* of all arms** (0.577 < fixed-law 0.800 < catalytic 1.224), with the
  *lowest* survival (0.46) and a *negative* late slope. Climbing resolution **hurts**: deeper type-paths
  make cross-production sparser, so closure (hence competence) *falls*. The earned law greedily overshoots
  the substrate's optimal richness (reach reached ~3.67 ≈ res ~6.7 within the first window) and stays in a
  worse regime.
- **The single-seed smoke was seed-noise.** A single run had earned climbing to reach 5 with a +0.009
  slope; across 6 seeds that vanishes (the exp046/exp052 discipline again).
- **Cold res8 does not collapse on the Red Queen base** (survival 0.60), correcting the isolated-substrate
  diagnostic — deeper resolution is merely *worse* (0.742 < fixed-law 0.800), not catastrophic here.
- **exp053's reaction expansion remains the best** (1.224): adding *reactions at fixed richness* beats
  expanding *construction depth*.

## Interpretation — the real limit is optimal richness, not a fixed law

exp054 refines exp053's open edge. Competence does not saturate because the law is *fixed* — it saturates
because **the constructible space has an optimal richness**, and the amount of competent (closure-forming)
structure at that richness is **finite**. Expanding the law along the *depth* axis moves *out* of the
optimum into sparser regimes where cross-production — the substrate of closure — is rarer, so competence
*drops*. The right kind of law expansion adds competent-structure *capacity at the optimal richness*
(exp053's reactions), not *depth*. This is a bias–variance-like ceiling: too shallow exhausts competent
structure (exp053 saturation); too deep starves cross-production (exp054). Competence is a rate up to the
optimal-richness ceiling, then a stock, and no depth-expansion breaks it.

**Consequence for rung 2 (exp055, transition-as-rule-change).** exp054 warns that a naive "richer/deeper
law" *hurts*; a rule-change must preserve viable (optimal-richness) cross-production. The level transition
is a *different* kind of rule-change — the higher tier composes lower-tier **collectives** (new entities,
a genuinely new level), not deeper paths of the same atoms — so exp054's depth-negative does not doom it;
but exp055 must derive the higher law so that cross-production stays viable at the new level, not just make
it "bigger."

## Honest scope
A clean negative on the both-corner typed_path substrate (6 seeds × 20k). It does not show *no* expanding
law can help — it shows the *construction-depth* axis is the wrong one (it degrades competence), and that
exp053's fixed-richness reaction expansion is the better mechanism. The earned climb could be tuned to
crawl (staying near res5), but the static res5 optimum itself does not compound (a −0.009 slope in the 16k
probe), so tuning converges to a non-compounding stock.

## Reproduce
`PYTHONPATH=. python3 studies/exp054_earned.py 20000 6 4000` → the table above; committed as
`studies/exp054_results.json` / `_console.txt`. Pinned by
`test_exp054_earned_law_climbs_construction_reach_with_achieved_closure` (reach climbs with achieved
closure, bounded by the cap; `earned_law` off ⇒ no climb). Deterministic across `PYTHONHASHSEED`;
`earned_law` default ⇒ exp001–053 byte-identical.
