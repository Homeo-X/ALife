# exp053 — The Catalytic Law breaks the competence-flat wall: competence COMPOUNDS, and it is a genuine ratchet

The self-improvement arc (exp044–052) found that collective competence never compounds — every
selection/representation/replicator/coevolution lever moved the competence *level* but never the *slope*.
exp049 named the one untried move and diagnosed why its own attempt failed: reifying a competent module
to a **new atom** hides its structure in an **opaque** primitive, out of the measured cross-production
network — a lateral move, not a ratchet. exp053 does it as a **reaction** instead, and it works.

## Mechanism (gated `catalytic_law`, default off ⇒ exp001–052 byte-identical)

Every `catalyst_period` ticks, promote the **busiest closure-core edge of the highest-competence deme**
(a `producers ∩ products` self-maintaining loop — achieved *competent* structure) to a persistent shared
**catalyst**: a reaction `anchor_cls → product_state` injected every tick. The promoted motif is thus
reliably re-supplied everywhere as a **network-visible class** (not an opaque atom — the exp049 fix), so
later collectives' compositions can build closures **on top of** earlier ones. Each period a *new* motif
is harvested from the now-more-competent frontier, so the reaction repertoire tracks the rising frontier
— a substrate law that changes with achieved competence. Runs on the exp052 Red Queen base (the strongest
competence-*level* platform, with non-collapsing networks).

## Result 1 — the 2×2 factorial (12k ticks, 6 seeds): both catalytic cells COMPOUND

|  | competence (mean, slope) | closure | survival | catalysts |
|---|:---:|:---:|:---:|:---:|
| **catalytic × Red Queen** | **1.183, +0.0186/win** | 0.26 → **0.43** | 0.57 → **0.79** | 11.0 |
| catalytic × closure | 0.990, **+0.0166/win** | → 0.35 | → 0.62 | 8.8 |
| fixed-law × Red Queen (exp052) | 0.820, −0.0208/win | → 0.20 | 0.71 | 0 |
| fixed-law × closure (exp038) | 0.673, +0.0041/win | → 0.18 | 0.57 | 0 |

**Both catalytic cells have a positive competence slope; both fixed-law cells are flat/declining.** The
catalytic+Red-Queen cell rises **monotonically** 0.893 → 1.237 over 12k ticks (~600 generations) — the
arc's **highest level and first sustained positive slope** — with closure and survival *also* rising. The
Catalytic Law lifts competence **+0.36** over its no-law control (Red Queen) and **+0.32** over closure.
The **Catalytic Law is the ingredient that tilts the slope**; the Red Queen maximizes both level and
slope (1.183 & +0.019 vs 0.990 & +0.017), but compounding does not strictly require it.

## Result 2 — the discriminating control: is it a genuine ratchet or mechanical injection?

Injecting reactions could pad the closure/breadth metric on its own. Control arm `catalyst_random`:
promote a **random edge from a random deme** (same injection rate, no competence-dependence).

| arm (Red Queen base) | competence trajectory | slope | mean |
|---|---|:---:|:---:|
| **competent** (closure-central, best deme) | 0.89 → 1.24 | **+0.0186** | **1.183** |
| random (arbitrary edge/deme) | 0.76 → 0.90 | +0.0058 | 0.915 |

**Verdict: a genuine ratchet, with a small mechanical floor.** Random injection *does* compound a little
(+0.006, and lifts the level ~0.10 above the no-law 0.820) — the mere *act* of re-supplying
network-visible reactions helps. But the **competence-dependent** harvest climbs **3× steeper** (+0.019
vs +0.006) to a **much higher** level (1.183 vs 0.915). The rise therefore requires promoting genuinely
*achieved competent* structure; it is not an artifact of injection. (The catalyst reactions also do not
directly write `_deme_edges` — they re-supply competent product *instances* that the normal composition
loop builds on — so the metric is not padded by construction.)

## Interpretation — the competence analogue of Ω-0.20

This is the arc's **first compounding-competence result**, and it lands exactly where the program's own
theory predicted. Ω-0.20 showed **novelty** is a *rate*, sustained only by *continuing reification* —
promoting achieved structure to new **primitives** keeps the construction space growing. exp049 tried the
literal analogue for competence and failed because a new **atom** is opaque. exp053 supplies the missing
piece: promote achieved competence to a new **reaction**, which keeps the structure **in the measured
network**, and competence becomes a rate too. **The substrate-law feedback is the ratchet; a receding
(Red Queen) target maximizes it.**

This **refines the arc's central negative.** "Open-ended novelty ≠ open-ended competence" (Ω-0.38) was
true *for a fixed substrate law* — and it named the fix. Once the law itself grows with achieved
competence (network-visibly), competence compounds like novelty does. Self-improvement in this substrate
is not impossible; it needs a **competence-dependent substrate law**, which pure
selection/representation/replicator/coevolution routes could not supply.

## Honest scope
- **A small part of the effect is mechanical** (random injection gives +0.006 and a level lift); the
  headline is the **3× steeper, higher competence-dependent** climb, not the raw rise.
- **Saturation is untested.** Competence rises over 12k ticks / ~600 generations; the catalyst repertoire
  (`catalyst_max=16`) reached ~11–14, near the cap. Whether competence keeps rising without bound or
  saturates as the repertoire fills is the **immediate next question** (a longer-horizon / larger-cap run).
- Within the both-corner typed_path substrate; 6 seeds × 12k. The competence metric is the exp042 composite
  (closure + breed-true + normalized breadth).

## Reproduce
`PYTHONPATH=. python3 studies/exp053_catalytic.py 12000 6 4000` (the 2×2 factorial) and
`PYTHONPATH=. python3 studies/exp053_control.py 12000 6 4000` (the competent-vs-random control) → the
tables above; committed as `studies/exp053_results.json` / `_console.txt` and
`studies/exp053_control_results.json` / `_console.txt`. Pinned by
`test_exp053_catalytic_law_promotes_closure_loops_to_network_visible_reactions` (a catalyst is harvested;
the promoted product is a real class in the registry, **not** a new atom; `catalytic_law` off ⇒ no
catalysts). Deterministic across `PYTHONHASHSEED`; `catalytic_law` default ⇒ exp001–052 byte-identical.
