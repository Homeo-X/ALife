# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.37).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds — the self-improvement arc is COMPLETE (Ω-0.24–0.37).** A precise, honest,
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
  (1.09 vs 0.62, closure 0.36 vs 0.13) but competence stays **high-and-flat**, not rising. The arc's
  closing lesson: **open-ended novelty ≠ open-ended competence** — the world compounds *what it builds*
  (Ω-0.31), not *how good its collectives are*. Compounding competence is **not achieved** in either
  substrate; the real open problem is *what makes competence a rate, not a stock*.

## The next frontier (highest priority)

**1. Truly unbounded, not in-miniature.** Every open-endedness result is ≤ 300k ticks / few seeds.
With the Ω-0.21 instrument, run 10⁶–10⁷ ticks, multi-seed, and deep towers (50+), with a *streaming*
novelty metric that does not retain the full class registry. *Predicted falsification:* the novelty
rate finds a positive floor, or it dilutes to zero at some horizon.

## Secondary threads

- **Competence as a *rate*, not a *stock* (the arc's sharpened open problem).** exp048 closed the
  loop-back: part-level replicators lift the competence *ceiling* but competence still plateaus — the
  world has open-ended *novelty* but not open-ended *competence*. The Ω-0.20 lesson (open-endedness is
  a rate, sustained only by *continuing* construction) has never been applied to competence. The open
  question: is there a dynamical coupling that makes a collective's competence *keep rising* — a
  competence analogue of reification, where achieved competence feeds back to raise the ceiling itself
  — or is bounded competence intrinsic to selection over a fixed substrate? A matched-control yes/no,
  and the real unsolved problem the self-improvement arc isolates.
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
