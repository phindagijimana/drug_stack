"""Smoke tests for the DrugStack companion package."""

from __future__ import annotations

import drug_handbook
from drug_handbook.cli import main


def test_version_string() -> None:
    assert isinstance(drug_handbook.__version__, str)
    assert drug_handbook.version() == drug_handbook.__version__


def test_cli_help_runs(capsys) -> None:
    rc = main([])
    captured = capsys.readouterr()
    assert rc == 0
    assert "DrugStack" in captured.out


def test_cli_docs_url(capsys) -> None:
    rc = main(["--docs-url"])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "https://phindagijimana.github.io/drug_stack/"
