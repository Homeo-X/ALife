#!/usr/bin/env python3
"""The core result in one screen: an OPEN+MODULAR substrate stays open-ended; a CLOSED one dies.

  exp030 (typed_path, the "both corner") — modular AND open-ended  -> novelty stays > 0
  exp029 (typed morphisms)               — modular but closed      -> novelty -> 0

Run from the repo root:  python3 examples/open_vs_closed.py
"""
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def novelty_pulse(exp: str, ticks: int = 1500) -> None:
    physics, config = get_experiment(exp)(seed=0, ticks=ticks, n_patches=24,
                                          propagule_mode="source")
    r = run(physics, config)
    npt = r.novelty_new_per_tick
    k = 8
    windows = [sum(npt[i * len(npt) // k:(i + 1) * len(npt) // k]) /
               max(1, len(npt) // k) for i in range(k)]
    hi = max(windows) or 1.0
    bars = "".join("▁▂▃▄▅▆▇█"[min(7, int(v / hi * 7))] for v in windows)
    print(f"  {exp:>7}  novelty rate over time  {bars}   "
          f"start {windows[0]:.2f} -> end {windows[-1]:.2f}")


if __name__ == "__main__":
    print("\nOpen-ended evolution needs infinite CONSTRUCTIBILITY, not infinite space.\n")
    print("  the OPEN + MODULAR 'both corner' keeps discovering; the CLOSED substrate exhausts:\n")
    novelty_pulse("exp030")   # open-ended AND modular
    novelty_pulse("exp029")   # modular but closed
    print("\n  (exp030 sustains a positive novelty rate; exp029 collapses toward zero.)\n")
