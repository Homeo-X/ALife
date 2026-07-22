"""exp057 — THE BOOTSTRAPPING FLOOR: is tower robustness timing-limited or structural?

exp056 (Ω-0.45) refuted the competence–diversity trade-off and relocated the limit on tower robustness:
~20% of seeds never establish a *tier-0* network, so the tower dies at depth 0 — "bootstrapping variance."
It left the mechanism open: is that floor *timing*-limited (a slow-to-establish tier 0 that more warmup
would cure) or *structural* (seeds whose initial configuration simply cannot form a founding network)?

`tier0_warmup` runs the FOUNDING tier (tier 0) for `int(ticks * tier0_warmup)` ticks, higher tiers
unchanged — a direct test. This sweeps it in the derived-law tower (`builder="exp053"`,
`law_from_competence=True`, the exp056 platform) and maps, per warmup: the tier-0 FAILURE RATE (fraction
of seeds that die at depth 0 — the bootstrapping floor), the mean tower DEPTH (does curing bootstrapping
unlock deeper towers?), and the across-tier competence SLOPE on survivors (does warmup preserve the exp055
meta-ratchet?).

Verdict:
  * warmup DROPS the tier-0 failure rate and RAISES mean depth => TIMING-limited — bootstrapping is slow
    establishment, curable with warmup; the deep-tower campaign is unblocked.
  * tier-0 failure rate FLAT across warmup => STRUCTURAL — the failing seeds cannot network at any horizon;
    tower robustness has an intrinsic floor that warmup does not move.
Run:
  PYTHONPATH=. python3 studies/exp057_bootstrap.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

WARMUPS = [1.0, 2.0, 4.0]


def _slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def _run(args) -> dict:
    warm, seed, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, builder="exp053",
                  law_from_competence=True, tier0_warmup=warm)
    return {"warmup": warm, "seed": seed, "depth": r.tower_depth,
            "competence": [t.competence for t in r.tiers]}


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 3500
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    jobs = [(w, s, max_tiers, ticks) for w in WARMUPS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for w in WARMUPS:
        rs = [r for r in rows if r["warmup"] == w]
        tier0_fail = mean(1.0 if r["depth"] == 0 else 0.0 for r in rs)   # bootstrapping floor
        mean_depth = mean(r["depth"] for r in rs)
        # survivors = towers that reached >= 2 tiers (a real across-level slope exists)
        surv = [r for r in rs if len(r["competence"]) >= 2 and r["depth"] >= 2]
        slope = mean(_slope(r["competence"]) for r in surv) if surv else 0.0
        summary[w] = {"tier0_fail_rate": tier0_fail, "mean_depth": mean_depth,
                      "across_tier_slope": slope, "n_survivors": len(surv), "n": len(rs)}
    json.dump({"max_tiers": max_tiers, "ticks_per_tier": ticks, "n_seeds": n,
               "warmups": WARMUPS, "summary": {str(k): v for k, v in summary.items()}},
              open("studies/exp057_results.json", "w"), indent=2)

    print(f"exp057 — is the bootstrapping floor timing-limited or structural? ({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    print(f"  {'warmup':>7} {'tier0_fail':>11} {'mean_depth':>11} {'slope':>9} {'survivors':>10}")
    for w in WARMUPS:
        s = summary[w]
        print(f"  {w:>6.1f}x {s['tier0_fail_rate']:>11.2f} {s['mean_depth']:>11.2f} "
              f"{s['across_tier_slope']:>+9.4f} {s['n_survivors']:>7}/{n}")
    print()

    base, top = summary[WARMUPS[0]], summary[WARMUPS[-1]]
    fail_drop = base["tier0_fail_rate"] - top["tier0_fail_rate"]
    depth_gain = top["mean_depth"] - base["mean_depth"]
    # monotone-ish check: failure rate non-increasing and depth non-decreasing with warmup
    fails = [summary[w]["tier0_fail_rate"] for w in WARMUPS]
    depths = [summary[w]["mean_depth"] for w in WARMUPS]
    timing = fail_drop >= 0.15 and depth_gain >= 0.3
    structural = abs(fail_drop) < 0.1 and abs(depth_gain) < 0.2
    print(f"  warmup 1.0x -> {WARMUPS[-1]:.0f}x:  tier0-fail {base['tier0_fail_rate']:.2f} -> {top['tier0_fail_rate']:.2f} "
          f"(drop {fail_drop:+.2f}),  mean-depth {base['mean_depth']:.2f} -> {top['mean_depth']:.2f} (gain {depth_gain:+.2f})\n")
    if timing:
        print("  => TIMING-LIMITED — extra tier-0 warmup DROPS the bootstrapping floor and RAISES mean")
        print("     depth: the failing seeds are slow to establish, not unable. Front-loading tier-0")
        print("     establishment cures the exp056 ~20% floor and unblocks the deep-tower campaign.")
    elif structural:
        print("  => STRUCTURAL — the tier-0 failure rate is FLAT across warmup: the failing seeds cannot")
        print("     network at any horizon. Tower robustness has an intrinsic floor that warmup does not")
        print("     move; reducing it needs a different lever (diversity-seeded start, not more time).")
    else:
        print("  => MIXED / PARTIAL — warmup moves the floor but not decisively (see the per-warmup table);")
        print("     bootstrapping is partly timing, partly structural.")


if __name__ == "__main__":
    main()
