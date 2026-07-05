"""exp019 — does patch-local feed unlock within-deme dominance without collapse?

exp018 showed the only way to raise within-deme dominance was to starve the global
feed, which kills demes (collapse, not collective victory). Local feed directs the
same total feed to under-full patches, so scarce feed keeps empty demes alive while
filled demes self-sustain. Question: at low feed, does local feed hold more demes
alive (higher dominance at matched survival) than global feed — and does the
collective then winnow (types-per-live-deme below the mixed null)?

Sweeps feed_rate x {global=exp018, local=exp019}. Records within-deme dominance,
survival, and collective winnowing together.
Run: PYTHONPATH=. python3 studies/exp019_local_feed.py [ticks] [n_seeds]
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
FEEDS = [8, 4, 2, 1]


def one_run(args):
    feed, mode, seed = args
    exp = 'exp019' if mode == 'local' else 'exp018'
    physics, cfg = get_experiment(exp)(seed=seed, ticks=TICKS, n_patches=24)
    physics.feed_rate = feed

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

    tail = res.metrics[-len(res.metrics) // 5:]
    ndt = mean(m['gauges'].get('n_deme_types', 0.0) for m in tail)
    live = mean(m['gauges'].get('n_live_demes', 0.0) for m in tail)
    return {
        "feed": feed, "mode": mode, "seed": seed,
        "within_dom": mean(dom_trace[-len(dom_trace) // 3:]) if dom_trace else 0.0,
        "ndt_late": ndt, "live_late": live,
        "types_per_live": ndt / live if live else 0.0,
        "final_pop": res.final_population,
    }


def main():
    jobs = [(f, m, s) for f in FEEDS for m in ('global', 'local') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_run, jobs))
    json.dump(rows, open('studies/exp019_results.json', 'w'), indent=2)

    print(f"{'feed':>4s} {'mode':>7s} {'within-dom':>10s} {'live_demes':>11s} "
          f"{'pop':>5s} {'n_deme_types':>12s} {'types/live':>11s}")
    print("-" * 68)
    for f in FEEDS:
        for m in ('global', 'local'):
            rs = [r for r in rows if r['feed'] == f and r['mode'] == m]
            print(f"{f:4d} {m:>7s} {mean(r['within_dom'] for r in rs):10.3f} "
                  f"{mean(r['live_late'] for r in rs):8.1f}/24 "
                  f"{mean(r['final_pop'] for r in rs):5.0f} "
                  f"{mean(r['ndt_late'] for r in rs):12.1f} "
                  f"{mean(r['types_per_live'] for r in rs):11.2f}")


if __name__ == '__main__':
    main()
