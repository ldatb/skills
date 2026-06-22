#!/usr/bin/env bash
# Deterministic CRUD + correlation helper for an Obsidian second-brain vault.
# Capture life/work/project notes fast, link entities, and find them again — with
# no destructive operation beyond a single guarded, in-vault delete.
#
#   vault.sh capture <type> <title>   -> create a typed note, print its path
#   vault.sh append  <note> <text>    -> append a timestamped bullet (atomic)
#   vault.sh link    <from> <to>      -> add a [[wikilink]] under "## Related"
#   vault.sh daily                    -> create-or-open today's daily note
#   vault.sh find    <query>          -> list notes matching tag/title/text
#   vault.sh rm      <note>           -> guarded delete of one note inside the vault
#   vault.sh --selftest               -> build a temp vault, exercise all of the above
#
# Vault root resolves from $VAULT (else ./vault). Types: person project meeting
# idea task decision daily. Shell, not Python: the job is slug + file plumbing.
# Bash is required for `set -o pipefail`; the rest stays POSIX-clean. Filenames
# never overwrite — uniqueness comes from a noclobber (`set -C`) reservation loop,
# the shell's O_EXCL, mirroring skillkit.unique_path. Deletion goes through a guard
# that refuses the vault root and anything outside it, mirroring skillkit.safe_remove.
set -euo pipefail

TYPES="person project meeting idea task decision daily"

# --- helpers ---------------------------------------------------------------

# Canonical absolute path of an existing directory. `CDPATH= cd` neutralizes a
# user CDPATH for this one command so resolution is deterministic.
abspath_dir() {
  # shellcheck disable=SC1007  # `CDPATH= cd` deliberately empties CDPATH here.
  CDPATH= cd -- "$1" && pwd -P
}

# Resolve the vault root (env override, then ./vault), created if absent.
vault_root() {
  local root="${VAULT:-./vault}"
  mkdir -p "$root"
  abspath_dir "$root"
}

# Deterministic, filesystem-safe slug from a title: lowercase, non-alphanumerics
# to hyphens, runs collapsed, ends trimmed. Empty input yields "untitled".
slugify() {
  local s
  s=$(printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -e 's/[^a-z0-9]\{1,\}/-/g' -e 's/^-\{1,\}//' -e 's/-\{1,\}$//')
  [ -n "$s" ] && printf '%s' "$s" || printf '%s' "untitled"
}

# Reject an unknown note type at the boundary with a clear message.
require_type() {
  echo "$TYPES" | grep -qw -- "$1" \
    || { echo "unknown type: $1 (allowed: $TYPES)" >&2; return 2; }
}

# Reserve a brand-new path under a directory, never overwriting. `set -C`
# (noclobber) makes the `>` redirect fail if the candidate exists — the shell's
# O_EXCL — so a uniqueness loop appends -2, -3, ... until a name is won.
# Echoes the reserved (now-empty) path. Mirrors skillkit.unique_path semantics.
reserve_path() {
  local dir="$1" base="$2" ext="$3" n=1 candidate
  mkdir -p "$dir"
  while :; do
    if [ "$n" -eq 1 ]; then
      candidate="$dir/$base$ext"
    else
      candidate="$dir/$base-$n$ext"
    fi
    if (set -C; : > "$candidate") 2>/dev/null; then
      printf '%s' "$candidate"
      return 0
    fi
    n=$((n + 1))
    [ "$n" -le 10000 ] || { echo "could not reserve a unique path in $dir" >&2; return 1; }
  done
}

# Write data to a path atomically: temp file in the same directory, then mv. A
# reader sees the old file or the new, never a half-written one.
atomic_write() {
  local target="$1" data="$2" dir tmp
  dir=$(dirname -- "$target")
  mkdir -p "$dir"
  tmp=$(mktemp "$dir/.vault.XXXXXX")
  printf '%s' "$data" > "$tmp"
  mv -f "$tmp" "$target"
}

# Resolve a note reference to an existing file path inside the vault. Accepts an
# absolute path, a vault-relative path, a bare filename, or a title/slug. Echoes
# the path, or returns 3 when no single match is found.
resolve_note() {
  local root="$1" ref="$2" cand slug hit
  if [ -f "$ref" ]; then printf '%s' "$ref"; return 0; fi
  cand="$root/$ref"
  [ -f "$cand" ] && { printf '%s' "$cand"; return 0; }
  cand="$root/$ref.md"
  [ -f "$cand" ] && { printf '%s' "$cand"; return 0; }
  slug=$(slugify "$ref")
  hit=$(find "$root" -type f -name "$slug.md" 2>/dev/null | head -n 1)
  [ -n "$hit" ] && { printf '%s' "$hit"; return 0; }
  hit=$(find "$root" -type f -name "$slug-*.md" 2>/dev/null | sort | head -n 1)
  [ -n "$hit" ] && { printf '%s' "$hit"; return 0; }
  echo "note not found: $ref" >&2
  return 3
}

