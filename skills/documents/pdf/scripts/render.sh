#!/usr/bin/env bash
# Deterministic PDF renderer. The LLM writes content as Markdown; this script
# renders it to PDF through pandoc and a real PDF engine, so the same Markdown
# yields the same document on every run. No reportlab/weasyprint code is written
# per run — the styling lives in CSS or a pandoc template the script applies.
#   render.sh content.md out.pdf                      -> render with an auto-detected engine
#   render.sh content.md out.pdf --engine weasyprint  -> render with a named engine
#   render.sh content.md out.pdf --css print.css      -> style via CSS (CSS engines only)
#   render.sh --selftest                              -> self-check, engine-tolerant
#
# Shell, not Python: the job is flag parsing plus one pandoc invocation. No
# destructive operation runs here — the script only reads the source and writes
# the named output (plus a self-cleaning temp dir during --selftest).
set -euo pipefail

# PDF engines in detection order. The CSS engines (weasyprint, wkhtmltopdf) honor
# a --css stylesheet; the rest are LaTeX/typst engines pandoc drives directly.
ENGINES="weasyprint wkhtmltopdf typst tectonic xelatex pdflatex"
CSS_ENGINES="weasyprint wkhtmltopdf"

# Echo the first engine on PATH from ENGINES; echo nothing when none is present.
detect_engine() {
  local candidate
  for candidate in $ENGINES; do
    if command -v "$candidate" >/dev/null 2>&1; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

# Test membership of an engine in the CSS-engine set as a fixed word.
is_css_engine() {
  echo "$CSS_ENGINES" | grep -qwF -- "$1"
}

# Render one Markdown file to PDF. Args: src out engine css (css may be "").
render() {
  local src="$1" out="$2" engine="$3" css="$4"
  if is_css_engine "$engine" && [ -n "$css" ]; then
    pandoc --from gfm --output "$out" --pdf-engine "$engine" --css "$css" "$src"
  else
    pandoc --from gfm --output "$out" --pdf-engine "$engine" "$src"
  fi
}

# Assert the rendered file exists and begins with the %PDF magic bytes. Returns
# non-zero with a message on stderr when either check fails.
assert_pdf() {
  local out="$1" magic
  [ -f "$out" ] || { echo "no output written: $out" >&2; return 1; }
  magic=$(head -c 4 "$out" 2>/dev/null || true)
  [ "$magic" = "%PDF" ] || { echo "output is not a PDF (missing %PDF magic): $out" >&2; return 1; }
}

# Self-check. With no engine present this prints a skip line and exits zero, so
# the gate stays green in an engine-free environment. With an engine present it
# renders a tiny Markdown file to a temp PDF and asserts the magic bytes.
selftest() {
  local engine tmp src out
  if ! engine=$(detect_engine); then
    echo "pdf render selftest: skipped (no PDF engine)"
    exit 0
  fi
  tmp=$(mktemp -d "${TMPDIR:-/tmp}/pdf-render.XXXXXX")
  trap 'test -n "${tmp:-}" && test -d "$tmp" && find "$tmp" -mindepth 0 -maxdepth 2 -delete' EXIT
  src="$tmp/sample.md"
  out="$tmp/sample.pdf"
  printf '%s\n' '# Selftest' '' 'A tiny paragraph rendered for the self-check.' > "$src"
  render "$src" "$out" "$engine" "" || { echo "pdf render selftest: FAIL (render error with $engine)"; exit 1; }
  assert_pdf "$out" || { echo "pdf render selftest: FAIL (bad output from $engine)"; exit 1; }
  echo "pdf render selftest: ok"
}

usage() {
  echo "usage: render.sh <content.md> <out.pdf> [--engine ENGINE] [--css FILE]" >&2
  echo "       render.sh --selftest" >&2
}

main() {
  if [ "${1:-}" = "--selftest" ]; then selftest; exit 0; fi
  if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then usage; exit 0; fi

  local src="" out="" engine="" css=""
  # Positional src/out come first; flags follow. Keep the parser flat.
  [ "$#" -ge 2 ] || { usage; exit 2; }
  src="$1"; out="$2"; shift 2
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --engine) engine="${2:-}"; shift 2 ;;
      --css)    css="${2:-}"; shift 2 ;;
      *) echo "unknown argument: $1" >&2; usage; exit 2 ;;
    esac
  done

  [ -f "$src" ] || { echo "content file not found: $src" >&2; exit 2; }

  if [ -z "$engine" ]; then
    engine=$(detect_engine) || {
      echo "no PDF engine found; install one of: weasyprint wkhtmltopdf typst tectonic xelatex" >&2
      exit 3
    }
  fi

  render "$src" "$out" "$engine" "$css"
  echo "wrote $out"
}

main "$@"
