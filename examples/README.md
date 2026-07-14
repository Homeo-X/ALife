# Examples

Three quick ways to see what Project Ω does. All pure standard library — nothing to install.
Run from the repository root.

## 1. Watch a living world (≈ instant)

```bash
python -m omega.world run --dashboard        # open http://localhost:8000
#   or, headless in the terminal:
python -m omega.world run --ticks 4000
#   or write a shareable self-contained snapshot:
python -m omega.world snapshot --out world.html
```

The novelty pulse, named lifeforms, collective communities, culture, a world map, and a "reach
in" panel to steer it. See [`../omega/docs/WORLD.md`](../omega/docs/WORLD.md).

## 2. The core result: open vs closed (≈ 20 s)

```bash
python3 examples/open_vs_closed.py
```

Runs the two substrates side by side — the **open+modular** "both corner" (exp030) vs the
**closed** control (exp029) — and shows the novelty rate staying alive in one and collapsing to
zero in the other. This is the constructibility hypothesis in a single screen.

## 3. The recursive tower (≈ 30 s)

```bash
python3 examples/the_tower.py
```

Runs the level stack: each tier's heritable collectives become the next tier's atoms, so
physics → chemistry → biology → culture emerge from one engine. Prints the tower depth and each
tier's heredity and novelty.
