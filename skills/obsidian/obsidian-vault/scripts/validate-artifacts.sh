#!/usr/bin/env bash
# Assert that a compiled vault has every required folder and control file present.
# Pure existence check: the same vault yields the same verdict on every run, with
# no LLM in the path. Shell, not Python -- the job is "do these paths exist?".
#
#   validate-artifacts.sh --vault PATH   -> check the vault, exit 1 if anything missing
#   validate-artifacts.sh --selftest     -> build temp fixtures, assert, exit 0
#
# Read-only: the checker never creates, moves, or deletes a path.
set -euo pipefail

# Required top-level folders of a compiled memory vault.
REQUIRED_DIRS=(
  "People" "Companies" "Projects" "Products" "Topics"
  "Decisions" "Commitments" "Procedures" "Preferences"
  "Context Packs" "Sources" "Maps" "Reports" "_tools"
)

# Required control files at the vault root.
REQUIRED_FILES=(
  "README.md" "SOURCE-MANIFEST.md" "VALIDATION-REPORT.md"
  "COMPLETION-AUDIT.md" "INGESTION-LOG.md" "state.json"
)

# Check one vault root. Prints each missing artifact; returns 1 if any missing.
check_vault() {
  local vault="$1"
  local missing=0 d f

  if [ ! -d "$vault" ]; then
    echo "error: vault is not a directory: $vault" >&2
    return 2
  fi

  for d in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$vault/$d" ]; then
      echo "missing directory: $d"
      missing=1
    fi
  done

  for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$vault/$f" ]; then
      echo "missing file: $f"
      missing=1
    fi
  done

  if [ "$missing" -eq 0 ]; then
    echo "validate-artifacts: all required folders and files present"
    return 0
  fi
  return 1
}

# Build a complete, valid vault skeleton under a caller-owned directory.
scaffold_complete() {
  local root="$1" d f
  for d in "${REQUIRED_DIRS[@]}"; do
    mkdir -p "$root/$d"
  done
  for f in "${REQUIRED_FILES[@]}"; do
    printf 'placeholder\n' > "$root/$f"
  done
}

# Self-check with no real vault: a complete skeleton must pass; removing one
# required file and one required directory must fail. Temp dir is mktemp-owned
# and removed only within its own tree.
selftest() {
  local tmp good bad out rc
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/artifacts-selftest.XXXXXX")
  # shellcheck disable=SC2317,SC2329  # invoked indirectly via the EXIT trap
  cleanup() {
    if [ -n "${tmp:-}" ] && [ -d "$tmp" ]; then
      find "$tmp" -mindepth 0 -maxdepth 4 -delete 2>/dev/null || true
    fi
    return 0
  }
  trap cleanup EXIT

  good="$tmp/good"
  mkdir -p "$good"
  scaffold_complete "$good"

  set +e
  out=$(check_vault "$good"); rc=$?
  set -e
  [ "$rc" -eq 0 ] || { echo "FAIL: complete vault rejected: $out"; exit 1; }

  bad="$tmp/bad"
  mkdir -p "$bad"
  scaffold_complete "$bad"
  rm -f "$bad/state.json"
  rmdir "$bad/Sources"

  set +e
  out=$(check_vault "$bad"); rc=$?
  set -e
  [ "$rc" -ne 0 ] || { echo "FAIL: incomplete vault accepted"; exit 1; }
  case "$out" in *"state.json"*) : ;; *) echo "FAIL: missing-file not reported"; exit 1 ;; esac
  case "$out" in *"Sources"*) : ;; *) echo "FAIL: missing-dir not reported"; exit 1 ;; esac

  echo "validate-artifacts selftest: ok"
}

usage() {
  echo "usage: validate-artifacts.sh --vault PATH" >&2
  echo "       validate-artifacts.sh --selftest" >&2
}

main() {
  case "${1:-}" in
    --selftest) selftest; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    --vault)
      [ -n "${2:-}" ] || { echo "error: --vault needs a path" >&2; usage; exit 2; }
      check_vault "$2"
      ;;
    *) usage; exit 2 ;;
  esac
}

main "$@"
