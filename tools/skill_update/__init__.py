"""skill-update — check for a newer toolchain release via GitHub tags.

No PyPI: the toolchain installs from the git checkout (scripts/install.sh) and
updates are tracked by comparing the installed package version against the repo's
latest GitHub tag. Version parsing and comparison are pure; the network call is
isolated in the CLI.
"""

from __future__ import annotations

__version__ = "0.1.0"
