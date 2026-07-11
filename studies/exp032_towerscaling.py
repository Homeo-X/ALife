"""exp032 Part B — tower-depth scaling: does the recursive tower keep climbing?

exp031 reached depth 4–5 at 2500 ticks/tier with max_tiers=5. But max_tiers=5 *caps* the
observable depth — it can't distinguish "the tower stops at 5" from "the tower would climb
further if allowed". This lifts the cap and asks the sharper question: is depth bounded by
an **intrinsic ceiling** or only by **compute**?

The structural crux (the primary test): each tier's alphabet = the previous tier's count
of stable heritable collectives. If that count is a rough **fixed point** (~20 in exp031,
independent of tier), the alphabet self-sustains and depth is compute-limited, not
ceiling-limited. If it **shrinks** each tier, the alphabet starves and the tower has a real
depth ceiling. So the primary study is a DEEP tower (max_tiers=15) read tier-by-tier:
does per-tier collective-count / heredity / novelty hold up, or decay with depth?

Secondary: a base-alphabet sweep (base_n_types ∈ {16,32,64}) at max_tiers=8 — does deeper
resource (a bigger base) buy more depth, or does depth saturate regardless of base?

Run: PYTHONPATH=. python3 studies/exp032_towerscaling.py [ticks] [deep_seeds] [sweep_seeds]
  defaults: 2500 ticks/tier, 2 deep-tower seeds (max_tiers=15), 3 sweep seeds.
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.levels.stack import run_stack, LEVEL_NAMES

DEEP_MAX = 15
SWEEP_BASES = (16, 32, 64)
SWEEP_MAX = 8


def _tower(args: tuple) -> dict:
    tag, seed, base, max_tiers, ticks = args
    r = run_stack(max_tiers=max_tiers, seed=seed, ticks=ticks, base_n_types=base)
    return {"tag": tag, "seed": seed, "base": base, "depth": r.tower_depth,
            "tiers": [{"tier": t.tier, "alphabet": t.alphabet_size,
                       "collectives": t.n_collectives, "self": t.hered_self,
                       "null": t.hered_null, "novelty": t.novelty,
                       "heritable": t.heritable} for t in r.tiers]}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 2500
    deep_seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    sweep_seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    deep_jobs = [("deep", s, 32, DEEP_MAX, ticks) for s in range(deep_seeds)]
    sweep_jobs = [("sweep", s, b, SWEEP_MAX, ticks)
                  for b in SWEEP_BASES for s in range(sweep_seeds)]
    with ProcessPoolExecutor(max_workers=8) as ex:
        deep = list(ex.map(_tower, deep_jobs))
        sweep = list(ex.map(_tower, sweep_jobs))

    json.dump({"ticks": ticks, "deep": deep, "sweep": sweep},
              open("studies/exp032_towerscaling_results.json", "w"), indent=2)

    print(f"exp032 Part B — tower-depth scaling ({ticks} ticks/tier)\n")

    # --- primary: the DEEP tower, tier by tier ---
    print(f"(1) DEEP tower — max_tiers={DEEP_MAX}, base=32, {deep_seeds} seeds "
          f"(is depth compute- or ceiling-limited?)")
    depths = [d["depth"] for d in deep]
    print(f"  tower depth: mean {mean(depths):.1f} ± {pstdev(depths):.1f}, "
          f"max {max(depths)}, per-seed {depths}")
    maxlen = max(len(d["tiers"]) for d in deep)
    print(f"  {'tier':>4} {'level':>13} {'alphabet':>8} {'collectives':>11} "
          f"{'self':>6} {'null':>6} {'novelty':>7} {'heritable':>10}")
    for i in range(maxlen):
        rows = [d["tiers"][i] for d in deep if i < len(d["tiers"])]
        lvl = LEVEL_NAMES[min(i, len(LEVEL_NAMES) - 1)] if i < len(LEVEL_NAMES) else f"L{i}"
        print(f"  {i:>4} {lvl:>13} {mean(r['alphabet'] for r in rows):>8.0f} "
              f"{mean(r['collectives'] for r in rows):>11.1f} "
              f"{mean(r['self'] for r in rows):>6.3f} {mean(r['null'] for r in rows):>6.3f} "
              f"{mean(r['novelty'] for r in rows):>7.2f} "
              f"{sum(r['heritable'] for r in rows)}/{len(rows):>d}")
    # is the alphabet a fixed point (self-sustaining) or shrinking (starving)?
    per_tier_coll = [mean(d["tiers"][i]["collectives"] for d in deep if i < len(d["tiers"]))
                     for i in range(maxlen)]
    if len(per_tier_coll) >= 3:
        early = mean(per_tier_coll[1:3]); late = mean(per_tier_coll[-2:])
        trend = "self-sustaining (~fixed point)" if late >= 0.75 * early else "starving (shrinks)"
        print(f"  alphabet trend: tier1-2 collectives ~{early:.1f} -> deepest ~{late:.1f} "
              f"=> {trend}")

    # --- secondary: does base size buy depth? ---
    print(f"\n(2) base-alphabet sweep — max_tiers={SWEEP_MAX}, {sweep_seeds} seeds/base")
    print(f"  {'base':>5} {'depth(mean±sd)':>16} {'max':>4} {'tier0 collectives':>18}")
    for b in SWEEP_BASES:
        rs = [d for d in sweep if d["base"] == b]
        ds = [r["depth"] for r in rs]
        t0 = mean(r["tiers"][0]["collectives"] for r in rs)
        print(f"  {b:>5} {mean(ds):>8.1f} ± {pstdev(ds):<5.1f} {max(ds):>4} {t0:>18.1f}")
    bases_depth = [mean(r["depth"] for r in sweep if r["base"] == b) for b in SWEEP_BASES]
    grows = bases_depth[-1] > bases_depth[0] + 0.5
    print(f"  depth vs base: {dict(zip(SWEEP_BASES, [round(x,1) for x in bases_depth]))} "
          f"=> {'grows with base' if grows else 'saturates (base-independent)'}")


if __name__ == "__main__":
    main()
