# Project Ω — Research Log

A running scientific narrative. Newest milestone at the top. This is a lab
notebook, not marketing: it records what was tried, what the evidence said, and
what was falsified.

---

## Milestone Ω-0.49 — The live recursive tower: levels emerge over wall-clock time and compound competence, and it is EVICTION-INVARIANT (exp060)

**Date:** 2026-07-23 · **Status:** complete · **Verdict:** a **positive** — the exp055 across-level
meta-ratchet runs live in a persistent, memory-bounded world, and the tower is *exactly* invariant to memory
eviction. Phase B of the living-world program. Detail: `studies/EXP060_FINDINGS.md`. Gated; the plain
single-tier `World` is unchanged.

exp059 (Ω-0.48) gave the living world a high competence *plateau* within one tier and named the fix: genuine
across-time compounding needs a *new level*. exp060 adds **`TowerWorld`** (`omega/world/tower.py`) — the
recursive tower (`run_stack`'s promotion logic) run **live** in the chunk-advanced `World` runtime, bounded
memory, checkpointable — so tiers emerge over wall-clock time (a `python -m omega.world tower` watch mode
shows chemistry→biology→culture→… born in real time, with `law_from_competence` deriving each level's law
from the one below).

**Result (5 tiers × 3000 ticks/tier, 6 seeds, three memory regimes).** The live tower grows to mean depth
**3.5/5** with competence rising **+0.039/tier** across the *emergent* levels — the meta-ratchet is not a
batch artifact. And it is **eviction-invariant**: a `live-tight` arm with the memory horizon set *below* each
tier's tick-life (so cold classes are genuinely evicted within every tier) is **byte-identical** to the
un-evicted batch ceiling on every metric (depth, slope, competence, failure rate). The tower reads the *live*
cross-production network and per-generation edge tallies, not the evicted class registry — so bounding memory
(what makes an indefinite world feasible, Ω-0.21) costs the tower nothing. The residual 1/6 tier-0 failure is
the exp057/58 bootstrapping floor, not a tower defect.

**Interpretation.** The two properties a genuine open-ended world needs together are now shown together: it
keeps building higher levels of organization (competence compounding across emergent tiers) *and* it can run
forever (flat memory, eviction-invariant). The live tower is the concrete "watch higher-order life appear"
artifact.

### Is / is not
- **Is:** the exp055 across-level meta-ratchet made live and watchable, at flat memory with zero dynamical
  cost from eviction — a structural invariance (the tower reads live state), so the exact-equality is robust.
- **Is not:** a settlement of *how deep* the tower goes (5 tiers → ~3.5; deeper towers + the 10⁶–10⁷ horizon
  are the Phase C census, which the eviction-invariance proven here makes feasible), and the +0.039/tier slope
  is modest (per-tier maturation time trades against tier count).

---

## Milestone Ω-0.48 — The self-improvement arc TRANSFERS to the living world: a persistent `living_world` is far more competent and self-maintaining than the exp030-era world (exp059)

**Date:** 2026-07-23 · **Status:** complete · **Verdict:** a **positive** (with two honest caveats) — the
Catalytic Law × Red Queen survives the persistent, spatial, reifying, eviction-bounded world regime; a
`living_world` reaches ~1.6× the competence and ~2× the life signals of the exp030-era world. This begins
Phase A of the *living-world* program (fold the arc into the watchable world; instrument its vital signs).
Detail: `studies/EXP059_FINDINGS.md`. Gated; the old `world` builder + `WorldVitals` + `genuine_novelty`
default off ⇒ exp001–058 byte-identical.

The watchable world (`omega/world/`) was frozen at the exp030 era (`deme_fitness="network"`, no Catalytic
Law / Red Queen / competence pressure, tower only in batch). exp059 adds a gated **`living_world`** builder
(the `world` foundation + `catalytic_law` + `deme_fitness="redqueen"` + `competence_pressure=1.0` + the
exp040 heredity channel) and a read-only **`WorldVitals`** reader (competence trajectory, autocatalytic
closure = the life signal, self-maintaining lifeform count, breed-true heredity, and the eviction-robust
*genuine* novelty rate — the Ω-0.39 sketch attached dynamics-invariantly). Both are surfaced on the terminal
+ browser dashboard ("vital signs" panel) and a `--physics living_world` CLI flag.

**Result (persistent bounded-memory worlds, 30k ticks, 4 seeds).** `living_world` vs the exp030 world:
competence **1.92 vs 1.20** (+0.72), closure **0.60 vs 0.27** (~2.2×), self-maintaining collectives **23.5
vs 9.8** (~2.4×), breed-true heredity **0.37 vs 0.03** (~12×); both stay genuinely open (positive
eviction-robust novelty). The arc is not a batch-only artifact — it transfers to the world.

**Two honest caveats.** (i) Competence reaches an elevated **plateau**, slope ≈ 0 within the single
persistent tier — the exp053/054 saturation-at-optimal-richness, so genuine *across-time* compounding needs
a **new level** (the live tower, Ω-0.49). (ii) The living world is **deeper, not wider**: *lower* raw
diversity (2.28 vs 4.46) and *lower* genuine-novelty rate (0.27 vs 0.60) — the exp056 canalization effect at
world scale (strong competence selection focuses the world on competent, self-maintaining, breed-true
structure rather than many novel-but-incompetent classes). A trade in *what kind* of open-endedness, not a
loss of it.

### Is / is not
- **Is:** the first proof the arc's competence/life machinery works in the *persistent watchable world*, with
  large effect sizes and legible vital signs (you can now *watch* competence and self-maintenance, not just a
  novelty pulse).
- **Is not:** a within-tier compounding *slope* (it plateaus — that's the tower's job), nor a claim the
  living world is more open-ended in raw novelty (it is deeper-not-wider). n=4 × 30k ticks — directions
  robust, exact numbers estimates.

---

## Milestone Ω-0.47 — The bootstrapping floor is a HARD FLOOR: starting diversity doesn't move it either, and over-provisioning the foundation shrinks the tower (exp058)

**Date:** 2026-07-23 · **Status:** complete · **Verdict:** a **confirming negative** — the exp046-predicted
falsification holds: tower robustness has a floor independent of *both* time (exp057) *and* starting
diversity (exp058). Detail: `studies/EXP058_FINDINGS.md`. Gated; `tier0_patches=24` (default) ⇒ the tower is
byte-identical.

exp057 (Ω-0.46) showed the bootstrapping floor is structural (warmup can't cure it) and pointed to a
starting-*diversity* lever. exp058 adds a gated `tier0_patches` that runs the founding tier (tier 0) with
more independent founder demes — higher tiers unchanged — and sweeps it in the derived-law tower
(`builder="exp053"`, `law_from_competence`).

**Result (5 tiers × 3500 ticks/tier, 32 seeds).** More founders move the tier-0 failure rate by only ~1 seed
(0.0625 → 0.03125, i.e. 2 → 1 of 32) and then **plateau** — 4× founders is no better than 2×, and neither
reaches zero — the same shape warmup showed. And more founders **monotonically shrink** the towers (mean
depth 3.88 → 3.50 → 3.12): a wider tier 0 promotes more collectives → a bloated tier-1 alphabet → diluted
higher-tier cross-production → shallower towers. So diversity has the same over-provisioning cost warmup had
(exp057 flipped the slope negative; exp058 lowers depth). The n=16 pilot's apparent "2× founders → zero
failures" was a single-seed fluctuation (0.03125 at n=32).

**Interpretation.** exp057 + exp058 close the tower-robustness question: the ~3–6% bootstrapping floor is
**irreducible by provisioning** — not slow establishment (time doesn't fix it), not a founder shortage
(diversity doesn't fix it) — it is a substrate property: a small fraction of random initial configurations
never seed a cross-production network. The foundation has a **moderate optimum** (24 founders → deepest
towers; adding founders trades one seed of robustness for shallower towers) — the exp054 optimal-richness /
exp057 equal-length-tiers lesson on the founder axis. Not a tower failure (94–97% establish, depth ~3–4 of
5); a precise bound. The only remaining lever is not *provisioning* the founding tier but changing the
substrate's **establishment dynamics** (e.g. an explicit founder-network seed) — a physics change.

### Is / is not
- **Is:** a clean confirming negative — the second ruled-out lever for the bootstrapping floor, with a robust
  monotone depth-decline showing over-provisioning hurts, and the n=16 "cure" shown to be a single-seed fluke.
- **Is not:** a claim that diversity helps by one seed (that move is at the noise floor) — the claim is that
  it does **not** decisively move the floor. The slope column is flat-and-noisy at this config and is not
  interpreted.

---

## Milestone Ω-0.46 — The tower's bootstrapping floor is STRUCTURAL, not timing-limited — and tier-0 warmup actively harms the meta-ratchet (exp057)

**Date:** 2026-07-22 · **Status:** complete · **Verdict:** a **double negative** — the exp056 bootstrapping
floor is not curable with more founding time (it is structural), and front-loading tier-0 *lowers* the
across-level compounding. Detail: `studies/EXP057_FINDINGS.md`. Gated; `tier0_warmup=1.0` (default) ⇒ the
tower is byte-identical.

exp056 (Ω-0.45) relocated the limit on tower robustness to tier-0 establishment (~20% of seeds never form a
founding network → the tower dies at depth 0) and left open *why*: timing or structure? exp057 adds a gated
`tier0_warmup` that runs the founding tier (tier 0) alone for `int(ticks · tier0_warmup)` ticks — higher
tiers unchanged — and sweeps it in the derived-law tower (`builder="exp053"`, `law_from_competence`).

**Result (5 tiers × 3500 ticks/tier, 16 seeds).** The floor is **structural**: warmup drops the tier-0
failure rate by ~1 seed (0.125 → 0.0625) and **plateaus at 2×** — 4× (14,000 tier-0 ticks) buys nothing more
— and mean depth stays **flat** (~3.7–3.9), so curing bootstrapping does *not* unlock deeper towers. The
failing seeds cannot network at any horizon. And warmup **actively harms** the exp055 meta-ratchet: the
across-tier competence slope goes **monotonically more negative** (−0.039 → −0.102 → −0.162) because
over-warming tier 0 drives it to the exp053/054 optimal-richness ceiling, leaving the higher tiers no
headroom to compound above the promoted alphabet.

**Interpretation.** Two honest negatives cleanly rule out a lever. Tower robustness will not yield to *more
time* — the structurally-starved seeds need a **starting-diversity** intervention (a diversity-seeded /
founder-networked tier-0 start), not a longer horizon. And "give the foundation longer to set" is worse than
neutral for the tower: because competence saturates at optimal richness, a front-loaded tier 0 spends the
ceiling early and the meta-ratchet has nothing to climb. The exp055/056 compounding is best served by tiers
of **equal, moderate** length.

### Is / is not
- **Is:** a clean double negative that answers the exp056 open question — the bootstrapping floor is
  structural (warmup plateaus at 2×), and warmup monotonically degrades the across-tier slope (three arms).
- **Is not:** a measurement of *how much* warmup helps robustness (the 0.125 → 0.0625 move is a single seed,
  at the noise floor) — the claim is that it does **not** decisively help, not that it helps by one seed. The
  1× slope baseline (−0.039) is configuration-dependent (5 short tiers vs exp056's 3 long ones); the robust
  finding is the *direction* under warmup, not the absolute level.

---

## Milestone Ω-0.45 — There is NO competence–diversity trade-off: full competence pressure dominates on every axis — the exp055 tension is retracted (exp056)

**Date:** 2026-07-19 · **Status:** complete · **Verdict:** a **corrective negative** — the Ω-0.44
competence–diversity tension was a small-n artifact; dialing competence-selection strength shows full
pressure is best on *every* axis at once. Detail: `studies/EXP056_FINDINGS.md`. Gated;
`competence_pressure=1.0` (default) ⇒ exp001–055 byte-identical (deterministic across `PYTHONHASHSEED`).

exp055 attributed its ~⅓ tower collapse to competence selection thinning the collective diversity the
transition needs (an exp047-scale tension), and the discussion raised whether it might be *fundamental*.
exp056 dials the strength of competence selection — `competence_pressure ∈ [0,1]` scales the Red Queen's
competence term (`weight = 0.05 + pressure·(closure + core-novelty)`) — and sweeps it in the derived-law
tower, measuring across-tier competence slope, collapse rate, and a direct diversity signal (mean stable
collectives tier 0 produces, the recursion fuel).

**Result (3 tiers × 7000 ticks/tier, 10 seeds):** the trade-off hypothesis is **refuted**. Full pressure
(1.0) has the **lowest** collapse (0.20), the **most** tier-0 diversity (21.5), the **deepest** towers
(2.50), *and* a strong across-level slope (+0.101). Softening selection makes towers **more** fragile
(collapse is **U-shaped** — worst at intermediate 0.33 → 0.50), and competence compounds across levels at
*every* pressure (+0.05 to +0.11). So more competence pressure gives *more* diversity and *fewer* collapses
— the opposite of "competence selection thins diversity." The exp055 ~⅓ collapse (measured at n=4) was
**bootstrapping variance** (seeds failing to establish any tier-0 network), not a competence-diversity
mechanism; at proper n/horizon it is 20% at full pressure.

**Interpretation.** This makes exp055's meta-ratchet **stronger, not weaker**: a competence-derived
transition compounds competence up the tower **and** (at full pressure) keeps towers robust and diverse —
no competence-vs-open-ended-recursion trade-off is paid. The apparent tension was small-n (2-of-4 collapse
read as a mechanism), now **retracted**, along with the discussion speculation that competence and
diversity are *fundamentally* opposed — they are, if anything, weakly *complementary* (strong consistent
selection canalizes demes into competent types that reliably network). The residual limit on tower
robustness is **bootstrapping variance** (the ~20% of seeds that never establish a tier-0 network), not
competence selection.

### Is / is not
- **Is:** a clean corrective negative (retraction kept on purpose) — full competence pressure dominant on
  slope, collapse, diversity, and depth; U-shaped collapse; competence-compounding at every pressure.
- **Is not:** a proof of *no* limit — tower robustness is bootstrapping-limited (~20% floor at n=10, ±0.15
  noise); the exact collapse rates are estimates. Retracts the Ω-0.44 tension; keeps its across-level
  compounding, now un-caveated.

---

## Milestone Ω-0.44 — Transition-as-rule-change: deriving each level's law from the level below makes competence rise *across* levels (a modest meta-ratchet) — ~~shadowed by a competence-vs-diversity tension~~ (exp055)

> **Retraction (Ω-0.45, exp056):** the "competence-vs-diversity tension" below was a small-n artifact. A
> 10-seed pressure sweep shows **no trade-off** — full competence pressure gives the *lowest* collapse, the
> *most* diversity, and the *deepest* towers while still compounding competence across levels. The ~⅓
> collapse was bootstrapping variance, not competence selection thinning diversity. Read the across-level
> compounding result below as un-caveated; disregard the tension framing.


**Date:** 2026-07-19 · **Status:** complete · **Verdict:** a **qualified positive** — the user's #1 idea
(major transitions as rule-changes) makes competence compound *across* levels, modestly, on towers that
survive; bounded by the arc's competence-vs-diversity tension. Detail: `studies/EXP055_FINDINGS.md`. Gated;
`law_from_competence` off + `builder='exp030'` ⇒ pre-exp055 tower byte-identical.

exp053 made competence a rate *within* a level; exp054 showed expanding the law along construction *depth*
fails (the richness must be a new *kind*). The level tower is that new kind — each tier composes the
tier-below's *collectives* as atoms. exp055 runs the compounding law (exp053: Catalytic Law + Red Queen)
at every tier, and `law_from_competence` makes the **transition change the law**: the next tier's
Catalytic-Law strength (`catalyst_period = base/(1+competence)`) is **derived from the lower tier's
achieved competence**. Arms: `self-similar` (exp030 tower), `compounding` (exp053 per tier, fixed law),
`derived-law` (exp053 + law-from-competence).

**Result (3 tiers × 6000 ticks/tier, 6 seeds; survivorship-robust metrics — the naive per-tier average is
a spurious +0.23 slope because collapsed towers bias the top-tier mean).** Three findings: (1) **per-tier
level lift** — the compounding law puts every tier at competence **~1.8** vs the self-similar tower's
**~1.25** (within-level compounding transfers up the tower); (2) **the rule-change compounds across
levels** — on full-depth towers the **derived-law** arm rises monotonically **1.78 → 1.89 → 1.94**
(within-seed slope **+0.081/tier**), ~8× the *fixed*-compounding arm's flat **+0.006** and self-similar's
+0.010, so *deriving* each level's law from the level below is the active ingredient (running the
compounding law per tier is not enough); (3) **a robustness cost** — both compounding arms **collapse ~⅓
of towers** (33% fail full depth; some produce 0 stable collectives at tier 0 and die) where the
self-similar tower **never** collapses.

**Interpretation.** The user's #1 gets a qualified yes: a transition that changes the law
competence-dependently makes competence a *rate across levels*, the first such result — but it is
**shadowed by the exp047 tension at the tower scale**: competence selection yields highly competent but
*less diverse* collectives, so fewer distinct signatures seed the next tier and the tower stalls or dies.
The meta-ratchet is real but fragile — competence rises up the towers that survive, while the same
pressure that drives the rise thins the diversity the tower needs to keep recursing. The two-rung
competence-dependent-physics sequence closes graded: exp053 compounds competence *within* a level (clean
positive); exp054 (depth expansion) failed; exp055 (rule-change) compounds it *across* levels modestly,
bounded by competence-vs-diversity.

### Is / is not
- **Is:** the first *across-level* competence rise (derived-law +0.081/tier, monotonic on 4 surviving
  seeds, ≫ fixed-law +0.006), showing the competence-derived *rule-change* — not the richer law alone — is
  the active ingredient; plus a large per-tier level lift (~1.8 vs ~1.25).
- **Is not:** an unbounded or robust meta-ratchet — 33% of compounding towers collapse (vs 0%
  self-similar), the survivor-n is modest (4/6), and the magnitude deserves more seeds. Competence and
  open-ended tower depth are in tension; a gentler competence pressure that preserves diversity is the
  open follow-on.

---

## Milestone Ω-0.43 — The Earned Law: expanding *construction depth* does not break exp053's saturation — the real limit is optimal richness, not a fixed law (exp054)

**Date:** 2026-07-19 · **Status:** complete · **Verdict:** an **honest negative that locates why competence
saturates** — the constructible space has an optimal richness with finite competent structure; expanding
the law along the *depth* axis degrades competence. Detail: `studies/EXP054_FINDINGS.md`. Gated;
exp001–053 byte-identical (deterministic across `PYTHONHASHSEED`).

exp053 compounds competence but **saturates** (~1.45 by ~8k ticks). Diagnostic: it is **not** the catalyst
cap (cap 16/80/400 byte-identical; only ~10 distinct closure-core edges ever qualify) — at fixed resolution
the constructible space is finite, so competent structure exhausts. `type_resolution` is the binding lever
(res → path length); res5 beats res3 cold, but res8 (isolated) collapses and raising resolution mid-life
orphans the network. exp054's `earned_law` therefore climbs resolution **gradually, at birth, per lineage**
(non-destructive, closure-gated), to test whether earning reaches deep regimes a cold start can't.

**Result (20k ticks, 6 seeds):** the Earned Law **fails**. Earned competence (mean **0.577**, late slope
−0.003, survival 0.46) is the **lowest of all arms** — below fixed-law res3 (0.800), fixed-high cold-res8
(0.742), and far below catalytic/exp053 (**1.224**). Climbing resolution **hurts**: deeper type-paths make
cross-production sparser, so closure (hence competence) falls, and the greedy climb overshoots the optimum
(reach ~3.67 ≈ res ~6.7 within the first window) into a worse regime. The single-seed smoke (reach 5, +0.009
slope) was seed-noise. Cold res8 did *not* collapse on the Red Queen base (0.60), correcting the isolated
diagnostic — deeper resolution is merely worse, not catastrophic. **exp053's reaction expansion (fixed
richness) remains the best.**

**Interpretation.** Competence does not saturate because the law is *fixed* — it saturates because the
constructible space has an **optimal richness** and the competent (closure-forming) structure at that
richness is **finite**. Expanding the law along *depth* moves *out* of the optimum into sparser regimes
where cross-production is rarer, so competence drops. The right expansion adds competent-structure capacity
*at* the optimal richness (exp053's reactions), not *depth* — a bias–variance-like ceiling (too shallow
exhausts; too deep starves cross-production). Competence is a rate up to the optimal-richness ceiling, then
a stock, and depth-expansion does not break it.

### Is / is not
- **Is:** a clean negative that locates exp053's saturation in the substrate's *optimal richness* (finite
  competent structure), shows the construction-*depth* axis degrades competence, and re-confirms
  fixed-richness reaction expansion (exp053) as the better mechanism.
- **Is not:** a proof that *no* expanding law helps — it rules out the depth axis. Warns rung 2 (exp055,
  transition-as-rule-change) that a naive "richer/deeper law" hurts; the tower transition is a *different*
  rule-change (composing lower-tier collectives, a new level) and must keep cross-production viable, not
  just bigger. Both-corner typed_path; 6 seeds × 20k.

---

## Milestone Ω-0.42 — The Catalytic Law breaks the competence-flat wall: competence COMPOUNDS, and it is a genuine ratchet (exp053)

**Date:** 2026-07-19 · **Status:** complete · **Verdict:** the self-improvement arc's **first
compounding-competence result** — competence becomes a *rate*, properly controlled. Detail:
`studies/EXP053_FINDINGS.md`. Gated; exp001–052 byte-identical (deterministic across `PYTHONHASHSEED`).

The arc (exp044–052) found competence never compounds — every selection/representation/replicator/
coevolution lever moved the *level* but never the *slope*. exp049 named the one untried move and diagnosed
why its own attempt failed: reifying a competent module to a **new atom** hides its structure in an
**opaque** primitive, out of the measured network. exp053 does it as a **reaction** instead. Every
`catalyst_period` ticks, `catalytic_law` promotes the busiest closure-core edge of the **highest-competence
deme** (achieved *competent* structure) to a persistent shared catalyst — a reaction `anchor_cls →
product_state` injected every tick — so the motif is re-supplied everywhere as a **network-visible class**
(not an opaque atom, the exp049 fix) and later collectives build closures on top of it. The reaction
repertoire tracks the rising frontier: a substrate law that changes with achieved competence. Run on the
exp052 Red Queen base as a 2×2 factorial (`catalytic_law` × {closure, redqueen}).

**Result 1 — the factorial (12k ticks, 6 seeds): both catalytic cells COMPOUND.** catalytic×Red-Queen
rises **monotonically 0.893 → 1.237** (slope **+0.0186/win**, mean **1.183** — the arc's highest level),
with closure (0.26 → 0.43) and survival (0.57 → 0.79) also rising; catalytic×closure +0.0166/win. Both
**fixed-law** cells are flat/declining (Red Queen −0.021, closure +0.004). The Catalytic Law lifts
competence **+0.36** over its no-law control. The **Catalytic Law tilts the slope**; the Red Queen
maximizes level and slope but compounding does not strictly require it.

**Result 2 — the discriminating control (genuine ratchet vs mechanical injection).** `catalyst_random`
promotes a **random edge from a random deme** (same injection rate, no competence-dependence). Random
injection compounds a *little* (+0.0058, mean 0.915 — a small mechanical floor from re-supplying
network-visible reactions), but the **competence-dependent** harvest climbs **3× steeper** (+0.0186) to a
**much higher** level (1.183 vs 0.915). The rise **requires promoting achieved competent structure** — it
is not an artifact of injection. (Catalyst reactions also do not directly write `_deme_edges`; they
re-supply competent product *instances* the composition loop builds on, so the metric is not padded.)

**Interpretation — the competence analogue of Ω-0.20.** Ω-0.20 showed *novelty* is a rate, sustained by
promoting achieved structure to new **primitives**; exp049 tried the literal analogue for competence and
failed because a new **atom** is opaque. exp053 promotes achieved competence to a new **reaction**, which
keeps the structure **in the measured network**, and competence becomes a rate too. This **refines the
arc's central negative**: "open-ended novelty ≠ open-ended competence" (Ω-0.38) held *for a fixed
substrate law* — and named the fix. Once the law itself grows with achieved competence (network-visibly),
competence compounds like novelty does. Self-improvement in this substrate is not impossible; it needs a
**competence-dependent substrate law**, which pure selection routes could not supply.

### Is / is not
- **Is:** the arc's first properly-controlled compounding-competence result — a monotonic rising slope
  (competence-dependent, 3× steeper than random injection) to the arc's highest level, with closure and
  survival also rising, cleanly attributed to a network-visible substrate-law feedback (strongest under a
  receding target).
- **Is not:** unbounded — a small part of the effect is mechanical (random injection ≈ +0.006), and
  **saturation is untested**: the catalyst repertoire (`catalyst_max=16`) reached ~11–14 near the cap, so
  whether competence keeps rising or saturates as the repertoire fills is the immediate next question
  (a longer-horizon / larger-cap run). Within the both-corner typed_path substrate; 6 seeds × 12k.

---

## Milestone Ω-0.41 — The Red Queen: a coevolutionary target raises the competence *ceiling* to the arc's highest, but competence still does not *compound* (exp052)

**Date:** 2026-07-19 · **Status:** complete · **Verdict:** the boldest attempt on the competence-flat
wall — a **level, not rate** result, the strongest yet, that raises the plateau above every fixed-target
baseline but still does not compound. Detail: `studies/EXP052_FINDINGS.md`. Gated; exp001–051
byte-identical (deterministic across `PYTHONHASHSEED`).

The arc (exp044–049) showed competence never compounds — it plateaus under every route, all of which
select against a **fixed target**; exp042's self-expanding scalar bar failed because a global number
chasing the frontier flattens its own gradient. exp052 grounds a **receding** target in real, local
rivals — an arms race. `deme_fitness="redqueen"` rewards a deme for its own autocatalytic closure **plus**
the fraction of its closure core a spatial rival cannot yet produce — a zero-sum, *closure-aligned*
antagonism whose gradient does not vanish (the rival co-acquires the classes, so the deme must innovate
new closed structure) and whose winning strategy **builds** competence (novelty inside the
self-maintaining core, not dead-ends). Decisive control `coevolve_frozen`: the same rule against a
**frozen** rival snapshot (fixed target), isolating the receding target from the fitness form. *(Iterated
to this form honestly: raw offense/defense collapsed diversity, a relative-competence bar inherited
exp042's vanishing gradient.)*

**Result (12k ticks, 6 seeds):** the receding target does **large, real work but does not tilt the
slope.** coevolve competence **0.820** is the **highest of any arm** — beating the frozen control by
**+0.190**, plain closure selection (0.673) by **+0.147**, and drift (0.615) by +0.205 — with the highest
closure (0.255), the most construction (5,505 classes), and the **healthiest, rising** network survival
(0.56 → 0.73; no collapse, unlike exp047). **But competence does not compound:** coevolve's slope is
**−0.021/win** (high-and-flat-to-declining). Same **level-not-rate** pattern as exp048 (replicators lifted
the ceiling ~2× without changing the slope), now in its strongest form and on the *same* substrate as its
controls.

**Interpretation.** exp052 is the **first mechanism in the arc to raise competence above plain closure
selection on the same substrate** (exp045/046 under-performed it, exp047 collapsed it, exp048 needed a
different substrate), and the closure-aligned design keeps networks healthy where naive antagonism
collapsed them. Yet it lands on the same wall: **competence is a stock, not a rate.** With a fixed
substrate law the arms race reaches a mutual-escape equilibrium (everyone running to stay in place —
competence high and steady, relative advantage flat); nothing turns achieved competence into *higher
achievable* competence. The receding target **moves the plateau; it does not remove the ceiling.**
**Open-ended novelty ≠ open-ended competence** (Ω-0.39/0.40 vs Ω-0.38) holds against the strongest lever
yet. The one untried class of move remains the substrate-law change exp049 named — a **Catalytic Law**
(promote competent closure loops to shared *reactions*, not opaque atoms). Natural next rung (exp053, the
user's staged plan): Red Queen + Catalytic Law — the receding pressure plus a substrate-level feedback
that could turn that pressure into a rising ceiling.

### Is / is not
- **Is:** the arc's strongest competence-*level* result — a grounded, receding coevolutionary target
  raises competence above every fixed-target baseline (coevolve − frozen = +0.19; coevolve − closure =
  +0.15) with healthy, rising network survival, cleanly isolated by the frozen control.
- **Is not:** compounding — coevolve's slope is flat-to-negative (−0.021), no rate. Within the both-corner
  typed_path substrate; the mechanism was iterated to its principled (closure-aligned) form before
  measuring.

---

## Milestone Ω-0.40 — The horizon stress: the genuine-novelty floor HOLDS to 3M ticks — the Ω-0.39 caveat closed (exp051)

**Date:** 2026-07-19 · **Status:** complete · **Verdict:** the last open edge of the novelty axis
**closed** — the floor converges to a positive constant, not a slow decline. Detail:
`studies/EXP051_FINDINGS.md`. Measurement only; `global_novelty=False` ⇒ byte-identical, deterministic
across `PYTHONHASHSEED`.

Ω-0.39 settled "stays open" at 10⁶ ticks but left one caveat: the late windows still sagged ~18%, so a
slow second-order decline toward zero was not strictly ruled out. exp051 stresses the horizon **3×
(3M ticks × 3 seeds)** with the eviction regime held **fixed** (`memory_horizon=5000`) so the floor is
compared fairly, and `relation_cap` shrunk for throughput (does not touch the registry-independent
global metric).

**Result (3M ticks, 3 seeds):** the floor **holds**. After the transient (global rate 0.22 → 0.08 over
the first ~1M ticks, a 64% fall), the eviction-robust rate is **flat within ~14% across the entire final
2M ticks** (0.084 → 0.070), decisively above the closed control's **exact 0.0000** — ~**281,400 distinct
classes ever/seed** (≈2.1× the 10⁶ value, consistent with a steady ~0.07–0.09/tick) vs the closed
alphabet's unchanged **144**. mid(~1–2M)=0.0815, final(~2–3M)=0.0699, **hold ratio 0.86**. The decline is
**decelerating toward an asymptote, not descending toward zero**: 64% over the first 1M, only ~14% over
the last 2M — log-like convergence to a positive floor, the opposite of linear dilution.

**Interpretation.** Constructibility is a **rate with a positive floor** that *holds*, not merely
*appears to hold* — shown over a 3× longer horizon with the eviction regime fixed and the closed control
reading exact zero throughout. The novelty axis of "truly unbounded" is now settled to 3M ticks. Read
with Ω-0.38, both axes are firm: **construction is open-ended** (a floor holding to 3M) while
**competence is not** (the arc plateaued) — the world compounds *what it builds*, durably, but not *how
good its collectives get*.

### Is / is not
- **Is:** the Ω-0.39 caveat closed — a 3× horizon stress showing the genuine rate flat within 14% across
  2M late ticks, decelerating (64%→14%) toward a positive asymptote, closed control exact-zero throughout.
- **Is not:** a proof of a *perfectly* flat rate — a residual ~14% sag remains, so a 10⁷ run could reveal
  a very slow drift (the deceleration argues against it). 3-seed stress; the 10⁶ result is the 5-seed
  anchor. Both-corner substrate; bounded-memory measurement (the global sketch is the right instrument).

---

## Milestone Ω-0.39 — "Stays open forever" settled at 10⁶ ticks: the genuine-novelty floor is REAL, and the Ω-0.31 decline was a transient (exp050)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** the program's **load-bearing claim, settled
at the literal long horizon** — a positive, asymptotic genuine-novelty floor. Detail:
`studies/EXP050_FINDINGS.md`. Measurement only (no physics change); `global_novelty=False` ⇒ every
experiment byte-identical, deterministic across `PYTHONHASHSEED`.

Ω-0.31 settled "constructibility keeps the world open" *honestly but partially*: on the eviction-robust
**global** novelty sketch (each class counted once *ever*, stripping the recycling that inflates the
windowed rate under bounded memory), the open engine's genuine rate was **positive but slowly declining**
— it *halved* over 300k ticks / 3 seeds, leaving open whether it floors or dilutes to zero. exp050 runs
the literal **10⁶-tick × 5-seed** campaign the thesis is stated for: open engine (exp030, the both
corner) vs closed control (exp029), both metrics over 10 windows of 100k ticks.

**Result (10⁶ ticks, 5 seeds):** the floor is **real**. The eviction-robust global rate runs
0.30 → 0.10 over the first ~400k ticks and then **levels onto ~0.085–0.10 genuinely-new classes/tick for
the entire second half**, decisively above the closed control's **exact 0.0000** — ~**130,600 distinct
classes ever per seed** (registry held flat at ~3,100 by eviction) vs the closed alphabet's **144**. The
late windowed/global inflation factor is **~5.0**, confirming Ω-0.31's diagnosis that the *windowed* rate
(flat ~0.465) is ~5× inflated by recycling. **The Ω-0.31 "slow decline" was a transient, not dilution:**
the steep drop is confined to the first ~400k ticks (a 67% fall), after which the rate sags only ~18%
across the next 600k — a decelerating curve converging to a positive constant, not descending toward
zero. Ω-0.31's open worry is resolved in favor of **floor**.

**Interpretation.** This is the strongest form of the program's central thesis, at the horizon it was
always stated for: **open-endedness of *construction* is genuine and asymptotic**, not a finite budget
draining through a measurement window. A *modular-and-open* both-corner substrate keeps building
genuinely-new organization at a stable positive rate to 10⁶ ticks; a *closed* substrate stops dead at
144 classes. Constructibility is a **rate with a positive floor** (~0.09 new classes/tick), and the
both-corner condition is what sustains it. Read with Ω-0.38: **construction is open-ended; competence is
not** — the world compounds *what it builds* (forever, measurably) but not *how good its collectives get*.

### Is / is not
- **Is:** the load-bearing claim ("stays open") settled on the conservative, eviction-robust metric at
  10⁶ ticks / 5 seeds, an order of magnitude beyond Ω-0.31, with the closed control as the exact-zero
  null and the "slow decline" worry resolved as a transient.
- **Is not:** a proof of a *perfectly* flat rate forever — windows 4–9 still sag ~18%, so a 10⁷ run
  could reveal a slower second-order decline (the deceleration argues against it). Within the both-corner
  substrate; bounded-memory measurement (exactly why the registry-independent global sketch is the
  instrument).

---

## Milestone Ω-0.38 — Competence as a *rate*, not a *stock*: reifying achieved competence does **not** raise the ceiling — the arc's open problem, closed (exp049)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** an **honest negative that resolves the arc's
sharpened open problem** — the Ω-0.20 rate-not-stock lever does not transfer from novelty to competence.
Detail: `studies/EXP049_FINDINGS.md`. Gated; exp001–048 byte-identical (deterministic across
`PYTHONHASHSEED`).

exp048 left the arc with one question. The program has *two* open-endednesses and had shown only one:
**construction is open-ended** (Ω-0.31, the genuine novelty rate stays positive) but **competence is
not** (exp048, collectives plateau at a substrate-set ceiling). The program's answer to plateauing
*novelty* was Ω-0.20: openness is a **rate**, sustained by **continuing reification** — promote achieved
structure to new primitives and the construction space keeps growing. exp049 aims that exact lever at
competence: `reify_by="closure"` promotes the most **closure-central** module (achieved *competent*
structure, a class repeatedly in demes' autocatalytic cores) to a new atom every `reify_period` ticks,
so each cohort builds on the previous cohort's competent modules and the ceiling might climb. Controls:
`reify_by="frequency"` (exp034 — promote *common*, not competent, structure) and `reify_period=0` (the
exp048 plateau, no reification).

**Result (12k ticks, 6 seeds):** competence **stays a stock.** All three arms are flat — reify-closure
slope **+0.0006**/win (mean 0.684), reify-freq +0.0022 (0.686), no-reify +0.0046 (0.673); competence
oscillates in a fixed ~0.63–0.80 band in every arm across all 8 windows and the ceiling does not climb.
Reifying *competent* structure is statistically indistinguishable from reifying *common* structure or
from *not reifying*. Strikingly, the reify arms grow their alphabet 32 → 51–53 atoms and find ~26% more
distinct classes (5.8k vs 4.6k) — **novelty compounds** — while competence does not: Ω-0.31's
open-ended-novelty-≠-open-ended-competence, demonstrated *within one experiment*.

**Interpretation.** Reification raises *novelty* because a new atom **enlarges** the constructible space
and the metric counts exactly that. It cannot raise *competence* because competence is measured on the
**cross-production network** (closure, breed-true heredity, breadth), and promoting a competent module
to an **opaque atom moves its internal structure *out* of that network** — the closure it embodied
stops being visible as closure. Reification trades measured competence *inside* the module for a bigger
alphabet *outside* it: a lateral move, not a ratchet. No dynamical coupling makes achieved competence
raise the *ceiling*; the ceiling is set by the substrate's fixed reaction law, which reification never
touches. **The Ω-0.20 rate-not-stock lever does not transfer from novelty to competence** — they are
genuinely different, and the competence plateau is intrinsic to selection over a fixed substrate.

**The arc's open problem is resolved (negatively).** Compounding competence is achieved by *no* move the
program has: not goal representation (exp044), credit assignment (exp045/046), selection grain (exp047),
replicating parts (exp048), or competence reification (exp049). Any future route must change the
**substrate law itself** during the run (make the reaction physics competence-dependent), not merely
grow its alphabet — a qualitatively harder move than anything in the arc.

### Is / is not
- **Is:** a direct, multi-seed test of the arc's last standing candidate lever, showing it fails and
  *why* (reification enlarges the alphabet, not the network competence lives on); a clean within-run
  demonstration that novelty compounds while competence does not.
- **Is not:** proof that *no* mechanism can compound competence — it rules out the reification lever and
  names the one class of move not yet tried (changing the substrate law mid-run). Within-substrate
  measure on the typed_path both-corner base.

---

## Milestone Ω-0.37 — The loop-back: part-level replicators lift the competence *ceiling* (~2×) but competence still doesn't *compound* — open-ended novelty ≠ open-ended competence (exp048)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** the arc's **closing result** — a mixed
outcome that separates two kinds of open-endedness. Detail: `studies/EXP048_FINDINGS.md`. Gated;
exp001–047 byte-identical (deterministic across `PYTHONHASHSEED`).

exp047's terminal diagnosis was that the typed_path substrate's parts are not replicators, so
collective competence can't compound. exp012 found genuine part-level replicators in the SKI-combinator
soup (`C·x → C`). exp048 runs the exp046 credit machinery on that **combinator substrate** — so a
credited part can copy its own heritable value — and closes the loop from the arc's end to its start.
Arms: `replicator` (combinator + credit), `network` (typed_path + credit = exp046), `replicator-drift`
(combinator + size).

**Result (12k ticks, 6 seeds):** part-level replicators **lift the ceiling but don't close the
compounding gap.** On the combinator substrate competence reaches **~1.09** (vs typed_path's 0.62) and
closure **~0.36** (vs 0.13), with ~6× more distinct classes — a large, robust *substrate* effect that
partially vindicates exp047 (whether parts are replicators strongly sets *how competent* collectives
get). **But competence is high-and-flat, not rising**: replicator+credit slope +0.001, drift +0.006,
network −0.008 — all ≈ 0. Credit is not the lever even here (it raises the plateau, flattens the slope).

**Interpretation.** The loop-back resolves the arc by separating two open-endednesses the program had
conflated. Ω-0.31 showed **construction is open-ended** — the genuine novelty rate stays positive, the
world keeps building never-seen classes forever (here ~19–23k distinct classes). exp048 shows
**competence is *not* open-ended** — collectives get more competent up to a substrate-set ceiling and
plateau, regardless of selection or the parts' replicator status. **Open-ended novelty ≠ open-ended
competence:** the world compounds *what it builds*, not *how good its collectives are*.
Self-improvement-as-unbounded-competence-growth is not achieved in this substrate family, and the
obstacle is deeper than "the parts aren't replicators" (fixing that only lifts the ceiling): nothing
in the dynamics couples a collective's competence to an *ever-rising* target. The sharpened open
problem is the Ω-0.20 lesson applied to competence — **what makes competence a *rate*, not a *stock***
— a substrate/measurement question, not another selection knob.

**The self-improvement arc (exp036–048) is complete.**

### Is / is not
- **Is:** a robust, multi-seed result that separates open-ended novelty (achieved) from open-ended
  competence (not achieved), shows part-level replicators raise the competence ceiling ~2× without
  tilting the trajectory, and names the real unsolved problem (competence as a rate).
- **Is not:** a clean "yes" to the loop-back, nor proof no substrate can compound competence — it shows
  the program's two substrates both plateau. Within-substrate measures; the combinator both-corner is
  weak (exp024–028 heredity wall).

---

## Milestone Ω-0.36 — Within-collective selection *collapses* the collective: competence is irreducibly collective — the self-improvement arc's terminal diagnosis (exp047)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** a **deep negative that closes the arc** with
a structural conclusion, connecting its end back to its origin (exp012). Detail:
`studies/EXP047_FINDINGS.md`. Gated; exp001–046 byte-identical (deterministic across `PYTHONHASHSEED`).

exp046 blamed the failure of credit-in-the-fitness on the selection *grain* — deme reproduction copies
a whole propagule and can't retain the credited parts. exp047 adds the missing grain: `within_select`
founds each offspring from the source deme's members sampled with probability rising in their credit
(Efraimidis–Spirakis weighted, with a floor) — parts competing *inside* the collective, a second
selection level below the deme. Control: exp046 (`within_select=False`).

**Result (12k ticks, 6 seeds):** it **collapses the collective.** Within-selection competence (mean
0.363, declining) is far *below* deme-only credit (0.615) and drift (0.613), and network survival falls
to **0.29** of demes (vs 0.43) — biasing reproduction toward high-credit members erodes the diversity
the cross-production network needs, so fewer demes sustain a network at all. Holds for both the strict
top-k and the gentler weighted form.

**Interpretation — the terminal diagnosis.** The credited parts have no value in isolation: a deme's
competence is a property of a *diverse, complementary* network of members that produce each other.
Select hard for those parts as individuals and you strip out their partners, destroying the network
and the competence it carried — part-level selection on credit is **self-defeating**. So **collective
competence is not decomposable into independently selectable part contributions** — the credit is not
localizable to parts, it lives in their relations. Credit assignment failed not because credit couldn't
be represented (exp046) or acted on at grain (exp047) but because it isn't *localizable*. The
resolution connects the arc to its origin: compounding would require the parts to be **replicators**
(units carrying/copying their own context-independent heritable value — the exp012 `C·x → C` lesson);
the type-path parts are context-dependent network components, not replicators, so no route through
goal representation (exp044), goal alignment (exp045), credit-in-fitness (exp046), or within-collective
selection (exp047) makes collective competence compound.

**The self-improvement arc (exp036–047) is complete** as a falsifiable sequence: it ruled out every
selection/representation route to compounding collective competence and terminated in a *substrate*
reason. The honest next move is not another deme-selection knob but revisiting whether a substrate
whose parts are themselves replicators lets collective competence compound.

### Is / is not
- **Is:** a robust, multi-seed, structural negative (within < credit on competence and network survival
  every window past the transient; both strict and weighted forms) that closes the arc with a
  substrate-level diagnosis and a named loop-back to exp012.
- **Is not:** proof no substrate can compound collective competence — it shows *this* one cannot via
  selection alone, and names the missing ingredient (part-level replicators), a substrate property.

---

## Milestone Ω-0.35 — Credit in the fitness still doesn't compound: the limit is the selection *grain* → within-collective selection (exp046)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** an **informative negative** that isolates
the deepest limit of the arc and names its final structural move. Detail: `studies/EXP046_FINDINGS.md`.
Gated; exp001–045 byte-identical (deterministic across `PYTHONHASHSEED`).

exp045 concluded credit assignment must live in the *fitness*, not the goal. exp046 does exactly that:
`deme_fitness="credit"` gives each deme a **heritable per-class contribution map** that accrues credit
for its autocatalytic closure-core classes (the parts that cause self-maintenance) each generation, and
selection rewards demes that **retain** their high-credit parts; the map is inherited so credit
accumulates down a lineage. Controls: exp038 `closure` (instantaneous closure selection) and `size`.

**Result (12k ticks, 6 seeds):** it **still does not compound — and is worse than plain closure
selection.** The credit arm's competence (mean 0.635, slope −0.008/win) does not rise and sits *below*
instantaneous closure selection (0.692), barely above drift (0.627); on closure itself the credit arm
(0.130) trails closure-select (0.188). (A 3-seed/4k pilot showed a spurious positive that did not
survive scale — the Ω-0.33 lesson applied.)

**Interpretation.** The credit signal is present, heritable, and correct — but **deme-level selection
cannot act on it at the right grain.** Reproduction copies a whole propagule; it can favour a deme that
currently *contains* high-credit parts but cannot preferentially **keep those specific parts** against
within-deme drift and recolonization sampling, so the fitness rewards *having* the parts, not
*retaining* them, and they wash out — the credit map becomes a passenger. An explicit heritable
contribution signal is **necessary but not sufficient**; the missing faculty is *acting* on it at
sub-collective granularity. **The frontier is the selection grain: parts must compete WITHIN the
collective.** Arc: exp044 (composable goals, transient) → exp045 (aim goal at closure → credit is a
representation problem) → exp046 (credit in the fitness → still no compounding → **within-collective
selection**, a second level *below* the deme).

### Is / is not
- **Is:** a robust multi-seed negative (credit ≤ closure-select on competence and closure past the
  transient) that isolates *why* an explicit credit model fails — the selection grain — and names the
  next rung (exp047: within-collective selection, differentially retaining high-credit parts inside a
  deme).
- **Is not:** proof no credit mechanism can work — it shows *this* whole-deme-granularity one does not.
  Within-substrate measures; one credit rule.

---

## Milestone Ω-0.34 — Credit assignment is a representation problem, not a targeting one: aiming the goal at the closure core still doesn't compound (exp045)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** an **informative negative** that sharpens
the arc's final frontier. Detail: `studies/EXP045_FINDINGS.md`. Gated; exp001–044 byte-identical
(deterministic across `PYTHONHASHSEED`).

exp044 diagnosed the barrier past *goal representation* as **goal alignment / credit assignment** — the
collective deepens goals but can't attribute its competence to its parts, so pursuing a deeper goal
cannibalises self-maintenance. exp045 tries the most direct fix: `goal_align=True` aims goal
reification at the deme's **autocatalytic closure core** (classes that are both producers AND products
— the self-maintaining loop that *is* its competence), so growing the goal should reinforce closure.
Matched control is exactly exp044 (`goal_align=False`).

**Result (12k ticks, 6 seeds):** it **still does not compound — and alignment is slightly worse.**
Aligned generic competence (mean 0.38, slope −0.083/win) is *below* the unaligned exp044 control
(0.41), and **both goal arms are far below the drift floor (0.63)** — selecting on goal achievement,
aligned or not, *degrades* competence. Aiming at the closure core did not even raise closure (aligned
0.047 < unaligned 0.053 < drift 0.097).

**Interpretation.** The fix was aimed at the wrong thing. Alignment changed the goal's **direction**
(grow it along the closure core) but not the **selection pressure**, which is still `achievement ×
depth` — so selection keeps rewarding *building the goal path* whether or not that maintains closure,
and merely pointing the target at the core does not change the trade. The lesson: **credit assignment
is a representation problem, not a targeting one.** For competence to compound, the collective needs an
*explicit, heritable model of which parts cause its competence that selection itself acts on* — not a
goal aimed at those parts. The substrate transmits a goal path and a developmental niche, but no
transmissible per-part *contribution* signal; without one, selection on any single achievement scalar
reverts to the same trade-off. Arc: exp039 → exp040 (break heredity ceiling) → exp041 → exp042 (goal
representation missing) → exp044 (composable goals, transient deepening, no competence lift) → exp045
(aim the goal at closure → still no compounding → **credit must live in the *fitness*, not the goal**).

### Is / is not
- **Is:** a robust, multi-seed negative (aligned ≤ unaligned ≤ drift on competence past the transient)
  that isolates *why* a natural credit-assignment fix fails, and names the next rung (exp046: a
  heritable, selectable per-part contribution representation).
- **Is not:** proof no alignment can work — it shows *this* direct target-aiming rule does not, and
  diagnoses the reason (it moves the target, not the selection pressure). Within-substrate measures.

---

## Milestone Ω-0.33 — Determinism restored: results are now byte-identical across PYTHONHASHSEED (consolidation)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** a **hardening consolidation** — a real
reproducibility bug, discovered while building exp044, is fixed at the source. Gated experiments
unchanged in kind; 72 tests green (incl. a new cross-hash-seed guard).

**The bug.** Building exp044 surfaced that the same `seed` produced different absolute results across
process invocations — e.g. `classes_ever_seen` for exp040 was 360 / 1005 / 1075 under
`PYTHONHASHSEED` 0 / 1 / 2. The cause was **`set`/`frozenset` iteration order**, which Python
randomises per process: the exp040 developmental template built its niche seed by iterating a deme's
signature (a `frozenset`) into a list and truncating `seed[:keep]` — so *which* product states seeded
the child, and the order they were later recycled by `rng.choice`, depended on the hash seed. Every
run using `network_template` (exp040/041/042/044) inherited the nondeterminism; the base engine
(exp030, dict/list-ordered, no template) was already deterministic (859/859/859), which is why it went
unnoticed.

**The fix (one line, plus a guard).** Sort the signature into a canonical order before building the
seed list (`sorted(self._deme_signature(src))`) — `frozenset` iteration is the only hash-dependent
step; dict iteration (insertion order) and the membership/Jaccard uses of the other sets are already
order-independent. After the fix, exp040/041/042/044 are byte-identical across hash seeds
(exp040 → 1246 at every seed; verified for exp030/34/35/36/37/38/39/41/42/44, culture, world). A new
`TestDeterminism.test_deterministic_across_hash_seeds` runs exp040 in two subprocesses with different
`PYTHONHASHSEED` and asserts exact agreement, so this cannot silently regress.

**Scope / honesty.** The fix **changes the specific numbers** of template-using runs (they were
previously computed under one uncontrolled hash seed; the deterministic engine picks the canonical
`sorted` ordering). The affected studies (exp040/041/042/044) were **re-run and their committed
`results.json`/findings refreshed** so every claim again traces to a reproducible artifact. The
**qualitative verdicts are unchanged** — they are matched-control inequalities robust across the
ordering (exp040 still breaks the heredity ceiling; exp044's composable goal depth still ratchets
while fixed stays pinned; exp041/042 still don't compound). This closes the determinism caveat noted
in Ω-0.32 and restores the program's "same config ⇒ same result" guarantee across machines, the
natural companion to Ω-0.31's measurement consolidation.

---

## Milestone Ω-0.32 — The frontier: heritable, composable GOALS make competence ratchet at last — but narrowly, and at the cost of generic competence (exp044)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** the **first over-generations *deepening*
in the entire arc** — a real, mixed positive — with an equally important honest caveat that names the
next frontier. Detail: `studies/EXP044_FINDINGS.md`. Gated; exp001–043 byte-identical.
*(Numbers corrected for the Ω-0.33 determinism fix: the effect is real but the earlier "sustained
ratchet 2.4→4.0, max 10" was partly a favourable `PYTHONHASHSEED` — deterministically the ratchet is
**transient**.)*

exp042 diagnosed the barrier to self-improvement as **goal representation**: the substrate can reify
*structure* but has no heritable, composable representation of a *goal* to reify. exp044 supplies it —
in `typed_path` a goal can be an object of the substrate's own kind, a **target path**: each deme
carries one that is heritable (transmitted + `_mutate_path`), achievement-measured (the path realized
as a contiguous stretch of a produced class or across a producer→product edge), and composable
(robust achievement **extends** the goal by one node, *directed* toward the atom the deme most
produces — faithful reification of achieved structure). Fitness = achievement × depth; controls are
`goal_reify=False` (fixed goals, isolating composability), the exp042 scalar `ratchet`, and `size`.

**Result (12k ticks, 4 seeds; deterministic, Ω-0.33):** (1) **the faculty has a real effect** —
composable goal depth climbs far above the fixed control (per-window **2.6 → peak 4.3 → 3.3**, max
depth **7**) while fixed goals stay pinned at exactly 2. Nothing in exp039/041/042 deepened over
generations; here composability does — the arc's first over-generations deepening. (2) **But it is
not sustained, and doesn't lift generic competence** — the depth trajectory is a **hump** (overshoots
then partially collapses: deeper goals outrun what the network can build), and generic competence
(closure + breed-true heredity + breadth) is middling: composable 0.46 beats fixed 0.39 and the
exp042 ratchet 0.30 but **loses to drift (0.60)**.

**Interpretation.** The arc advances from "no compounding" to "**transient deepening, not sustained**".
Deeper achievements *can* accumulate once collectives have a heritable, composable goal — but the
accumulation peaks and partially collapses, and does not transfer to general competence. The barrier
past goal representation is **goal alignment / credit assignment**: the collective can extend and
pursue a target but cannot tell *which of its parts* makes it competent, so it can neither aim the
goal at its own self-maintenance nor keep achieving a target that has grown past what its network can
build. The full sequence: exp039 (fixed multi-obj) → exp040 (break heredity ceiling) → exp041 (fixed
target) → exp042 (scalar self-expand → goal representation missing) → exp044 (heritable composable
goals → deeper goals accumulate but transiently → **goal alignment / credit assignment**).

### Is / is not
- **Is:** the first over-generations *deepening* the program has produced (composable ≫ fixed, peak
  ~4.3, max 7), decisively above a matched fixed-goal control — the represented faculty demonstrably
  produces deeper achievements; and a precisely named next rung (exp045: align goal reification with
  the collective's own closure/heredity/breadth).
- **Is not:** a *sustained* ratchet (it humps and partially collapses), nor a lift in *generic*
  competence (it loses to drift). "Competence"/"goal depth" are within-substrate measures.

---

## Milestone Ω-0.31 — "Stays open forever" settled with an eviction-robust metric: a genuine positive floor — and the old "flat rate" was ~4× a measurement artifact (exp043 / consolidation)

**Date:** 2026-07-18 · **Status:** complete · **Verdict:** the program's most load-bearing claim is
**confirmed in its correct form and its overclaimed part retired** — a model consolidation. Detail:
`studies/EXP043_FINDINGS.md`. Gated; exp001–042 byte-identical (70 tests green).

Every long-horizon open-endedness check had to run under bounded memory, which evicts cold class
records — so an evicted class that reappears **re-counts** in the novelty rate, and a positive
long-run *windowed* rate could not be told apart from classes recycling through the eviction window
(exp032's "positive-floor vs slow-dilution" open edge). This adds the missing instrument — a
fixed-memory **global** novelty estimator (`omega/emergence/global_novelty.py`, a scalable Bloom
"ever-seen" set; gated `run(global_novelty=True)`, off ⇒ byte-identical) that counts each class only
once *ever*. It is conservative by construction: repeats are never counted as new (all recycling
stripped), and genuine novelty is only ever under-counted by ≤ ~1% — so it can only *lower* the
measured rate, never fabricate openness.

**Result (300k ticks, 3 seeds; open = exp030 both corner, closed = exp029), two findings:**
- **The claim holds — a genuine positive floor.** With all recycling stripped, the open engine still
  discovers **never-before-seen** classes at **~0.13/tick at 300k** (retention 0.45–0.50 across
  seeds; ~61k distinct classes accumulated on a *flat* ~2k registry), **decisively above the closed
  control's exact 0.000**. The closed arm proves the instrument: its ~0.003/tick windowed residual is
  stripped to zero — pure recycling. "Stays open" is a real property of the genuine rate, well past
  exp032's ambiguous 120k edge.
- **But the old "flat rate" was ~4× a windowing artifact.** The *windowed* rate is flat at ~0.53 for
  the whole run (what the previous instrument reported as "sustained"); the global rate shows that
  flatness is **inflated 4.17×** late by recycling. The **true** genuine rate is **positive but
  declining** — it roughly **halves** over 300k (0.28 → 0.13), not constant.

**Interpretation.** Consolidation did its job: **confirmed** the world is genuinely open (a
seed-robust positive floor a closed substrate cannot produce), and **corrected** the overclaim — "the
novelty rate stays *flat* forever" was substantially a bounded-memory artifact; the honest statement
is "the genuine rate stays *positive* and decisively above closure while slowly declining." This
retroactively sharpens exp032/exp034: their *rankings* (open ≫ closed; continuing ≫ capped
construction) stand (common-mode, bounded-to-bounded), but their absolute "constant rate" readings are
an upper bound on the genuine rate.

### Is / is not
- **Is:** a hardened base — the core claim now rests on a conservative, artifact-free, multi-seed
  metric to 300k ticks, and the residual is a *measured* question (does the global rate asymptote
  above zero at 10⁶–10⁷?), not a conceptual gap.
- **Is not:** a proof of a non-zero asymptote (the verdict is about the last windows at 300k, 0.13/tick
  ≫ 0, not the limit); one law, ≤ 300k ticks. The global rate is a conservative under-estimate, so
  true novelty is ≥ what is plotted.

---

## Milestone Ω-0.30 — A self-expanding objective still doesn't compound: the barrier is *goal representation*, not the objective's mobility (exp042)

**Date:** 2026-07-17 · **Status:** complete · **Verdict:** an **informative negative that names the
deepest frontier** — and closes the self-improvement arc's logic. Detail: `studies/EXP042_FINDINGS.md`.
Gated; exp001–041 byte-identical (69 tests green).

exp041 pinned the blocker on the *fixed* objective; exp042 makes the objective itself grow.
`deme_fitness="ratchet"` scores each deme's absolute competence (closure + breed-true heredity +
normalized network breadth, ~[0,3]) and rewards it for **beating a moving bar** that is raised toward
the achieved frontier and never lowered — *goal reification*, the collective analogue of reifying
structure into primitives. Run with the exp040 heredity channel on; controls are exp041 (fixed
composite) and drift; the bar chase-rate is swept (lr ∈ {0.1, 0.25, 0.5}) so no single rate can be
blamed (8000 ticks × 5 seeds).

**Competence does not ratchet — and the moving objective is *worse* than the fixed one.** Every
chase-rate gives a flat-to-declining frontier slope (−0.029 / −0.025 / −0.084 per window; the
*fastest* chase is the *worst*), and the fixed composite ends with the **highest** frontier of all
(0.99 vs the best ratchet's 0.58). The heredity channel is engaged throughout (self/null 4.5–8.2×),
so this is a failure to *accumulate*, not to inherit.

**Two mechanisms, both pointing past the objective's mobility.** (1) A bar that chases the frontier
**flattens its own selection gradient**: once the bar converges near the top deme, `max(0, comp − bar)`
collapses to the floor for almost every deme → near-neutral drift (harder chase ⇒ flatter ⇒ observed
ordering). A "beat the current best" objective removes its gradient the instant competence stops
rising. (2) More deeply, the bar is a single **non-heritable, non-composable scalar** — the substrate
has no representation of a *goal* to reify. Reifying **structure** worked (Ω-0.20) because structure
is exactly what this substrate transmits; reifying a **goal** fails because there is no heritable,
composable goal representation to transmit.

So the arc lands precisely: **open-ended collective self-improvement needs a representational faculty
for heritable, composable goals — not just heritable structure (exp040) and not just a moving scalar
target (exp042).** The whole sequence: exp039 (fixed multi-objective doesn't compound → suspect
heredity) → exp040 (break the heredity ceiling) → exp041 (still doesn't compound → blame the fixed
target) → exp042 (self-expand the target → still doesn't, worse → the barrier is goal representation).

### Is / is not
- **Is:** a robust, multi-seed, multi-rate negative from a *powered* setup (heredity present), and a
  named next frontier that for the first time requires new *representational* machinery (heritable,
  composable goals), not a new selection rule.
- **Is not:** proof that no open-ended objective can work — it shows *this* natural family (scalar,
  self-referential bars) cannot, and diagnoses *why* (gradient collapse + no goal representation).
  "Competence" is a within-substrate composite, not task performance.

---

## Milestone Ω-0.29 — A higher heredity level is not enough: competence does not compound; the blocker moves to *the objective* (exp041)

**Date:** 2026-07-17 · **Status:** complete · **Verdict:** an **informative negative that sharpens
the located blocker** — the payoff capstone the whole self-improvement arc was built toward. Detail:
`studies/EXP041_FINDINGS.md`. Gated; exp001–040 byte-identical (68 tests green).

exp040 broke the collective-heredity *ceiling*; exp041 asks the arc's final question: with a strong
heredity channel available, does competence **compound** — closure, heredity, and function rising
together over generations? It runs the two mechanisms together (`deme_fitness="composite"` +
`network_template=0.5`) against exp039 as-is (composite, template off) and a drift arm (size +
template), and watches a **trajectory** (per generation-window closure, per-window heredity rate,
network-breadth function), 8000 ticks × 5 seeds, bounded memory.

**Both mechanisms work separately, but competence does not compound.** The template raises the
heredity *level* (treatment self 0.256 = **1.7× the composite-only control, 3.4× null**,
re-confirming exp040) and composite selection raises the constructive axes (closure 0.286 / function
4.55 vs the drift arm's 0.055 / 1.83). **Yet heredity still declines across generations in every arm**
(steady-state −4.5% / −6.7% / −13.6% per window); the developmental channel *slows* the erosion but
does not reverse it, and closure/function only drift near-flat. No arm gets the three axes rising
together. Raising the heredity *level* was **necessary but not sufficient**.

**The blocker moves from "weak heredity" to "no open-ended objective."** With a **fixed** selection
target, selection climbs to the bar and stops while mutation erodes fidelity — competence plateaus
and slowly decays; nothing makes the *target itself* keep rising, so there is no ratchet. This is the
program's own **"rate, not stock"** lesson (Ω-0.20) one level up: a substrate stays open only under
*continuing* construction, and a *collective* improves open-endedly only under a *continuing*
objective. The drift arm sharpens it — it gets the **highest** raw heredity (6.4× null) essentially
free from canalization yet has almost no closure or function: heredity level alone is not competence,
and the three axes genuinely trade off under any fixed scalar.

### Is / is not
- **Is:** a clean falsifiable negative from a *powered* setup (strong heredity is present, exp040) —
  the sign (heredity is the declining axis) is robust across full-run and steady-state and all three
  arms; and a precise hand-off — the named remaining gap is an **open-ended, self-expanding
  objective** (collective-level reification of *goals*, the analogue of substrate-level reification
  of *primitives*).
- **Is not:** a null from underpowering, and not a claim that self-improvement is impossible here —
  the machinery (exp037/038) and the heredity channel (exp040) are in place; what is missing is a
  moving target. The three axes are correlated within-substrate proxies, not independent faculties;
  "function" is network breadth, not task performance.

---

## Milestone Ω-0.18 — First-class levels: the transition recurses across *different* physics (exp033)

**Date:** 2026-07-11 · **Status:** complete · **Verdict:** the recursive tower does **not**
depend on one engine climbing itself. With a *different composition law per tier*, the major
transition still recurses across the physics boundary — **provided each level's law is itself
open + modular**. The one hard rung is **closure**, not difference. Detail:
`studies/EXP033_FINDINGS.md`. Gated (`run_stack(levels=…)`, default `None` byte-identical);
exp001–032 unchanged.

### Why / what was done
exp031/032 stacked a tower but ran the *same* exp030 `typed_path` engine at every tier — the
last "is not" in Ω-0.16/0.17 was that levels were not first-class. `omega/levels/stack.py`
now takes `levels=(...)`, a per-tier sequence of registered engines that share the type-atom
interface but apply different laws: exp029 (morphism composition, **closed**), exp030 (path
concatenation, **open**), exp031_culture (concatenation + horizontal transfer, **open +
Lamarckian**).

### The result splits cleanly (1500 ticks/tier, max_tiers=5, 3 seeds)
- **Crossing a boundary is free.** A tower alternating *two different open laws* (exp030 ↔
  exp031_culture) has **per-seed depth identical to the self-similar baseline** ([5, 0, 5])
  and **8/8 physics-boundary crossings survive** — a tier forms heritable collectives from
  the collectives of a tier that ran a *different law*. The recursion is a property of the
  both-corner condition, not of self-similarity. **Levels are first-class.**
- **The cost is closure, not heterogeneity.** Every tower containing the **closed** law
  (exp029) caps at depth 1: the closed tier forms only 1 collective (< 2), starving the
  promoted alphabet. `alt_two_open` crosses just as many boundaries with no penalty, so the
  culprit is closure — the exp030 **"both corner" condition reappears at every level
  boundary**: each level's law must itself be open + modular for the tower to continue.

### Is / is not
- **Is:** the level abstraction first-class — heterogeneous per-tier physics, the transition
  recurses across different composition laws (including the cultural law atop the biological),
  with the default tower kept byte-identical. One principle (open + modular) governs both the
  first transition and the composition of levels.
- **Is not:** proof that *any* law composes — a closed law is a terminal rung; the
  heterogeneity shown healthy is open-law × open-law across three type-atom engines. A
  genuinely new non-substrate level law remains future work.

---

## Milestone Ω-0.27 — Capstone: the machinery for self-improvement is present; high-fidelity collective heredity is not (exp039)

**Date:** 2026-07-13 · **Status:** complete · **Verdict:** closes the self-improvement arc
(exp036→039) with a precise, falsifiable location of the barrier. Detail:
`studies/EXP039_FINDINGS.md`. Gated; exp001–035 byte-identical (56 tests green).

exp038 left the question: does **multi-objective** selection beat the single-objective trade-off?
Two findings (6000 ticks, 3 seeds). **(1) The trade-off is not fundamental:** across demes closure
and collective heredity are **independent** (corr −0.001) — both-high demes exist. **(2) But
combining objectives still does not compound:** `deme_fitness="composite"` (maximin over the two
mean-normalized objectives) reaches the **highest closure of all** (0.078) yet leaves **heredity
low** (0.106 vs 0.209 under direct network selection); three composite formulations
(multiplicative, normalized, maximin) all give the same shape — closure compounds, heredity does
not.

**Diagnosis:** selection can only stack a property as fast as it is inherited, and **collective
heredity is the weak channel** — the exp028 ceiling (network signatures transmit at only ~3–5×
null, substrate-limited). Closure (a local, low-dimensional loop property) transmits well enough to
select; the full multi-edge network heredity does not, so competence **cannot compound**. Verdict
on the self-improvement question: the **machinery is present** — collectives carry evolvable
internal state (exp037) and are selectable on emergent coherence (exp038) — **but the missing piece
is high-fidelity collective heredity**, not more selection or a cleverer objective. The follow-on
work points squarely at the exp028 ceiling: raising whole-network transmission fidelity is the
prerequisite for open-ended collective self-improvement. Until then, Ω collectives are evolvable and
selectable but do not compound into minds.

---

## Milestone Ω-0.28 — The collective-heredity ceiling breaks: developmental (network-template) inheritance (exp040)

**Date:** 2026-07-14 · **Status:** complete · **Verdict:** a **major positive** — the single blocker
exp039 located is removed. Detail: `studies/EXP040_FINDINGS.md`. Gated; exp001–039 byte-identical
(57 tests green).

exp039 said competence cannot compound because collective heredity is stuck at the exp028 ceiling
(~3–5× null; the network is a dynamical attractor offspring don't re-form from inherited *members*).
exp040 transmits the **developmental niche** too: a fraction `network_template ∈ [0,1]` of the parent
network's product states is seeded into the child's recycle buffer, so it is re-fed the parent's
outputs and canalizes toward its edges (niche / parental-effect inheritance). The strength is a dial —
the collective-level analogue of exp030's resolution dial. Sweep (4000 ticks, 3 seeds; deterministic
figures as of Ω-0.33): **off** → self 0.14, 3.9×, novelty 0.49 (the ceiling); **strength 0.25–0.75** →
self ≈ **0.56** (**~4.1× the off baseline**, decisively past the exp028 self ≤ 0.28 ceiling; ~3.4–4.3×
null), novelty ~0.22 — the **collective "both corner": strong reproducible heredity AND
open-endedness at once**; full (1.0) → self 0.61, still open (~0.21). *(The originally reported
"8–9× null / full-pinning-closes-the-world" was partly a `PYTHONHASHSEED` artifact — see Ω-0.33; the
both-corner claim stands, on absolute self.)*

**The ceiling was never a hard wall — it was the exp029↔030 open-vs-reproducible trade-off one level
up, and it yields to the same fix: partial, modular transmission.** Full transmission reproduces
perfectly but closes; none stays open but can't reproduce; the intermediate is the both corner.
Honest scope: the channel is *developmental/ecological* (partial re-provisioning), not purely genetic,
and staying-open is seed-variable around strength ≈ 0.25–0.75 (heredity-breaking is robust). This
removes exp039's blocker and makes the arc's final question testable: with heredity strong and the
world still open, **does competence now compound?** → exp041.

---

## Milestone Ω-0.26 — Coherence is selectable and emergent — but single-objective selection trades off (exp038)

**Date:** 2026-07-13 · **Status:** complete · **Verdict:** a positive with an honest negative.
Third rung of the self-improvement roadmap. Detail: `studies/EXP038_FINDINGS.md`. Gated;
exp001–035 byte-identical (55 tests green).

exp037 showed evolvable architecture amplifies *whatever* is selected (Goodhart toward openness).
exp038 tries a better-aligned, **emergent** target: **autocatalytic closure** — the self-producing
fraction of a deme's cross-production network (a class both produced-by and itself-a-producer: a
self-maintaining loop), read off the real network, not imposed (contrast exp021's coop bit).
Result (6000 ticks, 3 seeds): (1) **coherence is selectable** — `deme_fitness="closure"` raises
closure 0.064 > network 0.046 > size 0.028 (clean ordering); an emergent collective property
selection can grip. (2) **But it trades off against heredity** — closure-selected demes have
collective heredity self 0.102 vs 0.209 under direct network selection. Closure (short
self-maintaining loops) and heredity (faithful reproduction of the whole network) are **competing
axes**; a single scalar fitness buys one by spending the other.

**The design constraint this exposes:** alignment is **multi-objective**. Every single proxy tried
now Goodharts — network → runaway openness (exp037), closure → low heredity (exp038). A
self-improving collective needs closure AND heredity AND intrinsic function *at once*, and no
scalar fitness yields the package. So the churn/short-life fix is **not** achieved by closure
selection alone; it needs combined, aligned selection — which is exactly what the capstone
(exp039/040) must confront: whether a *combined* objective plus exp037's per-collective evolvable
state produces collectives that compound rather than trade off.

---

## Milestone Ω-0.25 — Per-collective evolvable internal state: architecture *can* now evolve (exp037)

**Date:** 2026-07-13 · **Status:** complete · **Verdict:** a **weak positive** — the engine piece
exp036 said was missing is now present and works. Second rung of the self-improvement roadmap.
Detail: `studies/EXP037_FINDINGS.md`. Gated; exp001–035 byte-identical (54 tests green).

exp036 hit the third wall (you cannot select for what a collective cannot represent). exp037
supplies representation: each deme carries a **heritable, mutable construction rule of its own** —
its `type_resolution`, made first-class *per collective* (exp033 made physics first-class per
*level*) — used in its own compositions and transmitted (with mutation) to the demes it founds.
Result (6000 ticks, 3 seeds): with a selection channel the population's mean per-deme resolution
**moves** (treatment 3.5 → 4.14) while a no-selection control stays put (3.03) — a +1.11 gap. So a
collective can now carry heritable internal state that **selection acts on** — exactly what exp036
could not do.

**Two honest edges** that matter as much as the result: (i) the selection signal on architecture is
**weak and noisy** (a ~1-point drift, not a sharp optimum) — consistent with the exp028 heredity
ceiling; (ii) it evolves toward the **fitness proxy's extreme** (high resolution → runaway
openness), not the heredity "both corner" — evolvable architecture faithfully **amplifies whatever
is selected** (Goodhart). So engine piece #2 is necessary and now present, but turning it into
self-improvement needs **stronger collective heredity** (so selection bites) and a **better-aligned
target** (so it improves toward coherence, not proxy-gaming) — the next rung, exp038 (coherence /
autocatalytic closure).

---

## Milestone Ω-0.24 — Intrinsic function: selection for anticipation is *not enough* (exp036)

**Date:** 2026-07-13 · **Status:** complete · **Verdict:** a **negative-with-diagnosis**, and the
sharpest statement yet of what stands between Ω collectives and minds. First rung of the
self-improvement roadmap. Detail: `studies/EXP036_FINDINGS.md`. Gated; exp001–035 byte-identical
(53 tests green).

The discussion on evolving self-improving agents flagged that the usual levers (heredity, memory,
architecture) are *amplifiers* of whatever is selected, and that two **engine** pieces are missing:
(1) a reason for computation to be selected, and (2) a substrate that can *represent* it. exp036
tests (1) in isolation: give the environment a regularity worth predicting — a **cyclic feed**
whose favoured atom-band rotates each `feed_period` ticks — and select demes for **anticipation**
(products matching the *next* season). Matched controls isolate cause (cyclic+network; random+
anticipation). Result (4000 ticks, 3 seeds): the cyclic environment is weakly **tracked**
(reactivity: P(current band) 0.272 vs 0.245 random, +0.022), but **anticipation does not evolve** —
treat's P(next band) is −0.005 vs the network control and only +0.019 vs chance (the reactivity
bleed), robust across `feed_period` ∈ {80,150,300}.

**The third wall.** You cannot select for what the substrate cannot represent. A deme can be
reactive (products reflect what is currently fed) but not anticipatory, because a collective has
**no internal state that represents environmental timing** — no clock, no phase memory, no variable
it could set now to pay off later. With nothing to vary, selection has nothing to act on. This is
the same lesson as exp010 (a replicator needs von Neumann self-reference the substrate lacks) and
exp011 (function must be intrinsic, not bolted on): **intrinsic function needs a substrate that can
hold predictive state, not merely a fitness that rewards it.** So engine piece (1) is inert without
engine piece (2) — motivating exp037 (per-collective evolvable internal state / memory).

---

## Milestone Ω-0.23 — The world gains geography and a hand: space + interaction (`omega/world/`, v2)

**Date:** 2026-07-13 · **Status:** capability · **Verdict:** the watchable world (Ω-0.22) becomes
**spatial and steerable**, both gated so exp001–035 stay byte-identical (52 tests green). Detail:
`omega/docs/WORLD.md`.

**Space.** The kernel stays spaceless; space is imposed as *a constraint on which organizations
react* (the README's own rule), grown from the deme/patch structure: patches on a W×H torus,
migration to neighbours only, and extinct patches recolonized from *nearby* survivors (a steep
`0.25^dist` kernel). The dashboard renders a **world map** (cell = patch, hue = dominant lifeform,
brightness = population) with real spatial heterogeneity. *Honest finding:* class-level
isolation-by-distance is **weak** — the world's open-ended novelty differentiates every patch
regardless of proximity, so open-endedness actively works against class-level biogeography.
Geography lives in local migration/founding and per-patch heterogeneity, not class overlap.

**Interaction.** `World` exposes conservation-respecting perturbations — `seed_life`, `shock`
(mass extinction), `set_law` (tune `mut_prob`/`horizontal_transfer`/`reify_period`/`mig_rate`/
`decay_hazard` live), `reify_now` — surfaced on the dashboard as a "reach in" panel via a
`POST /act` endpoint applied between chunks. Each is appended to a checkpointed **replay log**; a
touched world is no longer seed-deterministic (by design), an untouched one still is. The only
follow-on left is embodied agent minds on top of this spatial, steerable world.

---

## Milestone Ω-0.22 — The living world: the engine turned into a persistent, watchable world (`omega/world/`)

**Date:** 2026-07-13 · **Status:** capability (not a scientific claim) · **Verdict:** the
research engine now runs as a **persistent, watchable world** — forever, at flat memory, with
checkpoint/resume — reusing the confirmed ingredients as one live configuration. Detail:
`omega/docs/WORLD.md`. Gated; exp001–035 byte-identical (48 tests green).

Ω's result is what most virtual worlds lack: self-generating, open-ended content with nothing
hand-authored. This packages that generative core as a world. A registered **`world`** physics
composes the confirmed pieces on one substrate — the both-corner (Ω-0.15) + collective
individuals + **reification** (continuing construction, Ω-0.20) + **culture** (Ω-0.16). A
**`World`** runtime (`omega/world/runtime.py`) advances it in chunks indefinitely with
bounded memory (Ω-0.21) always on; **checkpoint/resume** (`omega/world/checkpoint.py`, via the
new `Noise.getstate/setstate`) makes a world survive restarts and accrete history —
*resume-then-continue == run-through*, byte-identical. An **Observer** (`omega/world/observe.py`)
makes it legible: the **novelty pulse** (open-endedness made visible), named **lifeforms**
(persistent classes with real ages), transient **collectives** (network communities), culture,
the growing constructed alphabet, and an event feed. A pure-stdlib **dashboard**
(`omega/world/dashboard.py`) serves it live in a browser (`http.server`) or the terminal, and
writes self-contained HTML snapshots. Scope is the *watchable* foundation; interaction, spatial
geography, and embodied agents are the follow-ons it enables.

---

## Milestone Ω-0.21 — Scaling infrastructure: lifting the in-miniature cap (bounded memory + 3× faster kernel)

**Date:** 2026-07-12 · **Status:** infrastructure (no new scientific claim) · **Verdict:** the
three limits that kept every open-endedness result *in miniature* are lifted, gated so
exp001–035 stay byte-identical. Detail: `studies/SCALING.md`.

The verdict after Ω-0.20 named the gap: horizons ≤ 250k, few seeds, because (1) the class
registry + provenance relations grew O(ticks) → OOM at 10⁶ ticks, (2) `canonical_cls`/`depth`
were re-hashed 4×/tick on persistent state, and (3) `amplification()` rescanned every class
ever. Fixes: a **bounded-memory long-run mode** (`Universe.memory_horizon`/`relation_cap`,
default 0 = byte-identical) that evicts cold class records — decoupled from novelty via a
monotonic `classes_ever_seen` counter so the novelty *count* stays exact (bounded novelty is a
*horizon-windowed* rate, higher than unbounded, so bounded runs compare bounded-to-bounded);
and **memoizing** the pure state functions (`organization.py`, bounded LRU). Measured: registry
flat and peak RAM 70 → 10 MB at 12k ticks (gap grows with horizon), and **5.28 → 1.71 ms/tick
(3.1× faster)** — a 10⁶-tick run drops from ~90 min-and-OOM to ~28 min at flat memory. This
unblocks the campaign (10⁶-tick, multi-seed, deeper towers) that moves the unboundedness claims
from *in miniature* toward the program's original goal. Still open: optimizing the `normalize`
reduction engine (the dominant raw cost) and checkpoint/resume for multi-hour runs.

---

## Milestone Ω-0.20 — Sustained novelty needs *continuing* construction, not a bigger fixed alphabet (exp034, 250k ticks)

**Date:** 2026-07-12 · **Status:** complete · **Verdict:** the sharpest form of the founding
thesis. Ω-0.19 showed in-run reification sustains the novelty rate; this asks whether a
*one-time* alphabet enlargement suffices or whether construction must **keep running**. A
three-arm long-horizon run answers decisively: **only continuing construction sustains
novelty.** Detail: `studies/EXP034_FINDINGS.md`.

### The three arms (250k ticks, seed 0, 10 windows of 25k)
- **baseline** (exp030, never constructs): novelty rate 0.33 → 0.15, late/early **0.51** — halves.
- **capped** (exp034, low cap 64, alphabet freezes ~16k ticks): 0.42 → 0.25, late/early **0.67**
  — once the alphabet stops growing, the rate **resumes decaying**. A one-time construction
  bump *delays* but does not stop closure.
- **uncapped** (exp034, grows to 531 atoms / 499 reified): 0.64 → **0.80**, late/early **1.16**
  — flat to rising across every window, collective heredity alive throughout (self ≈ 0.085 ≫
  null ≈ 0.015).

### What it means
Constructibility is a **rate, not a stock**. The capped arm has a permanently *enlarged* fixed
alphabet and still closes; only the arm that keeps reifying stays open. So "infinite
constructibility, not infinite space" (Ω-0.1) sharpens to: open-endedness is sustained by the
**ongoing act of construction**, not by any fixed amount of it, however large. This is the
cleanest statement of the program's thesis to date, and it is a *falsifiable* one — the capped
arm is the matched control that shows a bigger fixed space is not enough.

### Is / is not
- **Is:** a decisive separation of one-time vs continuing construction — the capped/baseline
  arms are matched controls (stops / never), the uncapped arm holds its rate; heredity intact.
- **Is not:** a literal 10⁶-tick run (genuinely open-ended novelty grows the class registry
  ~unboundedly → memory-bound on a 16GB box; the early-filling cap puts the decisive post-cap
  regime inside a feasible 250k horizon), nor multi-seed (one deep trajectory). Whether the
  uncapped rate holds across 10⁶⁺ ticks, and the cost of unbounded alphabet growth, remain open.

---

## Milestone Ω-0.19 — The two open frontiers, closed: sustained novelty (reification) and a substrate-general both corner (exp034, exp035)

**Date:** 2026-07-11 · **Status:** complete · **Verdict:** the two frontiers Ω-0.17/0.18
handed forward are both answered. **(exp034)** The novelty-rate decay left open by Ω-0.17 is
*eliminated* by turning the constructibility lever on within a level — growing the atom
alphabet during the run holds the novelty rate flat while heredity stays alive. **(exp035)** A
genuinely new composition law (binary-tree grafting, outside the type-substrate family)
reaches the both corner and recurses in the tower — so what a level needs is the both-corner
*condition*, not a specific engine. Detail: `studies/EXP034_FINDINGS.md`,
`studies/EXP035_FINDINGS.md`. Both gated; exp001–033 byte-identical.

### exp034 — sustained novelty via in-level reification (the founding thesis, confirmed)
Ω-0.17's honest edge was that the both-corner's novelty *rate* drifts down over a long horizon
because its atom alphabet is fixed. exp034 applies the Ω-0.1 constructibility lever *inside*
the collective substrate: every 500 ticks the most common recent product motif is promoted to
a new atom (grows `self.atoms` during the run; no RNG → `reify_period=0` byte-identical). Over
30k ticks, 3 seeds: the fixed-alphabet **baseline** novelty rate decays 0.52 → 0.27 (late/early
ratio **0.53**, roughly halving), while the **reifying** run goes 0.53 → **0.67** (ratio
**1.11** — flat to rising, no decay; **2.38× the baseline** late), the alphabet grows 32 → 91
atoms (59 motifs reified), and collective heredity stays alive every window (self ≈ 4–5× null).
So the decay was **not** intrinsic to the deme dynamics — it was the fixed alphabet. Growing
*constructibility* (not space) sustains the novelty rate: "infinite constructibility, not
infinite space" (Ω-0.1), now shown at the collective level, at the place it was most in doubt.

### exp035 — a new level law: the both corner is substrate-general
Ω-0.18 crossed physics boundaries among three *type* substrates and found the hard requirement
is the both corner. exp035 adds a law unlike all three — organizations are binary **trees**,
composition grafts them into a node `(f,x)` with a depth cap (the branching analogue of path
truncation). It **reaches the both corner** (self > null with novelty > 0 at every resolution,
a closed↔open dial like typed_path) and **recurses in the tower** (a path↔tree tower reaches
the same depth as the homogeneous one, 6/6 path/tree boundaries survived). So a level needs the
both-corner *property*, not a particular law. Honest qualifier: the tree law's heredity is an
**order of magnitude weaker** than linear paths (self ~0.03–0.05 vs ~0.35) — the condition
generalizes, but linear concatenation is a specially strong instance, so a level's *law* still
sets the *quality* of individuality it attains.

### Is / is not
- **Is:** the Ω-0.17 novelty-decay edge closed (reification sustains the rate); the Ω-0.18
  first-class-levels result generalized beyond the type-substrate family (a genuinely new law
  works). The founding constructibility thesis confirmed at the collective level.
- **Is not:** a proof that reification sustains novelty *forever* (30k ticks, alphabet capped
  at 256; the 10⁶-tick behaviour and any late cost of unbounded alphabet growth are open), nor
  that all open+modular laws are equally good (tree heredity is weak). A fully heterogeneous
  *per-level-physics* tower with strong non-type laws remains the standing ambition.

---

## Milestone Ω-0.17 — Unboundedness, tested at scale: sustained within a level, no depth ceiling of levels (exp032)

**Date:** 2026-07-11 · **Status:** complete · **Verdict:** the program's original open
question — **unboundedness** — comes out **affirmative in miniature on both axes**, with the
honest edges named. Within a level the "both corner" is *sustained* (not a transient) to
120k ticks; the level tower shows **no intrinsic depth ceiling** up to 15 tiers. Detail:
`studies/EXP032_FINDINGS.md`. Analysis-only on the existing engine (one gated harness hook,
`record_stride`, to bound memory); exp001–031 stay byte-identical.

### Why this milestone
Every result before this was a bounded-horizon burst (400–4000 ticks); the log kept flagging
that the OEI falsification test had **never been run at long horizon**, exactly where the
program's two past false positives (exp003 cumulative counter, exp005 fix) lived. exp032
runs it, with the guardrails mandatory: **rates in temporal windows, not cumulatives; matched
controls; honest verdict either way.**

### Within a level — sustained (exp030 both corner, 40k×3 seeds + one 120k stretch)
Against a matched **closed** control (exp029, novelty→0): the open corner keeps novelty rate
**> 0 in every window** (0.27–0.58 at 40k) while the closed control collapses to **exactly
0.000** from window 1; collective heredity stays **self ≫ null (≈4–5×), flat**, across 40k
and out to **120k** (39 788 heredity events, 34 274 classes discovered), with stable
population (no collapse). **Heredity is the robust half — no erosion.** The one honest edge:
the novelty *rate* drifts down over the 120k stretch (~0.45→~0.16); it stays firmly above the
closed zero (open-vs-closed is decisive), but whether it holds a **positive floor** or is a
very slow dilution is **still not settled even at 120k** (the same asymptote caveat as Ω-0.2).
Absolute self-Jaccard is also lower in the sustained large-network regime (~0.085) than in the
short-horizon burst (~0.25) — the heritability *signal* persists though its magnitude shrinks
as networks grow.

### Of levels — no ceiling found (tower depth, 2500 ticks/tier)
Lifting the tier cap: a `max_tiers=15` tower **climbs to the full 15** whenever it survives
its early tiers, with a **self-sustaining ~fixed-point alphabet** — collectives/tier ≈ 23–24
*undiminished from tier 1 to 14*, self > null and novelty 0.49–0.60 at every tier. A base
sweep confirms depth is set by the **cap, not the base**: **8 of 9 seeds reach the cap**
across base ∈ {16, 32, 64}. So the promotion map has an attractor that keeps the alphabet
from starving — **depth is compute-limited, not ceiling-limited**, the strongest
open-endedness-*of-levels* evidence so far. Honest edge: a **stochastic early-tier failure**
(~1 seed in 3: deep [15,**0**], base-32 [8,**0**,8]) can abort a tower before it starts —
tower formation is per-seed stochastic, though conditional on surviving tier 0 it climbs to
whatever cap it is given.

### Is / is not
- **Is:** the sustained-horizon unboundedness test, run at last — collective heredity
  demonstrably persists (self ≫ null to 120k) and novelty stays open (vs a closed control's
  exact zero), and the recursive tower has no intrinsic depth ceiling up to 15.
- **Is not:** a proof of a *strictly non-decaying* novelty rate (the 120k rate drifts down;
  positive-floor vs slow-dilution unresolved), nor a guarantee that a tower forms on every
  seed (early-tier stochastic failure). Unbounded-in-principle is evidenced; unbounded-forever
  would need horizons beyond 120k and a resolved novelty-rate asymptote.

---

## Milestone Ω-0.16 — Multiple levels of organization: the transition recurses (exp031)

**Date:** 2026-07-06 · **Status:** complete · **Verdict:** the major transition to
collective individuality is not a single jump but a **recursive ladder** — each tier's
stable, heritable collectives become the atoms of the next tier, building a
physics → chemistry → biology → culture tower on one engine; and a distinct **culture**
level (horizontal, Lamarckian transmission) sits on top. Detail: `studies/EXP031_FINDINGS.md`,
`omega/docs/LEVELS.md`. All gated → exp001–030 byte-identical.

### The recursion (a self-sustaining tower)
Ω-0.15 (exp030) showed a substrate that is both **modular** and **open-ended** lets a
collective be heritable *and* open-ended at once. Because that condition is not specific
to one level, it should hold *again* if a tier's collectives become the next tier's
individuals. `omega/levels/stack.py` tests this: run the exp030 `typed_path` substrate;
promote each stable heritable collective (a deme with a non-trivial network signature) to
a fresh symbol; make that set the next tier's alphabet; recurse. Result (up to 5 tiers, 5
seeds): **tower depth mean 4.0, max 5, full 5-level stack in 4/5 seeds**, with *every*
tier forming heritable collectives (`self > null`) and staying open-ended (novelty
0.41–0.47, undiminished up the tower). Chemistry → biology → culture → meta-culture emerge
as successive tiers of one recursive engine, with explicit nesting (a high-tier individual
unfolds to the organizations it contains). **Tower depth** is a new open-endedness axis —
open-endedness *of levels*, complementary to within-level novelty.

### The culture level (a qualitatively distinct top tier)
Lower tiers transmit *vertically* (propagule → offspring). Culture is *horizontal and
Lamarckian*: a collective imitates a fitter collective's top motif within its lifetime
(`horizontal_transfer`), decoupled from reproduction. With transfer on, a substantial
horizontal channel opens (~0.68× the vertical rate) and — the signature of culture — it
**accelerates innovation**: novelty rises 0.41 → 0.57 and distinct collective signatures
13.5 → 17.0, as imported motifs recombine with each recipient's own faster than
reproduction could.

### Is / is not
- **Is:** multiple levels of organization, in miniature — a 4–5 deep recursive tower each
  tier heritable and open-ended, plus a distinct horizontal/cultural apex; the level
  abstraction made first-class (`omega/levels/`, `omega/docs/LEVELS.md`).
- **Is not:** proven **unbounded** (does depth grow without limit over 10⁵⁺ ticks?), nor
  fully heterogeneous per-level physics (the tower is the self-similar typed_path engine
  with culture layered on). The program's original unboundedness question now recurs at
  every level.

---

## Milestone Ω-0.15 — The collective-individuation arc: from inert machinery to a completed transition (exp018→exp030)

**Date:** 2026-07-06 · **Status:** complete · **Verdict:** a major transition to
collective individuality is achievable *in miniature* — collectives that are
heritable, selectable, and reproducible in an open-ended world — once the substrate
is both **modular** and **open-ended**. Collective selection was never the
bottleneck; the substrate was. Full detail per experiment in `studies/EXP0NN_FINDINGS.md`
and the synthesis `studies/COLLECTIVE_INDIVIDUATION_ARC.md`; all changes are gated so
exp001–017 stay byte-identical.

### Phase 1 — the multi-level machinery is inert on its own (exp018–020)
Extending exp017's deme reproduction (source = collective heredity vs a well-mixed
`mixed` null): adding heritable between-deme **fitness variance** (exp018), a
**patch-local feed** (exp019), and an explicit strong **replicase** (exp020) each
failed to make selection act on the collective. In every case `source` ≈ `mixed`; the
only diversity drops were population collapse, and strong replicators won *as
individuals* (colonizing every deme). **Diagnosis:** nothing group-selectable emerges
— every between-deme trait is individual-level.

### Phase 2 — supply a group trait; find what individuation needs (exp021–024)
An *imposed* cooperation trait (individually costly, collectively beneficial) makes
group selection work — textbook Price/Hamilton (exp021) — proving the machinery is
sound and the trait was missing. An *emergent* group trait, a deme's internal
**cross-production network**, is genuinely heritable and selectable (exp022). Niche
construction (recycling a deme's own products as feed) first lifts within-deme
dominance but homogenizes globally (exp023). Combining every lever plus forced
monoculture founding still does not individuate demes, and reveals a **substrate
type-space wall**: small SKI expressions reduce to only ~9 attractor normal forms, so
24 demes cannot hold distinct identities (exp024).

### Phase 3 — represent identity right, then fix the substrate (exp025–030)
Defining a deme's identity as its **network signature** (edge-set) rather than a
dominant class is more heritable and richer (exp025) — part of the "missing"
individuation was a measurement artefact. A richer *interacting* combinator basis
(B/C/W; inert data atoms were rejected — they kill cross-production) lifts heredity
1.6×→2.4× with novelty rising (exp026); a dose-response over the basis (3→11
combinators) finds a **Goldilocks optimum** ~3.3× that then declines as too-rich a
type space stops networks breeding true (exp027). The ceiling is **substrate-limited,
not transmission-limited**: a network-biased propagule that transmits the *whole*
source deme still caps at ~3× (exp028) — given identical members, combinator reduction
does not re-form the same network. Pivoting to a **typed substrate** (morphisms +
modular composition) makes networks reproducible (self 0.10→0.24, ~5×) but **closes**
the world (novelty→0) — the two substrates are opposite corners of one trade-off
(exp029). Finally, an **open-ended AND modular** substrate — variable-length type
**paths** composed by concatenation, with a tunable identity resolution — reaches the
**"both" corner** (exp030): strong reproducible collective heredity (self 0.22–0.28)
*and* sustained novelty (0.1–0.4 > 0) *and* rich networks (cross-production 4–7),
which neither pure substrate could.

### The deep result
The transition needs a collective phenotype that is at once **heritable** (so selection
can act on it) and **open-ended** (so the world does not close). On the combinator
substrate networks are open-ended but unreproducible; on the pure typed substrate they
are reproducible but closed. Modular *and* open-ended composition (path-morphisms with
bounded resolution) satisfies both — the heredity-vs-diversity tension (Ω-0.14) becomes
*graded* rather than *absolute*, and a heritable collective individual coexists with an
open-ended world.

### Is / is not
- **Is:** a completed major transition to collective individuality, *in miniature* —
  demes as heritable, selectable, reproducible collective individuals with open-ended
  novelty; the substrate condition (modular + open-ended) that makes it possible,
  precisely located and dialable.
- **Is not:** proven **unbounded** — that collective heredity *and* novelty both persist
  over 10⁵⁺ ticks and many seeds at the "both" corner is untested; nor a *transition of
  transitions* (collective individuals composing into a further level). This is the
  frontier the arc hands forward — the program's original unboundedness question, now at
  a higher level of organization.

---

## Milestone Ω-0.14 — A major transition, in miniature: selection acts on the collective

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** collective-level
selection is demonstrated once collective *reproduction fidelity* is high enough —
the onset of a major evolutionary transition, contingent (and modest), not
automatic.

### The question and the mechanism (exp017)

With obligate collectives occupying demes (Ω-0.13), does selection act on the
*collective*? Made demes **reproduce**: every `deme_gen` ticks a fraction go
extinct and are recolonized by a **propagule** copied from a surviving deme
(chosen by productivity, so fitter collectives found more). The null,
`propagule_mode="mixed"`, recolonizes from a well-mixed pool, destroying collective
heredity. Signature of collective selection: the number of distinct **deme types**
(each deme's dominant class) should *winnow* under heredity but not under the null.

### The path — three findings, not one

1. **First pass: null.** In the standard regime the deme-type count did not winnow
   (source ≈ mixed, ~19–20 of 24). Two parameter regimes, same flat result.
2. **Direct heredity measure (the diagnosis).** Do founded demes resemble their
   *source* (class-set Jaccard) more than a random deme? Barely: ratio **1.2×**,
   absolute overlap ~0.03. Collective heredity was real but far too weak to select
   on. Suspect: the random **feed** floods each child deme and washes out the
   propagule's signature.
3. **Confirm and fix.** Cutting the feed strengthened heredity monotonically —
   ratio **1.2 → 1.5 → 3.4** as `feed_rate` dropped 14 → 6 → 2. Feed dilution *was*
   the bottleneck. (Trade-off: low feed also thins diversity, 66 → 15 lineages.)

### The payoff (seed 0, 2500 t, low feed → strong heredity)

| mode | deme types early → late | heredity ratio | lineages |
|------|:---:|:---:|:---:|
| source (heredity) | 16.4 → **15.2** (winnows) | 3.21 | 39 |
| mixed (null) | 15.4 → **17.8** (drifts up) | 0.00 | 41 |

Under collective heredity the between-deme diversity **winnows** (fitter collectives
spread across demes); under the no-heredity null it **drifts upward**. The two move
in *opposite directions* — a null-controlled signature that **selection is now
acting on the collective as a unit.** And it coexists with continued open-ended
evolution (39 lineages) — both levels at once.

### What this is, and what it is not

* **Is:** the onset of collective-level (multi-level) selection — the defining
  feature of a major evolutionary transition to higher-level individuality —
  demonstrated against a matched heredity-free null.
* **Is not:** a completed transition. The winnowing is *modest* (Δ ≈ 2.6 deme
  types, not a collapse to one collective), single-seed, and **parameter-contingent
  on a Goldilocks regime** (low feed for heredity vs high feed for diversity). It is
  an onset, not a new stable individual.

### The deep result

The program has now surfaced the central tension of major transitions in this
substrate: **collective heredity requires high-fidelity reproduction (low feed),
which trades off against the feed that sustains open-ended diversity.** A full
transition needs a substrate where collectives self-sustain *without* a diluting
global feed — the concrete design target the next arc inherits.

### Honest limitations

* Single seed; modest effect; requires a tuned low-feed regime.
* The deme-type metric (dominant class) is noisy — the *direct* heredity ratio
  (3.2×) is the cleaner evidence that the precondition is met.
* Productivity-weighted source selection is a designed group-fitness; whether
  collective fitness would emerge *without* that scaffold is untested.

### Next steps

* **Self-sustaining demes:** replace the global feed with per-deme recycling so a
  deme's material comes from its own decayed members — heredity without the
  diversity cost, potentially both open-endedness *and* a full transition.
* **Map the (feed × migration × deme-size) regime** where winnowing is strongest,
  and confirm across seeds.
* **Watch for a new "individual":** once collectives reproduce true, do they begin
  to vary and accumulate collective-level adaptations — evolution *of* collectives?

---

## Milestone Ω-0.13 — Locality makes hypercycles OBLIGATE (organizations made of organizations)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the Ω-0.12 redundancy
diagnosis was correct and its predicted fix works — reducing production redundancy
by spatial locality turns topological cycles into **functionally obligate
hypercycles**, a genuine higher level of organization.

### The prediction

Ω-0.12 found hypercycles robust to knockout *because* the well-mixed soup is
densely connected — every product has many alternative producers, so no member is
essential. Prediction: partition the soup into demes so application only happens
*within* a patch; then each class has few local producers, redundancy falls, and a
member's removal should actually collapse its partners.

### The mechanism (exp016)

`CombinatorPhysics(n_patches=P)` assigns each organization to one of P patches; an
apply reaction only pairs organizations in the *same* patch. A product inherits its
function-parent's patch; feed lands randomly; a small `mig_rate` lets organizations
hop patches so demes stay coupled. Nothing else changes.

### Result — a clean dose-response (seed 0, 1200 t)

The knockout of Ω-0.12, re-run across patch counts (suppress one member of the
strongest 3-cycle; measure partner survival vs a random-knockout null):

| n_patches | partner survival (member KO) | random-KO null | z |
|:---:|:---:|:---:|:---:|
| 0 (well-mixed) | 0.880 | 1.098 ± 0.124 | −1.8 |
| 12 | 0.817 | 1.070 ± 0.125 | −2.0 |
| 24 (strong locality) | **0.272** | 1.133 ± 0.024 | **−35.4** |

At 24 patches, removing one hypercycle member **collapses its partners to 27%** of
control, while random knockouts of matched-abundance classes leave those same
partners *above* baseline (113%). The effect is **specific** (the null rules out a
"small soup, everything is fragile" confound) and **monotonic** in locality.

### What this means

* **Obligate hypercycles emerge.** Under locality the 3-cycles are not statistical
  artefacts and not weakly-coupled — the members *depend on each other*: knock one
  out and its partners collapse. This is a genuine collective — an *organization
  built out of organizations*, self-sustaining as a unit — exactly the manifesto's
  "collective behavior" and Eigen's obligate hypercycle.
* **The redundancy hypothesis is confirmed.** The same cycles were robust when
  well-mixed and obligate when local; the only change was how many alternative
  producers each class had. Functional interdependence is a matter of *redundancy*,
  which locality controls.
* **Locality also protects diversity** — more coexisting self-catalytic lineages
  than the well-mixed soup (19 vs 9 at matched ticks), the classic spatial effect.
  So locality buys *both* diversity and higher-order organization.

### Honest limitations

* **Single seed.** The z at 24 patches is enormous (−35) and the effect size huge
  (0.27 vs 1.13), so the qualitative result is not fragile — but cross-seed and
  cross-cycle statistics are still owed.
* **Tight null inflates z.** The headline is the *effect size* (partners → 27%), not
  the z per se; the null variance at 24 patches is small.
* **Very small demes.** 24 patches over ~160 organizations is ~7 per deme; whether
  obligate hypercycles persist at larger deme sizes (more realistic) is untested —
  there is presumably a redundancy threshold.
* **Migration was fixed** at 0.02; the coupling/isolation trade-off (too much
  migration re-mixes and destroys obligacy; too little fragments the soup) is a
  dial not yet swept.

### Next steps

* **Locality sweep × mutation:** map where in (n_patches, mut_prob, mig_rate) space
  the system has *both* open-ended evolution *and* obligate collectives — the
  regime that matters for major transitions.
* **Multi-level selection:** with obligate collectives, ask whether selection now
  acts on the *collective* (a hypercycle out-reproducing another hypercycle) — the
  next rung: individuality at a higher level.
* **Cross-seed / cross-cycle** confirmation and a deme-size threshold for obligacy.

---

## Milestone Ω-0.12 — Knockout test: weak functional coupling, dominated by redundancy (not obligate collectives)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the over-represented
3-cycles are a real *topological* property with at most a *weak* functional
coupling — partners survive a member's removal, so they are **not** obligate
collectives, but the effect is small and methodology-sensitive rather than zero.

### The test

Ω-0.11 found 3-cycles massively over-represented (z=+12.3). Over-representation is
necessary but not sufficient for a *functional* hypercycle (Eigen): members must
actually *depend* on each other. Direct test — a **knockout**: identify the
strongest 3-cycle {i,j,k} (min-edge-weight 267), continuously suppress member i so
it can never exist or act, and measure the surviving production of its partners
j,k against a null of suppressing random matched-abundance non-members.

### Result (seed 0, 1500 t) — and its instructive instability

| suppression | partner (j,k) survival | random-KO null | z |
|-------------|:---:|:---:|:---:|
| partial (dissolve each tick only) | 0.943 | 1.096 ± 0.134 | −1.1 (NS) |
| full (also block re-feed/rebuild) | 0.919 | 1.088 ± 0.049 | −3.5 (sig) |

The two runs **bracket significance** — and that spread *is* the finding. The
robust facts across both: (a) partners **survive at ~92–94%** — no collapse; (b)
knocking out the hypercycle member pushes partner production *down* (~0.92–0.94)
while random knockouts push it slightly *up* (~1.09), a specific negative effect of
roughly 8–15%. Whether that clears 2σ depends on how tight the null is, which
itself varies run to run.

### What this means

* Ω-0.11's **topological** claim stands (reciprocity/3-cycles beat the null).
* The **functional** reading is *partial*, not obligate. There is a **weak, real
  functional coupling** — a member's removal specifically depresses its partners —
  but the partners are **redundantly produced** and largely survive. So these are
  neither coincidental triangles nor Eigen *organisms*; they are a **redundant web
  of individually-robust replicators with weak mutual dependence.**
* Robustness-through-redundancy is itself life-like (biological pathways tolerate
  knockouts). "Organizations made of organizations" in the *strong* (obligate)
  sense has **not** emerged; a *weak* version arguably has.

### Honest limitations

* **Borderline, methodology-sensitive.** The significance flips with suppression
  completeness and null variance — so the honest headline is "weak effect", not a
  confident yes or no.
* **Only the strongest (most redundant) hypercycle tested;** single seed; n=6 null;
  all-or-nothing knockout (a graded knockdown might resolve the weak coupling
  better).

### Next steps

* **Obligate collectives may need a substrate nudge:** spatial locality or a
  reduced connectivity (fewer apply attempts, so each product has fewer alternative
  producers) would lower redundancy and could let genuinely dependent hypercycles
  form. Test whether reducing pathway redundancy converts topological cycles into
  functional ones.
* **Division of labour / niches** via production-graph clustering remains the other
  open ecological question.

---

## Milestone Ω-0.11 — Ecology: mutualism and hypercycles emerge (and evolution enriches them)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the coexisting
replicators form a real interaction network — significant excess mutualism and
strongly over-represented hypercycles — enriched by open-ended evolution. No
parasites (an honest null with a mechanistic reason).

### The question and the method

Ω-0.10 gave a diversifying population of ~37 replicator lineages. Do they merely
coexist, or *interact*? The interaction network is the **cross-production graph**:
a directed edge i → j means "class i, acting as a function, produced class j"
(exp014 records it). Ecological claims are **null-tested** against a
degree-preserving configuration model — only structure in *excess* of the graph's
own degree distribution counts.

### Result (seed 0)

| condition | reciprocity (obs / null) | **z** | mutual pairs | 3-cycles | parasites | self-cat lineages |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| takeover (mut=0), 3000 t   | 0.042 / 0.027 | **+3.5** | 42 | 156 | 0 | 22 |
| evolution (mut=0.05), 3000 t | 0.059 / 0.032 | **+5.8** | 66 | 343 | 0 | 37 |

* **Mutualism is real and null-beating.** Reciprocal production (i → j *and*
  j → i — organizations that build each other) exceeds the degree-matched null by
  3.5–5.8σ. Open-ended evolution makes it *stronger* (z +5.8 vs +3.5, mutual pairs
  66 vs 42).
* **Hypercycles are strongly over-represented.** A separate null test of 3-cycles
  (i → j → k → i, Eigen's hypercycle motif) on the evolving graph: **142 observed
  vs 52 ± 7 null, z = +12.3.** These loops are not a by-product of graph size — they
  are genuine *topological* structure. Evolution roughly doubles their count (343 vs
  156). **⚠ Caveat added in Ω-0.12:** a knockout test shows these cycles are *not*
  functionally obligate — removing a member barely dents its partners (redundant
  production). "Collective autocatalysis" below should be read as topological
  motif, not self-sustaining organism.
* **No parasites** — and this is honest, not a detector failure. A Tierra-style
  parasite exploits a *host's shared execution machinery*; this substrate has none
  (each application is self-contained). The small combinators that get produced a
  lot are shared *infrastructure* (they are also productive *functions*), not
  freeloaders, so the produced≫produces-and-small signature never appears.

### What this establishes

The soup is not a bag of independent self-copiers. Its replicators form an
**interacting ecology**: mutual catalysis and hypercyclic loops, exactly the
"collective behavior" and hypercycle organization the manifesto anticipated (and
Eigen predicted for prebiotic replicator networks) — arising, again, from the
conditions rather than being implemented. And the structure is a *product of the
evolutionary dynamics*: every ecological measure is higher under mutation-driven
evolution than under bare takeover.

### Honest limitations

* **Single seed.** The z-scores are large (mutualism +5.8, hypercycles +12.3), so
  the qualitative result is robust, but no cross-seed error bars yet.
* **Reciprocity is a minority structure.** Absolute reciprocity is small (~0.06) —
  most production is *not* reciprocal. Mutualism is a significant *excess*, not the
  dominant mode.
* **Directionality of the enrichment isn't proven causal.** Evolution has both more
  nodes and stronger structure; the null controls for degree, but a fuller test
  would match graph size directly.
* **Hypercycle = 3-cycle in the production graph.** That is the standard motif, but
  whether these loops are *functionally* self-sustaining (a true hypercycle that
  would persist if isolated) is a stronger claim not yet tested by knockouts.

### Method additions

* `metrics/ecology.py`: cross-production graph builder, reciprocity with a
  configuration-model null, and a parasite detector.
* `CombinatorPhysics(track_ecology=True)` records the cross-production graph;
  registered as `exp014`.

### Next steps

* **Knockout tests** for genuine hypercycles: remove one member of a 3-cycle and
  check whether the others' production collapses (functional dependence, not just a
  topological triangle).
* **Multi-seed** ecology statistics and a mutation-rate dose-response of the
  ecological measures (does the Goldilocks band for evolution also maximise
  ecological structure?).
* **Toward niches/division of labour:** cluster the production graph and ask
  whether distinct functional guilds (specialist producers vs generalist
  infrastructure) separate — the next rung toward the manifesto's "ecological
  niches".

---

## Milestone Ω-0.10 — The synthesis: open-ended evolution (reproduction that keeps innovating)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the program's goal, in
miniature — a diverse, self-reproducing, continually-innovating population — is
demonstrated, with a classic error-threshold Goldilocks zone.

### The setup

Ω-0.9 gave reproduction but a *takeover*: one replicator dominated and diversity
collapsed. Evolution needs the third ingredient beside reproduction and selection:
**heritable variation**. exp013 adds *imperfect reduction* — with probability
`mut_prob` a product is point-mutated (one combinator atom changed) then
re-normalised. `mut_prob=0` recovers the Ω-0.9 takeover control.

### Result (3000 ticks, seed 0) — a Goldilocks zone

| mut_prob | distinct classes early → late | self-cat lineages | max self-cat | novelty |
|:---:|:---:|:---:|:---:|:---:|
| 0.00 | 113 → **89** (collapse) | 22 | 7545 (one monopolises) | 4.06 |
| 0.02 | 119 → **113** (held) | **33** | 654 | **8.64** |
| 0.05 | 114 → **112** (held) | **37** | 4634 | **8.47** |
| 0.10 | 117 → 96 (declining) | 40 | 2928 | 4.95 |

Reading the columns:

* **mut=0** — takeover. One replicator (max self-cat 7545) monopolises, diversity
  erodes (113→89), novelty is low (4.06). Reproduction *versus* open-endedness.
* **mut≈0.02–0.05 — the synthesis.** Diversity is *held* (≈112 late), the number of
  coexisting **replicator lineages grows** (22 → 33 → 37), *no single* replicator
  monopolises (max self-cat falls), and **novelty roughly doubles** (≈8.5). A
  diverse population of self-reproducers that keeps generating new ones — this is
  reproduction *and* open-endedness at once.
* **mut=0.10 — error catastrophe.** Too much variation degrades replication
  fidelity: novelty falls back (4.95) and diversity starts collapsing again. This
  is Eigen's error threshold appearing unbidden — a hallmark of real evolutionary
  dynamics, not something coded in.

### Why this matters

The two halves that Ω-0.9 left in tension are now reconciled in one substrate:
**reproduction (self-catalysis) + heritable variation (mutation) + selection
(reservoir competition) → a sustained, diversifying population of replicators.**
That is open-ended evolution in miniature, and it is exactly the target the whole
program was built to reach — arrived at not by implementing evolution but by
implementing the *conditions* (a behaviour-first substrate, a resource gradient,
imperfect copying) and letting it happen. The error-threshold Goldilocks zone is
the strongest evidence it is genuine: the same knob, pushed too far, breaks it in
the way real evolutionary systems break.

### Honest limitations

* **Single seed** (the dose-response monotonicity and the mut=0 collapse vs mut>0
  hold-and-diversify contrast are clear, but no error bars yet).
* **"Sustained" = 3000 ticks**, not proven unbounded. Whether the replicator
  lineage count keeps climbing over 10⁵⁺ ticks — true unbounded open-ended
  evolution — is untested.
* **Novelty is combinator-expression novelty.** That self-cat *lineages* multiply
  (22→37) argues for diversification of replicator *function*, not mere drift, but
  a richer "is this ecologically interesting" analysis (functional guilds,
  parasites, cooperation) is future work.
* **A tuned regime, not automatic.** Open-ended evolution appears in a Goldilocks
  band, not at every mutation rate.

### Next steps

* **Multi-seed + longer horizons**, and track whether self-cat lineage count keeps
  growing (unbounded evolution) or saturates.
* **Ecology.** Look for interaction structure among replicators — parasites (short
  replicators exploiting long ones), cooperation, hypercycles — the next rung
  toward the manifesto's "ecological niches" and "collective behavior".
* **Re-open the old walls on the evolving substrate.** With replicators that have
  *function*, do reusable deep modules and cumulative innovation finally appear as
  *selected* traits rather than fed ones?

---

## Milestone Ω-0.9 — Behavior-first substrate: self-replication emerges (the copying wall breaks)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the copying wall is
**broken** by a substrate pivot; genuine self-replicators emerge — the program's
first crossing from construction into reproduction.

### The reasoning that forced a pivot

Three form-based experiments failed in a row: deep primitives stay terminal
(Ω-0.7 exp009), copying does not emerge (Ω-0.7 exp010), and functional selection
is marginal (Ω-0.8 exp011 — coupling operator persistence to activity or even to
*generativity* barely moved novelty/discovery: the substrate's open-endedness is
form-driven and operator selection is second-order). Together they say the same
thing: **you cannot reach function or reproduction by bolting selection onto a
substrate where behaviour is optional.** So, per Ω's authority to abandon an
approach, the *substrate* changed, not an add-on.

### The substrate (exp012)

An organization *is a function*: an **SKI-combinator expression**. Its identity is
its **behaviour** — the normal form it reduces to — not its written form.
Interaction is **application**: *f* applied to *x* yields `normalize(f x)`. The
whole of physics is three rules: `I x→x`, `K x y→x`, `S x y z→x z (y z)`. The **S**
rule *duplicates* — which is precisely why copying is an *attractor* here and was
an impossible quine in the string soup. Conservation is untouched: a reduction that
grows the expression pays the extra distinguishability from the reservoir, so
**reproduction is resource-limited** (replicators compete for free quanta — that is
the selection).

### Result — self-replication emerges (seed 0)

Detector: a class is a genuine replicator (not a mere convergence attractor) if
`(C x) → C` — applying it reproduces it (`max_selfcat` counts such events).

| substrate | amplification | dominance | **self-catalysis events** | replicator classes | distinct classes |
|-----------|:---:|:---:|:---:|:---:|:---:|
| string soup (exp010) | 16 | 0.032 | **0** | **0** | 201 |
| combinator, 1500 t | 1,564 | 0.103 | **1,344** | 16 | 93 |
| combinator, 3000 t | 8,982 | 0.140 | **7,218** | 21 | 73 |

The string soup produced **zero** self-catalysis, ever — structurally impossible
there. The combinator soup produces genuine self-replicators, thousands of events
across ~20 lineages, with amplification growing 100–500× and rising. A concrete
emergent replicator, captured live and non-trivial (my hand-guessed candidates
like `K K` do *not* self-replicate — these were discovered by the dynamics):

    ((S (K ((S S) K))) (K (K ((S S) K))))      — size 10, (C x) → C

This is the AlChemy result reproduced inside Ω, and the program's first genuine
**reproduction**: organizations that cause their own rebuilding, selected by a
resource gradient rather than by any hand-coded fitness.

### The new wall it reveals: reproduction vs open-endedness

Look at the last column: distinct classes **collapse** (201 → 93 → 73) as the
replicators take over. Reproduction here is *in tension with* open-ended novelty —
a successful replicator homogenises the soup, out-competing the diverse random
expressions for reservoir quanta. So the two halves of the goal are now both
demonstrated **but in different substrates and pulling against each other**:

* string/reification substrate → open-ended **construction**, no reproduction;
* combinator substrate → **reproduction**, but collapsing diversity.

Open-ended *evolution* — reproduction that keeps generating novelty rather than
converging — is neither, and is the synthesis the next arc must chase.

### Honest limitations

* **Diversity collapse.** The current combinator soup converges toward a few
  replicators; it is not open-ended. Whether mutation (imperfect reduction) +
  resource structure can turn takeover into open-ended evolution is untested.
* **Single seed.** The string-vs-combinator contrast is stark (0 vs thousands of
  self-catalysis events) so the qualitative result is robust, but effect sizes
  across seeds are not yet aggregated.
* **Non-termination handling.** Divergent/oversized reductions are dropped (fuel +
  size cap). This is a real modelling choice; a different cap could change which
  replicators are reachable.
* **"Self-catalysis" counts proposed reactions.** Nearly all commit (conservation
  permitting), but the count is of proposals, a slight over-estimate.

### Method additions

* `exp012_combinator.py`: a self-contained SKI reducer (`normalize`, fuel + size
  bounded) and `CombinatorPhysics`; a state encoding (str atom / 2-tuple app) so
  the kernel's distinguishability counts only atoms and conservation holds through
  duplication.
* `Universe.class_fed` / `class_constructed` / `amplification` (added Ω-0.7) now
  double as the cross-substrate replicator gauges; new `max_selfcat` gauge.

### Next steps

* **exp013 — from takeover to open-ended evolution.** Add *imperfect* reduction
  (rare mutation of the normal form) and/or spatial/resource structure, and ask
  whether the replicator population keeps *innovating* (sustained novelty *with*
  self-catalysis) instead of converging. This is the synthesis: open-ended
  construction ∧ reproduction.
* **Revisit the walls on the new substrate.** With behaviour intrinsic, re-run the
  deep-reuse question — a combinator that computes a useful function may finally be
  reused for *what it does*.
* **Multi-seed** confirmation and a mutation-rate dose-response.

---

## Milestone Ω-0.8 — Function is second-order on a form-based substrate (three walls point to a pivot)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** functional selection on
operator persistence is marginal — a null that, with exp009/exp010, motivated the
Ω-0.9 substrate pivot.

Decay was generalised from a kernel constant to a per-organization quantity a
Physics may set (decay was never in the immutable kernel). `exp011` couples an
operator's hazard to its **function**, two ways: `participation` (you matched
substrate) and `value` (your products were novel *and* survived). Against a uniform
control (1500 t, seed 0):

| mode | novelty | discovered ops | cum classes | op pattern len |
|------|:---:|:---:|:---:|:---:|
| control (uniform) | 9.29 | 7571 | 17,432 | 2.02 |
| participation | 9.89 | 7672 | 17,748 | 1.64 |
| value (generativity) | 9.30 | 7673 | 18,018 | 1.77 |

Selection *reshapes* the operator population (participation selects promiscuous
short patterns; value keeps them a bit longer), but novelty, discovery, and class
production are **essentially unchanged**. Open-endedness here is form-driven;
which operators persist is second-order because there is always a supply doing the
rewriting. Combined with the two Ω-0.7 negatives, the lesson is that *function must
be intrinsic to the substrate*, not selected on top of form — which is exactly what
Ω-0.9 does.

---

## Milestone Ω-0.7 — Two boundaries: deep primitives stay terminal, and copying does not emerge

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** two clean negative
results that map the *edge* of what this substrate can do.

### exp009 — reusable deep modules do not emerge (the terminal apex is intrinsic)

Ω-0.6 left the reuse pyramid with a terminal apex: deep primitives reused only
~2.6×. exp009 tried to fix it with a *persistent deep-module pool* (keep the most-
reused depth-≥5 primitives abundant in the feed). Dose-response (2500 ticks,
seed 0), success metric = **mean** reuse of deep primitives:

| module_prob | deep **mean** reuse | deep **max** reuse | overall max reuse |
|:---:|:---:|:---:|:---:|
| 0 (baseline) | 2.28 | 10 | 21 |
| 0.3 | 2.18 | 36 | 36 |
| 0.6 | 2.13 | 71 | 71 |
| 0.8 | 2.10 | 80 | 80 |

The pre-registered metric is **flat (~2.1) across a strong dose-response** — even
slightly down. The *tail* rises (deep max reuse 10→80, and the single most-reused
primitive becomes deep), but that is nearly tautological: I fed those 32 modules,
so they appear in many structures. The **mean staying flat** is the real result:
the terminal apex is **intrinsic**. A deep primitive here is a semantically
*arbitrary* string; nothing makes it broadly useful across contexts, so it cannot
earn reuse the way short, combinatorially-common shallow motifs do. Forced
exposure buys a few reused modules, not general deep reusability. Verdict:
negative on the pre-registered hypothesis.

### exp010 — the copying capstone: self-replication does not emerge

The manifesto's discipline for reproduction: don't build a replicator, make
duplication a *possible move* and see if a self-amplifying lineage is discovered.
Enabling condition: with probability `dup_prob`, an operator is a **template**
(p → p p). The kernel now splits each class's births into *fed* (from the
reservoir) vs *constructed* (by other organizations); a replicator is a class the
soup rebuilds far beyond what the feed supplies. Dose-response (1500 ticks, seed 0;
"amplification" = max constructed/(fed+1), "dominance" = largest class's population
share):

| dup_prob | amplification | dominance | distinct classes | novelty |
|:---:|:---:|:---:|:---:|:---:|
| 0 (control) | 28.1 | 0.012 | 233 | 10.6 |
| 0.3 | 20.1 | 0.022 | 225 | 10.7 |
| 0.6 | 15.8 | 0.034 | 201 | 10.0 |
| 0.9 | 29.5 | 0.044 | 174 | 9.2 |

**No replicator emerges.** Amplification does not rise with duplication — it is
~15–30 *including the control*, driven by generic recurrent products, not copying.
Duplication only mildly concentrates the population (dominance 1.2% → 4.4%, far
from takeover) and slightly *reduces* diversity and novelty.

The reason is structural and fundamental. A true replicator needs an organization
that carries the instructions for its own copying **and** has them executed *on
itself* — von Neumann's description/execution coupling. In this soup operators act
on *data* and produce *data*; there is no path for an operator to emit a copy of
*itself*. So **open-ended construction ≠ reproduction**. Persistence plus
construction — which this substrate has in abundance — is *not sufficient* for
self-replication; the manifesto's expectation that copying falls out of "imperfect
persistence" is, for this substrate, falsified. Reproduction would have to be
*scaffolded* (a self-referential constructor architecture), not discovered.

### Why these two negatives matter

They draw the substrate's boundary. Ω-0.2–0.6 showed it does one big thing
genuinely: **open-ended, deep, combinatorial, heavily-reused hierarchy** via
reification. Ω-0.7 shows two things it does *not* do without new architecture:
(a) make *deep* structure broadly reusable (needs semantics/function, absent
here), and (b) breed *self-replicators* (needs self-reference/description-execution
coupling, absent here). Both point the same way: the next real capability jump is
**function** — organizations whose *behaviour*, not just their form, is what
persists and is selected. Form-only construction has a ceiling, and we have now
found two of its walls.

### Method additions

* Kernel: per-class `class_fed` / `class_constructed` split and
  `Universe.amplification` (self-amplification detector).
* `ConstructionPhysics`: `dup_prob` (template operators) and `op_feed_rate`
  (keeps operators available against decay); publishes `amplification` and
  `dominance` gauges. `ReificationPhysics`: `module_prob` / `module_min_depth` /
  `module_size` (deep-module pool) and deep-reuse gauges.

### Next steps (a fork in the road)

* **Give organizations function.** Attach to each organization a cheap *behaviour*
  (e.g. it is scored by what its operator does to a held test input) so that
  *function*, not form, is what persists. Prediction: deep primitives that encode
  useful function become reusable, and description/execution coupling becomes
  possible — re-opening both exp009 and exp010 on a substrate that can actually
  support them.
* **Or scaffold self-reference minimally** (an operator able to emit operators
  structurally like itself) and re-run exp010 to confirm that description/execution
  coupling is *the* missing ingredient, not merely one candidate.

---

## Milestone Ω-0.6 — Depth and reuse are separate axes; a toolkit emerges as a pyramid

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the "deep hierarchy is
thin" prior was **falsified** (it is already combinatorial); reuse is a *separate*
controllable axis, and optimising it yields a realistic reuse pyramid.

### Measuring the reification DAG (falsifies "deep-but-thin")

exp007 gave depth; the natural worry was that the deep hierarchy is a thin ladder
(each primitive extended once, never recombined). Instrumenting the DAG
(`mean_reuse`, `max_reuse`, `combinatorial_fraction`) said otherwise:

| arm | primitives | max depth | mean reuse | max reuse | combinatorial frac |
|-----|:---:|:---:|:---:|:---:|:---:|
| baseline      | 314 | 12  | 2.25 | 24 | **0.91** |
| frontier=0.6  | 707 | 203 | 2.44 | 11 | **0.82** |

82–91% of reifications **fuse ≥2 reified primitives** — genuine recombination, not
a ladder. But reuse is *modest* (mean ~2.4), and frontier feeding *lowers* peak
reuse (24 → 11): racing depth-ward, it uses each primitive a few times before the
frontier moves on, so no stable, heavily-reused core forms.

### Optimising reuse — toolkit feeding

exp008 keeps the **most-reused** primitives abundant in the feed (an emergent
"toolkit"), the reuse-analogue of exp007's depth frontier. Result (2000 ticks,
seed 0, reify_max_len=6):

| arm | primitives | max depth | mean reuse | **max reuse** | deep≥5 |
|-----|:---:|:---:|:---:|:---:|:---:|
| baseline                    | 314  | 12  | 2.25 | 24  | 215 |
| frontier=0.6 (depth)        | 707  | 203 | 2.44 | 11  | 687 |
| library=0.6 (reuse)         | 550  | 7   | 2.20 | **78**  | 83  |
| library=0.3 + frontier=0.3  | 518  | 78  | 2.39 | **54**  | 394 |
| library=0.9 (aggressive)    | 1209 | 5   | 2.62 | **340** | 91  |

Three findings:

1. **Depth and reuse are orthogonal, controllable axes.** Frontier feeding buys
   depth (203) with thin reuse (11); toolkit feeding buys reuse (78) with shallow
   depth (7). Splitting the feed budget buys **both** — the combined arm is deep
   (78) *and* richly reused (54) with 394 deep primitives: the richest DAG.
2. **Reuse is heavy-tailed, and the core is shallow.** Toolkit feeding pushes peak
   reuse to 78–340 — a few "core components" reused hundreds of times — while mean
   reuse barely moves (~2.4). Inspecting the combined arm: the top-reused
   primitives are all depth 1–4 (reused 37–50×); shallow (≤3) primitives average
   **18.5** reuses, deep (≥5) primitives only **2.6**. So a **reuse pyramid**
   forms: a broad, heavily-reused foundation of low-level primitives under a
   unique, terminal deep apex — structurally like letters→words→books or
   atoms→molecules→organisms.
3. **Recombination is robust** (`combinatorial_fraction` 0.82–0.98 throughout).

### Honest limitations

* **Reusable *deep* modules do not emerge.** Deep primitives stay terminal (reused
  ~2.6×). There is no complex-yet-reused component — the analogue of a reusable
  organ or a widely-called library function that is itself deep. That is the
  clearest structural gap remaining.
* **Aggressive toolkit feeding degenerates toward shallow.** library=0.9 reaches
  max reuse 340 but max depth 5 — over-concentrating on shallow cores costs all
  depth. Moderate/combined settings are the sweet spot.
* **Mean reuse is stubbornly ~2.4** across every arm; only the *tail* thickens.
  Whether broad (not just peak) reuse can be raised is untested.
* **Single seed.**

### Method additions

DAG instrumentation on `ReificationPhysics`: `_reify_structure`, incremental
`_reuse` counts and `_combinatorial_count`, surfaced as gauges. New knobs
`library_prob` / `library_size` (toolkit feeding), composable with the frontier
knobs.

### Next steps

* **exp009 — reusable deep modules.** Bias reification toward structures that
  *reuse an existing deep primitive*, or make deep primitives cheaper to re-embed,
  and ask whether a complex-and-reused component can emerge (closing the pyramid's
  apex gap). This is the substrate's version of "a technology becoming a reusable
  part."
* **Multi-seed** confirmation of the depth/reuse orthogonality and the pyramid.
* With a deep, reused vocabulary now available, the long-deferred **copying**
  question (does any operator lineage discover self-templating over reified parts?)
  becomes the natural capstone.

---

## Milestone Ω-0.5 — Frontier-focused reification lifts the depth ceiling (a prediction, confirmed)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the Ω-0.4 rarity
mechanism and its predicted fix are **confirmed** — the first positive prediction
in the program to survive its test, after four straight falsifications.

### The prediction

Ω-0.4 concluded the depth plateau (~12) is a *rarity equilibrium*: the deepest
primitives are too scarce in the data pool for the next level to recur. It
predicted that **concentrating recurrence on the frontier** — keeping the
current-deepest primitives abundant — would lift depth *without* the breadth
explosion that global bar-loosening caused. exp007 implements exactly that: a
fraction `frontier_prob` of every fed symbol is drawn from the top `frontier_band`
depth levels rather than uniformly.

### Result — a clean dose-response (4000 ticks, seed 0, reify_max_len=6)

| frontier_prob | max depth | mean depth | primitives | depth-weighted | ops/1k(late) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 (baseline)   | 12 | 6.4 | 510 | 3,241 | 206 |
| 0.3 | 164 | 74 | 722 | 53,459 | 306 |
| 0.6 | 401 | 203 | 1,374 | 278,305 | 670 |
| 0.9 | **625** | **314** | 2,259 | 708,671 | 1,144 |
| `depth_discount` (Ω-0.4) | 8 | 6.6 | **7,990** | 52,460 | 3,996 |

Frontier concentration lifts the ceiling **from 12 to 625 (~50×)**, monotonically
in the dose. The prediction held exactly.

### The quality metric earns its keep

Ω-0.4 warned raw primitive count is gameable. Here is the proof it matters:
`depth_discount` mints **7,990** primitives — 3.5× *more* than frontier=0.9 — yet
its mean depth is **6.6** (shallow flood), while frontier=0.9 reaches mean depth
**314** with 13× the depth-weighted construction. A count-based scorecard would
crown the flood; the depth-based
:mod:`omega.metrics.construction_quality` (mean depth, depth-weighted total, deep
fraction) correctly credits the frontier runs. This is why exp007 is judged on
depth, not count.

### Is depth-625 real hierarchy or a degenerate ladder?

Checked, because a frontier that always feeds the single deepest symbol could
produce a linear depth-counter (Rₙ₊₁ = (Rₙ, x)) rather than structure. It does not.
At frontier=0.6 (1500 ticks): **524 primitives across 158 depth levels, ~3.3
primitives per level**, with branching at 137 of 158 levels (only 21 single-
primitive rungs). So it is a genuinely (if modestly) *branching* deep hierarchy —
real cumulative construction, not a unary counter and not a shallow flood.

### Honest limitations

* **Branching is modest (~3.3/level), not bushy.** Deep *and* wide hierarchy (a
  rich DAG with heavy reuse of deep primitives) is not yet demonstrated; ~3-wide is
  better than linear but far from a combinatorially rich tree.
* **Depth grows ~linearly in ticks with no observed saturation** through 4000
  ticks (frontier=0.9: 625 at ~0.16/tick). Unbounded-in-practice here, but a true
  asymptote at 10⁵–10⁶ ticks is untested; reservoir stability at high
  `frontier_prob` was not separately characterised.
* **Single seed.** The 5-point dose-response monotonicity is strong, but multi-seed
  confirmation and variance are future work.
* **High `frontier_prob` is an aggressive regime.** frontier=0.9 also triples the
  operator-discovery rate; whether that is healthy exploration or the frontier
  starving the rest of the ecology is not yet dissected. frontier=0.6 is the
  balanced illustration.

### Next steps

* **exp008 — rich hierarchy, not just deep.** Measure and then optimise the
  reification *DAG* (branching factor, reuse of deep primitives, not merely max
  depth). The goal shifts from "how deep" to "how richly cumulative".
* **Multi-seed dose-response** of `frontier_prob` to get error bars and locate the
  regime where depth grows fastest without destabilising the ecology.
* **Copying (exp009 territory).** With a deep, reusable primitive vocabulary now
  available, revisit whether any operator lineage discovers approximate
  self-copying over reified parts.

---

## Milestone Ω-0.4 — The depth ceiling is not length, it is rarity — and depth trades off against breadth

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the Ω-0.3
length-ceiling attribution was **falsified**; depth is a rarity equilibrium in
genuine trade-off with breadth.

### Test 1 — sweep the length caps (falsifies H-length)

Ω-0.3 guessed exp005's depth plateau (~13) came from the reified-structure length
cap. Sweeping `reify_max_len` at 4000 ticks (seed 0), with `max_len` kept
generously above it so raw string length is never binding:

| reify_max_len | max_len | final depth | depth / 1k |
|:---:|:---:|:---:|---|
| 4  | 16 | 13 | [9, 11, 12, 13] |
| 6  | 20 | 12 | [10, 12, 12, 12] |
| 8  | 24 | 11 | [9, 11, 11, 11] |
| 12 | 32 | 12 | [10, 10, 12, 12] |

The plateau is **flat at ~11–13 across a 3× range** of the cap (and *lower*, not
higher, at 8). Length is not the constraint. This matches the structural argument:
a length-L structure needs only *one* deep child to go one level deeper, so more
slots do not buy depth; and longer structures are themselves rarer, cancelling the
"more chances to include a deep child" effect.

### Test 2 — counteract rarity directly (confirms H-rarity, reveals a trade-off)

If depth is throttled by the *rarity* of the deepest primitives, then lowering the
recurrence bar for deeper motifs (`depth_discount`: bar shrinks one per child-depth
level) should let depth climb. It did the opposite (5000 ticks, seed 0,
`reify_max_len=6`):

| arm | final depth | depth / 1k | ops / 1k (late) | primitives |
|-----|:---:|---|:---:|:---:|
| baseline          | 12 | [10, 12, 12, 12, 12] | 112 | 566 |
| `depth_discount`  | **8** | [7, 7, 8, 8, 8] | **3996** | **9990** |

Discounting the bar **exploded breadth** (35× the discovery rate, 18× the
primitives) while **lowering depth** (12 → 8). The reason confirms rarity and adds
a twist: making reification promiscuous floods the pool with shallow primitives,
which makes any *specific* deep chain even rarer, so depth falls. **Depth and
breadth compete for the finite data pool.** A selective bar earns a few deep
primitives; a permissive bar mints a flood of shallow ones. You cannot have both by
tuning the bar or the length cap.

### What this means

Sustained open-endedness in this substrate is real (Ω-0.3) but its *shape* is
governed by a breadth–depth trade-off, and neither axis is unbounded under the
current mechanism:

* **Breadth** (distinct primitives over time) is sustained and can be pushed very
  high, but promiscuous reification is low-quality novelty — closer to relabelling
  than to construction.
* **Depth** (nesting / hierarchy) saturates ~12 because the deepest frontier is
  rare, and cannot be lifted by lowering the bar (that dilutes it further) or by
  raising the length cap (irrelevant).

Unbounded *hierarchy* therefore requires a mechanism that **concentrates recurrence
on the deepest frontier** — actively keeping the current-deepest primitives
abundant in the data pool so the next level up can form — rather than any global
loosening. That is a specific, testable direction, not a vague hope.

### Method additions

* `ReificationPhysics.depth_discount` — the depth-scaled recurrence bar (default
  off; behaviour-preserving).
* exp006 sweeps `reify_max_len`/`max_len` with `max_len` auto-scaled so length is
  never the hidden binding constraint.

### Next steps

* **exp007 — frontier-focused reification.** Bias the feed and/or the expand
  operators toward the *deepest* existing primitives so the top of the hierarchy
  stays abundant. Prediction (from Ω-0.4): depth climbs past ~12 *without* the
  breadth explosion, because recurrence is concentrated, not loosened.
* **Quality-of-novelty metric.** The breadth explosion shows raw primitive count is
  gameable; add a measure that credits *depth-weighted* or *reused* primitives over
  shallow one-offs, so the Open-Endedness Index cannot be inflated by relabelling.

---

## Milestone Ω-0.3 — The cumulative nesting ratchet (another hypothesis falsified, a stronger result found)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the dilution hypothesis
was **falsified**; the operative mechanism is a *nesting ratchet*, yielding the
strongest and first demonstrably *cumulative* open-endedness in the program.

### The hypothesis under test (and its failure)

Ω-0.2 blamed exp004's mild long-horizon rate decline on **dilution** — a random
feed spread over a growing alphabet makes any motif recur less — and proposed
feeding only base symbols so reified symbols would enter data only through
construction. A clean 2×2 factorial (knobs: `feed_reified` × `reify_threshold_
nested`) at 4000 ticks, seed 0, new operators per 1000-tick window:

| feed_reified | nested bar | ops/1k windows | depth | verdict |
|:---:|:---:|---|:---:|---|
| **True** | 4 (=exp004) | [193, 64, 58, 58] | 6 | OPEN-ENDED |
| **True** | 2 | **[424, 194, 190, 174]** | **12** | OPEN-ENDED |
| False | 4 | [324, **0, 0, 0**] | 1 | CONVERGED |
| False | 2 | [346, **0, 0, 0**] | 2 | CONVERGED |

The proposed fix (`feed_reified=False`) **froze the universe entirely** after the
first window. So feeding reified symbols back is not the cause of dilution — it is
the *essential fuel* of the mechanism: a higher-order motif can only recur, and so
be reified, if its reified components are abundant in the data pool, and
construction alone does not keep them abundant. Hypothesis falsified, cleanly, by
its own control.

### The actual lever: a nesting ratchet

The knob that matters is the **recurrence bar for nested motifs** (motifs that
already contain a reified symbol). Lowering it from 4 to 2 roughly **triples** the
sustained discovery rate (~58 → ~180 ops/1k) and **doubles** lineage depth (6 →
12), because it lets primitives-built-from-primitives form freely. This is a true
ratchet: each new higher-order primitive is a rung the next one can stand on.

### Long-horizon characterisation of the winning config (8000 ticks, seed 0)

`feed_reified=True, reify_threshold_nested=2`:

* new operators / 1000 ticks: **[424, 194, 190, 174, 138, 194, 98, 134]** — after
  the burst, noisy but **no decay toward zero** (~150/1k sustained; window 6
  rebounds to 194).
* reservoir pressure holds at **~0.25 throughout** — not resource-limited.
* lineage depth: 9 → 11 → 12 → 12 → 13 → 13 → 13 → 13 — **ratchets to ~13 then
  plateaus**, while new primitives keep appearing (~75/1k). So *depth* saturates
  (a structure-length ceiling from `reify_max_len=4`) but *breadth* — distinct
  primitives over time — does not.
* totals: 1550 operators, 744 primitives, **68,243 organizational classes** — an
  order of magnitude past exp004.

This is the strongest open-endedness in the program and the first that is
demonstrably **cumulative**: depth-13 nesting means primitives standing on
primitives, thirteen deep — the manifesto's "organizational depth", "hierarchy
formation", and "recursive innovation" all reading positive at once.

### Honest limitations

* **Depth plateaus (~13).** With `reify_max_len=4` and `max_len=10`, nesting hits a
  structural ceiling. Open-endedness here is sustained *breadth* at bounded depth,
  not unbounded depth. Whether lifting the length caps yields unbounded depth (or
  just slower saturation) is untested.
* **Sustained, not proven-infinite.** ~150 ops/1k is roughly flat with high
  variance through 8000 ticks; 10⁵–10⁶ ticks would be needed to distinguish a true
  positive asymptote from an extremely slow decline.
* **Single-seed long runs.** The 8000-tick characterisation is one seed (the
  factorial and the short tests are the multi-condition evidence); a multi-seed
  long-horizon study is the obvious next confirmation.
* **Method note.** The `gauges` facility (a Physics publishing scalar observables
  into the metrics stream) was added so lineage depth could be tracked without
  polluting the kernel's fixed schema.

### New hypotheses / next steps

* **exp006 — lift the depth ceiling.** Raise `reify_max_len`/`max_len` and re-run
  the depth trajectory. Prediction from the plateau diagnosis: depth climbs
  further before re-saturating; if it grows without bound, that is unbounded
  hierarchy.
* **exp006b — dependency DAG, not just max depth.** Record the full reification
  lineage graph and measure whether its *shape* (branching, reuse of deep
  primitives) keeps changing, i.e. cumulative *innovation* rather than cumulative
  *depth* alone.
* **Copying (exp007 territory).** With deep primitives available, ask whether any
  operator lineage implements approximate self-copying (a fold/expand pair acting
  as a template) — reproduction as a discovered strategy over reified parts.

---

## Milestone Ω-0.2 — Falsifying the v0.1 headline, and the first sustained open-endedness (reification)

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** the v0.1 open-endedness
claim was **falsified**; a new mechanism (reification) shows the first sustained
open-endedness, with caveats.

### 1. The v0.1 headline was wrong, and my own metric hid it

Ω-0.1 labelled exp003 "OPEN-ENDED (law set growing)". Running the falsification
conditions I had written down exposed that as an artefact. The index gated on
**cumulative** operator growth (`operator_growth > 0`). But cumulative totals only
ever go up — a universe that discovers a finite burst of operators and then
freezes still has a large positive total. The tell:

| seed | operators @400 ticks | operators @1500 ticks |
|------|----------------------|-----------------------|
| 0 | 30 | **30** |
| 1 | 28 | **28** |
| 2 | 52 | **52** |

The operator set is **identical** at 400 and 1500 ticks: it froze early. Over the
long horizon exp003's novel-class rate also collapses (saturation ~0.06–0.13). So
**exp003 is not open-ended** — it merely has a larger finite possibility space
than exp002. Claim retracted.

### 2. Two metric bugs, opposite signs

* **False positive (fixed).** Cumulative operator growth as an open-endedness
  gate. Replaced by `ConstructionTracker.recent_operator_rate` — new laws per tick
  *at the end of the run*. Zero ⇒ closed, regardless of how many were found
  earlier.
* **False negative (fixed).** The rate was first measured over a fixed 50-tick
  window. A genuinely sustained rate of ~0.05 laws/tick *quantizes to 0* in a
  50-tick window over a long run, producing a spurious CLOSED verdict — the exact
  mirror of the first bug. The window is now scaled to the horizon
  (`max(50, ticks//10)`). Both bugs came from confusing a **total** with a
  **rate**, and a **rate** with its **measurement resolution**. Logged prominently
  because this class of error is easy to make and invisible without long-horizon,
  multi-seed runs.

Novelty itself was demoted to a mere *liveness floor*: every experiment with a
random feed shows positive novelty forever (noise fakes it — exp001 is the proof),
so a nonzero novelty rate is necessary but not sufficient. The trustworthy signal
is a sustained rate of *new organizational laws*.

### 3. Diagnosis: bounded material ⇒ finite possibility space ⇒ forced closure

exp003 (and exp004's control) freeze because a fixed finite alphabet plus a length
ceiling makes the set of possible operators **finite**. Discovery must stop once
it is exhausted. Closure there is not bad luck; it is forced. A finite-material
universe can only stay open if its *space of possibilities keeps enlarging*.

### 4. exp004 — reification: promote persistent structure to a new primitive

The mechanism (Axiom 5 made concrete): when a composed organization becomes
reliably persistent (re-formed ≥ threshold times), mint a **new atomic symbol**
naming it and add it to the alphabet. Later feeds and operators may use it, so
structures and operators that were literally unconstructible before now exist. A
reified symbol may itself sit inside a later reified structure ⇒ an unbounded
ladder of primitives. Folding a k-symbol motif into one symbol also *returns k-1
quanta to the reservoir*, so compression relieves scarcity and funds further
construction — a self-maintenance advantage that falls out of the resource
gradient rather than being programmed.

**Results (3 seeds each; treatment `reify=True` vs matched control `reify=False`):**

| horizon | condition | operator_rate (late) | primitives | classes_ever | verdict |
|---------|-----------|----------------------|------------|--------------|---------|
| 2000 | reify ON  | 0.04–0.08 (sustained) | ~106 | ~16,700 | **OPEN-ENDED 3/3** |
| 2000 | reify OFF | 0.0 | 0 | ~900 | CONVERGED 3/3 |
| 2000 | exp003    | 0.0 | 0 | ~1,700 | CLOSED 3/3 |

At 2000 ticks the treatment's novelty saturation is **0.96** (late rate ≈ 96% of
early) and its operator set is still climbing (not plateaued) in every seed, while
the matched control — same physics, reification off — converges. This is the first
result in the program where a universe keeps enlarging its own possibility space
across seeds rather than exhausting it.

### 5. Honest caveat: the asymptote is not settled

A single 6000-tick run shows the discovery rate is **not perfectly constant**. Per
1000-tick window: new operators 193 → 64 → 58 → 58 → 54 → 34; new primitives 71 →
32 → 29 → 29 → 27 → 17. After the initial burst it is roughly flat (≈0.055
laws/tick) through the middle, with a mild decline at the end. Reservoir pressure
stays ~0.25 throughout, so it is **not** resource exhaustion. The likely brake is a
*dilution effect*: as the alphabet grows, the random feed spreads over more
symbols, so any given motif recurs less often and fewer motifs cross the
reification threshold — the growth of the alphabet throttles the mechanism that
grows the alphabet. Whether the rate asymptotes to a positive constant (true
open-endedness) or decays slowly to zero (closure, merely much delayed) is **not
determined** by these runs. Claiming "solved" here would repeat the v0.1 mistake.

### New hypotheses / next steps

* **exp005 — beat dilution.** Make reification pressure *relative* to the current
  alphabet (threshold scales with symbol count), or drive it by an operator's
  *usefulness* (how often it participates in surviving reactions) rather than raw
  motif recurrence. Prediction: a flat, non-declining discovery rate.
* **Cumulative dependency.** Measure whether later primitives are *built from*
  earlier ones (a growing DAG depth in the reification lineage). Sustained
  open-endedness should show ratcheting, not just a growing flat vocabulary.
* **exp004 self-maintenance angle.** The compression-frees-quanta effect predicts
  that reified lineages should out-compete un-reified ones under harder scarcity.
  Test with a much smaller reservoir.
* Run exp004 to 10⁴–10⁵ ticks to resolve the asymptote directly.

---

## Milestone Ω-0.1 — The constructive substrate and the closure/constructibility contrast

**Date:** 2026-07-04 · **Status:** complete · **Verdict:** hypothesis supported at
small scale.

### The pivot away from the CA/Lenia line

The parent directory contains an earlier line of work (`omega_coupled.py`,
`omega_geo.py`, `exp_selection.py`, `exp_landscape.py`). That work is careful and
worth keeping: it built a Lenia-style continuous cellular automaton with a
heritable gene `K`, showed with a matched control that **selection genuinely acts
on `K`** (variance culling beyond neutral drift), and used pairwise-invasibility
plots to ask whether the fitness landscape deforms under its own occupants.

But it is confined to exactly the paradigm the Ω manifesto rejects as the source
of closure:

* a **fixed physical space** (a 96×96 grid),
* a **fixed operator set** (one convolution + one growth function), and
* a **fixed genotype space** (a scalar `K ∈ [-1, 1]`).

No matter how rich the dynamics on that grid, the reachable set of organizations
is bounded a priori. Selection can climb the landscape; it cannot enlarge it.
Per the project's authority to *abandon previous hypotheses and redesign from
first principles*, Ω-0.1 starts over with a substrate that has **no space, no
fixed operators, and a genotype space that can grow at runtime.**

### The substrate

Everything is an `Organization`: an arrangement of atomic *differences* (Axiom 1),
represented as a nested tuple. There is no grid — the universe is an unordered
soup plus a **reservoir** of free distinguishability. The one immutable law is
**conservation of distinguishability**: `reservoir + Σ bound = const`. Novelty is
therefore always recombination, never inflation; the reservoir is a genuine
resource gradient, and when it empties, organizations must compete for the bound
quanta. That competition — not a hand-coded fitness — is where selection comes
from.

Laws (`Transform`s) live in a **mutable registry**. A `Physics` plugin supplies an
experiment's laws and, crucially, may *add* laws that organizations discover at
runtime. This is the mechanism intended to defeat closure.

### Experiments and results (seed 0)

> ⚠ **The exp003 verdict below was RETRACTED in Ω-0.2.** It relied on a cumulative
> operator-growth metric that could not tell "still discovering" from "discovered a
> finite burst then froze". Long-horizon multi-seed runs show exp003 freezes. See
> the Ω-0.2 milestone at the top of this log.

| Exp | Question | Key reading | Verdict |
|-----|----------|-------------|---------|
| 001 noise | Can persistence emerge from pure noise? | `composed_persistent = 0`, `max_reform = 1` | **No** — clean null |
| 002 binding | Can stable organizations emerge from local interaction? | `composed_persistent = 4`, `max_reform ≈ 2400` | **Yes** — but `OEI = 0` |
| 002 control (`bind=False`) | Is it the binding, not the small alphabet? | `composed_persistent = 0` | Confirms binding is the cause |
| ~~003 construction~~ | Can novelty self-amplify and enlarge the law set? | ~~`operator_growth > 0`~~ | ~~OPEN-ENDED~~ → **RETRACTED (freezes)** |

### What the numbers mean

1. **Persistence is not free (001).** Fed only high-entropy noise, the universe
   produces zero re-forming organizations. Every class is born once and decays.
   Importantly, 001's *novelty rate is enormous* — every tick is full of
   never-seen strings — yet it is not open-ended. This is the empirical
   justification for making the Open-Endedness Index multi-factor: **raw novelty
   is maximised by noise** and must be gated by persistence and constructibility.

2. **A methodological trap, found and fixed.** The first persistence metric
   ("class present for many ticks") reported the *noise control as persistent*,
   because with decay hazard `h` every instance survives ~`1/h` ticks. That
   measures the decay constant, not organization. The metric was rebuilt around
   **re-formation** (independent re-creations of a class), which is immune to the
   `1/h` artefact. The null then correctly reads zero. Recorded here because the
   trap is subtle and will recur.

3. **Persistence without constructibility → closure (002).** Binding produces
   genuinely persistent composed organizations (a correlation between two
   differences, re-formed thousands of times as individual instances decay). But
   the possibility space is a fixed, finite set of bond types; every class is
   discovered almost immediately and novelty collapses to zero. The index reads
   **CLOSED**. This is the failure mode the whole project is organized against,
   reproduced deliberately in miniature.

4. **Constructibility → open-endedness (003).** When operators can author
   operators (a rewrite whose replacement contains the delimiter yields a
   *new operator whose content the data determined*), the law registry grows
   without bound within the run and novelty stays positive. The index reads
   **OPEN-ENDED (law set growing)**. The contrast 002→003 is the core result: the
   difference between a dead end and an open universe was **not** more space or
   more time — both had the same reservoir and tick budget — it was whether the
   universe could enlarge its own operator set. This is direct (small-scale)
   support for the primary hypothesis: *open-endedness requires infinite
   constructibility, not infinite space.*

### Honest limitations of Ω-0.1

* **No hierarchy yet.** exp003 grows the operator set but strings stay shallow
  (compositional depth ~1). Open-ended *operator discovery* is demonstrated;
  open-ended *hierarchy formation* is not. The `hierarchy_index` barely moves.
* **Novelty in 003 is partly feed-noise.** The chemostat injects random data, so
  some 003 novelty is 001-style churn. It is the `operator_growth` term, not the
  raw novelty rate, that certifies open-endedness — which is why the verdict logic
  keys on it.
* **Bounded within a run, not proven unbounded.** "The registry grows for 400
  ticks" is not "grows forever." Whether operator discovery sustains, saturates,
  or explodes over 10⁴–10⁶ ticks is untested.
* **Single-seed narrative.** The suite is deterministic and the tests pin the
  qualitative claims, but effect sizes across many seeds are not yet aggregated.

### Falsification conditions carried forward

* If, over long runs, exp003's `operator_growth` saturates and `novelty_rate → 0`,
  the constructive-rewriting substrate closes and this substrate is falsified as
  a route to open-endedness.
* If a matched control that *permits operator authoring but forbids meta-operators*
  (replacements can never contain the delimiter) is **also** open-ended, then
  operator discovery is not the operative mechanism and the causal story is wrong.

---

## Next experiments (planned, not yet run)

* **exp004 — self-maintenance.** Introduce no explicit metabolism; deplete the
  reservoir harder and ask whether any organization discovers a cycle that
  re-creates its own components faster than they decay (an autocatalytic set).
  Metric: existence of a class whose re-formation is *causally closed* over its
  own lineage graph.
* **exp005 — copying.** Ask whether, among discovered operators, any implements
  (approximate) self-application that copies a data string — reproduction as a
  discovered strategy, not a primitive.
* **exp006 — cumulative innovation.** Track whether later-discovered operators
  build on earlier ones (lineage depth in the operator graph), i.e. ratcheting.
* **exp007/008 — meta-operators and search-space enlargement.** The
  `meta_prob = 0` vs `> 0` control above, run to long horizons, is the first cut
  at exp007. exp008 is the quantitative claim that each meta-operator strictly
  enlarges the reachable set.
* **Cross-cutting:** add the missing hierarchy mechanism (a composition operator
  that nests organizations) and re-ask whether depth becomes open-ended, closing
  the gap flagged above.
