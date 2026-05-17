#!/usr/bin/env python3
"""Quick validator for migrated Codex skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FORBIDDEN_PATTERNS = [
    r"\.cursor/skills",
    r"\.cursor\\skills",
    r"/sdx-",
    r"AskQuestion",
    r"\bRead\b",
    r"\bWrite\b",
    r"\bEdit\b",
    r"\bBash\b",
    r"Cursor",
    r"Claude",
    r"\.claude",
    r"CLAUDE\.md",
]


def read_text(path: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append("file must be UTF-8 without BOM")
        data = data[3:]
    try:
        return data.decode("utf-8"), errors
    except UnicodeDecodeError as exc:
        return None, [*errors, f"invalid UTF-8: {exc}"]


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    match = re.match(r"\A---\n(?P<body>.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}, ["missing opening frontmatter block"]

    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in match.group("body").splitlines():
        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if key_match:
            current_key = key_match.group(1)
            fields[current_key] = key_match.group(2)
        elif current_key == "description" and line.startswith("  "):
            fields[current_key] += "\n" + line[2:]
        elif line.strip():
            errors.append(f"unrecognized frontmatter line: {line}")

    keys = set(fields)
    if keys != {"name", "description"}:
        errors.append(f"frontmatter keys must be exactly name, description; got {sorted(keys)}")
    if not fields.get("name", "").strip():
        errors.append("name is empty")
    description = fields.get("description", "").replace(">", "").strip()
    if not description:
        errors.append("description is empty")

    return fields, errors


def validate_openai_yaml(skill_file: Path, skill_name: str) -> list[str]:
    errors: list[str] = []
    yaml_path = skill_file.parent / "agents" / "openai.yaml"
    if not yaml_path.exists():
        return [f"missing UI metadata: {yaml_path}"]
    text, read_errors = read_text(yaml_path)
    errors.extend(f"{yaml_path}: {error}" for error in read_errors)
    if text is None:
        return errors
    for field in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"(?m)^{re.escape(field)}:\s*\S", text):
            errors.append(f"{yaml_path}: missing {field}")
    if f"${skill_name}" not in text:
        errors.append(f"{yaml_path}: default_prompt must include ${skill_name}")
    return errors


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text, read_errors = read_text(path)
    errors.extend(read_errors)
    if text is None:
        return errors

    fields, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)
    skill_name = fields.get("name", "").strip()
    if skill_name and skill_name != path.parent.name:
        errors.append(f"name '{skill_name}' does not match directory '{path.parent.name}'")
    if skill_name:
        errors.extend(validate_openai_yaml(path, skill_name))

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"forbidden migrated reference remains: {pattern}")

    return errors


def main(argv: list[str]) -> int:
    root = Path.cwd()
    files = [Path(arg) for arg in argv]
    if not files:
        files = sorted((root / ".codex" / "skills").glob("seedpacespec-*/SKILL.md"))

    if not files:
        print("No SKILL.md files found.", file=sys.stderr)
        return 1

    failed = False
    for file in files:
        errors = validate_file(file)
        if errors:
            failed = True
            print(f"FAIL {file}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {file}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
