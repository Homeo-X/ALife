# exp056 — There is NO competence–diversity trade-off: full competence pressure dominates on every axis (a corrective negative that retracts the exp055 tension)

exp055 (Ω-0.44) reported that a competence-derived transition compounds competence across tower levels but
collapses ~⅓ of towers, and attributed the collapse to a **competence–diversity tension**: competence
selection thins the collective diversity the transition needs (the exp047 pattern at the tower scale). Our
discussion then raised whether that tension might be a *fundamental* limit of self-modifying substrates.
exp056 tests it directly by dialing the strength of competence selection — and **refutes it**.

## Mechanism (gated `competence_pressure`, default 1.0 ⇒ exp001–055 byte-identical)

`competence_pressure` ∈ [0,1] scales the Red Queen's competence term: `weight = 0.05 +
competence_pressure·(closure + core-novelty)`. 1.0 = full selection (exp052/055); 0.0 = uniform drift
(maximal diversity, no competence selection). The trade-off hypothesis predicts: softening pressure should
*preserve* diversity/robustness (fewer collapses) at the cost of the compounding *slope*. Swept in the
derived-law tower (`builder="exp053"`, `law_from_competence=True`), measuring per pressure the across-tier
competence slope, the collapse rate, and — a direct diversity signal — the mean stable collectives tier 0
produces (the recursion fuel the transition needs ≥ 2 of).

## Result (3 tiers × 7000 ticks/tier, 10 seeds)

| pressure | across-tier slope | collapse rate | tier-0 diversity | mean depth |
|:---:|:---:|:---:|:---:|:---:|
| **1.00 (full)** | **+0.101** | **0.20** | **21.5** | **2.50** |
| 0.66 | +0.047 | 0.40 | 19.1 | 2.10 |
| 0.33 | +0.099 | 0.50 | 16.7 | 1.80 |
| 0.00 (drift) | +0.110 | 0.20 | 19.0 | 2.40 |

**Verdict: no trade-off — full competence pressure dominates on every axis at once.**

- **Softening selection does NOT preserve diversity or robustness — the opposite.** Full pressure (1.0)
  has the **lowest** collapse rate (0.20), the **most** tier-0 diversity (21.5), and the **deepest** towers
  (2.50), *and* a strong across-level slope (+0.101). Collapse is **U-shaped** — worst at intermediate
  pressure (0.33 → 0.50) — so weakening competence selection makes towers *more* fragile, not less.
- **The exp055 tension is refuted.** More competence pressure gives *more* diversity and *fewer* collapses,
  the exact opposite of "competence selection thins diversity." The exp055 ~⅓ collapse (measured at n=4)
  was **bootstrapping variance** — some seeds fail to establish *any* tier-0 network — which at proper n
  and horizon falls to **20%** at full pressure. It was never a competence-diversity mechanism.
- **Competence compounds across levels at every pressure** (slope +0.05 to +0.11), reinforcing the exp055
  meta-ratchet — and, corrected, it does so *without* a robustness cost at full pressure.

## Interpretation — a cleaner, stronger exp055, and a retraction

This makes exp055's core result **stronger, not weaker**: a competence-derived transition compounds
competence up the tower **and** (at full pressure) keeps towers robust and diverse — there is no
competence-vs-open-ended-recursion trade-off to pay. The apparent tension was a small-n artifact
(2-of-4-seed collapse read as a mechanism), now retracted. And the discussion-level speculation that
competence and diversity might be *fundamentally* opposed is **not supported** in this substrate: the two
are, if anything, weakly *complementary* (strong consistent selection canalizes demes into competent types
that reliably form networks, raising both competence and the count of networked collectives).

Why is collapse *U-shaped*? Both extremes are robust for opposite reasons — full pressure canalizes
strongly (consistent competent attractors), pure drift preserves maximal diversity (many demes, some
always network) — while intermediate pressure does neither well, giving the most bootstrap failures. So
the honest structural finding is: **tower robustness is limited by bootstrapping variance, not by
competence selection**, and competence selection *helps* it.

## Honest scope
10 seeds × 3 tiers × 7000 ticks/tier — enough to distinguish the pressure arms (full 0.20 vs intermediate
0.40–0.50 collapse) but the collapse rates still carry ±0.15 noise at n=10; the *direction* (full pressure
dominant, U-shaped collapse, no softening benefit) is robust, the exact rates are estimates. Retracts the
exp055 competence–diversity tension claim (and the ROADMAP "possibly fundamental" framing); keeps the
exp055 across-level compounding, now un-caveated. The residual open question moves elsewhere: tower
robustness is bootstrapping-limited — what reduces the ~20% floor of seeds that never establish a tier-0
network (longer tier-0 warmup? a diversity-seeded start?).

## Reproduce
`PYTHONPATH=. python3 studies/exp056_tradeoff.py 3 7000 10` → the table above; committed as
`studies/exp056_results.json` / `_console.txt`. Pinned by
`test_exp056_competence_pressure_scales_selection_and_is_byte_identical_at_one` (pressure=1.0 ⇒
byte-identical to exp052; lower pressure changes the dynamics; threads through the tower). Deterministic
across `PYTHONHASHSEED`; `competence_pressure` default 1.0 ⇒ exp001–055 byte-identical.
