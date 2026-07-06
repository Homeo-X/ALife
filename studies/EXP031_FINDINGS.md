# exp031 — Multiple levels of organization: physics → chemistry → biology → culture

exp030 completed **one** major transition (organizations → reproducible collective
individuals) and handed forward the frontier: a *transition of transitions*. This work
introduces multiple levels of organization two ways at once (the chosen scope): a
general **recursive tower** where each transition promotes level-*N* collectives into
level-*(N+1)* atoms, and a distinct **culture** level with horizontal, Lamarckian
transmission.

**The four levels, and the recursion.** Physics = the kernel (atoms + conservation);
chemistry = organization composition (`compose_path`) + reification; biology = demes with
reproducible network signatures (exp017–030); culture = horizontal motif transfer. The
core move (`omega/levels/stack.py`): after a tier runs the exp030 `typed_path` substrate,
its **stable heritable collectives** (live demes carrying a non-trivial network signature,
`self > null`) are each promoted to a fresh symbol, and that set of symbols becomes the
**next tier's atom alphabet** — so a tier-*(N+1)* atom literally *is* a tier-*N* collective
(an explicit nesting map is kept). Enabling hooks are gated so exp012–030 stay
byte-identical (`seed_states`, `explicit_atoms`, `horizontal_transfer` default off;
determinism preserved; 37/37 tests pass).

## Part A — the transition recurses: a self-sustaining level tower

`run_stack`, 2500 ticks/tier, up to 5 tiers, 5 seeds:

| tier | level (individuals) | alphabet | collectives formed | self | null | novelty | heritable |
|-----:|---------------------|:--------:|:------------------:|:----:|:----:|:-------:|:---------:|
| 0 | chemistry     | 32 | 18 | 0.255 | 0.048 | 0.41 | 5/5 |
| 1 | biology       | 22 | 23 | 0.118 | 0.034 | 0.45 | 4/4 |
| 2 | culture       | 23 | 22 | 0.137 | 0.038 | 0.47 | 4/4 |
| 3 | meta-culture  | 22 | 23 | 0.125 | 0.034 | 0.46 | 4/4 |
| 4 | meta²-culture | 23 | 23 | 0.136 | 0.037 | 0.46 | 4/4 |

**Tower depth: mean 4.0, max 5, full 5-level stack in 4/5 seeds** (one seed failed at
tier 0 and never started — an honest failure case). The result is that **the major
transition recurses**: at every tier, the tier's collectives (a) form heritably
(`self > null` in every seed that reached the tier) and (b) keep the world open
(novelty 0.41–0.47, undiminished up the tower), so they satisfy the exp030 "both"
condition *again*, and their collectives become the next tier's individuals. Chemistry →
biology → culture → meta-culture emerge as successive tiers of one engine, with explicit
nesting (a tier-4 individual unfolds through tiers 3/2/1/0 to the base organizations it
contains). Collective heredity is strongest at tier 0 (0.255) and settles to a healthy
0.12–0.14 at higher tiers — the tower is self-sustaining, not decaying.

## Part B — the culture level: horizontal, Lamarckian transmission

Biology transmits *vertically* (propagule → offspring). Culture is *horizontal and
Lamarckian*: `horizontal_transfer` lets a deme imitate a fitter deme's top network motif
within its lifetime (injected into its recycle buffer), decoupled from reproduction.
Contrast at 2500 ticks, 5 seeds:

| horizontal_transfer | horizontal events | vertical events | H/V | # signatures | novelty |
|:-------------------:|:-----------------:|:---------------:|:---:|:------------:|:-------:|
| 0.0 | 0   | 868 | 0.00 | 13.5 | 0.41 |
| 0.3 | 589 | 868 | 0.68 | 17.0 | **0.57** |

A substantial horizontal channel opens (~0.68× the vertical rate), and — the distinctive
signature of culture — it **accelerates innovation**: novelty rises 0.41 → 0.57 and
distinct collective signatures rise 13.5 → 17.0. Horizontal transfer spreads motifs
across collectives, which *recombine* with each recipient's own motifs into new
signatures faster than reproduction alone could — memetic evolution as an innovation
amplifier, qualitatively distinct from the vertical genetic channel below it.

## Interpretation — organization is a recursive ladder, not a single jump

The whole exp017→031 arc resolves to this: a substrate that is modular *and* open-ended
(exp030) does not just permit *one* transition to collective individuality — the same
condition holds *at the collective level too*, so the transition **recurses**, building a
tower of organizational levels (Part A), and horizontal transmission adds a
qualitatively new *cultural* dynamic on top (Part B). Physics → chemistry → biology →
culture are not four hand-built modules but successive outputs of one recursive engine,
each level's individuals composed of the level below.

## Status and what remains
- **Multiple levels of organization: achieved in miniature** — a 4–5 deep recursive
  tower, each tier heritable and open-ended, plus a distinct horizontal/cultural level.
- **What remains** (the program's original frontier, now at every level): proving it
  **unbounded** — that the tower keeps climbing (does depth grow with more ticks/larger
  base?) and that each level's heredity *and* novelty persist over 10⁵⁺ ticks; and
  making the level abstraction fully first-class (per-level physics, not only the
  self-similar typed_path engine). exp031 turns "introduce multiple levels" from an
  aspiration into a working, measured recursive tower with a cultural apex.
