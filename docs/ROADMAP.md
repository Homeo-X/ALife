# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.35).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds** — a precise, honest arc that keeps naming the next barrier (Ω-0.24–0.35).
  Collectives carry evolvable internal state (exp037) and are selectable on emergent coherence
  (exp038); developmental inheritance broke the exp028 heredity ceiling (exp040); a higher heredity
  level (exp041) and even a self-expanding scalar objective (exp042) don't compound → **goal
  representation** was missing; exp044 supplied it (a heritable, composable target path) → the arc's
  first over-generations **deepening**, but *transient* and without lifting competence → **credit
  assignment**; exp045 aimed the goal at the closure core (no compounding → credit is a representation
  problem, put it in the fitness); exp046 put a heritable per-part credit model in the fitness (**still
  no compounding, worse than plain closure selection**) → the limit is the **selection grain**: deme
  reproduction copies a whole propagule and cannot retain the credited *parts*.

## The next frontier (highest priority)

**1. Within-collective selection (exp047).** exp046 ran the arc's predicted falsification: an explicit,
heritable per-part credit model in the deme fitness still did not make competence compound (and
underperformed instantaneous closure selection), because whole-deme reproduction cannot preferentially
keep the high-credit *parts* against within-deme drift — the credit signal is necessary but the
selection **grain** is wrong. The decisive next experiment adds a **second selection level *below* the
deme**: bias which members survive decay / seed the next generation by their credit (parts competing
*inside* the collective), so competence-causing parts are differentially retained within a deme, not
only across demes. Then test whether competence finally compounds. *Predicted falsification:* if parts
competing within the collective still don't compound, the limit is not the grain but the substrate's
lack of a *heritable part-level replicator* (a part that copies itself with its credit) — pointing back
to the exp012 von-Neumann-replicator lesson one level up.

**2. Truly unbounded, not in-miniature.** Every open-endedness result is ≤ 250k ticks / few seeds.
With the Ω-0.21 instrument, run 10⁶–10⁷ ticks, multi-seed, and deep towers (50+), with a *streaming*
novelty metric that does not retain the full class registry. *Predicted falsification:* the novelty
rate finds a positive floor, or it dilutes to zero at some horizon.

## Secondary threads

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
