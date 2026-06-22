"""skill-docs — deterministic documentation integrity checks.

Today it verifies that every relative link and file reference in Markdown resolves,
so docs cannot silently rot when code moves or is renamed. Checks are pure over file
contents and grow by Kaizen.
"""

from __future__ import annotations

__version__ = "0.1.0"