# Render the YAML-frontmatter + body template for a note type. Frontmatter is
# uniform across types (so correlation queries stay simple); the type drives the
# tag, the heading set, and the type-specific fields.
render_template() {
  local type="$1" title="$2" today="$3"
  printf '%s\n' '---'
  printf 'title: "%s"\n' "$title"
  printf 'type: %s\n' "$type"
  printf 'created: %s\n' "$today"
  printf 'tags: [%s]\n' "$type"
  case "$type" in
    person)   printf 'company:\nrole:\n' ;;
    project)  printf 'status: active\nowner:\n' ;;
    meeting)  printf 'date: %s\nattendees: []\n' "$today" ;;
    decision) printf 'date: %s\nstatus: proposed\n' "$today" ;;
    task)     printf 'status: todo\ndue:\n' ;;
    idea)     printf 'status: seed\n' ;;
    daily)    printf 'date: %s\n' "$today" ;;
  esac
  printf '%s\n\n' '---'
  printf '# %s\n\n' "$title"
  case "$type" in
    meeting)  printf '## Notes\n\n## Decisions\n\n## Action items\n\n' ;;
    decision) printf '## Context\n\n## Decision\n\n## Consequences\n\n' ;;
    daily)    printf '## Log\n\n## Tasks\n\n' ;;
    *)        printf '## Notes\n\n' ;;
  esac
  printf '## Related\n\n'
}

# --- subcommands -----------------------------------------------------------

# capture <type> <title>: create a typed note with a deterministic slug and a
# collision-free filename. Never overwrites; prints the created path.
cmd_capture() {
  [ "$#" -eq 2 ] || { echo "usage: vault.sh capture <type> <title>" >&2; return 2; }
  local type="$1" title="$2" root slug today path
  require_type "$type" || return 2
  root=$(vault_root)
  slug=$(slugify "$title")
  today=$(date +%Y-%m-%d)
  path=$(reserve_path "$root/$type" "$slug" ".md")
  atomic_write "$path" "$(render_template "$type" "$title" "$today")"
  printf '%s\n' "$path"
}

# append <note> <text>: add a timestamped bullet under the note's "## Log"
# section, atomically. The bullet lands at the top of Log (newest first) so
# captured entries never bleed into "## Related"; a missing Log is created after
# the H1 title.
cmd_append() {
  [ "$#" -eq 2 ] || { echo "usage: vault.sh append <note> <text>" >&2; return 2; }
  local root note text stamp body bullet
  root=$(vault_root)
  note=$(resolve_note "$root" "$1")
  text="$2"
  stamp=$(date +%Y-%m-%dT%H:%M)
  bullet="- $stamp $text"
  body=$(cat -- "$note")
  if printf '%s' "$body" | grep -q '^## Log'; then
    atomic_write "$note" "$(printf '%s' "$body" \
      | awk -v b="$bullet" '
          /^## Log/ { print; print b; next }
          { print }
        ')"
  elif printf '%s' "$body" | grep -q '^# '; then
    atomic_write "$note" "$(printf '%s' "$body" \
      | awk -v b="$bullet" '
          !done && /^# / { print; print ""; print "## Log"; print b; done=1; next }
          { print }
        ')"
  else
    atomic_write "$note" "$(printf '%s\n\n## Log\n%s\n' "$body" "$bullet")"
  fi
  printf '%s\n' "$note"
}

# link <from> <to>: add a [[wikilink]] to <to> in <from> under "## Related",
# creating the section when absent. Idempotent: an existing link is not doubled.
cmd_link() {
  [ "$#" -eq 2 ] || { echo "usage: vault.sh link <from> <to>" >&2; return 2; }
  local root from to_path to_slug wikilink body
  root=$(vault_root)
  from=$(resolve_note "$root" "$1")
  if to_path=$(resolve_note "$root" "$2" 2>/dev/null); then
    to_slug=$(basename -- "$to_path" .md)
  else
    to_slug=$(slugify "$2")
  fi
  wikilink="- [[$to_slug]]"
  body=$(cat -- "$from")
  if printf '%s' "$body" | grep -qF -- "[[$to_slug]]"; then
    printf '%s\n' "$from"
    return 0
  fi
  if printf '%s' "$body" | grep -q '^## Related'; then
    atomic_write "$from" "$(printf '%s' "$body" \
      | awk -v link="$wikilink" '
          /^## Related/ { print; print link; next }
          { print }
        ')"
  else
    atomic_write "$from" "$(printf '%s\n\n## Related\n%s\n' "$body" "$wikilink")"
  fi
  printf '%s\n' "$from"
}

