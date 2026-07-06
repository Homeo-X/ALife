"""exp025 — combinatorial deme identity: is a deme's cross-production NETWORK
SIGNATURE (edge-set) a more heritable collective phenotype than its dominant class?

exp024 found individuation blocked because deme identity (dominant class) draws from
only ~9 attractor types. Here identity = the set of active producer->product edges,
a combinatorially larger space. Headline comparison (within source runs): edge-set
heredity ratio (self/null Jaccard) vs the class-set heredity ratio, and whether the
signature space (n_deme_signatures) is richer than the class space (n_deme_types).
Run: PYTHONPATH=. python3 studies/exp025_network_identity.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def one(args):
    mode, seed = args
    p, c = get_experiment('exp025')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode=mode)
    r = run(p, c)

    def ratio(s, n):
        return (mean(s) / (mean(n) + 1e-9)) if (s and n) else 0.0
    tail = r.metrics[-len(r.metrics) // 5:]
    return {
        "mode": mode, "seed": seed,
        "edge_self": mean(p._hered_edge_self) if p._hered_edge_self else 0.0,
        "edge_null": mean(p._hered_edge_null) if p._hered_edge_null else 0.0,
        "edge_ratio": ratio(p._hered_edge_self, p._hered_edge_null),
        "class_ratio": ratio(p._hered_self, p._hered_null),
        "n_sigs": mean(m['gauges'].get('n_deme_signatures', 0.0) for m in tail),
        "n_types": mean(m['gauges'].get('n_deme_types', 0.0) for m in tail),
        "sig_size": mean(m['gauges'].get('mean_signature_size', 0.0) for m in tail),
        "novelty": r.open_endedness["novelty_rate"],
    }


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    jobs = [(m, s) for m in ('source', 'mixed') for s in seeds]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(seeds)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp025_results.json', 'w'), indent=2)

    def agg(mode, k):
        v = [r[k] for r in rows if r['mode'] == mode]
        return mean(v), pstdev(v)

    print("HEADLINE (source runs): is the network signature more heritable than the class?")
    er, ers = agg('source', 'edge_ratio')
    cr, crs = agg('source', 'class_ratio')
    print(f"  edge-set heredity ratio (self/null): {er:.2f} ± {ers:.2f}")
    print(f"  class-set heredity ratio (self/null): {cr:.2f} ± {crs:.2f}")
    print(f"  edge self/null raw: {agg('source','edge_self')[0]:.3f} / {agg('source','edge_null')[0]:.3f}")
    print(f"  seeds with edge_ratio > class_ratio: "
          f"{sum(1 for r in rows if r['mode']=='source' and r['edge_ratio']>r['class_ratio'])}"
          f"/{len(seeds)}")
    print("\nidentity-space richness and novelty:")
    print(f"{'mode':>7s} {'n_signatures':>12s} {'n_deme_types':>12s} {'sig_size':>9s} {'novelty':>8s}")
    for mode in ('source', 'mixed'):
        print(f"{mode:>7s} {agg(mode,'n_sigs')[0]:12.1f} {agg(mode,'n_types')[0]:12.1f} "
              f"{agg(mode,'sig_size')[0]:9.1f} {agg(mode,'novelty')[0]:8.2f}")


if __name__ == '__main__':
    main()
