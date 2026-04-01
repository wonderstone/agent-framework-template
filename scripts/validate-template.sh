#!/usr/bin/env bash
# validate-template.sh
#
# Thin wrapper kept for backwards compatibility.
# The structured checks now live in scripts/validate_template.py.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

python3 scripts/validate_template.py
