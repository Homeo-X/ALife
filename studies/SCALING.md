# Scaling Ω toward the initial goal (unbounded, not in-miniature)

The verdict after exp035/Ω-0.20 named the program's remaining gap plainly: the
open-endedness results are *in miniature* — horizons ≤ 250k ticks, few seeds — because two
structures cap how long a run can go, and a third makes every tick slow. This note records
the scaling infrastructure that lifts those caps. All of it is **gated / behavior-preserving**:
every prior experiment (exp001–035) is byte-identical, verified against the committed code.

## The three limits, and the fixes

### 1. Memory grew with cumulative novelty → OOM (the hard cap)
A genuinely open-ended run keeps minting new classes, and the kernel retained one record per
**class ever seen** (`Universe.class_registry`, plus the parallel `class_births/fed/constructed`
dicts) and one `Relation` per reaction **ever** — both O(ticks). A literal 10⁶-tick run hit
GB-scale RAM and could not complete (see the exp034 megatick note).

**Fix — bounded-memory long-run mode** (`omega/kernel/universe.py`, gated by
`Universe.memory_horizon` / `relation_cap`, both 0 by default → nothing evicted → byte-identical):
- The one coupling that blocked eviction was `NoveltyTracker`, which counted novelty as
  `len(class_registry)`. Decoupled via a monotonic `Universe.classes_ever_seen` counter
  (incremented when a class is first recorded); `NoveltyTracker` now counts against *it*, so
  the registry is free to shrink while novelty stays exact.
- `bound_memory()` (called each tick when a horizon is set) evicts class records not seen for
  `memory_horizon` ticks — from the registry **and** the amplification tallies, so
  `amplification()`'s scan stays bounded too (no incremental-tracking risk). Old provenance
  `relations` past `relation_cap` are trimmed.
- **Honest caveat (windowed novelty).** Because a class evicted after `memory_horizon` ticks of
  absence is counted as a fresh discovery if it reappears, bounded-mode novelty is a
  *horizon-windowed* rate — numerically **higher** than unbounded novelty (measured ~0.36 →
  0.51 at horizon 3000 on exp030/12k). It still cleanly separates open (> 0) from closed (→ 0),
  but bounded runs must be compared **bounded-to-bounded only** (the inflation is common-mode
  and cancels across arms of one study). Lifetime-aggregate readers (persistence spectrum,
  amplification) likewise become horizon-windowed under eviction.

Measured (exp030, 12k ticks): registry 5846 → 2084, peak traced memory **69.7 MB → 9.9 MB** —
and the gap widens without bound as the horizon grows, so 10⁶+ ticks now runs at flat memory.

### 2. Every tick re-hashed persistent state → 3× slower than necessary
`canonical_cls` (SHA1 of `repr(state)`), `distinguishability`, and `_depth` are **pure
functions of an immutable, hashable state**, yet were recomputed 4+ times per tick for every
live organization (`observe_classes`, ~3× `class_population`, `spawn`). 

**Fix — memoize the three** (`omega/kernel/organization.py`, bounded `lru_cache(maxsize=2^19)`
→ leak-free, byte-identical). Measured: exp030 **5.28 → 1.71 ms/tick (3.1× faster)**. A 10⁶-tick
run drops from ~90 min to ~28 min.

### 3. `amplification()` scanned every class ever → O(classes-ever)/tick
It rescans `class_constructed` each tick — fine at small scale, but asymptotically O(cumulative
classes) on a long horizon. The bounded-memory mode (fix 1) evicts cold entries from that dict
too, so the scan stays bounded automatically; no separate change needed.

## How to use it

```python
from omega.experiments.harness import run
r = run(physics, cfg, record_stride=..., memory_horizon=20000, relation_cap=50000)
```
`memory_horizon=0` (default) = unbounded, exact, byte-identical (all existing studies).
For a long run, pick a horizon **much larger than the class-turnover timescale** (to keep the
windowed-novelty inflation small) but small enough to bound memory — e.g. 10k–50k for a 10⁶-tick
run. Pinned by `test_bounded_memory_mode_flattens_registry_and_stays_open`.

## Instrument validation — bounded reproduces unbounded (250k, 3 arms)

Before trusting the bounded instrument at long horizons, it was checked against the *known*
unbounded 250k continuing-construction result (Ω-0.20). Same 3 arms (baseline / capped /
uncapped), `memory_horizon=50000`:

| arm | bounded late/early | unbounded late/early (Ω-0.20) | verdict |
|-----|:------------------:|:-----------------------------:|:-------:|
| baseline (never constructs) | 0.85 | 0.51 | decays |
| capped (stops constructing) | 0.96 | 0.67 | decays after freeze |
| **uncapped (keeps constructing)** | **1.25** | **1.16** | **sustains/rises** |

The **ordering and conclusion are identical** — only continuing construction sustains novelty;
uncapped's late-window rate (0.87) dwarfs capped (0.38) and baseline (0.28). The decaying arms'
ratios sit *higher* under bounding exactly because bounded novelty is horizon-windowed (the
reappearance floor lifts a decaying rate) — a common-mode effect that does not touch the
bounded-to-bounded comparison. Memory stayed flat (registry 18k–44k, not ~175k) and heredity
alive (self ≈ 0.085 ≫ null ≈ 0.015). **The bounded instrument is validated for long-horizon,
bounded-to-bounded studies** (`studies/exp034_megatick_bounded250000_results.json`).

## What this unblocks (the campaign)
With flat memory and 3× throughput, the headline open-endedness tests can move from *miniature*
to *at scale*: 10⁶-tick persistence and continuing-construction (bounded-to-bounded arms),
multi-seed distributions, and deeper towers. Still open for a future pass: optimizing the
`normalize` reduction engine (the dominant raw cost), and checkpoint/resume so multi-hour runs
survive container restarts (the RNG is picklable; `harness.run` would need to accept/emit a
`(Noise, Universe, physics, trackers, tick)` bundle).

## Update (Ω-0.31) — the reappearance floor is now measured out, not just controlled for

The caveat above — bounded novelty is horizon-windowed, so an evicted class that reappears re-counts
and lifts the rate (valid only for *bounded-to-bounded* comparison) — is now fixed by a fixed-memory
**global** novelty estimator: `omega/emergence/global_novelty.py` (`GlobalNoveltySketch`, a scalable
Bloom "ever-seen" set), enabled with `harness.run(global_novelty=True)` (gated, off ⇒ byte-identical).
It counts each class only once *ever*, so it strips the recycling inflation and measures the
**absolute** genuine-novelty rate, not just a bounded-to-bounded ratio.

`studies/exp043_unbounded.py` (300k ticks, 3 seeds) settles the headline claim with it: the open
engine (exp030) holds a **genuine positive novelty floor (~0.13 new-never-seen classes/tick at 300k)**,
decisively above the closed control (exp029, whose global rate is **exactly 0** — its windowed
"novelty" was 100% recycling). Two consequences: (1) "stays open" is real, not a windowing artifact,
now past the prior 120k/250k horizons; (2) the previously-reported *flat* windowed rate is **~4×
inflated** by recycling — the true genuine rate is positive but **slowly declining** (halves over
300k). So the absolute "constant rate" reading of earlier bounded runs is an *upper bound*; their
ranking claims (open ≫ closed; continuing ≫ capped construction) are unaffected. See
`studies/EXP043_FINDINGS.md` and `RESEARCH_LOG` Ω-0.31. Residual: does the global rate asymptote
above zero at 10⁶–10⁷ ticks? — now a clean run, not a conceptual gap.
