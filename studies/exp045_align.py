"""exp045 — GOAL ALIGNMENT / credit assignment: does aiming goal growth at the collective's own
competence make competence rise WITH goal depth?

exp044 gave collectives heritable, composable goals and got the arc's first over-generations
*deepening* — but the ratchet was transient and did NOT lift generic competence: goals grew toward an
*arbitrary* achievable path (the most-produced atom), so chasing a deeper target cannibalised
self-maintenance instead of reinforcing it. The diagnosis: the collective cannot attribute its
competence to its parts (credit assignment). exp045 tests the fix — `goal_align=True` aims goal
reification at the deme's **autocatalytic closure core** (classes that are both producers AND products,
the self-maintaining loop that *is* its competence), so growing/pursuing the goal reinforces closure.

Question: does the now-aligned goal ratchet make **generic competence rise with goal depth** — the
compounding the arc set out to find — or does it still fail (a deeper representational limit: the
substrate can't credit-assign even when handed its own closure set)?

Arms (all deme_fitness="goal", goal_reify=True, network_template=0.5):
  - "aligned"   : goal_align=True   (exp045 — extend the goal toward the closure core)
  - "unaligned" : goal_align=False  (exactly exp044 — extend toward the most-produced atom)
  - "size"      : deme_fitness="size" drift floor

Metrics per generation-window: mean COMPETENCE (`_deme_competence` = closure + breed-true heredity +
breadth — the thing we want to rise), mean CLOSURE (the axis alignment targets), and mean GOAL DEPTH.
Run:
  PYTHONPATH=. python3 studies/exp045_align.py [ticks] [n_seeds] [memory_horizon]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.experiments.exp012_combinator import _path_nodes
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

N_WINDOWS = 8
SAMPLE_STRIDE = 5
TRANSIENT = 2


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _goal_depth(p):
    ds = [len(_path_nodes(g)) for g in p._deme_goal.values()]
    return mean(ds) if ds else 0.0


def _run(args) -> dict:
    arm, fit, align, seed, ticks, mem = args
    p, c = get_experiment("exp045")(seed=seed, ticks=ticks,
                                    deme_fitness=fit, goal_align=align, network_template=0.5)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    win = max(1, ticks // N_WINDOWS)
    traj = []
    for w in range(N_WINDOWS):
        comp, clo, depth = [], [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                depth.append(_goal_depth(p))
                act = _active(p)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
                    clo.append(mean(p._deme_closure(pi) for pi in act))
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0,
                     "goal_depth": mean(depth) if depth else 0.0})
    return {"arm": arm, "seed": seed, "traj": traj}


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
    arms = [("aligned", "goal", True), ("unaligned", "goal", False), ("size", "size", False)]
    jobs = [(a, f, al, s, ticks, mem) for (a, f, al) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "goal_depth")}
             for (a, _f, _al) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs}, open("studies/exp045_results.json", "w"), indent=2)

    print(f"exp045 — does aiming goals at the closure core make competence rise WITH goal depth? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _f, _al in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>10} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>10} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>10} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        if arm != "size":
            print(f"    {'goal_depth':>10} " + " ".join(f"{v:>6.2f}" for v in tr['goal_depth']))
        print(f"    steady slopes: competence {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"closure {_slope(tr['closure'][TRANSIENT:]):+.4f}/win, "
              f"goal_depth {_slope(tr['goal_depth'][TRANSIENT:]):+.4f}/win\n")

    ac = trajs["aligned"]["competence"]; uc = trajs["unaligned"]["competence"]
    acl = trajs["aligned"]["closure"]; ucl = trajs["unaligned"]["closure"]
    a_slope = _slope(ac[TRANSIENT:]); u_slope = _slope(uc[TRANSIENT:])
    a_cl_slope = _slope(acl[TRANSIENT:])
    a_mean, u_mean = mean(ac[TRANSIENT:]), mean(uc[TRANSIENT:])
    drift_mean = mean(trajs["size"]["competence"][TRANSIENT:])
    print(f"  competence: aligned slope {a_slope:+.4f}/win (mean {a_mean:.3f}) vs unaligned slope "
          f"{u_slope:+.4f}/win (mean {u_mean:.3f}); drift mean {drift_mean:.3f}")
    print(f"  closure (the aligned axis): aligned slope {a_cl_slope:+.4f}/win, "
          f"aligned closure mean {mean(acl[TRANSIENT:]):.3f} vs unaligned {mean(ucl[TRANSIENT:]):.3f}\n")

    # success: alignment makes competence rise over generations AND beat the unaligned control AND
    # clear the drift floor — the compounding the arc set out to find.
    compounds = a_slope > 0.002 and a_mean > u_mean and a_mean >= drift_mean - 1e-9
    if compounds:
        print("  => IT COMPOUNDS: aiming goal growth at the deme's own closure core (credit assignment)")
        print("     makes generic competence rise over generations and beat both the unaligned goal")
        print("     ratchet (exp044) and the drift floor. Competence and goal depth climb TOGETHER —")
        print("     the compounding the whole arc was built toward. The missing piece past goal")
        print("     representation was goal↔competence ALIGNMENT, and a closure-core target supplies it.")
    else:
        print("  => STILL DOES NOT COMPOUND: even aiming the goal at the deme's own closure core does")
        print(f"     not make generic competence rise (aligned slope {a_slope:+.4f}, mean {a_mean:.3f} "
              f"vs unaligned {u_mean:.3f}, drift {drift_mean:.3f}).")
        print("     Handing the collective its own closure set is not enough to credit-assign: it")
        print("     cannot sustain building toward a competence-defined target any better than an")
        print("     arbitrary one. The barrier is a deeper representational limit — the substrate has")
        print("     no persistent, inheritable model of WHICH parts cause competence, only the goal")
        print("     path itself. A clean negative that pushes the frontier from 'aim the goal' to")
        print("     'represent the credit' (an explicit per-part contribution the collective inherits).")


if __name__ == "__main__":
    main()
