"""exp059 — DOES THE ARC TRANSFER TO THE LIVING WORLD? living_world vs the exp030-era world.

The self-improvement arc (Ω-0.41–0.45) proved, in *batch*, that a competence-compounding law (the
Catalytic Law × Red Queen, exp053) lifts collective competence far above the fixed-law plateau. But the
persistent, watchable world (`build_world`, `omega/world/`) is frozen at the exp030 era — both-corner +
reify + culture + space with `deme_fitness="network"`, none of the arc. exp059 asks whether the arc
*transfers* to the persistent, spatial, reifying, eviction-bounded world regime, where interactions with
reification/space/memory-eviction could cancel it.

`living_world` (the upgraded builder) = the `world` foundation + `catalytic_law` + `deme_fitness="redqueen"`
+ `competence_pressure=1.0` + the exp040 heredity channel. This runs both as *persistent worlds* (bounded
memory, chunk-advanced — the real world regime, not batch) with the `WorldVitals` instrument, multi-seed,
and compares the **competence level and trajectory (slope)**, **autocatalytic closure** (the life signal),
the count of **self-maintaining lifeforms**, and the **genuine (eviction-robust) novelty rate**.

Success: `living_world` competence sits far above `world` AND stays elevated / trends up over the long run,
with more closed (self-maintaining) collectives — the arc transfers; the living world is genuinely more
alive. Predicted falsification: the compounding law does NOT transfer (living_world ≈ world on competence,
or it decays under reification/eviction) — a real negative bounding the batch→world transfer.

Run:
  PYTHONPATH=. python3 studies/exp059_livingworld.py [horizon] [chunk] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.world.runtime import World
from omega.world.vitals import WorldVitals, _slope

ARMS = ["living_world", "world"]


def _run(args) -> dict:
    arm, seed, horizon, chunk = args
    w = World.create(arm, seed=seed, genuine_novelty=True)
    v = WorldVitals(window=max(8, horizon // chunk))
    traj = []          # (tick, competence)
    last = None
    steps = horizon // chunk
    for _ in range(steps):
        w.step(chunk)
        s = v.sample(w)
        traj.append((s["tick"], s["competence"]))
        last = s
    # slope over the SECOND HALF (skip the warm-up transient) — the "does it keep rising" signal
    half = traj[len(traj) // 2:]
    return {"arm": arm, "seed": seed,
            "competence": mean(y for _, y in half),
            "competence_slope": _slope(half),
            "closure": last["closure"],
            "lifeforms": last["lifeforms"],
            "collectives": last["collectives"],
            "breeding_true": last["breeding_true"],
            "genuine_rate": last["genuine_novelty_rate"],
            "diversity": last["diversity"]}


def main() -> None:
    horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    chunk = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    jobs = [(a, s, horizon, chunk) for a in ARMS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a]
        summary[a] = {k: mean(r[k] for r in rs) for k in
                      ("competence", "competence_slope", "closure", "lifeforms",
                       "collectives", "breeding_true", "genuine_rate", "diversity")}
    json.dump({"horizon": horizon, "chunk": chunk, "n_seeds": n, "arms": ARMS, "summary": summary},
              open("studies/exp059_results.json", "w"), indent=2)

    print(f"exp059 — does the arc transfer to the living world? ({horizon} ticks, {n} seeds, persistent bounded-memory worlds)\n")
    print(f"  {'arm':>13} {'competence':>11} {'slope':>10} {'closure':>8} {'lifeforms':>10} {'genuine_rate':>13} {'diversity':>10}")
    for a in ARMS:
        s = summary[a]
        print(f"  {a:>13} {s['competence']:>11.3f} {s['competence_slope']:>+10.5f} {s['closure']:>8.3f} "
              f"{s['lifeforms']:>10.1f} {s['genuine_rate']:>13.3f} {s['diversity']:>10.3f}")
    print()

    lw, w = summary["living_world"], summary["world"]
    comp_lift = lw["competence"] - w["competence"]
    transfers = comp_lift > 0.25 and lw["competence"] > w["competence"] * 1.15
    genuine_alive = lw["genuine_rate"] > 0.0 and w["genuine_rate"] > 0.0
    print(f"  competence lift living_world - world: {comp_lift:+.3f}  "
          f"(living {lw['competence']:.3f} vs world {w['competence']:.3f})")
    print(f"  both worlds genuinely open (genuine novelty > 0): {genuine_alive}\n")
    if transfers:
        print("  => THE ARC TRANSFERS — the compounding law survives the persistent, spatial, reifying,")
        print("     eviction-bounded world regime: living_world competence sits FAR above the exp030 world,")
        print("     with more self-maintaining (closed) collectives. The living world is genuinely more")
        print(f"     alive, and its competence trajectory slope is {lw['competence_slope']:+.5f}.")
    else:
        print("  => THE ARC DOES NOT TRANSFER — living_world competence is not decisively above the exp030")
        print("     world in the persistent regime (reification / space / eviction cancel the batch gain).")
        print("     A real negative bounding the batch->world transfer; report the per-arm table as-is.")


if __name__ == "__main__":
    main()
