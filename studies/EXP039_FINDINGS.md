# exp039 — Capstone: the machinery for self-improvement is present; high-fidelity collective heredity is not

This closes the self-improvement arc (exp036→039) that asked whether Ω's native collectives could
evolve toward something like self-improving agents. exp038 left the sharp question: every *single*
selection proxy Goodharts (network → runaway openness, closure → low heredity) — so does
**multi-objective** selection compound, or is the trade-off a hard frontier?

## Two findings

**(1) The trade-off is NOT fundamental.** Across demes, closure and collective heredity are
**independent** — corr = −0.001. Both-high demes exist; nothing in the substrate forbids a
collective that is *both* self-maintaining and faithfully reproduced. So exp038's trade-off was a
single-objective *selection* artefact, not a Pareto frontier.

**(2) But multi-objective selection still does NOT compound.** `deme_fitness="composite"` (a
maximin over the two mean-normalized objectives — the standard "force both high" operator) was run
against the single-objective controls (6000 ticks, 3 seeds):

| selection | closure | heredity (self) |
|-----------|:-------:|:---------------:|
| **composite** | **0.078** | 0.106 |
| closure | 0.064 | 0.102 |
| network | 0.046 | **0.209** |
| size | 0.028 | 0.117 |

Composite reaches the **highest closure of all** (0.078) but leaves **heredity low** (0.106 — vs
0.209 under direct network selection). Three composite formulations (multiplicative,
mean-normalized, maximin) all give the same shape: **closure compounds; heredity does not.**

## The diagnosis — it is the collective-heredity channel, not selection design

Why can selection lift closure but not heredity, when both-high demes exist? Because **collective
heredity is the weak channel** — the exp028 result, now decisive here. exp028 quantified that a
deme's network signature transmits only moderately faithfully (self ≈ 0.1–0.25, a ~3–5× ceiling
that is *substrate-limited*). Selection can only stack a property as fast as it is inherited; a
weakly-transmitted trait cannot be concentrated, no matter how the fitness is shaped. Closure (a
local, low-dimensional loop property) transmits well enough to select; the full multi-edge network
heredity does not. So competence **cannot compound** — each generation loses too much of the
collective phenotype for improvements to accumulate.

## The verdict on the self-improvement question

Across the arc, honestly:
- **exp036** — intrinsic function cannot be *selected* without a substrate that can *represent* it
  (the third wall).
- **exp037** — per-collective evolvable internal state supplies representation; architecture *can*
  evolve — but a single proxy Goodharts.
- **exp038** — an emergent, selectable coherence target (autocatalytic closure) exists — but a
  single proxy trades off.
- **exp039** — the trade-off is not fundamental (objectives are independent), yet multi-objective
  selection still cannot make competence **compound**, because **collective heredity is too
  low-fidelity** to stack a multi-property phenotype.

So: **the machinery for self-improvement is present** — collectives can carry evolvable internal
state (exp037) and be selected on emergent coherence (exp038) — **but the missing piece is
high-fidelity collective heredity**, not more selection pressure or a cleverer objective. This is a
precise, falsifiable location of the barrier, and it points the follow-on work squarely at the
exp028 ceiling: raising collective transmission fidelity (a stronger heritable substrate for the
*whole* network, not just its dominant loop) is the prerequisite for open-ended collective
self-improvement. Until then, Ω collectives are evolvable and selectable but do not compound into
minds.

## Reproduce
`PYTHONPATH=. python3 studies/exp039_capstone.py 6000 3` → the correlation + table above; committed
as `studies/exp039_results.json` / `_console.txt`. Claim pinned by `test_exp039_*` in
`omega/tests/test_experiments.py`; `deme_fitness != "composite"` leaves exp001–035 byte-identical.
