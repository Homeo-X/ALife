"""exp056 — THE COMPETENCE–DIVERSITY TRADE-OFF: is it navigable, or a strict Pareto frontier?

exp055 (Ω-0.44) showed a competence-derived transition compounds competence ACROSS tower levels, but
competence selection thins the collective diversity the transition needs, collapsing ~⅓ of towers. Is
that trade-off fundamental — every regime that compounds competence also collapses the tower — or is
there a sweet spot with BOTH a rising across-level competence AND deep, robust towers?

`competence_pressure` ∈ [0,1] dials the strength of the Red Queen's competence selection (weight = 0.05 +
pressure·(closure + core-novelty)): 1.0 = full selection (exp055), 0.0 = uniform drift (maximal diversity,
no competence selection). This sweeps it in the derived-law tower and maps, per pressure: the across-tier
competence SLOPE (does competence still compound?), the COLLAPSE RATE (tower robustness / diversity), and
the top-tier competence LEVEL.

Verdict:
  * a pressure with slope > 0 AND collapse ≈ 0  => NAVIGABLE — the trade-off has a sweet spot.
  * every pressure with slope > 0 also has high collapse (monotone frontier) => FUNDAMENTAL trade-off.
Run:
  PYTHONPATH=. python3 studies/exp056_tradeoff.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

PRESSURES = [1.0, 0.66, 0.33, 0.0]


def _slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def _run(args) -> dict:
    press, seed, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, builder="exp053",
                  law_from_competence=True, competence_pressure=press)
    return {"pressure": press, "seed": seed, "depth": r.tower_depth,
            "competence": [t.competence for t in r.tiers],
            "collectives": [t.n_collectives for t in r.tiers]}


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    jobs = [(p, s, max_tiers, ticks) for p in PRESSURES for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for p in PRESSURES:
        rs = [r for r in rows if r["pressure"] == p]
        full = [r for r in rs if len(r["competence"]) == max_tiers and r["depth"] == max_tiers]
        collapse = 1.0 - len(full) / len(rs)
        pt = [mean(r["competence"][t] for r in full) for t in range(max_tiers)] if full else [0.0] * max_tiers
        slope = mean(_slope(r["competence"]) for r in full) if full else 0.0
        # diversity fuel: mean stable collectives produced by tier 0 (what seeds tier 1), over ALL seeds —
        # the quantity the transition needs >= 2 of. A more sensitive diversity signal than binary collapse.
        div0 = mean(r["collectives"][0] if r["collectives"] else 0 for r in rs)
        summary[p] = {"collapse_rate": collapse, "across_tier_slope": slope,
                      "top_tier_competence": pt[-1], "per_tier_competence": pt,
                      "tier0_diversity": div0,
                      "mean_depth": mean(r["depth"] for r in rs), "n_full": len(full)}
    json.dump({"max_tiers": max_tiers, "ticks_per_tier": ticks, "n_seeds": n,
               "pressures": PRESSURES, "summary": {str(k): v for k, v in summary.items()}},
              open("studies/exp056_results.json", "w"), indent=2)

    print(f"exp056 — is the competence–diversity trade-off navigable? ({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    print(f"  {'pressure':>9} {'slope':>8} {'collapse':>9} {'tier0_div':>10} {'top-tier':>9} {'depth':>7} {'full':>6}")
    for p in PRESSURES:
        s = summary[p]
        print(f"  {p:>9.2f} {s['across_tier_slope']:>+8.4f} {s['collapse_rate']:>9.2f} "
              f"{s['tier0_diversity']:>10.1f} {s['top_tier_competence']:>9.3f} {s['mean_depth']:>7.2f} {s['n_full']:>4}/{n}")
    print()

    # a sweet spot: some pressure compounds competence across levels (slope > 0.02) with LOW collapse (<0.15).
    sweet = [p for p in PRESSURES if summary[p]["across_tier_slope"] > 0.02
             and summary[p]["collapse_rate"] < 0.15 and summary[p]["n_full"] >= max(2, n // 2)]
    # is it monotone (every compounding pressure collapses)?
    compounders = [p for p in PRESSURES if summary[p]["across_tier_slope"] > 0.02]
    if sweet:
        best = max(sweet, key=lambda p: summary[p]["across_tier_slope"])
        print(f"  => NAVIGABLE: pressure={best} compounds competence across levels "
              f"(slope {summary[best]['across_tier_slope']:+.4f}) with LOW collapse "
              f"({summary[best]['collapse_rate']:.2f}) — the competence–diversity trade-off has a SWEET SPOT.")
        print("     Softening competence selection preserves the collective diversity the transition needs,")
        print("     while still deriving a compounding law from it. Competence AND open-ended depth together.")
    elif compounders:
        print("  => A STRICT TRADE-OFF (fundamental, within this substrate): every pressure that compounds")
        print("     competence across levels also collapses towers; softening selection preserves depth but")
        print("     flattens the across-level slope. Competence and open-ended recursion cannot both be")
        print("     maximized — a Pareto frontier, not a sweet spot. The exp047/055 tension is intrinsic.")
    else:
        print("  => NO ACROSS-LEVEL COMPOUNDING AT ANY PRESSURE (a deeper negative): none of the swept")
        print("     pressures produce a rising across-level slope on robust towers.")


if __name__ == "__main__":
    main()
