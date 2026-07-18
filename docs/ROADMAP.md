# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.36).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds — the self-improvement arc is COMPLETE (Ω-0.24–0.36).** A precise, honest,
  falsifiable sequence that ruled out every selection/representation route to compounding collective
  competence and terminated in a *substrate* reason. Collectives carry evolvable state (exp037) and
  selectable coherence (exp038); developmental inheritance broke the exp028 heredity ceiling (exp040);
  a higher heredity level (exp041) and a self-expanding scalar objective (exp042) don't compound →
  **goal representation** missing; exp044 supplied it (heritable composable goals → first
  over-generations deepening, but transient) → **credit assignment**; exp045 (aim goal at closure) and
  exp046 (credit in the fitness) still don't compound → the **selection grain**; and exp047 (within-
  collective selection) **collapses the collective** → the terminal diagnosis: **competence is
  irreducibly collective, and its parts are not replicators**. Compounding self-improvement would need
  a substrate whose *parts are themselves replicators* (carrying context-independent heritable value —
  the exp012 `C·x → C` lesson), not another deme-selection knob.

## The next frontier (highest priority)

**1. Truly unbounded, not in-miniature.** Every open-endedness result is ≤ 300k ticks / few seeds.
With the Ω-0.21 instrument, run 10⁶–10⁷ ticks, multi-seed, and deep towers (50+), with a *streaming*
novelty metric that does not retain the full class registry. *Predicted falsification:* the novelty
rate finds a positive floor, or it dilutes to zero at some horizon.

## Secondary threads

- **Part-level replicators (the self-improvement arc's loop-back).** exp047 concluded collective
  competence can't be made to compound by selection because competence is irreducibly collective and
  the type-path parts aren't replicators. The decisive follow-on revisits exp012's genuine replicators
  (behaviour-first SKI soup, `C·x → C`): does a substrate whose *parts* carry and copy their own
  context-independent heritable value let collective competence compound where the type-path substrate
  could not? A yes/no with the same matched-control discipline, closing the arc's end back to its start.
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
