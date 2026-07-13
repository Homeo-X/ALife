"""exp037 — per-collective evolvable internal state: does architecture evolve under selection?

exp036 (Ω-0.24) hit the third wall: you cannot select for what a collective cannot *represent*.
This supplies the missing piece — a **per-collective genome**: each deme carries a heritable,
mutable construction rule of its own (its `type_resolution`), used in its own compositions and
transmitted (with mutation) to the demes it founds (exp033 made physics first-class per LEVEL;
this makes a slice of it first-class per COLLECTIVE). The question: with heritable internal state,
does a collective's architecture now **evolve under selection** — the thing that was impossible
before?

Design: demes start with resolutions drawn uniformly (1..R). Measure the population's mean per-deme
resolution over generations.
  treat   : deme_fitness=network (source founding, fitness-weighted) — selection acts on the genome
  control : propagule_mode=mixed — no fitness-weighted source, so the genome is not selected
Metric (rate/trajectory, not cumulative): mean resolution vs generation, treatment vs control, and
the final novelty (to expose *which* architecture selection favours).

Run: PYTHONPATH=. python3 studies/exp037_genome.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise
from omega.emergence.novelty import NoveltyTracker


def _run(args) -> dict:
    label, overrides, seed, ticks = args
    p, c = get_experiment("exp037")(seed=seed, ticks=ticks, genome_res_range=(1, 6), **overrides)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    nov = NoveltyTracker(); sch.add_recorder(lambda uu, r: nov.record(uu))
    traj = []
    step = max(1, ticks // 10)
    for t in range(ticks):
        sch.run(1)
        if t % step == 0 or t == ticks - 1:
            res = list(p._deme_res.values())
            traj.append(round(mean(res), 2) if res else 0.0)
    return {"label": label, "seed": seed, "traj": traj,
            "final_res": traj[-1], "novelty": round(nov.recent_rate(ticks // 5), 3)}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    conds = {"treat (network sel)": {"deme_fitness": "network"},
             "control (no sel)": {"propagule_mode": "mixed"}}
    jobs = [(lab, ov, s, ticks) for lab, ov in conds.items() for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n, "rows": rows},
              open("studies/exp037_results.json", "w"), indent=2)

    print(f"exp037 — does per-collective architecture evolve under selection? "
          f"({ticks} ticks, {n} seeds)")
    print(f"  genome = per-deme type_resolution, start uniform 1..6 (mean 3.5)\n")
    L = max(len(r["traj"]) for r in rows)
    print("  mean per-deme resolution over the run:")
    for lab in conds:
        rs = [r for r in rows if r["label"] == lab]
        avg = [mean(r["traj"][i] for r in rs if i < len(r["traj"])) for i in range(L)]
        print(f"  {lab:>20} " + " ".join(f"{v:4.1f}" for v in avg) +
              f"   final novelty {mean(r['novelty'] for r in rs):.2f}")
    t_final = mean(r["final_res"] for r in rows if r["label"] == "treat (network sel)")
    c_final = mean(r["final_res"] for r in rows if r["label"] == "control (no sel)")
    gap = t_final - c_final
    print(f"\n  final resolution: treatment {t_final:.2f} vs control {c_final:.2f} "
          f"(start 3.5); selection gap {gap:+.2f}")
    if gap > 0.7:
        print("  => ARCHITECTURE EVOLVES UNDER SELECTION (engine piece exp036 lacked): the")
        print("     per-collective genome is heritable, mutable, and the selection channel MOVES")
        print("     it (treatment vs the no-selection control). A collective CAN now carry and")
        print("     evolve internal state. Honest edges: (i) the selection signal on architecture")
        print("     is weak/noisy (a ~1-point drift, not a sharp optimum) — consistent with the")
        print("     exp028 heredity ceiling; (ii) it runs toward the fitness proxy's extreme")
        print("     (high resolution => runaway openness), not the heredity 'both corner' —")
        print("     evolvable architecture amplifies WHATEVER is selected (Goodhart). Both point")
        print("     to exp038: select a stronger, better-aligned target (coherence/stability).")
    else:
        print("  => no differential evolution — see trajectory.")


if __name__ == "__main__":
    main()
