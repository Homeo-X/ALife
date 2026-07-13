"""exp034 (10^6-tick horizon) — does sustained novelty need *continuing* construction?

exp034 (Ω-0.19) showed in-level reification holds the novelty rate flat over 30k ticks. But
the alphabet is capped (reify_max_atoms=256), and at the observed ~1 promotion / 500 ticks
that cap is reached around ~112k ticks. So a 10^6-tick run is a natural three-way experiment:

  baseline  : exp030, no reification        — never constructs (fixed alphabet)
  capped    : exp034, reify_max_atoms=256    — constructs, then STOPS at the cap (~112k)
  uncapped  : exp034, reify_max_atoms=0      — keeps constructing for the whole run

The sharp question: after the capped arm stops growing its alphabet, does its novelty rate
resume decaying (like the baseline), while the uncapped arm stays flat? If so, sustained
novelty requires *continuing* constructibility — not a one-time enlargement — the strongest
form of the Ω-0.1 thesis. Honest by construction: rates in temporal windows (not cumulative);
the capped/baseline arms are the matched controls for "stops constructing" / "never
constructs".

Single seed (seed 0): a 10^6-tick run is ~1h/arm on this box, so multi-seed is out of reach;
this is one deep trajectory, not a distribution. Run:
  PYTHONPATH=. python3 studies/exp034_megatick.py [ticks]   (default 1_000_000)
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 10


def _wins(xs: list, k: int) -> list:
    if not xs:
        return [0.0] * k
    n = len(xs)
    return [mean(xs[(w * n) // k:((w + 1) * n) // k] or [0.0]) for w in range(k)]


def _run(args: tuple) -> dict:
    tag, exp, extra, ticks, stride, mem_h = args
    physics, cfg = get_experiment(exp)(seed=0, ticks=ticks, **extra)
    r = run(physics, cfg, record_stride=stride, memory_horizon=mem_h,
            relation_cap=(mem_h * 4 if mem_h else 0))
    return {"tag": tag,
            "novelty_win": _wins(r.novelty_new_per_tick, NWIN),
            "self_win": _wins(physics._hered_edge_self, NWIN),
            "null_win": _wins(physics._hered_edge_null, NWIN),
            "atoms_final": len(physics.atoms),
            "reified": len(getattr(physics, "_reified", {})),
            "classes": r.final_classes_total, "final_pop": r.final_population}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    stride = max(1, ticks // 800)
    # Run arms SEQUENTIALLY and persist after EACH so a container reclaim only loses the
    # in-progress arm. Most-informative arm first: uncapped (keeps constructing) then capped
    # (constructs then stops) then baseline (never constructs). Two workers keep two cores
    # each on a 4-core box; a single long arm is CPU-bound anyway.
    # A LOW cap (64) makes the "constructs then stops" arm reach its ceiling early (~15-20k
    # ticks), so the post-cap regime — the decisive comparison — dominates the run without
    # needing a 10^6 horizon (open-ended novelty grows the class registry unboundedly, so a
    # literal 10^6 run is memory-bound on a 16GB box; this is the same experiment at a
    # feasible, memory-safe horizon).
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    # memory_horizon (arg 3): 0 = unbounded/exact (small horizons); >0 = bounded-memory mode
    # for very long horizons (all arms use the SAME horizon so the windowed-novelty inflation
    # is common-mode and the bounded-to-bounded comparison stays valid). Pick it >> the
    # class-turnover timescale to keep inflation small.
    mem_h = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    jobs = [
        ("uncapped", "exp034", {"reify_max_atoms": 0}, ticks, stride, mem_h),
        ("capped",   "exp034", {"reify_max_atoms": cap}, ticks, stride, mem_h),
        ("baseline", "exp030", {}, ticks, stride, mem_h),
    ]
    out_path = ("studies/exp034_megatick_results.json" if not mem_h
               else f"studies/exp034_megatick_bounded{ticks}_results.json")
    rows = []
    with ProcessPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(_run, j) for j in jobs]
        for f in as_completed(futs):
            rows.append(f.result())
            json.dump({"ticks": ticks, "nwin": NWIN, "mem_h": mem_h, "rows": rows},
                      open(out_path, "w"), indent=2)
            print(f"[done {rows[-1]['tag']}] atoms={rows[-1]['atoms_final']} "
                  f"classes={rows[-1]['classes']}", flush=True)
    by = {r["tag"]: r for r in rows}
    if not all(t in by for t in ("baseline", "capped", "uncapped")):
        return  # partial (reclaimed); results.json holds completed arms

    win_ticks = ticks // NWIN
    cap_reified = by["capped"]["reified"]
    print(f"exp034 — long-horizon: does sustained novelty need CONTINUING construction?")
    print(f"  {ticks} ticks, seed 0, {NWIN} windows of {win_ticks} ticks; the capped arm "
          f"stopped growing at {by['capped']['atoms_final']} atoms ({cap_reified} reified)\n")
    hdr = "  " + "".join(f"w{w:<6}" for w in range(NWIN))
    print("  novelty rate / window (new classes/tick):")
    print(hdr)
    for tag in ("baseline", "capped", "uncapped"):
        print(f"  {tag[:4]} " + " ".join(f"{v:6.3f}" for v in by[tag]["novelty_win"]))

    print("\n  collective heredity self>null (uncapped arm — must stay heritable):")
    print("  self " + " ".join(f"{v:6.3f}" for v in by["uncapped"]["self_win"]))
    print("  null " + " ".join(f"{v:6.3f}" for v in by["uncapped"]["null_win"]))

    def late_early(w):
        return (mean(w[-3:]) / mean(w[1:3])) if mean(w[1:3]) > 0 else 0.0
    print(f"\n  atoms final: baseline {by['baseline']['atoms_final']}, "
          f"capped {by['capped']['atoms_final']} ({by['capped']['reified']} reified), "
          f"uncapped {by['uncapped']['atoms_final']} ({by['uncapped']['reified']} reified)")
    print(f"  novelty-rate late/early ratio (higher = less decay):")
    for tag in ("baseline", "capped", "uncapped"):
        print(f"    {tag:>9}: {late_early(by[tag]['novelty_win']):.2f}")
    bl = late_early(by["baseline"]["novelty_win"])
    cp = late_early(by["capped"]["novelty_win"])
    un = late_early(by["uncapped"]["novelty_win"])
    if un > cp + 0.2 and un >= 0.85:
        print("\n  => sustained novelty needs CONTINUING construction: the uncapped arm holds")
        print("     its rate while the capped arm decays after its alphabet stops growing.")
    elif cp >= 0.85 and un >= 0.85:
        print("\n  => a one-time alphabet enlargement suffices: both capped and uncapped hold")
        print("     their rate (a modest fixed construction budget is enough at this horizon).")
    else:
        print("\n  => see trajectory: novelty decays even with construction — a deeper limit.")


if __name__ == "__main__":
    main()
