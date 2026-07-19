# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.42).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds — the self-improvement arc found the answer (Ω-0.24–0.42).** A precise, honest,
  falsifiable sequence that ruled out every *selection/representation* route to compounding collective
  competence, located the reason in the *substrate law*, and then **broke the wall** with a
  substrate-law feedback (exp053). Collectives carry evolvable state (exp037) and
  selectable coherence (exp038); developmental inheritance broke the exp028 heredity ceiling (exp040);
  a higher heredity level (exp041) and a self-expanding scalar objective (exp042) don't compound →
  **goal representation** missing; exp044 supplied it (heritable composable goals → first
  over-generations deepening, but transient) → **credit assignment**; exp045 (aim goal at closure) and
  exp046 (credit in the fitness) still don't compound → the **selection grain**; and exp047 (within-
  collective selection) **collapses the collective** → competence is **irreducibly collective**, and
  the type-path parts are not replicators. The loop-back (exp048) ran it on the combinator substrate,
  where parts *are* replicators (exp012 `C·x → C`): replicating parts **lift the competence ceiling ~2×**
  (1.09 vs 0.62, closure 0.36 vs 0.13) but competence stays **high-and-flat**, not rising. The loop-back's
  sharpened open problem — *what makes competence a rate, not a stock* — then got its own direct test:
  exp049 aimed the Ω-0.20 reification lever at competence (reify the most closure-central *competent*
  module to a new atom) and it **stays flat** (slopes ≈ 0; reifying competent structure is
  indistinguishable from reifying common structure or not reifying), even as the alphabet grows 32→53 and
  novelty compounds — because reifying a competent module hides its structure in an **opaque atom**, out
  of the measured network. This located the reason — the competence ceiling
  is set by the substrate's **fixed reaction law** — and named the fix: make the law itself
  competence-dependent, but keep the promoted structure *network-visible* (exp049 failed because a new
  *atom* is opaque). **exp053 (Ω-0.42) does exactly that and breaks the wall:** the **Catalytic Law**
  promotes the highest-competence deme's closure loop to a shared *reaction* (`anchor → product`, injected
  every tick, not an opaque atom), so competent structure becomes a reusable construction operation later
  collectives build on. Competence **compounds** — catalytic×Red-Queen rises monotonically 0.89 → 1.24
  (slope +0.019, the arc's highest level; closure and survival rising) where every fixed-law cell is flat,
  and a random-injection control (3× shallower) shows the ratchet is genuinely *competence-dependent*, not
  mechanical. The refined lesson: **open-ended novelty ≠ open-ended competence was true only for a *fixed*
  substrate law** — once the law grows with achieved competence (network-visibly), competence is a *rate*
  too, the exp053 analogue of the Ω-0.20 reification-of-novelty result. Open edge: **saturation** (does it
  rise without bound or fill the catalyst repertoire?).

## The next frontier (highest priority)

**1. Truly unbounded — the novelty axis is SETTLED and STRESS-TESTED (Ω-0.39–40); the tower axis is
not.** The streaming-novelty question is answered and stressed: on the eviction-robust global sketch the
open engine's genuine rate **finds a positive floor** (~0.09 new classes/tick; ~130k distinct at 10⁶ / 5
seeds, ~281k at 3M / 3 seeds; decisively above the closed control's exact 0), and a **3× horizon stress
to 3M ticks** (Ω-0.40) showed it stays **flat within ~14% across the final 2M**, decelerating (64%→14%)
onto a positive asymptote — not diluting. What remains open here is a **10⁷ stress** (a residual ~14% sag
means a very slow second-order drift is not *mathematically* excluded) and, separately, **deep towers
(50+ levels)** at the long horizon — tower depth has only been pushed in-miniature (Ω-0.17), never to 10⁶
ticks with the streaming instrument. *Predicted falsification:* at 10⁷ the floor finally dilutes to zero,
or tower depth hits an intrinsic ceiling under bounded memory. The tower axis is now the higher-value
open piece of "truly unbounded."

## Secondary threads

- **Does compounding competence rise without bound, or saturate? (the exp053 follow-on, now highest-
  value on the competence axis).** exp053 (Ω-0.42) **broke the competence-flat wall**: a **Catalytic Law**
  (promote the highest-competence deme's closure loop to a shared, network-visible *reaction*) makes
  competence **compound** — catalytic×Red-Queen rises monotonically to the arc's highest level (slope
  +0.019 vs flat fixed-law cells), and a random-injection control (3× shallower) confirms the ratchet is
  competence-dependent, not mechanical. The open question is now the **shape of the rise**: competence
  climbs over 12k ticks / ~600 generations, but the catalyst repertoire (`catalyst_max=16`) reached ~11–14
  near the cap, so a longer-horizon / larger-cap run must show whether competence keeps rising (a genuine
  unbounded ratchet — the strongest possible result) or saturates as the repertoire fills. *Predicted
  falsification:* the slope decays to zero once the repertoire is full → competence is a *larger stock*,
  not truly unbounded. Secondary: separate the mechanical injection floor (random ≈ +0.006) more tightly;
  test whether the Red Queen is necessary or merely maximal (catalytic×closure also compounds, +0.017).
- **A strong non-type law.** exp035's tree law reached the "both corner" only weakly (~10× lower
  heredity than linear paths). Is there a genuinely different law with *strong* both-corner heredity?
- **Fully heterogeneous per-level physics.** The tower is still largely the self-similar engine;
  make each level a qualitatively different law with its own promotion adapter.
- **World follow-ons.** The watchable, spatial, steerable world (Ω-0.22–0.23) enables: embodied
  agent minds that perceive and act; richer geography (emergent, not imposed); multi-user worlds.

## Engineering

- **Checkpoint/resume for multi-hour runs** (the RNG is picklable; the world already checkpoints).
- **Optimize the `normalize` reduction engine** — the dominant remaining per-tick cost.
- **CI on the default branch** (added) and coverage of the long-horizon studies as smoke tests.

## How to propose work

Open an issue framed as a **yes/no question with a matched control and a predicted falsification
condition**. That is the unit of work here — see [`CONTRIBUTING.md`](CONTRIBUTING.md).
