---
name: setup
description: Install or update the ldatb/skills toolchain on this machine. Use when the user wants to install the skills, set up the CLIs, or check for toolchain updates.
---

The skills call CLI tools — `skill-lint`, `skill-gate`, and friends. This skill puts those tools on PATH and checks for updates. The install is a script, not a list of manual steps.

## Steps

1. **Check uv.** Confirm `uv` is installed with `uv --version`. The toolchain installs through uv; without it, point the user at https://docs.astral.sh/uv/.

2. **Install.** Run `./scripts/install.sh` from the repo root. The script installs the CLIs (skill-lint, skill-new, skill-gate, skill-changelog, skill-docs, skill-update) onto PATH.

3. **Verify.** Run `skill-lint --version`. A version string confirms the tools resolve on PATH; a "command not found" means the shell path needs `uv tool update-shell` and a restart.

4. **Check for updates.** Run `skill-update`. The command compares the installed version against the latest GitHub tag and prints the upgrade command when a newer one exists.
