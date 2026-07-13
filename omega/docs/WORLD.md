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

## Geography (space)

The kernel stays spaceless — space is *a constraint a Physics imposes on which organizations
may react* (the README's rule), grown from the existing deme/patch structure. With `space` on
(default in the `world` builder), the patches are laid on a **W×H torus** and locality becomes
geography: **migration** hops only to a neighbouring patch, and an extinct patch is
**recolonized preferentially from a nearby survivor** (a steep `0.25^distance` kernel) — so
founding is local. The dashboard shows the **world map**: each cell a patch, hue = its dominant
lifeform, brightness = population; regions differ and drift over time. Gated: `space=False`
(everywhere except the world) is byte-identical to the pre-space engine.

*Honest finding:* class-level **isolation-by-distance is weak** here — the world's open-ended
novelty continuously mints unique classes in every patch, so neighbours share little *class*
composition regardless of proximity. Geography lives in local migration/founding and in
per-patch heterogeneity (the map), not in class overlap — open-endedness actively works against
class-level biogeography, which is itself a real observation.

## Interaction (reach in)

A running world is steerable. `World` exposes conservation-respecting perturbations, also on the
dashboard ("reach in" panel) via a `POST /act` endpoint applied *between* chunks (no race with
the stepping thread):

- `seed_life(n, patch)` — inject organisms (spawns from the reservoir; conservative).
- `shock(magnitude, patch)` — a mass-extinction pulse (globally or in one region; dissolving
  returns quanta to the reservoir).
- `set_law(name, value)` — tune a law live (`mut_prob`, `horizontal_transfer`, `reify_period`,
  `mig_rate`, `decay_hazard`) and watch the world respond.
- `reify_now()` — force a persistent motif into a new primitive.

Every perturbation is appended to a **replay log** (`world.interactions`, checkpointed). By
design, a *touched* world is no longer a pure function of its seed; an **untouched** world stays
fully deterministic (pinned by `test_world`).

## Honest notes

- **Bounded novelty is horizon-windowed.** With memory bounded, a class evicted after
  `memory_horizon` ticks of absence and later reappearing counts as newly discovered — so the
  world's novelty rate is a *windowed* rate, not an all-time one (see `SCALING.md`). It cleanly
  shows the world stays open; it is not a cumulative census.
- **Scope.** v1 was the *watchable* foundation; v2 adds **geography** (space) and **interaction**
  (reach in). The remaining follow-on the runtime enables is **embodied agent minds** (perceiving,
  acting inhabitants) on top of this spatial, steerable world.
