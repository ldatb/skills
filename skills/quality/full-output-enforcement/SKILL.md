---
name: full-output-enforcement
description: Enforce complete output — every requested item delivered in full, every file written end to end, no truncation, no placeholders, no stub handed back as done. Use when a deliverable spans many files or items, when output is long enough to tempt an ellipsis, when writing or editing whole files, when enumerating a list, when handing back generated code, or when a prior turn left "// ... rest" / "fill in the rest" / "(repeat for the others)" / a stub presented as finished.
---

A deliverable is complete when each item the request named is present in full and nothing was silently dropped. Partial work declared finished is the defect this skill exists to stop. The enemy is the convenient shortcut — an ellipsis standing in for code, a "similar to above" standing in for the seventh item, a stub function dressed as a finished one.

Completeness is a contract, not a preference. Run the procedure below before handing any deliverable back. The standard is observable: scan the artifact for banned shortcuts, count delivered items against requested items, and confirm no stub claims completion. Read [the completeness rules](references/completeness-rules.md) for the contract, the banned-shortcut catalog, the large-output protocol, and a worked truncated-vs-complete contrast.

## Steps

1. **List the requested items.** Enumerate what the request named — each file, each function, each list entry, each section — as an explicit checklist. A deliverable cannot be checked complete against an unstated scope, so the checklist is the first artifact. Done when the requested-item count is written down.

2. **Deliver each item in full.** Write every listed item end to end, with no body deferred to a later turn and no placeholder standing in for content. The completeness rules name the [banned shortcuts](references/completeness-rules.md#banned-shortcuts) — ellipsis-omission, "fill in the rest", "similar to above", silent list-dropping, a stub presented as complete. Done when each checklist item has a full body, not a promise of one.

3. **Split large output into complete pieces.** Output too large for one message gets divided across files or messages, each piece whole on its own — never a fragment that trails into an ellipsis. State plainly what remains and continue until the checklist is exhausted. The [large-output protocol](references/completeness-rules.md#handling-genuinely-large-output) governs the split. Done when every piece stands complete and the remainder is named.

4. **Scan for banned shortcuts.** Search the artifact for the omission markers: `...` inside code standing for skipped lines, the phrases "rest of the code" / "fill in" / "similar to above" / "repeat for", and any function body that is a stub where the request asked for an implementation. Done when no ellipsis-omission and no shortcut phrase remains.

5. **Count delivered against requested.** Compare the delivered-item count to the checklist from step 1; a list of N requested items has N present, not N minus the tedious ones. Scope that shrank between request and delivery is the finding. Done when delivered count equals requested count.

6. **Verify claimed done equals observed done.** Confirm each item said to be finished is finished in the artifact, not merely asserted in prose — claimed completion without an observable body is the failure named in [verification-before-completion](references/completeness-rules.md#link-to-verification-before-completion). A stub, a `pass`-body marker, or a "left as an exercise" is not done. Done when every completion claim is backed by a full body in the deliverable.

7. **Report against the three criteria.** State the verdict on each: no ellipsis-omission remains, every requested item is present, no stub is presented as done. A failed criterion blocks the hand-off and sends the deliverable back to step 2. Done when all three criteria read pass.
