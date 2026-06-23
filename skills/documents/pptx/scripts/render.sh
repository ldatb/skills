#!/usr/bin/env bash
# render.sh — render a Markdown slide deck to .pptx with pandoc, deterministically.
# The model writes content (Markdown); this script owns the render so the same
# input yields the same deck. In pandoc's Markdown-to-slides model a level-1 (or the
# configured slide-level) heading starts a new slide, so one '#' heading == one slide.
# A reference template, when supplied and present, carries the brand (theme, fonts).
# Shell, not Python: the job is input validation plus one pandoc call.
#   render.sh <content.md> <out.pptx> [reference.pptx]   render the deck
#   render.sh --selftest                                 render a tiny deck and check it
set -euo pipefail

render() { # src out [ref] -> writes out via pandoc; returns 2/3 on a boundary failure
  local src="$1" out="$2" ref="${3:-}"
  [ -f "$src" ] || { echo "render: no such content file: $src" >&2; return 2; }
  command -v pandoc >/dev/null 2>&1 || { echo "render: pandoc not on PATH" >&2; return 3; }
  if [ -n "$ref" ] && [ -f "$ref" ]; then
    pandoc --from gfm --to pptx --reference-doc "$ref" --output "$out" "$src"
  else
    pandoc --from gfm --to pptx --output "$out" "$src"
  fi
  echo "wrote $out"
}

cleanup() { # remove only the two files this selftest made, then the now-empty dir
  local dir="$1"
  rm -f "$dir/deck.md" "$dir/deck.pptx"
  rmdir "$dir" 2>/dev/null || true
}

selftest() {
  command -v pandoc >/dev/null 2>&1 || { echo "render selftest: skipped (pandoc absent)"; exit 0; }
  local dir src out
  dir="$(mktemp -d)"
  src="$dir/deck.md"
  out="$dir/deck.pptx"
  cat >"$src" <<'MD'
# First slide

- One idea, stated once
- A second supporting point

# Second slide

- One idea per slide
- Bullets carry the detail
MD
  local listing rc=0
  render "$src" "$out" >/dev/null || { echo "render selftest: FAIL (render errored)"; cleanup "$dir"; exit 1; }
  # Capture the archive listing first, then match the captured text. Piping unzip
  # straight into `grep -q` races: grep exits on the first match and unzip dies of
  # SIGPIPE (141), which `pipefail` would surface as a flaky failure.
  listing="$(unzip -l "$out")" || rc=$?
  [ "$rc" -eq 0 ] || { echo "pptx render selftest: FAIL (unzip rc=$rc)"; cleanup "$dir"; exit 1; }
  case "$listing" in
    *ppt/presentation.xml*)
      cleanup "$dir"
      echo "pptx render selftest: ok" ;;
    *)
      cleanup "$dir"
      echo "pptx render selftest: FAIL (no ppt/presentation.xml)"
      exit 1 ;;
  esac
}

main() {
  if [ "${1:-}" = "--selftest" ]; then selftest; exit 0; fi
  if [ "$#" -lt 2 ]; then
    echo "usage: render.sh <content.md> <out.pptx> [reference.pptx]" >&2
    echo "       render.sh --selftest" >&2
    exit 2
  fi
  render "$1" "$2" "${3:-}"
}

main "$@"