# daily: create-or-open today's daily note. Idempotent — an existing note for
# today is returned untouched, so re-running never duplicates or overwrites.
cmd_daily() {
  local root today path
  root=$(vault_root)
  today=$(date +%Y-%m-%d)
  path="$root/daily/$today.md"
  if [ -f "$path" ]; then
    printf '%s\n' "$path"
    return 0
  fi
  mkdir -p "$root/daily"
  atomic_write "$path" "$(render_template daily "$today" "$today")"
  printf '%s\n' "$path"
}

# find <query>: list vault notes whose tag, title, or text matches the query.
# Prints matching paths; exit 0 even on no match (an empty result is not an error).
cmd_find() {
  [ "$#" -eq 1 ] || { echo "usage: vault.sh find <query>" >&2; return 2; }
  local root
  root=$(vault_root)
  grep -rliIF -- "$1" "$root" --include='*.md' 2>/dev/null | sort || true
}

# rm <note>: delete a single note, only inside the vault. Refuses the vault root
# itself and anything outside it (mirrors skillkit.safe_remove). The one
# destructive path in this tool, structurally guarded against mass deletion.
cmd_rm() {
  [ "$#" -eq 1 ] || { echo "usage: vault.sh rm <note>" >&2; return 2; }
  local root note note_real root_real arg_real
  root=$(vault_root)
  root_real=$(abspath_dir "$root")
  # Refuse the vault root up front, before resolution can reinterpret it.
  arg_real=$(abspath_dir "$(dirname -- "$1")" 2>/dev/null)/$(basename -- "$1") || arg_real=""
  [ "$arg_real" = "$root_real" ] && { echo "refusing to remove vault root itself" >&2; return 2; }
  note=$(resolve_note "$root" "$1")
  note_real=$(abspath_dir "$(dirname -- "$note")")/$(basename -- "$note")
  case "$note_real" in
    "$root_real") echo "refusing to remove vault root itself" >&2; return 2 ;;
    "$root_real"/*) : ;;
    *) echo "refusing to remove outside vault: $note_real" >&2; return 2 ;;
  esac
  [ -d "$note_real" ] && { echo "refusing to remove a directory: $note_real" >&2; return 2; }
  rm -- "$note_real"
  printf 'removed: %s\n' "$note_real"
}

# --- selftest --------------------------------------------------------------

# Build a throwaway vault, exercise every subcommand, and assert structure (not
# exact timestamps). Cleans up only the mktemp-owned directory. Exit 0 on success.
selftest() {
  local tmp out person project meeting

  tmp=$(mktemp -d "${TMPDIR:-/tmp}/second-brain.XXXXXX")
  trap 'test -n "${tmp:-}" && test -d "$tmp" && find "$tmp" -mindepth 0 -maxdepth 4 -delete' EXIT
  export VAULT="$tmp/vault"

  # slugify is deterministic and filesystem-safe.
  [ "$(slugify 'Ada Lovelace!')" = "ada-lovelace" ] || { echo "FAIL: slugify basic"; exit 1; }
  [ "$(slugify '  Q3   Roadmap  ')" = "q3-roadmap" ] || { echo "FAIL: slugify spaces"; exit 1; }
  [ "$(slugify '@@@')" = "untitled" ] || { echo "FAIL: slugify empty"; exit 1; }

  # unknown type is rejected.
  cmd_capture bogus "x" 2>/dev/null && { echo "FAIL: bad type accepted"; exit 1; } || true

  # capture creates a typed note with frontmatter and a slug filename.
  person=$(cmd_capture person "Ada Lovelace")
  [ -f "$person" ] || { echo "FAIL: person note not created"; exit 1; }
  case "$person" in */person/ada-lovelace.md) : ;; *) echo "FAIL: person path ($person)"; exit 1 ;; esac
  grep -q '^type: person$' "$person" || { echo "FAIL: person frontmatter type"; exit 1; }
  grep -q '^## Related$' "$person" || { echo "FAIL: person Related section"; exit 1; }

  # capture never overwrites: a second person of the same title gets a -2 name.
  out=$(cmd_capture person "Ada Lovelace")
  case "$out" in */person/ada-lovelace-2.md) : ;; *) echo "FAIL: collision suffix ($out)"; exit 1 ;; esac
  [ "$out" != "$person" ] || { echo "FAIL: collision overwrote"; exit 1; }

  project=$(cmd_capture project "Q3 Roadmap")
  grep -q '^status: active$' "$project" || { echo "FAIL: project status field"; exit 1; }

  meeting=$(cmd_capture meeting "Kickoff sync")
  grep -q '^## Action items$' "$meeting" || { echo "FAIL: meeting headings"; exit 1; }

  # append adds a timestamped bullet under ## Log (assert bullet + text + section,
  # not the exact time), and never below ## Related.
  cmd_append "$meeting" "agreed on scope" >/dev/null
  grep -q -- '- .* agreed on scope$' "$meeting" || { echo "FAIL: append bullet"; exit 1; }
  grep -q '^## Log$' "$meeting" || { echo "FAIL: append Log section"; exit 1; }
  awk '/^## Log$/{l=NR} /agreed on scope/{b=NR} /^## Related$/{r=NR}
       END{exit !(l<b && b<r)}' "$meeting" \
    || { echo "FAIL: append bullet not between Log and Related"; exit 1; }

  # link adds a [[wikilink]] under ## Related, and is idempotent.
  cmd_link "$meeting" "$person" >/dev/null
  grep -qF -- '[[ada-lovelace]]' "$meeting" || { echo "FAIL: link to person"; exit 1; }
  cmd_link "$meeting" "Q3 Roadmap" >/dev/null
  grep -qF -- '[[q3-roadmap]]' "$meeting" || { echo "FAIL: link to project by title"; exit 1; }
  cmd_link "$meeting" "$person" >/dev/null
  [ "$(grep -cF -- '[[ada-lovelace]]' "$meeting")" -eq 1 ] || { echo "FAIL: link not idempotent"; exit 1; }

  # link creates the ## Related section when a note lacks one.
  printf '%s\n' '# bare' > "$tmp/vault/bare.md"
  cmd_link "$tmp/vault/bare.md" "Ada Lovelace" >/dev/null
  grep -q '^## Related$' "$tmp/vault/bare.md" || { echo "FAIL: Related not created"; exit 1; }
  grep -qF -- '[[ada-lovelace]]' "$tmp/vault/bare.md" || { echo "FAIL: link into bare note"; exit 1; }

  # daily is idempotent: same path twice, no duplicate.
  local d1 d2
  d1=$(cmd_daily); d2=$(cmd_daily)
  [ "$d1" = "$d2" ] || { echo "FAIL: daily not idempotent"; exit 1; }
  [ -f "$d1" ] || { echo "FAIL: daily note missing"; exit 1; }
  grep -q '^## Log$' "$d1" || { echo "FAIL: daily template"; exit 1; }

  # find locates a note by its content.
  out=$(cmd_find "agreed on scope")
  case "$out" in *"$meeting"*) : ;; *) echo "FAIL: find by text"; exit 1 ;; esac
  # find by tag matches the project frontmatter.
  out=$(cmd_find "tags: [project]")
  case "$out" in *"$project"*) : ;; *) echo "FAIL: find by tag"; exit 1 ;; esac

  # rm guard: the root guard fires with its own message, not a generic miss.
  out=$(cmd_rm "$tmp/vault" 2>&1) && { echo "FAIL: rm accepted vault root"; exit 1; } || true
  case "$out" in *"vault root"*) : ;; *) echo "FAIL: rm root message ($out)"; exit 1 ;; esac
  cmd_rm "$tmp/outside.md" 2>/dev/null && { echo "FAIL: rm accepted missing/outside"; exit 1; } || true
  cmd_rm "$person" >/dev/null
  [ -f "$person" ] && { echo "FAIL: rm did not delete note"; exit 1; } || true

  echo "vault selftest: ok"
}

# --- dispatch --------------------------------------------------------------

usage() {
  echo "usage: vault.sh <capture|append|link|daily|find|rm> [args]" >&2
  echo "       vault.sh --selftest" >&2
  echo "types: $TYPES" >&2
  echo "vault root: \$VAULT (default ./vault)" >&2
}

main() {
  case "${1:-}" in
    --selftest) selftest; exit 0 ;;
    -h|--help) usage; exit 0 ;;
  esac
  [ "$#" -ge 1 ] || { usage; exit 2; }
  local sub="$1"; shift
  case "$sub" in
    capture) cmd_capture "$@" ;;
    append)  cmd_append "$@" ;;
    link)    cmd_link "$@" ;;
    daily)   cmd_daily "$@" ;;
    find)    cmd_find "$@" ;;
    rm)      cmd_rm "$@" ;;
    *) echo "unknown subcommand: $sub" >&2; usage; exit 2 ;;
  esac
}

main "$@"
