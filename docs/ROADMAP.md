# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.27).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds** — the self-improvement machinery is present but the blocker is located
  (Ω-0.24–0.27): collectives can carry evolvable internal state and be selected on emergent
  coherence, but **competence cannot compound until collective heredity beats the exp028 ceiling**.

## The next frontier (highest priority)

**1. Break the collective-heredity ceiling.** exp039 showed the single quantified blocker between
Ω collectives and self-improvement: whole-network transmission fidelity (~3–5× null,
substrate-limited since exp028). The decisive experiment is a substrate where a collective's
*entire* cross-production network is transmitted with **high fidelity** (not sampled), then re-run
the capstone: does competence finally compound (closure **and** heredity **and** function rising
together over generations)? *Predicted falsification:* if fidelity rises but competence still does
not compound, the barrier is deeper than heredity.

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
