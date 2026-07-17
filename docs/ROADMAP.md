# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.30).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds** — the self-improvement machinery is present, the heredity ceiling is broken, and
  the remaining blocker is now precisely located (Ω-0.24–0.30): collectives carry evolvable internal
  state (exp037) and are selectable on emergent coherence (exp038); developmental inheritance broke
  the exp028 heredity ceiling (exp040, 8–9× null, world still open); but exp041 showed a higher
  heredity *level* is **not enough** (competence erodes under a fixed objective), and exp042 showed
  even a **self-expanding** objective does not ratchet — it is *worse*, because a moving scalar bar
  flattens its own selection gradient and the substrate has no *goal* to reify. The barrier is now
  **goal representation**, and it needs new representational machinery, not another selection rule.

## The next frontier (highest priority)

**1. Heritable, composable goals (a representational faculty, not a selection rule).** exp042 ran the
arc's predicted falsification: even a *self-expanding* objective (a monotonic competence bar chasing
the frontier) failed to make competence ratchet — worse than the fixed objective, robustly across
chase-rates — for two reasons past the objective's mobility: a self-referential bar **removes its own
selection gradient** once competence stops rising, and, more deeply, the bar is a single
**non-heritable, non-composable scalar** — the substrate can reify *structure* (Ω-0.20) but has no
representation of a *goal* to reify. The decisive next experiment (exp043) is therefore a **substrate
extension**: give collectives a *transmissible, mutating, recombining representation of what to build
next* (a goal that inherits and composes like the type-path structure does), then test whether
competence ratchets. *Predicted falsification:* if heritable goals still don't compound, the missing
piece is not representation but *credit assignment* — the collective cannot tell which of its parts
caused its competence — which would redirect the arc a third time.

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
