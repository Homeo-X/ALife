"""exp018 — can collectives outcompete individuals once the substrate supplies
BOTH ingredients multi-level selection needs? 2x2 factorial:

    deme_fitness  in {size, productivity}   (heritable between-deme fitness variance)
    heredity      in {weak, strong}         (weak = exp017 defaults; strong = isolated
                                             demes + deme-dominating propagule + fast turnover)

Winnowing of n_deme_types (fit deme-types sweeping) is the signature that the
collective is winning. Run: PYTHONPATH=. python3 studies/exp018_collective_fitness.py
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
SEEDS = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 6))

WEAK = dict(mig_rate=0.02, propagule_size=4, deme_gen=40)
STRONG = dict(mig_rate=0.0, propagule_size=16, deme_gen=20)

CELLS = {
    "size / weak  (=exp017 baseline)": dict(deme_fitness="size", **WEAK),
    "size / strong": dict(deme_fitness="size", **STRONG),
    "productivity / weak": dict(deme_fitness="productivity", **WEAK),
    "productivity / strong (=exp018)": dict(deme_fitness="productivity", **STRONG),
}


def one_run(args):
    label, kw, seed = args
    physics, cfg = get_experiment('exp017')(seed=seed, ticks=TICKS, n_patches=24,
                                            propagule_mode='source', **kw)
    res = run(physics, cfg)
    ndt = [m['gauges'].get('n_deme_types', 0.0) for m in res.metrics]
    hs, hn = physics._hered_self, physics._hered_null

    def late(x):
        seg = x[2 * len(x) // 3:]
        return mean(seg) if seg else 0.0
    return {
        "label": label, "seed": seed,
        "ndt_early": mean(ndt[:len(ndt) // 3]) if ndt else 0.0,
        "ndt_late": mean(ndt[-len(ndt) // 5:]) if ndt else 0.0,
        "ndt_min": min(ndt) if ndt else 0.0,
        "gap_late": late(hs) - late(hn),
        "self_late": late(hs), "null_late": late(hn),
        "final_pop": res.final_population,
    }


def main():
    jobs = [(label, kw, s) for label, kw in CELLS.items() for s in SEEDS]
    print(f"{len(jobs)} runs @ {TICKS} ticks, {len(SEEDS)} seeds/cell\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_run, jobs))
    json.dump(rows, open('studies/exp018_results.json', 'w'), indent=2)

    print(f"{'cell':34s} {'n_deme_types (early>late, min)':32s} {'heredity self/null':20s} {'pop':>5s}")
    print("-" * 96)
    for label in CELLS:
        rs = [r for r in rows if r['label'] == label]
        e, l = mean(r['ndt_early'] for r in rs), mean(r['ndt_late'] for r in rs)
        mn = mean(r['ndt_min'] for r in rs)
        s, n = mean(r['self_late'] for r in rs), mean(r['null_late'] for r in rs)
        pop = mean(r['final_pop'] for r in rs)
        ld = pstdev(r['ndt_late'] for r in rs)
        print(f"{label:34s} {e:5.1f} -> {l:5.1f} ±{ld:4.1f} (min {mn:4.1f})/24   "
              f"{s:.3f}/{n:.3f} ({s/n if n else 0:.2f}x)   {pop:5.0f}")


if __name__ == '__main__':
    main()
