"""exp027 — how far does the substrate dial go? A dose-response of collective
individuation vs interacting-basis richness. exp026 showed enriching the combinator
basis (SKI->BCW) lifts network-signature heredity 1.6x->2.4x. Here we sweep the basis
from 3 to 11 combinators and ask: does edge-set heredity keep climbing toward strong
(self >> null), or plateau?

Primary axis = basis richness. Secondary = expression size. For each we report the
edge-set heredity ratio, identity-space size, novelty, and the type-space diagnostic.
Run: PYTHONPATH=. python3 studies/exp027_substrate_dial.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run
from omega.substrate.noise import Noise
from omega.kernel.organization import canonical_cls

# increasing interacting bases (label -> extra_combinators token string)
BASES = [
    ("SKI(3)", ""), ("+B(4)", "B"), ("+BC(5)", "B,C"), ("+BCW(6)", "B,C,W"),
    ("+T(7)", "B,C,W,T"), ("+V(8)", "B,C,W,T,V"), ("+primed(11)", "B,C,W,T,V,B1,C1,S1"),
]


def _edge_heredity(p):
    es = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    en = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    return es, en, (es / (en + 1e-9) if es else 0.0)


def one_basis(args):
    label, extra, seed = args
    p, c = get_experiment('exp027')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source', extra_combinators=extra)
    r = run(p, c)
    es, en, ratio = _edge_heredity(p)
    tail = r.metrics[-len(r.metrics) // 5:]
    return {"label": label, "extra": extra, "seed": seed, "ratio": ratio,
            "n_sigs": mean(m['gauges'].get('n_deme_signatures', 0.0) for m in tail),
            "novelty": r.open_endedness["novelty_rate"],
            "n_atoms": 3 + len([t for t in extra.split(",") if t])}


def one_size(args):
    esz, seed = args
    p, c = get_experiment('exp027')(seed=seed, ticks=int(TICKS), n_patches=24,
                                    propagule_mode='source',
                                    extra_combinators="B,C,W", expr_size=esz)
    r = run(p, c)
    _, _, ratio = _edge_heredity(p)
    return {"expr_size": esz, "seed": seed, "ratio": ratio,
            "novelty": r.open_endedness["novelty_rate"]}


def type_space(extra):
    p, _ = get_experiment('exp027')(seed=0, n_patches=24, extra_combinators=extra)
    rng = Noise(0)
    ctr = Counter(canonical_cls(p._random_normal(rng)) for _ in range(5000))
    return len(ctr), sum(n for _, n in ctr.most_common(9)) / 5000


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    jobs = [(lb, ex, s) for (lb, ex) in BASES for s in seeds]
    print(f"basis dose-response: {len(jobs)} runs @ {TICKS} ticks, {len(seeds)} seeds\n", flush=True)
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one_basis, jobs))
        size_rows = list(ex.map(one_size, [(sz, s) for sz in (5, 8, 12) for s in seeds]))
    json.dump({"basis": rows, "size": size_rows}, open('studies/exp027_results.json', 'w'), indent=2)

    print(f"{'basis':>12s} {'n_atoms':>7s} {'types':>6s} {'top9':>5s} "
          f"{'edge heredity':>14s} {'n_sigs':>7s} {'novelty':>8s}")
    print("-" * 70)
    for lb, ex in BASES:
        rs = [r for r in rows if r['label'] == lb]
        nt, cov = type_space(ex)
        er = [r['ratio'] for r in rs]
        print(f"{lb:>12s} {rs[0]['n_atoms']:>7d} {nt:>6d} {cov:>5.2f} "
              f"{mean(er):8.2f} ± {pstdev(er):.2f} {mean(r['n_sigs'] for r in rs):7.1f} "
              f"{mean(r['novelty'] for r in rs):8.2f}")
    print("\nexpr_size dial (basis fixed at BCW): edge heredity, novelty")
    for sz in (5, 8, 12):
        rs = [r for r in size_rows if r['expr_size'] == sz]
        print(f"  expr_size={sz:2d}: {mean(r['ratio'] for r in rs):.2f} ± "
              f"{pstdev(r['ratio'] for r in rs):.2f}  (novelty {mean(r['novelty'] for r in rs):.2f})")


if __name__ == '__main__':
    main()
