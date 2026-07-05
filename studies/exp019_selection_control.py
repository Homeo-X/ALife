"""Decisive control for exp019: at local feed, is the low types-per-live-deme
genuine collective selection or just a property of local+low feed? Compare source
(selection ON) vs mixed (OFF) under LOCAL feed at feed in {4,2}. If source's
types-per-live-deme is meaningfully below mixed at matched survival, collectives
are finally outcompeting individuals.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

SEEDS = list(range(6))


def one(args):
    feed, mode, seed = args
    physics, cfg = get_experiment('exp019')(seed=seed, ticks=6000, n_patches=24,
                                            propagule_mode=mode)
    physics.feed_rate = feed
    res = run(physics, cfg)
    tail = res.metrics[-len(res.metrics) // 5:]
    ndt = mean(m['gauges'].get('n_deme_types', 0.0) for m in tail)
    live = mean(m['gauges'].get('n_live_demes', 0.0) for m in tail)
    return {"feed": feed, "mode": mode, "seed": seed, "ndt": ndt, "live": live,
            "pop": res.final_population, "types_per_live": ndt / live if live else 0.0}


jobs = [(f, m, s) for f in (4, 2) for m in ("source", "mixed") for s in SEEDS]
with ProcessPoolExecutor(max_workers=8) as ex:
    rows = list(ex.map(one, jobs))

print(f"LOCAL feed | {len(SEEDS)} seeds")
print(f"{'feed':>4s} {'mode':>7s} {'n_deme_types':>13s} {'live':>9s} {'types/live':>12s} {'pop':>5s}")
print("-" * 56)
for f in (4, 2):
    for m in ("source", "mixed"):
        rs = [r for r in rows if r['feed'] == f and r['mode'] == m]
        tl = [r['types_per_live'] for r in rs]
        print(f"{f:4d} {m:>7s} {mean(r['ndt'] for r in rs):10.1f}   {mean(r['live'] for r in rs):6.1f}/24 "
              f"{mean(tl):9.3f}±{pstdev(tl):.3f} {mean(r['pop'] for r in rs):5.0f}")
