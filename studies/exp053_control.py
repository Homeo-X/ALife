"""exp053 discriminating control — is the competence compounding a GENUINE ratchet, or mechanical
metric-padding by injecting any reactions?

The 2x2 factorial (exp053_catalytic.py) showed both catalytic cells COMPOUND. This isolates whether the
rise requires promoting genuinely COMPETENT structure (the most closure-central edge of the
HIGHEST-competence deme) or whether injecting ANY harvested reaction does it. Two arms on the Red Queen
base, both with catalytic_law on:
  - "competent" : catalyst_random=False (the real mechanism — competence-dependent harvest)
  - "random"    : catalyst_random=True  (promote a RANDOM edge from a RANDOM deme — same injection rate,
                  no competence-dependence)
If competent compounds (slope > 0) and random does NOT (or clearly less), the ratchet is real: achieved
competence, fed back as network-visible reactions, raises achievable competence. Run:
  PYTHONPATH=. python3 studies/exp053_control.py [ticks] [n_seeds] [memory_horizon]
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


def _run(args) -> dict:
    arm, rand, seed, ticks, mem = args
    p, c = get_experiment("exp053")(seed=seed, ticks=ticks, catalyst_random=rand)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    win = max(1, ticks // N_WINDOWS)
    traj = []
    for w in range(N_WINDOWS):
        comp = []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
        traj.append(mean(comp) if comp else 0.0)
    return {"arm": arm, "seed": seed, "traj": traj, "catalysts": len(p._catalysts)}


def _slope(ys):
    n = len(ys); xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    arms = [("competent", False), ("random", True)]
    jobs = [(a, r, s, ticks, mem) for (a, r) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    def avg(arm):
        rs = [r for r in rows if r["arm"] == arm]
        return [mean(r["traj"][w] for r in rs) for w in range(N_WINDOWS)]

    trajs = {a: avg(a) for (a, _r) in arms}
    ncat = {a: mean(r["catalysts"] for r in rows if r["arm"] == a) for (a, _r) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "trajectories": trajs,
               "catalysts": ncat}, open("studies/exp053_control_results.json", "w"), indent=2)

    print(f"exp053 control — genuine ratchet or mechanical injection? ({ticks} ticks, {n} seeds)\n")
    for a, _r in arms:
        t = trajs[a]
        print(f"  [{a}] " + " ".join(f"{v:>6.3f}" for v in t))
        print(f"       slope {_slope(t[TRANSIENT:]):+.4f}/win, mean {mean(t[TRANSIENT:]):.3f}, catalysts {ncat[a]:.1f}")
    cs, rs = _slope(trajs["competent"][TRANSIENT:]), _slope(trajs["random"][TRANSIENT:])
    cm, rm = mean(trajs["competent"][TRANSIENT:]), mean(trajs["random"][TRANSIENT:])
    print(f"\n  competent slope {cs:+.4f} (mean {cm:.3f}) vs random slope {rs:+.4f} (mean {rm:.3f})")
    if cs > 0.002 and cs > rs and cm > rm:
        print("  => GENUINE RATCHET: competence-dependent harvest compounds and beats random injection —")
        print("     the rise requires promoting achieved COMPETENT structure, not merely injecting reactions.")
    elif rs > 0.002:
        print("  => MECHANICAL (honest caveat): random injection compounds too — the rise is partly the ACT")
        print("     of injecting network-visible reactions, not specifically competence-dependent feedback.")
    else:
        print("  => AMBIGUOUS: neither clearly compounds at this horizon; report with caution.")


if __name__ == "__main__":
    main()
