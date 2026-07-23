"""exp061 — THE WORLD CENSUS: does the living world stay alive, open, and competent at the long horizon,
and how deep does the live tower climb? (Ω-0.50)

Phases A (Ω-0.48) and B (Ω-0.49) built a living world that embodies the arc and grows a tower of levels
live, and showed the tower is eviction-invariant (so an indefinite run is feasible). exp061 gathers the
rich, long-horizon dataset that settles what happens *at scale*:

  Part A — living_world VITAL-SIGNS TIME SERIES over a long horizon (bounded memory): does competence stay
    elevated, does the genuine (eviction-robust) novelty rate hold a positive floor, do self-maintaining
    lifeforms persist — or does any of it decay?
  Part B — the DEEP TOWER profile: pushing many tiers, how deep does the live tower actually climb, and
    does competence keep compounding across the emergent levels or hit a ceiling?

Emits a machine-readable census (`studies/exp061_census.json`) and a self-contained, shareable HTML report
(`studies/exp061_census.html`, inline SVG, no dependencies).

Predicted falsifications: (A) at length the genuine-novelty floor dilutes to ~0 or competence collapses —
the living world does not sustain OEE/life at scale; (B) tower depth hits a hard ceiling well below the
tiers attempted — level-emergence is intrinsically bounded.

Run:
  PYTHONPATH=. python3 studies/exp061_census.py [horizon] [stride] [n_seeds] [max_tiers] [tier_ticks]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.world.runtime import World
from omega.world.vitals import WorldVitals, _slope
from omega.world.tower import TowerWorld


def _living(args) -> dict:
    seed, horizon, stride = args
    w = World.create("living_world", seed=seed, genuine_novelty=True)
    v = WorldVitals(window=horizon // stride + 2)
    series = []
    for _ in range(horizon // stride):
        w.step(stride)
        s = v.sample(w)
        series.append({"tick": s["tick"], "competence": round(s["competence"], 4),
                       "closure": round(s["closure"], 4), "lifeforms": s["lifeforms"],
                       "genuine_rate": round(s["genuine_novelty_rate"], 4),
                       "genuine_distinct": s["genuine_distinct"], "diversity": round(s["diversity"], 4)})
    return {"seed": seed, "series": series}


def _tower(args) -> dict:
    seed, max_tiers, tier_ticks = args
    tw = TowerWorld(builder="exp053", seed=seed, tier_ticks=tier_ticks, max_tiers=max_tiers,
                    law_from_competence=True, memory_horizon=20000)
    budget = max_tiers * tier_ticks + tier_ticks
    while not tw.done and tw.total_ticks < budget:
        tw.step(tier_ticks // 2)
    return {"seed": seed, "depth": tw.tower_depth,
            "per_tier": [round(t.competence, 4) for t in tw.tiers]}


def _avg_series(runs: list, keys) -> list:
    """Average the per-seed time series stride-by-stride (aligned by index)."""
    if not runs:
        return []
    n = min(len(r["series"]) for r in runs)
    out = []
    for i in range(n):
        row = {"tick": runs[0]["series"][i]["tick"]}
        for k in keys:
            row[k] = round(mean(r["series"][i][k] for r in runs), 4)
        out.append(row)
    return out


def main() -> None:
    horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    stride = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    max_tiers = int(sys.argv[4]) if len(sys.argv) > 4 else 15
    tier_ticks = int(sys.argv[5]) if len(sys.argv) > 5 else 2500

    with ProcessPoolExecutor(max_workers=4) as ex:
        living = list(ex.map(_living, [(s, horizon, stride) for s in range(n)]))
        towers = list(ex.map(_tower, [(s, max_tiers, tier_ticks) for s in range(n)]))

    keys = ("competence", "closure", "lifeforms", "genuine_rate", "genuine_distinct", "diversity")
    avg = _avg_series(living, keys)
    # depth profile: fraction of seeds reaching each depth; per-tier competence averaged over reachers
    depths = [t["depth"] for t in towers]
    max_reached = max(depths) if depths else 0
    per_tier = []
    for k in range(max(max_reached, max((len(t["per_tier"]) for t in towers), default=0))):
        vals = [t["per_tier"][k] for t in towers if len(t["per_tier"]) > k and t["per_tier"][k] > 0]
        per_tier.append(round(mean(vals), 4) if vals else 0.0)

    census = {
        "horizon": horizon, "stride": stride, "n_seeds": n,
        "living_world": {"avg_series": avg,
                         "final": avg[-1] if avg else {},
                         "genuine_rate_first": avg[0]["genuine_rate"] if avg else 0.0,
                         "genuine_rate_last": avg[-1]["genuine_rate"] if avg else 0.0,
                         "competence_slope": _slope([(r["tick"], r["competence"]) for r in avg])},
        "tower": {"max_tiers_attempted": max_tiers, "tier_ticks": tier_ticks,
                  "depths": depths, "mean_depth": mean(depths) if depths else 0.0,
                  "max_depth": max_reached, "per_tier_competence": per_tier,
                  "across_tier_slope": _slope(list(enumerate(per_tier))) if len(per_tier) >= 2 else 0.0},
    }
    json.dump(census, open("studies/exp061_census.json", "w"), indent=2)
    open("studies/exp061_census.html", "w", encoding="utf-8").write(_render_html(census))

    lw = census["living_world"]
    tw = census["tower"]
    print(f"exp061 — the world census ({horizon:,} ticks, {n} seeds; deep tower {max_tiers} tiers)\n")
    print("  LIVING WORLD (long-horizon vital signs, averaged):")
    print(f"    competence      {avg[0]['competence']:.3f} -> {avg[-1]['competence']:.3f}  (slope {lw['competence_slope']:+.2e}/tick)")
    print(f"    genuine novelty {lw['genuine_rate_first']:.3f} -> {lw['genuine_rate_last']:.3f} /tick  "
          f"({avg[-1]['genuine_distinct']:,.0f} distinct classes ever)")
    print(f"    closure         {avg[0]['closure']:.3f} -> {avg[-1]['closure']:.3f}   "
          f"lifeforms {avg[0]['lifeforms']:.1f} -> {avg[-1]['lifeforms']:.1f}   diversity -> {avg[-1]['diversity']:.2f}")
    print(f"\n  DEEP TOWER: max depth {tw['max_depth']}/{max_tiers}, mean {tw['mean_depth']:.1f}, "
          f"across-tier slope {tw['across_tier_slope']:+.4f}")
    print(f"    per-tier competence: {tw['per_tier_competence']}")
    alive = lw["genuine_rate_last"] > 0.0 and avg[-1]["competence"] > 0.5 * avg[0]["competence"]
    print(f"\n  => living world {'STAYS ALIVE & OPEN' if alive else 'DECAYS'} at {horizon:,} ticks; "
          f"tower climbs to depth {tw['max_depth']}. Census: studies/exp061_census.html")


def _spark_svg(series, key, color, w=560, h=90):
    ys = [r[key] for r in series]
    if not ys:
        return ""
    lo, hi = min(ys), max(ys)
    rng = (hi - lo) or 1.0
    n = len(ys)
    pts = " ".join(f"{i/(n-1)*w:.1f},{h - (y-lo)/rng*(h-10) - 5:.1f}" for i, y in enumerate(ys)) \
        if n > 1 else f"0,{h/2}"
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" style="background:#0b0e14;border-radius:4px">'
            f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>'
            f'<text x="6" y="14" fill="#5b6b82" font-size="11">{key}: {ys[0]:.3f} → {ys[-1]:.3f}</text></svg>')


def _render_html(c) -> str:
    avg = c["living_world"]["avg_series"]
    tw = c["tower"]
    bars = ""
    for i, comp in enumerate(tw["per_tier_competence"]):
        bw = max(2, min(100, comp / 2.2 * 100))
        bars += (f'<div style="display:flex;gap:8px;align-items:center;margin:2px 0">'
                 f'<span style="color:#5b6b82;width:60px">tier {i}</span>'
                 f'<div style="height:14px;width:{bw:.0f}%;background:#ffd18a;border-radius:3px"></div>'
                 f'<span style="color:#e8eef7">{comp:.3f}</span></div>')
    charts = "".join(f'<div style="margin:10px 0">{_spark_svg(avg, k, col)}</div>'
                     for k, col in (("competence", "#ffd18a"), ("genuine_rate", "#8affc1"),
                                    ("closure", "#7fd1ff"), ("lifeforms", "#e88aff")))
    fin = c["living_world"]["final"]
    return f"""<!doctype html><meta charset=utf-8><title>Ω World Census</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#0b0e14;color:#c8d3e0;
