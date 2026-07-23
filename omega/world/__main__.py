"""CLI for the Ω world — start/resume a persistent, watchable world.

    python -m omega.world run                       # run in the terminal (headless watch)
    python -m omega.world run --dashboard           # serve the live browser dashboard
    python -m omega.world run --checkpoint w.ckpt   # persist / resume across restarts
    python -m omega.world snapshot --out world.html # write a self-contained HTML snapshot

Resumes automatically when ``--checkpoint`` points at an existing file, so a world accretes
history across sessions (and survives container restarts).
"""
from __future__ import annotations

import argparse
import sys
import time

from omega.world import checkpoint as _ckpt
from omega.world.dashboard import render_html, render_terminal, serve
from omega.world.observe import Observer
from omega.world.runtime import World, DEFAULT_MEMORY_HORIZON


def _load_or_create(args) -> World:
    if args.checkpoint and _ckpt.exists(args.checkpoint):
        w = _ckpt.load(args.checkpoint)
        print(f"resumed world from {args.checkpoint} at tick {w.tick:,}")
        return w
    # genuine_novelty attaches the eviction-robust global sketch (Ω-0.39) so the vital-signs panel
    # can show the *genuine* ever-new rate — dynamics-invariant, so it's always safe to enable.
    return World.create(getattr(args, "physics", "world"), seed=args.seed,
                        memory_horizon=args.memory_horizon, genuine_novelty=True)


def _cmd_run(args) -> None:
    world = _load_or_create(args)
    if args.dashboard:
        serve(world, port=args.port, chunk=args.chunk,
              checkpoint_path=args.checkpoint, checkpoint_every=args.checkpoint_every)
        return
    # headless terminal watch loop
    obs = Observer()
    chunks = 0
    target = None if args.ticks <= 0 else world.tick + args.ticks
    try:
        while target is None or world.tick < target:
            world.step(args.chunk)
            chunks += 1
            sys.stdout.write("\033[2J\033[H" + render_terminal(obs.snapshot(world)) + "\n")
            sys.stdout.flush()
            if args.checkpoint and chunks % args.checkpoint_every == 0:
                _ckpt.save(world, args.checkpoint)
            if args.delay:
                time.sleep(args.delay)
    except KeyboardInterrupt:
        pass
    finally:
        if args.checkpoint:
            _ckpt.save(world, args.checkpoint)
            print(f"\ncheckpointed at tick {world.tick:,} -> {args.checkpoint}")


def _cmd_snapshot(args) -> None:
    world = _load_or_create(args)
    if world.tick == 0:
        world.step(args.warmup)
    obs = Observer()
    for _ in range(8):                     # a few chunks so the pulse/events are populated
        world.step(args.chunk)
        snap = obs.snapshot(world)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(render_html(snap))
    print(f"wrote self-contained snapshot ({world.tick:,} ticks) -> {args.out}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="python -m omega.world", description=__doc__)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--physics", default="world",
                    help="world builder: 'world' (exp030-era) or 'living_world' (carries the "
                         "self-improvement arc — Catalytic Law + Red Queen + full competence pressure)")
    ap.add_argument("--chunk", type=int, default=40, help="ticks advanced per snapshot")
    ap.add_argument("--checkpoint", help="checkpoint file (resume if it exists)")
    ap.add_argument("--checkpoint-every", type=int, default=25, help="checkpoint every N chunks")
    ap.add_argument("--memory-horizon", type=int, default=DEFAULT_MEMORY_HORIZON)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run/resume the world")
    r.add_argument("--dashboard", action="store_true", help="serve the live browser dashboard")
    r.add_argument("--port", type=int, default=8000)
    r.add_argument("--ticks", type=int, default=0, help="stop after N ticks (0 = forever)")
    r.add_argument("--delay", type=float, default=0.0, help="seconds between terminal frames")
    r.set_defaults(func=_cmd_run)

    s = sub.add_parser("snapshot", help="write a self-contained HTML snapshot")
    s.add_argument("--out", default="world_snapshot.html")
    s.add_argument("--warmup", type=int, default=2000)
    s.set_defaults(func=_cmd_snapshot)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
