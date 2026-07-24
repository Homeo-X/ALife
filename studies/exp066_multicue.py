"""exp066 — MULTI-CUE PERCEPTION: does INTEGRATING two observable cues pay? Perceptual breadth toward cognition.

exp065 (Ω-0.54) solved a partially-observable world with MEMORY (infer the hidden season direction from
history). exp066 asks the complementary question: can an agent solve it instead with a richer PERCEPTUAL
channel — integrating two *observable* cues? The decisive design is a 2×2 that isolates cue integration:

  env_cues:      1 (the next band depends on the season ALONE — sawtooth cur+1; the regime cue is present
                    but IRRELEVANT)
                 2 (the next band is a CONJUNCTION of season AND regime — cur+1 if reg=0 else cur-1; the
                    season alone underdetermines it, so you must read BOTH cues)
  agent_policy:  embodied (single-cue: perceives the season cur only — no memory, no second cue)
                 multi    (two-cue: perceives cur AND the regime, via a per-regime action table phi[reg])

The regime cue (and the multi agent's 2-entry table) is present in BOTH env conditions, so the multi agent
pays the same "perceive two things" cost either way — a benefit only under env=2 isolates INTEGRATION, not
extra parameters.

Prediction (a double dissociation): multi pays IFF the world requires it —
  * env=2: multi > embodied (single cue cannot resolve the conjunction)
  * env=1: multi <= embodied (the second cue is present but useless — no free lunch for extra perception)
An interaction (not a main effect) is the clean signature that it is cue INTEGRATION that pays.

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
POLICIES = ["embodied", "multi"]


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
    env, policy, seed, warmup, cycle = args
    p, c = get_experiment("exp066")(seed=seed, env_cues=env, agent_policy=policy, forage_n=6)
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
    return {"env": env, "policy": policy, "seed": seed,
            "anticip": mean(vals) if vals else 0.0}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 7000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
    jobs = [(e, pol, seed, warmup, cycle) for e in ENVS for pol in POLICIES for seed in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    cell = {f"{e}:{pol}": mean(r["anticip"] for r in rows if r["env"] == e and r["policy"] == pol)
            for e in ENVS for pol in POLICIES}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "cells": cell},
              open("studies/exp066_results.json", "w"), indent=2)

    print(f"exp066 — does multi-cue perception (integrating two cues) pay? 2x2 env x policy "
          f"({n} seeds; chance=0.25)\n")
    print(f"  {'env_cues':>9} {'embodied (1 cue)':>18} {'multi (2 cues)':>16} {'multi-embodied':>16}")
    diff = {}
    for e in ENVS:
        emb, mlt = cell[f"{e}:embodied"], cell[f"{e}:multi"]
        diff[e] = mlt - emb
        label = "1 (season only)" if e == 1 else "2 (conjunction)"
        print(f"  {label:>9} {emb:>18.3f} {mlt:>16.3f} {diff[e]:>+16.3f}")
    print()

    interaction = diff[2] - diff[1]
    multi_pays_when_needed = diff[2] > 0.03
    not_a_main_effect = diff[1] <= 0.03
    print(f"  multi-minus-embodied: env=2 {diff[2]:+.3f}, env=1 {diff[1]:+.3f}  "
          f"(interaction {interaction:+.3f})\n")
    if multi_pays_when_needed and not_a_main_effect and interaction > 0.05:
        print("  => MULTI-CUE PERCEPTION PAYS — AND ONLY WHEN THE WORLD REQUIRES IT (a double dissociation).")
        print("     When the reward is a CONJUNCTION of two observable cues (env=2), an agent that integrates")
        print("     both out-anticipates the single-cue agent; when the second cue is present but irrelevant")
        print("     (env=1) it does not (indeed pays a small cost for the useless channel). The interaction —")
        print("     not a main effect — shows it is cue INTEGRATION that pays, not extra parameters. A second")
        print("     route to cognition (breadth), complementing exp065's memory (depth in time).")
    elif multi_pays_when_needed:
        print("  => MULTI-CUE HELPS IN THE CONJUNCTIVE WORLD, but the dissociation is imperfect (it also")
        print("     helps / doesn't clearly hurt when the cue is irrelevant) — report the 2x2 as-is.")
    else:
        print("  => MULTI-CUE DOES NOT PAY — even when the reward depends on both cues the two-cue agent does")
        print("     not out-anticipate the single-cue one (a clean negative bounding perceptual breadth here).")


if __name__ == "__main__":
    main()
