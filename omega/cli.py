"""Command-line runner for Ω experiments.

    python -m omega.cli list
    python -m omega.cli run exp001 --seed 0 --ticks 300
    python -m omega.cli run exp002 --bind false          # matched control
    python -m omega.cli suite                              # run the whole v0.1 suite

Results are written to ``results/<experiment>_seed<seed>.json`` for later
analysis and are fully reproducible from the embedded config.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from omega.experiments import run
from omega.experiments.registry import EXPERIMENTS, get_experiment
from omega.logging_setup import get_logger

log = get_logger("omega.cli")
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def _coerce(value: str):
    low = value.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def cmd_list() -> None:
    print("Registered experiments:")
    for name in sorted(EXPERIMENTS):
        print(f"  {name}")


def _run_one(name: str, seed: int, overrides: dict, label: str | None = None) -> None:
    physics, cfg = get_experiment(name)(seed=seed, **overrides)
    log.info("running %s seed=%d ticks=%d quanta=%d", label or name, seed, cfg.ticks, cfg.total_quanta)
    result = run(physics, cfg)
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"{label or name}_seed{seed}.json"
    result.to_json(out)
    print(result.headline())
    print(f"  -> {out}")


def cmd_run(args) -> None:
    overrides = {}
    for item in args.set or []:
        key, _, val = item.partition("=")
        overrides[key] = _coerce(val)
    if args.ticks is not None:
        overrides["ticks"] = args.ticks
    _run_one(args.experiment, args.seed, overrides)


def cmd_suite(args) -> None:
    print("=== Omega Kernel experiment suite ===\n")
    _run_one("exp001", args.seed, {})
    print()
    _run_one("exp002", args.seed, {"bind": True})
    _run_one("exp002", args.seed, {"bind": False}, label="exp002_control")  # matched control
    print()
    _run_one("exp003", args.seed, {})
    print()
    # exp004 needs a long horizon to distinguish sustained growth from a burst.
    _run_one("exp004", args.seed, {"ticks": args.ticks or 2000, "reify": True})
    _run_one("exp004", args.seed, {"ticks": args.ticks or 2000, "reify": False},
             label="exp004_control")
    print()
    # exp005: the nesting ratchet (treatment) vs the falsified feed-only "fix".
    _run_one("exp005", args.seed, {"ticks": args.ticks or 2000})
    _run_one("exp005", args.seed, {"ticks": args.ticks or 2000, "feed_reified": False},
             label="exp005_frozen_control")


def cmd_study(args) -> None:
    from omega.experiments.study import run_study
    overrides = {}
    for item in args.set or []:
        key, _, val = item.partition("=")
        overrides[key] = _coerce(val)
    if args.ticks is not None:
        overrides["ticks"] = args.ticks
    report = run_study(args.experiment, list(range(args.seeds)), **overrides)
    print(report.summary())


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="omega", description="Project Omega experiment runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list registered experiments")

    p_run = sub.add_parser("run", help="run one experiment")
    p_run.add_argument("experiment")
    p_run.add_argument("--seed", type=int, default=0)
    p_run.add_argument("--ticks", type=int, default=None)
    p_run.add_argument("--set", action="append", metavar="key=value",
                       help="override a config/physics param, e.g. --set bind=false")

    p_suite = sub.add_parser("suite", help="run the whole suite")
    p_suite.add_argument("--seed", type=int, default=0)
    p_suite.add_argument("--ticks", type=int, default=None)

    p_study = sub.add_parser("study", help="run one experiment across seeds and aggregate")
    p_study.add_argument("experiment")
    p_study.add_argument("--seeds", type=int, default=5, help="number of seeds (0..N-1)")
    p_study.add_argument("--ticks", type=int, default=None)
    p_study.add_argument("--set", action="append", metavar="key=value")

    args = parser.parse_args(argv)
    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "run":
        cmd_run(args)
    elif args.cmd == "suite":
        cmd_suite(args)
    elif args.cmd == "study":
        cmd_study(args)


if __name__ == "__main__":
    main()
