"""One assertion per rule, plus suppression, code-fence, and CLI exit-code behavior.

Every rule the linter enforces has a fixture that triggers it and the clean
fixture proves the rule set does not fire on well-formed skills. New ambiguities
become a new case here (Kaizen).
"""

from __future__ import annotations

from pathlib import Path

from skill_lint.checks import run_checks
from skill_lint.cli import main
from skill_lint.core import SkillDoc, load_rules

RULES = load_rules()
FIXTURES = Path(__file__).parent / "fixtures"
DEFAULT_FM = "name: {name}\ndescription: Demo skill. Use when testing the linter.\ndisable-model-invocation: true"


def write_skill(tmp_path: Path, name: str, body: str, *, frontmatter: str | None = None) -> Path:
    folder = tmp_path / name
    folder.mkdir()
    fm = frontmatter if frontmatter is not None else DEFAULT_FM.format(name=name)
    path = folder / "SKILL.md"
    path.write_text(f"---\n{fm}\n---\n\n{body}\n")
    return path


def ids(path: Path) -> set[str]:
    return {f.rule_id for f in run_checks(SkillDoc.load(path), RULES)}


# --- the clean fixture fires nothing, even under strict --------------------
def test_good_fixture_is_clean():
    assert ids(FIXTURES / "good-skill" / "SKILL.md") == set()


def test_good_fixture_passes_cli_strict():
    assert main(["--strict", str(FIXTURES / "good-skill")]) == 0


# --- frontmatter ----------------------------------------------------------
def test_sk001_missing_frontmatter(tmp_path):
    folder = tmp_path / "nofm"
    folder.mkdir()
    (folder / "SKILL.md").write_text("Just a body, no frontmatter.\n")
    assert "SK001" in ids(folder / "SKILL.md")


def test_sk003_name_mismatch(tmp_path):
    p = write_skill(
        tmp_path,
        "real-folder",
        "Body.",
        frontmatter="name: wrong-name\ndescription: x. Use when testing.\ndisable-model-invocation: true",
    )
    assert "SK003" in ids(p)


def test_sk004_name_not_kebab(tmp_path):
    p = write_skill(
        tmp_path,
        "Bad_Name",
        "Body.",
        frontmatter="name: Bad_Name\ndescription: x. Use when testing.\ndisable-model-invocation: true",
    )
    assert "SK004" in ids(p)


def test_sk005_description_missing(tmp_path):
    p = write_skill(
        tmp_path, "nodesc", "Body.", frontmatter="name: nodesc\ndisable-model-invocation: true"
    )
    assert "SK005" in ids(p)


def test_sk007_model_invoked_without_trigger(tmp_path):
    p = write_skill(
        tmp_path,
        "modelinv",
        "Body.",
        frontmatter="name: modelinv\ndescription: A skill that does a thing.",
    )
    assert "SK007" in ids(p)


def test_sk008_unknown_key(tmp_path):
    p = write_skill(
        tmp_path,
        "extrakey",
        "Body.",
        frontmatter="name: extrakey\ndescription: x. Use when testing.\ndisable-model-invocation: true\nbogus: 1",
    )
    assert "SK008" in ids(p)


# --- ambiguity ------------------------------------------------------------
def test_sk010_pronoun(tmp_path):
    assert "SK010" in ids(write_skill(tmp_path, "p", "It should run quickly."))


def test_sk010_qualified_pronoun_is_clean(tmp_path):
    assert "SK010" not in ids(write_skill(tmp_path, "p", "This file holds the configuration."))


def test_sk020_context_explosion(tmp_path):
    assert "SK020" in ids(write_skill(tmp_path, "q", "Review the code for each file in the repo."))


def test_sk030_conditional_complexity(tmp_path):
    assert "SK030" in ids(
        write_skill(tmp_path, "c", "If the build passes and when tests are green, deploy.")
    )


def test_sk040_destructive(tmp_path):
    assert "SK040" in ids(write_skill(tmp_path, "d", "Run rm -rf build to reset the output."))


def test_sk041_vague_destructive(tmp_path):
    assert "SK041" in ids(write_skill(tmp_path, "vd", "Clean up the workspace folder."))


def test_sk050_concurrency(tmp_path):
    assert "SK050" in ids(
        write_skill(tmp_path, "cc", "Create a file using the current timestamp as the name.")
    )


def test_sk060_vague_imperative(tmp_path):
    assert "SK060" in ids(write_skill(tmp_path, "v", "Make sure the output is correct."))


def test_sk080_marker(tmp_path):
    assert "SK080" in ids(write_skill(tmp_path, "m", "Read input. TODO finish this."))


# --- suppression, code fences, sprawl -------------------------------------
def test_inline_suppression(tmp_path):
    p = write_skill(tmp_path, "s", "Make sure it works. <!-- skill-lint: allow SK060 -->")
    assert "SK060" not in ids(p)


def test_prose_rule_skips_code_but_destructive_is_caught(tmp_path):
    body = "```sh\nmake sure to rm -rf node_modules\n```"
    found = ids(write_skill(tmp_path, "fence", body))
    assert "SK060" not in found  # natural-language rule ignores code
    assert "SK040" in found  # destructive rule scans code


def test_sk070_sprawl(tmp_path):
    body = "\n".join(f"Numbered item {i} in the list." for i in range(600))
    assert "SK070" in ids(write_skill(tmp_path, "long", body))


# --- CLI exit codes -------------------------------------------------------
def test_cli_fails_on_error(tmp_path):
    write_skill(tmp_path, "bad", "Run rm -rf build now.")
    assert main([str(tmp_path)]) == 1


def test_cli_passes_clean_default(tmp_path):
    write_skill(tmp_path, "okay", "Read the file named in the prompt, then stop.")
    assert main([str(tmp_path)]) == 0
