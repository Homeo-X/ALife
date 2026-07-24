"""exp066 — MULTI-CUE PERCEPTION: does INTEGRATING two observable cues pay? Perceptual breadth toward cognition.

exp065 (Ω-0.54) solved a partially-observable world with MEMORY (infer the hidden season direction from
history). exp066 asks the complementary question: can an agent solve it instead with a richer PERCEPTUAL
channel — integrating two *observable* cues? The decisive design is a 2×3 that isolates cue integration from
the confound of merely carrying a richer policy:

  env_cues:      1 (the next band depends on the season ALONE — sawtooth cur+1; the regime cue is present
                    but IRRELEVANT)
                 2 (the next band is a CONJUNCTION of season AND regime — cur+1 if reg=0 else cur-1; the
                    season alone underdetermines it, so you must read BOTH cues)
  agent_policy:  embodied  (single-cue reference: perceives the season cur only, a SCALAR phase genome)
                 cue_blind (MATCHED control: the *same* per-regime table genome as `multi`, same parameter
                            count and mutation load, but its regime percept is DECOUPLED (fixed) — it cannot
                            read the second cue)
                 multi     (two-cue treatment: perceives cur AND the regime, acting via the per-regime table)

The key contrast is **multi vs cue_blind**: identical genome, the ONLY difference is whether the agent reads
the second cue — so any advantage is INTEGRATION, not extra parameters (the exp062 embodied-vs-blind design
applied to cue 2). The **cue_blind vs embodied** contrast separately exposes the parameter/genome effect.

Prediction (a double dissociation): multi > cue_blind IFF env=2, and multi ~ cue_blind when env=1 (the second
cue is present but useless). The interaction is the clean signature that it is cue INTEGRATION that pays.

Run:
  PYTHONPATH=. python3 studies/exp066_multicue.py [n_seeds] [warmup] [cycle_ticks]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

ENVS = [1, 2]
# (label, agent_policy, cue_blind)
ARMS = [("embodied", "embodied", False), ("cue_blind", "multi", True), ("multi", "multi", False)]


def _anticip(p) -> float | None:
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
    env, label, policy, cb, seed, warmup, cycle = args
    p, c = get_experiment("exp066")(seed=seed, env_cues=env, agent_policy=policy, cue_blind=cb, forage_n=6)
    u, rng = Universe(total_quanta=c.total_quanta), Noise(c.seed); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    sch.run(warmup)
    vals = []
    for _ in range(12):                                    # average over >= 2 regime periods
        sch.run(cycle // 12)
        v = _anticip(p)
        if v is not None:
            vals.append(v)
    return {"env": env, "label": label, "seed": seed,
            "anticip": mean(vals) if vals else 0.0}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 7000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
    jobs = [(e, lab, pol, cb, seed, warmup, cycle)
            for e in ENVS for (lab, pol, cb) in ARMS for seed in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    cell = {f"{e}:{lab}": mean(r["anticip"] for r in rows if r["env"] == e and r["label"] == lab)
            for e in ENVS for (lab, _, _) in ARMS}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "cells": cell},
              open("studies/exp066_results.json", "w"), indent=2)

    print(f"exp066 — does multi-cue perception (integrating two cues) pay? 2x3 env x arm "
          f"({n} seeds; chance=0.25)\n")
    print(f"  {'env_cues':>15} {'embodied':>10} {'cue_blind':>10} {'multi':>8} "
          f"{'multi-blind':>12} {'blind-embod':>12}")
    integ = {}
    for e in ENVS:
        emb, blind, mlt = cell[f"{e}:embodied"], cell[f"{e}:cue_blind"], cell[f"{e}:multi"]
        integ[e] = mlt - blind
        label = "1 (season only)" if e == 1 else "2 (conjunction)"
        print(f"  {label:>15} {emb:>10.3f} {blind:>10.3f} {mlt:>8.3f} "
              f"{integ[e]:>+12.3f} {blind - emb:>+12.3f}")
    print()

    interaction = integ[2] - integ[1]
    pays_when_needed = integ[2] > 0.03
    not_when_useless = integ[1] <= 0.03
    print(f"  INTEGRATION (multi - matched cue_blind): env=2 {integ[2]:+.3f}, env=1 {integ[1]:+.3f}  "
          f"(interaction {interaction:+.3f})\n")
    if pays_when_needed and not_when_useless and interaction > 0.05:
        print("  => MULTI-CUE PERCEPTION PAYS — AND ONLY WHEN THE CUE IS RELEVANT (a double dissociation,")
        print("     genome matched). Against the cue_blind control that carries the IDENTICAL table genome but")
        print("     cannot read the second cue, INTEGRATING it out-anticipates only when the reward depends on")
        print("     it (env=2), and gives nothing when it is present-but-useless (env=1). The naive contrast vs")
        print("     the scalar `embodied` agent shows a spurious main effect (the richer table genome helps in")
        print("     both env's — the `blind-embod` column); the matched control isolates that it is cue")
        print("     INTEGRATION, not extra parameters, that pays. A second route to cognition (perceptual")
        print("     breadth), complementing exp065's memory (depth in time).")
    else:
        print("  => NO CLEAN INTEGRATION SIGNATURE against the matched cue_blind control — report the 2x3 as-is.")


if __name__ == "__main__":
    main()
