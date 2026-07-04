"""Structured logging setup.

A single helper so every entry point logs consistently. Kept dependency-free
(stdlib ``logging``); the format is compact and parseable.
"""
from __future__ import annotations

import logging
import sys


def get_logger(name: str = "omega", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # already configured
        return logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
