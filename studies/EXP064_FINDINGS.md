# exp064 — An exogenous resource does NOT rescue locomotive agency: it deepens the negative — directed movement herds, random dispersal is the ideal-free optimum (Ω-0.53)

exp063 (Ω-0.52) found perception-directed movement (taxis) *worse* than random, and attributed it to the
resource being **self-generated and local** — predicting that an **exogenous, spatial** resource would make
taxis pay. exp064 tests that prediction directly and **refutes it**: making the resource exogenous does not
rescue locomotive agency; it makes taxis *worse* relative to random, and reveals the real reason locomotive
agency fails.

## Mechanism (gated `spatial_feed`, off ⇒ byte-identical)

`spatial_feed` makes the **environment** inject the next-season band into a rotating set of **resource
patches** (`patch % feed_bands == season`), so the anticipated resource genuinely lives *elsewhere* — a
patchy, dynamic map. Agent foraging is **off**, so the only way to reach the resource is to **move** to it.
Arms: **blind** (random neighbour == default), **greedy** (richest *absolute* neighbour), **taxis** (richest
*per-capita* — ideal-free). Swept as a **dose-response** in the resource strength (`spatial_feed_n`).

## Result (5 seeds; anticipation over a season cycle; blind spread = 24/24 throughout)

| resource strength | blind | greedy | taxis | taxis − blind | taxis occupied /24 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 4 (weak) | 0.277 | 0.278 | 0.278 | +0.001 | 18.6 |
| 12 | 0.381 | 0.290 | 0.283 | −0.097 | 18.0 |
| 24 (strong) | **0.565** | 0.311 | 0.363 | **−0.202** | 18.6 |

**Verdict: the exogenous resource does not rescue locomotive agency — it deepens the exp063 negative.** No
taxis policy beats random dispersal at any strength, and the gap *widens against* taxis as the resource
grows: a stronger exogenous resource makes **blind** much better at anticipation (0.28 → 0.57 — more
next-band material to build from) but **taxis barely moves** (0.28 → 0.36).

## Interpretation — why locomotive agency fails: shared-perception movement is anti-cooperative

The mechanism is in the spatial spread. **Random dispersal already realizes the ideal-free distribution**:
blind keeps agents evenly across all 24 patches, so as the rotating resource patches pass through every
neighbourhood, each deme harvests its share — random movement is *optimal* for a distributed, rotating
resource. **Directed movement herds**: taxis concentrates agents onto ~18/24 patches (the perceived-best
resource patches), crowding them so the per-capita resource collapses, while abandoning the rest of the map
the rotating resource also visits. The stronger the resource, the more costly the herd — hence the widening
gap.

Crucially, even the **per-capita "ideal-free" taxis herds**, because all agents best-respond to the *same
stale state at the same instant*: they all compute the same argmax and move there simultaneously, so the
crowding they each discount for has not happened *yet* when they decide. True ideal-free settling needs
asynchronous/iterated moves or private information; synchronous shared perception produces an information
cascade. So the failure of locomotive agency is **not about where the resource is** (self-generated in
exp063, exogenous here — both fail) — it is that **shared-perception, simultaneous movement is
anti-cooperative**. Together exp063 + exp064 make the bound on embodiment precise and general: **agency that
BUILDS (acts on the agent's own patch — exp062) pays; agency that RELOCATES the agent does not, because
directed relocation from shared perception herds, and random dispersal is already optimal.** The value of
embodiment in this world is **construction, not locomotion.**

## Honest scope
5 seeds × 3 resource strengths × 3 policies. The direction is robust (monotone widening gap; blind full
spread at every cell; two directed policies both herd and both lose). It does **not** claim locomotive agency
*can never* pay in *any* substrate — only that neither the resource's location (exp063 vs exp064) nor its
strength makes directed movement beat random dispersal *here*, and it identifies the mechanism (synchronous
shared-perception herding). The predicted regime where taxis *should* pay — **private/heterogeneous
perception or asynchronous settling**, breaking the shared-percept cascade — is the natural next probe.
`spatial_feed=False` / `spatial_policy=""` ⇒ exp001–063 byte-identical; deterministic across `PYTHONHASHSEED`.

## Reproduce
`PYTHONPATH=. python3 studies/exp064_spatialforage.py 5 6000 1200` → the table above; committed as
`studies/exp064_results.json` / `_console.txt`. Pinned by
`test_exp064_exogenous_resource_does_not_rescue_locomotive_agency` (`spatial_feed=False` byte-identical;
injection acts; under a strong exogenous resource blind out-anticipates taxis, which herds onto fewer patches).
