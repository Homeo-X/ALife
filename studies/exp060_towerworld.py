"""exp060 — THE LIVE TOWER: do levels emerge and compound competence in the PERSISTENT world regime?

exp055 (Ω-0.44) showed a competence-derived transition compounds competence *across* tower levels — in
*batch* (`run_stack`). exp059 (Ω-0.48) folded the arc into the persistent world but found competence
*plateaus* within a single tier: genuine across-time compounding needs a *new level*. exp060 closes that
gap: it runs the recursive tower **live** (`TowerWorld`, chunk-advanced, bounded memory, checkpointable),
so levels emerge over wall-clock time — and asks whether the batch across-level meta-ratchet SURVIVES the
streaming, memory-evicting regime a real world runs in.

Arms (all `builder="exp053"`, `law_from_competence=True`, derived-law tower):
  * live-bounded  — TowerWorld at a realistic memory horizon (the world regime).
  * live-unevicted — TowerWorld with no eviction (== batch run_stack; the ceiling).
Metrics per arm: mean tower DEPTH, the across-tier competence SLOPE (does competence compound across the
EMERGENT levels?), the top-tier competence, and the tier-0 bootstrapping FAILURE rate (exp057/58 — some
seeds never network; not a tower defect).

Success: live-bounded reaches deep towers with a positive across-tier slope, ≈ the un-evicted ceiling —
the meta-ratchet survives the world regime; levels genuinely emerge live. Predicted falsification: bounded
eviction STALLS the live tower (depth ≪ un-evicted, slope ≤ 0) — live open-ended level-emergence is bounded
below the batch result, a clean negative.

Run:
  PYTHONPATH=. python3 studies/exp060_towerworld.py [max_tiers] [tier_ticks] [n_seeds] [horizon]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.world.tower import TowerWorld
from omega.world.vitals import _slope

# arm -> memory_horizon (0 = no eviction). live-tight sets the horizon BELOW a tier's tick-life so
# eviction genuinely bites within every tier — the real stress test of the streaming world regime.
ARMS = {"live-tight": 1200, "live-bounded": 20000, "live-unevicted": 0}


def _run(args) -> dict:
    arm, mh, seed, max_tiers, tier_ticks = args
    tw = TowerWorld(builder="exp053", seed=seed, tier_ticks=tier_ticks, max_tiers=max_tiers,
                    law_from_competence=True, memory_horizon=mh,
                    relation_cap=(80000 if mh else 0))
    budget = max_tiers * tier_ticks + tier_ticks         # a little slack past the last tier
    while not tw.done and tw.total_ticks < budget:
        tw.step(tier_ticks // 2)
    comps = [t.competence for t in tw.tiers if t.heritable and t.n_collectives >= 2]
    tier0_fail = 1.0 if (not tw.tiers or tw.tiers[0].competence == 0.0
                         or tw.tiers[0].n_collectives < 2) else 0.0
    return {"arm": arm, "seed": seed, "depth": tw.tower_depth,
            "slope": _slope(list(enumerate(comps))) if len(comps) >= 2 else 0.0,
            "top": comps[-1] if comps else 0.0, "tier0_fail": tier0_fail}


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    tier_ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    jobs = [(a, mh, s, max_tiers, tier_ticks) for a, mh in ARMS.items() for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a]
        surv = [r for r in rs if r["tier0_fail"] == 0.0]           # seeds that established tier 0
        summary[a] = {
            "mean_depth": mean(r["depth"] for r in rs),
            "across_tier_slope": mean(r["slope"] for r in surv) if surv else 0.0,
            "top_competence": mean(r["top"] for r in surv) if surv else 0.0,
            "tier0_fail_rate": mean(r["tier0_fail"] for r in rs),
            "n_survivors": len(surv), "n": len(rs)}
    json.dump({"max_tiers": max_tiers, "tier_ticks": tier_ticks, "n_seeds": n,
               "summary": summary}, open("studies/exp060_results.json", "w"), indent=2)

    print(f"exp060 — the live tower: do levels emerge & compound competence in the persistent regime? "
          f"({max_tiers} tiers, {tier_ticks} ticks/tier, {n} seeds)\n")
    print(f"  {'arm':>15} {'mean_depth':>11} {'across_slope':>13} {'top_comp':>9} {'tier0_fail':>11} {'survivors':>10}")
    for a in ARMS:
        s = summary[a]
        print(f"  {a:>15} {s['mean_depth']:>11.2f} {s['across_tier_slope']:>+13.4f} {s['top_competence']:>9.3f} "
              f"{s['tier0_fail_rate']:>11.2f} {s['n_survivors']:>7}/{s['n']}")
    print()

    # the real eviction test: live-TIGHT (horizon < tier life, eviction bites) vs the un-evicted ceiling.
    lb, lu = summary["live-tight"], summary["live-unevicted"]
    depth_ratio = lb["mean_depth"] / lu["mean_depth"] if lu["mean_depth"] else 0.0
    survives = lb["mean_depth"] >= 0.8 * lu["mean_depth"] and lb["across_tier_slope"] > 0.0
    print(f"  live-TIGHT (evicting) vs un-evicted ceiling: depth {lb['mean_depth']:.2f} vs {lu['mean_depth']:.2f} "
          f"(ratio {depth_ratio:.2f}), across-tier slope {lb['across_tier_slope']:+.4f} vs {lu['across_tier_slope']:+.4f}\n")
    if survives:
        print("  => THE META-RATCHET SURVIVES THE WORLD REGIME — the live, bounded-memory tower grows levels")
        print("     over wall-clock time to ~the un-evicted depth, with competence rising across the EMERGENT")
        print("     levels. Higher-order life forms live; the exp055 across-level compounding is not a batch")
        print("     artifact. (The residual tier-0 failure rate is the exp057/58 bootstrapping floor, not a")
        print("     tower defect.)")
    else:
        print("  => BOUNDED EVICTION STALLS THE LIVE TOWER — depth / across-tier slope fall well short of the")
        print("     un-evicted ceiling: live open-ended level-emergence is bounded below the batch result in")
        print("     the streaming regime. A real negative; report the per-arm table as-is.")


if __name__ == "__main__":
    main()
