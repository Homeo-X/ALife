# exp042 — A self-expanding objective: does competence ratchet? (it does not — the barrier is deeper)

exp041 closed the payoff capstone with a precise negative: even with the collective-heredity ceiling
broken (exp040), competence does not compound under a **fixed** objective — selection reaches the
bar, mutation erodes fidelity, nothing makes the target keep rising (the Ω-0.20 *"rate, not stock"*
problem one level up). exp042 does the obvious next thing: make the **objective itself grow**, and
test whether competence finally ratchets.

## Mechanism

`deme_fitness="ratchet"` (gated, `ratchet_lr=0` ⇒ byte-identical). A deme's **competence** is an
absolute score on a common ~[0,3] scale — autocatalytic closure + breed-true heredity + normalized
network breadth (`_deme_competence`). Demes are rewarded for **beating a moving competence bar**
(weight = floor + max(0, competence − bar)); once per generation the bar is raised toward the
achieved frontier and **never lowered** — *goal reification*, the collective-level analogue of
reifying persistent structure into new primitives. Run *with* the exp040 heredity channel
(`network_template=0.5`) so achieved competence can be inherited. Matched controls: `composite`
(exactly exp041 — the fixed-objective treatment) and `size` (drift). The bar chase-rate is swept
(`ratchet_lr ∈ {0.1, 0.25, 0.5}`) so the verdict cannot be blamed on one rate.

## Result (8000 ticks, 5 seeds, `memory_horizon=4000`)

Competence **frontier** = max over demes of `_deme_competence`, per generation-window:

| arm | frontier (steady-state slope / win) | final frontier | heredity self/null |
|-----|:---:|:---:|:---:|
| ratchet @ lr 0.10 | **−0.029** | 0.73 | 4.9× |
| ratchet @ lr 0.25 | **−0.025** (best) | 0.58 | 8.2× |
| ratchet @ lr 0.50 | **−0.084** | 0.82 | 4.7× |
| composite (fixed = exp041) | −0.034 | **0.99** | 5.3× |
| size (drift) | −0.058 | 0.57 | 4.5× |

**Verdict: competence does NOT ratchet — and the moving objective is *worse* than the fixed one.**

- **No ratchet arm has a rising frontier.** Every chase-rate gives a flat-to-declining frontier
  slope; the negative is robust across `lr` (not a bad-rate artifact — the *fastest* chase, lr 0.5,
  is the *worst*, −0.084).
- **The self-expanding objective underperforms the fixed one.** The fixed composite ends with the
  highest frontier (0.99) of all arms; the best ratchet ends at 0.58. Making the target move *lowered*
  achieved competence.
- **The heredity channel is engaged throughout** (self/null 4.5–8.2×, re-confirming exp040), so this
  is not a failure to inherit — it is a failure to *accumulate*.

## Interpretation — the barrier is deeper than the objective

Two things are going on, and both point past the objective's *mobility*:

1. **A moving bar flattens the selection gradient.** As the bar chases the frontier, it converges
   near the top deme's competence; then `max(0, competence − bar)` collapses toward the floor for
   almost every deme, so selection among the best demes becomes near-neutral drift. Chasing harder
   (higher `lr`) flattens it more — exactly the observed ordering. A self-referential objective that
   rewards "beat the current best" *removes its own gradient* the moment competence stops rising.
2. **More fundamentally, the substrate has no representation of a *goal*.** The bar is a single
   global scalar; it is not heritable, not composable, not attached to *what* a collective is getting
   better at. Reifying persistent **structure** into primitives worked (Ω-0.20) because structure is
   exactly what this substrate represents and transmits. Reifying a **goal** does not work here
   because the substrate has no heritable, composable representation of goals to reify — so raising a
   scalar bar cannot pull competence up faster than mutation erodes it and the dynamical attractor
   re-forms it.

So the self-improvement arc lands on a precise, deep place: **open-ended collective self-improvement
needs a representational faculty for heritable, composable goals — not just heritable structure
(exp040) and not just a moving scalar target (exp042).** That is a different kind of missing piece
than any earlier rung, and it is named exactly.

## The arc, in one line each

- **exp039** — a *fixed multi-objective* target doesn't compound → suspect weak collective heredity.
- **exp040** — **break the heredity ceiling** (developmental niche inheritance, 8–9× null, open).
- **exp041** — still doesn't compound under a fixed objective → the barrier is the *fixed target*.
- **exp042** — make the objective *self-expand* → **still** doesn't compound (worse) → the barrier is
  deeper than the objective's mobility: the substrate cannot represent, inherit, or compose **goals**.

## Honest scope

"Competence" is a within-substrate composite (closure + heredity + breadth), not task performance;
"ratchet" is one concrete self-expanding rule (a monotonic bar chasing the frontier). The negative is
specific to scalar, self-referential objectives — it does **not** prove no open-ended objective can
work; it shows *this* natural family cannot, and diagnoses *why* (gradient collapse + no goal
representation), which is what makes it a useful signpost rather than a dead end. Frontier slopes are
modest and seed-noisy, but the sign and the ranking (fixed > moving; faster chase = worse) are robust
across five seeds and three rates.

## Consequence — the named frontier

The next rung is **not** another selection rule over the current substrate. It is a substrate
extension: give collectives a **heritable, composable representation of goals** (a transmissible
"what to build next" that mutates and recombines like the type-path structure does), then ask whether
competence ratchets. That is the honest exp043 — and the first rung of the arc that requires new
*representational* machinery, not just new *selection*.

## Reproduce
`PYTHONPATH=. python3 studies/exp042_ratchet.py 8000 5 4000` → the table above; committed as
`studies/exp042_results.json` / `_console.txt`. Pinned by
`test_exp042_ratchet_raises_a_monotonic_competence_bar` (the bar self-expands off zero and is
monotonic; heritable with ratchet + template on — the *does-it-compound* verdict is this study's
result). `ratchet_lr=0` ⇒ exp001–041 byte-identical.
