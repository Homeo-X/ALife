<p align="center">
  <img src="docs/banner.svg" alt="Project Ω — open-ended organizational complexity" width="100%">
</p>

<p align="center">
  <a href="#quickstart"><img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="python 3.10+"></a>
  <img src="https://img.shields.io/badge/dependencies-none%20(stdlib%20only)-8affc1" alt="stdlib only">
  <img src="https://img.shields.io/badge/tests-89%20passing-brightgreen" alt="tests">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license">
</p>

# Project Ω (Omega)

**A falsifiable research engine for open-ended organizational complexity** — testing one hypothesis:

> **Open-ended evolution does not require infinite space. It requires infinite _constructibility_.**

Most artificial-life worlds are hand-authored and therefore finite: they eventually run out of
new things. Ω asks the opposite question — *what minimal substrate lets a world keep building
genuinely new organization forever, with nothing designed in advance?* — and answers it as a
lab notebook: every claim is a yes/no question against a matched control, and **retracted claims
and negative results are kept on purpose** (that is what makes it science, not a demo).

Everything is an **Organization** — a persistent arrangement of interacting differences. Space,
time, matter, and life are *not* primitives; if they appear, they must appear *as* organizations.
The only fixed laws are identity, consistency, causality, and conservation of distinguishability.

---

## The one result, in one line

Feeding persistent structure back as new primitives — growing *constructibility* while the
material is unchanged — turns a world that closes into one that stays open **forever**, and that
open+modular substrate lets collectives become **reproducible individuals** that stack into a
**tower of organizational levels**:

```
                              ╭──────────────╮  ← each tier's heritable collectives
             culture          │  culture     │    become the next tier's atoms
                ▲             ╭┴──────────────┤    (reification across levels)
             biology          │  biology      │
                ▲            ╭┴───────────────┤   novelty rate  ▁▂▃▄▅▆▇█▇▆▇█▇█  (never → 0)
            chemistry         │  chemistry     │   heredity      self ≫ null (reproducible)
                ▲           ╭┴────────────────┤   depth         no ceiling found (compute-limited)
             physics  ─────► │  physics (kernel)│
                              ╰────────────────╯
     "constructibility, not space"        one recursive engine
```

## Key results

Each row is a falsifiable experiment (or milestone) with a matched control. Full detail in
[`omega/docs/RESEARCH_LOG.md`](omega/docs/RESEARCH_LOG.md); the per-experiment table is in
[`omega/docs/README.md`](omega/docs/README.md).

