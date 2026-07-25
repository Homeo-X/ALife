"""exp068 — THE CROSS-TIER COMPETENCE RATCHET: is the tower's ~1.9 competence plateau a SATISFICING plateau
or a HARD expressivity ceiling?

exp067 (Ω-0.56) showed *transparent* promotion does not lift the across-tier competence slope — the cap is
the per-tier substrate's optimal-richness ceiling, not the promotion boundary. exp068 asks the sharp
follow-on: does a RISING TARGET, carried across the boundary, push competence up the tower? It runs the
exp053 network-visible Catalytic Law but with `deme_fitness="ratchet"` (exp042: reward = 0.05 + max(0,
competence − _ratchet_bar), the bar chasing the achieved frontier and never lowering). With
`run_stack(carry_ratchet_bar=True)` the transition SEEDS tier N+1's bar from the level tier N reached, so
each tier must EXCEED the last to score above the floor.

Arms (each an N-tier tower):
  - "ratchet_reset"  : builder="exp068"                          (bar resets per tier — the within-tier
                       ratchet at tower scale, exp042's known plateau)
  - "ratchet_carry"  : + carry_ratchet_bar=True                  (H2: seed the bar from below — differs from
                       reset ONLY by the carry)
  - "census_ref"     : builder="exp053", law_from_competence=True (the census tower — anchors the ~1.9 plateau)

Two clean outcomes: SATISFICING ⇒ ratchet_carry climbs (positive across-tier slope); HARD CEILING ⇒ no deme
clears the seeded bar, selection drifts, competence stays flat / the tower collapses. Metric: across-tier
competence SLOPE and COLLAPSE rate. Run:
  PYTHONPATH=. python3 studies/exp068_ratchet.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

ARMS = [("ratchet_reset", {"builder": "exp068"}),
        ("ratchet_carry", {"builder": "exp068", "carry_ratchet_bar": True}),
        ("census_ref", {"builder": "exp053", "law_from_competence": True})]


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
              open("studies/exp068_results.json", "w"), indent=2)

    print(f"exp068 — cross-tier competence ratchet: is the ~1.9 plateau satisficing or a hard ceiling? "
          f"({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    for arm, _kw in ARMS:
        s = summary[arm]
        print(f"  [{arm:14}] per-tier competence " +
              " ".join(f"{v:.3f}" for v in s["per_tier_competence_fulldepth"]) +
              f"  ({s['n_full']}/{n} full-depth)")
        print(f"    across-tier slope {s['within_seed_across_tier_slope']:+.4f}, "
              f"collapse {s['collapse_rate']:.2f}, mean depth {s['mean_depth']:.2f}\n")

    rr, rc = summary["ratchet_reset"], summary["ratchet_carry"]
    rr_s, rc_s = rr["within_seed_across_tier_slope"], rc["within_seed_across_tier_slope"]
    print(f"  across-tier competence slope: ratchet_reset {rr_s:+.4f}  ->  ratchet_carry {rc_s:+.4f}  "
          f"(delta {rc_s - rr_s:+.4f})")
    print(f"  collapse: reset {rr['collapse_rate']:.2f} -> carry {rc['collapse_rate']:.2f}\n")
    climbs = rc_s > 0.03 and rc_s > rr_s + 0.02 and rc["collapse_rate"] <= rr["collapse_rate"] + 0.1
    if climbs:
        print("  => SATISFICING PLATEAU: the carried rising target makes competence CLIMB across tiers where")
        print("     the reset bar plateaus — competence compounds across levels once each tier is selected to")
        print("     EXCEED the last. The ~1.9 plateau was selection relaxing, not a hard expressivity limit.")
    else:
        print("  => HARD CEILING: carrying the bar across tiers does NOT make competence climb (it stays flat")
        print("     / collapses — no deme clears the seeded bar, so selection drifts). The ~1.9 plateau is a")
        print("     hard expressivity limit of the per-tier substrate; a rising target cannot pass it. This")
        print("     tightens exp067: cross-level competence is capped by what each tier can EXPRESS, not by")
        print("     selection — the next lever is a richer per-tier law (H3), not more pressure.")


if __name__ == "__main__":
    main()
