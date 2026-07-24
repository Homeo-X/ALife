"""exp062 — EMBODIED AGENCY: is a heritable PERCEPTION->ACTION policy selectable? (the first rung of minds)

The living world sustains open-ended novelty and self-maintaining life at scale (Ω-0.48–0.50). This opens the
embodiment thread: are its collectives *agents* — do they perceive their environment and act on it, and is
that selected? An **agent** here is a collective with a heritable policy: it perceives the environment's
season (the cyclic feed band, exp036) and forages atoms from the band an offset `phi` away from the
*perceived* season, which become material it builds with. Selection is `deme_fitness="anticipation"` (reward
products matching the NEXT band), so an embodied agent that evolves `phi=1` forages the next band and
anticipates.

The decisive matched control is **`agent_policy="blind"`**: identical policy + forage repertoire, but the
percept is a FIXED constant (decoupled from the real, moving season) — same action, no sensing. This
isolates whether *perception that informs action* is what pays. Swept as a **dose-response in the action
strength** (`forage_n`): does a stronger perception-coupled action produce a larger advantage over blind?

Per arm we measure two things: the mean **anticipation-match** over a full season cycle (does the agent's
behaviour track the environment?), and the fraction of demes whose policy sits at the anticipatory phase
**phi=1** (is perception *used and selected*, vs blind drift?).

Verdict:
  * embodied concentrates phi at 1 (>> blind) AND its anticipation advantage over blind GROWS with forage_n
    => agency is selectable and perception pays, dose-dependently — a proto-mind.
  * embodied ≈ blind at every strength => sensing confers no advantage here (a clean negative).
Run:
  PYTHONPATH=. python3 studies/exp062_agency.py [n_seeds] [warmup] [cycle_ticks]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

POLICIES = ["embodied", "blind"]
FORAGE = [2, 6, 12]


def _anticip(p) -> float | None:
    """Fraction of the demes' current products whose atoms fall in the NEXT season's band."""
    nb = p._next_band
    if not nb:
        return None
    tot = match = 0
    for d in p._deme_atoms.values():
        for a, nn in d.items():
            tot += nn
            if a in nb:
                match += nn
    return match / tot if tot else 0.0


def _run(args) -> dict:
    policy, fn, seed, warmup, cycle = args
    p, c = get_experiment("exp062")(seed=seed, agent_policy=policy, forage_n=fn)
    rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    sch.run(warmup)
    samples, step = 12, max(1, cycle // 12)
    vals = []
    for _ in range(samples):                                # average over a full season cycle
        sch.run(step)
        v = _anticip(p)
        if v is not None:
            vals.append(v)
    phis = list(p._deme_phase.values())
    phi1 = sum(1 for x in phis if x == 1) / len(phis) if phis else 0.0
    return {"policy": policy, "forage_n": fn, "seed": seed,
            "anticip": mean(vals) if vals else 0.0, "phi1": phi1}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    jobs = [(pol, fn, s, warmup, cycle) for pol in POLICIES for fn in FORAGE for s in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    summary = {}
    for pol in POLICIES:
        for fn in FORAGE:
            rs = [r for r in rows if r["policy"] == pol and r["forage_n"] == fn]
            summary[f"{pol}:{fn}"] = {"anticip": mean(r["anticip"] for r in rs),
                                      "phi1": mean(r["phi1"] for r in rs)}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "policies": POLICIES,
               "forage": FORAGE, "summary": summary},
              open("studies/exp062_results.json", "w"), indent=2)

    print(f"exp062 — is embodied agency selectable? dose-response in action strength ({n} seeds)\n")
    print(f"  {'forage_n':>8} {'embodied anticip':>18} {'blind anticip':>15} {'gap':>7}   "
          f"{'emb phi=1':>10} {'blind phi=1':>12}")
    gaps = {}
    for fn in FORAGE:
        e, b = summary[f"embodied:{fn}"], summary[f"blind:{fn}"]
        gap = e["anticip"] - b["anticip"]; gaps[fn] = gap
        print(f"  {fn:>8} {e['anticip']:>18.3f} {b['anticip']:>15.3f} {gap:>+7.3f}   "
              f"{e['phi1']:>10.2f} {b['phi1']:>12.2f}")
    print()

    # perception is USED and SELECTED: at the weakest action (least confounded by flooding), embodied
    # policies concentrate at the anticipatory phi=1 far above blind (chance ~1/feed_bands = 0.25).
    e_lo, b_lo = summary[f"embodied:{FORAGE[0]}"], summary[f"blind:{FORAGE[0]}"]
    perception_selected = e_lo["phi1"] > b_lo["phi1"] + 0.15
    # perception PAYS, dose-dependently: the embodied advantage over blind grows with action strength.
    dose_dependent = gaps[FORAGE[-1]] > gaps[FORAGE[0]] + 0.05 and gaps[FORAGE[-1]] > 0.05
    print(f"  perception selected (emb phi=1 {e_lo['phi1']:.2f} >> blind {b_lo['phi1']:.2f} at weak action): {perception_selected}")
    print(f"  perception pays, dose-dependently (gap {gaps[FORAGE[0]]:+.3f} -> {gaps[FORAGE[-1]]:+.3f}): {dose_dependent}\n")
    if perception_selected and dose_dependent:
        print("  => AGENCY IS SELECTABLE — embodied policies concentrate at the informative phase (perception")
        print("     is USED and SELECTED, where blind policies drift), and the embodied anticipation advantage")
        print("     over blind GROWS with action strength (perception PAYS, dose-dependently). Sensing-and-")
        print("     acting is a selectable, behaviourally-advantageous trait: the minimal proto-mind. The world")
        print("     is not just alive — its collectives are agents.")
    elif perception_selected:
        print("  => PERCEPTION IS SELECTED BUT WEAKLY PAID — embodied policies concentrate at the informative")
        print("     phase, but the anticipation advantage over blind does not grow decisively with action")
        print("     strength: agency is representable and selected, its behavioural payoff bounded here.")
    else:
        print("  => NO SELECTABLE AGENCY — embodied ≈ blind on both phi-concentration and anticipation:")
        print("     perception does not pay in this world (a clean negative bounding embodiment).")


if __name__ == "__main__":
    main()
