"""exp026 — pushing weak (~1.6x) network individuation toward strong, via two levers
at once, in a 2x2 factorial:
  substrate: SKI (baseline) vs BCW (extra B/C/W combinators — richer *interacting*
             types; inert data atoms enrich types but kill cross-production)
  fitness:   network (cross-production count, exp025) vs breed_true (select demes
             whose network signature reproduces faithfully)

Headline metric: edge-set heredity ratio (self/null Jaccard of a founded deme's
network signature) — does it cross from weak (~1.6x) toward strong? Also tracks the
identity-space size (n_deme_signatures) and novelty rate (the cost side of the
Ω-0.14 heredity-vs-diversity tension).
Run: PYTHONPATH=. python3 studies/exp026_strong_individuation.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run
from omega.substrate.noise import Noise
from omega.kernel.organization import canonical_cls

CELLS = [("SKI", ""), ("BCW", "BCW")]
FITS = ["network", "breed_true"]


def one(args):
    sub_name, extra, fit, seed = args
    p, c = get_experiment('exp026')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source',
                                    extra_combinators=extra, deme_fitness=fit)
    r = run(p, c)
    es = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    en = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    tail = r.metrics[-len(r.metrics) // 5:]
    return {"sub": sub_name, "fit": fit, "seed": seed,
            "edge_ratio": es / (en + 1e-9) if es else 0.0,
            "edge_self": es, "edge_null": en,
            "n_sigs": mean(m['gauges'].get('n_deme_signatures', 0.0) for m in tail),
            "novelty": r.open_endedness["novelty_rate"],
            "cross_prod": mean(m['gauges'].get('mean_cross_prod', 0.0) for m in tail),
            "pop": r.final_population}


def type_space(extra):
    p, _ = get_experiment('exp026')(seed=0, n_patches=24, extra_combinators=extra)
    rng = Noise(0)
    ctr = Counter(canonical_cls(p._random_normal(rng)) for _ in range(5000))
    return len(ctr), sum(n for _, n in ctr.most_common(9)) / 5000


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    jobs = [(sn, ex, fit, s) for (sn, ex) in CELLS for fit in FITS for s in seeds]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(seeds)} seeds/cell\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp026_results.json', 'w'), indent=2)

    print("type space (feed distribution, 5000 draws):")
    for sn, extra in CELLS:
        n, cov = type_space(extra)
        print(f"  {sn}: distinct normal forms {n}, top-9 cover {cov:.2f}")

    def agg(sn, fit, k):
        v = [r[k] for r in rows if r['sub'] == sn and r['fit'] == fit]
        return mean(v), pstdev(v)

    print(f"\n{'substrate':>9s} {'fitness':>11s} {'edge heredity':>14s} "
          f"{'n_signatures':>12s} {'novelty':>8s} {'x-prod':>7s}")
    print("-" * 68)
    for sn, _ in CELLS:
        for fit in FITS:
            er, es = agg(sn, fit, 'edge_ratio')
            print(f"{sn:>9s} {fit:>11s} {er:8.2f} ± {es:.2f} "
                  f"{agg(sn,fit,'n_sigs')[0]:12.1f} {agg(sn,fit,'novelty')[0]:8.2f} "
                  f"{agg(sn,fit,'cross_prod')[0]:7.1f}")
    print("\nlever effects on edge-set heredity (self/null):")
    print(f"  substrate SKI->BCW (network fitness): "
          f"{agg('SKI','network','edge_ratio')[0]:.2f} -> {agg('BCW','network','edge_ratio')[0]:.2f}")
    print(f"  fitness network->breed_true (BCW): "
          f"{agg('BCW','network','edge_ratio')[0]:.2f} -> {agg('BCW','breed_true','edge_ratio')[0]:.2f} "
          f"(novelty {agg('BCW','network','novelty')[0]:.2f} -> {agg('BCW','breed_true','novelty')[0]:.2f})")


if __name__ == '__main__':
    main()
