# exp020 — Explicit replicase: when a strong replicator finally emerges, does the *collective* win?

exp017–019 hit the same wall: the SKI-combinator soup never makes a replicator
strong enough to sweep a patch (within-deme dominance caps ~0.37), so multi-level
selection has no heritable collective unit. exp019 traced this to the individual
level and predicted the fix was a stronger copying primitive. exp020 adds one.

**Mechanism (gated; exp012–019 stay byte-identical; determinism preserved; 23/23
tests pass).** An explicit **replicase**: a copy reaction `T -> T + T` where the
template is catalytic (not consumed) and the copy's distinguishability is paid from
the reservoir, so replication stays resource-limited (cheaper/compact templates win
the reservoir competition). `copy_rate` sets its strength, `copy_mut` its fidelity;
the copy inherits the template's patch, so replication is local. Registered as
`exp020` (= exp019 + replicase). Reproduce with `studies/exp020_replicase.py`.

## Result: replicators finally consolidate the soup — but as *individuals*, not collectives

### Copy strength raises consolidation, not within-deme dominance (seed 0, 3k ticks)

| condition | within-deme dom | global dom | n_deme_types | population |
|-----------|:---------------:|:----------:|:------------:|:----------:|
| exp019 (no copy)     | 0.251 | 0.076 | 19.4 | 175  |
| copy_rate 0.2        | 0.262 | 0.176 | 9.0  | 1089 |
| copy_rate 0.5        | 0.312 | 0.239 | 6.9  | 1662 |
| copy_rate 1.0        | 0.321 | 0.206 | 7.4  | 1513 |
| copy_rate 1.0, mut 0 | 0.337 | 0.162 | 10.4 | 1133 |

Copying grows the population to carrying capacity (175 → ~1500) and drives strong
consolidation — `n_deme_types` collapses 19 → ~7 and global dominance rises
0.08 → ~0.24. But **within-deme dominance never clears ~0.36**, even at perfect
fidelity. A *uniform* per-capita copy rate replicates every class equally, so it is
frequency-neutral within a deme; the only force shifting composition is the weak
compact-template advantage from reservoir competition. That advantage is enough to
make a few classes the global plurality, but never enough to fixate a deme.

### The decisive control: the consolidation is individual, not collective (source vs mixed, 4k ticks, 5 seeds)

| copy | mode | within-dom | global-dom | n_deme_types | live | types/live | pop |
|-----:|:----:|:----------:|:----------:|:------------:|:----:|:----------:|:---:|
| 0.0 | source | 0.250 | 0.079 | 19.3 | 24/24 | 0.804 | 174 |
| 0.0 | mixed  | 0.235 | 0.065 | 19.4 | 24/24 | 0.808 | 184 |
| 0.5 | source | 0.310 | 0.208 | 8.3  | 24/24 | **0.347** | 1156 |
| 0.5 | mixed  | 0.297 | 0.212 | 7.9  | 24/24 | **0.331** | 1383 |

With copying on, `source` and `mixed` are **identical on every axis** — within-deme
dominance (0.31 vs 0.30), global dominance (0.21 vs 0.21), `n_deme_types` (8.3 vs
7.9), and types-per-live-deme (**0.347 vs 0.331** — source is if anything *more*
diverse, not less). All 24 demes stay alive; population is up, not collapsed.

So the dramatic consolidation copying produces is **individual-level selection**: a
few compact replicators (cheapest to copy) colonize *every* deme equally, becoming
the plurality everywhere. Whether propagules preserve collective heredity (`source`)
or destroy it (`mixed`) makes no difference. This is not the collapse confound of
exp018/019 (demes are alive and full) — it is simply individuals winning.

## Conclusion — the four-experiment verdict

**In this substrate collectives never reliably outcompete individuals.** Four
escalating interventions each removed a candidate bottleneck and hit the same wall:

| exp | intervention | collective selection? |
|-----|--------------|:---------------------:|
| 017 | multi-level selection + collective heredity | no — heredity plateaus, no winnowing |
| 018 | + heritable between-deme fitness variance | no — winnowing only via collapse |
| 019 | + patch-local feed (local carrying capacity) | no — dominance ≤0.37, no winnowing |
| 020 | + explicit strong replicase | no — consolidation is individual (source = mixed) |

The multi-level structure is **inert**: across every regime, making the collective
heritable (source) versus not (mixed) never changes the outcome. When replicators
are weak (017–019) demes stay diverse mixes with no type to select; when a strong
replicase finally makes replicators consolidate the soup (020), they win as
individuals — colonizing all demes equally — and the collective level is
epiphenomenal. The only thing that ever reduces raw deme-type count *without* being
matched by the well-mixed null is population collapse (018–019 at starvation), which
is the opposite of a collective winning.

**Why (mechanistically).** A genuine collective transition needs (i) within-deme
dominance so each deme has a heritable type, and (ii) that type to be a *deme-level*
property selection can sort. This soup gives neither: replication is either too weak
to fixate a deme (017–019) or, when strong, is frequency-neutral per-capita so it
amplifies whole demes without differentiating them, and the compact-template
advantage acts globally (individual level), not between demes. Nothing in the
combinator dynamics couples a deme's *composition* to a deme-level *reproductive
rate* in a heritable way — the precondition Ω-0.14…0.17 were probing for.

**Next, if the thread is pursued:** the missing coupling would have to be built in
explicitly — e.g. a deme-level replicase whose *fidelity or rate depends on the
deme's collective composition* (a group-level trait), not a per-individual copy.
Short of that, the combinator substrate supports individual selection and open-ended
individual novelty (exp012–014) but not a major transition to collective
individuality. The honest verdict across exp017–020 stands: collectives do not
outcompete individuals here; every appearance of them doing so is either collapse or
individual replicators winning under a collective label.