| # | Question | Result |
|---|----------|--------|
| **Ω-0.2** reification | Can a bounded material stay open-ended? | **Yes** — promoting persistent structure to *new primitives* keeps the possibility space growing; the matched control (no reification) freezes. |
| **Ω-0.15** collective individuality | Can a collective become a *reproducible individual*? | **Yes, in miniature** — a substrate that is **modular _and_ open-ended** (variable-length type paths) reaches the "both corner": strong reproducible heredity **and** sustained novelty. |
| **Ω-0.16** levels of organization | Does the transition *recurse*? | **Yes** — each tier's heritable collectives become the next tier's atoms: physics → chemistry → biology → culture from **one engine**. |
| **Ω-0.17** unboundedness | Does it persist over 10⁵ ticks / keep climbing? | **Affirmative in miniature** — heredity flat & novelty > 0 to 120k ticks; no intrinsic tower-depth ceiling found. |
| **Ω-0.31** settling openness | Is the long-run novelty *real*, or an eviction-window artifact? | **A genuine positive floor — with an honest correction.** A fixed-memory global-novelty sketch (counts each class once *ever*) shows the open engine still discovers never-before-seen classes at **~0.13/tick at 300k ticks, 3 seeds**, decisively above the closed control's exact **0**. But the previously-reported *flat* rate was **~4× inflated** by eviction recycling; the true genuine rate is **positive but slowly declining** (halves over 300k). Claim confirmed, overclaim retired. |
| **Ω-0.39–40** settled at 10⁶, held to 3M | Does the genuine-novelty floor *survive* the literal long horizon, or dilute? | **Real, and it holds under stress.** At **10⁶ ticks × 5 seeds** the eviction-robust global rate falls 0.30→0.10 then **levels onto ~0.09 genuinely-new classes/tick** (~130,600 distinct classes ever/seed), decisively above the closed control's **exact 0.0000** (144 classes, ever) — the Ω-0.31 "slow decline" was a **transient**. A **3× horizon stress to 3M ticks** (Ω-0.40) confirms it: after the transient the rate is **flat within ~14% across the final 2M ticks** (~281,400 distinct/seed), decelerating (64%→14%) toward a positive asymptote, not toward zero. "Stays open forever" holds at, and past, the horizon the thesis is stated for. |
| **Ω-0.20** sustained novelty | Does open-endedness need *continuing* construction? | **Yes** — a one-time alphabet bump still closes; only *ongoing* reification holds the novelty rate. Constructibility is a **rate, not a stock**. |
| **Ω-0.42** compounding competence | Can collective *competence* become a rate too (not just novelty)? | **Yes — the self-improvement arc's first positive.** After ~10 experiments where every selection/representation/replicator/coevolution lever moved the competence *level* but never the *slope*, the **Catalytic Law** (promote the best deme's closure loop to a shared, network-visible *reaction* — the fix to exp049's opaque-atom failure) makes competence **compound**: it rises monotonically 0.89 → 1.24 (slope **+0.019**) where every fixed-law control is flat, and a random-injection control (3× shallower) shows the ratchet is genuinely competence-dependent. Competence is a **rate** once the substrate law grows with what's achieved — the exact analogue of Ω-0.20 for competence. Open edge: saturation. |
| **Ω-0.21** scaling | Can it run at 10⁶ ticks? | Bounded-memory mode + a **3× faster** kernel, validated against known results — the "in-miniature" cap lifted. |
| **Ω-0.22–23** the living world | Can you *watch* it? | A persistent, checkpointing **world** with a live dashboard: named lifeforms, cultures, a novelty pulse, geography, and the ability to reach in and steer it. |
| **Ω-0.48** the living world *embodies the arc* | Does the compounding-competence arc *transfer* from batch to the persistent, watchable world? | **Yes — and its life signals are now legible.** A gated **`living_world`** builder folds the arc's winners (Catalytic Law + Red Queen + full competence pressure) into the persistent, spatial, reifying world; a read-only **vital-signs** panel surfaces competence, autocatalytic **closure** (the self-maintenance/life signal), self-maintaining lifeform count, and the *genuine* (eviction-robust) novelty rate. Over 30k-tick worlds it reaches ~**1.6× the competence** (1.92 vs 1.20), ~**2.2× the closure** (0.60 vs 0.27), and ~**12× the breed-true heredity** of the exp030-era world. Two honest caveats: competence **plateaus** (single-tier saturation — across-time compounding needs the live tower next), and it's **deeper-not-wider** (lower raw diversity — competence selection canalizes). `living_world` off ⇒ the old world byte-identical. |
| **Ω-0.49** the live tower — *watch levels emerge* | Does the across-level meta-ratchet run *live* in the persistent, memory-bounded world (not just batch)? | **Yes — and it costs nothing to bound memory.** A gated **`TowerWorld`** runs the recursive tower live: it advances the top tier as a persistent world, then **promotes** its stable collectives to a new tier when they mature — so chemistry → biology → culture → … are *born over wall-clock time* (`python -m omega.world tower`), each playing by rules derived from the level below. Over 5-tier / 6-seed runs it reaches mean depth **3.5** with competence rising **+0.039/tier** across the *emergent* levels, and it is **eviction-invariant**: a memory horizon set *below* a tier's lifetime (so eviction genuinely bites) is **byte-identical** to the un-evicted batch ceiling — the tower reads the *live* network, not the evicted registry. So the world can grow a tower of levels **indefinitely, at flat memory**. |
| **Ω-0.24–47** toward minds | Can collectives become self-improving? | **A precise, honest arc that keeps naming the next barrier — and finally breaks the wall.** exp039 pinned collective heredity → **exp040 broke that ceiling** (self ≈ 0.56, world still open); **exp041/042** showed a higher heredity level and even a *self-expanding* scalar objective don't compound → barrier is **goal representation**. **exp044** supplies it (a heritable, composable target *path*) and gets the arc's first over-generations *deepening* — but *transient* and without lifting competence → barrier is **credit assignment**. **exp045** tries the direct fix (aim the goal at the closure core) — **still no compounding**: credit is a *representation* problem (put it in the fitness). **exp046** does that (a heritable per-part credit model in deme selection) — **still no compounding** → the limit is the **selection grain**. **exp047** adds within-collective selection — it **collapses the collective**: **competence is irreducibly collective**, and compounding would need **part-level replicators** (the exp012 lesson). **exp048** runs it on the replicator (combinator) substrate — replicating parts **lift the competence ceiling ~2×** (1.09 vs 0.62) but competence stays **high-and-flat**. **exp049** aims the Ω-0.20 *rate-not-stock* lever at competence itself (reify the most closure-central *competent* module to a new atom) — **still flat** (slopes ≈ 0), and reifying *competent* structure is indistinguishable from reifying *common* structure or *not reifying*; yet the alphabet grows 32→53 and finds ~26% more classes, so **novelty compounds while competence doesn't, within one run**. Reifying a competent module moves its structure into an **opaque atom** (out of the measured network) — the Ω-0.20 lever **does not transfer** from novelty to competence. The arc's closing lesson: **open-ended novelty ≠ open-ended competence** — the world compounds *what it builds* (Ω-0.31), not *how good its collectives are*. **exp052** tries the boldest lever — a **Red Queen** (a receding, coevolutionary target: reward a deme's closure *plus* the fraction of its closure core a live rival can't yet produce) — and it is the **first mechanism to raise competence above plain closure selection on the same substrate** (0.820 vs 0.673; +0.19 over the frozen-rival control; healthiest, non-collapsing networks) — **yet competence still doesn't compound** (slope −0.021): the receding target moves the *plateau*, not the *slope* — the same level-not-rate pattern as exp048, in its strongest form. The competence ceiling is set by the **substrate's fixed law**. **exp053 changes that law mid-run and BREAKS THE WALL:** the **Catalytic Law** promotes the highest-competence deme's closure loop to a shared *reaction* (`anchor → product`, injected every tick — network-visible, *not* an opaque atom, the exp049 fix), so competent structure becomes a reusable construction operation later collectives build on. **Competence compounds** — catalytic×Red-Queen rises monotonically 0.89 → 1.24 (slope **+0.019**, the arc's highest level; closure & survival rising) where every fixed-law cell is flat, and a random-injection control (3× shallower) confirms the ratchet is genuinely **competence-dependent**, not mechanical. The refined lesson: **open-ended novelty ≠ open-ended competence held only for a _fixed_ substrate law** — once the law grows with achieved competence (network-visibly), competence is a **rate** too (the exp053 analogue of Ω-0.20). Open edge: **saturation** — which **exp054** then characterizes: exp053 plateaus (~1.45), and it is **not** the catalyst cap (cap 16/80/400 byte-identical) but the substrate's **optimal richness** (finite competent structure). An **Earned Law** that expands the composition law along *construction depth* (lineages climbing `type_resolution` with closure) **fails** — earned competence 0.577 is the *lowest* arm (deeper paths starve cross-production). Competence has a **bias–variance ceiling** (too shallow exhausts competent structure, too deep starves closure), so it's a rate up to the optimal-richness ceiling, then a stock. **exp055** lifts that to the *tower*: running the compounding law at each level and **deriving each level's law from the level below's competence** (a **major transition as a rule-change**) makes competence **rise across levels** — the derived-law tower climbs 1.78 → 1.94 tier-over-tier (+0.081/tier) where the *fixed* compounding law is flat (+0.006), a first **across-level** meta-ratchet, and every tier sits far above the self-similar tower (~1.8 vs ~1.25). exp055 reported this as **fragile** (~⅓ of towers collapse, read as competence selection thinning the diversity recursion needs — the exp047 tension at the tower scale), but **exp056 retracts that**: dialing competence-selection strength (`competence_pressure ∈ [0,1]`) shows **no competence–diversity trade-off** — full pressure (1.0) is best on *every* axis at once (lowest collapse 0.20, most tier-0 diversity 21.5, deepest towers, strongest slope +0.101), and softening makes towers *more* fragile (collapse **U-shaped**, worst at intermediate pressure). The exp055 ~⅓ collapse (n=4) was **bootstrapping variance** (seeds never establishing a tier-0 network), not a competence-diversity mechanism. So competence compounds within a level (exp053) and, via a competence-derived rule-change, across levels (exp055) — and the across-level ratchet keeps towers robust and diverse at full pressure (exp056), no trade-off paid. **exp057** then probes what *does* limit tower robustness — exp056's residual **bootstrapping floor** (~10–20% of seeds never establish a founding tier-0 network) — and finds it is **structural, not timing-limited**: a tier-0 warmup drops the failure rate by only ~1 seed and **plateaus at 2×** (4× buys nothing), leaving mean depth flat, while *over*-warming tier 0 drives it to the exp053/054 optimal-richness ceiling and flips the across-tier slope **monotonically negative** (−0.039 → −0.102 → −0.162) — so the floor needs a **starting-diversity** lever, not more time, and equal-length tiers beat a front-loaded foundation. **exp058** then tests that starting-diversity lever (seed tier 0 with more independent founder demes) and finds it **doesn't** move the floor either: more founders drop the failure rate by only ~1 seed then **plateau** (never to zero), and *over*-provisioning founders **monotonically shrinks** the towers (depth 3.88 → 3.50 → 3.12, a bloated tier-1 alphabet diluting higher-tier cross-production). So tower robustness has a **hard floor** independent of *both* time (exp057) *and* starting diversity (exp058) — the residual ~3–6% of seeds are intrinsically non-networking, a substrate property; the foundation has a moderate optimum, and the only remaining lever is a physics change to the establishment dynamics, not tier-0 provisioning. |

