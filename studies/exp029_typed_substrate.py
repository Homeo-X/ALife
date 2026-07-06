"""exp029 — the substrate pivot. exp028 proved the ~3.3x individuation ceiling is
substrate-limited: combinator reduction doesn't re-form a deme's network from identical
members. This pivots to a TYPED substrate — morphisms (in,out) with modular composition
((a->b)o(b->c)=(a->c)) — so a deme's network is deterministic in its member set. Does
modularity break the reproducibility ceiling, and at what cost?

Compares combinator (exp027 BCWTV) vs typed (exp029) on the same collective machinery,
and sweeps n_types. Reports edge-set heredity self/null, cross-production/signature
size (network richness), and novelty (open-endedness). Run:
PYTHONPATH=. python3 studies/exp029_typed_substrate.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def _metrics(p, r):
    es = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    en = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    tail = r.metrics[-len(r.metrics) // 5:]
    g = lambda k: mean(m['gauges'].get(k, 0.0) for m in tail)
    return {"self": es, "null": en, "ratio": es / (en + 1e-9) if es else 0.0,
            "xprod": g('mean_cross_prod'), "sig_size": g('mean_signature_size'),
            "novelty": r.open_endedness["novelty_rate"]}


def one_compare(args):
    arm, seed = args
    if arm == "combinator":
        p, c = get_experiment('exp027')(seed=seed, ticks=int(TICKS), n_patches=24,
                                        propagule_mode='source', extra_combinators="B,C,W,T,V")
    else:
        p, c = get_experiment('exp029')(seed=seed, ticks=int(TICKS), n_patches=24,
                                        propagule_mode='source')
    r = run(p, c)
    return {"arm": arm, "seed": seed, **_metrics(p, r)}


def one_ntypes(args):
    nt, seed = args
    p, c = get_experiment('exp029')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source', n_types=nt)
    r = run(p, c)
    return {"n_types": nt, "seed": seed, **_metrics(p, r)}


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    with ProcessPoolExecutor(max_workers=8) as ex:
        cmp = list(ex.map(one_compare, [(a, s) for a in ("combinator", "typed") for s in seeds]))
        nts = list(ex.map(one_ntypes, [(nt, s) for nt in (6, 12, 24, 48) for s in seeds]))
    json.dump({"compare": cmp, "n_types": nts}, open('studies/exp029_results.json', 'w'), indent=2)

    def ag(rows, key, k):
        v = [r[k] for r in rows if r.get('arm') == key or r.get('n_types') == key]
        return mean(v), pstdev(v)

    print(f"combinator (exp027 BCWTV) vs typed (exp029), source, {len(seeds)} seeds:")
    print(f"{'arm':>11s} {'edge self':>10s} {'edge null':>10s} {'self/null':>10s} "
          f"{'x-prod':>7s} {'sig_size':>9s} {'novelty':>8s}")
    for arm in ("combinator", "typed"):
        print(f"{arm:>11s} {ag(cmp,arm,'self')[0]:10.3f} {ag(cmp,arm,'null')[0]:10.3f} "
              f"{ag(cmp,arm,'ratio')[0]:10.2f} {ag(cmp,arm,'xprod')[0]:7.1f} "
              f"{ag(cmp,arm,'sig_size')[0]:9.2f} {ag(cmp,arm,'novelty')[0]:8.2f}")
    print("\ntyped substrate, n_types sweep (ratio climbs but networks thin, novelty~0):")
    print(f"{'n_types':>8s} {'edge self':>10s} {'self/null':>10s} {'x-prod':>7s} "
          f"{'sig_size':>9s} {'novelty':>8s}")
    for nt in (6, 12, 24, 48):
        print(f"{nt:>8d} {ag(nts,nt,'self')[0]:10.3f} {ag(nts,nt,'ratio')[0]:10.2f} "
              f"{ag(nts,nt,'xprod')[0]:7.1f} {ag(nts,nt,'sig_size')[0]:9.2f} "
              f"{ag(nts,nt,'novelty')[0]:8.2f}")


if __name__ == '__main__':
    main()
