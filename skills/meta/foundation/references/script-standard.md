# Script standard

A skill reaches for a script whenever the work can be made deterministic. Every script
a skill ships meets this standard, so the agent can trust it the way it trusts a
compiler.

## Rules

1. **One job.** A script does one well-defined thing. Many small scripts beat one
   large one (Kanso). Target under 400 lines.

2. **Explicit interface.** Arguments via `argparse` with `--help`. No positional magic,
   no environment-variable surprises. The signature *is* the contract.

3. **Deterministic output.** Same input, same output. No reliance on wall-clock,
   network, or locale unless that is the explicit job — and if it is, isolate it behind
   a flag.

4. **Exit codes are the truth.** `0` success, non-zero failure. The agent branches on
   the exit code, never on parsing prose from stdout.

5. **Use the primitives.** File creation goes through `skillkit.unique_path`; writes go
   through `atomic_write`; deletion goes through `safe_remove`. Never hand-roll these.

6. **No unguarded destruction.** No `rm -rf`, no `git reset --hard`, no `DROP` without a
   guarded helper and an explicit, narrow scope.

7. **Concurrency-safe.** Assume the script runs 50 times at once. Reserve names
   atomically; never check-then-write.

8. **Validate at the boundary.** Reject malformed input fast, with a clear message. Do
   not trust arguments, file contents, or API responses.

9. **Tested.** A script ships with a test that fails if the logic breaks. Run via
   `make test`. No test, not done.

## Skeleton

```python
#!/usr/bin/env python3
"""One-line statement of the single job."""

from __future__ import annotations

import argparse

from skillkit import atomic_write, unique_path


def run(target: str) -> int:
    # validate input at the boundary, do the one job, return an exit code
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One-line statement of the single job.")
    parser.add_argument("--target", required=True)
    args = parser.parse_args(argv)
    return run(args.target)


if __name__ == "__main__":
    raise SystemExit(main())
```

## Why Python here

Python is the toolchain language for this repo: the richest ecosystem for the text and
AST work the linters do, zero build step, and the fastest path to iterate a rule set
that grows weekly (Kaizen). A script in another language is fine when the job demands
it — but it meets the same nine rules above.
