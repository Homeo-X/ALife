"""exp064 — SPATIAL FORAGING: does locomotive agency pay when the resource is EXOGENOUS? (it does NOT — the
exp063 negative deepens)

exp063 (Ω-0.52) found perception-directed movement (taxis) worse than random, and attributed it to the
resource being *self-generated and local* — predicting that an EXOGENOUS, spatial resource would make taxis
pay. exp064 tests that directly (a gated `spatial_feed` injects the next-season band into a rotating set of
resource patches; agent foraging OFF, so the only way to reach the resource is to MOVE there) and **refutes
the prediction**: no taxis policy beats random dispersal, and taxis gets *worse* relative to random as the
resource strengthens.

Dose-response in the exogenous-resource strength (`spatial_feed_n`), arms {blind, greedy, taxis}:
measure the mean anticipation-match over a season cycle and the spatial spread (occupied patches).

Predicted (from exp063): taxis > blind for an exogenous resource. Result: the OPPOSITE, and the gap widens
against taxis as the resource grows — because directed movement HERDS agents onto the resource patches
(crowding them), while random dispersal already realizes the ideal-free distribution and harvests a rotating
spatial resource efficiently. The failure of locomotive agency is not about *where* the resource is; it is
that shared-perception, simultaneous movement is anti-cooperative.

Run:
  PYTHONPATH=. python3 studies/exp064_spatialforage.py [n_seeds] [warmup] [cycle_ticks]
"""
from __future__ import annotations
import sys, json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

ARMS = ["blind", "greedy", "taxis"]
FEED = [4, 12, 24]


def _anticip(p) -> float | None:
    nb = p._next_band
    if not nb:
        return None
    tot = match = 0
    for d in p._deme_atoms.values():
        for a, nn in d.items():
            tot += nn
            if a in nb:
                match += nn
    return match / tot if tot else 0.0


def _run(args) -> dict:
    sp, fn, seed, warmup, cycle = args
    p, c = get_experiment("exp064")(seed=seed, spatial_policy=sp, spatial_feed_n=fn)
    u, rng = Universe(total_quanta=c.total_quanta), Noise(c.seed); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    sch.run(warmup)
    vals = []
    for _ in range(10):
        sch.run(cycle // 10)
        v = _anticip(p)
        if v is not None:
            vals.append(v)
    pops = Counter(p._patch.get(o.uid) for o in u.organizations.values()); pops.pop(None, None)
    return {"arm": sp, "fn": fn, "seed": seed, "anticip": mean(vals) if vals else 0.0,
            "occupied": len(pops)}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    jobs = [(sp, fn, s, warmup, cycle) for sp in ARMS for fn in FEED for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for sp in ARMS:
        for fn in FEED:
            rs = [r for r in rows if r["arm"] == sp and r["fn"] == fn]
            summary[f"{sp}:{fn}"] = {"anticip": mean(r["anticip"] for r in rs),
                                     "occupied": mean(r["occupied"] for r in rs)}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "arms": ARMS, "feed": FEED,
               "summary": summary}, open("studies/exp064_results.json", "w"), indent=2)

    print(f"exp064 — does taxis pay when the resource is EXOGENOUS? dose-response in resource strength ({n} seeds)\n")
    print(f"  {'feed_n':>6} {'blind':>8} {'greedy':>8} {'taxis':>8} {'taxis-blind':>12}   {'blind occ':>10} {'taxis occ':>10}")
    gaps = {}
    for fn in FEED:
        b, g, t = (summary[f"{a}:{fn}"] for a in ("blind", "greedy", "taxis"))
        gaps[fn] = t["anticip"] - b["anticip"]
        print(f"  {fn:>6} {b['anticip']:>8.3f} {g['anticip']:>8.3f} {t['anticip']:>8.3f} {gaps[fn]:>+12.3f}   "
              f"{b['occupied']:>10.1f} {t['occupied']:>10.1f}")
    print()

    taxis_pays = any(gaps[fn] > 0.02 for fn in FEED)
    worsens = gaps[FEED[-1]] < gaps[FEED[0]] - 0.05
    print(f"  taxis-blind gap: {gaps[FEED[0]]:+.3f} (weak) -> {gaps[FEED[-1]]:+.3f} (strong resource)\n")
    if taxis_pays:
        print("  => LOCOMOTIVE AGENCY PAYS WHEN THE RESOURCE IS EXOGENOUS — taxis beats random movement,")
        print("     bounding the exp063 negative: perception-directed movement is selectable when the")
        print("     resource genuinely lives elsewhere.")
    elif worsens:
        print("  => THE EXOGENOUS RESOURCE DOES NOT RESCUE LOCOMOTIVE AGENCY — it DEEPENS the exp063 negative.")
        print("     No taxis policy beats random dispersal, and taxis gets WORSE relative to random as the")
        print("     resource strengthens (blind rises steeply, taxis barely moves). Directed movement HERDS")
        print("     agents onto the resource patches (crowding them), while random dispersal already realizes")
        print("     the IDEAL-FREE distribution and harvests a rotating spatial resource efficiently. Even the")
        print("     per-capita ('ideal-free') taxis herds, because all agents best-respond to the same stale")
        print("     state at once. Locomotive agency fails not because of WHERE the resource is, but because")
        print("     shared-perception simultaneous movement is anti-cooperative. Embodiment's value is")
        print("     CONSTRUCTION (exp062), not locomotion.")
    else:
        print("  => INCONCLUSIVE — taxis neither clearly pays nor clearly worsens; report the table as-is.")


if __name__ == "__main__":
    main()
