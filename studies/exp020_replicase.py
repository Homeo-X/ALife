"""exp020 — explicit replicase: does a strong copy channel finally let collectives
outcompete individuals? An explicit T -> T + T copy reaction (reservoir-limited,
copy_mut fidelity) is added on top of exp019 (local feed + collective machinery).

Two things to separate:
  (1) does within-deme dominance clear ~0.5 (a crisp heritable deme type)?
  (2) the n_deme_types consolidation copying causes — is it collective SELECTION
      (source winnows below the mixed null) or just a few compact replicators
      colonizing every deme globally (source ~= mixed)?

Records within-deme dominance, GLOBAL dominance, n_deme_types, types-per-live-deme,
and population for source vs mixed. Run: PYTHONPATH=. python3 studies/exp020_replicase.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
COPY_RATES = [0.0, 0.5]


def one_run(args):
    copy_rate, mode, seed = args
    physics, cfg = get_experiment('exp020')(seed=seed, ticks=TICKS, n_patches=24,
                                            propagule_mode=mode, copy_rate=copy_rate)
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
    gdom = mean(m['gauges'].get('dominance', 0.0) for m in tail)
    return {
        "copy_rate": copy_rate, "mode": mode, "seed": seed,
        "within_dom": mean(dom_trace[-len(dom_trace) // 3:]) if dom_trace else 0.0,
        "global_dom": gdom, "ndt_late": ndt, "live_late": live,
        "types_per_live": ndt / live if live else 0.0,
        "final_pop": res.final_population,
    }


def main():
    jobs = [(cr, m, s) for cr in COPY_RATES for m in ('source', 'mixed') for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_run, jobs))
    json.dump(rows, open('studies/exp020_results.json', 'w'), indent=2)

    print(f"{'copy':>5s} {'mode':>7s} {'within-dom':>10s} {'global-dom':>10s} "
          f"{'n_deme_types':>12s} {'live':>8s} {'types/live':>11s} {'pop':>6s}")
    print("-" * 78)
    for cr in COPY_RATES:
        for m in ('source', 'mixed'):
            rs = [r for r in rows if r['copy_rate'] == cr and r['mode'] == m]
            tl = [r['types_per_live'] for r in rs]
            print(f"{cr:5.1f} {m:>7s} {mean(r['within_dom'] for r in rs):10.3f} "
                  f"{mean(r['global_dom'] for r in rs):10.3f} "
                  f"{mean(r['ndt_late'] for r in rs):12.1f} "
                  f"{mean(r['live_late'] for r in rs):6.1f}/24 "
                  f"{mean(tl):8.3f}±{pstdev(tl):.3f} {mean(r['final_pop'] for r in rs):6.0f}")


if __name__ == '__main__':
    main()
