# exp033 — First-class levels: heterogeneous per-level physics

exp031/032 built a recursive tower, but *every tier ran the same exp030 `typed_path`
engine* — the self-similar engine climbing itself. The open frontier the arc handed forward
was to make the level abstraction **first-class**: let each tier run a **different
composition law** and ask whether the major transition still recurses **across a physics
boundary**, or whether the tower depended on self-similarity all along.

`omega/levels/stack.py` now takes `levels=(...)` — a per-tier sequence of registered
engines (cycled to `max_tiers`). Default `levels=None` runs `exp030` at every tier,
byte-identical to the pre-exp033 tower. Three engines share the type-atom interface (each
ingests the promoted alphabet via `explicit_atoms`, each exposes deme signatures) yet apply
**different composition laws**:

| engine | law | corner |
|--------|-----|--------|
| exp029 (typed) | morphism composition `(a→b)∘(b→c)` | modular, **closed** (novelty→0) |
| exp030 (typed_path) | path **concatenation** | modular, **open** |
| exp031_culture | typed_path **+ horizontal transfer** | modular, open, **+ Lamarckian** |

## Result (1500 ticks/tier, max_tiers=5, 3 seeds)

| recipe | law sequence | depth (per-seed) | boundaries survived |
|--------|--------------|:----------------:|:-------------------:|
| homogeneous_open | exp030×5 (self-similar) | **[5, 0, 5]** | 0/0 (none) |
| **alt_two_open** | exp030 ↔ exp031_culture (two *different* open laws) | **[5, 0, 5]** | **8/8** |
| alt_open_closed | exp030 ↔ exp029 (open vs closed) | [1, 0, 1] | 0/2 |
| progression | exp030→exp029→culture (a law per tier) | [1, 0, 1] | 0/2 |

Two facts, cleanly separated:

**(1) Crossing a physics boundary is *free*.** The `alt_two_open` tower — a *different*
composition law at every tier (concatenation alternating with concatenation+horizontal) —
has **per-seed depth identical to the self-similar baseline** ([5, 0, 5]) and **every one of
its 8 physics-boundary crossings survives** (the boundary tier forms heritable collectives
from the collectives of a tier that ran a *different law*). A tier does **not** need to run
the same engine as the tier below it. The recursion is a property of the *both-corner
condition*, not of self-similarity — **levels are first-class.** (The shared seed-1 `0` is
the same stochastic tier-0 failure documented in exp032; it hits the homogeneous baseline
identically, so it is not a heterogeneity effect.)

**(2) The one hard rung is *closure*, not difference.** Every tower that includes the
**closed** law (exp029) caps at depth 1: the closed tier forms only **1** collective
(heritable, self 0.176 > null 0.000, but < 2), so it cannot supply a ≥2-symbol alphabet
upward and the tower stops. This is not the boundary's fault — `alt_two_open` crosses just as
many boundaries and pays no penalty. It is *closure*: a closed law produces too few distinct
collectives to seed the next level. So the exp030 **"both corner" requirement reappears at
every level boundary** — each tier's law must itself be open **and** modular for the tower to
keep climbing. A closed law is a terminal rung.

## Interpretation

The recursive ladder does not depend on one engine climbing itself. Any level whose law is
**open-ended and modular** can sit on any other such level's collectives and continue the
tower — including a genuinely different law, and including the qualitatively distinct
*cultural* law on top of the biological one. What a level may **not** be, if the tower is to
continue, is *closed*: closure starves the promoted alphabet. This is the same condition that
made the *first* transition possible (exp030), now shown to govern the *composition of
levels* — one principle, operating both within a level and between levels.

- **Is:** the level abstraction made first-class — heterogeneous per-tier physics, the
  transition recurses across different composition laws (8/8 boundaries, no depth penalty),
  reproduced by `run_stack(levels=...)` with the default kept byte-identical.
- **Is not:** a demonstration that *every* law composes — a closed law is a terminal rung,
  and the set tested is three type-atom engines (a brand-new non-substrate law is future
  work). The healthy heterogeneity here is *open-law × open-law*.

## Reproduce
`PYTHONPATH=. python3 studies/exp033_heterogeneous.py 1500 5 3` prints the table above;
committed as `studies/exp033_results.json` / `_console.txt`. Claim pinned by
`test_exp033_tower_recurses_across_a_physics_boundary` (two different open laws stack across
a boundary; `levels=None` stays the self-similar exp030 tower) in
`omega/tests/test_experiments.py`.
