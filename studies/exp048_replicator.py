"""exp048 — THE LOOP-BACK: does collective competence compound when the PARTS are replicators?

The self-improvement arc (exp036–047) closed with a terminal diagnosis: collective competence is
irreducibly collective, and the typed_path substrate's parts are context-dependent network components,
not replicators — so no selection/representation route makes competence compound. exp012 found the one
place genuine PART-LEVEL replicators emerge: the behaviour-first SKI-combinator soup, where an
organization can emit a copy of *itself* (C·x → C). This runs the exp046 credit machinery on that
combinator substrate, so a credited part can carry and copy its OWN heritable value — and asks whether
competence finally compounds over generations, closing the arc's end back to its beginning.

Arms:
  - "replicator"  : substrate="combinator", deme_fitness="credit"  (exp048 — parts CAN self-replicate)
  - "network"     : substrate="typed_path", deme_fitness="credit"  (exactly exp046 — non-replicating parts)
  - "replicator-drift" : substrate="combinator", deme_fitness="size"  (isolates whether credit does
                          anything ON the replicator substrate)

Metrics per generation-window: mean COMPETENCE (closure + breed-true heredity + breadth), mean CLOSURE,
and the novelty rate proxy (distinct-class growth). Headline: does the replicator substrate make
competence RISE over generations (slope > 0) where typed_path (exp046) was flat/declining, and does
credit beat drift there? Run:
  PYTHONPATH=. python3 studies/exp048_replicator.py [ticks] [n_seeds] [memory_horizon]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

N_WINDOWS = 8
SAMPLE_STRIDE = 5
TRANSIENT = 2


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _run(args) -> dict:
    arm, substrate, fit, seed, ticks, mem = args
    p, c = get_experiment("exp048")(seed=seed, ticks=ticks,
                                    substrate=substrate, deme_fitness=fit, network_template=0.5)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    win = max(1, ticks // N_WINDOWS)
    traj = []
    for w in range(N_WINDOWS):
        comp, clo = [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
                    clo.append(mean(p._deme_closure(pi) for pi in act))
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0})
    return {"arm": arm, "seed": seed, "traj": traj, "classes": u.classes_ever_seen}


def _avg(rows, arm, key):
    rs = [r for r in rows if r["arm"] == arm]
    return [mean(r["traj"][w][key] for r in rs) for w in range(N_WINDOWS)]


def _slope(ys):
    n = len(ys); xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    arms = [("replicator", "combinator", "credit"),
            ("network", "typed_path", "credit"),
            ("replicator-drift", "combinator", "size")]
    jobs = [(a, sub, f, s, ticks, mem) for (a, sub, f) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure")} for (a, _s, _f) in arms}
    classes = {a: mean(r["classes"] for r in rows if r["arm"] == a) for (a, _s, _f) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs, "classes": classes}, open("studies/exp048_results.json", "w"), indent=2)

    print(f"exp048 — does collective competence compound when the PARTS are replicators? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _s, _f in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>12} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>12} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>12} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"mean {mean(tr['competence'][TRANSIENT:]):.3f}, classes {classes[arm]:.0f}\n")

    rc = trajs["replicator"]["competence"]; nc = trajs["network"]["competence"]; dc = trajs["replicator-drift"]["competence"]
    r_slope, n_slope = _slope(rc[TRANSIENT:]), _slope(nc[TRANSIENT:])
    r_mean, n_mean, d_mean = mean(rc[TRANSIENT:]), mean(nc[TRANSIENT:]), mean(dc[TRANSIENT:])
    print(f"  competence slope: replicator {r_slope:+.4f}/win (mean {r_mean:.3f}) vs typed_path/exp046 "
          f"{n_slope:+.4f}/win (mean {n_mean:.3f})")
    print(f"  credit vs drift ON the replicator substrate: {r_mean:.3f} vs {d_mean:.3f}\n")

    # loop-back confirmed: on the replicator substrate competence rises over generations AND credit
    # beats drift there AND it compounds where typed_path did not.
    compounds = r_slope > 0.002 and r_mean > d_mean and r_slope > n_slope
    if compounds:
        print("  => THE LOOP-BACK CLOSES: with part-level REPLICATORS (combinator substrate), collective")
        print("     competence compounds over generations — it rises, beats drift, and does so where the")
        print("     typed_path substrate (exp046) could not. exp047's diagnosis is confirmed from the")
        print("     other side: competence would not compound because the PARTS were not replicators;")
        print("     give the substrate replicating parts and the arc's dead end opens. The whole")
        print("     self-improvement question turns on a SUBSTRATE property (replicators), not a")
        print("     selection mechanism — the loop from exp047 back to exp012 is real.")
    else:
        print("  => THE LOOP-BACK DOES NOT CLOSE (a deeper negative): even with part-level replicators")
        print(f"     (combinator substrate), competence does not compound (slope {r_slope:+.4f}, mean")
        print(f"     {r_mean:.3f} vs drift {d_mean:.3f}, vs typed_path {n_mean:.3f}). Replicating parts are")
        print("     NOT sufficient — the irreducibly-collective nature of competence blocks compounding")
        print("     even where parts carry their own value. The limit is deeper than exp012's replicator")
        print("     lesson: a collective's competence and its parts' self-replication pull apart (the")
        print("     exp012 'replicator takeover collapses diversity' wall, now at the competence level).")


if __name__ == "__main__":
    main()
