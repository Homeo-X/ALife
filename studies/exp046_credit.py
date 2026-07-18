"""exp046 — CREDIT ASSIGNMENT IN SELECTION: does a heritable per-part contribution model, acted on by
selection, finally make competence compound?

exp045 showed that *aiming the goal* at the collective's closure core does not lift competence, because
it moves the goal's direction but not the selection pressure. exp046 puts credit into the FITNESS:
`deme_fitness="credit"` gives each deme a heritable per-class contribution map that accrues credit for
the classes in its autocatalytic closure core (the parts that cause self-maintenance) each generation,
and selection rewards demes that RETAIN their high-credit parts — so selection directly preserves
competence-causing structure, and the credit model is inherited so it accumulates down a lineage.

Question: does generic competence (closure + breed-true heredity + breadth) RISE over generations under
credit selection — the compounding the arc set out to find — beating both instantaneous closure
selection (exp038, the snapshot that traded off) and a drift floor? Or does even explicit heritable
credit fail, pointing to the selection GRAIN (deme-level selection cannot reward sub-deme parts) as the
deeper limit?

Arms (all network_template=0.5):
  - "credit"  : deme_fitness="credit"   (exp046 — heritable per-part credit in the fitness)
  - "closure" : deme_fitness="closure"  (exp038 — select on instantaneous closure)
  - "size"    : deme_fitness="size"     (drift floor)

Metrics per generation-window: mean COMPETENCE, mean CLOSURE, and heredity self/null. Run:
  PYTHONPATH=. python3 studies/exp046_credit.py [ticks] [n_seeds] [memory_horizon]
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
    arm, fit, seed, ticks, mem = args
    p, c = get_experiment("exp046")(seed=seed, ticks=ticks, deme_fitness=fit, network_template=0.5)
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
        comp, clo = [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
                    clo.append(mean(p._deme_closure(pi) for pi in act))
        new_self = p._hered_edge_self[prev_self:]
        prev_self = len(p._hered_edge_self)
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0,
                     "self": mean(new_self) if new_self else 0.0})
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
    arms = [("credit", "credit"), ("closure", "closure"), ("size", "size")]
    jobs = [(a, f, s, ticks, mem) for (a, f) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "self")}
             for (a, _f) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs}, open("studies/exp046_results.json", "w"), indent=2)

    print(f"exp046 — does heritable per-part credit in SELECTION make competence compound? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _f in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>10} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>10} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>10} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        sm = mean(tr['self']); print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
                                     f"closure slope {_slope(tr['closure'][TRANSIENT:]):+.4f}/win, "
                                     f"mean heredity self {sm:.3f}\n")

    cc = trajs["credit"]["competence"]; xc = trajs["closure"]["competence"]; sc = trajs["size"]["competence"]
    c_slope = _slope(cc[TRANSIENT:])
    c_mean, x_mean, s_mean = mean(cc[TRANSIENT:]), mean(xc[TRANSIENT:]), mean(sc[TRANSIENT:])
    print(f"  competence: credit slope {c_slope:+.4f}/win (mean {c_mean:.3f}) vs closure-select "
          f"{x_mean:.3f} vs drift {s_mean:.3f}")
    print(f"  closure (the credited axis): credit mean {mean(trajs['credit']['closure'][TRANSIENT:]):.3f} "
          f"vs closure-select {mean(trajs['closure']['closure'][TRANSIENT:]):.3f} vs drift "
          f"{mean(trajs['size']['closure'][TRANSIENT:]):.3f}\n")

    compounds = c_slope > 0.002 and c_mean > x_mean and c_mean >= s_mean - 1e-9
    if compounds:
        print("  => IT COMPOUNDS AT LAST: putting an explicit, heritable per-part credit model into the")
        print("     FITNESS — rewarding demes that retain the parts that cause their competence — makes")
        print("     generic competence RISE over generations and beat both instantaneous closure")
        print("     selection (exp038) and the drift floor. Credit assignment was a representation")
        print("     problem, and representing it in selection resolves the arc: competence compounds.")
    else:
        print("  => STILL DOES NOT COMPOUND: even an explicit, heritable per-part credit model acted on")
        print(f"     by selection does not make competence rise (credit slope {c_slope:+.4f}, mean "
              f"{c_mean:.3f} vs closure-select {x_mean:.3f}, drift {s_mean:.3f}). Rewarding retention of")
        print("     competence-causing parts is not enough — the limit is the selection GRAIN: deme-")
        print("     level reproduction copies a whole propagule, so it cannot preferentially keep the")
        print("     high-credit *parts* against within-deme drift. The frontier moves to WITHIN-")
        print("     collective selection (parts competing inside the deme), the last rung of the arc.")


if __name__ == "__main__":
    main()
