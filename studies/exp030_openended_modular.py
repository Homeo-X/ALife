"""exp030 — the capstone: an OPEN-ENDED and MODULAR substrate. exp029 found the two
substrates are opposite corners of one trade-off (combinator: open-ended but networks
unreproducible; typed: reproducible but closed). typed_path uses variable-length type
PATHS composed by concatenation — modular (networks reproducible) yet paths grow
(open-ended). type_resolution truncates products to their last N nodes, dialing between
the corners. Question: does an intermediate regime give BOTH strong network heredity
AND sustained novelty AND rich networks — a completed transition?

Reports, per (n_types, resolution): edge-set heredity self/null, cross-production and
signature size (network richness), and novelty (open-endedness). The three baselines
(combinator, typed, best typed_path) are printed for comparison.
Run: PYTHONPATH=. python3 studies/exp030_openended_modular.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def _m(p, r):
    es = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    en = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    tail = r.metrics[-len(r.metrics) // 5:]
    g = lambda k: mean(m['gauges'].get(k, 0.0) for m in tail)
    return {"self": es, "null": en, "ratio": es / (en + 1e-9) if es else 0.0,
            "xprod": g('mean_cross_prod'), "sig_size": g('mean_signature_size'),
            "novelty": r.open_endedness["novelty_rate"]}


def one_grid(args):
    nt, res, seed = args
    p, c = get_experiment('exp030')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source', n_types=nt, type_resolution=res)
    r = run(p, c)
    return {"n_types": nt, "res": res, "seed": seed, **_m(p, r)}


def one_baseline(args):
    name, seed = args
    if name == "combinator":
        p, c = get_experiment('exp027')(seed=seed, ticks=int(TICKS), n_patches=24,
                                        propagule_mode='source', extra_combinators="B,C,W,T,V")
    else:  # typed (exp029)
        p, c = get_experiment('exp029')(seed=seed, ticks=int(TICKS), n_patches=24,
                                        propagule_mode='source')
    r = run(p, c)
    return {"name": name, "seed": seed, **_m(p, r)}


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    grid = [(nt, res) for nt in (16, 32, 64) for res in (2, 3, 4)]
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_grid, [(nt, res, s) for (nt, res) in grid for s in seeds]))
        base = list(ex.map(one_baseline, [(n, s) for n in ("combinator", "typed") for s in seeds]))
    json.dump({"grid": rows, "baseline": base}, open('studies/exp030_results.json', 'w'), indent=2)

    def ag(rows, pred, k):
        v = [r[k] for r in rows if pred(r)]
        return mean(v), pstdev(v)

    print("baselines (source, %d seeds): the two corners of the trade-off" % len(seeds))
    print(f"{'substrate':>11s} {'edge self':>10s} {'self/null':>10s} {'x-prod':>7s} {'novelty':>8s}")
    for n in ("combinator", "typed"):
        pr = lambda r, n=n: r['name'] == n
        print(f"{n:>11s} {ag(base,pr,'self')[0]:10.3f} {ag(base,pr,'ratio')[0]:10.2f} "
              f"{ag(base,pr,'xprod')[0]:7.1f} {ag(base,pr,'novelty')[0]:8.2f}")

    print("\nexp030 typed_path grid — looking for BOTH (self>=0.15 AND novelty>0 AND rich):")
    print(f"{'n_types':>7s} {'res':>4s} {'edge self':>10s} {'self/null':>10s} "
          f"{'x-prod':>7s} {'sig_size':>9s} {'novelty':>8s} {'BOTH?':>6s}")
    for nt, res in grid:
        pr = lambda r, nt=nt, res=res: r['n_types'] == nt and r['res'] == res
        s = ag(rows, pr, 'self')[0]; nov = ag(rows, pr, 'novelty')[0]
        xp = ag(rows, pr, 'xprod')[0]
        both = "  <==" if (s >= 0.15 and nov > 0.05 and xp > 2.0) else ""
        print(f"{nt:>7d} {res:>4d} {s:10.3f} {ag(rows,pr,'ratio')[0]:10.2f} "
              f"{xp:7.1f} {ag(rows,pr,'sig_size')[0]:9.2f} {nov:8.2f} {both:>6s}")


if __name__ == '__main__':
    main()
