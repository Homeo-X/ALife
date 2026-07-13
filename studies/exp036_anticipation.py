"""exp036 — intrinsic function: can selection for ANTICIPATION produce it?

The engine piece exp011 said was missing: function must be intrinsic and *selected*, not bolted
on. Here the environment is given a regularity worth predicting — a **cyclic feed** whose favoured
band of atoms rotates every `feed_period` ticks — and demes are selected for **anticipation** (a
deme whose recent products match the *next* season is fitter). Does prediction evolve?

Metric (rate, not cumulative): over a late window, the fraction of the population's atoms that lie
in the **current** season's band (reactivity) and in the **next** season's band (anticipation),
vs chance = 1/bands. Matched controls isolate the cause:
  treat        : cyclic feed + deme_fitness=anticipation   (structure present AND selected)
  network-ctrl : cyclic feed + deme_fitness=network        (structure present, NOT selected)
  random-null  : random feed + deme_fitness=anticipation   (nothing to anticipate)

Anticipation is real only if treat's P(next band) exceeds BOTH the network control (isolating the
fitness) and chance. Run: PYTHONPATH=. python3 studies/exp036_anticipation.py [ticks] [n_seeds]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise


def _band(a, w, k):
    return (int(a[1:]) // w) % k if isinstance(a, str) and a.startswith("y") and a[1:].isdigit() else None


def _atoms(state):
    out, stk = [], [state]
    while stk:
        x = stk.pop()
        (stk.extend(x) if isinstance(x, tuple) else out.append(x))
    return out


def _run(args) -> dict:
    label, overrides, seed, ticks = args
    p, c = get_experiment("exp036")(seed=seed, ticks=ticks, **overrides)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    k = p.feed_bands; w = max(1, len(p.atoms) // k)
    curP, nxtP = [], []
    for t in range(ticks):
        sch.run(1)
        if t > ticks // 2 and t % 40 == 0 and p.feed_period > 0:
            cur = (u.tick // p.feed_period) % k; nxt = (cur + 1) % k
            cc = nn = tt = 0
            for o in u.organizations.values():
                for a in _atoms(o.state):
                    b = _band(a, w, k)
                    if b is not None:
                        tt += 1; cc += (b == cur); nn += (b == nxt)
            if tt:
                curP.append(cc / tt); nxtP.append(nn / tt)
    return {"label": label, "seed": seed,
            "p_current": mean(curP) if curP else 0.0,
            "p_next": mean(nxtP) if nxtP else 0.0}


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    conds = {"treat": {}, "network-ctrl": {"deme_fitness": "network"},
             "random-null": {"feed_pattern": "random"}}
    jobs = [(lab, ov, s, ticks) for lab, ov in conds.items() for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))
    json.dump({"ticks": ticks, "n_seeds": n, "rows": rows},
              open("studies/exp036_results.json", "w"), indent=2)

    chance = 0.25
    print(f"exp036 — does selection for anticipation produce it? ({ticks} ticks, {n} seeds)")
    print(f"  chance = 1/bands = {chance}\n")
    print(f"  {'condition':>13} {'P(current band)':>16} {'P(next band)':>14}")
    agg = {}
    for lab in conds:
        rs = [r for r in rows if r["label"] == lab]
        pc = mean(r["p_current"] for r in rs); pn = mean(r["p_next"] for r in rs)
        agg[lab] = (pc, pn)
        print(f"  {lab:>13} {pc:>16.3f} {pn:>14.3f}")
    react = agg["treat"][0] - chance
    antic_vs_ctrl = agg["treat"][1] - agg["network-ctrl"][1]
    antic_vs_chance = agg["treat"][1] - chance
    print(f"\n  reactivity (treat P(current) - chance)         : {react:+.3f}")
    print(f"  anticipation gain (treat - network control)    : {antic_vs_ctrl:+.3f}")
    print(f"  anticipation vs chance (treat P(next) - chance): {antic_vs_chance:+.3f}")
    if antic_vs_ctrl > 0.05 and antic_vs_chance > 0.05:
        print("\n  => ANTICIPATION EVOLVES: selection for prediction produced it.")
    elif react > 0.02:
        print("\n  => REACTIVITY ONLY (negative-with-diagnosis): the cyclic environment is weakly")
        print("     tracked, but selection for anticipation adds ~nothing over the control — the")
        print("     substrate has no internal state to REPRESENT environmental timing, so")
        print("     prediction cannot be selected. Motivates exp037 (evolvable internal memory).")
    else:
        print("\n  => no environmental structure formed at all — see per-condition table.")


if __name__ == "__main__":
    main()
