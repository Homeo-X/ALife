# exp057 — The tower's bootstrapping floor is STRUCTURAL, not timing-limited — and warmup actively harms the meta-ratchet (a double negative that answers exp056's open question)

exp056 (Ω-0.45) refuted the competence–diversity trade-off and relocated the limit on tower robustness to
**tier-0 establishment**: ~20% of seeds never form a founding network, so the tower dies at depth 0
("bootstrapping variance"). It left the mechanism open — is that floor *timing*-limited (a slow-to-establish
tier 0 that more warmup would cure) or *structural* (seeds that simply cannot network)? exp057 tests it
directly and answers **structural**, with a bonus negative: more tier-0 time actively *lowers* the
across-level compounding.

## Mechanism (gated `tier0_warmup`, default 1.0 ⇒ tower byte-identical)

`tier0_warmup` runs the **founding tier (tier 0) only** for `int(ticks · tier0_warmup)` ticks — higher
tiers unchanged — so it isolates "give tier 0 more time to establish" from everything else. Swept in the
derived-law tower (`builder="exp053"`, `law_from_competence=True`, the exp056 platform), measuring per
warmup: the **tier-0 failure rate** (fraction of seeds that die at depth 0 — the bootstrapping floor), the
**mean tower depth** (does curing bootstrapping unlock deeper towers?), and the **across-tier competence
slope** on survivors (does warmup preserve the exp055 meta-ratchet?).

## Result (5 tiers × 3500 ticks/tier, 16 seeds)

| warmup | tier-0 failure | mean depth | across-tier slope | survivors |
|:---:|:---:|:---:|:---:|:---:|
| **1×** | 0.125 | 3.69 | **−0.039** | 12/16 |
| 2× | 0.0625 | 3.88 | **−0.102** | 13/16 |
| 4× | 0.0625 | 3.75 | **−0.162** | 13/16 |

**Verdict: the bootstrapping floor is structural (warmup does not cure it), and warmup monotonically
degrades the meta-ratchet.**

- **The floor is STRUCTURAL, not timing-limited.** More tier-0 warmup drops the failure rate by only ~1
  seed (0.125 → 0.0625) and **plateaus immediately at 2×** — even 4× (14,000 tier-0 ticks) buys nothing
  more. The remaining failing seeds cannot establish a founding network *at any horizon*; the establishment
  failure is in the seed's initial configuration, not in how long it runs. Mean depth is **flat** (~3.7–3.9)
  across warmup — curing (the little that's curable of) bootstrapping does **not** unlock deeper towers.
- **Warmup actively HARMS the across-level compounding.** The competence slope goes **monotonically more
  negative** with warmup: −0.039 → −0.102 → −0.162. Over-warming tier 0 pushes it to its **optimal-richness
  competence ceiling** (the exp053/054 saturation), so the promoted alphabet is already maximally competent
  and the higher tiers have no headroom to compound above it — competence *declines* up the tower. More
  founding time is not free; it spends the ceiling early.

## Interpretation — the wrong lever, cleanly ruled out

exp057 closes the exp056 follow-on with two honest negatives. (i) Tower robustness will **not** yield to
*more time* — the ~6–12% of seeds that fail to bootstrap a tier-0 network are structurally, not temporally,
starved; the lever must change the *starting diversity/structure* (a diversity-seeded start, more founding
patches, or an explicitly seeded founder network), not the horizon. (ii) The naive intuition "give the
foundation longer to set" is worse than neutral for the *tower*: because competence saturates at the
substrate's optimal richness (exp054), a longer-warmed tier 0 arrives at the ceiling and leaves the
meta-ratchet nothing to climb — so warmup trades a negligible robustness gain for a real compounding loss.
The exp055/056 meta-ratchet is best served by tiers of **equal, moderate** length, not a front-loaded
foundation.

Note on the slope baseline: at this 5-tier / 3500-ticks-per-tier configuration even the 1× arm sits near
zero (−0.039), lower than exp056's +0.101 at 3 tiers / 7000 ticks — deeper, shorter-per-tier towers push
more tiers past the tier-where-competence-peaks, so the *absolute* slope is configuration-dependent. The
robust, within-experiment finding is the **direction**: warmup drives the slope monotonically downward, and
the failure floor is flat.

## Honest scope
16 seeds × 5 tiers × 3500 ticks/tier. The failure-rate movement (0.125 → 0.0625) is a single seed and is at
the noise floor — the *claim* is that warmup does **not** decisively reduce the floor (it plateaus at 2×),
i.e. the floor is not timing-limited, **not** that warmup helps by exactly one seed. The slope degradation
(−0.039 → −0.102 → −0.162) is monotone across three arms and is the load-bearing result. Both point the same
way: warmup is the wrong lever. The open question sharpens: reducing the structural bootstrapping floor needs
a **starting-diversity** intervention (seed tier 0 with a richer/founder-networked start), tested next.

## Reproduce
`PYTHONPATH=. python3 studies/exp057_bootstrap.py 5 3500 16` → the table above; committed as
`studies/exp057_results.json` / `_console.txt`. Pinned by
`test_exp057_tier0_warmup_extends_founding_tier_and_is_byte_identical_at_one` (`tier0_warmup=1.0` ⇒
whole-tower byte-identical; larger warmup ⇒ different tier-0 history; threads the tower). `tier0_warmup`
default 1.0 ⇒ the exact pre-exp057 tower.
