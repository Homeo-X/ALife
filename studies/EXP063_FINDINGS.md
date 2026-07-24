# exp063 — Locomotive agency does NOT pay: perception-directed movement (taxis) is worse than random in a niche-constructing world (an honest negative, Ω-0.52)

exp062 (Ω-0.51) showed the embodiment thread's first rung is a positive: perception-directed *construction*
(an agent forages the band its heritable policy targets) is selected and pays. exp063 is the second rung —
action on **space** — and it is an honest **negative**: perception-directed *movement* (taxis) is not
selectable here, and the reason is instructive and clean.

## Mechanism (gated `spatial_policy`, off ⇒ byte-identical)

In the same spatial, seasonal world (embodied foraging on, so patches differ in the next-season band — the
anticipated resource), a migrating deme chooses its neighbour by policy:
- **blind** — a *random* neighbour (perception-ablated control == the default migration).
- **greedy** — the neighbour richest in the next band *absolute* (positive-feedback taxis).
- **taxis** — the neighbour richest *per-capita* (band ÷ population — ideal-free, crowding-aware).

Selection is `deme_fitness="anticipation"`. Pre-registered prediction: taxis > blind ⇒ locomotive agency is
selectable. `spatial_policy=""` ⇒ the pre-exp063 random-neighbour hop, byte-identical.

## Result (6 seeds; anticipation over a season cycle; spatial spread diagnoses herding)

| policy | anticipation | occupied patches /24 | max-patch pop |
|:---|:---:|:---:|:---:|
| **blind** (random) | **0.425** | **24.0** | 17 |
| greedy (absolute) | 0.307 | 18.5 | 48 |
| taxis (per-capita) | 0.291 | 20.5 | 40 |

**Verdict: locomotive agency does not pay — no taxis policy beats random movement.** The prediction is
falsified in the opposite direction: both directed policies are *worse* than blind (0.31/0.29 vs 0.43), and
even the ideal-free (crowding-aware) taxis, which spreads agents more than greedy (20.5 vs 18.5 patches),
still underperforms random.

## Interpretation — why constructive agency pays but locomotive agency doesn't

The mechanism is clean and shows in the spatial spread. **Random movement already gives the optimal
even spread** (blind: 24/24 patches, max-patch population 17). Any *directed* movement can only
**concentrate** agents onto the shared "best" patches — **herding** (greedy: 18.5/24, a crowded max of 48).
And the deeper reason it cannot help: in this world the resource is **self-generated and local** — each
embodied deme forages the next-season band *into its own patch* (exp062). So the "richest neighbour" a taxis
agent moves toward is just *another deme's* self-built patch; moving there **abandons the resource the agent
itself created** and crowds a rival's. There is no exogenous spatial structure for movement to exploit, so
perception-directed movement is strictly worse than staying put (which random, low-rate migration
approximates).

This bounds embodiment precisely and complements exp062: **agency that BUILDS (acts on the agent's own
patch) is selectable; agency that RELOCATES (moves the agent to another patch) is not, in a
niche-constructing world** — because relocation abandons self-built structure. It mirrors a real biological
intuition: niche-constructing / sessile organisms gain from building, not from chasing resources they
themselves make. The value of embodiment in exp062 was **construction**, not **locomotion**.

## Honest scope
6 seeds; two taxis designs tested (greedy and ideal-free), both worse than random, so the negative is not an
artifact of one bad policy. It is specific to a world where the anticipated resource is **self-generated**;
the **predicted positive follow-on** is direct: introduce an **exogenous, patchy resource** (a spatial feed
that favours different bands in different patches) so the resource genuinely lives *elsewhere* — there,
perception-directed movement toward it should pay, and taxis should beat blind. That is the natural next
rung (and the falsification of *this* negative's scope claim). `spatial_policy=""` ⇒ exp001–062
byte-identical; deterministic across `PYTHONHASHSEED`.

## Reproduce
`PYTHONPATH=. python3 studies/exp063_taxis.py 6 6000 1200` → the table above; committed as
`studies/exp063_results.json` / `_console.txt`. Pinned by
`test_exp063_spatial_taxis_gates_cleanly_and_greedy_herds` (`spatial_policy=""` == blind, byte-identical;
taxis changes movement; greedy herds onto fewer patches than blind).
