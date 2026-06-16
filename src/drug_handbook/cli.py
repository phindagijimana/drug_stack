"""Minimal CLI entry point for the DrugStack companion package.

Usage:

    drug-handbook --version
    drug-handbook --help

The handbook itself lives in ``docs/`` and is served with ``mkdocs serve``.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="drug-handbook",
        description="DrugStack companion CLI. The handbook itself is in docs/.",
    )
    parser.add_argument("--version", action="version", version=f"drug-handbook {__version__}")
    parser.add_argument(
        "--docs-url",
        action="store_true",
        help="Print the URL of the rendered handbook.",
    )
    args = parser.parse_args(argv)

    if args.docs_url:
        print("https://phindagijimana.github.io/drug_stack/")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
