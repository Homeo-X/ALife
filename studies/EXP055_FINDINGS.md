# exp055 — Transition-as-rule-change: deriving each level's law from the level below makes competence rise *across* levels (a modest meta-ratchet) — bought at a cost in tower robustness

exp053 (Ω-0.42) made competence a *rate* **within** a level (the Catalytic Law → network-visible
reactions). exp054 (Ω-0.43) showed expanding the law along construction *depth* fails — the richness must
be a **new kind**. The level tower is exactly that: each tier composes the tier-below's *collectives* as
its atoms (a genuinely new level), sidestepping the depth trap. exp055 runs the compounding law at every
tier and asks the user's #1 question — do **major transitions as rule-changes** make competence rise
**across** levels? The honest answer: **yes, modestly, when the transition DERIVES the higher law from the
lower level's competence — but only on towers that survive, and the compounding law collapses ~a third of
them.**

## Mechanism (gated in `omega/levels/stack.py`; default off ⇒ pre-exp055 tower byte-identical)

`run_stack(builder="exp053")` runs the Catalytic-Law + Red-Queen compounding physics at every tier;
`law_from_competence=True` makes the **transition itself change the law** — the next tier's Catalytic-Law
strength (`catalyst_period = base/(1+competence)`) is **derived from the lower tier's achieved competence**
(a competent level grants its successor a stronger law). Arms: `self-similar` (the current `exp030`
tower), `compounding` (exp053 per tier, fixed law), `derived-law` (exp053 + law-from-competence).

## Result (3 tiers, 6000 ticks/tier, 6 seeds — survivorship-robust metrics)

The naive aggregate (per-tier competence averaged over *all seeds reaching that tier*) shows a spurious
steep "+0.23 across-tier slope" — **survivorship bias**, because the compounding law collapses some towers
entirely and the top-tier average is then taken over only the survivors. The honest metrics: per-tier
competence and within-seed across-tier slope on **full-depth towers only**, plus the **collapse rate**.

| arm | full-depth per-tier competence | within-seed across-tier slope | collapse rate | full-depth |
|-----|:---:|:---:|:---:|:---:|
| self-similar (exp030) | 1.24 · 1.23 · 1.26 | +0.010 | **0%** | 6/6 |
| compounding (exp053, fixed law) | 1.78 · 1.79 · 1.79 | +0.006 (flat) | 33% | 4/6 |
| **derived-law** (law from competence) | **1.78 · 1.89 · 1.94** | **+0.081 (rises)** | 33% | 4/6 |

**Verdict — the rule-change compounds competence across levels (modestly), at a robustness cost.**

- **The compounding law raises per-tier competence at *every* level.** On full-depth towers each tier
  sits at **~1.8** vs the self-similar tower's **~1.25** — the within-level competence-compounding (exp053)
  *transfers up the tower*: a level built on competent collectives is itself highly competent, at every
  tier. A large, robust **level** effect.
- **Deriving the law from competence makes competence RISE across levels.** On surviving towers the
  **derived-law** arm climbs monotonically **1.78 → 1.89 → 1.94** (within-seed slope **+0.081/tier**) —
  ~8× the *fixed*-compounding arm's flat **+0.006** and the self-similar +0.010. So the **transition-as-
  rule-change is the active ingredient**: running the compounding law per tier is not enough (flat);
  *deriving* each level's law from the level below is what tilts the across-level slope. A genuine, if
  modest, **meta-ratchet** — competence compounding *across* levels, the user's #1.
- **But it costs tower robustness.** Both compounding arms **collapse ~a third of towers** (33% fail to
  reach full depth — some produce 0 stable collectives at tier 0 and die), where the self-similar tower
  **never** collapses (0%). Competence selection (the Red Queen especially) collapses the collective
  **diversity** the transition needs to seed the next level.

## Interpretation — a modest meta-ratchet, shadowed by the exp047 tension

exp055 gives the user's #1 idea a **qualified yes**: a **major transition that changes the law**
(deriving the higher level's Catalytic-Law strength from the lower level's achieved competence) makes
competence **rise across levels** (+0.081/tier on surviving towers) where merely *running* the compounding
law per tier is flat (+0.006). Competence is a *rate* across levels, not just within one — the exp053
within-level ratchet, lifted to the tower by making the transition itself competence-dependent. This is
the first across-level competence rise in the program, and it is specifically the *rule-change* (not the
richer law alone) that produces it.

But it is **shadowed by the arc's recurring tension**, now at the tower scale: **the mechanism that makes
competence high collapses the diversity that open-ended recursion needs.** exp047 found this within a
level (within-collective selection collapses the collective); here it is *between* levels — competence
selection yields highly competent but **less diverse** collectives, so fewer distinct signatures seed the
next tier, and ~a third of towers stall or die (0 collapses for the self-similar tower). So the
meta-ratchet is **real but fragile**: competence rises up the towers that survive, but the same competence
pressure that drives the rise thins the diversity the tower needs to keep recursing.

So the two-rung competence-dependent-physics sequence closes with a graded result. **exp053** compounds
competence *within* a level (the clean positive). **exp054** (expand the law along depth) *failed*.
**exp055** (transition-as-rule-change) compounds competence *across* levels **modestly** — a genuine
meta-ratchet driven by the competence-derived rule change — but bounded by a competence-vs-diversity
tension that caps how deep the compounding tower can go. Making competence a rate *and* keeping the tower
open-endedly deep are in tension; the open follow-on is a gentler competence pressure that preserves the
collective diversity recursion needs (at the cost of some of the very competence the rule-change compounds).

## Honest scope
Small-n on the tower (6 seeds, 4 of them full-depth per compounding arm); 3 tiers × 6000 ticks/tier. The
derived-law's across-tier rise (+0.081/tier, 1.78→1.94) is monotonic across 4 surviving seeds and clearly
above the fixed-compounding (+0.006) and self-similar (+0.010) arms, but the survivor-n is modest — the
*direction* is robust (rule-change > fixed law > self-similar), the *magnitude* deserves more seeds. The
collapse-rate cost (33% vs 0%) and the large per-tier level lift (~1.8 vs ~1.25) are firm. The competence-
vs-diversity tension is the key structural finding; a gentler competence pressure (to preserve diversity)
is the natural follow-on, but it trades away some of the competence the rule-change compounds.

## Reproduce
`PYTHONPATH=. python3 studies/exp055_transition.py 3 6000 6` → the survivorship-robust table (full-depth
per-tier competence, within-seed across-tier slope, collapse rate); committed as
`studies/exp055_results.json` / `_console.txt`. Pinned by
`test_exp055_transition_derives_the_next_tier_law_from_achieved_competence` (the transition derives a
stronger successor law from achieved competence; off ⇒ fixed-law tower, byte-identical). Deterministic.
