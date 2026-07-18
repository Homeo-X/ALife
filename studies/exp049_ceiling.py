"""exp049 — COMPETENCE AS A RATE, NOT A STOCK: does reifying achieved competence raise the ceiling?

exp048 closed the self-improvement arc with the lesson that collective competence *plateaus* at a
substrate-set ceiling — the world has open-ended *novelty* (Ω-0.31) but not open-ended *competence*.
The program's answer to plateauing *novelty* was Ω-0.20: open-endedness is a **rate**, sustained only
by *continuing reification* — promoting achieved structure to new primitives keeps the construction
space growing. This experiment applies that exact lever to competence. `reify_by="closure"` promotes
the most CLOSURE-CENTRAL module (a class that repeatedly sits in demes' autocatalytic cores — achieved
*competent* structure) to a new atom every `reify_period` ticks, so each cohort of collectives builds
on the previous cohort's competent modules and the competence *ceiling* itself might climb.

Arms:
  - "reify-closure" : reify_period=400, reify_by="closure"  (exp049 — reify COMPETENT structure)
  - "reify-freq"    : reify_period=400, reify_by="frequency" (exp034 reification — reify COMMON structure)
  - "no-reify"      : reify_period=0                          (the exp048 plateau — no reification at all)

Metrics per generation-window: mean COMPETENCE (closure + breed-true heredity + breadth), mean CLOSURE,
and the constructed-alphabet size (how many atoms were reified). Headline: does reifying achieved
competence make competence RISE over generations (slope > 0) where every selection route (exp039–048)
left it flat — and does closure-reify beat frequency-reify and no-reify? Run:
  PYTHONPATH=. python3 studies/exp049_ceiling.py [ticks] [n_seeds] [memory_horizon]
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
    arm, reify_period, reify_by, seed, ticks, mem = args
    p, c = get_experiment("exp049")(seed=seed, ticks=ticks,
                                    reify_period=reify_period, reify_by=reify_by)
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
                     "closure": mean(clo) if clo else 0.0,
                     "atoms": len(p.atoms)})
    return {"arm": arm, "seed": seed, "traj": traj, "classes": u.classes_ever_seen,
            "final_atoms": len(p.atoms)}


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
    arms = [("reify-closure", 400, "closure"),
            ("reify-freq", 400, "frequency"),
            ("no-reify", 0, "closure")]
    jobs = [(a, rp, rb, s, ticks, mem) for (a, rp, rb) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "atoms")} for (a, _rp, _rb) in arms}
    classes = {a: mean(r["classes"] for r in rows if r["arm"] == a) for (a, _rp, _rb) in arms}
    atoms = {a: mean(r["final_atoms"] for r in rows if r["arm"] == a) for (a, _rp, _rb) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs, "classes": classes, "final_atoms": atoms},
              open("studies/exp049_results.json", "w"), indent=2)

    print(f"exp049 — does reifying achieved COMPETENCE raise the competence ceiling? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _rp, _rb in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>12} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>12} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>12} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        print(f"    {'atoms':>12} " + " ".join(f"{v:>6.1f}" for v in tr['atoms']))
        print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"mean {mean(tr['competence'][TRANSIENT:]):.3f}, atoms {atoms[arm]:.0f}, "
              f"classes {classes[arm]:.0f}\n")

    cc = trajs["reify-closure"]["competence"]
    fc = trajs["reify-freq"]["competence"]
    nc = trajs["no-reify"]["competence"]
    c_slope, f_slope, n_slope = _slope(cc[TRANSIENT:]), _slope(fc[TRANSIENT:]), _slope(nc[TRANSIENT:])
    c_mean, f_mean, n_mean = mean(cc[TRANSIENT:]), mean(fc[TRANSIENT:]), mean(nc[TRANSIENT:])
    print(f"  competence slope: reify-closure {c_slope:+.4f}/win (mean {c_mean:.3f}) vs "
          f"reify-freq {f_slope:+.4f}/win (mean {f_mean:.3f}) vs no-reify {n_slope:+.4f}/win (mean {n_mean:.3f})\n")

    # does reifying achieved competence make competence compound over generations?
    compounds = c_slope > 0.002 and c_slope > f_slope and c_mean >= n_mean
    if compounds:
        print("  => COMPETENCE BECOMES A RATE: reifying achieved (closure-central) competence makes")
        print("     collective competence RISE over generations — the ceiling climbs where every")
        print("     selection route (exp039–048) left it flat. The Ω-0.20 lever (open-endedness is a")
        print("     rate sustained by continuing reification) transfers from NOVELTY to COMPETENCE:")
        print("     achieved competence, fed back as new primitives, raises the ceiling itself.")
    else:
        print("  => COMPETENCE STAYS A STOCK (the honest negative): reifying achieved competence does")
        print(f"     NOT make competence compound (closure slope {c_slope:+.4f} vs freq {f_slope:+.4f} vs")
        print(f"     no-reify {n_slope:+.4f}; mean {c_mean:.3f} vs {f_mean:.3f} vs {n_mean:.3f}). The Ω-0.20")
        print("     rate-not-stock lever that keeps NOVELTY open does not transfer to COMPETENCE:")
        print("     promoting a competent module to an opaque atom moves its competence INSIDE the atom")
        print("     (out of the measured network), so the ceiling does not climb. Open-ended novelty and")
        print("     open-ended competence are genuinely different — the plateau is intrinsic to selection")
        print("     over a fixed substrate, not a missing reification. This closes the arc's open problem.")


if __name__ == "__main__":
    main()
