# Japanese quality principles, mapped to mechanics

These are not decoration. Each principle names a concrete mechanism in this repo. The
standard is the one from the Toyota Production System and the *monozukuri* (ものづくり,
"the craft of making") tradition: quality is built in, never inspected in afterward.

| Principle | Meaning | Mechanism here |
|-----------|---------|----------------|
| **Poka-yoke** (ポカヨケ) | Mistake-proofing — make the error impossible, not discouraged | `skillkit.safe_remove` cannot delete outside its root; `skill-new` cannot emit a malformed skill; the destructive-op rule (SK040) blocks inlined `rm -rf` |
| **Jidoka** (自働化) | Autonomation — stop the line the instant a defect appears | `skill-lint --strict` fails the pre-commit hook *and* CI; a violation halts the merge |
| **Genchi Genbutsu** (現地現物) | Go and see — decide from real, observed output | Verify a skill by running the linter and reading its findings; verify registration by reading `plugin.json`, never by assuming |
| **Kaizen** (改善) | Continuous improvement — small, permanent | Every new ambiguity becomes a rule in `rules.yaml` plus a test fixture; the linter only ever grows sharper |
| **Kanso** (簡素) | Simplicity — eliminate clutter | Many small files over few large ones; the shortest skill that works wins; prune no-op lines |
| **Seiri / Seiton / Seiso / Seiketsu / Shitsuke** (5S) | Sort, set in order, shine, standardize, sustain | One category folder per domain; one source of truth per meaning; templates standardize; CI sustains |
| **Shokunin** (職人) | Craftsman's ownership of quality | The author owns the green build; "it mostly works" is not done |
| **Hansei** (反省) | Honest reflection without excuse | When a defect escapes, add the check that would have caught it before moving on |
| **Muda / Mura / Muri** (無駄・斑・無理) | Waste / unevenness / overburden | No-op lines are *muda*; nondeterministic drift is *mura*; context explosion is *muri* on the model |

## How they compose

The three load-bearing ones, in order of use:

1. **Poka-yoke first.** Before writing a warning, ask whether the mistake can be made
   impossible. A guarded primitive beats a cautionary sentence every time.
2. **Jidoka second.** Whatever cannot be designed out is caught by a gate that stops
   the line. The linter is the andon cord; a red build is not negotiable.
3. **Kaizen forever.** Each escape becomes a permanent check, so the same defect never
   ships twice.

Genchi Genbutsu sits underneath all three: every claim of "done" is backed by observed
output, never by assumption.
