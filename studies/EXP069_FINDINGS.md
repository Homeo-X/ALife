# exp069 — A richer per-tier construction law does NOT make competence compound across levels — it starves cross-production and collapses the tower: the ~1.9 ceiling is a HARD bound of the substrate (Ω-0.58)

exp067 (transparent promotion) and exp068 (a rising cross-tier target) both failed and **triangulated** the
limit to the per-tier construction law — the ~1.9 plateau is set by *what each tier can express*. exp069 tests
the last remaining lever: change what each tier can express. **It fails too — decisively.** A richer per-tier
law does not lift competence; it *starves cross-production and collapses the tower*. With exp067 and exp068,
all three candidate levers are now ruled out: **cross-level competence compounding is impossible in this
substrate.**

## Lever (gated `resolution_from_competence`, off ⇒ byte-identical)

`resolution_from_competence` DERIVES each tier's construction resolution from the competence achieved below:
a tier that clears `resolution_step` (=1.5) earns its successor a **+1 deeper composition law**
(`type_resolution`), capped at `resolution_cap` (=4). This is exp054's earned-reach idea applied *across* the
tower boundary — where the added richness composes lower-tier *collectives* (a genuinely new kind), the one
regime that exp055 argued might escape the within-tier depth trap that starved exp054. Two arms on the
exp053 + `law_from_competence` census tower: **fixed_law** (fixed per-tier resolution — the saturating
reference) and **richer_law** (+ `resolution_from_competence`; differs ONLY by the derived resolution).

## Result (5 tiers, 6000 ticks/tier, 5 seeds)

| arm | across-tier competence slope | collapse rate | mean depth | full-depth towers |
|:---|:---:|:---:|:---:|:---:|
| fixed_law | +0.0240 | 0.40 | 3.20 | 3/5 |
| **richer_law** | — | **1.00** | **2.40** | **0/5** |

**The richer law collapses the tower.** *No* seed reached full depth (collapse 1.00 vs 0.40; mean depth 2.40
vs 3.20), so there is no full-depth tower on which to even measure an across-tier slope — the deeper
construction law **starves cross-production** and the tower dies before it can climb. A shallower 4-tier
probe (3 seeds) shows the milder regime, where towers that *do* survive plateau flat: richer_law per-tier
**1.22, 1.88, 1.91, 1.88** vs fixed **1.22, 1.87, 1.95, 1.97** — **no climb**, ~1.9 at every tier. So the
richer law fails in both regimes: where it stays shallow it does not lift competence, and where it goes deep
it collapses the tower.

## Interpretation — the ~1.9 ceiling is a HARD bound; the program closes

This is exactly the exp054 mechanism, now at tower scale. A deeper construction reach makes the composition
law demand more parts per product than the network can reliably supply, so cross-production (the
autocatalytic closure the competence metric rewards) **starves** — within a tier exp054 saw competence
*fall* (0.577, the lowest arm); across tiers the starvation *compounds*, killing the tower outright. The
substrate has a fixed **optimal richness**: below it, structure is under-exploited; above it, closure
starves. A tier cannot be made to express more competence than that optimum, by *any* of the three levers a
cross-level ratchet could pull:

- **exp067 — carry the structure across the boundary (transparency):** does not lift the slope (the cap is
  not the boundary).
- **exp068 — raise the selection target across the boundary (a rising bar):** makes competence *fall* and
  collapses towers (no deme clears a bar the substrate can't reach — the cap is not the target).
- **exp069 — enrich the construction law across the boundary (a deeper reach):** starves cross-production and
  collapses the tower (the cap is not selection-side at all — it is the substrate's expressivity, and a
  richer law overshoots the optimum).

**The three-experiment triangulation is complete and consistent: cross-level competence compounding is
impossible in this substrate.** The world is open-ended in *construction and individuality* indefinitely
(novelty is a rate, towers have no intrinsic depth ceiling — Ω-0.39/0.50), and competent to a high, stable
level (~1.9), but **competence is a STOCK, not a rate, at world scale.** This is the precise, falsifiable
close of the self-improvement arc: the Catalytic Law made competence a rate *within* a level (Ω-0.42) up to
the substrate's optimal richness (Ω-0.43); that optimum is a **hard ceiling** that holds across tower levels
and cannot be passed by carrying structure, raising the target, or enriching the law. To exceed it would
require a *different substrate* whose per-level optimal richness is itself unbounded — a new physics, not a
new lever on this one.

## Is / is not
- **Is:** a decisive, mechanism-diagnosed negative (a richer law starves cross-production and collapses the
  tower; the exp054 depth trap at tower scale), completing a consistent three-lever triangulation that the
  ~1.9 ceiling is a hard bound of the substrate's expressivity.
- **Is not:** a claim that *no* substrate can compound competence across levels — only that *this* one cannot,
  via any of the three levers a cross-tier ratchet affords. The escape (an unbounded-optimal-richness
  per-level law) is a new-physics question, outside this substrate. 5 seeds; the collapse (1.00 vs 0.40) is
  unambiguous; the no-climb regime is from a 4-tier probe. `resolution_from_competence=False` ⇒ byte-identical.

## Reproduce
`PYTHONPATH=. python3 studies/exp069_richerlaw.py 5 6000 5` → the table above; committed as
`studies/exp069_results.json` / `_console.txt`. Pinned by
`test_exp069_richer_per_tier_law_derives_resolution_and_gates` (`resolution_from_competence=False` ⇒
byte-identical tier-for-tier; on with a low step, tier 0 is unchanged and deeper tiers run a richer law and
differ).
