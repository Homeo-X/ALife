# Project Ω — Architecture

## The one-sentence design

A universe is an unordered **soup of Organizations** plus a **reservoir** of free
distinguishability; it evolves only by applying conservation-checked **Reactions**
proposed by a pluggable **Physics**; everything measurable is a property of
**classes** (continued recognizability), not instances.

## Layers (dependency flows downward only)

```
experiments/         exp001..003 — each supplies a Physics + Config
   │  (registry, harness: identical instrumentation for all)
   ▼
metrics/             novelty, complexity, persistence spectrum, Open-Endedness Index
emergence/           read-only detectors: persistence, novelty, construction
   │
   ▼
kernel/              Organization, Reaction, Transform, Universe, Scheduler, Conservation
   ▲
   │
substrate/           Noise (determinism), DifferenceSource, Constraint, Gradient
```

* **kernel** knows nothing about any experiment. Physics is a `Protocol`
  (dependency inversion): the scheduler calls `physics.propose(...)` without ever
  importing a concrete physics.
* **emergence** and **metrics** are strictly *observational* — they never mutate
  the universe. A positive reading is thus evidence about the substrate, not about
  the detector that produced it.
* **substrate** supplies raw materials only; nothing there is organized.

## The immutable kernel (the only fixed things)

| Invariant | Where it lives | How it is enforced |
|-----------|----------------|--------------------|
| **Identity** = continued recognizability | `Organization.cls` (canonical hash of state) | metrics track classes, not uids |
| **Consistency** | `canonical_cls`, `distinguishability` are pure functions | same state ⇒ same identity & mass, always |
| **Causality** | `Universe.apply_reaction` is the *only* mutation path | `Organization` is frozen; nothing changes in place |
| **Conservation of distinguishability** | `conservation.verify_conservation` | asserted every tick by the scheduler |

Everything else — space, decay, the operator set, even the laws — is supplied by a
Physics and may be discovered, rewritten, or abandoned.

## Core data structures

* **`Organization`** *(frozen dataclass)* — `uid`, `state` (nested tuple of
  atoms), `kind`, `birth_tick`, `lineage`. Derived: `cls`, `distinguishability`,
  `depth`. Immutable so identity and history stay cleanly separated (dynamic
  bookkeeping lives in `OrgStats`).
* **`Reaction`** — a proposed causal event: `inputs`, `consume` (subset actually
  destroyed; catalysts are in `inputs` but not `consume`), `outputs`
  (`(state, kind)` pairs), `via`. A reaction with no inputs draws novelty from the
  reservoir (a "feed").
* **`Transform`** — a named, arity-typed law; `catalytic` and `discovered` flags.
  Discovered transforms are the open-endedness signal.
* **`Universe`** — holds `organizations`, `stats`, `reservoir`, `transforms`
  (mutable law registry), `class_registry` (+ `class_births`), and `relations`.
  Owns `spawn` / `dissolve` / `apply_reaction` — the conservative mutation API.
* **`Physics`** *(Protocol)* — `seed(universe, rng)` and
  `propose(universe, rng) -> [Reaction]`.

## The universe loop (`Scheduler.step`)

Not `for particle in particles`. Each tick:

1. **Observe** — snapshot the class census; accumulate recognizability / births.
2. **Propose** — `physics.propose` returns candidate reactions.
3. **Constrain** — enact them in randomized order; each is conservation-checked
   and fails closed if an input was already consumed.
4. **Decay** — every organization faces the *same* uniform dissolution hazard.
   Persistence is never granted; a class survives only if production keeps pace.
5. **Measure** — recorders append the time series.
6. **Verify** — assert conservation. A failure is a kernel bug, never physics.

The loop is a pure function of the seed ⇒ deterministic replay.

## Determinism & serialization

A single `Noise(seed)` drives *all* stochastic choices (difference generation,
reaction ordering, decay, operator sampling). `Config` round-trips through JSON;
`RunResult.to_json` writes the full time series plus the embedded config, so any
result is reproducible from the file that produced it.

## Extending the framework

Add an experiment by writing a `Physics` and a `@register("expNNN")` builder in
`experiments/`. The harness gives it the standard instrumentation for free. Add a
metric as a pure function over `Universe` in `metrics/`. Add a discovered-law
mechanism by having your Physics call `universe.register_transform(...)` when it
detects a new organizational law in the soup (see `exp003`).
