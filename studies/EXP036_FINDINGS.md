# exp036 — Intrinsic function: selection for anticipation is *not enough*

The self-improvement discussion identified two engine pieces missing from the usual "amplifier"
levers (heredity, memory, architecture): **(1) a reason for computation to be selected** and
**(2) a substrate that can represent it**. exp036 tests the first in isolation, and in doing so
exposes the second — the program's third instance of the same lesson (after exp010 "construction ≠
reproduction" and exp011 "function must be intrinsic, not bolted on").

## Setup

The environment is given a **regularity worth predicting**: a **cyclic feed** whose favoured band
of atoms rotates every `feed_period` ticks (4 seasons over the 32-type alphabet). Demes are
selected for **anticipation** — `deme_fitness="anticipation"` rewards a deme whose recent products
already contain the atoms the *next* season will favour. Matched controls isolate cause from
environment (all gated; `feed_pattern="random"` / other fitness ⇒ exp001–035 byte-identical):

| condition | feed | selection |
|-----------|------|-----------|
| **treat** | cyclic (structure present) | anticipation (structure selected) |
| **network-ctrl** | cyclic (structure present) | network (structure *not* selected) |
| **random-null** | random (no structure) | anticipation (nothing to anticipate) |

Metric (rate, not cumulative): over a late window, the fraction of the population's atoms lying in
the **current** season's band (*reactivity*) and the **next** season's band (*anticipation*), vs
chance = 1/bands = 0.25.

## Result (4000 ticks, 3 seeds)

| condition | P(current band) | P(next band) |
|-----------|:---------------:|:------------:|
| treat (cyclic + anticipation) | 0.272 | 0.269 |
| network-ctrl (cyclic + network) | 0.288 | 0.274 |
| random-null (random feed) | 0.245 | 0.240 |

- **Reactivity is real but weak:** under a cyclic feed the population tracks the *current* season
  slightly above chance (0.272 vs 0.245 for random; +0.022). The environment does contain
  exploitable structure.
- **Anticipation does not evolve:** selection for anticipation adds **nothing** — treat's
  P(next band) is **−0.005 vs the network control** (0.269 vs 0.274) and only +0.019 vs chance,
  which is just the reactivity bleeding into the "next" measurement. Robust across `feed_period`
  ∈ {80, 150, 300} (anticipation gain < 0.02 everywhere).

## Interpretation — the third wall: you cannot select for what the substrate cannot represent

This is a **negative-with-diagnosis**, and it is the sharpest statement yet of what stands between
Ω collectives and minds. Selection pressure for prediction is **necessary but not sufficient**: a
deme can be *reactive* (its products reflect the atoms currently being fed) but cannot be
*anticipatory*, because the substrate gives a collective **no internal state that represents
environmental timing** — no clock, no memory of the season's phase, no variable it could set now to
pay off later. With nothing to vary, there is nothing for selection to act on, so anticipation
fitness ≈ network fitness. This mirrors exp010 (a replicator needs von Neumann self-reference the
substrate lacks) and exp011 (function must be intrinsic): **intrinsic function requires a substrate
that can hold predictive state, not just a fitness function that rewards it.**

## What it means for the roadmap

exp036 was the "engine piece #1" (selection for function). It shows piece #1 is inert without
**engine piece #2 — per-collective evolvable internal state** (exp037: a collective carrying its
own heritable, mutable construction rules / memory). The correct reading is not "anticipation is
impossible in Ω" but "anticipation cannot be *selected into existence* until collectives can
*represent* it." That is exactly what the next rung supplies.

## Reproduce
`PYTHONPATH=. python3 studies/exp036_anticipation.py 4000 3` → the table above; committed as
`studies/exp036_results.json` / `_console.txt`. Mechanism pinned by `test_exp036_*` in
`omega/tests/test_experiments.py`; all gated knobs off leave exp001–035 byte-identical.
