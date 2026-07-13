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

## What this unblocks (the campaign)
With flat memory and 3× throughput, the headline open-endedness tests can move from *miniature*
to *at scale*: 10⁶-tick persistence and continuing-construction (bounded-to-bounded arms),
multi-seed distributions, and deeper towers. Still open for a future pass: optimizing the
`normalize` reduction engine (the dominant raw cost), and checkpoint/resume so multi-hour runs
survive container restarts (the RNG is picklable; `harness.run` would need to accept/emit a
`(Noise, Universe, physics, trackers, tick)` bundle).
