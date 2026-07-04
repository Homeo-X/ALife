"""Ecology metrics — structure in the cross-production graph.

Once a soup contains many coexisting replicators, the question is whether they
merely coexist or actually *interact* in structured ways. The interaction network
is the **cross-production graph**: a directed edge i → j means "class i (as a
function) produced class j". Read off it:

* **Mutualism / hypercycles** — reciprocated edges (i → j and j → i) and longer
  cycles: organizations that help build each other. Measured as graph
  *reciprocity*, tested against a degree-preserving null (a random graph with the
  same in/out-degree sequences), because some reciprocity is expected by chance and
  only an excess over the null is real structure.

* **Parasitism** — classes that are *produced* a lot but *produce* little, and are
  *small* (cheap to copy): freeloaders that consume reservoir without contributing.

These are deliberately null-tested: an ecological claim must beat the graph's own
degree distribution, not just be nonzero.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev

from omega.substrate.noise import Noise


def build_edges(cross: dict, min_weight: int = 5, exclude_self: bool = True) -> dict:
    """Significant directed edges (i→j) with their weights."""
    return {(i, j): w for (i, j), w in cross.items()
            if w >= min_weight and (i != j if exclude_self else True)}


def reciprocity(edges: dict) -> float:
    keys = set(edges)
    directed = [k for k in keys if k[0] != k[1]]
    if not directed:
        return 0.0
    recp = sum(1 for (i, j) in directed if (j, i) in keys)
    return recp / len(directed)


def _null_reciprocity(edges: dict, rng: Noise, trials: int = 200) -> tuple[float, float]:
    """Reciprocity of degree-preserving random rewirings (configuration model)."""
    srcs = [i for (i, j) in edges]
    dsts = [j for (i, j) in edges]
    vals = []
    for _ in range(trials):
        shuffled = list(dsts)
        rng.shuffle(shuffled)
        rewired = set(zip(srcs, shuffled))
        directed = [k for k in rewired if k[0] != k[1]]
        if directed:
            vals.append(sum(1 for (i, j) in directed if (j, i) in rewired) / len(directed))
    if not vals:
        return 0.0, 0.0
    return fmean(vals), (pstdev(vals) if len(vals) > 1 else 0.0)


@dataclass
class EcologyReport:
    n_nodes: int
    n_edges: int
    reciprocity: float
    null_reciprocity: float
    null_std: float
    reciprocity_z: float          # (obs - null) / null_std : excess mutualism
    n_mutual_pairs: int
    n_parasites: int
    top_parasites: list           # (class, produced, produces, size)

    def summary(self) -> str:
        return (
            f"nodes={self.n_nodes} edges={self.n_edges} "
            f"reciprocity={self.reciprocity:.3f} (null {self.null_reciprocity:.3f}"
            f"±{self.null_std:.3f}, z={self.reciprocity_z:+.1f}) "
            f"mutual_pairs={self.n_mutual_pairs} parasites={self.n_parasites}"
        )


def analyze(cross: dict, produces: dict, produced: dict, size_of: dict,
            seed: int = 0, min_weight: int = 5,
            parasite_ratio: float = 4.0, parasite_max_size: int = 4) -> EcologyReport:
    edges = build_edges(cross, min_weight=min_weight, exclude_self=True)
    nodes = {n for e in edges for n in e}
    obs = reciprocity(edges)
    null_m, null_s = _null_reciprocity(edges, Noise(seed))
    z = (obs - null_m) / null_s if null_s > 1e-9 else 0.0
    mutual = sum(1 for (i, j) in edges if i < j and (j, i) in edges)

    # parasites: produced >> produces, and small
    parasites = []
    for cls, pin in produced.items():
        pout = produces.get(cls, 0)
        sz = size_of.get(cls, 99)
        if pin >= parasite_ratio * (pout + 1) and sz <= parasite_max_size and pin >= min_weight:
            parasites.append((cls, pin, pout, sz))
    parasites.sort(key=lambda t: -t[1])

    return EcologyReport(
        n_nodes=len(nodes), n_edges=len(edges),
        reciprocity=obs, null_reciprocity=null_m, null_std=null_s, reciprocity_z=z,
        n_mutual_pairs=mutual, n_parasites=len(parasites), top_parasites=parasites[:8],
    )
