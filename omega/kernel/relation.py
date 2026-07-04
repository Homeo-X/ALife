"""Relations — Axiom 2 (Interaction) made explicit.

A relation records that two organizations *can* or *did* influence one another.
In v0.1 relations are lightweight and mostly diagnostic: the interaction itself
is carried by :class:`~omega.kernel.transform.Reaction`. Relations let emergence
detectors and metrics reconstruct the interaction graph after the fact.

We deliberately do **not** give relations a spatial meaning. Proximity, if it
ever matters, must emerge as a constraint on which organizations can relate — it
is not built in.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Relation:
    """A directed influence from ``source`` to ``target`` via some transform."""

    source: int
    target: int
    via: str
    tick: int
    kind: str = "interaction"
