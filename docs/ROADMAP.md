# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.41).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds — the self-improvement arc is COMPLETE (Ω-0.24–0.38).** A precise, honest,
  falsifiable sequence that ruled out every selection/representation route to compounding collective
  competence and terminated in a *substrate* reason. Collectives carry evolvable state (exp037) and
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
  of the measured network. The arc's closing lesson: **open-ended novelty ≠ open-ended competence** — the
  world compounds *what it builds* (Ω-0.31), not *how good its collectives are*. Compounding competence is
  **not achieved** in either substrate by any selection/representation/replicator/reification move; the
  competence ceiling is set by the substrate's **fixed reaction law**, and the one untried class of move
  is to make that law itself competence-dependent *during the run*.

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

- **Competence via a mid-run change to the substrate law — the arc's *last* untried move (exp053).**
  Two levers have now been tried and both raise the competence *level* without tilting the *slope*.
  exp049 reified competent modules to new atoms — no compounding (the atom is **opaque**, hiding the
  structure out of the measured network). exp052 (Ω-0.41) grounded a **Red Queen** (a receding,
  coevolutionary target): it is the strongest competence-*level* lever the program has found — coevolve
  competence 0.820 beats plain closure selection (0.673) and the frozen-rival control (0.630, a +0.19
  receding-target effect), with healthy rising network survival — **yet competence still does not
  compound** (slope −0.021). Both confirm: the ceiling is set by the substrate's **fixed reaction law**,
  and selection/coevolution move the plateau but not the rate. The one class of move never tried is to
  make that **law itself competence-dependent during the run** — a **Catalytic Law**: promote a
  collective's achieved closure loops to shared *reactions* (not opaque atoms), so competent structure
  becomes new construction *operations* later collectives build on. **exp053** (the user's staged plan)
  combines it with the Red Queen: the receding pressure plus a substrate-level feedback that could turn
  that pressure into a rising ceiling. A substrate change, not a selection knob — the real open problem.
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
