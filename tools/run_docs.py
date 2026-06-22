#!/usr/bin/env python3
"""Zero-install runner for pre-commit: checks that Markdown links resolve.

Like run_lint.py, pre-commit invokes this by path so the package is never installed
into the hook environment.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill_docs.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