font:14px/1.5 ui-monospace,Menlo,monospace;padding:24px;max-width:760px;margin:auto}}
h1{{color:#7fd1ff;font-size:18px;letter-spacing:.08em}}h2{{color:#7fd1ff;font-size:13px;
text-transform:uppercase;letter-spacing:.1em;margin-top:24px}}.k{{color:#5b6b82}}.v{{color:#e8eef7}}
.card{{background:#111624;border:1px solid #1d2433;border-radius:8px;padding:14px 16px;margin:10px 0}}</style>
<h1>Ω WORLD CENSUS</h1>
<div class=k>{c['horizon']:,} ticks · {c['n_seeds']} seeds · bounded memory · living_world + live tower</div>
<h2>Living world — vital signs over the long horizon</h2>
<div class=card>{charts}
<div class=k style=margin-top:8px>final: competence <span class=v>{fin.get('competence',0):.3f}</span> ·
 genuine novelty <span class=v>{fin.get('genuine_rate',0):.3f}/tick</span> ·
 {fin.get('genuine_distinct',0):,.0f} classes ever · closure <span class=v>{fin.get('closure',0):.3f}</span> ·
 self-maintaining lifeforms <span class=v>{fin.get('lifeforms',0):.0f}</span> ·
 diversity <span class=v>{fin.get('diversity',0):.2f}</span></div></div>
<h2>The live tower — how deep do levels climb?</h2>
<div class=card><div class=k>max depth <span class=v>{tw['max_depth']}</span> / {tw['max_tiers_attempted']} attempted ·
 mean depth <span class=v>{tw['mean_depth']:.1f}</span> · across-tier competence slope
 <span class=v>{tw['across_tier_slope']:+.4f}</span></div>
<div style=margin-top:10px>{bars}</div></div>
<div class=k style=margin-top:20px>Generated by studies/exp061_census.py — Project Ω (Ω-0.50).</div>"""


if __name__ == "__main__":
    main()
