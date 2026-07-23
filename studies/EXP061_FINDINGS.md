# exp061 — The world census: the living world SUSTAINS open-ended novelty and self-maintaining life at 250k ticks, and grows a deep tower — but competence saturates to a stable plateau across levels (Ω-0.50)

Phase A (Ω-0.48) gave the living world the arc's competence and life signals; Phase B (Ω-0.49) grew a tower
of levels live and eviction-invariantly, making an indefinite run feasible. exp061 is the **census**: the
rich, long-horizon dataset that settles what happens *at scale* — does the living world stay alive, open,
and competent over a long horizon, and how deep does the live tower actually climb?

## Method — `studies/exp061_census.py` (bounded memory throughout)

Two parallel campaigns, emitting a machine-readable census (`exp061_census.json`) and a self-contained,
shareable HTML report (`exp061_census.html`, inline SVG):
- **Part A — living_world vital-signs time series** over **250,000 ticks × 4 seeds**, sampled every 12,500
  ticks: competence, autocatalytic closure, self-maintaining lifeform count, and the *genuine*
  (eviction-robust) novelty rate (Ω-0.39 sketch).
- **Part B — the deep tower profile**: a live `TowerWorld` pushing **16 tiers** × 4 seeds — max depth
  reached and the per-tier competence profile.

## Result

**Part A — the living world stays alive, open, and competent at 250k ticks.**

| signal | start | end (250k) | over the horizon |
|:---|:---:|:---:|:---|
| competence | 1.878 | **1.923** | stable **1.88–2.01** plateau, slope ~0 (+7e-9/tick) |
| genuine novelty rate | — | **0.244/tick** | holds **0.227–0.244/tick** throughout; **62,515** distinct classes ever |
| autocatalytic closure | 0.573 | **0.604** | stable/rising — self-maintenance holds |
| self-maintaining lifeforms | 21 | **24** | persist and grow |
| diversity | — | 2.41 | stable |

The living world **does not decay**: competence holds a high plateau (~1.9), the genuine eviction-robust
novelty rate holds a **positive floor** (~0.24/tick — it keeps discovering genuinely-new organization, not
recycling), and self-maintaining, autocatalytically-closed lifeforms persist. The Ω-0.39 "stays open
forever" floor now holds for the *full arc-on living world*, not just the plain engine, and *alongside* a
sustained high competence and a standing population of self-maintaining life.

**Part B — tower depth is not intrinsically ceilinged, but competence saturates across levels.**

- Per-seed depths were **[16, 0, 9, 1]** (mean **6.5**, max **16/16**). One seed climbed **all sixteen
  tiers attempted** — so there is **no intrinsic depth ceiling** in the tested range (the ROADMAP's
  "tower depth hits an intrinsic ceiling" falsification is *not* triggered). Depth is highly **variable**,
  because reaching deep requires many *consecutive* successful promotions and each tier carries the
  exp057/58 bootstrapping-type failure probability (one seed failed at tier 0; compounding those risks
  spreads the depths widely).
- Per-tier competence is a **flat ~1.85 plateau** across all reached levels (slope **−0.0002**): competence
  is lifted to a high level in the first tiers and **holds there** across deeper ones. The across-level
  meta-ratchet (exp055 +0.081/tier, exp060 +0.039/tier over ≤ 5 tiers) is a **transient lift to a stable
  plateau**, not an unbounded climb — the tower-scale analogue of the within-tier saturation at optimal
  richness (exp053/054).

## Interpretation — a genuine world that sustains OEE and life, honestly bounded

The census is the program's most complete single picture of the built world, and it is a **qualified
positive**: the living world genuinely **sustains open-ended novelty and self-maintaining life at scale and
at flat memory** — the two hard requirements together (Ω-0.48/0.49) now shown to *persist* to 250k ticks —
and it **grows a deep tower of levels** with no intrinsic depth ceiling in range. The honest bound is on
*competence*, not on novelty, life, or depth: competence saturates to a stable high plateau (~1.85–1.9) both
within a tier and across tower levels. This is consistent with the entire arc — competence is a *rate up to
the substrate's optimal richness, then a stock* (exp053/054), and that holds at the tower scale too. So the
world is open-ended in **construction and individuality** indefinitely, and competent to a high stable
level, but not *unboundedly* self-improving — a precise, falsifiable statement of what this substrate does.

## Honest scope
4 seeds. Part A is a single 250k-tick horizon (the genuine floor held to 3M in the *plain* engine, Ω-0.40;
this shows the *arc-on living world* holds to 250k — a 10⁶–10⁷ living-world stress remains open). Part B's
depth distribution (16/0/9/1) is wide at n=4 — the *direction* (no depth ceiling in range; competence flat
across levels) is clear, the mean depth (6.5) is a rough estimate. The competence-plateau-across-levels
finding is robust (flat over up to 16 tiers). Bounded memory throughout; genuine novelty via the Ω-0.39
sketch.

## Reproduce
`PYTHONPATH=. python3 studies/exp061_census.py 250000 12500 4 16 2500` → `studies/exp061_census.json`
(the full time series + tower profile) and `studies/exp061_census.html` (the shareable report). Bounded
memory is what makes the run feasible (the tower is eviction-invariant, Ω-0.49).