*(Kept honestly: exp003 was a retracted false positive; exp009/010/011/018–020/028/036 are
informative **negatives**. The program is organized against closure, not for hype.)*

## Watch a world live

```bash
python -m omega.world run --dashboard          # live browser dashboard at localhost:8000
python -m omega.world run --checkpoint w.ckpt  # a world that persists across restarts
python -m omega.world snapshot --out world.html # a self-contained HTML snapshot
```

You'll see the **novelty pulse** (open-endedness made visible), a roster of **named lifeforms**
with real ages, transient **collective communities**, the growing constructed alphabet, cultural
transmission, a **world map**, and a "reach in" panel to seed life, trigger extinctions, or tune
the laws while it runs. See [`omega/docs/WORLD.md`](omega/docs/WORLD.md).

## Quickstart

Pure **Python 3.10+**, **standard library only — no dependencies to install.**

```bash
git clone https://github.com/homeo-x/alife && cd alife
python -m omega.cli list                    # list experiments
python -m omega.cli run exp030 --seed 0     # a completed transition to collective individuality
python -m omega.cli run exp002 --set bind=false   # a matched control
python -m unittest discover -s omega/tests  # run the test suite (89 tests)
```

More runnable one-liners are in [`examples/`](examples/).

## Why it matters

- **Open-ended evolution** is a central unsolved problem in ALife: real biology keeps inventing;
  our simulations almost always stall. Ω isolates *why*, and shows one mechanism that doesn't.
