---
name: changelog-gen
description: Generate a CHANGELOG from conventional commits, deterministically. Use when the user wants to update the changelog, cut release notes, or summarize commits since a tag.
---

The changelog is generated, never hand-written. `skill-changelog` parses conventional commits into a Keep-a-Changelog section, so the same history always yields the same notes.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Pick the range.** Identify the previous release tag and the target ref. The range runs from the previous tag to `HEAD`.

2. **Generate.** Run `skill-changelog --version <version> --from <previous-tag> --to HEAD`. The output is a grouped section: features, fixes, breaking changes.

3. **Review the groups.** Read the section. A commit that landed in the wrong group points to a malformed commit subject, not a tool bug.

4. **Write the file.** Rerun with `--write CHANGELOG.md` to prepend the section above prior entries. The previous entries stay intact below.

5. **Confirm.** Open `CHANGELOG.md` and confirm the new version sits at the top with the prior history beneath it.
