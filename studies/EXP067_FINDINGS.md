# exp067 — Transparent cross-tier reification does NOT make competence compound across levels (the ceiling is intrinsic) — but it makes the tower more robust and deeper (Ω-0.56)

The world census (Ω-0.50) settled that per-tier competence saturates to a flat ~1.85 plateau across up to 16
emergent tower levels. The diagnosis (from the arc's own central lesson, exp049→exp053): promotion drops each
collective at an **opaque** atom and carries only a scalar law strength, re-introducing the exp049 opacity at
the tower boundary — so competence can't build on competence. exp067 tests the direct fix: make promotion
**transparent** and ask whether competence then compounds across levels. **It does not — the competence
ceiling is intrinsic to the per-tier substrate.** But the lever has a real, unexpected *secondary* benefit:
it makes the tower **more robust and deeper**.

## Lever (gated `carry_catalysts`, off ⇒ byte-identical)

At each promotion, `carry_catalysts` carries the finishing tier's learned **catalytic repertoire**
(`physics._catalysts` — network-visible `anchor→product` reactions) into the next tier (`seed_catalysts`),
and seeds the child with the parent collectives' representative product states (`seed_states`) so those
reactions' anchors are present and keep firing — the exp053 "keep competent structure network-visible" fix
applied *across* the tier boundary. Three arms on the exp053 compounding physics: **compounding** (fixed law,
opaque), **law_only** (`law_from_competence`, exp055's scalar lift — the census tower), **transparent**
(law_only + `carry_catalysts`; differs from law_only ONLY by the carry).

## Result (5 tiers, 6000 ticks/tier, 5 seeds; per-tier competence on full-depth towers)

| arm | tier0 | tier1 | tier2 | tier3 | tier4 | across-tier slope | collapse | mean depth |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| compounding | 1.830 | 1.753 | 1.764 | 1.755 | 1.831 | +0.0005 | 0.40 | 3.20 |
| law_only | 1.830 | 1.865 | 1.923 | 1.958 | 1.903 | **+0.0240** | 0.40 | 3.20 |
| transparent | 1.822 | **1.947** | 1.918 | 1.914 | 1.878 | **+0.0078** | **0.20** | **4.00** |

**Headline — no cross-level compounding.** Transparent carry-over does **not** raise the across-tier
competence slope: transparent **+0.0078** is *below* law_only's **+0.0240**, and both are far from a genuine
climb — competence still sits on the substrate's intrinsic **~1.9 plateau** at every tier. Transparent gives
a **one-time lift at the first transparent boundary** (tier 1 = 1.947, the highest tier-1 of any arm) and
then flattens (1.918 → 1.914 → 1.878). Carrying the competent structure forward helps the *first* child, but
the benefit does not accumulate — exactly the "transient lift to a plateau" pattern exp055 found, now shown
to survive even when the boundary is made transparent.

**Side-finding — transparent promotion makes the tower more robust and deeper.** Transparent **halves the
collapse rate** (0.20 vs 0.40) and **deepens the tower** (mean depth 4.0 vs 3.2, 4/5 vs 3/5 full-depth).
Carrying the parent's competent structure across the boundary helps the child tier **establish** — it
attacks the exp057/58 *bootstrapping* floor, not the competence ceiling. (Suggestive at n=5 — a one-seed
difference in full-depth count — but consistent with the mechanism: a child seeded with competent structure
is less likely to fail to network.)

## Interpretation — the competence ceiling is intrinsic, not a boundary artifact

The pre-registered hypothesis was that opacity *at the promotion boundary* caps cross-level competence, so
transparency would let it climb. **Falsified.** Making the boundary transparent did not lift the slope, which
means the cap is **not** the boundary — it is the **per-tier substrate's own optimal-richness ceiling**
(exp053/054): each tier, transparent or not, re-attains ~1.9 and no more, because that is the most competence
the single-tier construction law can express. The arc's within-level result — competence is *a rate up to the
substrate's optimal richness, then a stock* — is now shown to hold **at the tower scale, and to be
boundary-independent**: transparent reification cannot make a level exceed what its substrate law allows, it
can only help the level *reach* that ceiling (which is why it aids bootstrapping/depth, not the slope).

This sharpens the census bound into a precise statement: **cross-level competence compounding is limited by
the per-tier construction law, not by what promotion carries across the boundary.** To make competence climb
across levels, the lever must change *what each tier can express* (a rising target that forces each tier to
exceed the last — **H2**, the cross-tier competence ratchet; or a genuinely richer per-tier law — **H3**),
not merely carry the previous tier's structure forward. That is the next rung.

## Is / is not
- **Is:** a clean, honest negative on the headline (transparent carry-over does not raise the across-tier
  competence slope; the ceiling is intrinsic and boundary-independent), plus a real secondary positive
  (lower collapse, greater depth — transparency aids bootstrapping).
- **Is not:** a claim that cross-level competence compounding is *impossible* — only that *transparent
  reification alone* does not achieve it (H2/H3 untested here). 5 seeds; the slope negative is clear, the
  robustness/depth benefit is suggestive at this n. `carry_catalysts=False` ⇒ byte-identical.

## Reproduce
`PYTHONPATH=. python3 studies/exp067_transparent.py 5 6000 5` → the table above; committed as
`studies/exp067_results.json` / `_console.txt`. Pinned by
`test_exp067_transparent_cross_tier_reification_gates_and_acts` (`carry_catalysts=False` ⇒ the tower is
byte-identical tier-for-tier; on, tier 0 is unchanged and tier 1+ differ — the carried competent structure
acts across the boundary).
