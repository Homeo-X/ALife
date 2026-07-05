"""exp018 decisive test: collectives can only be selected if they HAVE a heritable
type. The diagnostic showed that at the default feed (14) no class dominates a deme
(within-deme dominance ~0.25) — demes are churning mixes with no 'type', so no
weighting rule can make collectives win. The global feed is the churn source.

Here we cut feed_rate with all collective ingredients ON (productivity fitness +
strong heredity) and measure, together: within-deme dominance (does a local type
form?) and n_deme_types late (does between-deme selection finally winnow?).

Run: PYTHONPATH=. python3 studies/exp018_feed_and_dominance.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
FEEDS = [14, 8, 4, 2]


def one_run(args):
    feed, seed = args
    # exp018 = productivity fitness + strong heredity (mig0, ps16, gen20)
    physics, cfg = get_experiment('exp018')(seed=seed, ticks=TICKS, n_patches=24)
    physics.feed_rate = feed

    # instance-level recorder for within-deme dominance (shadows the bound method)
    dom_trace = []
    _orig = physics._deme_reproduction

    def wrapped(universe, rng, _orig=_orig, _phys=physics):
        by = {}
        for o in universe.organizations.values():
            p = _phys._patch.get(o.uid)
            if p is not None:
                by.setdefault(p, []).append(o)
        ds = [Counter(o.cls for o in v).most_common(1)[0][1] / len(v)
              for v in by.values() if len(v) >= 3]
        if ds:
            dom_trace.append(mean(ds))
        return _orig(universe, rng)

    physics._deme_reproduction = wrapped
    res = run(physics, cfg)

    ndt = [m['gauges'].get('n_deme_types', 0.0) for m in res.metrics]
    hs, hn = physics._hered_self, physics._hered_null

    def late(x):
        seg = x[2 * len(x) // 3:]
        return mean(seg) if seg else 0.0
    return {
        "feed": feed, "seed": seed,
        "within_dom_late": mean(dom_trace[-len(dom_trace) // 3:]) if dom_trace else 0.0,
        "ndt_early": mean(ndt[:len(ndt) // 3]) if ndt else 0.0,
        "ndt_late": mean(ndt[-len(ndt) // 5:]) if ndt else 0.0,
        "heredity_ratio": (late(hs) / late(hn)) if late(hn) else 0.0,
        "final_pop": res.final_population,
        "n_live_demes_late": mean(m['gauges'].get('n_live_demes', 0.0)
                                  for m in res.metrics[-len(res.metrics) // 5:]),
    }


def main():
    jobs = [(f, s) for f in FEEDS for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds/feed "
          f"(productivity fitness + strong heredity)\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_run, jobs))
    json.dump(rows, open('studies/exp018_feed_results.json', 'w'), indent=2)

    print(f"{'feed_rate':>9s} {'within-deme dom':>16s} {'n_deme_types e>late':>21s} "
          f"{'heredity':>9s} {'pop':>6s} {'live demes':>11s}")
    print("-" * 82)
    for f in FEEDS:
        rs = [r for r in rows if r['feed'] == f]
        wd = mean(r['within_dom_late'] for r in rs)
        e = mean(r['ndt_early'] for r in rs)
        l = mean(r['ndt_late'] for r in rs)
        sd = pstdev(r['ndt_late'] for r in rs)
        hr = mean(r['heredity_ratio'] for r in rs)
        pop = mean(r['final_pop'] for r in rs)
        ld = mean(r['n_live_demes_late'] for r in rs)
        print(f"{f:9d} {wd:16.3f} {e:8.1f} ->{l:6.1f}±{sd:3.1f} {hr:9.2f}x {pop:6.0f} {ld:8.1f}/24")


if __name__ == '__main__':
    main()
