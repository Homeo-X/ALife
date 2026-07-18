"""exp044 — THE FRONTIER: do heritable, composable GOALS make competence ratchet at last?

The self-improvement arc ended (exp042) with competence still not compounding even under a
self-expanding objective, diagnosed as a **goal-representation** barrier: the substrate can reify
structure but has no heritable, composable representation of a *goal* to reify, and a scalar moving
bar flattens its own selection gradient. exp044 gives collectives that faculty — each deme carries a
heritable target PATH (an object of the substrate's own kind: heritable, mutable via `_mutate_path`,
composable via path concatenation), is selected on how well it CONSTRUCTS that target (achievement ×
depth), and, when it robustly achieves, has the target EXTENDED (goal reification). Runs with the
exp040 heredity channel so achieved goals are inherited.

The decisive question: does **achieved goal DEPTH ratchet up over generations** — competence
compounds at last — or plateau (a deeper barrier still: credit assignment)?

Arms (all `network_template=0.5`):
  - "goals+reify" : deme_fitness="goal", goal_reify=True   (treatment — composable goals)
  - "goals-fixed" : deme_fitness="goal", goal_reify=False  (control isolating COMPOSABILITY: goals
                     inherited & selected on, but never extended — depth pinned at 2)
  - "ratchet"     : deme_fitness="ratchet"                 (exp042 scalar self-expanding bar — failed)
  - "size"        : deme_fitness="size"                    (drift floor)

Metrics per generation-window: mean GOAL DEPTH (goal arms — the direct ratchet signal) and the
exp042 competence composite (`_deme_competence`, all arms — does goal-directed construction compound
competence where exp041/042 did not?). Run:
  PYTHONPATH=. python3 studies/exp044_goals.py [ticks] [n_seeds] [memory_horizon]
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
    arm, fit, reify, seed, ticks, mem = args
    p, c = get_experiment("exp044")(seed=seed, ticks=ticks,
                                    deme_fitness=fit, goal_reify=reify, network_template=0.5)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)

    win = max(1, ticks // N_WINDOWS)
    traj = []
    prev_self = 0
    for w in range(N_WINDOWS):
        depth, comp = [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                depth.append(_goal_depth(p))
                act = _active(p)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
        new_self = p._hered_edge_self[prev_self:]
        prev_self = len(p._hered_edge_self)
        traj.append({
            "goal_depth": mean(depth) if depth else 0.0,
            "competence": mean(comp) if comp else 0.0,
            "self": mean(new_self) if new_self else 0.0,
        })
    return {"arm": arm, "seed": seed, "traj": traj,
            "max_goal_depth": max((len(_path_nodes(g)) for g in p._deme_goal.values()), default=0)}


def _avg(rows, arm, key):
    rs = [r for r in rows if r["arm"] == arm]
    return [mean(r["traj"][w][key] for r in rs) for w in range(N_WINDOWS)]


def _slope(ys):
    n = len(ys); xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    arms = [
        ("goals+reify", "goal", True),
        ("goals-fixed", "goal", False),
        ("ratchet", "ratchet", False),
        ("size", "size", False),
    ]
    jobs = [(a, f, r, s, ticks, mem) for (a, f, r) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("goal_depth", "competence", "self")}
             for (a, _f, _r) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs,
               "max_goal_depth": {a: max(r["max_goal_depth"] for r in rows if r["arm"] == a)
                                  for (a, _f, _r) in arms}},
              open("studies/exp044_results.json", "w"), indent=2)

    print(f"exp044 — do heritable, composable GOALS make competence ratchet? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    print(f"  competence = closure + breed-true heredity + normalized breadth (~[0,3])\n")
    for arm, _f, _r in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>10} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        if arm.startswith("goals"):
            print(f"    {'goal_depth':>10} " + " ".join(f"{v:>6.2f}" for v in tr['goal_depth']))
        print(f"    {'competence':>10} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        gd = tr['goal_depth']
        print(f"    goal-depth steady slope {_slope(gd[TRANSIENT:]):+.4f}/win  "
              f"competence steady slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win  "
              f"max depth {max(r['max_goal_depth'] for r in rows if r['arm']==arm)}\n")

    # --- claim 1 (the frontier faculty): does GOAL DEPTH ratchet under composability vs fixed? ---
    gr = trajs["goals+reify"]["goal_depth"]
    gf = trajs["goals-fixed"]["goal_depth"]
    gr_slope, gf_slope = _slope(gr[TRANSIENT:]), _slope(gf[TRANSIENT:])
    faculty = gr_slope > 0.01 and gr[-1] > gf[-1] + 0.2
    print(f"  (1) achieved GOAL DEPTH ratchet: composable {gr[0]:.2f}->{gr[-1]:.2f} "
          f"(slope {gr_slope:+.4f}/win) vs fixed {gf[0]:.2f}->{gf[-1]:.2f} (slope {gf_slope:+.4f}/win) "
          f"=> {'RATCHETS' if faculty else 'flat'}")
    # --- claim 2 (does it generalize): does the goal ratchet also lift GENERIC competence? ---
    cr = trajs["goals+reify"]["competence"]
    cr_slope = _slope(cr[TRANSIENT:])
    others = {a: mean(trajs[a]["competence"][TRANSIENT:]) for a in ("goals-fixed", "ratchet", "size")}
    cr_mean = mean(cr[TRANSIENT:])
    generalizes = cr_slope >= -0.005 and cr_mean >= max(others.values()) - 1e-9
    print(f"  (2) does it lift GENERIC competence? composable slope {cr_slope:+.4f}/win, mean "
          f"{cr_mean:.3f} vs fixed {others['goals-fixed']:.3f} / ratchet {others['ratchet']:.3f} / "
          f"size {others['size']:.3f} => {'yes' if generalizes else 'no (narrow)'}\n")

    if faculty and generalizes:
        print("  => THE ARC'S PAYOFF: heritable, composable goals make competence ratchet — achieved")
        print("     goal depth climbs over generations AND generic competence rises with it. Given a")
        print("     goal the substrate can represent, inherit, and COMPOSE, open-ended self-improvement")
        print("     finally stacks. exp042's diagnosis is confirmed from the other side: the missing")
        print("     piece WAS goal representation.")
    elif faculty:
        print("  => THE FACULTY WORKS, BUT NARROWLY (a partial positive — the first compounding in the")
        print("     whole arc). Heritable, composable goals produce a genuine over-generations RATCHET")
        print("     in the represented dimension: achieved goal depth climbs (composable ≫ fixed),")
        print("     where exp041/042 could not make anything compound. So goal representation WAS a")
        print("     real missing piece — given it, the collective accumulates deeper achievements. BUT")
        print("     the ratchet is *specialized*: chasing a deeper idiosyncratic target does not lift")
        print("     GENERIC competence (closure/heredity/breadth). The next rung is to ALIGN the goal")
        print("     with self-maintenance — a credit-assignment / goal-alignment problem — so the")
        print("     represented ratchet also generalizes. The arc advances from 'no compounding' to")
        print("     'compounding, but narrow'.")
    else:
        print("  => DOES NOT RATCHET: even heritable, composable goals do not make achieved depth")
        print(f"     climb (composable slope {gr_slope:+.4f} vs fixed {gf_slope:+.4f}). The collective")
        print("     builds toward a target but cannot tell WHICH of its parts caused achievement, so it")
        print("     cannot direct construction to extend the pathway — the barrier past goal")
        print("     representation is CREDIT ASSIGNMENT, the ROADMAP-predicted third redirection.")


if __name__ == "__main__":
    main()
