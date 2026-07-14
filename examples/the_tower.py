#!/usr/bin/env python3
"""The recursive tower: physics -> chemistry -> biology -> culture from ONE engine.

Each tier runs the open+modular substrate; its stable, heritable collectives are promoted to the
next tier's atoms (reification across levels), and the same engine runs one level up.

Run from the repo root:  python3 examples/the_tower.py
"""
from omega.levels.stack import run_stack, LEVEL_NAMES


if __name__ == "__main__":
    print("\nRunning the recursive level stack (each tier's collectives = the next tier's atoms)...\n")
    result = run_stack(max_tiers=5, seed=0, ticks=2500)
    print(f"  tower depth: {result.tower_depth}  "
          f"(levels that formed >=2 heritable, open-ended collectives)\n")
    print(f"  {'tier':>4}  {'level':<13} {'collectives':>11} {'heredity self>null':>19} {'novelty':>8}")
    for t in result.tiers:
        mark = "heritable" if t.heritable else "flat"
        print(f"  {t.tier:>4}  {t.level:<13} {t.n_collectives:>11} "
              f"{t.hered_self:>8.3f} > {t.hered_null:<6.3f} {mark:>0}  {t.novelty:>6.2f}")
    print("\n  physics -> chemistry -> biology -> culture: a major transition that RECURSES.\n")
