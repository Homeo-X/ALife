"""exp034 — sustained novelty via in-level reification (the constructibility lever).

exp032 found the both-corner's novelty *rate* drifts down over a long horizon (~0.45→0.16
across 120k ticks) because the atom alphabet is fixed — the open edge left in Ω-0.17. The
program's core thesis (Ω-0.1) is that open-ended complexity needs infinite *constructibility*,
not infinite space: reification (exp004) — promoting a persistent motif to a NEW primitive —
was the mechanism that kept an individual-level world open. This turns that lever on *within*
the collective both-corner substrate: every `reify_period` ticks the most common recent
product motif becomes a new atom (growing `self.atoms` during the run).

Test: does growing the constructive base flatten the novelty-rate decay? Compare, over a long
horizon in temporal windows (rate, not cumulative), the baseline exp030 (fixed alphabet) vs
exp034 (reify on). Success = exp034's late-window novelty rate is materially higher than the
baseline's (the decay is arrested/slowed); the honest null = reification does not help (the
decay is intrinsic to the deme dynamics, not the fixed alphabet).

Run: PYTHONPATH=. python3 studies/exp034_reification.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.harness import run

NWIN = 8


def _wins(xs: list, k: int) -> list:
    if not xs:
        return [0.0] * k
    n = len(xs)
    return [mean(xs[(w * n) // k:((w + 1) * n) // k] or [0.0]) for w in range(k)]


def _run(args: tuple) -> dict:
    tag, exp, seed, ticks, stride = args
    physics, cfg = get_experiment(exp)(seed=seed, ticks=ticks)
    r = run(physics, cfg, record_stride=stride)
    return {"tag": tag, "seed": seed,
            "novelty_win": _wins(r.novelty_new_per_tick, NWIN),
            "self_win": _wins(physics._hered_edge_self, NWIN),
            "null_win": _wins(physics._hered_edge_null, NWIN),
            "atoms_final": len(physics.atoms),
            "reified": len(getattr(physics, "_reified", {})),
            "classes": r.final_classes_total, "final_pop": r.final_population}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    n_seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    stride = max(1, ticks // 800)
    jobs = ([("baseline", "exp030", s, ticks, stride) for s in range(n_seeds)]
            + [("reify", "exp034", s, ticks, stride) for s in range(n_seeds)])
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n_seeds, "rows": rows},
              open("studies/exp034_results.json", "w"), indent=2)

    base = [r for r in rows if r["tag"] == "baseline"]
    reif = [r for r in rows if r["tag"] == "reify"]
    bn = [mean(r["novelty_win"][w] for r in base) for w in range(NWIN)]
    rn = [mean(r["novelty_win"][w] for r in reif) for w in range(NWIN)]
    rs = [mean(r["self_win"][w] for r in reif) for w in range(NWIN)]
    rnull = [mean(r["null_win"][w] for r in reif) for w in range(NWIN)]

    print(f"exp034 — sustained novelty via in-level reification "
          f"({ticks} ticks, {n_seeds} seeds, {NWIN} windows)\n")
    hdr = "  " + "".join(f"w{w:<6}" for w in range(NWIN))
    print("  novelty rate / window (new classes/tick):")
    print(hdr)
    print("  base " + " ".join(f"{v:6.3f}" for v in bn))
    print("  reif " + " ".join(f"{v:6.3f}" for v in rn))
    print("\n  reify heredity / window (self vs null — must stay heritable):")
    print("  self " + " ".join(f"{v:6.3f}" for v in rs))
    print("  null " + " ".join(f"{v:6.3f}" for v in rnull))

    def decay(w):  # late/early novelty-rate ratio over windows 1..end (skip w0 burst)
        return (mean(w[-2:]) / mean(w[1:3])) if mean(w[1:3]) > 0 else 0.0
    b_last, r_last = mean(bn[-2:]), mean(rn[-2:])
    print(f"\n  atoms grown (reify): {32} -> "
          f"{mean(r['atoms_final'] for r in reif):.0f} "
          f"({mean(r['reified'] for r in reif):.0f} motifs reified)")
    print(f"  late-window novelty rate: baseline {b_last:.3f} vs reify {r_last:.3f} "
          f"({r_last / b_last:.2f}x)" if b_last else "")
    print(f"  decay (late/early ratio): baseline {decay(bn):.2f} vs reify {decay(rn):.2f} "
          f"(higher = less decay)")
    her_ok = all(rs[w] > rnull[w] for w in range(1, NWIN))
    if r_last > b_last * 1.15 and her_ok:
        print("  => reification SLOWS the novelty-rate decay while heredity stays alive:")
        print("     growing constructibility (not space) sustains novelty. Thesis supported.")
    elif her_ok:
        print("  => reification does NOT materially slow the decay (heredity intact): the")
        print("     rate decline is intrinsic to the deme dynamics, not the fixed alphabet.")
    else:
        print("  => reification perturbs heredity — see per-window detail.")


if __name__ == "__main__":
    main()
