"""skill-changelog — deterministic CHANGELOG from conventional commits.

Parsing and rendering are pure functions: the same commit subjects and version
always produce the same changelog section. Git access and file writing are the only
side effects, isolated in the CLI.
"""

from __future__ import annotations

__version__ = "0.1.0"
