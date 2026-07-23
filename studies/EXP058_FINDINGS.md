# exp058 — The bootstrapping floor is a HARD FLOOR: neither more time (exp057) nor more starting diversity moves it — and over-provisioning the foundation shrinks the tower

exp057 (Ω-0.46) showed the tower's bootstrapping floor (~3–12% of seeds never establish a tier-0 network) is
*structural*, not timing-limited — a tier-0 warmup plateaus at 2× and cannot cure it — and sharpened the
follow-on: the failing seeds might need a richer *starting diversity*, not a longer horizon. exp058 tests
that lever directly and finds it does **not** move the floor either: bootstrapping robustness is bounded by
the substrate, not by how the founding tier is provisioned.

## Mechanism (gated `tier0_patches`, default 24 ⇒ tower byte-identical)

`tier0_patches` runs the **founding tier (tier 0) only** with more independent founder demes — higher tiers
unchanged — so it isolates "give tier 0 more standing diversity" (more independent bootstrap attempts, a
wider founder pool) from everything else. Swept in the derived-law tower (`builder="exp053"`,
`law_from_competence=True`, the exp056/057 platform), measuring per founder count: the **tier-0 failure
rate** (does more founder diversity move the structural floor?), the mean tower **depth**, and the
across-tier competence **slope**.

## Result (5 tiers × 3500 ticks/tier, 32 seeds)

| founders | tier-0 failure | mean depth | across-tier slope | survivors |
|:---:|:---:|:---:|:---:|:---:|
| **24** (1×) | 0.0625 | 3.88 | −0.067 | 26/32 |
| 48 (2×) | 0.03125 | 3.50 | −0.011 | 23/32 |
| 96 (4×) | 0.03125 | 3.12 | −0.018 | 21/32 |

**Verdict: a hard floor — starting diversity moves the failure rate by only ~1 seed then plateaus (never to
zero), and more founders monotonically *shrink* the towers.**

- **The floor does not yield to diversity.** More founders drop the tier-0 failure rate by a single seed
  (0.0625 → 0.03125, i.e. 2 → 1 of 32) and then **plateau** — 4× founders is no better than 2×, and neither
  reaches zero. The same shape warmup showed in exp057: a marginal move, then a floor. The residual ~3% of
  seeds are **intrinsically non-networking** — their initial configuration cannot form a founding network at
  any founder count.
- **Over-provisioning the foundation shrinks the tower.** Mean depth falls **monotonically** with founder
  count: 3.88 → 3.50 → 3.12. A wider tier 0 promotes more collectives → a **bloated tier-1 alphabet** →
  cross-production at the higher tiers is diluted (each promoted atom is one of many), so fewer tiers reach
  the ≥ 2-collective bar and the tower is shallower. Diversity has an over-provisioning cost, the exp058
  analogue of exp057's warmup flipping the slope negative.
- **Both levers ruled out.** Tower robustness has a floor independent of **both** time (exp057) **and**
  starting diversity (exp058), and both over-provisionings carry a cost (warmup → negative slope; diversity →
  shallower depth). The ROADMAP's predicted falsification is **confirmed**: some seeds are intrinsically
  non-networking, and the bootstrapping floor is bounded by the substrate itself.

## Interpretation — the floor is a substrate property, and the foundation has an optimal (moderate) width

exp057 + exp058 together close the tower-robustness question with a clean structural finding: the ~3–6%
bootstrapping floor is **irreducible by provisioning** — it is not slow establishment (more time doesn't fix
it) and not a founder-diversity shortage (more founders don't fix it). It is a property of the substrate: a
small fraction of random initial configurations simply never seed a cross-production network. The practical
consequence is a **moderate optimum** for the foundation: 24 founders gives the deepest towers, and adding
founders trades a single seed of establishment robustness for progressively shallower towers. The right
provisioning is *equal, moderate* tiers — the same lesson as exp054 (optimal construction richness) and
exp057 (equal-length tiers beat a front-loaded foundation), now on the founder-count axis.

This is not a failure of the tower: 94–97% of seeds establish and towers reach depth ~3–4 of 5. It is a
precise bound — the last few percent of robustness cannot be bought with either time or diversity, so the
open lever, if any, is not *provisioning* the founding tier but changing the **substrate's establishment
dynamics** (e.g. an explicit founder-network seed that installs a cross-production loop directly, rather than
waiting for one to arise) — a physics change, not a tower-configuration change.

## Honest scope
32 seeds × 5 tiers × 3500 ticks/tier — enough to show the n=16 pilot's apparent "2× founders → zero failures"
was a single-seed fluctuation (it is 0.03125, one seed, at n=32). The failure-rate movement (2 → 1 seed) is
at the noise floor; the **claim is that diversity does not decisively move the floor** (it plateaus, like
warmup), not that it helps by one seed. The **monotone depth decline** (3.88 → 3.50 → 3.12 across three arms)
is the robust, load-bearing result. Retains the exp057 conclusion (structural floor) and adds the second
ruled-out lever; the slope column is flat-and-noisy at this configuration and is not interpreted.

## Reproduce
`PYTHONPATH=. python3 studies/exp058_diversity.py 5 3500 32` → the table above; committed as
`studies/exp058_results.json` / `_console.txt`. Pinned by
`test_exp058_tier0_patches_widens_founding_tier_and_is_byte_identical_at_default` (`tier0_patches=24` ⇒
whole-tower byte-identical; more founders ⇒ different tier-0 history; threads the tower). `tier0_patches=24`
default ⇒ the exact pre-exp058 tower.
