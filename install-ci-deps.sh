#!/usr/bin/env bash
# Install the dependencies used by CI and review experiments.
set -euo pipefail

python -m pip install --upgrade pip wheel setuptools
python -m pip install --upgrade -r requirements-test.txt
python -m pip install --editable .
