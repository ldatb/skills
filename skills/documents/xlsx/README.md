# xlsx

> Generate extremely beautiful, correct spreadsheets deterministically — the model writes a JSON spec of sheets, columns, rows, and number formats, and a Python script renders the styled workbook via openpyxl. Use when the user asks to create, build, or generate an .xlsx / Excel / spreadsheet, a data table, or a tabular report; when numbers must be consistently formatted; or when a workbook needs styled headers, frozen panes, and sized columns rather than raw gridlines.

**Model-invoked** — the agent runs it automatically when your request matches the triggers below. You can also invoke it by name.

## When to use

- create
- build
- generate an .xlsx / Excel / spreadsheet
- a data table
- a tabular report; when numbers must be consistently formatted;
- when a workbook needs styled headers
- frozen panes
- and sized columns rather than raw gridlines

## What it does

1. State the workbook's purpose and its sheets.
2. Assemble the data into a JSON spec.
3. Render the workbook deterministically.
4. Verify the artifact by reopening it.

## Scripts

- `scripts/render.py`

## Learn more

- [SKILL.md](SKILL.md) — the full procedure the agent follows.

---

*Generated from SKILL.md by `skill-readme`. Run `skill-readme` to refresh; do not edit by hand.*
