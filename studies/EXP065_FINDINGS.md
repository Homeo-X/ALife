# exp065 — Memory pays, and only when the world requires it: internal state is selectable in a partially-observable season (Ω-0.54)

exp062 (Ω-0.51) showed a **reactive** agent — one that acts on the *instant* percept — is selectable in a
fully-observable sawtooth season. exp065 asks the deeper, cognition-facing question: does an agent with
**internal state / memory** — one that acts on the *history* of its percepts — pay when the instant percept
is insufficient? The answer is a clean **double dissociation**: memory pays *iff* the world is partially
observable, and it *hurts* when the world is instant-observable. That interaction — not a main effect — is
the signature that it is **memory itself** that is selected, not merely a different policy.

## Design (gated; `agent_policy=""` / `season_pattern="sawtooth"` ⇒ exp001–064 byte-identical)

A 2×2 that isolates memory:

- **season_pattern** — `sawtooth` (0,1,2,3,0,1,2,3,… — the current band **implies** the next: instant-observable)
  vs `triangle` (0,1,2,3,2,1,0,1,2,3,… — the current band does **not** imply the next; the season may be
  ascending or descending, so knowing the direction requires **remembering the previous season**: partially
  observable / a POMDP).
- **agent_policy** — `embodied` (reactive: forage the band `phi` away from the *perceived* current season,
  `phi` heritable — no memory) vs `memory` (carry internal state — the last observed season *direction* — and
  extrapolate it: `next ≈ clamp(cur + dir)`).

Selection is `deme_fitness="anticipation"` (reward products whose atoms fall in the **next** band). Anticipation
is measured as the fraction of live demes' product atoms in `_next_band`, averaged over a full season cycle
(chance = 0.25 with 4 bands).

## Result (5 seeds; anticipation over a season cycle; chance = 0.25)

| season | embodied (reactive) | memory | memory − reactive |
|:---|:---:|:---:|:---:|
| sawtooth (instant-observable) | **0.391** | 0.290 | **−0.101** |
| triangle (partially observable) | 0.320 | **0.364** | **+0.044** |

**Interaction (the double dissociation): +0.145.** Memory *out-anticipates* the reactive agent in the
partially-observable triangle season (+0.044), and *under-performs* it in the instant-observable sawtooth
(−0.101). The verdict logic (memory helps in triangle, does not help in sawtooth, interaction > 0.05) fires:
**MEMORY PAYS — AND ONLY WHEN THE WORLD REQUIRES IT.**

## Interpretation — the first rung of genuine cognition

In the **sawtooth** season the current band fully determines the next, so a fixed heritable phase (`phi=1`)
already anticipates perfectly; there is nothing for memory to add, and the direction-extrapolator is actively
*confused by the wrap* (3→0 reads as a −1 step, so it forages the wrong band), which is exactly why memory
*loses* there. In the **triangle** season no fixed phase works — the same current band precedes an *ascending*
or a *descending* neighbour depending on where you are in the cycle — so the only way to anticipate is to
**remember the last season and carry the direction forward**. The agent that keeps that internal state
integrates the past and wins.

This is the clean, falsifiable form of the claim that **internal state is selectable**: because the benefit
appears as an **interaction** (memory × partial-observability) and not as a main effect of the policy, it is
*memory* — acting on history — that is being selected, not just a different reflex. It is the embodiment
thread's step from *reflex* to *cognition*: exp062 showed perception→action is selectable; exp065 shows
**perception→memory→action** is selectable exactly when the instant percept underdetermines the right action.

## Where this sits in the embodiment thread
- **exp062 (Ω-0.51):** construction agency (perceive the season, build from it) **PAYS** — reflex is selectable.
- **exp063 / exp064 (Ω-0.52 / 0.53):** locomotive agency (taxis) does **not** pay — shared-perception
  movement herds; random dispersal is the ideal-free optimum.
- **exp065 (Ω-0.54, this):** memory / internal state **PAYS** — and only when the world is partially
  observable. Cognition is selectable when the environment demands it.

## Honest scope
5 seeds; a single memory architecture (last-direction extrapolation) against a single reactive control. The
direction is robust (the interaction reproduces at single-seed scale: triangle +0.111, sawtooth −0.208 at
seed 0, pinned by the test). It does **not** claim this is the *best* memory policy, nor that richer internal
state (multi-step history, learned models) would not do better — only that the *simplest* internal state
that integrates the past is **selected exactly when partial observability makes it necessary**, and not
otherwise. `agent_policy=""` / `season_pattern="sawtooth"` ⇒ exp001–064 byte-identical; deterministic across
`PYTHONHASHSEED`.

## Reproduce
`PYTHONPATH=. python3 studies/exp065_memory.py 5 7000 2400` → the table above; committed as
`studies/exp065_results.json` / `_console.txt`. Pinned by
`test_exp065_memory_pays_only_when_the_world_is_partially_observable` (`agent_policy=""` / `sawtooth`
byte-identical to exp036; memory acts when on; the double dissociation: memory > reactive in triangle,
reactive > memory in sawtooth, interaction > 0.05).
