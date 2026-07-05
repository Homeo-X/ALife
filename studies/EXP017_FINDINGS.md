# exp017 — Do collectives reliably outcompete individuals over long timescales?

**Question.** exp017 adds multi-level selection to the combinator soup: demes
(patches) reproduce — every `deme_gen` ticks a fraction go extinct and are
recolonized by a propagule copied out of a surviving deme, chosen with
probability proportional to its size (productivity). The open question was
whether selection genuinely acts on the *collective*: do fitter deme-types
spread and outcompete the rest, or does within-deme individual selection erode
collective structure until it collapses?

**Design.** Two studies, all `source` unless noted, 24 patches, `mut_prob=0.05`.

1. **Long-horizon contrast** — `propagule_mode="source"` (recolonize from a
   *single* surviving deme → collective composition is heritable) vs
   `"mixed"` (recolonize from the *well-mixed* survivor pool → heredity
   destroyed, identical disturbance). Horizons 1,500 / 6,000 / 12,000 ticks,
   6–8 seeds/arm.
2. **Mechanism sweep** — vary the exposed homogenization knobs
   (`mig_rate`, `propagule_size`, `deme_gen`) to see whether *any* of them
   convert the signal into genuine collective takeover. 6,000 ticks, 4 seeds.

Measured per run:

- **Collective heredity gap** = Jaccard(child deme class-set, its *source*) −
  Jaccard(child, a *random other* deme). Positive ⇒ children resemble their
  source more than chance ⇒ the collective is a unit of heredity. (Defined only
  for `source`; `mixed` has no source, so it reads 0 by construction.)
- **Between-deme winnowing** = `n_deme_types` (distinct most-abundant-class
  "types" across the 24 demes). Collective *selection* should drive this *down*
  as fit deme-types sweep. This is the signature that collectives are winning.
- **Collapse indicators** = final/min population, live-deme count.

Reproduce:
`python3 studies/exp017_multilevel_longrun.py <ticks> <n_seeds>` and
`PYTHONPATH=. python3 studies/exp017_mechanism_sweep.py`.

## Result: neither — a stable, near-neutral stalemate

### 1. Long-horizon contrast

| horizon | source late gap (self−null) | seeds +gap | n_deme_types early→late | final pop | live demes |
|--------:|:---------------------------:|:----------:|:-----------------------:|:---------:|:----------:|
| 1,500   | −0.0013 ± 0.0035            | 1/2        | 19.3 → 19.8             | 164 ± 6   | 23.9 / 24  |
| 6,000   | +0.0042 ± 0.0041            | 7/8        | 19.4 → 19.5             | 170 ± 9   | 23.9 / 24  |
| 12,000  | +0.0038 ± 0.0043            | 5/6        | 19.4 → 19.5             | 168 ± 8   | 23.9 / 24  |

Heredity-gap trajectory over 12,000 ticks (5 equal windows, source):
`+0.0019  +0.0047  +0.0030  +0.0042  +0.0038` — it rises early then **plateaus
at ~+0.004**; it does not compound. And it never converts into winnowing:
`n_deme_types` is pinned at ~19.5 of 24 at every horizon.

### 2. Mechanism sweep (6,000 ticks, 4 seeds, source)

| condition | heredity gap (late) | self / null | n_deme_types | final pop |
|-----------|:-------------------:|:-----------:|:------------:|:---------:|
| baseline (mig .02, psize 4, gen 40)   | +0.0059 | 0.033 / 0.027 (1.22×) | 19.4 / 24 | 172 |
| isolation (mig 0)                     | +0.0057 | —                     | 19.4 / 24 | 174 |
| big propagule (psize 16)              | +0.0044 | —                     | 19.5 / 24 | 170 |
| **isolation + big + fast (mig0, ps16, gen20)** | **+0.0368** | **0.065 / 0.028 (2.31×)** | **18.9 / 24** | 173 |

## Interpretation

**1. Collectives do NOT reliably outcompete individuals.** Between-deme
winnowing never happens: `n_deme_types` stays at ~19 of 24 at every horizon and
under every condition. The demes remain almost maximally diverse — no fit
collective ever sweeps.

**2. Collectives do NOT collapse either.** Population is ~170 with 23.9/24 demes
occupied across 1,500 → 12,000 ticks and across all sweep conditions; minimum
population never drops below ~68. No tragedy-of-the-commons crash.

**3. The limiting factor is NOT heredity — it is between-deme fitness variance.**
This is the sweep's key result and it corrects the obvious first guess (that a
global feed homogenizes demes and starves heredity). Removing migration and
using a deme-dominating propagule with fast turnover **more than doubles**
collective heredity (self/null 1.22× → 2.31×, a 6× larger gap). Yet that strong
heritable collective variation produces essentially **no** extra winnowing
(19.4 → 18.9 of 24). Heredity is necessary but nowhere near sufficient.

The missing ingredient is *heritable differences in deme fitness*. Deme
reproduction is weighted by deme size, but the reservoir cap (`total_quanta`
fixed, feed throttled by `reservoir_pressure`) pins every deme to roughly the
same size. With near-zero variance in the selected trait, size-weighted
propagule choice is effectively **neutral** — collective-level dynamics are
drift, not selection, no matter how heritable the collective is. That is exactly
the observed signature: a real but non-amplifying heredity channel riding on top
of a robustly stable individual-level ecology, with no directional collective
sorting.

## Takeaway and next lever

The "promising but modest" reading was right, and now has a mechanism: exp017
established collective **heredity** (and the sweep shows it can be made strong),
but never collective **selection**, because the substrate gives demes no
heritable fitness variance to select on. To make collectives actually outcompete
individuals the next experiment must create between-deme fitness differences that
propagate — e.g. a **per-deme resource budget** (each deme draws from its own
local reservoir, so a more productive deme composition literally supports a
larger/faster deme and founds more propagules), rather than one global cap that
equalizes them. Falsifiable prediction: under per-deme budgets the source arm's
`n_deme_types` should fall well below the mixed control; if it still does not,
collective selection is not viable in this substrate regardless of heredity
strength.
