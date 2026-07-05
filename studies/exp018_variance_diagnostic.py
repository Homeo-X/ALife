"""Diagnostic: does the substrate actually provide heritable between-deme fitness
variance? Measure, at each deme-reproduction, the coefficient of variation (CV)
of per-deme productivity and per-deme size, and the mean within-deme dominance
(fraction the most-abundant class holds inside a deme). Low CV => fitness is
equalized => deme selection is near-neutral regardless of the weighting rule.
Low within-deme dominance => demes have no stable 'type' for selection to sort.
"""
from __future__ import annotations
from statistics import mean, pstdev
from collections import Counter

from omega.experiments import exp012_combinator as M
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

prod_cv, size_cv, dom = [], [], []

_orig = M.CombinatorPhysics._deme_reproduction
def patched(self, universe, rng):
    pop = list(universe.organizations.values())
    by = {}
    for o in pop:
        p = self._patch.get(o.uid)
        if p is not None:
            by.setdefault(p, []).append(o)
    sizes = [len(v) for v in by.values() if v]
    prods = [self._deme_prod.get(p, 0) for p in by if by[p]]
    if len(sizes) > 2 and mean(sizes) > 0:
        size_cv.append(pstdev(sizes) / mean(sizes))
    if len(prods) > 2 and mean(prods) > 0:
        prod_cv.append(pstdev(prods) / mean(prods))
    # within-deme dominance: mean over demes of top-class fraction
    ds = []
    for v in by.values():
        if len(v) >= 3:
            c = Counter(o.cls for o in v)
            ds.append(c.most_common(1)[0][1] / len(v))
    if ds:
        dom.append(mean(ds))
    return _orig(self, universe, rng)

M.CombinatorPhysics._deme_reproduction = patched

physics, cfg = get_experiment('exp018')(seed=0, ticks=4000, n_patches=24)
run(physics, cfg)
print(f"between-deme SIZE  CV: mean {mean(size_cv):.3f}  (n={len(size_cv)})")
print(f"between-deme PROD  CV: mean {mean(prod_cv):.3f}  (n={len(prod_cv)})")
print(f"within-deme DOMINANCE (top-class frac): mean {mean(dom):.3f}, max {max(dom):.3f}")
print(f"  -> deme sizes ~{ 'EQUALIZED' if mean(size_cv)<0.25 else 'variable'}, "
      f"productivity ~{'EQUALIZED' if mean(prod_cv)<0.25 else 'VARIABLE'}, "
      f"within-deme type {'ABSENT (churn)' if mean(dom)<0.3 else 'present'}")
