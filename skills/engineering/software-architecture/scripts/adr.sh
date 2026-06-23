#!/usr/bin/env bash
# adr.sh — own the deterministic shell of an Architecture Decision Record: the
# sequential number, the template, and the collision-free filename. The agent writes
# the Context/Decision/Consequences prose; this script never invents reasoning.
# Deterministic; never overwrites an existing file (Poka-yoke); writes atomically
# (temp + mv); reserves the number from the highest existing ADR (concurrency-aware).
#   adr.sh new "<title>" [dir]   create the next ADR-NNNN-<slug>.md in dir (default docs/adr)
#   adr.sh --selftest
set -euo pipefail

# Lowercase, collapse every non-alphanumeric run to a single hyphen, trim hyphens.
slugify() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
}

# Highest existing ADR number under dir, zero if none. Reads the NNNN field from each
# ADR-NNNN-*.md filename; ignores anything that does not match the shape.
highest_number() {
  local dir="$1" n max=0 base
  for path in "$dir"/ADR-[0-9][0-9][0-9][0-9]-*.md; do
    [ -e "$path" ] || continue
    base="$(basename "$path")"
    n="${base#ADR-}"
    n="${n%%-*}"
    n="$((10#$n))"
    [ "$n" -gt "$max" ] && max="$n"
  done
  printf '%s' "$max"
}

adr_template() { # number title date
  local num="$1" title="$2" date="$3"
  cat <<TMPL
status: proposed
date: ${date}

# ADR-${num}: ${title}

## Status

proposed

## Context

<the forces in play: the requirement, the constraints, the ranked quality attributes
that pressure this choice, and the scale numbers that matter. State the problem so a
reader who was not in the room understands what was being decided and why now.>

## Decision

<the option chosen, stated as one active sentence, then a short paragraph on how it
works — only as far as the decision needs.>

## Consequences

- Positive: <what becomes easier or possible.>
- Negative: <what becomes harder or impossible — the cost accepted. Name at least one.>
- Follow-ups: <the work this decision now requires, if any.>

## Alternatives considered

- <Alternative A>: <what it is, and the one reason it lost.>
- <Alternative B>: <what it is, and the one reason it lost.>
TMPL
}

cmd_new() {
  local title="${1:-}" dir="${2:-docs/adr}" num slug date path tmp
  [ -n "$title" ] || { echo "usage: adr.sh new \"<title>\" [dir]" >&2; return 2; }
  mkdir -p "$dir"
  num="$(printf '%04d' "$(( $(highest_number "$dir") + 1 ))")"
  slug="$(slugify "$title")"
  [ -n "$slug" ] || slug="adr"
  date="$(date +%Y-%m-%d)"
  path="$dir/ADR-${num}-${slug}.md"
  if [ -e "$path" ]; then echo "refusing to overwrite $path" >&2; return 1; fi
  tmp="$(mktemp "$dir/.adr.XXXXXX")"
  adr_template "$num" "$title" "$date" >"$tmp"
  mv "$tmp" "$path"
  echo "$path"
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
  local first second slug
  _SELFTEST_DIR="$(mktemp -d)"
  trap cleanup_selftest EXIT
  first="$(cmd_new "Use a partitioned key value store" "$_SELFTEST_DIR/docs/adr")"
  case "$first" in
    */ADR-0001-*.md) : ;;
    *) echo "FAIL: first ADR not numbered 0001: $first"; exit 1 ;;
  esac
  grep -q '^# ADR-0001: ' "$first" || { echo "FAIL: missing title header"; exit 1; }
  for header in '## Status' '## Context' '## Decision' '## Consequences' '## Alternatives considered'; do
    grep -qF "$header" "$first" || { echo "FAIL: missing section $header"; exit 1; }
  done
  grep -q '^status: proposed$' "$first" || { echo "FAIL: missing status header"; exit 1; }
  second="$(cmd_new "Adopt event driven ingestion" "$_SELFTEST_DIR/docs/adr")"
  case "$second" in
    */ADR-0002-*.md) : ;;
    *) echo "FAIL: second ADR did not increment to 0002: $second"; exit 1 ;;
  esac
  slug="$(slugify 'Use a partitioned key value store!!')"
  [ "$slug" = "use-a-partitioned-key-value-store" ] || { echo "FAIL: bad slug: $slug"; exit 1; }
  echo "adr selftest: ok"
}

main() {
  case "${1:-}" in
    new) shift; cmd_new "${1:-}" "${2:-docs/adr}" ;;
    --selftest) selftest ;;
    *) echo "usage: adr.sh new \"<title>\" [dir]  |  --selftest" >&2; exit 2 ;;
  esac
}

main "$@"
