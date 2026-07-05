# exp019 — Does patch-local feed unlock collective selection?

exp018 traced the failure of collective selection to an upstream, individual-level
cause: demes never crystallize a heritable *type* (within-deme dominance ≤0.35),
and the global feed's constant injection of random forms is the churn that blocks
local replicator takeover. Its predicted fix was a **patch-local feed**. exp019
implements and tests it.

**Mechanism (gated; exp012–018 stay byte-identical; determinism preserved; tests
pass).** `local_feed=True` directs each fed organism to a patch with probability
proportional to that patch's *local vacancy* (`target − occupancy`) instead of a
uniformly random patch. Scarce feed flows to empty demes (keeping them alive)
while a deme a replicator has filled stops receiving diluting feed — local carrying
capacity, at unchanged *total* feed (no global starvation). Registered as `exp019`
(= exp018 collective ingredients + local feed). Reproduce with `studies/exp019_*.py`.

## Result: local feed helps on two axes but still does not unlock collective selection

### Local vs global feed, feed_rate sweep (6k ticks, 5 seeds, `source`)

| feed | mode | within-deme dom | live demes | pop | types / live deme |
|-----:|:----:|:---------------:|:----------:|:---:|:-----------------:|
| 8 | global | 0.285 | 23.6/24 | 110 | 0.83 |
| 8 | local  | **0.321** | 24.0/24 | 113 | 0.85 |
| 4 | global | 0.330 | 21.7/24 | 57 | 0.82 |
| 4 | local  | **0.370** | **23.7/24** | 61 | 0.83 |
| 2 | global | 0.351 | 13.6/24 | 20 | 0.71 |
| 2 | local  | 0.333 | **18.7/24** | 16 | 0.54 |

Two genuine improvements from local feed: **within-deme dominance rises** at matched
feed (0.330 → 0.370 at feed 4), and **more demes stay alive** under low feed
(13.6 → 18.7 live at feed 2). It does relieve the exp018 collapse pressure somewhat.

### But the selection test fails (source vs mixed null, LOCAL feed, 6k ticks, 6 seeds)

The clean statistic is distinct types per *live* deme (divides out demes that merely
died). Collective selection ⇒ `source` below the well-mixed `mixed` null.

| feed | mode | live demes | pop | **types / live deme** |
|-----:|:----:|:----------:|:---:|:---------------------:|
| 4 (healthy) | source | 23.7/24 | 60 | **0.835** |
| 4 (healthy) | mixed  | 23.7/24 | 94 | **0.778** |
| 2 (collapsing) | source | 18.6/24 | 16 | 0.543 |
| 2 (collapsing) | mixed  | 22.4/24 | 70 | 0.706 |

In the **healthy** regime (feed 4, ~60 orgs, 23.7/24 demes alive) `source`'s
types/live is **0.835 — not below the null's 0.778, but slightly above it.** No
collective winnowing. The only regime where `source` drops below `mixed` (feed 2:
0.543 vs 0.706) is again near-collapse — `source` pop has fallen to 16 (~1 org per
live deme), so the low count is a tiny, class-poor population, not live demes
converging on winning types. Same collapse confound as exp018.

## Conclusion

**Patch-local feed does not unlock collective selection.** It is a real improvement
— higher within-deme dominance and much better deme survival under scarcity — but it
does not clear the barrier:

- within-deme dominance still **caps at ~0.37**; no deme ever crystallizes a crisp,
  heritable type;
- in every *healthy* regime, `source` shows **no** winnowing relative to the mixed
  null (feed 4: 0.835 ≥ 0.778);
- the only sub-null types/live is again a collapse artifact (feed 2, pop 16).

The barrier is deeper than feed geometry. Across exp017→exp019, within-deme
dominance never exceeds ~0.37 under *any* feed rate, feed placement, deme-fitness
rule, or heredity strength. The combinator soup simply does not produce a
self-replicator strong enough to sweep even a single isolated, locally-fed patch —
consistent with exp010's earlier result that copying never takes over. Multi-level
selection has no heritable collective unit to act on because the **individual level
never produces one**.

## Where this leaves the multi-level-selection thread

Three experiments (017 heredity, 018 fitness variance, 019 feed locality) have each
removed a *candidate* bottleneck and found the same wall. The evidence now points
away from the collective machinery entirely and onto the substrate's replicators:
**collective individuality cannot emerge until a within-deme replicator can locally
dominate (dominance → ~1), and the SKI-combinator soup does not support one.** The
productive next step is therefore not another multi-level knob but a stronger
copying primitive at the individual level — e.g. an explicit replicase/template
reaction whose fidelity and rate can push local dominance past ~0.5 — after which
exp017–019's collective machinery can be re-run to see whether selection finally
grips. Absent that, the honest verdict stands: **in this substrate collectives
never reliably outcompete individuals; the appearance of winnowing is always
collapse.**