- **Major evolutionary transitions** (genes → cells → organisms → societies) are re-derived here
  as a single recursive move — and the exact substrate condition that enables them is measured.
- **Honest AI-relevance**: the self-improvement arc (Ω-0.24–42) asks whether evolved collectives
  could become mind-like — it ruled out every *selection* route with quantified negatives, located the
  blocker in the *substrate law*, and then **broke it**: competence compounds once the law grows with
  achieved competence (a network-visible reaction feedback), the exact analogue of how novelty stays open.

## Repository map

```
omega/kernel/       the immutable core: organizations, conservation, reactions, the universe
omega/experiments/  the physics plugins — every experiment as a gated mode (byte-identical when off)
omega/levels/       the recursive level tower (physics → chemistry → biology → culture)
omega/world/        the persistent, watchable, steerable world (runtime, checkpoint, dashboard)
omega/emergence/    novelty / construction / persistence trackers (the anti-closure signals)
omega/metrics/      open-endedness index and organization metrics
omega/docs/         the science: README (per-experiment), RESEARCH_LOG, ARCHITECTURE, LEVELS, WORLD, SCALING
studies/            one matched-control study + findings (EXP0NN_FINDINGS.md) per experiment
docs/               presentation: this banner, ROADMAP, CONTRIBUTING
```

## Status & roadmap

**Status:** the constructibility hypothesis is confirmed *in miniature* and consolidated; a
living world exists; the self-improvement question is answered with a located blocker. Full
history in [`omega/docs/RESEARCH_LOG.md`](omega/docs/RESEARCH_LOG.md) (milestones Ω-0.1 → Ω-0.49).

**Next frontier** (see [`docs/ROADMAP.md`](docs/ROADMAP.md)): the self-improvement arc closed by
*locating* the blocker — every route through selection, representation, replicators, and now
**competence reification** (exp049) leaves competence flat, because reifying a competent module hides
its structure in an opaque atom rather than raising the ceiling. The ceiling is set by the substrate's
**fixed reaction law**, so the one untried class of move is to make that **law itself competence-
dependent during the run** — a substrate change, not another selection knob. The other standing
frontier is **truly unbounded** construction: 10⁶–10⁷ ticks on the Ω-0.31 eviction-robust metric.

## License

MIT — see [`LICENSE`](LICENSE). Contributions welcome; please read
[`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) (the falsifiable, gated, byte-identical discipline
is the whole point).
