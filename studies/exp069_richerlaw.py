"""exp069 — RICHER PER-TIER CONSTRUCTION LAW (the last lever): does changing WHAT EACH TIER CAN EXPRESS make
competence compound across levels, where carrying structure (exp067) and raising the target (exp068) failed?

exp067 (transparent promotion) and exp068 (a rising cross-tier target) both failed and *triangulated* the
limit to the per-tier construction law — the ~1.9 plateau is set by what each tier can EXPRESS. exp069
changes that: a gated `resolution_from_competence` DERIVES each tier's construction resolution from the
competence achieved below — a tier that clears `resolution_step` earns its successor a +1 deeper composition
law (`type_resolution`), capped at `resolution_cap`. This is exp054's earned-reach idea applied ACROSS the
boundary, where the added richness composes lower-tier *collectives* (a new kind — so it may escape the
within-tier depth trap that starved exp054).

Arms (each an N-tier tower on the exp053 compounding physics + law_from_competence):
  - "fixed_law"   : the census tower (fixed per-tier resolution — the saturating reference)
  - "richer_law"  : + resolution_from_competence=True (H3: a deeper construction law up the tower; differs
                    from fixed_law ONLY by the derived resolution)

Metric: across-tier competence SLOPE + collapse rate. Two clean outcomes: a richer law lets competence CLIMB
(cross-level compounding is possible), OR the deeper law re-plateaus / starves cross-production (the ~1.9
ceiling is a hard bound of this substrate — the program's decisive close). Run:
  PYTHONPATH=. python3 studies/exp069_richerlaw.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

ARMS = [("fixed_law", {"builder": "exp053", "law_from_competence": True}),
        ("richer_law", {"builder": "exp053", "law_from_competence": True,
                        "resolution_from_competence": True})]


def _run(args) -> dict:
    arm, kw, seed, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, **kw)
    return {"arm": arm, "seed": seed,
            "competence": [t.competence for t in r.tiers],
            "depth": r.tower_depth}


def _slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    jobs = [(a, kw, s, max_tiers, ticks) for (a, kw) in ARMS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for arm, _kw in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        full = [r for r in rs if len(r["competence"]) == max_tiers and r["depth"] == max_tiers]
        collapse = 1.0 - len(full) / len(rs) if rs else 1.0
        pt = [mean(r["competence"][t] for r in full) for t in range(max_tiers)] if full else [0.0] * max_tiers
        slope = mean(_slope(r["competence"]) for r in full) if full else 0.0
        summary[arm] = {"per_tier_competence_fulldepth": pt, "within_seed_across_tier_slope": slope,
                        "collapse_rate": collapse, "mean_depth": mean(r["depth"] for r in rs) if rs else 0.0,
                        "n_full": len(full)}
    json.dump({"max_tiers": max_tiers, "ticks_per_tier": ticks, "n_seeds": n, "summary": summary},
              open("studies/exp069_results.json", "w"), indent=2)

    print(f"exp069 — does a richer per-tier construction law make competence compound across levels? "
          f"({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    for arm, _kw in ARMS:
        s = summary[arm]
        print(f"  [{arm:11}] per-tier competence " +
              " ".join(f"{v:.3f}" for v in s["per_tier_competence_fulldepth"]) +
              f"  ({s['n_full']}/{n} full-depth)")
        print(f"    across-tier slope {s['within_seed_across_tier_slope']:+.4f}, "
              f"collapse {s['collapse_rate']:.2f}, mean depth {s['mean_depth']:.2f}\n")

    fx, ri = summary["fixed_law"], summary["richer_law"]
    fx_s, ri_s = fx["within_seed_across_tier_slope"], ri["within_seed_across_tier_slope"]
    print(f"  across-tier competence slope: fixed_law {fx_s:+.4f}  ->  richer_law {ri_s:+.4f}  "
          f"(delta {ri_s - fx_s:+.4f})")
    print(f"  collapse: fixed {fx['collapse_rate']:.2f} -> richer {ri['collapse_rate']:.2f}\n")
    climbs = ri_s > 0.05 and ri_s > fx_s + 0.03 and ri["collapse_rate"] <= fx["collapse_rate"] + 0.1
    if climbs:
        print("  => A RICHER PER-TIER LAW MAKES COMPETENCE COMPOUND ACROSS LEVELS: deriving each tier's")
        print("     construction resolution from the competence below turns the flat plateau into a rising")
        print("     slope — competence is a rate up the tower when each level can EXPRESS more than the last.")
    else:
        print("  => THE CEILING IS A HARD BOUND OF THE SUBSTRATE: even a richer per-tier construction law does")
        print("     not lift the across-tier slope (it re-plateaus / starves cross-production, the exp054 depth")
        print("     trap at tower scale). With exp067 (structure) and exp068 (target), all three levers fail —")
        print("     cross-level competence compounding is IMPOSSIBLE in this substrate: the world is open-ended")
        print("     in construction and individuality, but competence is a STOCK at world scale. A hard bound.")


if __name__ == "__main__":
    main()
