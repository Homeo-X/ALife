# The Ω World — the research engine as a watchable living world

Project Ω is a falsifiable research engine: batch runs → JSON/metrics. But its result is the
thing most virtual worlds lack — **content that generates itself, open-endedly, with nothing
hand-authored**: a physics→chemistry→biology→culture tower, novelty sustained by *continuing*
construction (Ω-0.20), heritable collective individuals (Ω-0.15), a cultural channel (Ω-0.16).
`omega/world/` turns that generative core into a **persistent, watchable world** — one you can
run forever and *watch* rather than measure to a horizon. It adds only what a world needs on
top of the engine; every kernel behaviour is unchanged (exp001–035 byte-identical).

## Run it

```bash
python -m omega.world run                      # headless: live terminal dashboard
python -m omega.world run --dashboard           # browser dashboard at http://localhost:8000
python -m omega.world run --checkpoint w.ckpt   # persist + resume across restarts
python -m omega.world snapshot --out world.html # a self-contained HTML snapshot (shareable)
```

A world resumes automatically when `--checkpoint` points at an existing file, so it **accretes
history across sessions** and survives container restarts.

## What you see (`omega/world/observe.py`)

- **The novelty pulse** — the windowed new-class-discovery rate over time. In a living world it
  never falls to zero; that pulse *is* open-endedness made visible.
- **Lifeforms** — the persistent organizational classes, named deterministically and shown with
  real ages (`ticks_present`), depth, and peak population. These are the stable characters you
  follow (e.g. *Tekuta*, alive 1,600+ ticks).
- **Collectives** — the live roster of cross-production **network communities** (deme
  signatures — the research's collective individuals). These are genuinely *transient* (networks
  reconfigure each generation), so they are shown as a current population, not aged.
- **Culture** — horizontal vs vertical transmission counts (memes spreading between collectives).
- **Construction** — the alphabet growing as persistent motifs are **reified** into new
  primitives (the lever that keeps novelty alive).
- **Event feed** — reification events and enduring lifeforms, diffed between snapshots.

## How it works

- **Runtime** (`omega/world/runtime.py`) — `World` owns the same live state the harness builds
  (`Noise`, `Universe`, physics, `NoveltyTracker`, `ConstructionTracker`) and advances in
  *chunks* forever, with **bounded memory always on** (Ω-0.21) — the reason an indefinite run is
  feasible. Chunking is transparent to the dynamics (a world is the same deterministic function
  of its seed as the equivalent batch run).
- **Checkpoint/resume** (`omega/world/checkpoint.py`) — atomically pickles the full state bundle
  (RNG state via `Noise.getstate`, universe, the whole physics object — whose large mutable state
  lives outside the universe — and the trackers); the scheduler is rebuilt on load. Guarantee:
  *resume-then-continue N ticks == run-through N ticks*, byte-identical (pinned by
  `test_world`).
- **World physics** — the registered `world` builder: the exp030 both-corner (`typed_path`) +
  collectives + reification + culture, i.e. the most-alive single-tier configuration.

## Honest notes

- **Bounded novelty is horizon-windowed.** With memory bounded, a class evicted after
  `memory_horizon` ticks of absence and later reappearing counts as newly discovered — so the
  world's novelty rate is a *windowed* rate, not an all-time one (see `SCALING.md`). It cleanly
  shows the world stays open; it is not a cumulative census.
- **Scope (v1).** This is the *watchable* foundation. Interaction (seeding/steering the world),
  spatial geography, and embodied agent minds are deliberate follow-ons the runtime enables, not
  part of v1.
