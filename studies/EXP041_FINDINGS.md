# exp041 — Does competence compound once the heredity ceiling is broken? (the payoff capstone)

The self-improvement arc (exp036–039) ended with a precise verdict: the machinery for mind-like
collectives is present (exp037 evolvable per-collective state; exp038 selectable emergent coherence)
but **competence could not compound** because collective heredity was too weak (exp039: even the
aligned closure-AND-heredity maximin left heredity pinned at the exp028 ceiling). exp040 then
**broke that ceiling** — developmental (network-template) niche inheritance lifted collective
heredity well past it while a *partial* template kept the world open. exp041 is the test the whole
arc was built toward: with a strong heredity channel now available, does competence finally
**compound** — closure, heredity, and function rising *together* over generations — or does aligned
multi-objective selection still trade them off?

## Design

Run the two mechanisms together and watch a **trajectory** (not exp039's endpoint means). Three
matched arms, all with `measure_xprod=True` (a pure gauge — no RNG, cannot perturb dynamics):

- **composite+template** (treatment): `deme_fitness="composite"` + `network_template=0.5`
- **composite** (control): `deme_fitness="composite"` + `network_template=0.0` — *exactly exp039*;
  isolates the developmental channel's contribution
- **size+template** (drift): `deme_fitness="size"` + `network_template=0.5` — isolates the template
  from selection

The run is binned into 8 generation-windows. Per window we record mean **closure**
(`_deme_closure`), **heredity** (mean of the *new* `_hered_edge_self` vs `_hered_edge_null` entries
in that window — a per-window rate measured *at* reproduction events, so phase-correct), and a
**function** proxy (network breadth `len(_deme_edges)`, sampled densely to average over the
deme-generation phase). We report each axis's *relative* slope (fractional change per window) over
the full run and over the post-transient steady state, and a normalized weakest-axis trajectory.

## Result (8000 ticks, 5 seeds, `memory_horizon=4000`)

| arm | closure (mean · steady slope) | heredity self (mean · steady slope) | function (mean · steady slope) | self/null |
|-----|:---:|:---:|:---:|:---:|
| **composite+template** (treatment) | 0.286 · **+1.1%** | 0.256 · **−4.5%** | 4.55 · **+3.6%** | **3.4×** |
| composite (control = exp039) | 0.221 · +2.5% | 0.149 · **−6.7%** | 5.01 · +4.4% | 3.2× |
| size+template (drift) | 0.055 · +4.6% | 0.263 · **−13.6%** | 1.83 · −5.5% | 6.4× |

**Verdict: competence does NOT compound.**

- **Both mechanisms work — separately.** The template raises the heredity *level*: treatment self
  0.256 = **1.7× the composite-only control** and **3.4× null**, re-confirming exp040. Composite
  selection raises the constructive axes: closure 0.286 and function 4.55 tower over the drift arm's
  0.055 / 1.83. Neither is inert.
- **But heredity still declines across generations in every arm** (steady-state −4.5% / −6.7% /
  −13.6% per window). The developmental channel *slows* the erosion (−4.5% treatment vs −6.7%
  control) but does not reverse it. Closure and function only drift near-flat. **No arm shows the
  three axes rising together** — the weakest axis (heredity) erodes while the others hold.
- **Raising the heredity *level* was necessary but not sufficient.** A higher floor does not make a
  multi-property phenotype *accumulate*; the collective still loses reproduction fidelity to
  mutation faster than selection rebuilds it.

## Interpretation — the blocker moves from "weak heredity" to "no open-ended objective"

exp040 fixed the *level* of collective heredity; exp041 shows the barrier to self-improvement was
never only the level. There is a **separate compounding barrier**: with a **fixed** selection
objective, selection climbs to the bar and stops, while mutation continuously erodes fidelity — so
competence plateaus and slowly decays instead of stacking. Nothing in the setup makes the *target
itself* keep rising, so there is no ratchet.

This is the program's own **"rate, not stock"** lesson (Ω-0.20) re-derived one level up. Ω-0.20
showed a *substrate* stays open only under *continuing* construction (reification is a rate). exp041
shows a *collective* improves open-endedly only under a *continuing* objective — a selection target
that reifies new goals as competence grows. A fixed composite maximin is a **stock**; open-ended
self-improvement needs a **rate**. The drift arm makes the point sharply: it gets the *highest* raw
heredity (6.4× null) essentially for free from canalization, yet has almost no closure or function —
heredity level alone is not competence, and the three axes genuinely trade against one another under
any fixed scalar.

## Honest scope

The three axes are correlated proxies within one substrate, not independent faculties; "function"
is network breadth, a construction proxy, not task performance. The steady-state slopes are modest
and seed-noisy, but the *sign* is robust and agrees between the full-run and post-transient
measurements, and across all three arms: heredity is the declining axis everywhere. The verdict is
therefore a clean **negative that sharpens the located blocker**, not a null from underpowering:
strong collective heredity is available (exp040) and still does not produce compounding, because the
missing piece is an **open-ended objective**, not more heredity or more selection pressure.

## Consequence — the next frontier

The self-improvement arc closes with a precise, falsifiable hand-off. The machinery is present
(exp037/038), the heredity channel is open (exp040), and the remaining gap is named: **an
open-ended, self-expanding selection objective** — collective-level reification of *goals*, the
analogue of substrate-level reification of *primitives*. That is the natural exp042 (see
`docs/ROADMAP.md`): make the deme objective itself grow — e.g. reward *increasing* closure/heredity/
breadth relative to a moving baseline, or promote a collective's achieved competence into the next
target — and test whether competence then ratchets.

## Reproduce
`PYTHONPATH=. python3 studies/exp041_compound.py 8000 5 4000` → the trajectories above; committed as
`studies/exp041_results.json` / `_console.txt`. Pinned by
`test_exp041_composite_and_template_compose` in `omega/tests/test_experiments.py` (the mechanism is
sound: heritable with the template on, and composite selection acts atop it — the compounding
verdict is this study's result). `network_template=0` ⇒ exp001–040 byte-identical.
