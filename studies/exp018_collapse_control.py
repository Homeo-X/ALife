"""Control: at low feed, is the n_deme_types drop genuine collective selection or
just deme die-off? Compare source (collective heredity+selection ON) vs mixed
(OFF) at the SAME feed/disturbance. If source winnows below mixed at matched
population/live-demes, that's real collective selection; if source ~= mixed, the
drop is collapse, not the collective winning.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

SEEDS = list(range(5))


def one(args):
    feed, mode, seed = args
    physics, cfg = get_experiment('exp018')(seed=seed, ticks=6000, n_patches=24,
                                            propagule_mode=mode)
    physics.feed_rate = feed
    res = run(physics, cfg)
    tail = res.metrics[-len(res.metrics) // 5:]
    ndt = mean(m['gauges'].get('n_deme_types', 0.0) for m in tail)
    live = mean(m['gauges'].get('n_live_demes', 0.0) for m in tail)
    return {"feed": feed, "mode": mode, "seed": seed, "ndt": ndt,
            "live": live, "pop": res.final_population,
            "types_per_live": ndt / live if live else 0.0}


jobs = [(f, m, s) for f in (4, 2) for m in ("source", "mixed") for s in SEEDS]
with ProcessPoolExecutor(max_workers=8) as ex:
    rows = list(ex.map(one, jobs))

print(f"{'feed':>4s} {'mode':>7s} {'n_deme_types':>13s} {'live_demes':>11s} "
      f"{'types/live':>11s} {'pop':>5s}")
print("-" * 60)
for f in (4, 2):
    for m in ("source", "mixed"):
        rs = [r for r in rows if r['feed'] == f and r['mode'] == m]
        print(f"{f:4d} {m:>7s} {mean(r['ndt'] for r in rs):10.1f}±{pstdev(r['ndt'] for r in rs):3.1f} "
              f"{mean(r['live'] for r in rs):9.1f}/24 {mean(r['types_per_live'] for r in rs):10.2f} "
              f"{mean(r['pop'] for r in rs):5.0f}")
