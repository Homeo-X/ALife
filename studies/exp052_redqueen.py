"""exp052 — THE RED QUEEN: does a coevolutionary (receding) target break the competence-flat wall?

The self-improvement arc (exp044–049) showed collective competence never compounds — it plateaus at a
substrate-set ceiling under every selection/representation/replicator/reification route. exp042 diagnosed
a common cause: selection is against a FIXED target, and its self-expanding scalar bar failed because a
single global number chasing the frontier flattens its own gradient. exp052 grounds a *receding* target
in real, LOCAL rivals — the biological driver of open-ended competence (an arms race).

`deme_fitness="redqueen"` rewards a deme for (a) its own autocatalytic CLOSURE and (b) the fraction of its
closure CORE (producers∩products) a spatial rival cannot yet produce — a zero-sum, *closure-aligned*
antagonism whose gradient does not vanish (as the rival co-acquires those classes, the deme must innovate
new closed structure). Arms:
  - "coevolve" : redqueen, LIVE rival (the bar co-adapts — the receding target).
  - "frozen"   : redqueen, coevolve_frozen=True (rival producers frozen at freeze_gen — fixed target;
                 isolates the *receding* target from the fitness form).
  - "closure"  : deme_fitness="closure" (exp038 static-competence selection — the arc's flat baseline).
  - "drift"    : deme_fitness="size" (reference).

Per generation-window: mean COMPETENCE (closure + breed-true heredity + breadth), mean CLOSURE, and
live-deme SURVIVAL (fraction of patches with a network — catches an exp047-style collapse). Headline:
does coevolve competence RISE (slope > 0) and beat frozen + closure + drift? And, more weakly, does the
receding target at least raise the competence LEVEL (coevolve > frozen)? Run:
  PYTHONPATH=. python3 studies/exp052_redqueen.py [ticks] [n_seeds] [memory_horizon]
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
SAMPLE_STRIDE = 25
TRANSIENT = 2


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _run(args) -> dict:
    arm, exp, ov, seed, ticks, mem = args
    p, c = get_experiment(exp)(seed=seed, ticks=ticks, **ov)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    win = max(1, ticks // N_WINDOWS)
    traj = []
    for w in range(N_WINDOWS):
        comp, clo, surv = [], [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                surv.append(len(act) / p.n_patches)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
                    clo.append(mean(p._deme_closure(pi) for pi in act))
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0,
                     "survival": mean(surv) if surv else 0.0})
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
    arms = [("coevolve", "exp052", {}),
            ("frozen", "exp052", {"coevolve_frozen": True}),
            ("closure", "exp049", {"reify_period": 0, "deme_fitness": "closure"}),
            ("drift", "exp049", {"reify_period": 0, "deme_fitness": "size"})]
    jobs = [(a, exp, ov, s, ticks, mem) for (a, exp, ov) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "survival")}
             for (a, _e, _o) in arms}
    classes = {a: mean(r["classes"] for r in rows if r["arm"] == a) for (a, _e, _o) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs, "classes": classes},
              open("studies/exp052_results.json", "w"), indent=2)

    print(f"exp052 — does a coevolutionary (receding) target break the competence-flat wall? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _e, _o in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>11} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>11} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>11} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        print(f"    {'survival':>11} " + " ".join(f"{v:>6.2f}" for v in tr['survival']))
        print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"mean {mean(tr['competence'][TRANSIENT:]):.3f}, classes {classes[arm]:.0f}\n")

    co = trajs["coevolve"]["competence"]
    fr = trajs["frozen"]["competence"]
    cl = trajs["closure"]["competence"]
    dr = trajs["drift"]["competence"]
    co_s = _slope(co[TRANSIENT:])
    co_m, fr_m, cl_m, dr_m = (mean(x[TRANSIENT:]) for x in (co, fr, cl, dr))
    print(f"  competence slope (coevolve): {co_s:+.4f}/win")
    print(f"  competence mean: coevolve {co_m:.3f} | frozen {fr_m:.3f} | closure {cl_m:.3f} | drift {dr_m:.3f}")
    print(f"  receding-target effect (coevolve - frozen): {co_m - fr_m:+.3f}\n")

    compounds = co_s > 0.002 and co_m > cl_m and co_m > fr_m
    if compounds:
        print("  => THE WALL BREAKS: under a receding coevolutionary target collective competence")
        print("     COMPOUNDS over generations (slope > 0) and beats the fixed-target controls (frozen,")
        print("     closure). Self-improvement needs a receding target — the arc's flat-competence wall")
        print("     was a fixed-target artifact. Next: combine with the Catalytic Law (exp053).")
    elif co_m > fr_m + 0.02:
        print("  => THE WALL HOLDS, but the receding target LIFTS THE LEVEL (not the slope): coevolve")
        print("     competence exceeds frozen (the receding target does real work) yet does not COMPOUND")
        print("     (slope ≈ 0) — the same level-not-rate pattern as exp048's replicators. Competence")
        print("     remains a STOCK: a coevolutionary target raises the plateau but not the trajectory.")
    else:
        print("  => THE WALL HOLDS (a deep negative): even a grounded, receding coevolutionary target does")
        print("     not make competence compound OR clearly exceed the fixed-target controls. The")
        print("     competence ceiling is substrate-intrinsic, not a fixed-target artifact — the strongest")
        print("     statement of the flat-competence wall the arc has reached.")


if __name__ == "__main__":
    main()
