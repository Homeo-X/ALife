# exp059 — The self-improvement arc TRANSFERS to the living world: a persistent `living_world` is far more competent and self-maintaining than the exp030-era world (Ω-0.48)

The arc (Ω-0.41–0.47) proved *in batch* that a competence-compounding law (the Catalytic Law × Red Queen,
exp053) lifts collective competence far above the fixed-law plateau. But the watchable, persistent world
(`build_world`, `omega/world/`) was frozen at the exp030 era — both-corner + reify + culture + space with
`deme_fitness="network"`, none of the arc. exp059 asks whether the arc *transfers* to the persistent,
spatial, reifying, memory-eviction-bounded world regime — where it could easily be cancelled — and finds it
transfers strongly.

## Mechanism — the `living_world` builder + `WorldVitals` (both gated; the old `world` is byte-identical)

`living_world` = the `world` foundation (both-corner `typed_path` + reification + culture + spatial torus)
**plus** the arc's winners, all pre-existing gated knobs: `catalytic_law=True` (exp053, the compounding,
network-visible law), `deme_fitness="redqueen"` (exp052, the receding coevolutionary target),
`competence_pressure=1.0` (exp056, most robust *and* most diverse), and the exp040 heredity channel
(`network_template`). `WorldVitals` (`omega/world/vitals.py`) is a read-only reader that surfaces the arc's
signals live: the **competence trajectory** (mean `_deme_competence` + slope), **autocatalytic closure**
(mean `_deme_closure` — the life/self-maintenance signal, exp038), the **self-maintaining lifeform** count
(closed collectives), **breed-true heredity**, and the **genuine (eviction-robust) novelty rate** (the
Ω-0.39 global sketch, attached dynamics-invariantly to the universe). The old `world` builder and exp001–058
stay byte-identical.

## Result (persistent bounded-memory worlds, 30,000 ticks, 4 seeds)

| arm | competence | closure | self-maint. lifeforms | breed-true | genuine-novelty rate | diversity |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **living_world** | **1.92** | **0.60** | **23.5** | **0.37** | 0.27 | 2.28 |
| world (exp030-era) | 1.20 | 0.27 | 9.8 | 0.03 | 0.60 | 4.46 |

**Verdict: the arc transfers — the living world is dramatically more competent and more alive.**

- **Competence transfers (+0.72, ~60% lift).** `living_world` reaches competence **1.92** vs the exp030
  world's **1.20** — the Catalytic Law × Red Queen survives the persistent, spatial, reifying,
  eviction-bounded regime that could have cancelled it. It is not a batch-only artifact.
- **Life signals are ~2× stronger.** Autocatalytic closure **0.60 vs 0.27** (~2.2×), self-maintaining
  collectives **23.5 vs 9.8** (~2.4×), and breed-true heredity **0.37 vs 0.03** (~12×). By the substrate's
  own definition of life — autocatalytically-closed, self-maintaining, heritable collectives — the living
  world contains far more life.
- **Both worlds stay genuinely open.** The eviction-robust global-novelty rate is positive in both (0.27,
  0.60), so neither has converged; the living world *does* stay open-ended while compounding competence.

## Interpretation — two honest caveats (the science, not a demo)

1. **Competence reaches an elevated PLATEAU, not a rising slope (slope ≈ 0 in both arms).** Within a single
   persistent tier, `living_world` competence saturates high (~1.9) rather than climbing — exactly the
   exp053/exp054 lesson: the Catalytic Law compounds *then saturates at the substrate's optimal richness*.
   So the world upgrade buys a much higher competence **level**, but genuine *across-time* compounding needs
   a **new level** — the live recursive tower (Phase B / Ω-0.49), the exp055 across-level meta-ratchet made
   live. The honest headline is the level (and the life signals), not a within-tier slope.
2. **The living world is DEEPER, not WIDER.** It has *lower* raw diversity (2.28 vs 4.46 nats) and a *lower*
   genuine-novelty rate (0.27 vs 0.60) than the plain world. This is the exp056 canalization effect at world
   scale: strong competence selection focuses the world on competent, self-maintaining, breed-true structure
   (fewer, better, more persistent classes) rather than spraying many novel-but-incompetent ones. It is a
   real trade in *what kind* of open-endedness you get — competent depth vs raw novelty breadth — not a loss
   of open-endedness (both floors are positive). Which is "more alive" is a genuine question the census
   (Phase C) can quantify over the long horizon.

## Honest scope
4 seeds × 30,000 ticks, persistent bounded-memory worlds (the real world regime, not batch). The effect
sizes are large (competence +0.72, closure ~2.2×, breed-true ~12×) — well beyond seed noise at n=4 — so the
*direction* (the arc transfers; the living world is more competent and more alive but deeper-not-wider) is
robust; the exact numbers are estimates. The slope≈0 result is a plateau statement at this horizon, not a
claim about 10⁶ ticks (Phase C). Genuine novelty uses the Ω-0.39 eviction-robust sketch.

## Reproduce
`PYTHONPATH=. python3 studies/exp059_livingworld.py 30000 1000 4` → the table above; committed as
`studies/exp059_results.json` / `_console.txt`. Watch it live:
`python -m omega.world run --physics living_world --dashboard` (the vital-signs panel shows competence,
closure, self-maintaining lifeforms, and the genuine-novelty rate). Pinned by
`omega/tests/test_world.py::TestLivingWorldVitals` (living_world carries the arc and is more competent;
genuine novelty is dynamics-invariant and checkpoints). `living_world`/`WorldVitals`/`genuine_novelty`
default off ⇒ the exp030-era world byte-identical.
