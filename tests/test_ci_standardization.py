"""Test the shared CI and test entry-point conventions."""

import os
import re
import subprocess
from pathlib import Path

from pytest import mark

SCRIPT = Path(__file__).resolve().parent.parent / "runtests"


class TestCiStandardization:
    @mark.parametrize(
        "argument",
        [
            "-p",
            "--override-ini=addopts=-p malicious",
            "../test.py",
            "tests/test_package_meta.py::test_get_version[$(id)]",
        ],
    )
    def test_rejects_unsupported_arguments(self, argument):
        result = subprocess.run([str(SCRIPT), argument], capture_output=True, text=True)
        assert result.returncode != 0
        assert "unsupported" in result.stderr.lower()

    def test_runs_a_single_selected_test(self):
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
    def test_runs_a_parametrized_case(self, case):
        result = subprocess.run(
            [str(SCRIPT), f"tests/test_package_meta.py::test_get_version[{case}]"],
            cwd=SCRIPT.parent,
            env={**os.environ, "PYTEST_ADDOPTS": "-o addopts="},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "1 passed" in result.stdout

    @mark.parametrize(
        "selector",
        [
            "tests/test_utils.py::test_parse_vaddr[10.200.0.0/16-virtual_addr2]",
            "tests/test_utils.py::test_parse_transport_prefixed_peer[udp6:[2001:db8::3]:1194-peer2]",
        ],
    )
    def test_runs_a_parametrized_address_case(self, selector):
        result = subprocess.run(
            [str(SCRIPT), selector],
            cwd=SCRIPT.parent,
            env={**os.environ, "PYTEST_ADDOPTS": "-o addopts="},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "1 passed" in result.stdout

    def test_runs_a_parametrized_option_case(self):
        selector = (
            "tests/test_ci_standardization.py::TestCiStandardization::"
            "test_rejects_unsupported_arguments[--override-ini=addopts=-p malicious]"
        )
        result = subprocess.run(
            [str(SCRIPT), selector],
            cwd=SCRIPT.parent,
            env={**os.environ, "PYTEST_ADDOPTS": "-o addopts="},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "1 passed" in result.stdout

    def test_failure_bot_uses_ci_workflow(self):
        workflows = SCRIPT.parent / ".github" / "workflows"
        ci = (workflows / "ci.yml").read_text()
        bot = (workflows / "bot-ci-failure.yml").read_text()
        name = re.search(r"(?m)^name: (.+)$", ci).group(1)
        assert f'workflows: ["{name}"]' in bot
        assert "github.event.workflow_run.path == '.github/workflows/ci.yml'" in bot
