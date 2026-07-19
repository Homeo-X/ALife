# Project Ω (OMEGA) — the detailed record

> 🔭 **New here? Start with the [top-level README](../../README.md)** for the big-picture
> overview, the headline results, and how to watch a living world. *This* document is the dense,
> per-experiment scientific record — every yes/no question, control, and number.

> Discovering the minimal computational substrate that permits *indefinitely
> increasing* organizational complexity. Not another ALife simulator: a research
> framework for testing one hypothesis —
>
> **Open-ended evolution does not require infinite space. It requires infinite
> constructibility.**

```
   the whole program on one page
   ──────────────────────────────
   physics  (the kernel: atoms, conservation, reactions — the only fixed laws)
      │  compose + REIFY persistent structure into new primitives      ← keeps a bounded world OPEN
      ▼
   chemistry → biology → culture   (a recursive tower: each tier's heritable
      │                             collectives become the next tier's atoms)
      ▼
   a living world  (persistent · watchable · spatial · steerable)
      │
      ▼
   toward minds?  (machinery present; collective-heredity ceiling is the located blocker)
```

Everything is an **Organization**: a persistent arrangement of interacting
differences. Space, time, matter, and life are *not* primitives; if they appear
they must appear as organizations. The only fixed laws are identity, consistency,
causality, and conservation of distinguishability. See
[`ARCHITECTURE.md`](ARCHITECTURE.md) for the design and
[`RESEARCH_LOG.md`](RESEARCH_LOG.md) for the science (including why this line
departs from the earlier CA/Lenia prototypes in the parent directory).

## Requirements

Pure Python **3.10+**, standard library only. No third-party dependencies.

## Quickstart

```bash
# from the parent directory (the one containing the `omega/` package)
python -m omega.cli list                     # list experiments
python -m omega.cli suite --seed 0           # run the whole v0.1 suite
python -m omega.cli run exp003 --seed 1      # run one experiment
python -m omega.cli run exp002 --set bind=false   # the matched control
python -m omega.visualization.plot results/exp003_seed0.json   # text plots
```

Results are written to `results/<exp>_seed<seed>.json`, fully reproducible from
the embedded config.

## The experiment suite

Development proceeds strictly in sequence — never jump to organisms. Each
experiment answers one yes/no question against a control. Findings are stated as
the evidence supports them, including a retracted claim (that is the point of a
falsifiable program).

