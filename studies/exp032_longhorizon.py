"""exp032 Part A — within-level long-horizon persistence (the unboundedness test).

Every findings doc hands forward the same frontier and it is the program's original
goal (Ω-0.1/0.10/0.14): *unboundedness*. All headline results are bounded-horizon bursts
(400–4000 ticks). This runs the exp030 "both corner" (open-ended AND modular) to a long
horizon and asks: over 10^4–10^5 ticks, do the novelty **rate** and collective **heredity**
*both* stay alive, or does one decay (the exp004 dilution caveat at scale)?

Method (guardrails mandatory — the program has two metric-artefact false positives on
record): measure **rates in temporal windows, not cumulatives**, with a matched **closed**
control (exp029, novelty→0) so the sustained novelty is attributable to the open corner.
 - novelty rate/window: mean new classes/tick over K equal *tick* windows
   (`RunResult.novelty_new_per_tick`, per-tick, unaffected by record_stride).
 - collective heredity/window: the physics' `_hered_edge_self` / `_hered_edge_null` lists
   sliced (in append/temporal order) into K windows. NB these are **event-count** windows
   (one entry per deme-founding heredity event), an approximate temporal alignment, not
   exact tick windows.
 - population + reservoir pressure: stability (from the subsampled metrics snapshot).

Success: both novelty rate and heredity (self > null) stay > 0 across *all* windows — the
"both corner" is sustained, not a transient. Null: one decays; we report which corner
fails first (novelty dilution vs heredity erosion) and at what fraction of the horizon.

Run: PYTHONPATH=. python3 studies/exp032_longhorizon.py [ticks] [n_seeds] [stretch_ticks]
  defaults: 40000 ticks, 3 seeds, one 120000-tick stretch run (open corner, seed 0).
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 8  # temporal windows


def _wins(xs: list, k: int) -> list:
    """Split a series into k contiguous windows; mean of each (0.0 for an empty window)."""
    if not xs:
        return [0.0] * k
    n = len(xs)
    out = []
    for w in range(k):
        lo, hi = (w * n) // k, ((w + 1) * n) // k
        seg = xs[lo:hi]
        out.append(mean(seg) if seg else 0.0)
    return out


def _run(args: tuple) -> dict:
    tag, exp, seed, ticks, stride = args
    physics, cfg = get_experiment(exp)(seed=seed, ticks=ticks)
    r = run(physics, cfg, record_stride=stride)
    pops = [m["population"] for m in r.metrics]
    press = [m["reservoir_pressure"] for m in r.metrics]
    return {
        "tag": tag, "exp": exp, "seed": seed, "ticks": ticks,
        "novelty_win": _wins(r.novelty_new_per_tick, NWIN),
        "self_win": _wins(physics._hered_edge_self, NWIN),
        "null_win": _wins(physics._hered_edge_null, NWIN),
        "n_hered_events": len(physics._hered_edge_self),
        "novelty_rate": r.open_endedness["novelty_rate"],
        "verdict": r.open_endedness["verdict"],
        "final_pop": r.final_population,
        "final_classes": r.final_classes_total,
        "pop_lo": min(pops) if pops else 0, "pop_hi": max(pops) if pops else 0,
        "press_last": press[-1] if press else 0.0,
    }


def _agg(rows: list, k: int) -> dict:
    """Average per-window across seeds."""
    return {
        "novelty": [mean(r["novelty_win"][w] for r in rows) for w in range(k)],
        "self": [mean(r["self_win"][w] for r in rows) for w in range(k)],
        "null": [mean(r["null_win"][w] for r in rows) for w in range(k)],
    }


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    n_seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    stretch = int(sys.argv[3]) if len(sys.argv) > 3 else 120000
    seeds = list(range(n_seeds))
    stride = max(1, ticks // 800)          # ~800 metric snapshots regardless of horizon
    sstride = max(1, stretch // 800)

    jobs = ([("open", "exp030", s, ticks, stride) for s in seeds]
            + [("closed", "exp029", s, ticks, stride) for s in seeds]
            + [("stretch", "exp030", 0, stretch, sstride)])   # overlap the long run
    with ProcessPoolExecutor(max_workers=8) as ex:
        allrows = list(ex.map(_run, jobs))
    open_rows = [r for r in allrows if r["tag"] == "open"]
    closed_rows = [r for r in allrows if r["tag"] == "closed"]
    stretch_row = next(r for r in allrows if r["tag"] == "stretch")

    payload = {"ticks": ticks, "n_seeds": n_seeds, "nwin": NWIN,
               "open": open_rows, "closed": closed_rows, "stretch": stretch_row}
    json.dump(payload, open("studies/exp032_longhorizon_results.json", "w"), indent=2)

    print(f"exp032 Part A — within-level persistence at the 'both corner'")
    print(f"  open = exp030 (typed_path, open+modular); closed = exp029 (typed, modular-only)")
    print(f"  {ticks} ticks, {n_seeds} seeds, {NWIN} temporal windows\n")

    o = _agg(open_rows, NWIN)
    c = _agg(closed_rows, NWIN)
    hdr = "  " + "".join(f"w{w:<7}" for w in range(NWIN))
    print("  novelty rate/window (new classes/tick):")
    print(hdr)
    print("  open " + " ".join(f"{v:6.3f}" for v in o["novelty"]))
    print("  clsd " + " ".join(f"{v:6.3f}" for v in c["novelty"]))
    print("\n  collective heredity/window (edge-set Jaccard, self vs null):")
    print(hdr)
    print("  self " + " ".join(f"{v:6.3f}" for v in o["self"]))
    print("  null " + " ".join(f"{v:6.3f}" for v in o["null"]))

    # verdicts
    nov_alive = all(v > 0 for v in o["novelty"])
    her_alive = all(o["self"][w] > o["null"][w] for w in range(NWIN))
    clsd_closes = c["novelty"][-1] <= o["novelty"][-1] * 0.5
    print(f"\n  open-corner novelty rate > 0 across ALL windows : {nov_alive}")
    print(f"  open-corner heredity self > null across ALL windows: {her_alive}")
    print(f"  closed control novelty collapses vs open           : {clsd_closes} "
          f"(closed last window {c['novelty'][-1]:.3f} vs open {o['novelty'][-1]:.3f})")
    if nov_alive and her_alive:
        print("  => SUSTAINED: the 'both corner' persists at long horizon (not a transient).")
    else:
        print("  => DECAYS: one corner fails — see per-window trajectory above.")

    pops = [r["final_pop"] for r in open_rows]
    print(f"\n  stability (open): final pop {mean(pops):.0f}±{pstdev(pops):.0f}, "
          f"pop range over run [{min(r['pop_lo'] for r in open_rows)},"
          f"{max(r['pop_hi'] for r in open_rows)}], reservoir_pressure_last "
          f"{mean(r['press_last'] for r in open_rows):.3f}")

    s = stretch_row
    sn = _wins(s["novelty_win"], NWIN) if False else s["novelty_win"]
    print(f"\n  stretch run — exp030 seed 0 to {stretch} ticks "
          f"({s['n_hered_events']} heredity events):")
    print("  novelty " + " ".join(f"{v:6.3f}" for v in s["novelty_win"]))
    print("  self    " + " ".join(f"{v:6.3f}" for v in s["self_win"]))
    print("  null    " + " ".join(f"{v:6.3f}" for v in s["null_win"]))
    s_nov = all(v > 0 for v in s["novelty_win"])
    s_her = all(s["self_win"][w] > s["null_win"][w] for w in range(NWIN))
    print(f"  stretch verdict: novelty_alive={s_nov} heredity_alive={s_her} "
          f"(final_classes={s['final_classes']}, final_pop={s['final_pop']})")


if __name__ == "__main__":
    main()
