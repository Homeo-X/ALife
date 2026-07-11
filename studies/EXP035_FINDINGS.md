# exp035 — A genuinely new level law: binary-tree grafting

exp033 (Ω-0.18) made levels first-class and showed the tower crosses physics boundaries
freely — but among **three type substrates** (typed / typed_path / culture), and it found
the hard requirement at each level is the exp030 "both corner" (open AND modular). This asks
the deeper question: is the both corner a property of that *family* of laws, or of **any**
open+modular law? It adds a law unlike all three and tests whether it, too, yields heritable,
open collectives and recurses.

## The new law

Organizations are binary **trees**; composition grafts two into a node `(f, x)` — a
non-associative, non-commutative branching combination — then caps depth to
`tree_resolution` (collapsing subtrees deeper than the cap to their leftmost atom), the
branching analogue of typed_path's path-length truncation. It is distinct from all prior
laws: linear concatenation (associative), morphism composition (endpoint-matched), and
combinator reduction (rewriting). The depth cap is what bounds identity so products fall back
into existing classes (closed loops → heredity); without it (large resolution) trees grow
unboundedly distinct — the open-but-unreproducible combinator corner. Gated: `substrate !=
"tree"` is byte-identical.

## Part A — does the new law reach the both corner? (1500 ticks, 3 seeds)

| law | self | null | ratio | novelty | both corner? |
|-----|:----:|:----:|:-----:|:-------:|:------------:|
| tree, resolution 2 | 0.048 | 0.016 | 3.10 | 0.033 | yes (barely open) |
| tree, resolution 3 | 0.032 | 0.011 | 2.85 | 10.37 | yes |
| tree, resolution 4 | 0.030 | 0.008 | 3.67 | 12.71 | yes |
| **path (exp030 ref)** | **0.346** | **0.071** | **4.91** | **0.398** | **yes (strong)** |

The tree law **reaches the both corner** — heritable collectives (self > null, ratio ~3×)
coexist with sustained novelty (> 0) at every resolution, and `tree_resolution` is a
closed↔open dial (res 2 nearly closed, res 3–4 wide open) exactly like typed_path's dial.
**But its heredity is an order of magnitude weaker** than linear paths (self ~0.03–0.05 vs
exp030's ~0.35; ratio ~3× vs ~5×). So the *condition* generalizes; the *strength* does not —
linear concatenation is a specially good both-corner law, the branching law a viable but weak
one.

## Part B — does the new law recurse in the tower? (path ↔ tree)

| recipe | tower depth (mean±sd) | boundaries survived |
|--------|:---------------------:|:-------------------:|
| homogeneous_path (exp030×4) | 2.7 ± 1.9 | 0 |
| alt_path_tree (exp030 ↔ exp035) | 2.7 ± 1.9 | **6** |

A tower alternating path and tree tiers reaches the **same depth as the homogeneous path
tower** (2.7 ± 1.9; the high variance is the stochastic early-tier failure seen since exp031,
not a tree effect), and **every path/tree boundary crossed is survived** (6/6 across seeds).
Per-tier (seed 0): tier0 path (heritable, open), tier1 tree (heritable), tier2 path
(heritable, open), tier3 tree (heritable) — the tree law forms heritable collectives from a
path tier's collectives and hands its own collectives back to a path tier. **The new law
recurses**, extending exp033's first-class-levels result to a law outside the type-substrate
family.

## Interpretation

Combined with exp033, the picture is: what a level needs is not a particular composition law
but the **both-corner property** (open + modular). A branching law unlike all three type
substrates satisfies it and slots into the tower — so the recursive ladder is substrate-
general, governed by a *condition*, not a specific engine. The honest qualifier: not all
open+modular laws are equal — linear path concatenation reaches far stronger collective
heredity than tree grafting, so the *quality* of individuality a level attains does depend on
its law.

## Honest scope
- The tree both corner is **weak** (self ~0.03–0.05); it clears self > null and novelty > 0
  robustly across seeds, but does not approach typed_path's strong reproducible heredity.
- Tree tiers in the tower run at the default `tree_resolution=2` (near-closed, novelty ~0 at
  a tier) yet remain heritable — they recurse, but contribute little within-tier openness;
  the path tiers carry the tower's novelty.

## Reproduce
`PYTHONPATH=. python3 studies/exp035_tree.py 1500 3` → the tables above; committed as
`studies/exp035_results.json` / `_console.txt`. Claim pinned by
`test_exp035_new_tree_law_reaches_the_both_corner` in `omega/tests/test_experiments.py`.
