"""Text sparklines for a saved RunResult — read the shape of a run at a glance.

    python -m omega.visualization.plot results/exp003_seed0.json

Zero dependencies. The point is to see, without a plotting stack, whether novelty
is sustained or collapsing and whether the discovered-operator count is climbing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Sequence

_BARS = " ▁▂▃▄▅▆▇█"


def sparkline(values: Sequence[float], width: int = 60) -> str:
    if not values:
        return ""
    # resample to `width` buckets (mean) so long runs still fit one line
    n = len(values)
    if n > width:
        step = n / width
        buckets = []
        for i in range(width):
            lo, hi = int(i * step), int((i + 1) * step)
            chunk = values[lo:hi] or values[lo:lo + 1]
            buckets.append(sum(chunk) / len(chunk))
        values = buckets
    lo, hi = min(values), max(values)
    span = hi - lo or 1.0
    return "".join(_BARS[min(len(_BARS) - 1, int((v - lo) / span * (len(_BARS) - 1)))]
                   for v in values)


def plot_result_file(path: str | Path) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cfg = data["config"]
    print(f"=== {cfg['experiment']}  seed={cfg['seed']}  ticks={cfg['ticks']} ===")
    oe = data["open_endedness"]
    p = data["persistence"]
    print(f"OEI={oe['index']:.4f} [{oe['verdict']}]  "
          f"operator_growth={oe['operator_growth']}  "
          f"composed_persistent={p['composed_persistent']}\n")

    series = [
        ("new classes / tick ", data["novelty_new_per_tick"]),
        ("cumulative classes ", data["novelty_cumulative"]),
        ("discovered operators", data["discovered_per_tick"]),
        ("max depth           ", data["depth_per_tick"]),
    ]
    entropy = [m["entropy_bits"] for m in data["metrics"]]
    reservoir = [m["reservoir_pressure"] for m in data["metrics"]]
    primitives = [m.get("primitive_count", 0) for m in data["metrics"]]
    series.append(("emergent primitives ", primitives))
    # reification lineage depth (a Physics gauge) — the ratchet signal, if present
    reify_depth = [m.get("gauges", {}).get("reify_depth", 0) for m in data["metrics"]]
    if any(reify_depth):
        series.append(("reification depth   ", reify_depth))
    series.append(("entropy (bits)      ", entropy))
    series.append(("reservoir pressure  ", reservoir))

    for label, vals in series:
        if not vals:
            continue
        lo, hi = min(vals), max(vals)
        print(f"{label} |{sparkline(vals)}|  [{lo:.3g} .. {hi:.3g}]")


def main(argv=None) -> None:
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: python -m omega.visualization.plot <results.json> [...]")
        return
    for path in argv:
        plot_result_file(path)
        print()


if __name__ == "__main__":
    main()
