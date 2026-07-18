"""exp051 (consolidation) — the horizon stress: does the ~0.09 genuine-novelty floor HOLD past 10⁶, or
resume declining?

Ω-0.39 (exp050) settled "stays open forever" at 10⁶ ticks: the eviction-robust global rate falls
0.30 → 0.10 over the first ~400k ticks, then levels onto ~0.085–0.10 genuinely-new classes/tick for the
whole second half — a decelerating curve that *looks* like it converges to a positive floor. But the
last windows still sag ~18%, so a slower second-order decline toward zero is not strictly ruled out.
This pushes the horizon **3× further (3M ticks)** with the eviction regime held FIXED, and asks the one
remaining question: does the floor stay flat from 10⁶ to 3M (converged), or keep sliding (dilution on a
longer timescale)?

Key methodological choice: `memory_horizon` is held **fixed** (not scaled with ticks) so the eviction
regime is identical across horizons — the genuine (global) rate is registry-independent anyway, but a
fixed window keeps the windowed/global inflation comparable. `relation_cap` is kept small: it bounds the
relation registry for speed and does **not** affect the global-novelty sketch (which is the headline
metric), so shrinking it trades only windowed-registry detail for throughput.

Reuses the exp050 machinery (`_one`, `_wins`, `NWIN`) but with its OWN results file so the Ω-0.39 10⁶
artifact is preserved. Arms run in a pool with reclaim-safe partial writes per completed job. Run:
  PYTHONPATH=. python3 studies/exp051_horizonstress.py [ticks] [n_seeds] [memory_horizon] [workers]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 12
OUT = "studies/exp051_horizonstress_results.json"
RELATION_CAP = 8000  # bounds the relation registry (speed); does NOT touch the global-novelty sketch


def _wins(xs: list, k: int) -> list:
    if not xs:
        return [0.0] * k
    n = len(xs)
    return [mean(xs[(w * n) // k:((w + 1) * n) // k] or [0.0]) for w in range(k)]


def _one(args) -> dict:
    tag, exp, seed, ticks, mem_h = args
    physics, cfg = get_experiment(exp)(seed=seed, ticks=ticks)
    stride = max(1, ticks // 1000)
    r = run(physics, cfg, record_stride=stride, memory_horizon=mem_h,
            relation_cap=RELATION_CAP, global_novelty=True)
    return {
        "tag": tag, "exp": exp, "seed": seed,
        "windowed_win": _wins(r.novelty_new_per_tick, NWIN),
        "global_win": _wins(r.novelty_global_new_per_tick, NWIN),
        "classes_registry": r.final_classes_total,
        "classes_global": r.final_classes_global,
        "final_pop": r.final_population,
    }


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    mem_h = int(sys.argv[3]) if len(sys.argv) > 3 else 5000   # FIXED (matches the Ω-0.39 eviction regime)
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4

    arms = [("open", "exp030"), ("closed", "exp029")]
    jobs = [(f"{tag}-s{s}", exp, s, ticks, mem_h) for (tag, exp) in arms for s in range(n)]
    rows: list = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_one, j): j[0] for j in jobs}
        for fut in as_completed(futs):
            rows.append(fut.result())
            json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem_h, "nwin": NWIN,
                       "relation_cap": RELATION_CAP, "rows": rows}, open(OUT, "w"), indent=2)
            r = rows[-1]
            print(f"[done {r['tag']}] registry={r['classes_registry']} "
                  f"global_distinct={r['classes_global']} "
                  f"late_global={mean(r['global_win'][-3:]):.4f}", flush=True)

    def agg(tag, key):
        rs = [r for r in rows if r["tag"].startswith(tag)]
        return [mean(r[key][w] for r in rs) for w in range(NWIN)]

    print(f"\nexp051 — does the genuine-novelty floor HOLD past 10⁶? "
          f"({ticks} ticks, {n} seeds, mem_h={mem_h} FIXED, {NWIN} windows)\n")
    for tag, exp in arms:
        ww, gw = agg(tag, "windowed_win"), agg(tag, "global_win")
        print(f"  [{tag} = {exp}]")
        print(f"    {'window':>9} " + " ".join(f"{w:>7}" for w in range(NWIN)))
        print(f"    {'windowed':>9} " + " ".join(f"{v:>7.4f}" for v in ww))
        print(f"    {'global':>9} " + " ".join(f"{v:>7.4f}" for v in gw))
        print()

    open_g = agg("open", "global_win")
    closed_g = agg("closed", "global_win")
    # compare the FIRST-third late region (~10⁶-scale) to the FINAL region (~3M) — did the floor hold?
    third = NWIN // 3
    mid = mean(open_g[third:2 * third])      # ~1M–2M region
    late = mean(open_g[-third:])             # ~2M–3M region (the final third)
    closed_late = mean(closed_g[-third:])
    global_distinct = mean(r["classes_global"] for r in rows if r["tag"].startswith("open"))
    hold_ratio = (late / mid) if mid > 0 else 0.0
    floor = late > 0.01 and late > 5 * max(closed_late, 1e-9)
    held = floor and hold_ratio > 0.75      # final third within 25% of the mid region ⇒ flat floor
    print(f"  open global: mid(~1–2M)={mid:.4f}  final(~2–3M)={late:.4f}  hold_ratio={hold_ratio:.2f}  "
          f"distinct-ever≈{global_distinct:.0f}")
    print(f"  closed global final = {closed_late:.4f} (instrument sanity: must be ~0)\n")
    if held:
        print("  => FLOOR HOLDS TO 3M (converged): the genuine-novelty rate is flat within 25% across the")
        print("     final 2M ticks, decisively above the closed control. The Ω-0.39 deceleration has")
        print("     converged to a positive constant — 'stays open forever' survives a 3× horizon stress,")
        print("     with no sign of second-order dilution toward zero.")
    elif floor:
        print("  => FLOOR STILL SLOWLY SLIDING: the rate stays clearly positive and ≫ closed to 3M, but the")
        print(f"     final third is {hold_ratio:.2f}× the mid region — a slow second-order decline persists.")
        print("     Open at 3M but not yet provably converged; the honest reading is a large finite budget")
        print("     draining very slowly, not a proven asymptotic floor.")
    else:
        print("  => FLOOR DILUTES BY 3M (honest negative): the genuine rate falls toward the closed control")
        print("     at the longer horizon — 'ever-open' narrows to a finite constructive budget after all.")


if __name__ == "__main__":
    main()
