"""exp058 — THE DIVERSITY-SEEDED START: does a richer founding tier move the STRUCTURAL bootstrapping floor?

exp057 (Ω-0.46) showed the tower's bootstrapping floor (~10–20% of seeds never establish a tier-0 network)
is *structural*, not timing-limited — a tier-0 warmup plateaus at 2× and cannot cure it — and sharpened the
follow-on: the failing seeds need a richer *starting diversity*, not a longer horizon. exp058 tests that lever
directly: `tier0_patches` runs the founding tier with more independent founder demes (default 24; higher tiers
unchanged), the diversity intervention exp057 pointed to.

This sweeps it in the derived-law tower (`builder="exp053"`, `law_from_competence=True`, the exp056/057
platform) and maps, per founder count: the tier-0 FAILURE RATE (does more founder diversity move the
structural floor?), the mean tower DEPTH, and the across-tier competence SLOPE (does a wider foundation
preserve the exp055 meta-ratchet, unlike warmup which flipped it negative?).

Verdict:
  * more founders DROP the tier-0 failure rate => the floor is a FOUNDER-DIVERSITY limit, curable with a
    richer start (the exp057 follow-on confirmed).
  * failure rate FLAT across founder count => a HARD FLOOR: some seeds are intrinsically non-networking, and
    tower robustness has a floor independent of BOTH time (exp057) AND starting diversity (exp058) — the
    ROADMAP's predicted falsification.
Run:
  PYTHONPATH=. python3 studies/exp058_diversity.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

PATCHES = [24, 48, 96]


def _slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def _run(args) -> dict:
    npatch, seed, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, builder="exp053",
                  law_from_competence=True, tier0_patches=npatch)
    return {"patches": npatch, "seed": seed, "depth": r.tower_depth,
            "competence": [t.competence for t in r.tiers]}


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 3500
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    jobs = [(p, s, max_tiers, ticks) for p in PATCHES for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for p in PATCHES:
        rs = [r for r in rows if r["patches"] == p]
        tier0_fail = mean(1.0 if r["depth"] == 0 else 0.0 for r in rs)   # bootstrapping floor
        mean_depth = mean(r["depth"] for r in rs)
        surv = [r for r in rs if len(r["competence"]) >= 2 and r["depth"] >= 2]
        slope = mean(_slope(r["competence"]) for r in surv) if surv else 0.0
        summary[p] = {"tier0_fail_rate": tier0_fail, "mean_depth": mean_depth,
                      "across_tier_slope": slope, "n_survivors": len(surv), "n": len(rs)}
    json.dump({"max_tiers": max_tiers, "ticks_per_tier": ticks, "n_seeds": n,
               "patches": PATCHES, "summary": {str(k): v for k, v in summary.items()}},
              open("studies/exp058_results.json", "w"), indent=2)

    print(f"exp058 — does a diversity-seeded founding tier move the structural floor? ({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    print(f"  {'founders':>8} {'tier0_fail':>11} {'mean_depth':>11} {'slope':>9} {'survivors':>10}")
    for p in PATCHES:
        s = summary[p]
        print(f"  {p:>8} {s['tier0_fail_rate']:>11.2f} {s['mean_depth']:>11.2f} "
              f"{s['across_tier_slope']:>+9.4f} {s['n_survivors']:>7}/{n}")
    print()

    # The founder axis need not be monotone: a MODERATE increase may reduce establishment failure without
    # cost, while a LARGE one bloats the promoted (tier-1) alphabet and dilutes higher-tier networking, so
    # depth falls. Detect the real pattern rather than only comparing the endpoints.
    base = summary[PATCHES[0]]
    mid = summary[PATCHES[len(PATCHES) // 2]]           # the moderate-diversity arm
    top = summary[PATCHES[-1]]
    best_fail = min(summary[p]["tier0_fail_rate"] for p in PATCHES)
    best_p = min(PATCHES, key=lambda p: (summary[p]["tier0_fail_rate"], -summary[p]["mean_depth"]))
    moderate_helps = (mid["tier0_fail_rate"] <= base["tier0_fail_rate"] - 0.05
                      and mid["mean_depth"] >= base["mean_depth"] - 0.2)
    over_provision_hurts = top["mean_depth"] < base["mean_depth"] - 0.3
    flat_floor = abs(best_fail - base["tier0_fail_rate"]) < 0.05 and base["tier0_fail_rate"] > 0.02
    print(f"  best founder count: {best_p} (tier0-fail {best_fail:.2f}, depth {summary[best_p]['mean_depth']:.2f})")
    print(f"  founders {PATCHES[0]} -> {PATCHES[-1]}:  tier0-fail {base['tier0_fail_rate']:.2f} -> {top['tier0_fail_rate']:.2f},  "
          f"mean-depth {base['mean_depth']:.2f} -> {top['mean_depth']:.2f},  "
          f"slope {base['across_tier_slope']:+.4f} -> {top['across_tier_slope']:+.4f}\n")
    if moderate_helps and over_provision_hurts:
        print("  => DIVERSITY HELPS, WITH AN OPTIMUM — a MODERATE founder increase reduces the tier-0 failure")
        print("     floor without a depth cost (the lever warmup could not move — exp057), but OVER-provisioning")
        print("     the foundation bloats the promoted alphabet and SHRINKS the towers (depth falls). So the")
        print("     structural floor yields to starting DIVERSITY, not time — but the foundation has an optimal")
        print("     WIDTH, mirroring exp054's optimal-richness / exp057's equal-length-tiers lesson.")
    elif moderate_helps:
        print("  => DIVERSITY HELPS — a richer founding tier reduces the tier-0 failure floor that warmup")
        print("     (exp057) could not move: the structural floor is (at least partly) a founder-diversity")
        print("     limit, curable by seeding tier 0 wider rather than running it longer.")
    elif flat_floor:
        print("  => A HARD FLOOR — the best founder count still fails to establish: some seeds are intrinsically")
        print("     non-networking, and tower robustness has a floor independent of BOTH time (exp057) AND")
        print("     starting diversity (exp058) — bounded by the substrate, not by how tier 0 is provisioned.")
    else:
        print("  => PARTIAL / NOISY — founders move the floor but not decisively (see the per-founder table);")
        print("     the failure counts are at the noise floor at this n — report the table as-is.")


if __name__ == "__main__":
    main()
