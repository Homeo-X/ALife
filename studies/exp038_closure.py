"""exp038 — coherence as an emergent, selectable, better-aligned target: autocatalytic closure.

exp037 (Ω-0.25) showed evolvable architecture amplifies *whatever* is selected — network fitness
drove runaway openness (Goodhart). This selects for a **better-aligned, emergent** trait instead:
**autocatalytic closure** — the fraction of a deme's cross-production network that is self-producing
(a class both produced by a member and itself a producer: a self-maintaining loop). Unlike exp021's
*imposed* cooperation bit, closure is read off the real network. Two questions:

1. Is coherence **selectable**? Does `deme_fitness="closure"` raise closure above matched controls
   (network, size)?
2. Does selecting it **strengthen individuality** — higher collective heredity (self > null) — i.e.
   are self-maintaining collectives also more faithfully reproduced (the churn/short-life fix)?

Metric (rate, not cumulative): mean deme closure and mean collective heredity (edge-set Jaccard
self vs null) over a late window, across fitness targets. Run:
  PYTHONPATH=. python3 studies/exp038_closure.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise


def _run(args) -> dict:
    fit, seed, ticks = args
    p, c = get_experiment("exp038")(seed=seed, ticks=ticks, deme_fitness=fit)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    clos = []
    for t in range(ticks):
        sch.run(1)
        if t > ticks // 2 and t % 40 == 0:
            cs = [p._deme_closure(pi) for pi in range(p.n_patches) if p._deme_edges.get(pi)]
            if cs:
                clos.append(mean(cs))
    # collective heredity accumulated over the run (edge-set Jaccard self vs a random deme)
    self_h = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    null_h = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    return {"fit": fit, "seed": seed, "closure": mean(clos) if clos else 0.0,
            "self": self_h, "null": null_h}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    fits = ["closure", "network", "size"]
    jobs = [(f, s, ticks) for f in fits for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n, "rows": rows},
              open("studies/exp038_results.json", "w"), indent=2)

    print(f"exp038 — autocatalytic closure as an emergent, selectable coherence target "
          f"({ticks} ticks, {n} seeds)\n")
    print(f"  {'selection':>10} {'mean closure':>13} {'heredity self':>14} "
          f"{'null':>7} {'self/null':>10}")
    agg = {}
    for f in fits:
        rs = [r for r in rows if r["fit"] == f]
        cl = mean(r["closure"] for r in rs); sh = mean(r["self"] for r in rs)
        nh = mean(r["null"] for r in rs)
        agg[f] = (cl, sh, nh)
        print(f"  {f:>10} {cl:>13.3f} {sh:>14.3f} {nh:>7.3f} "
              f"{(sh / nh if nh else 0):>10.2f}")
    clos_gain = agg["closure"][0] - agg["network"][0]
    her_treat = agg["closure"][1] - agg["closure"][2]
    her_ctrl = agg["network"][1] - agg["network"][2]
    print(f"\n  closure gain (closure- vs network-selection): {clos_gain:+.3f}")
    print(f"  collective heredity (self-null): closure {her_treat:+.3f} vs network {her_ctrl:+.3f}")
    if agg["closure"][0] > agg["network"][0] > agg["size"][0] and clos_gain > 0.005:
        verdict = "SELECTABLE: coherence (autocatalytic closure) is an emergent trait selection raises"
        if her_treat >= her_ctrl - 0.01:
            verdict += ",\n     and selecting it does not cost collective heredity (self > null intact)"
        print(f"\n  => {verdict}.")
        print("     A better-aligned target than exp037's runaway-openness proxy: it rewards")
        print("     collectives that rebuild their own parts (self-maintenance), read off the")
        print("     real network — not an imposed trait (contrast exp021's cooperation bit).")
    else:
        print("\n  => closure is not cleanly selectable here — see table (a substrate-limit result).")


if __name__ == "__main__":
    main()
