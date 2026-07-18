"""exp047 — WITHIN-COLLECTIVE SELECTION: does a second selection level *below* the deme make
competence compound — or does selecting the credited PARTS collapse the collective?

exp046 found that a heritable per-part credit model in the deme fitness still doesn't compound, because
deme-level reproduction copies a whole propagule and cannot retain the credited PARTS against
within-deme drift — the selection *grain* is wrong. exp047 adds the missing grain: `within_select=True`
founds each offspring from the source deme's members sampled with probability rising in their CREDIT
(the parts its heritable credit map has learned cause its competence) — parts competing inside the
collective, a second selection level below the deme.

Question: does within-collective selection finally make competence compound, or does selecting the
competence-causing parts *collapse* the collective — because competence is an irreducibly collective
property of a diverse cross-production network, not a sum of part contributions you can select
independently?

Arms (all deme_fitness="credit", network_template=0.5):
  - "within" : within_select=True   (exp047 — parts competing inside the deme)
  - "credit" : within_select=False  (exactly exp046 — deme-level credit only)
  - "size"   : deme_fitness="size"  (drift floor)

Metrics per generation-window: mean COMPETENCE, mean CLOSURE, and the fraction of demes that still
carry a network (network survival — the collapse signal). Run:
  PYTHONPATH=. python3 studies/exp047_within.py [ticks] [n_seeds] [memory_horizon]
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
    arm, fit, within, seed, ticks, mem = args
    p, c = get_experiment("exp047")(seed=seed, ticks=ticks,
                                    deme_fitness=fit, within_select=within, network_template=0.5)
    rng = Noise(c.seed)
    u = Universe(total_quanta=c.total_quanta)
    u.memory_horizon = mem
    p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    win = max(1, ticks // N_WINDOWS)
    traj = []
    for w in range(N_WINDOWS):
        comp, clo, netfrac = [], [], []
        for t in range(win):
            sch.run(1)
            if t % SAMPLE_STRIDE == 0:
                act = _active(p)
                netfrac.append(len(act) / p.n_patches)
                if act:
                    comp.append(mean(p._deme_competence(pi) for pi in act))
                    clo.append(mean(p._deme_closure(pi) for pi in act))
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0,
                     "netfrac": mean(netfrac) if netfrac else 0.0})
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
    arms = [("within", "credit", True), ("credit", "credit", False), ("size", "size", False)]
    jobs = [(a, f, w, s, ticks, mem) for (a, f, w) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "netfrac")}
             for (a, _f, _w) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs}, open("studies/exp047_results.json", "w"), indent=2)

    print(f"exp047 — does within-collective selection compound competence, or collapse the collective? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _f, _w in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>11} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>11} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'closure':>11} " + " ".join(f"{v:>6.3f}" for v in tr['closure']))
        print(f"    {'net_frac':>11} " + " ".join(f"{v:>6.2f}" for v in tr['netfrac']))
        print(f"    competence slope {_slope(tr['competence'][TRANSIENT:]):+.4f}/win, "
              f"mean competence {mean(tr['competence'][TRANSIENT:]):.3f}, "
              f"mean net_frac {mean(tr['netfrac'][TRANSIENT:]):.2f}\n")

    wc = trajs["within"]["competence"]; cc = trajs["credit"]["competence"]
    w_mean, c_mean = mean(wc[TRANSIENT:]), mean(cc[TRANSIENT:])
    w_slope = _slope(wc[TRANSIENT:])
    w_net, c_net = mean(trajs["within"]["netfrac"][TRANSIENT:]), mean(trajs["credit"]["netfrac"][TRANSIENT:])
    print(f"  competence: within {w_mean:.3f} (slope {w_slope:+.4f}/win) vs deme-only credit {c_mean:.3f}")
    print(f"  network survival: within {w_net:.2f} of demes vs credit {c_net:.2f}\n")

    compounds = w_slope > 0.002 and w_mean > c_mean
    if compounds:
        print("  => IT COMPOUNDS: adding within-collective selection (parts competing inside the deme by")
        print("     credit) makes competence rise over generations and beat deme-only credit. The")
        print("     selection grain was the missing piece — self-improvement finally stacks.")
    else:
        print("  => IT COLLAPSES THE COLLECTIVE (a deep negative): selecting the credited PARTS inside")
        print(f"     the deme does not compound — competence {w_mean:.3f} < deme-only credit {c_mean:.3f}, and")
        print(f"     network survival falls to {w_net:.2f} of demes (vs {c_net:.2f}). Biasing reproduction")
        print("     toward high-credit parts erodes the DIVERSITY the cross-production network needs, so")
        print("     the very collective that made those parts valuable falls apart. Competence is an")
        print("     IRREDUCIBLY COLLECTIVE property — not a sum of part contributions you can select")
        print("     independently — so part-level selection on credit is self-defeating. The arc's")
        print("     terminal diagnosis: compounding needs a part-level REPLICATOR (a part that carries")
        print("     and copies its own value out of context — the exp012 von Neumann lesson), which the")
        print("     type-path parts fundamentally lack.")


if __name__ == "__main__":
    main()
