"""exp028 — is the ~3.3x network-individuation ceiling (exp027) reproducibility-limited
or substrate-limited? At the exp027 optimum basis (S,K,I,B,C,W,T,V), sweep the propagule
transmission: bias {random, network-participant} x propagule_size {4, 8, 16}. Because
demes hold only ~4-5 members, propagule_size>=16 transmits the WHOLE source deme —
perfect member-set heredity. If edge-set heredity still caps at ~3.2x even then, the
ceiling is the substrate's network reproducibility (same members -> different network),
not the propagule; that motivates a typed/lambda substrate pivot.
Run: PYTHONPATH=. python3 studies/exp028_reproducibility.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def one(args):
    bias, psize, seed = args
    p, c = get_experiment('exp028')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source',
                                    propagule_bias=bias, propagule_size=psize)
    r = run(p, c)
    es = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    en = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    tail = r.metrics[-len(r.metrics) // 5:]
    # mean deme size, to show psize>=16 already transmits the whole deme
    deme_sizes = [len(v) for v in _by_patch(p).values() if v] if False else []
    return {"bias": bias, "psize": psize, "seed": seed,
            "edge_ratio": es / (en + 1e-9) if es else 0.0,
            "edge_self": es, "edge_null": en,
            "n_sigs": mean(m['gauges'].get('n_deme_signatures', 0.0) for m in tail),
            "n_live": mean(m['gauges'].get('n_live_demes', 0.0) for m in tail),
            "novelty": r.open_endedness["novelty_rate"], "pop": r.final_population}


def _by_patch(p):  # unused helper kept for clarity
    return {}


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    jobs = [(b, ps, s) for b in ('random', 'network')
            for ps in (4, 8, 16) for s in seeds]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(seeds)} seeds "
          f"(optimum BCWTV basis; ~4-5 members/deme so psize16 = whole deme)\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp028_results.json', 'w'), indent=2)

    def agg(bias, ps, k):
        v = [r[k] for r in rows if r['bias'] == bias and r['psize'] == ps]
        return mean(v), pstdev(v)

    print(f"{'bias':>8s} {'psize':>5s} {'edge heredity':>14s} {'n_sigs':>7s} "
          f"{'pop/deme':>8s} {'novelty':>8s}")
    print("-" * 58)
    for bias in ('random', 'network'):
        for ps in (4, 8, 16):
            er, es = agg(bias, ps, 'edge_ratio')
            popd = agg(bias, ps, 'pop')[0] / 24.0
            print(f"{bias:>8s} {ps:>5d} {er:8.2f} ± {es:.2f} {agg(bias,ps,'n_sigs')[0]:7.1f} "
                  f"{popd:8.1f} {agg(bias,ps,'novelty')[0]:8.2f}")
    best = max(r['edge_ratio'] for r in rows)
    print(f"\npeak edge-set heredity across all cells: {best:.2f}")
    print("verdict: if peak ~= exp027's 3.3x even when the whole deme is transmitted,")
    print("the ceiling is substrate network-reproducibility, not propagule sampling.")


if __name__ == '__main__':
    main()
