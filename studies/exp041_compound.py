"""exp041 — the PAYOFF capstone: does competence COMPOUND once the heredity ceiling is broken?

The self-improvement arc found the machinery for mind-like collectives is present (exp037 evolvable
per-collective state; exp038 selectable emergent coherence) but that **competence could not compound**
because collective heredity was too weak (exp039: even the aligned closure-AND-heredity maximin left
heredity pinned at the exp028 ceiling, so a multi-property phenotype could not stack). exp040 then
**broke that ceiling**: developmental (network-template) niche inheritance lifted collective heredity
to 8-9x null while a *partial* template kept the world open.

This runs the two together and asks the payoff question: with a strong heredity channel now
available, does the composite objective make **closure AND heredity AND function rise together over
generations** — competence compounds — or does single-scalar selection still trade them off?

Three matched arms (all with `measure_xprod=True`, a pure gauge that consumes no RNG so it cannot
perturb dynamics — see exp012 line ~967):
  - "composite+template" : deme_fitness="composite", network_template=0.5   (treatment)
  - "composite"          : deme_fitness="composite", network_template=0.0   (exactly exp039 — the
                            control that isolates the developmental channel)
  - "size+template"      : deme_fitness="size",      network_template=0.5   (drift — isolates
                            selection from the template)

Metric = a TRAJECTORY (the difference from exp039's endpoint means): the run is binned into
generation-windows; per window we record mean **closure** (`_deme_closure`), **heredity** (mean of
the NEW `_hered_edge_self` vs `_hered_edge_null` entries in that window — a per-window rate, not a
cumulative average), and a **function** proxy (per-deme cross-production `_xprod`). We then test
whether the weakest of the three axes trends UP over generations under the treatment and beats the
composite-only control. Run:
  PYTHONPATH=. python3 studies/exp041_compound.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

N_WINDOWS = 8          # generation-windows across the run
SAMPLE_STRIDE = 5      # ticks between closure/function snapshots (< deme_gen=20, so we average
                       # OVER the deme-generation phase instead of aliasing it — the within-
                       # generation network build-up (_deme_edges/_xprod reset every generation)
TRANSIENT = 2          # windows to drop for the steady-state slope (initial-similarity washout)


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _run(args) -> dict:
    arm, fit, template, seed, ticks, mem = args
    p, c = get_experiment("exp041")(seed=seed, ticks=ticks,
                                     deme_fitness=fit, network_template=template,
                                     measure_xprod=True)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem                    # bound memory over the long horizon (0 => off)
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)

    win = max(1, ticks // N_WINDOWS)
    traj = []                                 # per-window (closure, self, null, function)
    prev_self = prev_null = 0                  # cumulative-list lengths at last window boundary
    for w in range(N_WINDOWS):
        clos, func = [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                if act:
                    clos.append(mean(p._deme_closure(pi) for pi in act))
                    # function = network breadth: distinct cross-production edges the collective
                    # builds (raw constructive output, distinct from closure's ratio and heredity's
                    # cross-generation similarity). Averaged over dense in-generation samples.
                    func.append(mean(len(p._deme_edges.get(pi, ())) for pi in act))
        # per-window heredity rate = mean of the entries appended DURING this window (measured AT
        # reproduction events, so — unlike closure/function — it is phase-correct by construction)
        new_self = p._hered_edge_self[prev_self:]
        new_null = p._hered_edge_null[prev_null:]
        prev_self, prev_null = len(p._hered_edge_self), len(p._hered_edge_null)
        traj.append({
            "closure": mean(clos) if clos else 0.0,
            "self": mean(new_self) if new_self else 0.0,
            "null": mean(new_null) if new_null else 0.0,
            "function": mean(func) if func else 0.0,
        })
    return {"arm": arm, "seed": seed, "traj": traj}


def _avg_traj(rows, arm):
    rs = [r for r in rows if r["arm"] == arm]
    out = []
    for w in range(N_WINDOWS):
        out.append({k: mean(r["traj"][w][k] for r in rs)
                    for k in ("closure", "self", "null", "function")})
    return out


def _slope(ys):
    """least-squares slope over evenly spaced windows (sign = rising/falling)."""
    n = len(ys)
    xs = list(range(n))
    mx, my = mean(xs), mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom if denom else 0.0


def _norm_min_traj(traj):
    """weakest-axis competence per window: min over the three axes, each normalized to its own
    max across the run so the axes are comparable (closure~[0,1], heredity self, function counts)."""
    cmax = max(w["closure"] for w in traj) or 1.0
    smax = max(w["self"] for w in traj) or 1.0
    fmax = max(w["function"] for w in traj) or 1.0
    return [min(w["closure"] / cmax, w["self"] / smax, w["function"] / fmax) for w in traj]


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000   # memory_horizon for the long run
    arms = [
        ("composite+template", "composite", 0.5),
        ("composite",          "composite", 0.0),
        ("size+template",      "size",      0.5),
    ]
    jobs = [(a, f, tpl, s, ticks, mem) for (a, f, tpl) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: _avg_traj(rows, a) for (a, _f, _t) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs},
              open("studies/exp041_results.json", "w"), indent=2)

    print(f"exp041 — does competence compound once the heredity ceiling is broken? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")

    for arm, _f, _t in arms:
        tr = trajs[arm]
        c0, c1 = tr[0]["closure"], tr[-1]["closure"]
        s0, s1 = tr[0]["self"], tr[-1]["self"]
        f0, f1 = tr[0]["function"], tr[-1]["function"]
        nl = mean(w["null"] for w in tr) or 1e-9
        sm = mean(w["self"] for w in tr)
        print(f"  [{arm}]")
        print(f"    {'window':>7} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'closure':>7} " + " ".join(f"{w['closure']:>6.3f}" for w in tr))
        print(f"    {'hered':>7} " + " ".join(f"{w['self']:>6.3f}" for w in tr))
        print(f"    {'funcxn':>7} " + " ".join(f"{w['function']:>6.2f}" for w in tr))
        print(f"    trend: closure {_slope([w['closure'] for w in tr]):+.4f}/win, "
              f"heredity {_slope([w['self'] for w in tr]):+.4f}/win, "
              f"function {_slope([w['function'] for w in tr]):+.3f}/win")
        print(f"    mean heredity self/null = {sm:.3f}/{nl:.3f} = {sm/nl:.1f}x\n")

    # --- the headline: do the three axes rise TOGETHER (compound) or trade off? ---
    # Per-axis *relative* slope (slope / mean) makes closure/heredity/function comparable despite
    # different units. An axis is "declining" if its relative slope is below -TOL (a real trade-off,
    # not noise). Compounding = no axis declines AND the weakest-axis (normalized-min) trajectory
    # rises and ends at least level with the composite-only control.
    TOL = 0.02

    def rel_slopes(tr, lo=0):
        # relative slope (slope / mean) over windows [lo:], so closure/heredity/function compare
        out = {}
        for k in ("closure", "self", "function"):
            ys = [w[k] for w in tr][lo:]
            m = mean(ys) or 1e-9
            out[k] = _slope(ys) / m
        return out

    def decliners(rel):
        return [k for k, v in rel.items() if v < -TOL]

    # steady state drops the initial-similarity transient (all arms start highly similar and relax)
    t_rel, c_rel = rel_slopes(trajs["composite+template"], TRANSIENT), rel_slopes(trajs["composite"], TRANSIENT)
    t_rel_full, c_rel_full = rel_slopes(trajs["composite+template"]), rel_slopes(trajs["composite"])
    tmin = _norm_min_traj(trajs["composite+template"])
    cmin = _norm_min_traj(trajs["composite"])
    t_min_slope, c_min_slope = _slope(tmin[TRANSIENT:]), _slope(cmin[TRANSIENT:])
    t_her = mean(w["self"] for w in trajs["composite+template"])
    c_her = mean(w["self"] for w in trajs["composite"])
    nl = mean(w["null"] for w in trajs["composite+template"]) or 1e-9

    print(f"  per-axis relative slope (fractional change / window; < -{TOL:.0%} = trade-off):")
    print(f"    {'axis':>9}  {'treatment(full/steady)':>24}  {'control(full/steady)':>24}")
    for k in ("closure", "self", "function"):
        print(f"    {k:>9}  {t_rel_full[k]:>+10.1%} /{t_rel[k]:>+9.1%}   "
              f"{c_rel_full[k]:>+10.1%} /{c_rel[k]:>+9.1%}")
    print(f"\n  weakest-axis (normalized min of the three) steady-state trajectory:")
    print(f"    composite+template : slope {t_min_slope:+.4f}/win, final {tmin[-1]:.3f}")
    print(f"    composite (control): slope {c_min_slope:+.4f}/win, final {cmin[-1]:.3f}")
    t_dec, c_dec = decliners(t_rel), decliners(c_rel)
    print(f"    steady-state declining axis(es): treatment {t_dec or 'none'} vs control {c_dec or 'none'}")
    print(f"\n  collective-heredity LEVEL (the exp040 channel): treatment self {t_her:.3f} vs control "
          f"{c_her:.3f} (null {nl:.3f}) — template {t_her/c_her:.1f}x the control, {t_her/nl:.1f}x null\n")

    compounds = (not t_dec) and t_min_slope > 0 and tmin[-1] >= cmin[-1] - 1e-9
    if compounds:
        print("  => COMPETENCE COMPOUNDS: with the developmental channel ON, none of closure,")
        print("     heredity, or function declines over generations and the weakest axis rises,")
        print(f"     ending level-or-above the composite-only control (which trades off: {c_dec}).")
        print("     Aligned multi-objective selection now makes the three accumulate TOGETHER —")
        print("     self-improvement in this substrate is selection-limited, not substrate-limited.")
        print("     The collective-heredity ceiling was the gate; exp040 opened it, and here the")
        print("     capstone objective finally stacks competence instead of trading it away.")
    else:
        print("  => DOES NOT COMPOUND. The developmental channel does its job on the LEVEL axis —")
        print(f"     it raises collective heredity to {t_her/nl:.1f}x null ({t_her/c_her:.1f}x the composite-only")
        print("     control), re-confirming exp040 — but a HIGHER heredity level is not enough:")
        print(f"     over generations the three axes still do not rise together (treatment declining")
        print(f"     axis: {t_dec or 'none'}; weakest-axis slope {t_min_slope:+.4f}). Competence does not")
        print("     accumulate. So the barrier to self-improvement is NOT (only) heredity fidelity,")
        print("     which exp040 fixed — there is a SEPARATE compounding barrier: single-scalar")
        print("     selection over a fixed objective cannot make closure, heredity, and construction")
        print("     grow jointly across generations. The located blocker moves from 'weak heredity'")
        print("     to 'no open-ended objective' — the substrate can now transmit competence but has")
        print("     nothing that makes the target itself keep expanding (an open-ended-selection gap).")


if __name__ == "__main__":
    main()
