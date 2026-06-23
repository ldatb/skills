#!/usr/bin/env bash
# Render a Markdown file to a .docx deterministically via pandoc, with an optional
# reference-doc style template. The LLM writes the Markdown content; this script
# owns the conversion, so the same content yields the same document every run.
#
#   render.sh <content.md> <out.docx> [reference.docx]  -> render, print "wrote <out>"
#   render.sh --selftest                                -> render a fixture, assert, exit 0
#
# Exit codes: 0 success; 2 missing content file; 3 pandoc not on PATH.
set -euo pipefail

# Convert one Markdown source to a .docx. A reference template is applied only
# when the path is given AND the file exists on disk.
render() {
  local src="$1"
  local out="$2"
  local ref="${3:-}"

  if [ ! -f "$src" ]; then
    echo "error: content file not found: $src" >&2
    return 2
  fi
  if ! command -v pandoc >/dev/null 2>&1; then
    echo "error: pandoc is not on PATH" >&2
    return 3
  fi

  if [ -n "$ref" ] && [ -f "$ref" ]; then
    pandoc --from gfm --to docx --output "$out" --reference-doc "$ref" "$src"
  else
    pandoc --from gfm --to docx --output "$out" "$src"
  fi

  echo "wrote $out"
}

# Self-check with no caller input: render a tiny Markdown fixture and assert the
# result is a real docx (its zip container holds word/document.xml). Skips
# cleanly when pandoc is absent so the gate stays green on a bare machine. The
# temp dir is mktemp-owned and pruned only within its own tree.
selftest() {
  if ! command -v pandoc >/dev/null 2>&1; then
    echo "render selftest: skipped (pandoc absent)"
    exit 0
  fi

  local tmp src out
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/docx-render-selftest.XXXXXX")
  # shellcheck disable=SC2317,SC2329  # invoked indirectly via the EXIT trap
  cleanup() {
    if [ -n "${tmp:-}" ] && [ -d "$tmp" ]; then
      find "$tmp" -mindepth 0 -maxdepth 2 -delete 2>/dev/null || true
    fi
    return 0
  }
  trap cleanup EXIT

  src="$tmp/content.md"
  out="$tmp/out.docx"
  printf '# Selftest\n\nA paragraph rendered by pandoc.\n' > "$src"

  render "$src" "$out" >/dev/null

  if [ ! -f "$out" ]; then
    echo "FAIL: render produced no output file" >&2
    exit 1
  fi
  # Capture the listing first, then match it. Piping unzip straight into
  # `grep -q` lets grep close the pipe early, and under `set -o pipefail` the
  # resulting SIGPIPE on unzip would fail a valid render.
  local listing
  listing=$(unzip -l "$out")
  if ! printf '%s\n' "$listing" | grep -q word/document.xml; then
    echo "FAIL: output is not a valid docx (no word/document.xml)" >&2
    exit 1
  fi

  echo "docx render selftest: ok"
}

usage() {
  echo "usage: render.sh <content.md> <out.docx> [reference.docx]" >&2
  echo "       render.sh --selftest" >&2
}

main() {
  case "${1:-}" in
    --selftest) selftest; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    "") usage; exit 2 ;;
    *)
      [ -n "${2:-}" ] || { echo "error: out path is required" >&2; usage; exit 2; }
      render "$1" "$2" "${3:-}"
      ;;
  esac
}

main "$@"
