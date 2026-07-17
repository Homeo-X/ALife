# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.29).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds** — the self-improvement machinery is present, the heredity ceiling is broken, and
  the remaining blocker is now precisely located (Ω-0.24–0.29): collectives carry evolvable internal
  state (exp037) and are selectable on emergent coherence (exp038); developmental inheritance broke
  the exp028 heredity ceiling (exp040, 8–9× null, world still open); but exp041 showed a higher
  heredity *level* is **not enough** — under a **fixed** objective competence still doesn't compound
  (heredity erodes every generation). The barrier moved to **the objective itself**.

## The next frontier (highest priority)

**1. An open-ended, self-expanding objective.** exp041 ran the arc's predicted falisfication: with
the heredity ceiling broken (exp040), competence *still* did not compound under a fixed composite
target — the three axes (closure, heredity, function) do not rise together across generations,
because selection reaches a fixed bar while mutation erodes fidelity. So the barrier is deeper than
heredity: it is the **stock-vs-rate** problem one level up (Ω-0.20). The decisive experiment
(exp042) makes the *deme objective itself grow* — reward *increasing* closure/heredity/breadth
against a moving baseline, or promote a collective's achieved competence into the next target
(collective-level reification of *goals*, the analogue of substrate-level reification of
*primitives*) — then test whether competence finally **ratchets**. *Predicted falsification:* if a
moving objective still does not compound, self-improvement in this substrate needs a new
representational faculty (goals the substrate can't yet express), not just a moving target.

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
