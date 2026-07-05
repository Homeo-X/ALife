"""exp022 — an EMERGENT (not imposed) collective trait, and its transmission
threshold. Deme fitness = internal cross-production (a member producing a different
member — irreducibly collective, unmaximizable by any single replicator). No copy
channel, no imposed coop bit.

Central question: does collective selection (source) favor emergent cross-producing
networks over the well-mixed mixed null — and does it require a propagule big enough
to TRANSMIT the multi-member network? Prediction (opposite of exp021's single-locus
cooperation, which wanted small propagules): the source advantage should rise with
propagule size up to an intermediate optimum, then fall as the bottleneck weakens.
Run: PYTHONPATH=. python3 studies/exp022_emergent_network.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
PSIZES = [2, 4, 8, 16, 24, 40, 60]


def one(args):
    psize, mode, seed = args
    p, c = get_experiment('exp022')(seed=seed, ticks=TICKS, n_patches=24,
                                    propagule_mode=mode, propagule_size=psize)
    r = run(p, c)
    g = [m['gauges'].get('mean_cross_prod', 0.0) for m in r.metrics]
    tail = r.metrics[-len(r.metrics) // 4:]
    ndt = mean(m['gauges'].get('n_deme_types', 0.0) for m in tail)
    return {"psize": psize, "mode": mode, "seed": seed,
            "cross": mean(g[-len(g) // 4:]) if g else 0.0,
            "ndt": ndt, "pop": r.final_population}


def main():
    jobs = [(ps, m, s) for ps in PSIZES for m in ('source', 'mixed') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds "
          f"(emergent cross-production fitness, no copy/coop)\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp022_results.json', 'w'), indent=2)

    print(f"{'propagule':>9s} {'source xprod':>13s} {'mixed xprod':>13s} "
          f"{'source/mixed':>12s} {'n_deme_types(s/m)':>18s}")
    print("-" * 70)
    for ps in PSIZES:
        s = [r['cross'] for r in rows if r['psize'] == ps and r['mode'] == 'source']
        x = [r['cross'] for r in rows if r['psize'] == ps and r['mode'] == 'mixed']
        sn = mean(r['ndt'] for r in rows if r['psize'] == ps and r['mode'] == 'source')
        xn = mean(r['ndt'] for r in rows if r['psize'] == ps and r['mode'] == 'mixed')
        ratio = mean(s) / mean(x) if mean(x) else 0.0
        flag = "  <== collective favored" if ratio > 1.10 else (
               "  (transmission fails)" if ratio < 0.98 else "")
        print(f"{ps:9d} {mean(s):8.2f}±{pstdev(s):.2f} {mean(x):8.2f}±{pstdev(x):.2f} "
              f"{ratio:12.2f} {sn:7.1f} /{xn:6.1f}{flag}")


if __name__ == '__main__':
    main()
