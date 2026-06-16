"""DrugStack companion package — currently a stub.

The handbook is documentation-first. This package exists so that:

- ``pip install -e ".[docs,dev]"`` works for contributors.
- Future runnable examples (similarity search, QSAR, docking, generative design)
  have a place to live as importable modules.

For now the only public surface is :func:`version` and the ``drug-handbook`` CLI.
"""

from __future__ import annotations

__all__ = ["__version__", "version"]

__version__ = "0.1.0"


def version() -> str:
    """Return the installed package version."""
    return __version__
