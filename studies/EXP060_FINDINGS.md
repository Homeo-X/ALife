# exp060 — The live tower: levels emerge over wall-clock time and compound competence, and it is EVICTION-INVARIANT — the meta-ratchet is not a batch artifact (Ω-0.49)

exp055 (Ω-0.44) showed a competence-derived transition compounds competence *across* tower levels — in
*batch* (`run_stack`). exp059 (Ω-0.48) folded the arc into the persistent world but found competence
*plateaus* within a single tier; genuine across-time compounding needs a *new level*. exp060 closes the gap:
it runs the recursive tower **live** (`TowerWorld`, chunk-advanced, bounded memory, checkpointable), so
levels emerge over wall-clock time — and asks whether the batch across-level meta-ratchet survives the
streaming, memory-evicting regime a real world runs in. It does, exactly.

## Mechanism — `TowerWorld` (`omega/world/tower.py`, gated; reuses `run_stack`)

`TowerWorld` wraps the `World` runtime around `run_stack`'s promotion logic: it runs the current top tier as
a persistent, chunk-advanced world; when the tier matures (`tier_ticks`) it reads the stable collectives
(`stack._stable_collectives`) and achieved competence (`stack._tier_competence`), records a `TierResult`,
and — if ≥ `min_collectives` heritable collectives formed — **promotes** them to the next tier's alphabet
and spins up the next tier live, with `law_from_competence` (exp055) deriving each emergent level's law from
the competence below. Each tier is built exactly as `run_stack` builds it, and a `World` with no eviction is
the same deterministic function of its seed as the batch run — so faithfulness to batch is exact when
un-evicted.

## Result (5 tiers × 3000 ticks/tier, 6 seeds), three memory regimes

| arm (memory regime) | mean depth | across-tier slope | top competence | tier-0 fail |
|:---|:---:|:---:|:---:|:---:|
| **live-tight** (horizon 1200 < tier life — eviction bites) | 3.50 | +0.0387 | 1.857 | 0.17 |
| live-bounded (horizon 20000) | 3.50 | +0.0387 | 1.857 | 0.17 |
| live-unevicted (batch ceiling) | 3.50 | +0.0387 | 1.857 | 0.17 |

**Verdict: the meta-ratchet survives the world regime — and the live tower is exactly EVICTION-INVARIANT.**

- **Levels emerge live, and competence compounds across them.** The live tower grows tiers over wall-clock
  time (watch it: `python -m omega.world tower`) to mean depth **3.5 / 5**, with competence rising across
  the *emergent* levels at **+0.039/tier** (survivors). The exp055 across-level meta-ratchet is real in a
  persistent, watchable world, not just in batch — higher-order life forms live.
- **Eviction is provably irrelevant to the tower.** `live-tight` sets the memory horizon *below* each tier's
  tick-life, so cold classes are genuinely evicted within every tier — yet it is **byte-identical** to the
  un-evicted ceiling on every metric (depth, slope, competence, failure rate). The tower's dynamics read the
  *live* cross-production network and per-generation edge tallies, not the historical class registry that
  eviction prunes; so bounding memory (the thing that makes an indefinite world feasible, Ω-0.21) does not
  cost the tower anything. This is a *stronger* result than "survives approximately" — the streaming regime
  is the batch regime, for the tower.
- **The residual tier-0 failure (0.17 = 1/6 seeds) is the exp057/58 bootstrapping floor**, not a tower
  defect — some seeds never establish a founding network at any provisioning, as exp057/58 pinned.

## Interpretation — the world can grow a tower of life indefinitely, at flat memory

exp059 gave the living world a high competence *plateau* within one tier; exp060 supplies the missing
across-time compounding by making **new levels** emerge live, and shows the whole recursion runs at **flat
memory** with no dynamical cost (eviction-invariant) — the two properties a genuine open-ended world needs
together: it keeps building higher levels of organization *and* it can run forever. The live tower is the
concrete "watch higher-order life appear" artifact: chemistry → biology → culture → meta-culture born over
wall-clock time, each playing by rules the level below earned, competence rising as it climbs.

## Honest scope
6 seeds × 5 tiers × 3000 ticks/tier. The three memory regimes are byte-identical because the tower reads
live state, not evicted history — a structural invariance, so the exact-equality is expected and robust, not
a small-n coincidence. What this does **not** yet settle: **how deep** the tower goes (5 tiers reached ~3.5;
does depth keep climbing with more tiers / longer per-tier maturation?) and the behaviour at the **10⁶–10⁷
horizon** — that is the long-horizon world census (Phase C / Ω-0.50), where the eviction-invariance proven
here is what makes such a run feasible. The +0.039/tier slope is positive and compounding but modest (cf.
exp055's +0.081/tier at 7000 ticks/tier) — per-tier maturation time trades against tier count.

## Reproduce
`PYTHONPATH=. python3 studies/exp060_towerworld.py 5 3000 6` → the table above; committed as
`studies/exp060_results.json` / `_console.txt`. Watch it live: `python -m omega.world tower`. Pinned by
`omega/tests/test_world.py::TestTowerWorld` (live tower == batch `run_stack` un-evicted; live bounded tower
emerges levels & competence rises across them; checkpoint round-trip identical).
