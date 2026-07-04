"""Visualization hooks — deliberately zero-dependency.

v0.1 ships text-based sparklines so the framework runs anywhere with just the
standard library. A matplotlib backend can be added later behind the same
``plot`` entry point without changing callers.
"""
from __future__ import annotations

# Note: submodules are imported lazily (``from omega.visualization.plot import
# ...``) rather than eagerly here, so that ``python -m omega.visualization.plot``
# does not trip runpy's double-import warning.
__all__ = ["plot"]
