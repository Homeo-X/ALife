"""exp017 mechanism sweep: can ANY exposed lever convert the capped collective-
heredity plateau into genuine between-deme winnowing? Tests the homogenization
hypothesis using only exposed knobs (mig_rate, propagule_size, deme_gen).

If isolating demes (mig_rate=0) + a dominant propagule still leaves the heredity
gap capped and n_deme_types un-winnowed, the cap is the *global feed*, not the
migration/propagule channels.
"""
from __future__ import annotations
import json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = 6000
SEEDS = list(range(4))

CONDITIONS = {
    "baseline (mig .02, psize 4, gen 40)":   dict(mig_rate=0.02, propagule_size=4,  deme_gen=40),
    "isolation (mig 0)":                      dict(mig_rate=0.0,  propagule_size=4,  deme_gen=40),
    "big propagule (psize 16)":               dict(mig_rate=0.02, propagule_size=16, deme_gen=40),
    "isolation+big+fast (mig0,ps16,gen20)":   dict(mig_rate=0.0,  propagule_size=16, deme_gen=20),
}


def one_run(args):
    label, kw, seed = args
    build = get_experiment('exp017')
    physics, cfg = build(seed=seed, ticks=TICKS, n_patches=24,
                         propagule_mode='source', **kw)
    res = run(physics, cfg)
    hs, hn = physics._hered_self, physics._hered_null
    # late = last third of temporally-ordered heredity measurements
    def late(x):
        seg = x[2 * len(x) // 3:]
        return mean(seg) if seg else 0.0
    ndt = [m['gauges'].get('n_deme_types', 0.0) for m in res.metrics]
    return {
        "label": label, "seed": seed,
        "gap_late": late(hs) - late(hn),
        "self_late": late(hs), "null_late": late(hn),
        "ndt_late": mean(ndt[-len(ndt)//5:]) if ndt else 0.0,
        "final_pop": res.final_population,
    }


def main():
    jobs = [(label, kw, s) for label, kw in CONDITIONS.items() for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds/condition\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_run, jobs))
    json.dump(rows, open('studies/exp017_mechanism_results.json', 'w'), indent=2)

    print(f"{'condition':40s} {'gap_late':>10s} {'n_deme_types':>13s} {'final_pop':>10s}")
    print("-" * 76)
    for label in CONDITIONS:
        rs = [r for r in rows if r['label'] == label]
        g = [r['gap_late'] for r in rs]
        ndt = [r['ndt_late'] for r in rs]
        pop = [r['final_pop'] for r in rs]
        pos = sum(1 for x in g if x > 0)
        print(f"{label:40s} {mean(g):+.4f}±{pstdev(g):.4f}  {mean(ndt):5.1f}/24  "
              f"{mean(pop):6.0f}   (+gap {pos}/{len(rs)})")


if __name__ == '__main__':
    main()
