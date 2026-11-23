"""Check the test entry point accepts tests and rejects runner escape options."""

import os
import subprocess
from pathlib import Path

from pytest import mark

SCRIPT = Path(__file__).resolve().parent.parent / "runtests"


@mark.parametrize(
    "argument",
    [
        "--override-ini=addopts=-p malicious",
        "../test.py",
        "tests/test_package_meta.py::test_get_version[$(id)]",
    ],
)
def test_rejects_unsupported_arguments(argument):
    result = subprocess.run([str(SCRIPT), argument], capture_output=True, text=True)
    assert result.returncode != 0
    assert "unsupported" in result.stderr.lower()


def test_runs_a_single_selected_test():
    result = subprocess.run(
        [str(SCRIPT), "tests/test_package_meta.py::test_shortcut"],
        cwd=SCRIPT.parent,
        env={**os.environ, "PYTEST_ADDOPTS": "-o addopts="},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "1 passed" in result.stdout


@mark.parametrize("case", ["version0-1.2.3 pre-alpha", "version1-1.2.3.post1"])
def test_runs_a_parametrized_case(case):
    result = subprocess.run(
        [str(SCRIPT), f"tests/test_package_meta.py::test_get_version[{case}]"],
        cwd=SCRIPT.parent,
        env={**os.environ, "PYTEST_ADDOPTS": "-o addopts="},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "1 passed" in result.stdout
