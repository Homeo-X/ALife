"""exp063 — SPATIAL AGENCY (taxis): is perception-directed MOVEMENT selectable? (an honest negative)

exp062 (Ω-0.51) showed perception-directed *construction* (an agent forages the band its policy targets)
is selectable and pays. exp063 asks the same of perception-directed *movement*: in the same spatial,
seasonal world, does an agent that PERCEIVES which neighbour patch is richest in the next season's band and
MIGRATES toward it out-compete one that moves at random? It does **not** — and the reason is instructive.

Arms (`deme_fitness="anticipation"`; embodied foraging on, so patches differ in the next-band resource):
  * blind  — migrate to a RANDOM neighbour (perception-ablated control == the default migration).
  * greedy — migrate toward the richest ABSOLUTE neighbour (positive-feedback taxis).
  * taxis  — migrate toward the richest PER-CAPITA neighbour (band/pop — ideal-free, crowding-aware).

Per arm: mean anticipation-match over a season cycle, and the spatial spread (occupied patches / max-patch
population) that diagnoses herding.

Predicted (pre-registered) contrast: taxis > blind => locomotive agency is selectable. The result is the
OPPOSITE — no taxis policy beats random movement, because the resource is *self-generated and local* (each
deme forages it into its own patch), so random movement already gives the optimal even spread and directed
movement can only concentrate agents onto shared "best" patches (herding), abandoning self-built resource.

Run:
  PYTHONPATH=. python3 studies/exp063_taxis.py [n_seeds] [warmup] [cycle_ticks]
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
    sp, seed, warmup, cycle = args
    p, c = get_experiment("exp063")(seed=seed, spatial_policy=sp)
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
    return {"arm": sp, "seed": seed, "anticip": mean(vals) if vals else 0.0,
            "occupied": len(pops), "max_pop": max(pops.values()) if pops else 0}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    jobs = [(sp, s, warmup, cycle) for sp in ARMS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {sp: {k: mean(r[k] for r in rows if r["arm"] == sp)
                    for k in ("anticip", "occupied", "max_pop")} for sp in ARMS}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "arms": ARMS, "summary": summary},
              open("studies/exp063_results.json", "w"), indent=2)

    print(f"exp063 — is perception-directed MOVEMENT (taxis) selectable? ({n} seeds)\n")
    print(f"  {'policy':>7} {'anticipation':>13} {'occupied/24':>12} {'max-patch pop':>14}")
    for sp in ARMS:
        s = summary[sp]
        print(f"  {sp:>7} {s['anticip']:>13.3f} {s['occupied']:>12.1f} {s['max_pop']:>14.0f}")
    print()

    bl, gr, tx = summary["blind"], summary["greedy"], summary["taxis"]
    taxis_helps = max(gr["anticip"], tx["anticip"]) > bl["anticip"] + 0.02
    herds = gr["occupied"] < bl["occupied"] - 1.0            # greedy concentrates agents
    print(f"  best taxis {max(gr['anticip'], tx['anticip']):.3f} vs blind {bl['anticip']:.3f}; "
          f"blind spread {bl['occupied']:.1f}/24 vs greedy {gr['occupied']:.1f}/24\n")
    if taxis_helps:
        print("  => LOCOMOTIVE AGENCY IS SELECTABLE — a taxis policy out-anticipates random movement:")
        print("     perception-directed movement pays.")
    else:
        print("  => LOCOMOTIVE AGENCY DOES NOT PAY (an honest negative) — no taxis policy beats random")
        print("     movement. The resource is SELF-GENERATED and LOCAL (each deme forages the next band into")
        print("     its own patch), so random movement already gives the optimal even spatial spread and")
        print("     directed movement can only CONCENTRATE agents onto shared 'best' patches (greedy herds:")
        print(f"     {gr['occupied']:.0f}/24 vs blind {bl['occupied']:.0f}/24), abandoning self-built resource. Constructive")
        print("     agency (exp062) pays; locomotive agency does not, in a niche-constructing world. Predicted")
        print("     positive follow-on: an EXOGENOUS patchy resource (a spatial feed) should make taxis pay.")


if __name__ == "__main__":
    main()
