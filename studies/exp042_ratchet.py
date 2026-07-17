"""exp042 — a self-expanding objective: does competence finally RATCHET?

exp041 was the payoff capstone and returned an honest negative: with the collective-heredity ceiling
broken (exp040), competence *still* did not compound under a **fixed** objective — selection reaches
the bar, mutation erodes fidelity, and nothing makes the target keep rising. That is the program's
own Ω-0.20 lesson one level up: open-endedness is a **rate, not a stock**. So exp042 makes the
*objective itself* grow. `deme_fitness="ratchet"` rewards demes for BEATING a moving competence bar,
and the bar is then raised toward the achieved frontier and never lowered — goal reification (the
collective-level analogue of reifying persistent structure into new primitives). It runs *with* the
exp040 heredity channel (`network_template=0.5`) so achieved competence can be inherited.

Question: does the achieved competence **frontier** (max over demes of closure + breed-true heredity
+ normalized network breadth, `_deme_competence`) ratchet UP over generations — competence compounds
at last — or plateau (a deeper barrier: the substrate cannot accumulate the goal)?

Three matched arms, all with `network_template=0.5`:
  - "ratchet"   : deme_fitness="ratchet", ratchet_lr=0.25   (treatment — self-expanding objective)
  - "composite" : deme_fitness="composite", ratchet_lr=0.0  (exactly exp041 — the FIXED-objective control)
  - "size"      : deme_fitness="size",      ratchet_lr=0.0  (drift floor)

Metric = the per-generation-window trajectory of the competence frontier (and mean, and the moving
bar). Run:
  PYTHONPATH=. python3 studies/exp042_ratchet.py [ticks] [n_seeds] [memory_horizon]
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
SAMPLE_STRIDE = 5      # < deme_gen=20, so we average over the within-generation network build-up
TRANSIENT = 2          # windows dropped for the steady-state slope (initial-similarity washout)


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _run(args) -> dict:
    arm, fit, lr, seed, ticks, mem = args
    p, c = get_experiment("exp042")(seed=seed, ticks=ticks,
                                    deme_fitness=fit, ratchet_lr=lr, network_template=0.5)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)

    win = max(1, ticks // N_WINDOWS)
    traj = []
    prev_self = prev_null = 0
    for w in range(N_WINDOWS):
        front, meanc = [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                if act:
                    comps = [p._deme_competence(pi) for pi in act]
                    front.append(max(comps))
                    meanc.append(mean(comps))
        new_self = p._hered_edge_self[prev_self:]
        new_null = p._hered_edge_null[prev_null:]
        prev_self, prev_null = len(p._hered_edge_self), len(p._hered_edge_null)
        traj.append({
            "frontier": mean(front) if front else 0.0,
            "mean_comp": mean(meanc) if meanc else 0.0,
            "bar": p._ratchet_bar,
            "self": mean(new_self) if new_self else 0.0,
            "null": mean(new_null) if new_null else 0.0,
        })
    return {"arm": arm, "seed": seed, "traj": traj}


def _avg_traj(rows, arm):
    rs = [r for r in rows if r["arm"] == arm]
    return [{k: mean(r["traj"][w][k] for r in rs)
             for k in ("frontier", "mean_comp", "bar", "self", "null")}
            for w in range(N_WINDOWS)]


def _slope(ys):
    n = len(ys); xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    # sweep the bar chase-rate so the verdict cannot be blamed on one badly chosen lr
    arms = [
        ("ratchet@0.10", "ratchet",   0.10),
        ("ratchet@0.25", "ratchet",   0.25),
        ("ratchet@0.50", "ratchet",   0.50),
        ("composite",    "composite", 0.0),
        ("size",         "size",      0.0),
    ]
    jobs = [(a, f, lr, s, ticks, mem) for (a, f, lr) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: _avg_traj(rows, a) for (a, _f, _lr) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs},
              open("studies/exp042_results.json", "w"), indent=2)

    print(f"exp042 — does a self-expanding objective make competence RATCHET? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    print(f"  competence = closure + breed-true heredity + normalized network breadth (~[0,3])\n")

    for arm, _f, _lr in arms:
        tr = trajs[arm]
        fr = [w["frontier"] for w in tr]
        print(f"  [{arm}]")
        print(f"    {'window':>8} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'frontier':>8} " + " ".join(f"{w['frontier']:>6.2f}" for w in tr))
        print(f"    {'mean':>8} " + " ".join(f"{w['mean_comp']:>6.2f}" for w in tr))
        if arm == "ratchet":
            print(f"    {'bar':>8} " + " ".join(f"{w['bar']:>6.2f}" for w in tr))
        print(f"    frontier trend: full {_slope(fr):+.4f}/win, "
              f"steady {_slope(fr[TRANSIENT:]):+.4f}/win, "
              f"Δ(last−first) {fr[-1]-fr[0]:+.3f}")
        sm = mean(w["self"] for w in tr); nl = mean(w["null"] for w in tr) or 1e-9
        print(f"    heredity self/null = {sm:.3f}/{nl:.3f} = {sm/nl:.1f}x\n")

    # --- headline: does the frontier ratchet up under the moving objective, beating the fixed one? ---
    # take the BEST ratchet rate (highest steady-state frontier slope) so the verdict is not blamed
    # on one badly chosen lr.
    ratchet_arms = [a for (a, _f, _lr) in arms if a.startswith("ratchet")]
    ct = [w["frontier"] for w in trajs["composite"]]
    c_slope = _slope(ct[TRANSIENT:])
    best = max(ratchet_arms, key=lambda a: _slope([w["frontier"] for w in trajs[a]][TRANSIENT:]))
    rt = [w["frontier"] for w in trajs[best]]
    r_slope = _slope(rt[TRANSIENT:])
    print(f"  best ratchet rate by steady-state frontier slope: {best}")
    print(f"  frontier steady-state slope: {best} {r_slope:+.4f}/win vs fixed-composite {c_slope:+.4f}/win")
    print(f"  frontier final: {best} {rt[-1]:.3f} vs fixed-composite {ct[-1]:.3f}\n")

    ratchets = (r_slope > 0.0 and rt[-1] > ct[-1] and r_slope > c_slope)
    if ratchets:
        print("  => COMPETENCE RATCHETS: coupling the objective to achievement (raise the bar toward")
        print("     the frontier, never lower it) makes the achieved competence frontier climb over")
        print("     generations and beat the fixed-objective control. The exp041 barrier was the")
        print("     FIXED target: with a self-expanding objective (goal reification), competence")
        print("     finally compounds. Open-endedness at the collective level is a RATE, not a stock —")
        print("     the Ω-0.20 principle re-derived one level up, now for objectives.")
    else:
        print("  => DOES NOT RATCHET: even a self-expanding objective does not make the competence")
        print(f"     frontier climb over generations (ratchet steady slope {r_slope:+.4f}, vs fixed")
        print(f"     {c_slope:+.4f}). Raising the bar cannot pull competence up faster than mutation")
        print("     erodes it and the substrate re-forms it: the barrier is deeper than the objective")
        print("     — the collective cannot accumulate an open-ended goal without a representational")
        print("     faculty the substrate does not yet have (heritable, composable GOALS, not just")
        print("     heritable structure). A clean, publishable negative that names the missing piece.")


if __name__ == "__main__":
    main()
