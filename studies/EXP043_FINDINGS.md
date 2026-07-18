# exp043 (consolidation) — "Stays open forever," settled: a genuine positive novelty floor — and the old "flat rate" was ~4× a measurement artifact

The whole program rests on one claim: **constructibility keeps the world open**. Every long-horizon
check of it (exp032, exp034) had to run under bounded memory (`memory_horizon`), which evicts cold
class records — so an evicted class that reappears **re-counts** in the novelty rate. A positive
long-run *windowed* rate therefore could not be distinguished from the same classes recycling through
the eviction window (exp032's explicit "positive-floor vs slow-dilution unsettled" edge). This
consolidation builds the missing instrument and settles the claim.

## The instrument

`omega/emergence/global_novelty.py` — a **scalable Bloom "ever-seen" set** (`GlobalNoveltySketch`,
stdlib only). At each new-class registration the universe asks the sketch whether the class id has
*ever* been seen; only genuinely-first sightings increment `classes_ever_seen_global`. Gated
(`run(global_novelty=True)`), default off ⇒ every experiment byte-identical. Two invariants make it
safe: **repeats are never counted as new** (all eviction-recycling stripped), and genuine novelty is
only ever **under-counted** by ≤ the aggregate false-positive rate (~1%) — so the global rate is
*conservative*: it can only ever lower the measured novelty, never fabricate open-endedness. (A single
fixed Bloom filter would fill and its rising FPR would manufacture a spurious decay; the scalable
design holds the ~1% bias flat across the run.)

## Result (300k ticks, 3 seeds, `memory_horizon=2500`; open = exp030 both corner, closed = exp029)

Novelty rate (new classes/tick) per window, windowed (`classes_ever_seen`, inflated) vs global
(deduplicated, eviction-robust):

| window | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| **open windowed** | .519 | .551 | .534 | .548 | .524 | .533 | .556 | .540 | .537 | .552 |
| **open global** | .365 | .304 | .246 | .192 | .168 | .193 | .174 | .146 | .122 | .123 |
| **closed windowed** | .009 | .003 | .003 | .002 | .003 | .004 | .003 | .003 | .002 | .003 |
| **closed global** | .005 | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |

- Distinct-classes-ever (deduplicated): open **≈ 61,000** per seed (63.6k / 59.7k / 59.7k) with a
  **flat bounded registry ~2,000**; closed **144** (a fixed alphabet). The registry is bounded but the
  *genuine* class count grows into the tens of thousands — real, non-recycled construction.

**Verdict — two findings, both important:**

1. **The claim holds: a genuine positive floor.** With *all* eviction-recycling stripped, the open
   engine still discovers **never-before-seen** classes at **~0.13/tick at 300k ticks** (retention
   0.45–0.50 across 3 seeds), **decisively above the closed control's exact 0.000**. The closed arm is
   the instrument's proof: its small windowed residual (~0.003/tick) is stripped to **0** — that
   "novelty" was 100% recycling. So "stays open" is a **real property of the genuine novelty rate**,
   not a windowing artifact — settled, and well past exp032's ambiguous 120k edge.

2. **But the old "flat rate" was ~4× a measurement artifact.** The *windowed* rate is flat at ~0.53
   across the whole run — exactly the "sustained open-endedness" the previous instrument reported. The
   global rate shows that flatness is **inflated 4.17×** late in the run by eviction recycling. The
   **true** genuine-novelty rate is **positive but declining** — it roughly **halves** over 300k ticks
   (0.28 → 0.13) rather than holding constant.

## Interpretation — the claim, corrected and hardened

Consolidation did exactly its job: it **confirmed the core claim and retired the overclaimed part**.

- **Confirmed:** the world is genuinely open — a positive, seed-robust floor of real novel
  construction that a closed substrate cannot produce (closed → exactly 0). The Ω-0.1 thesis survives
  contact with a conservative, artifact-free instrument.
- **Corrected:** "the novelty rate stays *flat* forever" was substantially a bounded-memory windowing
  artifact (~4× inflation). The honest statement is **"the genuine novelty rate stays *positive* and
  decisively above closure, while slowly declining."** Whether it asymptotes to a strictly-positive
  floor or continues a slow decay toward zero over much longer horizons is the **residual open edge** —
  but it is now a *measured* question about a conservative global rate (0.13/tick and clearly > 0 at
  300k), not the unfalsifiable windowed one.

This also retroactively sharpens exp032/exp034: their "flat novelty rate" trajectories were read off
the windowed metric and are inflated by this factor; their *ranking* claims (open ≫ closed; continuing
construction ≫ capped) are unaffected (they were bounded-to-bounded, common-mode), but the absolute
"constant rate" reading should be understood as an upper bound on the genuine rate.

## Honest scope

One law (exp030 vs exp029), 300k ticks — long past the prior 120k/250k horizons but not 10⁷; the
global rate is a conservative *under*-estimate (true novelty is ≥ what is plotted). The decline is
robust across 3 seeds (retention 0.45–0.50). The verdict "positive floor" is a statement about the
last windows at 300k (0.13/tick ≫ 0), not a proof of a non-zero asymptote — that asymptote is the
named next long-run question, now equipped with the instrument to answer it.

## Consequence

The program's most load-bearing claim is upgraded from "sustained in miniature (windowed)" to
"**genuinely open with a conservative, eviction-robust metric to 300k ticks, multi-seed — positive
floor, honestly-bounded slow decline.**" Every downstream result (the tower, the transition, the
self-improvement arc) now rests on a hardened base. The residual — does the global rate asymptote
above zero at 10⁶–10⁷? — is a clean future run, not a conceptual gap.

## Reproduce
`PYTHONPATH=. python3 studies/exp043_unbounded.py 300000 3 2500` → the table above; committed as
`studies/exp043_unbounded_results.json` / `_console.txt`. Pinned by
`test_global_novelty_sketch_is_conservative_and_eviction_robust` in `omega/tests/test_experiments.py`
(the sketch strips recycling, never over-counts, and `global_novelty=False` is byte-identical).
