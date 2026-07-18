"""exp043 (consolidation) — settle "stays open forever": is the long-run novelty a POSITIVE FLOOR
or eviction-window recycling?

The load-bearing claim of the whole program is that constructibility keeps the world open. It is only
shown in miniature, and its long-horizon form is unsettled for a concrete reason: a long run needs
bounded memory (`memory_horizon`), which evicts cold class records, so an evicted class that reappears
RE-COUNTS in the windowed novelty rate. A positive long-run windowed rate therefore cannot be told
apart from the same classes cycling through the eviction window (exp032's "positive-floor vs
slow-dilution" open edge).

This run uses the eviction-robust GLOBAL novelty estimator (`run(global_novelty=True)`, a scalable
Bloom 'ever-seen' set: omega/emergence/global_novelty.py) to strip that inflation. It reports BOTH the
windowed rate (`classes_ever_seen`, inflated) and the global rate (deduplicated, conservative) over
windows, for the open engine (exp030, the both corner) vs a closed control (exp029, novelty→0).

Verdict:
  * global rate stays positive to the horizon  => a GENUINE positive floor — the claim is settled.
  * global rate -> 0 while windowed stays > 0   => long-run openness WAS eviction recycling (dilution)
                                                   — an honest negative that retires an overclaim.
The closed control must read ~0 on both (instrument sanity).

Feasibility: bounded memory keeps RAM flat and the Bloom sketch is fixed-memory, so a literal long run
is memory-safe. Arms run sequentially with the results.json rewritten after EACH (so a container
reclaim only loses the in-progress arm). Run:
  PYTHONPATH=. python3 studies/exp043_unbounded.py [ticks] [n_seeds] [memory_horizon]
"""
from __future__ import annotations
import json, sys
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 10


def _wins(xs: list, k: int) -> list:
    if not xs:
        return [0.0] * k
    n = len(xs)
    return [mean(xs[(w * n) // k:((w + 1) * n) // k] or [0.0]) for w in range(k)]


def _one(tag: str, exp: str, seed: int, ticks: int, mem_h: int) -> dict:
    physics, cfg = get_experiment(exp)(seed=seed, ticks=ticks)
    stride = max(1, ticks // 800)
    r = run(physics, cfg, record_stride=stride, memory_horizon=mem_h,
            relation_cap=(mem_h * 4 if mem_h else 0), global_novelty=True)
    return {
        "tag": tag, "exp": exp, "seed": seed,
        "windowed_win": _wins(r.novelty_new_per_tick, NWIN),      # inflated under eviction
        "global_win": _wins(r.novelty_global_new_per_tick, NWIN),  # eviction-robust
        "classes_registry": r.final_classes_total,                 # bounded (flat) registry size
        "classes_global": r.final_classes_global,                  # true distinct-ever (deduplicated)
        "final_pop": r.final_population,
    }


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    # horizon >> class-turnover timescale so the registry stays flat but eviction is real; default
    # scales with the run. All arms share it, so windowed inflation is common-mode.
    mem_h = int(sys.argv[3]) if len(sys.argv) > 3 else max(2000, ticks // 200)

    arms = [("open", "exp030"), ("closed", "exp029")]
    jobs = [(f"{tag}-s{s}", exp, s) for (tag, exp) in arms for s in range(n)]
    out = "studies/exp043_unbounded_results.json"
    rows = []
    for name, exp, seed in jobs:
        rows.append(_one(name, exp, seed, ticks, mem_h))
        json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem_h, "nwin": NWIN, "rows": rows},
                  open(out, "w"), indent=2)
        r = rows[-1]
        print(f"[done {name}] registry={r['classes_registry']} global_distinct={r['classes_global']} "
              f"late_global={mean(r['global_win'][-3:]):.4f}", flush=True)

    def agg(tag, key):
        rs = [r for r in rows if r["tag"].startswith(tag)]
        return [mean(r[key][w] for r in rs) for w in range(NWIN)]

    print(f"\nexp043 — is long-run novelty a POSITIVE FLOOR or eviction recycling? "
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
    # a positive floor: the eviction-robust global rate is still clearly > 0 in the last windows, and
    # decisively above the closed control (which must be ~0 on the global metric).
    floor = open_late > 0.01 and open_late > 5 * max(closed_late, 1e-9)
    retention = (open_late / open_early) if open_early > 0 else 0.0
    print(f"  open global novelty: early(w1-2)={open_early:.4f}  late(w-3..)={open_late:.4f}  "
          f"retention={retention:.2f}")
    print(f"  closed global novelty late = {closed_late:.4f} (instrument sanity: must be ~0)\n")
    if floor:
        print("  => POSITIVE FLOOR (settled): even with all eviction-recycling stripped, the open")
        print("     engine keeps discovering genuinely-never-seen classes to the horizon, decisively")
        print("     above the closed control. 'Stays open forever' is a real property of the global")
        print("     novelty rate, not an artifact of the bounded-memory measurement window.")
    else:
        print("  => NO GLOBAL FLOOR (honest negative): once recycling is stripped, the open engine's")
        print("     genuine-novelty rate decays toward the closed control — the apparent long-run")
        print("     openness was largely eviction-window recycling. The claim narrows to a finite")
        print("     (very large) constructive budget, not literally ever-open — a clean overclaim retirement.")


if __name__ == "__main__":
    main()
