"""exp054 — THE EARNED LAW: does gradually EARNING a deeper construction law sustain the competence rise
where exp053's bounded Catalytic Law saturates — and reach regimes a COLD high-resolution start cannot?

exp053 (Ω-0.42) broke the competence-flat wall but SATURATES (~1.45 by ~8k ticks) — and it is NOT the
catalyst cap (cap16/80/400 are byte-identical, only ~10 distinct closure-core edges ever qualify): at
fixed resolution the constructible space is finite, so competent structure exhausts. Deeper construction
(higher type_resolution → longer type-paths → a larger competent-structure space) helps FROM A COLD START
up to ~res5, but res8 cold-starts COLLAPSE (the length-8 path space is too sparse for cross-production).
exp054 grows the composition law itself: `earned_law` lets a competent LINEAGE climb resolution by +1 at
BIRTH (per deme, fixed for life — no destructive mid-life re-classification) iff it achieved enough
closure at its current reach. Hypothesis: earning your way up **gradually** reaches deep regimes a cold
start cannot, extending the compounding rise.

Arms (all on the exp052 Red Queen base):
  - "earned"     : exp054 earned_law — resolution climbs with achieved closure, per lineage, at birth.
  - "fixed-high" : type_resolution=8 from the START (cold max reach — the decisive control: does EARNING
                   matter, or just being deep? cold res8 collapses in the diagnostic).
  - "catalytic"  : exp053 (the bounded reaction-repertoire law that saturates).
  - "fixed-law"  : exp052 res3 (the baseline plateau).

Per generation-window: mean COMPETENCE, CLOSURE, live-deme SURVIVAL, mean earned REACH. Headline: does
earned competence keep a NON-DECAYING slope (vs catalytic's saturation) AND stay alive where fixed-high
(cold res8) collapses? Long horizon (saturation is the question). Run:
  PYTHONPATH=. python3 studies/exp054_earned.py [ticks] [n_seeds] [memory_horizon]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

N_WINDOWS = 10
SAMPLE_STRIDE = 25
TRANSIENT = 2


def _active(p):
    return [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]


def _run(args) -> dict:
    arm, exp, ov, seed, ticks, mem = args
    p, c = get_experiment(exp)(seed=seed, ticks=ticks, **ov)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); u.memory_horizon = mem
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
        reach = mean(p._deme_reach.values()) if getattr(p, "_deme_reach", None) else 0.0
        traj.append({"competence": mean(comp) if comp else 0.0,
                     "closure": mean(clo) if clo else 0.0,
                     "survival": mean(surv) if surv else 0.0, "reach": reach})
    return {"arm": arm, "seed": seed, "traj": traj, "classes": u.classes_ever_seen}


def _avg(rows, arm, key):
    rs = [r for r in rows if r["arm"] == arm]
    return [mean(r["traj"][w][key] for r in rs) for w in range(N_WINDOWS)]


def _slope(ys):
    n = len(ys); xs = list(range(n)); mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    mem = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    arms = [("earned", "exp054", {}),
            ("fixed-high", "exp052", {"type_resolution": 8}),
            ("catalytic", "exp053", {}),
            ("fixed-law", "exp052", {})]
    jobs = [(a, e, ov, s, ticks, mem) for (a, e, ov) in arms for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    trajs = {a: {k: _avg(rows, a, k) for k in ("competence", "closure", "survival", "reach")}
             for (a, _e, _o) in arms}
    classes = {a: mean(r["classes"] for r in rows if r["arm"] == a) for (a, _e, _o) in arms}
    json.dump({"ticks": ticks, "n_seeds": n, "memory_horizon": mem, "n_windows": N_WINDOWS,
               "trajectories": trajs, "classes": classes},
              open("studies/exp054_results.json", "w"), indent=2)

    print(f"exp054 — does an EARNED (expanding) law sustain the competence rise past exp053's saturation? "
          f"({ticks} ticks, {n} seeds, {N_WINDOWS} windows, mem={mem})\n")
    for arm, _e, _o in arms:
        tr = trajs[arm]
        print(f"  [{arm}]")
        print(f"    {'window':>11} " + " ".join(f"{w:>6}" for w in range(N_WINDOWS)))
        print(f"    {'competence':>11} " + " ".join(f"{v:>6.3f}" for v in tr['competence']))
        print(f"    {'survival':>11} " + " ".join(f"{v:>6.2f}" for v in tr['survival']))
        print(f"    {'reach':>11} " + " ".join(f"{v:>6.2f}" for v in tr['reach']))
        print(f"    late-half slope {_slope(tr['competence'][N_WINDOWS // 2:]):+.4f}/win, "
              f"mean(post-transient) {mean(tr['competence'][TRANSIENT:]):.3f}, "
              f"end-survival {tr['survival'][-1]:.2f}\n")

    def late(a):
        return _slope(trajs[a]["competence"][N_WINDOWS // 2:])

    def mn(a):
        return mean(trajs[a]["competence"][TRANSIENT:])

    print(f"  late-half competence slope: earned {late('earned'):+.4f} | catalytic {late('catalytic'):+.4f} "
          f"| fixed-high {late('fixed-high'):+.4f} | fixed-law {late('fixed-law'):+.4f}")
    print(f"  earned end-survival {trajs['earned']['survival'][-1]:.2f} vs fixed-high (cold res8) "
          f"{trajs['fixed-high']['survival'][-1]:.2f}; earned max reach {max(trajs['earned']['reach']):.2f}\n")

    earned_sustains = late("earned") > 0.002 and late("earned") > late("catalytic")
    earned_reaches = trajs["earned"]["survival"][-1] > 2 * max(trajs["fixed-high"]["survival"][-1], 1e-9)
    if earned_sustains and earned_reaches:
        print("  => THE EARNED LAW EXTENDS THE RISE: competence keeps a non-decaying slope where the")
        print("     bounded Catalytic Law SATURATES, and the earned lineage stays ALIVE at a deep")
        print("     construction regime where a COLD high-resolution start (fixed-high) collapses. Earning")
        print("     your way up — gradual, competence-gated law expansion — reaches regimes cold-start")
        print("     cannot, and pushes the competence ceiling toward the substrate's max viable depth.")
    elif earned_reaches:
        print("  => EARNING ENABLES DEPTH, BUT COMPETENCE STILL SATURATES: the earned lineage survives a")
        print("     deep regime that cold-start can't (a real result), yet competence plateaus once it")
        print("     hits the substrate's max-viable-depth ceiling — a rate up to that depth, then a stock.")
    else:
        print("  => THE EARNED LAW DOES NOT BREAK SATURATION (honest negative): an expanding construction")
        print("     law does not sustain the rise past exp053's plateau. Competence is bounded by the")
        print("     substrate's optimal construction richness, not by the law being fixed.")


if __name__ == "__main__":
    main()
