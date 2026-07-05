"""exp021 — group selection of a cooperation trait. The canonical test of whether
collectives can outcompete individuals: a trait that is individually costly
(cooperators replicate slower) but collectively beneficial (a deme founds
propagules in proportion to its cooperator fraction). Within-deme selection erodes
cooperation; between-deme selection (source propagules) can maintain it.

Sweeps coop_cost (individual-selection strength) at a strong-relatedness regime
(single-founder bottleneck, fast/strong deme turnover), comparing source
(collective heredity ON) vs the well-mixed mixed null. The signature of collectives
outcompeting individuals is a positive, cost-dependent source-minus-mixed gap in
late cooperator fraction.
Run: PYTHONPATH=. python3 studies/exp021_cooperation.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 2500
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
COSTS = [0.0, 0.05, 0.1, 0.2, 0.4]


def one(args):
    cost, mode, seed = args
    # exp021 defaults are the strong-relatedness regime; vary only the cost + mode.
    p, c = get_experiment('exp021')(seed=seed, ticks=TICKS, n_patches=24,
                                    propagule_mode=mode, coop_cost=cost)
    r = run(p, c)
    cf = [m['gauges'].get('coop_frac', 0.0) for m in r.metrics]
    late = mean(cf[-len(cf) // 4:]) if cf else 0.0
    return {"cost": cost, "mode": mode, "seed": seed, "coop_late": late,
            "pop": r.final_population}


def main():
    jobs = [(cost, m, s) for cost in COSTS for m in ('source', 'mixed') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds "
          f"(single-founder bottleneck, deme_gen 5, benefit 10)\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp021_results.json', 'w'), indent=2)

    print(f"{'coop_cost':>9s} {'source coop':>16s} {'mixed coop':>16s} {'source-mixed':>13s}")
    print("-" * 60)
    for cost in COSTS:
        s = [r['coop_late'] for r in rows if r['cost'] == cost and r['mode'] == 'source']
        x = [r['coop_late'] for r in rows if r['cost'] == cost and r['mode'] == 'mixed']
        gap = mean(s) - mean(x)
        flag = "  group selection maintains coop" if gap > 0.03 else ""
        print(f"{cost:9.2f} {mean(s):8.3f}±{pstdev(s):.3f} {mean(x):8.3f}±{pstdev(x):.3f} "
              f"{gap:+11.3f}{flag}")


if __name__ == '__main__':
    main()
