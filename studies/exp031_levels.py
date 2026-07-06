"""exp031 — multiple levels of organization (physics → chemistry → biology → culture).

Two studies:
 (A) the recursive TOWER: run the LevelStack — each tier's stable heritable collectives
     become the next tier's atoms — and measure how many organizational levels
     spontaneously stack (tower depth), each still heritable AND open-ended.
 (B) the CULTURE level: horizontal (Lamarckian) motif transfer between collectives,
     decoupled from reproduction. Contrast a motif's spread with vs without transfer,
     and horizontal vs vertical transmission rate.
Run: PYTHONPATH=. python3 studies/exp031_levels.py [ticks] [n_seeds]
"""
from __future__ import annotations
import json, sys
from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev

from omega.levels.stack import run_stack, LEVEL_NAMES
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run


def _tower(seed):
    r = run_stack(max_tiers=5, seed=seed, ticks=int(TICKS))
    return {"seed": seed, "depth": r.tower_depth,
            "tiers": [{"tier": t.tier, "level": t.level, "alphabet": t.alphabet_size,
                       "collectives": t.n_collectives, "self": t.hered_self,
                       "null": t.hered_null, "novelty": t.novelty,
                       "heritable": t.heritable} for t in r.tiers]}


def _culture(args):
    ht, seed = args
    p, c = get_experiment('exp031_culture')(seed=seed, ticks=int(TICKS), n_patches=24,
                                            propagule_mode='source', horizontal_transfer=ht)
    r = run(p, c)
    tail = r.metrics[-len(r.metrics) // 5:]
    ndt = mean(m['gauges'].get('n_deme_signatures', 0.0) for m in tail)
    return {"ht": ht, "seed": seed, "horizontal": p._meme_horizontal,
            "vertical": p._meme_vertical, "n_signatures": ndt,
            "novelty": r.open_endedness["novelty_rate"]}


def main():
    global TICKS
    TICKS = int(sys.argv[1]) if len(sys.argv) > 1 else 2500
    seeds = list(range(int(sys.argv[2]) if len(sys.argv) > 2 else 5))
    with ProcessPoolExecutor(max_workers=8) as ex:
        towers = list(ex.map(_tower, seeds))
        cults = list(ex.map(_culture, [(ht, s) for ht in (0.0, 0.3) for s in seeds]))
    json.dump({"towers": towers, "culture": cults}, open('studies/exp031_results.json', 'w'), indent=2)

    print(f"(A) recursive tower — how many organizational levels stack? ({len(seeds)} seeds)")
    depths = [t['depth'] for t in towers]
    print(f"  tower depth: mean {mean(depths):.1f} ± {pstdev(depths):.1f}, "
          f"max {max(depths)}, per-seed {depths}")
    maxlen = max(len(t['tiers']) for t in towers)
    print(f"  {'tier':>4} {'level':>13} {'alphabet':>8} {'collectives':>11} "
          f"{'self':>6} {'null':>6} {'novelty':>7} {'heritable':>9}")
    for i in range(maxlen):
        rows = [t['tiers'][i] for t in towers if i < len(t['tiers'])]
        print(f"  {i:>4} {LEVEL_NAMES[min(i,len(LEVEL_NAMES)-1)]:>13} "
              f"{mean(r['alphabet'] for r in rows):>8.0f} {mean(r['collectives'] for r in rows):>11.0f} "
              f"{mean(r['self'] for r in rows):>6.3f} {mean(r['null'] for r in rows):>6.3f} "
              f"{mean(r['novelty'] for r in rows):>7.2f} "
              f"{sum(r['heritable'] for r in rows)}/{len(rows):>d} heritable")

    print(f"\n(B) culture — horizontal (Lamarckian) transfer between collectives:")
    print(f"  {'transfer':>9} {'horizontal':>10} {'vertical':>9} {'H/V':>5} "
          f"{'n_signatures':>12} {'novelty':>8}")
    for ht in (0.0, 0.3):
        rs = [c for c in cults if c['ht'] == ht]
        h = mean(r['horizontal'] for r in rs); v = mean(r['vertical'] for r in rs)
        print(f"  {ht:>9} {h:>10.0f} {v:>9.0f} {(h/v if v else 0):>5.2f} "
              f"{mean(r['n_signatures'] for r in rs):>12.1f} {mean(r['novelty'] for r in rs):>8.2f}")


if __name__ == '__main__':
    main()
