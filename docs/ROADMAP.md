# Roadmap

Project Ω is a falsifiable research program, so this roadmap is a list of **open questions with
predicted falsification conditions**, not a feature backlog. Status is tracked milestone-by-
milestone in [`omega/docs/RESEARCH_LOG.md`](../omega/docs/RESEARCH_LOG.md) (Ω-0.1 → Ω-0.32).

## Where we are

- **Constructibility, not space** — confirmed *in miniature* and consolidated (Ω-0.1 → Ω-0.20):
  reification sustains open-endedness; a modular+open-ended substrate yields reproducible
  collective individuals that stack into a recursive level tower; sustaining novelty needs
  *continuing* construction (a rate, not a stock).
- **Scale** — bounded-memory long-run mode + a 3× faster kernel, validated (Ω-0.21).
- **A living world** — persistent, checkpointing, watchable, spatial, steerable (Ω-0.22–0.23).
- **Toward minds** — the arc reached its **first sustained compounding** (Ω-0.24–0.32): collectives
  carry evolvable internal state (exp037) and are selectable on emergent coherence (exp038);
  developmental inheritance broke the exp028 heredity ceiling (exp040); a higher heredity level
  (exp041) and even a self-expanding scalar objective (exp042) still don't compound → the barrier was
  **goal representation**; and exp044 supplied it — a *heritable, composable target path* — producing
  the arc's first over-generations **ratchet** (goal depth 2.4→4.0, max 10, vs a fixed-goal control
  pinned at 2). But the ratchet is **narrow and costly**: chasing a deeper idiosyncratic goal
  *cannibalizes* generic competence (closure/heredity/breadth). The barrier is now **goal alignment /
  credit assignment**.

## The next frontier (highest priority)

**1. Goal alignment / credit assignment (exp045).** exp044 confirmed exp042's diagnosis from the
other side — given a heritable, composable goal the collective *does* accumulate deeper achievements
across generations (the first compounding in the program) — but the represented goal ratchets
*itself*, not general competence, and the two are in tension: selecting for deeper goal-achievement
trades away closure and heredity. The decisive next experiment makes goal reification **align with the
collective's own self-maintenance** — extend a goal only in directions that *increase* the deme's
closure/heredity/breadth (credit-assign the goal to what actually makes the collective competent) —
then test whether the now-aligned ratchet lifts generic competence instead of cannibalizing it.
*Predicted falsification:* if aligned goals still trade off, the collective genuinely cannot
attribute its competence to its parts, and the missing faculty is an explicit **credit-assignment
mechanism** (which parts caused achievement), not just an aligned target.

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
