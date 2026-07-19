"""exp053 — THE CATALYTIC LAW × THE RED QUEEN: a 2×2 factorial for stock-vs-rate.

Seven experiments (exp044–052) moved the competence LEVEL but never the SLOPE — every lever selects
against a FIXED substrate law. exp049 named the one untried move and diagnosed why its own attempt failed:
reifying a competent module to a NEW ATOM hides its structure in an opaque primitive, out of the measured
network. `catalytic_law` does it as a REACTION instead — every catalyst_period ticks it promotes the most
closure-central production of the highest-competence deme to a persistent shared catalyst (anchor_cls →
product_state), injected every tick, so competent structure becomes a reusable, NETWORK-VISIBLE
construction operation later collectives build closures on top of. This crosses that new axis against the
target axis (fixed closure vs receding Red Queen) in a 2×2 factorial:

  cell                    deme_fitness  catalytic_law   status
  fixed-law × closure     closure       off             have data (flat plateau)
  fixed-law × redqueen    redqueen      off             have data (exp052: highest plateau, flat)
  catalytic × closure     closure       on              NEW — law-feedback alone
  catalytic × redqueen    redqueen      on              NEW — the combination (best shot at a rising ceiling)

Per generation-window: mean COMPETENCE (closure + breed-true + breadth), CLOSURE, live-deme SURVIVAL
(collapse guard), and catalyst count. Headline: does competence COMPOUND (slope > 0) in the
catalytic+redqueen cell, beating the three fixed-law/flat cells? Which ingredient does it? Run:
  PYTHONPATH=. python3 studies/exp053_catalytic.py [ticks] [n_seeds] [memory_horizon]
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
    arm, fit, catalytic, seed, ticks, mem = args
    p, c = get_experiment("exp053")(seed=seed, ticks=ticks,
                                    deme_fitness=fit, catalytic_law=catalytic)
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
    return {"arm": arm, "seed": seed, "traj": traj,
            "classes": u.classes_ever_seen, "catalysts": len(p._catalysts)}


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
    # (arm, deme_fitness, catalytic_law)
    arms = [("cat+redqueen", "redqueen", True),
            ("cat+closure", "closure", True),
            ("redqueen", "redqueen", False),
            ("closure", "closure", False)]
    jobs = [(a, f, cat, s, ticks, mem) for (a, f, cat) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "survival")}
             for (a, _f, _c) in arms}
    classes = {a: mean(r["classes"] for r in rows if r["arm"] == a) for (a, _f, _c) in arms}
    ncat = {a: mean(r["catalysts"] for r in rows if r["arm"] == a) for (a, _f, _c) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs, "classes": classes, "catalysts": ncat},
              open("studies/exp053_results.json", "w"), indent=2)

    print(f"exp053 — Catalytic Law × Red Queen: does competence finally COMPOUND? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _f, _c in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>11} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>11} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>11} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        print(f"    {'survival':>11} " + " ".join(f"{v:>6.2f}" for v in tr['survival']))
        print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"mean {mean(tr['competence'][TRANSIENT:]):.3f}, catalysts {ncat[arm]:.1f}, classes {classes[arm]:.0f}\n")

    def sl(a):
        return _slope(trajs[a]["competence"][TRANSIENT:])

    def mn(a):
        return mean(trajs[a]["competence"][TRANSIENT:])

    cr, cc, rq, cl = "cat+redqueen", "cat+closure", "redqueen", "closure"
    print(f"  competence slope: {cr} {sl(cr):+.4f} | {cc} {sl(cc):+.4f} | {rq} {sl(rq):+.4f} | {cl} {sl(cl):+.4f}")
    print(f"  competence mean:  {cr} {mn(cr):.3f} | {cc} {mn(cc):.3f} | {rq} {mn(rq):.3f} | {cl} {mn(cl):.3f}")
    print(f"  catalytic-law level lift: (cat+redqueen − redqueen) {mn(cr) - mn(rq):+.3f}, "
          f"(cat+closure − closure) {mn(cc) - mn(cl):+.3f}\n")

    # a catalytic cell "compounds" if it has a positive slope AND beats its fixed-law counterpart on slope.
    combo_compounds = sl(cr) > 0.002 and sl(cr) > sl(rq) and mn(cr) >= mn(rq)
    catclo_compounds = sl(cc) > 0.002 and sl(cc) > sl(cl) and mn(cc) >= mn(cl)
    if combo_compounds and mn(cr) >= mn(cc):
        print("  => THE WALL BREAKS: competence COMPOUNDS in the catalytic+Red-Queen cell (slope > 0, above")
        print("     its no-law control) at the arc's highest level. A substrate-law feedback that keeps")
        print("     competent structure NETWORK-VISIBLE (a reaction, not an opaque atom) turns achieved")
        print("     competence into higher achievable competence — the arc's first rising ceiling. The")
        print("     receding target supplies the pressure; the Catalytic Law supplies the ratchet.")
    elif combo_compounds or catclo_compounds:
        print("  => THE CATALYTIC LAW TILTS THE SLOPE: at least one catalytic cell compounds (slope > 0,")
        print("     above its fixed-law control) — the network-visible substrate-law feedback is the first")
        print("     lever in the arc to make competence a RATE, not just a higher stock. Which target it")
        print("     needs (closure vs Red Queen) is read from the per-cell slopes above.")
    else:
        print("  => THE WALL HOLDS (deepest negative, arc-closing): even a receding target PLUS a")
        print("     network-visible substrate-law feedback does not make competence compound (catalytic")
        print("     slopes ≈ 0). The competence ceiling is SUBSTRATE-INTRINSIC — no reaction-repertoire")
        print("     growth turns achieved competence into higher achievable competence. Open-ended novelty")
        print("     ≠ open-ended competence is closed at its strongest. (A level lift is not a rate.)")


if __name__ == "__main__":
    main()
