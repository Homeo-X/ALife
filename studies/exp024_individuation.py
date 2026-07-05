"""exp024 — the combination: recycle feed (exp023 within-deme dominance) + network
fitness (exp022 collective selection) + monoculture founding (forced divergence) +
isolation. Does combining every partial lever finally individuate demes — discrete,
heritable collective individuals — or do they collapse onto shared global attractors?

Measures within-deme dominance, collective heredity ratio (self/null Jaccard), and
n_deme_types trajectory, source vs mixed. Also reports the substrate type-space
diagnostic (how many distinct stable normal forms the feed actually offers).
Run: PYTHONPATH=. python3 studies/exp024_individuation.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments import exp012_combinator as M
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run
from omega.kernel.organization import canonical_cls
from omega.substrate.noise import Noise

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))


def one(args):
    exp, mode, seed = args
    p, c = get_experiment(exp)(seed=seed, ticks=TICKS, n_patches=24, propagule_mode=mode)
    dom = []
    _orig = p._deme_reproduction

    def wrapped(u, rng, _orig=_orig, _p=p):
        by = {}
        for o in u.organizations.values():
            pi = _p._patch.get(o.uid)
            if pi is not None:
                by.setdefault(pi, []).append(o)
        ds = [Counter(o.cls for o in v).most_common(1)[0][1] / len(v)
              for v in by.values() if len(v) >= 3]
        if ds:
            dom.append(mean(ds))
        return _orig(u, rng)

    p._deme_reproduction = wrapped
    r = run(p, c)
    g = [m['gauges'].get('n_deme_types', 0.0) for m in r.metrics]
    hs = mean(p._hered_self) if p._hered_self else 0.0
    hn = mean(p._hered_null) if p._hered_null else 1e-9
    return {"exp": exp, "mode": mode, "seed": seed,
            "within_dom": mean(dom[-len(dom) // 3:]) if dom else 0.0,
            "hered_ratio": hs / (hn + 1e-9),
            "ndt_t0": g[0] if g else 0.0,
            "ndt_late": mean(g[-len(g) // 5:]) if g else 0.0,
            "pop": r.final_population}


def type_space_diagnostic():
    p, _ = get_experiment('exp024')(seed=0, n_patches=24)
    rng = Noise(0)
    cls = [canonical_cls(p._random_normal(rng)) for _ in range(5000)]
    ctr = Counter(cls)
    top = [round(n / 5000, 3) for _, n in ctr.most_common(9)]
    return len(ctr), sum(n for _, n in ctr.most_common(9)) / 5000, top


def main():
    jobs = [(exp, m, s) for exp in ('exp023', 'exp024')
            for m in ('source', 'mixed') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp024_results.json', 'w'), indent=2)

    def agg(exp, mode, k):
        return mean(r[k] for r in rows if r['exp'] == exp and r['mode'] == mode)

    print(f"{'exp':>7s} {'mode':>7s} {'within-dom':>10s} {'heredity s/n':>12s} "
          f"{'ndt @t0':>8s} {'ndt late':>9s}")
    print("-" * 60)
    for exp in ('exp023', 'exp024'):
        for mode in ('source', 'mixed'):
            print(f"{exp:>7s} {mode:>7s} {agg(exp,mode,'within_dom'):10.3f} "
                  f"{agg(exp,mode,'hered_ratio'):12.2f} {agg(exp,mode,'ndt_t0'):8.1f} "
                  f"{agg(exp,mode,'ndt_late'):9.1f}")
    print("\nindividuation check (exp024, source vs mixed):")
    print(f"  within-dom: {agg('exp024','source','within_dom'):.3f} vs {agg('exp024','mixed','within_dom'):.3f}")
    print(f"  ndt late  : {agg('exp024','source','ndt_late'):.1f} vs {agg('exp024','mixed','ndt_late'):.1f}")
    n, cov9, top = type_space_diagnostic()
    print(f"\nsubstrate type-space diagnostic (feed distribution, 5000 draws):")
    print(f"  distinct normal forms: {n};  top-9 cover {cov9:.2f} of mass;  top-9 freqs: {top}")
    print("  -> monoculture founders collide onto ~a dozen shared attractor types;")
    print("     24 demes cannot be given distinct persistent identities.")


if __name__ == '__main__':
    main()
