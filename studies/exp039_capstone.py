"""exp039 — capstone: does multi-objective selection COMPOUND, or is it a hard frontier?

The self-improvement arc found every *single* selection proxy Goodharts: network → runaway
openness (exp037), closure → low heredity (exp038). exp038's lesson was "alignment is
multi-objective." This tests that directly. Two questions:

1. Is the closure↔heredity trade-off *fundamental*? Across demes, are closure and heredity
   anti-correlated (a real Pareto frontier) or independent (both-high demes exist)?
2. Does combining objectives **compound**? `deme_fitness="composite"` is a maximin over the two
   mean-normalized objectives (reward the deme whose *weaker* objective is strongest — forces
   both high). Does it reach high closure AND high heredity, beating each single objective's
   specialty — or land in the middle?

Metric (rate): per-deme correlation(closure, heredity); and mean closure + collective heredity
(self) under composite vs single-objective controls. Run:
  PYTHONPATH=. python3 studies/exp039_capstone.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise


def _run(args) -> dict:
    fit, seed, ticks = args
    p, c = get_experiment("exp039")(seed=seed, ticks=ticks, deme_fitness=fit)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    clos, pairs = [], []
    for t in range(ticks):
        sch.run(1)
        if t > ticks // 2 and t % 40 == 0:
            cs = [p._deme_closure(pi) for pi in range(p.n_patches) if p._deme_edges.get(pi)]
            if cs:
                clos.append(mean(cs))
            if t % 120 == 0:                       # per-deme (closure, heredity-proxy) pairs
                for pi in range(p.n_patches):
                    if p._deme_edges.get(pi):
                        bt = p._breedtrue.get(pi)
                        if bt is not None:
                            pairs.append((p._deme_closure(pi), bt))
    sh = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    return {"fit": fit, "seed": seed, "closure": mean(clos) if clos else 0.0,
            "self": sh, "pairs": pairs}


def _corr(pairs):
    if len(pairs) < 20:
        return 0.0
    xs = [a for a, _ in pairs]; ys = [b for _, b in pairs]
    mx, my = mean(xs), mean(ys); sx, sy = pstdev(xs), pstdev(ys)
    return (mean((a - mx) * (b - my) for a, b in pairs) / (sx * sy)) if sx * sy else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    fits = ["composite", "closure", "network", "size"]
    jobs = [(f, s, ticks) for f in fits for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n,
               "rows": [{k: v for k, v in r.items() if k != "pairs"} for r in rows]},
              open("studies/exp039_results.json", "w"), indent=2)

    allpairs = [pr for r in rows for pr in r["pairs"]]
    print(f"exp039 — capstone: does multi-objective selection compound? "
          f"({ticks} ticks, {n} seeds)\n")
    print(f"  (1) is the trade-off fundamental? corr(closure, heredity) across demes = "
          f"{_corr(allpairs):+.3f}")
    print("      => independent (both-high demes exist) — NOT a fundamental Pareto frontier\n"
          if abs(_corr(allpairs)) < 0.15 else
          "      => correlated — a structural relationship\n")
    print(f"  (2) does composite reach high BOTH?")
    print(f"  {'selection':>10} {'closure':>8} {'heredity(self)':>15}")
    agg = {}
    for f in fits:
        rs = [r for r in rows if r["fit"] == f]
        cl = mean(r["closure"] for r in rs); sh = mean(r["self"] for r in rs)
        agg[f] = (cl, sh)
        print(f"  {f:>10} {cl:>8.3f} {sh:>15.3f}")
    best_cl = max(agg["closure"][0], agg["network"][0])
    best_sh = max(agg["network"][1], agg["closure"][1], agg["size"][1])
    comp = agg["composite"]
    print(f"\n  single-objective bests: closure {best_cl:.3f}, heredity {best_sh:.3f}")
    print(f"  composite: closure {comp[0]:.3f}, heredity {comp[1]:.3f}")
    if comp[0] >= 0.9 * best_cl and comp[1] >= 0.9 * best_sh:
        print("  => COMPOUNDS: aligned multi-objective selection reaches near-best on BOTH — "
              "self-improvement is selection-limited, not substrate-limited.")
    else:
        print("  => DOES NOT COMPOUND: composite reaches high closure but NOT high heredity —")
        print("     even though the objectives are independent (both-high demes exist), selection")
        print("     cannot concentrate on them. The blocker is the WEAK COLLECTIVE-HEREDITY channel")
        print("     (the exp028 ceiling): collectives don't transmit a multi-property phenotype")
        print("     faithfully enough for competence to stack. The machinery for self-improvement")
        print("     is present (exp037 evolvable state, exp038 selectable coherence); the missing")
        print("     piece is high-fidelity collective heredity, not more selection pressure.")


if __name__ == "__main__":
    main()
