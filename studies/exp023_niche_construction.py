"""exp023 — niche construction: does recycling a deme's own products as its feed
lift within-deme dominance and let demes individuate, without collapsing OEI?

2x2: feed_mode {random, recycle} x propagule {source, mixed}. Measures within-deme
dominance, n_deme_types (source<mixed => genuine collective individuation), the OEI
verdict/novelty (must not collapse), and per-deme self-sufficiency. The wall from
exp017-022 was within-deme dominance stuck at ~0.37 under a diluting random feed.
Run: PYTHONPATH=. python3 studies/exp023_niche_construction.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments import exp012_combinator as M
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))


def one(args):
    feed_mode, mode, seed = args
    # exp023 defaults carry feed_mode=recycle; override to "random" for the baseline.
    p, c = get_experiment('exp023')(seed=seed, ticks=TICKS, n_patches=24,
                                    propagule_mode=mode, feed_mode=feed_mode)
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
    tail = r.metrics[-len(r.metrics) // 5:]
    ndt = mean(m['gauges'].get('n_deme_types', 0.0) for m in tail)
    live = mean(m['gauges'].get('n_live_demes', 0.0) for m in tail)
    return {
        "feed": feed_mode, "mode": mode, "seed": seed,
        "within_dom": mean(dom[-len(dom) // 3:]) if dom else 0.0,
        "ndt": ndt, "types_per_live": ndt / live if live else 0.0,
        "oei": r.open_endedness["index"], "verdict": r.open_endedness["verdict"],
        "novelty_rate": r.open_endedness["novelty_rate"],
        "classes": r.final_classes_total, "pop": r.final_population,
    }


def main():
    jobs = [(fm, m, s) for fm in ('random', 'recycle')
            for m in ('source', 'mixed') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, jobs))
    json.dump(rows, open('studies/exp023_results.json', 'w'), indent=2)

    def agg(fm, mode, key):
        return mean(r[key] for r in rows if r['feed'] == fm and r['mode'] == mode)

    print(f"{'feed':>8s} {'mode':>7s} {'within-dom':>10s} {'n_deme_types':>12s} "
          f"{'types/live':>11s} {'OEI':>7s} {'novelty_rate':>12s} {'classes':>8s}")
    print("-" * 82)
    for fm in ('random', 'recycle'):
        for mode in ('source', 'mixed'):
            print(f"{fm:>8s} {mode:>7s} {agg(fm,mode,'within_dom'):10.3f} "
                  f"{agg(fm,mode,'ndt'):12.1f} {agg(fm,mode,'types_per_live'):11.3f} "
                  f"{agg(fm,mode,'oei'):7.3f} {agg(fm,mode,'novelty_rate'):12.3f} "
                  f"{agg(fm,mode,'classes'):8.0f}")
    print("\nindividuation check (source n_deme_types below mixed => collective winnowing):")
    for fm in ('random', 'recycle'):
        s = agg(fm, 'source', 'ndt'); x = agg(fm, 'mixed', 'ndt')
        st = agg(fm, 'source', 'types_per_live'); xt = agg(fm, 'mixed', 'types_per_live')
        print(f"  {fm:>7s}: ndt source {s:.1f} vs mixed {x:.1f} (diff {s-x:+.1f}); "
              f"types/live source {st:.3f} vs mixed {xt:.3f} (diff {st-xt:+.3f})")


if __name__ == '__main__':
    main()
