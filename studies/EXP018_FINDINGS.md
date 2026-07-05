# exp018 — Can collectives outcompete individuals if the substrate supplies what multi-level selection needs?

exp017's long-run study (`EXP017_FINDINGS.md`) found real collective **heredity**
but no collective **selection**: `n_deme_types` never winnowed. This follow-up
asks whether *engineering in* the missing ingredients makes collectives actually
win — and, if the only way to make them win is to starve the system, whether that
is victory or collapse. It ends on a firm answer: **collectives never reliably
outcompete individuals in this substrate; the one regime that superficially looks
like collective winnowing is deme die-off (collapse), and it is the same knob.**

New mechanism added (gated, exp012–017 stay byte-identical; determinism preserved;
20/20 scientific-claim tests pass): `deme_fitness="productivity"` weights a deme's
chance of founding propagules by its **construction throughput** (viable
applications it produced this generation) — a heritable, composition-derived trait
— instead of by headcount (`"size"`, the exp017 default). Registered as `exp018`
(productivity fitness + strong heredity). Reproduce with the four `studies/exp018_*.py`.

## Step 1 — Heritable fitness variance alone does nothing (2×2 factorial, 6k ticks, 6 seeds)

| cell | n_deme_types early→late | heredity self/null |
|------|:-----------------------:|:------------------:|
| size / weak (=exp017 baseline)   | 19.4 → 19.5 | 1.19× |
| size / strong                    | 19.1 → 18.9 | 2.37× |
| productivity / weak              | 19.4 → 19.3 | 1.02× |
| **productivity / strong (=exp018)** | 18.7 → 18.8 | 1.97× |

No cell winnows — all sit at ~19 of 24 deme-types. Productivity weighting (even
with strong heredity) does **not** make the collective win.

## Step 2 — Why: demes have no heritable "type" (variance diagnostic)

Measured at every deme reproduction (feed 14, `exp018`):

- between-deme **size** CV ≈ 0.52, **productivity** CV ≈ 0.31 → fitness variance
  *exists* (the weighting is not neutral — my first guess, that it was equalized,
  was wrong), but with ~7 organisms per deme it is dominated by small-number noise,
  and productivity/weak heredity self/null = 1.02× shows it is **not heritable**.
- **within-deme dominance** (fraction the most-abundant class holds inside a deme):
  mean **0.248**, max **0.339**.

The decisive number is within-deme dominance. No class ever dominates a deme; each
patch is a churning ~7-organism mix of mostly-distinct classes with no stable type.
A deme's "type" is a ~25%-plurality that reshuffles constantly — so there is no
heritable collective phenotype for between-deme selection to act on, no matter how
the propagule is weighted. The obstacle is upstream, at the **individual** level:
the combinator soup under constant global feed never produces a local replicator
takeover.

## Step 3 — Starving the feed makes heredity strong but crashes the system (feed sweep, exp018, 6k/5seed)

The global feed is the churn source, so cut it (all collective ingredients ON):

| feed_rate | within-deme dom | n_deme_types | heredity | final pop | live demes |
|----------:|:---------------:|:------------:|:--------:|:---------:|:----------:|
| 14 | 0.245 | 18.9 | 1.90× | 173 | 23.9/24 |
| 8  | 0.285 | 19.6 | 2.39× | 110 | 23.6/24 |
| 4  | 0.330 | 17.9 | 4.47× | 57  | 21.7/24 |
| 2  | 0.351 | **9.6** | 6.15× | **20** | **13.6/24** |

Heredity climbs to 6× as feed falls — but `n_deme_types` only drops at feed=2,
where population has crashed to 20 and 10 of 24 demes are **dead**. Within-deme
dominance never exceeds 0.35: even under starvation no crisp local type forms.

## Step 4 — The low-feed winnowing is collapse, not selection (source vs mixed control)

Compare `source` (collective selection ON) with the well-mixed `mixed` null at the
*same* feed. The clean statistic is **distinct types per _live_ deme** — it divides
out demes that merely died:

| feed | mode | n_deme_types | live demes | **types / live deme** | pop |
|-----:|:----:|:------------:|:----------:|:---------------------:|:---:|
| 4 | source | 17.9 | 21.7 | 0.82 | 57 |
| 4 | mixed  | 17.4 | 22.4 | 0.78 | 82 |
| 2 | source | 9.6  | 13.6 | **0.71** | 20 |
| 2 | mixed  | 14.1 | 20.3 | **0.70** | 66 |

At feed=2 `source` shows a much lower raw type count (9.6 vs 14.1) — but its
**types-per-live-deme is identical to the null (0.71 vs 0.70)**. The entire drop is
explained by having fewer live demes (13.6 vs 20.3), i.e. **demes dying**, not by
live demes converging onto shared winning types. If collective selection were
operating, `source` would have a *lower* types/live ratio than `mixed`; it does not.

## Conclusion

**Do collectives reliably outcompete individuals over long timescales, or collapse?
Neither — and the two are the same knob.**

- Collectives never outcompete: across long horizons, heritable deme-fitness
  variance, strong heredity, and the full feed range, between-deme selection never
  consolidates live demes onto shared winning types (types/live ≈ 0.7–0.8, matching
  the well-mixed null at every feed).
- The only thing that reduces deme-type diversity is deme **die-off** under
  starvation — collapse, not victory — and the feed cut that finally makes
  collective heredity strong (up to 6×) is precisely what crashes the population
  (173 → 20) and kills demes (24 → 13.6 live). There is no window where collectives
  cleanly win while the system stays healthy.
- Root cause (Step 2): individual-level dynamics never yield within-deme dominance
  (top class ≤ 0.35 even under starvation), so demes never crystallize a heritable
  type — multi-level selection has no unit to grip. This is robust to every lever
  the substrate exposes.

**Where this points.** The bottleneck is not the multi-level machinery but the
absence of a local replicator takeover. A genuine major transition here would
require the individual level to first produce within-deme dominance — e.g. a
**patch-local feed** (feed inherits a patch instead of landing globally) or a
per-patch reservoir, so a good local replicator can sweep its deme and give the
collective a stable, heritable phenotype *before* between-deme selection is asked
to sort it. Until within-deme dominance clears ~0.35, no amount of collective-level
selection pressure will make collectives outcompete individuals.
