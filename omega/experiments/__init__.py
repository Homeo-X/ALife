"""The experiment registry and shared run harness.

Every experiment is a small module that supplies a :class:`~omega.kernel.transform.Physics`
and a default :class:`~omega.config.Config`. The harness wires up the universe,
scheduler, recorders, and emergence trackers identically for all of them, so
results are comparable and each experiment file only has to express *its physics*.

Development proceeds strictly in sequence (001 -> 008); jumping to organisms is
forbidden. Each experiment answers one yes/no question against a control.
"""
from __future__ import annotations

from omega.experiments.harness import RunResult, run
from omega.experiments.registry import EXPERIMENTS, get_experiment, register

__all__ = ["RunResult", "run", "EXPERIMENTS", "get_experiment", "register"]
