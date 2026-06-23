#!/usr/bin/env bash
# handoff.sh — stamp the structure of a handoff document so a fresh reader can resume
# work without asking the author a question. The script owns the structure (every run
# the same headers); the agent fills each section with judgment. Deterministic; never
# overwrites an existing file (Poka-yoke); writes atomically (temp + mv).
#   handoff.sh new [path]    create a handoff (default HANDOFF.md) only if absent
#   handoff.sh --selftest
set -euo pipefail

handoff_template() {
  cat <<'TMPL'
# Handoff: <fill: what the work must ultimately deliver>

## Summary
<one or two sentences: the goal, the yardstick every section below is measured against>

## Current state
<where the work stands now: the branch, what builds and runs, what is broken, the last action>

## What's done
<the finished work, so the reader neither redoes it nor distrusts it>

## What's left / next steps
<each remaining item as a concrete next action: the file to open, the function to change,
the command to run, the expected outcome — specific enough to start cold>

## How to run / build / test
<the exact commands that build, run, and prove the work correct, with the result to expect>

## Risks & gotchas
<the traps a reader steps on without warning: the flaky test, the service that must boot
first, the off-by-one that already cost an hour, the env var with no default>

## Key files & links
<the files changed, created, or deleted, plus external artifacts: a migration, a preview,
a draft PR, a design doc — the map of the blast radius>

## Contacts / owners
<who or what clears each blocker, who owns each area, who decided the open questions>
TMPL
}

status() { [ -f "$1" ] && echo present || echo MISSING; }

write_new() { # path template-fn — create only if absent, atomically
  local path="$1" fn="$2" tmp
  if [ -e "$path" ]; then echo "kept existing $path"; return 0; fi
  tmp="$(mktemp "$(dirname "$path")/.handoff.XXXXXX")"
  "$fn" >"$tmp"
  mv "$tmp" "$path"
  echo "created $path"
}

cmd_new() {
  local path="${1:-HANDOFF.md}" dir
  dir="$(dirname "$path")"
  [ -d "$dir" ] || { echo "no such directory: $dir" >&2; return 2; }
  write_new "$path" handoff_template
}

# Narrow cleanup: delete only the single mktemp -d sandbox, guarded so it can never
# point outside a temp root, and never the root itself. No broad inline destruction.
_SELFTEST_DIR=""
cleanup_selftest() {
  local d="$_SELFTEST_DIR"
  _SELFTEST_DIR=""
  [ -n "$d" ] || return 0
  case "$d" in
    "${TMPDIR:-/tmp}"/*|/tmp/*|/var/folders/*) [ -d "$d" ] && rm -rf -- "$d" ;;
    *) echo "refusing to remove non-temp path: $d" >&2 ;;
  esac
}

selftest() {
  local f
  _SELFTEST_DIR="$(mktemp -d)"
  trap cleanup_selftest EXIT
  f="$_SELFTEST_DIR/HANDOFF.md"
  cmd_new "$f" >/dev/null
  [ -f "$f" ] || { echo "FAIL: handoff not created"; exit 1; }
  grep -q '^# Handoff:' "$f" || { echo "FAIL: missing title header"; exit 1; }
  grep -q '^## Summary' "$f" || { echo "FAIL: missing Summary header"; exit 1; }
  grep -q '^## Current state' "$f" || { echo "FAIL: missing Current state header"; exit 1; }
  grep -q "^## What's done" "$f" || { echo "FAIL: missing What's done header"; exit 1; }
  grep -q "^## What's left / next steps" "$f" || { echo "FAIL: missing next-steps header"; exit 1; }
  grep -q '^## How to run / build / test' "$f" || { echo "FAIL: missing run/build/test header"; exit 1; }
  grep -q '^## Risks & gotchas' "$f" || { echo "FAIL: missing Risks header"; exit 1; }
  grep -q '^## Key files & links' "$f" || { echo "FAIL: missing Key files header"; exit 1; }
  grep -q '^## Contacts / owners' "$f" || { echo "FAIL: missing Contacts header"; exit 1; }
  printf 'marker\n' >>"$f"
  cmd_new "$f" >/dev/null
  grep -q marker "$f" || { echo "FAIL: overwrote existing handoff"; exit 1; }
  echo "handoff selftest: ok"
}

main() {
  case "${1:-}" in
    new) shift; cmd_new "${1:-HANDOFF.md}" ;;
    --selftest) selftest ;;
    *) echo "usage: handoff.sh new [path]  |  --selftest" >&2; exit 2 ;;
  esac
}

main "$@"
