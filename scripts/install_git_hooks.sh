#!/usr/bin/env bash
# Install repository-local git hooks shipped by the framework.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "${ROOT}" config core.hooksPath .githooks
chmod +x "${ROOT}/.githooks/pre-commit" "${ROOT}/.githooks/pre-push"

echo "Installed git hooks from .githooks/"
echo "Git core.hooksPath is now set to .githooks"