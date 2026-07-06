"""A tiny experiment registry (name -> builder).

A builder returns ``(Physics, Config)`` given an optional seed / overrides. This
keeps the harness ignorant of concrete experiments (dependency inversion) and
gives the CLI a single place to enumerate what can be run.
"""
from __future__ import annotations

from typing import Callable, Protocol

from omega.config import Config
from omega.kernel.transform import Physics


class ExperimentBuilder(Protocol):
    def __call__(self, seed: int = 0, **overrides) -> tuple[Physics, Config]: ...


EXPERIMENTS: dict[str, ExperimentBuilder] = {}


def register(name: str) -> Callable[[ExperimentBuilder], ExperimentBuilder]:
    def deco(builder: ExperimentBuilder) -> ExperimentBuilder:
        EXPERIMENTS[name] = builder
        return builder
    return deco


def get_experiment(name: str) -> ExperimentBuilder:
    if name not in EXPERIMENTS:
        raise KeyError(f"unknown experiment {name!r}; known: {sorted(EXPERIMENTS)}")
    return EXPERIMENTS[name]


def _ensure_loaded() -> None:
    """Import experiment modules so their @register side-effects run."""
    from omega.experiments import (  # noqa: F401
        exp001_noise,
        exp002_persistence,
        exp003_construction,
        exp004_reification,
        exp005_cumulative,
        exp006_hierarchy,
        exp007_frontier,
        exp008_toolkit,
        exp009_modules,
        exp010_copying,
        exp011_function,
        exp012_combinator,  # also registers exp013..030 (evolution→typed pivot→open-ended modular)
    )


_ensure_loaded()
