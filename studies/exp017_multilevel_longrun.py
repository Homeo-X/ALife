"""exp017 long-timescale study: do collectives reliably outcompete individuals,
or collapse? Primary contrast: propagule_mode 'source' (collective heredity ON)
vs 'mixed' (heredity OFF, same disturbance regime). Multiple seeds, long horizon.
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def _win_means(vals, k):
    """Split a temporally-ordered list into k windows, return per-window means."""
    if not vals:
        return [0.0] * k
    n = len(vals)
    out = []
    for i in range(k):
        seg = vals[i * n // k:(i + 1) * n // k]
        out.append(mean(seg) if seg else 0.0)
    return out


def one_run(args):
    mode, seed, ticks, n_patches, deme_gen = args
    build = get_experiment('exp017')
    physics, cfg = build(seed=seed, ticks=ticks, n_patches=n_patches,
                         deme_gen=deme_gen, propagule_mode=mode)
    res = run(physics, cfg)

    gseries = [m['gauges'] for m in res.metrics]
    ndt = [g.get('n_deme_types', float('nan')) for g in gseries]
    nld = [g.get('n_live_demes', float('nan')) for g in gseries]
    pop = [m['population'] for m in res.metrics]
    ent = [m['entropy_bits'] for m in res.metrics]
    amp = [g.get('amplification', 0.0) for g in gseries]

    K = 5  # trajectory windows
    hs, hn = physics._hered_self, physics._hered_null
    self_w = _win_means(hs, K)
    null_w = _win_means(hn, K)
    gap_w = [s - n for s, n in zip(self_w, null_w)]

    def tail(x, frac=0.2):
        m = max(1, int(len(x) * frac))
        return x[-m:]

    return {
        'mode': mode, 'seed': seed, 'ticks': ticks,
        'final_pop': res.final_population,
        'classes_ever': res.final_classes_total,
        'hered_self_windows': self_w,
        'hered_null_windows': null_w,
        'hered_gap_windows': gap_w,
        'hered_n_measurements': len(hs),
        'ndt_early': mean(ndt[:len(ndt)//3]) if ndt else 0.0,
        'ndt_late': mean(tail(ndt)) if ndt else 0.0,
        'nld_late': mean(tail(nld)) if nld else 0.0,
        'pop_late': mean(tail(pop)) if pop else 0.0,
        'pop_min': min(pop) if pop else 0,
        'entropy_late': mean(tail(ent)) if ent else 0.0,
        'amp_late': mean(tail(amp)) if amp else 0.0,
    }


def main():
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 8))
    n_patches, deme_gen = 24, 40
    jobs = [(mode, s, ticks, n_patches, deme_gen)
            for mode in ('source', 'mixed') for s in seeds]
    print(f"running {len(jobs)} runs @ {ticks} ticks, seeds={seeds}", flush=True)

    with ProcessPoolExecutor(max_workers=min(8, len(jobs))) as ex:
        rows = list(ex.map(one_run, jobs))

    with open('studies/exp017_longrun_results.json', 'w') as f:
        json.dump(rows, f, indent=2)

    # ---- summary ----
    def agg(mode, key):
        vals = [r[key] for r in rows if r['mode'] == mode]
        return mean(vals), pstdev(vals)

    print("\n" + "=" * 78)
    print(f"exp017 collectives-vs-individuals | {ticks} ticks | {len(seeds)} seeds/arm")
    print("=" * 78)
    for mode in ('source', 'mixed'):
        rs = [r for r in rows if r['mode'] == mode]
        K = len(rs[0]['hered_gap_windows'])
        gap_late = [r['hered_gap_windows'][-1] for r in rs]
        self_late = [r['hered_self_windows'][-1] for r in rs]
        null_late = [r['hered_null_windows'][-1] for r in rs]
        print(f"\n[{mode}]")
        print(f"  collective heredity gap (self-null Jaccard) trajectory ({K} windows):")
        traj = [mean(r['hered_gap_windows'][w] for r in rs) for w in range(K)]
        print("     " + "  ".join(f"{g:+.4f}" for g in traj))
        print(f"     late window: {mean(gap_late):+.4f} ± {pstdev(gap_late):.4f}  "
              f"(self {mean(self_late):.3f} vs null {mean(null_late):.3f})")
        pos = sum(1 for g in gap_late if g > 0)
        print(f"     seeds with POSITIVE late gap: {pos}/{len(rs)}")
        print(f"  between-deme diversity n_deme_types: "
              f"early {agg(mode,'ndt_early')[0]:.1f} -> late {agg(mode,'ndt_late')[0]:.1f}")
        print(f"  collapse check: final_pop {agg(mode,'final_pop')[0]:.0f}"
              f"±{agg(mode,'final_pop')[1]:.0f}, pop_min {min(r['pop_min'] for r in rs)}, "
              f"live_demes_late {agg(mode,'nld_late')[0]:.1f}/24")
        print(f"  organization: amp_late {agg(mode,'amp_late')[0]:.1f}, "
              f"entropy_late {agg(mode,'entropy_late')[0]:.2f}, "
              f"classes_ever {agg(mode,'classes_ever')[0]:.0f}")


if __name__ == '__main__':
    main()
