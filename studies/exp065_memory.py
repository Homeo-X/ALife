"""exp065 — MEMORY (internal state): does acting on HISTORY pay? The step toward cognition.

exp062 (Ω-0.51) showed a *reactive* agent (act on the instant percept) is selectable in a fully-observable
sawtooth season. exp065 asks the deeper question: does an agent with **internal state / memory** — one that
acts on the *history* of its percepts — pay when the instant percept is insufficient? The decisive design is
a 2×2 that isolates memory itself:

  season_pattern:  sawtooth (0,1,2,3,0,... — the current band IMPLIES the next: instant-observable)
                   triangle (0,1,2,3,2,1,0,... — the current band does NOT imply the next; you must
                             remember the previous season to know the direction: PARTIALLY observable)
  agent_policy:    embodied (reactive: forage cur+phi, phi heritable — no memory)
                   memory   (carry internal state — the last observed season direction — and extrapolate it)

Prediction (a double dissociation): memory pays IFF the world requires it —
  * triangle: memory > embodied (reactive cannot track a reversing season)
  * sawtooth: memory <= embodied (memory is confused by the wrap; the instant percept already suffices)
An interaction (not a main effect) is the clean signature that it is MEMORY, not just a different policy.

Run:
  PYTHONPATH=. python3 studies/exp065_memory.py [n_seeds] [warmup] [cycle_ticks]
"""
from __future__ import annotations
import sys, json
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from omega.experiments.registry import get_experiment
from omega.kernel.universe import Universe
from omega.kernel.scheduler import Scheduler
from omega.substrate.noise import Noise

SEASONS = ["sawtooth", "triangle"]
POLICIES = ["embodied", "memory"]


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
    season, policy, seed, warmup, cycle = args
    p, c = get_experiment("exp065")(seed=seed, season_pattern=season, agent_policy=policy, forage_n=6)
    u, rng = Universe(total_quanta=c.total_quanta), Noise(c.seed); p.seed(u, rng)
    sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                    max_reactions_per_tick=c.max_reactions_per_tick)
    sch.run(warmup)
    vals = []
    for _ in range(12):                                    # average over a full triangle/sawtooth cycle
        sch.run(cycle // 12)
        v = _anticip(p)
        if v is not None:
            vals.append(v)
    return {"season": season, "policy": policy, "seed": seed,
            "anticip": mean(vals) if vals else 0.0}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 7000
    cycle = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
    jobs = [(s, pol, seed, warmup, cycle) for s in SEASONS for pol in POLICIES for seed in range(n)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(_run, jobs))

    cell = {f"{s}:{pol}": mean(r["anticip"] for r in rows if r["season"] == s and r["policy"] == pol)
            for s in SEASONS for pol in POLICIES}
    json.dump({"n_seeds": n, "warmup": warmup, "cycle": cycle, "cells": cell},
              open("studies/exp065_results.json", "w"), indent=2)

    print(f"exp065 — does memory (acting on history) pay? 2x2 season x policy ({n} seeds; chance=0.25)\n")
    print(f"  {'season':>9} {'embodied (reactive)':>20} {'memory':>10} {'memory-reactive':>16}")
    diff = {}
    for s in SEASONS:
        e, m = cell[f"{s}:embodied"], cell[f"{s}:memory"]
        diff[s] = m - e
        print(f"  {s:>9} {e:>20.3f} {m:>10.3f} {diff[s]:>+16.3f}")
    print()

    interaction = diff["triangle"] - diff["sawtooth"]
    memory_pays_when_needed = diff["triangle"] > 0.03
    not_a_main_effect = diff["sawtooth"] <= 0.03
    print(f"  memory-minus-reactive: triangle {diff['triangle']:+.3f}, sawtooth {diff['sawtooth']:+.3f}  "
          f"(interaction {interaction:+.3f})\n")
    if memory_pays_when_needed and not_a_main_effect and interaction > 0.05:
        print("  => MEMORY PAYS — AND ONLY WHEN THE WORLD REQUIRES IT (a double dissociation). In the")
        print("     partially-observable triangle season a memory agent (acting on the history of percepts)")
        print("     out-anticipates the reactive agent, while in the instant-observable sawtooth it does not")
        print("     (indeed is confused by the wrap). The interaction — not a main effect — shows it is")
        print("     MEMORY that pays, exactly when the instant percept underdetermines the right action. The")
        print("     first rung of genuine cognition: internal state that integrates the past is selectable.")
    elif memory_pays_when_needed:
        print("  => MEMORY HELPS IN THE PARTIALLY-OBSERVABLE WORLD, but the dissociation is imperfect (it also")
        print("     helps / doesn't clearly hurt in the sawtooth) — report the 2x2 as-is.")
    else:
        print("  => MEMORY DOES NOT PAY — even in the partially-observable triangle season the memory agent")
        print("     does not out-anticipate the reactive one (a clean negative bounding cognition here).")


if __name__ == "__main__":
    main()
