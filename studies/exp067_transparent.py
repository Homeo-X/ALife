"""exp067 — TRANSPARENT CROSS-TIER REIFICATION: does carrying competent structure across the tower boundary
make competence COMPOUND across levels, where the census (Ω-0.50) found it saturates?

The census settled that per-tier competence is a flat ~1.85 plateau across up to 16 emergent tower levels —
because promotion drops each collective at an *opaque* atom (`L{n}_{i}`) and carries only a scalar law
strength, re-introducing the exp049 opacity at the tower boundary (each higher tier re-bootstraps from
scratch). exp067 makes promotion **transparent**: the finishing tier's learned catalytic repertoire
(network-visible anchor→product reactions) is carried into the next tier, and the child is seeded with the
parent collectives' product states so those reactions keep firing — the exp053 "keep competent structure
network-visible" fix applied *across* the boundary, so competence can build on competence.

Arms (each an N-tier tower on the exp053 compounding physics):
  - "compounding"  : builder="exp053"                              (fixed law, opaque promotion — baseline)
  - "law_only"     : + law_from_competence=True                    (exp055's scalar lift — the census tower)
  - "transparent"  : + law_from_competence=True, carry_catalysts=True   (H1: carry the competent structure)

`transparent` differs from `law_only` ONLY by `carry_catalysts`, isolating transparent reification. Metric:
per-tier mean COMPETENCE and the within-seed across-tier competence SLOPE on full-depth towers. Prediction:
`transparent` slope > `law_only` (≈ 0, the plateau). Falsification: `transparent` also re-plateaus ⇒ the
ceiling is intrinsic to the per-tier substrate (a clean negative bounding cross-level competence). Run:
  PYTHONPATH=. python3 studies/exp067_transparent.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

ARMS = [("compounding", {"builder": "exp053"}),
        ("law_only", {"builder": "exp053", "law_from_competence": True}),
        ("transparent", {"builder": "exp053", "law_from_competence": True, "carry_catalysts": True})]


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
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    jobs = [(a, kw, s, max_tiers, ticks) for (a, kw) in ARMS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    # Metrics on FULL-DEPTH towers only (a rise must not be an artifact of averaging the top tier over just
    # the seeds that survived to it): per-tier competence, within-seed across-tier slope, collapse rate.
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
              open("studies/exp067_results.json", "w"), indent=2)

    print(f"exp067 — does TRANSPARENT cross-tier reification make competence compound across levels? "
          f"({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    for arm, _kw in ARMS:
        s = summary[arm]
        print(f"  [{arm:12}] per-tier competence " +
              " ".join(f"{v:.3f}" for v in s["per_tier_competence_fulldepth"]) +
              f"  ({s['n_full']}/{n} full-depth)")
        print(f"    across-tier slope {s['within_seed_across_tier_slope']:+.4f}, "
              f"collapse {s['collapse_rate']:.2f}, mean depth {s['mean_depth']:.2f}\n")

    lo, tr = summary["law_only"], summary["transparent"]
    lo_s, tr_s = lo["within_seed_across_tier_slope"], tr["within_seed_across_tier_slope"]
    print(f"  across-tier competence slope: law_only {lo_s:+.4f}  ->  transparent {tr_s:+.4f}  "
          f"(delta {tr_s - lo_s:+.4f})\n")
    compounds = tr_s > 0.03 and tr_s > lo_s + 0.02 and tr["collapse_rate"] <= lo["collapse_rate"] + 0.1
    if compounds:
        print("  => TRANSPARENT REIFICATION MAKES COMPETENCE COMPOUND ACROSS LEVELS: carrying the tier's")
        print("     network-visible competent repertoire across the boundary turns the flat across-tier")
        print("     plateau (law_only, the census tower) into a rising slope — the exp053 fix works one level")
        print("     up. Competence is a rate up the tower when the boundary is transparent, not opaque.")
    else:
        print("  => NO CROSS-LEVEL COMPOUNDING: transparent carry-over does not lift the across-tier slope")
        print("     above the opaque tower — the competence ceiling is intrinsic to the per-tier substrate")
        print("     (a clean negative bounding cross-level competence; the next lever is a rising target / H2).")


if __name__ == "__main__":
    main()
