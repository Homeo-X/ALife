# The Collective-Individuation Arc (exp017 → exp030)

A single investigation, run as a falsifiable lab notebook, of one question the earlier
program handed forward from exp016 (obligate hypercycles — "organizations made of
organizations"):

> **Once you have collectives, does selection act on the collective — a major
> evolutionary transition to a higher level of individuality?**

Each rung is a gated, byte-identical addition to `omega/experiments/exp012_combinator.py`,
a matched-control study in `studies/`, and a claim pinned in
`omega/tests/test_experiments.py`. Full per-experiment detail is in the `EXP0NN_FINDINGS.md`
files; this is the through-line.

## The three phases

### Phase 1 — Is the multi-level machinery even the problem? (exp017–020)
Demes reproduce (extinction + propagule recolonization), with `source` (collective
heredity ON) vs a well-mixed `mixed` null.

- **exp017** multi-level selection + heredity → a **stalemate**: heredity plateaus, no
  between-deme winnowing, no collapse.
- **exp018** + heritable between-deme fitness variance → **no** winnowing; the only
  diversity drop is population collapse.
- **exp019** + patch-local feed → within-deme dominance rises to ~0.37 but no
  individuation.
- **exp020** + an explicit strong replicase → replicators consolidate the soup, but **as
  individuals** (`source` = `mixed` — the collective layer is inert).

**Verdict:** the multi-level structure is inert *because nothing group-selectable
emerges* — every trait that varies between demes is individual-level.

### Phase 2 — Give it a group trait; find what individuation needs (exp021–024)
- **exp021** an *imposed* cooperation trait (individually costly, collectively beneficial)
  → **group selection works** (textbook Price/Hamilton) — the machinery is sound; the
  trait was missing.
- **exp022** an *emergent* group trait = a deme's internal **cross-production network** →
  genuinely heritable and selectable, with a novel transmission threshold.
- **exp023** niche construction (recycle a deme's own products as feed) → first lever to
  lift within-deme dominance (0.25→0.32), but it homogenizes globally, not per-deme.
- **exp024** combine every lever + forced monoculture founding → **no** individuation,
  and the diagnosis: a **substrate type-space wall** — ~9 attractor normal forms, so 24
  demes can't hold distinct identities.

### Phase 3 — Represent identity right, then fix the substrate (exp025–030)
- **exp025** define deme identity as its **network signature** (edge-set), not a dominant
  class → more heritable than the class (1.6×) and a richer identity space — part of the
  "missing" individuation was a measurement artefact.
- **exp026** a richer *interacting* combinator basis (B/C/W; inert data atoms were rejected
  — they kill cross-production) → heredity 1.6×→2.4×, novelty *up*. Breed-true selection
  adds a bounded, canalizing push.
- **exp027** dose-response over the basis (3→11 combinators) → a **Goldilocks optimum**:
  heredity peaks at ~3.3× (7–8 combinators) then falls as too-rich a type space stops
  networks breeding true.
- **exp028** is the ceiling transmission- or substrate-limited? A network-biased propagule
  (even transmitting the *whole* deme) can't break ~3× → **substrate-limited**: the
  reduction dynamics don't re-form a deme's network even from identical members.
- **exp029** the substrate pivot — a **typed** substrate (morphisms + modular composition)
  → networks breed true (self 0.10→0.24, ratio ~5×), **but closed** (novelty→0). The two
  substrates are opposite corners of one trade-off: open-ended-but-unreproducible vs
  reproducible-but-closed.
- **exp030** an **open-ended AND modular** substrate — variable-length type **paths**
  composed by concatenation, with a `type_resolution` dial → the **"both" corner**
  (n_types 32–64, res 2–3): strong reproducible heredity (self 0.22–0.28) **and** sustained
  novelty (0.1–0.4 > 0) **and** rich networks (x-prod 4–7). **A completed transition to
  collective individuality, in miniature.**

## The one-line result

| corner | substrate | heredity (self) | open-ended (novelty) |
|--------|-----------|:---------------:|:--------------------:|
| open, unreproducible | combinator (exp027) | 0.10 (weak) | 4.5 |
| reproducible, closed | typed (exp029) | 0.24 (strong) | 0.0 |
| **both** | **typed_path (exp030)** | **0.22–0.28 (strong)** | **0.1–0.4 (open)** |

Collective selection was never the bottleneck; the bottleneck was a substrate that could
make a deme's collective phenotype **both heritable and open-ended**. A modular,
open-ended substrate (path-morphisms with bounded identity resolution) provides it.

## What remains — now measured (exp032, Ω-0.17)

The frontier the whole program shares (Ω-0.1, Ω-0.10, Ω-0.14) — show it **unbounded** — was
tested at scale in exp032 and comes out **affirmative in miniature on both axes**, with honest
edges. *Within a level:* at the both corner, collective heredity persists robustly (self ≫
null, flat, to **120k ticks**) and novelty stays open (> 0 every window vs the closed
control's exact zero) — sustained, not transient; the one open edge is whether the novelty
*rate* holds a positive floor or dilutes very slowly (unsettled even at 120k). *Of levels:*
the recursive tower has **no intrinsic depth ceiling up to 15** (a self-sustaining
fixed-point alphabet; 8/9 seeds reach the cap regardless of base), tempered by a stochastic
early-tier failure that can abort a tower. See `studies/EXP032_FINDINGS.md`. The
collective-individuality question is answered in miniature, and its unboundedness — the
program's original question — is now answered *in miniature* too, with the remaining edges
(a strictly non-decaying novelty rate; guaranteed tower formation) named rather than hidden.

## Coda — the transition recurses (exp031): multiple levels of organization

exp030 completed *one* transition; exp031 shows it **recurses**. Because a modular +
open-ended substrate lets a collective be heritable *and* open-ended, the same condition
holds when a tier's collectives become the next tier's atoms. `omega/levels/stack.py`
promotes each tier's stable heritable collectives to the next tier's alphabet and recurses:

- **A self-sustaining tower** — mean depth ~4, max 5 (physics → chemistry → biology →
  culture → meta-culture), *every* tier heritable (self > null) and open-ended (novelty
  ~0.4–0.5, undiminished up the tower). "Tower depth" is a new open-endedness axis:
  open-endedness *of levels*.
- **A distinct culture apex** — horizontal, Lamarckian motif transfer between collectives
  (~0.68× the vertical rate) that *accelerates innovation* (novelty 0.41→0.57), memes
  recombining across collectives faster than reproduction.

So organizational complexity in this substrate is a **recursive ladder of individuality**:
physics → chemistry → biology → culture as successive outputs of one engine, each level's
individuals composed of the level below. See `studies/EXP031_FINDINGS.md` and
`omega/docs/LEVELS.md`.

## Reproduce

Each `studies/exp0NN_*.py` runs its study (`PYTHONPATH=. python3 studies/exp0NN_*.py`);
results are committed as `studies/exp0NN_results.json` / `_console.txt`. The registered
builders are `exp017`…`exp030` plus `exp031_culture` in
`omega/experiments/exp012_combinator.py`; the level tower is `omega/levels/stack.py`; every
claim is pinned by a `test_exp0NN_*` / `test_exp031_*` in
`omega/tests/test_experiments.py` (39 tests).
