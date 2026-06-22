#!/usr/bin/env python3
"""Zero-install runner for pre-commit.

pre-commit invokes this by path from the repo root, so the package never has to be
installed into the hook environment. It puts ``tools/`` on the path and delegates
to the CLI.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill_lint.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
