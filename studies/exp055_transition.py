"""exp055 — TRANSITION-AS-RULE-CHANGE: does competence compound ACROSS levels of the tower?

exp053 (Ω-0.42) made competence a RATE *within* a level — the Catalytic Law (promote a competent deme's
closure loop to a shared, network-visible reaction). exp054 (Ω-0.43) showed expanding the law along
construction *depth* fails (deeper paths starve cross-production); the richness has to be a NEW KIND. The
level tower is exactly that: each tier composes the tier-below's *collectives* as its atoms (a genuinely
new level), so it avoids the depth trap. exp055 runs the compounding law at every tier and asks the user's
#1 question — do "major transitions as rule-changes" make competence rise ACROSS levels?

Arms (each a 3-tier tower):
  - "self-similar" : builder="exp030"  (the current tower — fixed both-corner law, no compounding).
  - "compounding"  : builder="exp053"  (the Catalytic-Law + Red-Queen compounding physics at every tier,
                     fixed catalyst_period — does the compounding law alone lift competence up the tower?).
  - "derived-law"  : builder="exp053", law_from_competence=True (the TRANSITION grants the next tier a
                     law strength derived from THIS tier's competence: period = base/(1+competence) —
                     does deriving the law from achieved competence add beyond the fixed compounding law?).

Metric: per-tier mean COMPETENCE (does it rise across tiers?), tower DEPTH, and the competence SLOPE
across tiers. Multi-seed. Run:
  PYTHONPATH=. python3 studies/exp055_transition.py [max_tiers] [ticks_per_tier] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.levels.stack import run_stack

ARMS = [("self-similar", {"builder": "exp030"}),
        ("compounding", {"builder": "exp053"}),
        ("derived-law", {"builder": "exp053", "law_from_competence": True})]


def _run(args) -> dict:
    arm, kw, seed, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, **kw)
    return {"arm": arm, "seed": seed,
            "competence": [t.competence for t in r.tiers],
            "depth": r.tower_depth,
            "periods": [t.catalyst_period for t in r.tiers]}


def _slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    max_tiers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    jobs = [(a, kw, s, max_tiers, ticks) for (a, kw) in ARMS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    def per_tier(arm):
        rs = [r for r in rows if r["arm"] == arm]
        # average competence per tier across seeds that reached that tier
        out = []
        for tier in range(max_tiers):
            vals = [r["competence"][tier] for r in rs if len(r["competence"]) > tier]
            out.append(mean(vals) if vals else 0.0)
        return out

    summary = {}
    for arm, _kw in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        pt = per_tier(arm)
        summary[arm] = {"per_tier_competence": pt,
                        "mean_depth": mean(r["depth"] for r in rs),
                        "across_tier_slope": _slope(pt)}
    json.dump({"max_tiers": max_tiers, "ticks_per_tier": ticks, "n_seeds": n, "summary": summary},
              open("studies/exp055_results.json", "w"), indent=2)

    print(f"exp055 — does competence compound ACROSS levels? ({max_tiers} tiers, {ticks} ticks/tier, {n} seeds)\n")
    for arm, _kw in ARMS:
        s = summary[arm]
        print(f"  [{arm}]  per-tier competence " + " ".join(f"{v:.3f}" for v in s["per_tier_competence"]))
        print(f"    across-tier slope {s['across_tier_slope']:+.4f}, mean tower depth {s['mean_depth']:.2f}\n")

    ss, co, dv = (summary[a]["across_tier_slope"] for a in ("self-similar", "compounding", "derived-law"))
    ssm = summary["self-similar"]["per_tier_competence"]
    com = summary["compounding"]["per_tier_competence"]
    dvm = summary["derived-law"]["per_tier_competence"]
    print(f"  across-tier competence slope: self-similar {ss:+.4f} | compounding {co:+.4f} | derived-law {dv:+.4f}")
    print(f"  top-tier competence: self-similar {ssm[-1]:.3f} | compounding {com[-1]:.3f} | derived-law {dvm[-1]:.3f}\n")

    compounds_up = co > 0.01 and mean(com) > mean(ssm)
    derived_adds = dv > co + 0.005 or dvm[-1] > com[-1] + 0.05
    if compounds_up and derived_adds:
        print("  => COMPETENCE COMPOUNDS ACROSS LEVELS, AND THE RULE-CHANGE ADDS: running the compounding")
        print("     law at each tier makes competence RISE up the tower (a meta-ratchet), and DERIVING the")
        print("     higher law from the lower level's competence beats the fixed compounding law — major")
        print("     transitions as rule-changes compound competence across levels (the user's #1).")
    elif compounds_up:
        print("  => COMPETENCE COMPOUNDS ACROSS LEVELS (the compounding law lifts competence up the tower,")
        print("     well above the self-similar tower), but DERIVING the law from competence does not clearly")
        print("     beat the fixed compounding law — the level transition (a new KIND of richness) is what")
        print("     matters, not the specific competence-derivation. A meta-ratchet either way.")
    else:
        print("  => NO ACROSS-LEVEL COMPOUNDING (honest negative): competence does not rise up the tower even")
        print("     with the compounding law per tier — the transition adds a new kind of richness but")
        print("     competence stays level-bounded. The ratchet is within-level only.")


if __name__ == "__main__":
    main()
