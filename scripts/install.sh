#!/usr/bin/env bash
# Install the ldatb/skills toolchain (skill-lint, skill-gate, ...) onto PATH.
# Idempotent: re-run to update after `git pull`. Requires uv.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "error: uv is required — https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

# Installs the project's console scripts into uv's tool bin (usually ~/.local/bin).
uv tool install --force "$REPO_ROOT"

echo
echo "installed: skill-lint, skill-new, skill-gate, skill-changelog, skill-docs, skill-update"
echo "if the commands are not found, run: uv tool update-shell  (then restart your shell)"
