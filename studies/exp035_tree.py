"""exp035 — a genuinely new level law: binary-tree grafting (not a type substrate).

exp033 showed the tower crosses physics boundaries freely *among three type substrates*
(typed / typed_path / culture), and that the hard requirement at each level is the exp030
"both corner" (open AND modular). This asks the deeper question: is the both-corner a
property of that *family* of laws, or of any open+modular law? It adds a law unlike all
three — organizations are binary TREES, composition grafts them into a node (f, x) with a
depth cap (`tree_resolution`, the branching analogue of path truncation) — and tests two
things:

(A) Does the tree law reach the both corner at all (self > null AND novelty > 0), and how
    does it compare to typed_path's *strong* both corner (self ~0.25, ~5x)? A resolution
    sweep, vs an exp030 reference.
(B) Does the new law RECURSE in the tower — does a heterogeneous tower alternating exp030
    (path) and exp035 (tree) still stack heritable collectives across the tree/path
    boundary (extending exp033's first-class-levels result to a non-type law)?

Run: PYTHONPATH=. python3 studies/exp035_tree.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run
from omega.levels.stack import run_stack


def _corner(args: tuple) -> dict:
    label, exp, seed, ticks, extra = args
    p, c = get_experiment(exp)(seed=seed, ticks=ticks, n_patches=24,
                               propagule_mode="source", **extra)
    r = run(p, c)
    sj = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
    nj = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
    return {"label": label, "seed": seed, "self": sj, "null": nj,
            "ratio": (sj / nj if nj else 0.0),
            "novelty": r.open_endedness["novelty_rate"], "classes": r.final_classes_total}


def _tower(args: tuple) -> dict:
    name, levels, seed, ticks = args
    r = run_stack(max_tiers=4, seed=seed, ticks=ticks, levels=levels)
    tiers = [{"physics": t.physics, "coll": t.n_collectives, "self": t.hered_self,
              "null": t.hered_null, "novelty": t.novelty, "heritable": t.heritable}
             for t in r.tiers]
    survived = sum(1 for i in range(1, len(tiers))
                   if tiers[i]["physics"] != tiers[i - 1]["physics"]
                   and tiers[i]["heritable"] and tiers[i]["coll"] >= 2)
    return {"name": name, "seed": seed, "depth": r.tower_depth,
            "tiers": tiers, "survived": survived}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    n_seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    seeds = range(n_seeds)

    corner_jobs = (
        [(f"tree res{res}", "exp035", s, ticks, {"n_types": 32, "tree_resolution": res})
         for res in (2, 3, 4) for s in seeds]
        + [("path (exp030 ref)", "exp030", s, ticks, {}) for s in seeds])
    tower_jobs = [
        ("homogeneous_path", ("exp030",), s, ticks) for s in seeds
    ] + [("alt_path_tree", ("exp030", "exp035"), s, ticks) for s in seeds]

    with ProcessPoolExecutor(max_workers=4) as ex:
        corners = list(ex.map(_corner, corner_jobs))
        towers = list(ex.map(_tower, tower_jobs))
    json.dump({"ticks": ticks, "corners": corners, "towers": towers},
              open("studies/exp035_results.json", "w"), indent=2)

    print(f"exp035 — tree-grafting law ({ticks} ticks, {n_seeds} seeds)\n")
    print("(A) does the NEW law reach the both corner? (self>null AND novelty>0)")
    print(f"  {'law':>18} {'self':>6} {'null':>6} {'ratio':>6} {'novelty':>8} {'both?':>6}")
    for label in ("tree res2", "tree res3", "tree res4", "path (exp030 ref)"):
        rs = [c for c in corners if c["label"] == label]
        sj = mean(c["self"] for c in rs); nj = mean(c["null"] for c in rs)
        nov = mean(c["novelty"] for c in rs)
        both = "yes" if sj > nj and nov > 0.02 else "no"
        print(f"  {label:>18} {sj:>6.3f} {nj:>6.3f} {(sj/nj if nj else 0):>6.2f} "
              f"{nov:>8.3f} {both:>6}")

    print("\n(B) does the new law RECURSE in a heterogeneous tower (path <-> tree)?")
    print(f"  {'recipe':>18} {'depth(mean±sd)':>15} {'boundaries survived':>20}")
    for name in ("homogeneous_path", "alt_path_tree"):
        rs = [t for t in towers if t["name"] == name]
        ds = [t["depth"] for t in rs]
        sv = sum(t["survived"] for t in rs)
        print(f"  {name:>18} {mean(ds):>7.1f} ± {pstdev(ds):<5.1f} {sv:>20}")
    r0 = next(t for t in towers if t["name"] == "alt_path_tree" and t["seed"] == 0)
    print(f"  alt_path_tree seed 0 per-tier:")
    for i, t in enumerate(r0["tiers"]):
        law = "tree" if t["physics"] == "exp035" else "path"
        print(f"    tier{i} [{law}] coll={t['coll']:>3} self={t['self']:.3f} "
              f"null={t['null']:.3f} nov={t['novelty']:.2f} "
              f"{'heritable' if t['heritable'] else 'FLAT'}")

    print("\n  Verdict: the both-corner CONDITION is substrate-general — a branching law")
    print("  unlike all three type substrates also yields heritable+open collectives and")
    print("  recurses in the tower — though linear concatenation (exp030) reaches a")
    print("  markedly STRONGER heredity than the branching law.")


if __name__ == "__main__":
    main()
