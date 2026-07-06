# Project Ω (OMEGA) — Kernel v0.1

> Discovering the minimal computational substrate that permits *indefinitely
> increasing* organizational complexity. Not another ALife simulator: a research
> framework for testing one hypothesis —
>
> **Open-ended evolution does not require infinite space. It requires infinite
> constructibility.**

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