| Experiment | Question | Result (multi-seed) |
|------------|----------|---------------------|
| **exp001** noise | Can persistence emerge from pure noise? | **No** — null control; high novelty, zero re-formation |
| **exp002** binding | Can stable organizations emerge from local interaction? | **Yes**, but the possibility space is finite → **CONVERGED** |
| **exp003** construction | Can organizations author operators and enlarge the law set? | A *finite burst* of operators, then **freezes** → **CLOSED**. (v0.1 called this OPEN-ENDED; **retracted** — it was a cumulative-metric artefact.) |
| **exp004** reification | Can promoting persistent structure to *new primitives* keep the possibility space enlarging? | **Yes, sustained across seeds through 2000 ticks** → **OPEN-ENDED**; matched control (reify off) CONVERGES. Mild long-horizon decline. |
| **exp005** nesting ratchet | Is the decline fixable dilution, and is reification cumulative? | Dilution hypothesis **falsified** (a feed-only "fix" *freezes* the universe). The real lever is a **nesting ratchet**: ~150 new laws/1k sustained to 8000 ticks, lineage **depth 13** (primitives built from primitives), 68k classes. First **cumulative** open-endedness. |
| **exp006** depth ceiling | Is the depth-13 plateau a length cap? | **No** — sweeping the length cap 3× leaves depth flat (~12). Depth is a **rarity equilibrium** that **trades off against breadth**: loosening the bar to fight rarity explodes breadth (35× laws) but *lowers* depth. Unbounded hierarchy needs frontier-concentration, not global loosening. |
| **exp007** frontier reification | Can concentrating recurrence on the deepest primitives lift the ceiling? | **Yes** — a clean dose-response: frontier feeding lifts max depth **12 → 625** (~50×) as *quality* (mean depth 6→314), not gameable breadth. Genuinely branching (~3.3 primitives/level), not a linear counter. First **confirmed** prediction. |
| **exp008** toolkit / DAG richness | Is the deep hierarchy thin, and can reuse be enriched? | The DAG is **already combinatorial** (82–91% of reifications fuse ≥2 primitives). Depth and reuse are **separate axes**: frontier feeding buys depth, **toolkit feeding** (keep most-reused primitives abundant) buys reuse (peak reuse 11→340). Combined → deep *and* reused. Reuse forms a realistic **pyramid** (shallow core reused ~18×, deep apex terminal). |
| **exp009** deep modules | Can *deep* primitives become broadly reusable? | **No** (negative) — persistent module feeding leaves mean deep-reuse flat (~2.1) across a strong dose-response. The terminal apex is **intrinsic**: semantically-arbitrary deep structures have no reason to be reused across contexts. |
| **exp010** copying capstone | Does self-replication emerge if duplication is possible? | **No** (negative) — amplification doesn't rise with duplication (control matches it); dominance stays <5% (no takeover). **Construction ≠ reproduction**: a replicator needs von Neumann self-reference (an operator emitting a copy of *itself*) the string substrate lacks. |
| **exp011** function | Does selecting operators for what they *do* help? | **Marginal** (null) — coupling persistence to activity/generativity reshapes operators but barely moves novelty/discovery. Open-endedness is *form-driven*; function must be **intrinsic**, not bolted on. Three walls → pivot. |
| **exp012** behavior-first (SKI) | Does reproduction emerge if organizations *are* functions? | **YES — breakthrough.** In an SKI-combinator soup (identity = behaviour), genuine self-replicators emerge (`C·x → C`): thousands of self-catalysis events, ~20 lineages, vs **0** in the string soup. New wall revealed: replicator takeover *collapses* diversity — reproduction vs open-endedness. |
| **exp013** synthesis | Does adding heritable variation give open-ended *evolution*? | **YES — the goal, in miniature.** Mutation (imperfect reduction) turns takeover into a sustained, diversifying population: diversity held, replicator lineages grow (22→37), novelty doubles — reproduction *and* open-endedness together. A Goldilocks band, with an **error catastrophe** at high mutation (Eigen's threshold, unbidden). |
| **exp014** ecology | Do the evolving replicators *interact*? | **YES.** The cross-production graph shows **excess mutualism** (reciprocal production, z=+5.8 vs null) and **over-represented hypercycles** (3-cycles: 142 vs 52 null, z=+12.3), both *enriched by evolution*. No parasites (substrate has no shared-execution host to exploit). Real interaction structure emerges. |
| **exp015** knockout | Are the well-mixed hypercycles *functional* (obligate)? | **Weakly, not obligate.** Knocking out a member leaves partners at ~92% (vs ~109% random) — small effect (z −1.1 to −3.5). Redundancy dominates: partners survive. Diagnosis: too many alternative producers. |
| **exp016** locality | Does reducing redundancy (demes) make hypercycles obligate? | **YES.** A clean dose-response: partner survival on knockout falls 0.88 → 0.82 → **0.27** as patches go 0 → 12 → 24 (z=−35). Partners *collapse* when a member is removed. **Obligate hypercycles** — organizations made of organizations — emerge; locality also protects diversity. |
| **exp017** multi-level selection | Does selection act on the *collective*? | **In miniature, yes.** Demes reproduce (propagule); with high heredity fidelity (achieved by cutting feed dilution → heredity 3.2× vs null) between-deme diversity **winnows** under heredity (16.4→15.2) but **drifts up** under a heredity-free null (15.4→17.8) — the onset of a major transition. Modest, tuned, coexists with open-ended evolution. Central tension found: heredity fidelity vs feed-sustained diversity. |
| **exp018** collective fitness | Does heritable between-deme *fitness variance* make collectives win? | **No** — `source` ≈ `mixed`; the only diversity drop is population collapse. The multi-level structure is inert. |
| **exp019** local feed | Does a patch-local feed let a collective winnow? | **No** — within-deme dominance rises to ~0.37 but no individuation. |
| **exp020** replicase | Does an explicit strong replicator help the collective? | **No** — replicators consolidate the soup **as individuals** (colonize every deme); `source` = `mixed`. |
| **exp021** cooperation | Does group selection work given an *imposed* group-beneficial trait? | **YES** — textbook Price/Hamilton: `source` maintains cooperation far above `mixed` (gap +0.04→+0.22, decaying with cost). The machinery is sound; the trait was missing. |
| **exp022** emergent trait | Can a group-selectable trait *emerge*? | **Yes** — a deme's internal **cross-production network** is heritable and selectable (`source` up to 1.5× the mixed null), with a transmission threshold. |
| **exp023** niche construction | Does recycling a deme's products as feed individuate demes? | **Partly** — first lever to lift within-deme dominance (0.25→0.32), but it homogenizes globally, not per-deme, and costs novelty. |
| **exp024** individuation attempt | Do all levers + forced founder divergence individuate? | **No** — reveals a **substrate type-space wall**: ~9 attractor normal forms, so 24 demes collide onto ~13 shared identities. |
| **exp025** network identity | Is a deme's *network signature* a better collective identity than its dominant class? | **Yes** — more heritable (1.6× vs 1.5×) and a richer identity space; part of the "missing" individuation was a measurement artefact. |
| **exp026** richer basis | Does a richer *interacting* basis strengthen network heredity? | **YES** — adding B/C/W combinators lifts heredity 1.6×→2.4× with novelty *rising* (inert data atoms were rejected — they kill cross-production). Turns the substrate wall into a **dial**. |
| **exp027** substrate dial | How far does the dial go? | A **Goldilocks optimum** — heredity peaks ~3.3× at 7–8 combinators (S,K,I,B,C,W,T,V) then declines as too-rich a type space stops networks breeding true. |
| **exp028** transmission vs substrate | Is the ceiling fixable by better propagule transmission? | **No** — even transmitting the *whole* source deme caps at ~3×. The ceiling is **substrate-limited**: identical members ⇏ same network. |
| **exp029** typed substrate | Does modular composition break the reproducibility ceiling? | **YES, but closes.** A typed substrate (morphisms + modular composition) makes networks breed true (self 0.10→0.24, ~5×) but is **closed** (novelty→0). The two substrates are opposite corners of one trade-off. |
| **exp030** open-ended + modular | Can a substrate be *both* open-ended and modular? | **YES — the transition, completed in miniature.** Type **paths** composed by concatenation (modular *and* open-ended), with a tunable identity resolution, reach a **"both" corner**: strong reproducible collective heredity (self 0.22–0.28) **and** sustained novelty (0.1–0.4 > 0) **and** rich networks — which neither pure substrate could. |
| **exp031** levels of organization | Does the transition *recurse* into a tower of levels? | **YES.** Each tier's stable heritable collectives become the next tier's atoms (`omega/levels/`): the tower stacks **mean depth 4, max 5** (physics→chemistry→biology→culture→…), every tier heritable *and* open-ended. Plus a distinct **culture** level — horizontal/Lamarckian motif transfer (~0.68× the vertical rate) that **accelerates innovation** (novelty 0.41→0.57). |
| **exp032** unboundedness | Does it persist over 10⁵ ticks, and does the tower keep climbing? | **Affirmative in miniature, both axes.** At the both corner, heredity stays self ≫ null (≈4–5×, flat) and novelty > 0 every window out to **120k ticks** vs a closed control's exact zero (sustained, not transient — open edge: the novelty *rate* drifts down, positive-floor vs slow-dilution unsettled). The tower shows **no intrinsic depth ceiling to 15** — a self-sustaining ~fixed-point alphabet, 8/9 seeds reach the cap regardless of base (open edge: a stochastic early-tier failure can abort a tower). |
| **exp033** first-class levels | Is the tower one engine climbing itself, or are levels first-class? | **First-class.** With a different composition law per tier, the transition recurses *across a physics boundary*: a tower alternating two different open laws matches the self-similar baseline's depth (8/8 boundaries heritable). The one hard rung is **closure, not difference** — every tower containing the closed law caps at depth 1. The both-corner condition governs each level boundary. |
| **exp034** sustained novelty | Can the 120k novelty-rate decay (exp032's open edge) be arrested — and does it need *continuing* construction? | **Yes, and yes.** Turning the *reification* lever on (persistent motifs → new atoms) turns a baseline rate that halves (0.52→0.27 over 30k) into one that holds (0.53→0.67, **2.38× baseline** late) with heredity alive. And a 250k three-arm run shows it needs **continuing** construction: an arm that constructs then *stops* (capped) resumes decaying (ratio 0.67), while one that keeps constructing (→531 atoms) stays flat/rising (1.16). Constructibility is a **rate, not a stock** — the sharpest form of "constructibility, not space". |
| **exp035** new level law | Is the both corner special to the type substrates, or any open+modular law? | **Substrate-general.** A genuinely different law — binary-tree grafting, outside the type family — reaches the both corner (self>null + novelty>0, a closed↔open dial) and recurses in a path↔tree tower (same depth, 6/6 boundaries survived). A level needs the *condition*, not a specific engine — though linear concatenation's heredity is ~10× stronger than the tree law's. |
| **exp036** intrinsic function | Does selecting collectives for *anticipating* a structured environment produce prediction? | **No — negative-with-diagnosis** (the third wall). A cyclic feed (a "season" of atoms that rotates) is weakly *tracked* (reactivity +0.022 vs random), but selection for anticipation adds ~nothing over the control (next-band gain −0.005). You cannot select for what the substrate cannot *represent*: collectives have no internal state for environmental timing. Like exp010/011 — intrinsic function needs a substrate that can hold predictive state, motivating per-collective memory (exp037). |
| **exp037** evolvable architecture | Given heritable internal state, can a collective evolve its own construction rule? | **Yes (weak positive)** — the piece exp036 lacked. Each deme carries a heritable, mutable `type_resolution` (first-class *per collective*); under selection the population's rule **moves** (3.5→4.14) while a no-selection control stays put (3.03, gap +1.11). Honest edges: the signal is weak/noisy (the exp028 heredity ceiling) and it runs toward the proxy's extreme (openness, not the heredity corner) — Goodhart. Motivates exp038 (select coherence). |
| **exp038** emergent coherence | Can internal coordination be an *emergent, selectable* target (not imposed)? | **Yes, but it trades off.** Autocatalytic closure (a deme's self-producing network fraction, read off the real network) is selectable — closure 0.064 > network 0.046 > size 0.028 — and emergent, unlike exp021's imposed coop bit. **But** selecting it *lowers* heredity (self 0.10 vs 0.21 under network selection): closure and heredity are competing axes. The lesson: **alignment is multi-objective** — every single proxy Goodharts. |
| **exp039** capstone | Does *multi-objective* selection make competence compound? | **Not by itself — the blocker is heredity.** Closure & heredity are independent (both-high demes exist), yet composite selection still can't compound: selection stacks a property only as fast as it's inherited, and collective heredity is the weak channel (the exp028 ceiling). The machinery is present; **high-fidelity collective heredity is the missing piece.** |
| **exp040** breaking the ceiling | Can collective heredity break past the exp028 ceiling? | **Yes.** Transmitting the *developmental niche* (seed offspring with a random fraction of the parent network's products) lifts heredity to **self ≈ 0.56 — ~4.1× the off baseline, decisively past the exp028 self ≤ 0.28 ceiling** (~3.4–4.3× null) — while a **partial** template keeps the world open: the **collective "both corner"** (heredity ✔ + novelty ✔), the exp030 logic one level up. Removes exp039's blocker → sets up exp041. *(Ω-0.33: earlier "8–9× / full-closes" figures were partly a hash-seed artifact; both-corner claim stands.)* |
| **exp041** does competence compound? | With the heredity ceiling broken, does aligned multi-objective selection make competence *compound* over generations? | **No — and the blocker moves.** The template raises the heredity *level* (**1.7× the composite-only control, 3.4× null**) and composite selection raises closure/function, but **heredity still declines every generation in all arms** (−4.5% to −13.6%/win) — no arm gets the three axes rising together. A higher heredity level is **necessary but not sufficient**. The remaining gap is a **fixed objective**: selection reaches the bar and mutation erodes fidelity, so nothing ratchets — the Ω-0.20 *"rate, not stock"* lesson one level up. Next: an **open-ended, self-expanding objective** (collective reification of *goals*). |
| **exp042** self-expanding objective | Make the objective itself grow (reward beating a moving competence bar, raised toward the frontier, never lowered) — does competence *ratchet*? | **No — and the moving objective is *worse* than the fixed one** (frontier 0.58 vs 0.99), robustly across chase-rates lr ∈ {0.1,0.25,0.5}. Two reasons, both past the objective's mobility: a bar chasing the frontier **flattens its own selection gradient** (→ drift; faster chase = worse), and the bar is a **non-heritable, non-composable scalar** — the substrate has no *goal* to reify. The barrier is **goal representation**: open-ended self-improvement needs *heritable, composable goals*, not just heritable structure (exp040) or a moving scalar (exp042). The first rung needing new *representational* machinery. |
| **exp043** settling openness (consolidation) | Is the long-run novelty a genuine positive floor, or eviction-window recycling? | **A genuine positive floor — and a correction.** A fixed-memory global-novelty sketch (a scalable Bloom "ever-seen" set; counts each class once *ever*) strips the recycling that bounded memory injects. At **300k ticks, 3 seeds** the open engine keeps discovering never-seen classes at **~0.13/tick** (≈61k distinct, flat ~2k registry), **decisively above the closed control's exact 0** (whose windowed "novelty" is 100% recycling). **But** the previously-reported *flat* windowed rate is **~4× inflated**; the true genuine rate is positive-but-**declining** (halves over 300k). The core claim is confirmed on a conservative metric and the "constant rate" overclaim retired; residual (does it asymptote > 0 at 10⁶–10⁷?) settled by **exp050**. |
| **exp050** settled at 10⁶ (consolidation) | Does the genuine-novelty floor *survive* the literal long horizon, or dilute to zero? | **Real — the floor holds an order of magnitude out.** At **10⁶ ticks, 5 seeds** the eviction-robust global rate falls 0.30→0.10 over the first ~400k ticks then **levels onto ~0.09 genuinely-new classes/tick for the whole second half** (~**130,600 distinct classes ever/seed**, registry flat ~3.1k), **decisively above the closed control's exact 0.0000** (144 classes, ever). The Ω-0.31 "slow decline" was a **transient**, not dilution — the curve decelerates onto a positive floor (67% early drop vs 18% late sag). "Stays open forever" is settled at the horizon the thesis is stated for; residual = a 10⁷ stress + deep towers at the long horizon. |
| **exp051** horizon stress (consolidation) | Does the ~0.09 floor *hold* past 10⁶, or resume declining? | **Holds — the Ω-0.39 caveat closed.** A **3× stress to 3M ticks** (mem_h fixed) shows the eviction-robust rate, after the transient (0.22→0.08 over the first 1M, a **64%** fall), goes **flat within ~14% across the final 2M ticks** (0.084→0.070, ~**281,400 distinct/seed**), decisively above the closed control's **exact 0.0000**. The decline is **decelerating toward an asymptote** (64%→14%), not descending to zero — log-like convergence to a positive floor. Residual: a 10⁷ stress (a ~14% sag isn't *mathematically* excluded) + deep towers at the long horizon. |
| **exp044** heritable composable goals (the frontier) | exp042 said the barrier is *goal representation* — give collectives a heritable, composable goal (a target path). Does competence ratchet? | **Deeper goals accumulate — the arc's first over-generations deepening — but transiently, and without lifting competence.** Composable goal depth climbs far above a matched *fixed*-goal control (per-window 2.6 → peak **4.3**, max **7** vs fixed pinned at 2): composability is the active ingredient, confirming exp042's diagnosis. **But** the depth is *hump-shaped* (overshoots then partially collapses — deeper goals outrun what the network can build), and generic competence is middling (composable 0.46 > fixed 0.39 > ratchet 0.30, but **< drift 0.60**). Barrier past goal representation = **goal alignment / credit assignment**. *(Ω-0.33: earlier "sustained 2.4→4.0" was a hash-seed artifact.)* |
| **exp045** goal alignment / credit assignment | Aim goal growth at the deme's own closure core (credit assignment). Does competence now rise *with* goal depth? | **No — and it's slightly worse (a clean negative).** Aligned competence (mean 0.38) is *below* the unaligned exp044 control (0.41), and **both goal arms are far below drift (0.63)**; aiming at the closure core didn't even raise closure (0.047 < 0.053 < drift 0.097). The reason: alignment moved the goal's *direction* but not the *selection pressure* (still achievement × depth), which is what trades off. **Credit assignment is a representation problem, not a targeting one** — it must live in the *fitness* (a heritable, selectable per-part contribution), not the goal. Next: **exp046**. |
| **exp046** credit in the fitness | Put an explicit *heritable per-part credit model* into deme selection (reward retaining the parts that cause competence). Does it compound now? | **Still no — and worse than plain closure selection (the limit is the selection *grain*).** Credit competence (mean 0.635, slope −0.008) sits *below* instantaneous closure selection (0.692) and barely above drift (0.627); it doesn't even raise closure (0.130 < 0.188). The credit signal is heritable and correct, but **deme-level reproduction copies a whole propagule — it can't preferentially retain the credited *parts*** against within-deme drift, so credit becomes a passenger. Necessary but not sufficient: the missing move is **within-collective selection** (parts competing inside the deme). Next: **exp047**. *(A 3-seed pilot's positive didn't survive 6 seeds — the Ω-0.33 lesson.)* |
| **exp047** within-collective selection | Add a second selection level *below* the deme — parts competing inside it by credit. Does competence finally compound? | **No — it *collapses* the collective.** Within-selection competence (0.363, declining) falls *below* deme-only credit (0.615) and drift, and network survival drops to **0.29** of demes (vs 0.43): selecting the "high-credit parts" strips out the complementary partners the cross-production network needs. **Competence is irreducibly collective** — not a sum of independently selectable part contributions — so part-level selection is self-defeating → compounding needs **part-level replicators** (the exp012 lesson), which the type-path parts lack. |
| **exp048** the loop-back (arc close) | Run the credit machinery on the **combinator substrate**, where parts *are* replicators (exp012 `C·x→C`). Does competence compound now? | **Part-level replicators lift the *ceiling* ~2× but don't close the *compounding* gap.** On the replicator substrate competence reaches **1.09** (vs typed_path 0.62) and closure **0.36** (vs 0.13), ~6× more classes — a large substrate effect that partly vindicates exp047. **But competence is high-and-*flat*** (all slopes ≈ 0), on either substrate, under credit or drift. The arc's closing lesson: **open-ended novelty ≠ open-ended competence** — the world compounds *what it builds* (Ω-0.31) but not *how good its collectives are*. The self-improvement arc (exp036–048) rests here; the real open problem is *competence as a rate, not a stock*. |
| **exp049** competence reification (arc's open problem) | Apply the Ω-0.20 rate-not-stock lever to *competence*: reify the most closure-central (achieved *competent*) module to a new atom every period. Does competence finally compound? | **No — competence stays a *stock* (the honest negative that closes the arc's open problem).** All arms flat: reify-closure slope +0.0006/win (mean 0.684), reify-freq +0.0022 (0.686), no-reify +0.0046 (0.673) — reifying *competent* structure is indistinguishable from reifying *common* structure or *not reifying*. Yet the reify arms grow the alphabet 32→51–53 atoms and find ~26% more classes (5.8k vs 4.6k): **novelty compounds while competence doesn't**, within one run. Why: promoting a competent module to an **opaque atom moves its structure *out* of the measured cross-production network** — a lateral move, not a ratchet. The Ω-0.20 lever **does not transfer** from novelty to competence; the ceiling is set by the substrate's fixed law. Any future route must change the **substrate law mid-run**, not grow its alphabet. |
| **exp052** the Red Queen (boldest lever) | Ground a *receding* target in real rivals — reward a deme's closure *plus* the fraction of its closure core a spatial rival can't yet produce (a coevolutionary arms race). Does competence compound now? | **The wall holds, but this is the arc's strongest ceiling-lifter.** coevolve competence **0.820** is the **highest of any arm** — beating plain closure selection (0.673) by +0.15, the frozen-rival control (0.630) by **+0.19** (isolating the *receding* target), and drift (0.615) — with the highest closure (0.255) and the **healthiest, rising** network survival (0.56→0.73; no collapse, unlike exp047). **But competence still doesn't compound** (slope −0.021): the arms race reaches a mutual-escape equilibrium (everyone running to stay in place), so the receding target raises the *plateau* but not the *slope* — the **level-not-rate** pattern of exp048, in its strongest form. First mechanism to beat closure selection on the same substrate; still a stock. Next: a **Catalytic Law** (exp053, Red Queen + promote closure loops to shared *reactions*). |
| **exp053** the Catalytic Law (arc's first positive) | Change the substrate law mid-run: promote the highest-competence deme's closure loop to a shared, network-visible *reaction* (`anchor → product`, not an opaque atom — the exp049 fix). Does competence finally compound? | **YES — the wall breaks.** In a 2×2 factorial (catalytic_law × {closure, redqueen}) **both catalytic cells compound** while both fixed-law cells stay flat: catalytic×Red-Queen rises **monotonically 0.89 → 1.24** (slope **+0.019/win**, mean **1.183** — the arc's highest level; closure 0.26→0.43 and survival 0.57→0.79 also rising), catalytic×closure +0.017; vs redqueen −0.021 and closure +0.004. A discriminating control (`catalyst_random`: promote a *random* edge from a *random* deme) climbs **3× shallower** (+0.006 vs +0.019) → the ratchet is genuinely **competence-dependent**, not mechanical injection. The competence analogue of Ω-0.20: promote achieved competence to a **reaction** (network-visible) and competence is a **rate**. **Open edge: saturation** (catalysts reached ~11–14 near the cap of 16; does it rise without bound?). |
| **exp054** the Earned Law (honest negative) | exp053 saturates (~1.45) — is it the bounded repertoire? Expand the *law itself*: let a competent lineage climb its construction reach (`type_resolution`) with achieved closure. Does an expanding law sustain the rise? | **No — depth is the wrong axis (a locating negative).** Saturation is **not** the catalyst cap (cap 16/80/400 byte-identical — only ~10 distinct closure-core edges ever qualify). And earning deeper construction **hurts**: earned competence **0.577** is the *lowest* arm (< fixed-law 0.800 < fixed-high cold-res8 0.742 < catalytic **1.224**), because deeper type-paths make cross-production sparser, so closure/competence *fall*; the greedy climb overshoots the optimum (reach ~3.67 ≈ res ~6.7). Competence has a **bias–variance ceiling** — too shallow exhausts competent structure (exp053), too deep starves cross-production (exp054) — so it saturates at the substrate's **optimal richness**, not because the law is fixed. Next: a *level transition* that adds a new *kind* of richness (exp055). |
| **exp039** capstone | Does *multi-objective* selection compound coherence + heredity into self-improvement? | **No — and the barrier is now located.** The trade-off is *not* fundamental (closure & heredity are independent across demes, corr −0.001), yet composite (maximin) selection lifts closure (0.078, highest) but **not** heredity (0.106 vs 0.209) — competence can't compound. Diagnosis: the **collective-heredity channel is too weak** (the exp028 ceiling). Machinery for self-improvement is present (exp037 evolvable state, exp038 selectable coherence); the missing piece is **high-fidelity collective heredity**, not more selection. |
| **exp033** first-class levels | Does the tower need one engine climbing itself, or can levels run *different* physics? | **First-class.** With a *different composition law per tier* (`run_stack(levels=…)`), the transition still recurses across the physics boundary: a tower of two different **open** laws stacks to the *same* depth as the self-similar baseline, **8/8 boundaries heritable**. The one hard rung is **closure** — a *closed* law (exp029) starves the next alphabet and caps the tower, so each level's law must itself be open **and** modular (the "both corner" condition, now between levels). |

### Levels of organization (physics → chemistry → biology → culture)

The transition to collective individuality is a **recursive ladder**, not a single jump:
a stable, heritable collective at level *N* is promoted to a single atom at level *N+1*,
and the same modular+open-ended engine (exp030) runs one tier up. The four analogues —
**physics** (kernel: atoms + conservation), **chemistry** (composition + reification),
**biology** (deme reproduction/selection/heredity), **culture** (horizontal, Lamarckian
transmission) — and the recursion are documented in [`LEVELS.md`](LEVELS.md), built by
`omega/levels/stack.py`, and evidenced in `studies/EXP031_FINDINGS.md`.

### The living world (`omega/world/`)

The same engine can be run not as a batch experiment but as a **persistent, watchable world**
— forever, at flat memory, with checkpoint/resume — its self-generating open-ended content
(lifeforms, collectives, cultures, never-ending novelty) made legible and alive. Watch it:

```bash
python -m omega.world run --dashboard            # live browser dashboard (localhost:8000)
python -m omega.world run --checkpoint w.ckpt    # persist + resume across restarts
python -m omega.world snapshot --out world.html  # a self-contained HTML snapshot
```

See [`WORLD.md`](WORLD.md). Scope is the *watchable* foundation; interaction, spatial
geography, and embodied agents are the follow-ons it enables.

The headline is the **exp003 → exp004 → exp005 arc**: a bounded alphabet forces
closure no matter how cleverly operators recombine (exp003); reifying persistent
structure into new primitives keeps the alphabet growing (exp004); and lowering the
recurrence bar for *nested* motifs — fuelled by feeding reified symbols back into
the pool — turns that into a **cumulative ratchet** of primitives-built-from-
primitives (exp005). Open-endedness came from enlarging, and then recursively
stacking, the vocabulary of difference — not from more space or time. Two of the
milestones along the way were *falsifications of my own prior claims*; see
[`RESEARCH_LOG.md`](RESEARCH_LOG.md) for the full story and the metric bugs found
and fixed.

```bash
python -m omega.cli study exp005 --seeds 3 --ticks 2000                     # the ratchet
python -m omega.cli study exp005 --seeds 3 --ticks 2000 --set feed_reified=false  # frozen control
python -m omega.cli study exp004 --seeds 3 --ticks 2000 --set reify=false   # earlier control
```

## Metrics (the only scorecard)

Vanity metrics (population, fitness, species count) are deliberately excluded —
they all saturate. We track what should *not* saturate in an open-ended universe:

* **novelty rate** — new organizational classes per tick (0 ⇒ closure)
* **persistence spectrum** — re-formation counts; *composed* persistence isolates
  maintained arrangements of ≥2 differences from lone re-appearing atoms
* **hierarchy index** — mean compositional depth
* **discovered operators** — laws the population authored at runtime
* **Open-Endedness Index** — a product-like combination that collapses if *any*
  of novelty / depth / operator-growth dies

If the Open-Endedness Index trends to zero, the universe has failed. That is the
falsification condition for the whole program.

## Tests

```bash
python -m unittest discover -s omega/tests -v
```

Covers kernel identity/causality, a randomized conservation property test,
determinism (same seed ⇒ identical run), and regression guards on each
experiment's scientific claim.

## Layout

```
omega/
  kernel/        Organization, Reaction, Transform, Universe, Scheduler, Conservation
  substrate/     Noise (determinism), DifferenceSource, Constraint, Gradient
  emergence/     read-only detectors: persistence, novelty, construction
  metrics/       complexity, novelty index, organization metrics, open-endedness
  experiments/   registry + harness + exp001..003
  visualization/ text-based time-series plots (zero-dependency)
  tests/         unit + property + scientific-claim tests
  docs/          README, ARCHITECTURE, RESEARCH_LOG
configs/         JSON configs for deterministic replay
results/         run outputs (generated)
```
