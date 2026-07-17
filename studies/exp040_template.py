"""exp040 — breaking the collective-heredity ceiling with developmental (network-template) inheritance.

exp039 located the blocker between Ω collectives and self-improvement: collective heredity is too
weak (the exp028 ceiling ~3-5x null; self ~0.08-0.28), because a deme's cross-production network is a
dynamical attractor that offspring do not re-form from inherited *members* alone. This transmits the
developmental *niche* too: a fraction (`network_template` ∈ [0,1]) of the parent network's product
states is seeded into the child's recycle buffer, so it is re-fed the parent's outputs and canalizes
toward the parent's edges.

The sweep is the collective-level analogue of exp030's resolution dial:
  strength 0   = off (the ceiling: open but weak heredity, byte-identical to exp028-style transmission)
  strength 1   = full pinning (strong heredity but the world CLOSES, novelty -> 0)
  intermediate = the collective BOTH CORNER (strong heredity AND sustained novelty)

Metric (ratio + rate): collective heredity self vs null (`_hered_edge_self`/`_hered_edge_null`) and
the novelty rate, vs template strength, multi-seed. Run:
  PYTHONPATH=. python3 studies/exp040_template.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

STRENGTHS = [0.0, 0.25, 0.5, 0.75, 1.0]


def _run(args) -> dict:
    strength, seed, ticks = args
    p, c = get_experiment("exp040")(seed=seed, ticks=ticks, network_template=strength)
    r = run(p, c)
    return {"strength": strength, "seed": seed,
            "self": mean(p._hered_edge_self) if p._hered_edge_self else 0.0,
            "null": mean(p._hered_edge_null) if p._hered_edge_null else 0.0,
            "novelty": r.open_endedness["novelty_rate"]}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    jobs = [(st, s, ticks) for st in STRENGTHS for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n, "rows": rows},
              open("studies/exp040_results.json", "w"), indent=2)

    print(f"exp040 — developmental network-template inheritance vs the heredity ceiling "
          f"({ticks} ticks, {n} seeds)")
    print(f"  the exp028 ceiling is ~3-5x null / self ~0.1-0.28\n")
    print(f"  {'template':>9} {'heredity self':>14} {'null':>7} {'ratio':>7} {'novelty':>8}  corner")
    agg = {}
    for st in STRENGTHS:
        rs = [r for r in rows if r["strength"] == st]
        s = mean(r["self"] for r in rs); nl = mean(r["null"] for r in rs)
        v = mean(r["novelty"] for r in rs)
        agg[st] = (s, nl, v)
        corner = ("BOTH (heredity✔ open✔)" if s > 0.3 and v > 0.05
                  else "closed" if v <= 0.02 else "open, weak heredity" if s < 0.25 else "")
        print(f"  {st:>9} {s:>14.3f} {nl:>7.3f} {(s/nl if nl else 0):>6.1f}x {v:>8.3f}  {corner}")

    off_s, _, off_v = agg[0.0]
    both = [st for st in STRENGTHS if 0 < st < 1 and agg[st][0] > 0.3 and agg[st][2] > 0.05]
    print()
    if both:
        st = both[0]; s, nl, v = agg[st]
        print(f"  => CEILING BROKEN at the both corner: strength {st} gives self {s:.3f} "
              f"({s/off_s:.1f}x the off baseline {off_s:.3f}) AND novelty {v:.3f} > 0.")
        print("     A PARTIAL developmental template breaks collective heredity past the exp028")
        print("     ceiling while keeping the world open — the exp030 'both corner' logic (modular,")
        print("     partial transmission) re-derived one level up. Full pinning (1.0) closes it.")
    else:
        print("  => no both corner found — template either fails to lift heredity or always closes.")


if __name__ == "__main__":
    main()
