"""exp050 (consolidation) — the LITERAL 10⁶-tick campaign: is the genuine-novelty floor real at the
long horizon, or does it dilute to zero?

Ω-0.31 (studies/exp043_unbounded.py) settled "stays open forever" on the eviction-robust GLOBAL
novelty sketch — but only to **300k ticks / 3 seeds**, where it found the genuine (deduplicated) rate
is a *positive but slowly declining* floor. The ROADMAP's #1 frontier is to push that to the literal
long horizon the whole thesis rests on: **10⁶ ticks, multi-seed**. This study runs exactly that and
asks whether the genuine-novelty floor **survives** an order of magnitude more time or **decays toward
the closed control** (dilution).

Instrument (unchanged, gated): `run(global_novelty=True)` threads a fixed-memory scalable-Bloom
'ever-seen' set (omega/emergence/global_novelty.py) that counts each class *once ever*, stripping the
eviction-window recycling that inflates the windowed rate under bounded memory. Reports BOTH the
windowed rate (`classes_ever_seen`, inflated) and the global rate (deduplicated, conservative) over
windows, for the open engine (exp030, the both corner) vs a closed control (exp029, novelty→0).

Verdict (on the GLOBAL rate at 10⁶):
  * late global rate clearly > 0 and ≫ closed  => the positive floor is REAL at 10⁶ — the strongest
                                                  form of the thesis, settled an order of magnitude out.
  * late global rate -> ~closed (≈0)           => the floor DILUTES at the long horizon — an honest
                                                  negative that narrows "ever-open" to a (large) finite
                                                  constructive budget.
The closed control must read ~0 on the global metric at every horizon (instrument sanity).

Runs arms in a process pool (default 4 workers) and rewrites results.json after EACH job COMPLETES, so
a container reclaim only loses the in-flight jobs. Memory is bounded (per-worker `memory_horizon` +
`relation_cap`; the Bloom sketch is fixed-size), so a literal 10⁶ run is memory-safe. Run:
  PYTHONPATH=. python3 studies/exp050_megahorizon.py [ticks] [n_seeds] [memory_horizon] [workers]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 10
OUT = "studies/exp050_megahorizon_results.json"


def _wins(xs: list, k: int) -> list:
    if not xs:
        return [0.0] * k
    n = len(xs)
    return [mean(xs[(w * n) // k:((w + 1) * n) // k] or [0.0]) for w in range(k)]


def _one(args) -> dict:
    tag, exp, seed, ticks, mem_h = args
    physics, cfg = get_experiment(exp)(seed=seed, ticks=ticks)
    stride = max(1, ticks // 800)
    r = run(physics, cfg, record_stride=stride, memory_horizon=mem_h,
            relation_cap=(mem_h * 4 if mem_h else 0), global_novelty=True)
    return {
        "tag": tag, "exp": exp, "seed": seed,
        "windowed_win": _wins(r.novelty_new_per_tick, NWIN),       # inflated under eviction
        "global_win": _wins(r.novelty_global_new_per_tick, NWIN),   # eviction-robust
        "classes_registry": r.final_classes_total,                  # bounded (flat) registry size
        "classes_global": r.final_classes_global,                   # true distinct-ever (deduplicated)
        "final_pop": r.final_population,
    }


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    mem_h = int(sys.argv[3]) if len(sys.argv) > 3 else max(2000, ticks // 200)
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4

    arms = [("open", "exp030"), ("closed", "exp029")]
    jobs = [(f"{tag}-s{s}", exp, s, ticks, mem_h) for (tag, exp) in arms for s in range(n)]
    rows: list = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_one, j): j[0] for j in jobs}
        for fut in as_completed(futs):
            rows.append(fut.result())
            json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem_h, "nwin": NWIN,
                       "rows": rows}, open(OUT, "w"), indent=2)
            r = rows[-1]
            print(f"[done {r['tag']}] registry={r['classes_registry']} "
                  f"global_distinct={r['classes_global']} "
                  f"late_global={mean(r['global_win'][-3:]):.4f}", flush=True)

    def agg(tag, key):
        rs = [r for r in rows if r["tag"].startswith(tag)]
        return [mean(r[key][w] for r in rs) for w in range(NWIN)]

    print(f"\nexp050 — is the genuine-novelty floor REAL at 10⁶ or does it DILUTE? "
          f"({ticks} ticks, {n} seeds, mem_h={mem_h}, {NWIN} windows)\n")
    for tag, exp in arms:
        ww, gw = agg(tag, "windowed_win"), agg(tag, "global_win")
        print(f"  [{tag} = {exp}]")
        print(f"    {'window':>9} " + " ".join(f"{w:>7}" for w in range(NWIN)))
        print(f"    {'windowed':>9} " + " ".join(f"{v:>7.4f}" for v in ww))
        print(f"    {'global':>9} " + " ".join(f"{v:>7.4f}" for v in gw))
        infl = (mean(ww[-3:]) / mean(gw[-3:])) if mean(gw[-3:]) > 0 else float("inf")
        print(f"    late windowed/global inflation factor = {infl:.2f}\n")

    open_g = agg("open", "global_win")
    closed_g = agg("closed", "global_win")
    open_late = mean(open_g[-3:]); open_early = mean(open_g[1:3])
    closed_late = mean(closed_g[-3:])
    global_distinct = mean(r["classes_global"] for r in rows if r["tag"].startswith("open"))
    floor = open_late > 0.01 and open_late > 5 * max(closed_late, 1e-9)
    retention = (open_late / open_early) if open_early > 0 else 0.0
    print(f"  open global novelty: early(w1-2)={open_early:.4f}  late(w-3..)={open_late:.4f}  "
          f"retention={retention:.2f}  distinct-ever≈{global_distinct:.0f}")
    print(f"  closed global novelty late = {closed_late:.4f} (instrument sanity: must be ~0)\n")
    if floor:
        print("  => POSITIVE FLOOR HOLDS AT 10⁶ (settled an order of magnitude out): with all eviction-")
        print("     recycling stripped, the open engine STILL discovers genuinely-never-seen classes to")
        print("     the 10⁶ horizon, decisively above the closed control. 'Stays open forever' is a real")
        print("     property of the global novelty rate at the long horizon, not a windowing artifact.")
    else:
        print("  => FLOOR DILUTES AT 10⁶ (honest negative): once recycling is stripped, the open engine's")
        print("     genuine-novelty rate decays toward the closed control at the long horizon — 'ever-open'")
        print("     narrows to a large but FINITE constructive budget. A clean overclaim retirement.")


if __name__ == "__main__":
    main()
