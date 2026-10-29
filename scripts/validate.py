"""Validate the distributable template, not a participant's customized clone."""

import argparse
import re
import sys
from pathlib import Path

import yaml


EXPECTED_SKILLS = {
    "assistant-setup",
    "assistant-learn",
    "assistant-skill",
    "assistant-share",
}


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        if len(mapping) != len(node.value):
            raise yaml.constructor.ConstructorError(
                None, None, "duplicate frontmatter key", node.start_mark
            )
        return mapping


def validate(root: Path) -> list[str]:
    errors = []
    for name in ("README.md", "AGENTS.md"):
        path = root / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"{name}: required nonempty file is missing")

    skills_root = root / ".agents" / "skills"
    paths = sorted(skills_root.glob("*/SKILL.md"))
    names = {path.parent.name for path in paths}
    if names != EXPECTED_SKILLS:
        errors.append(
            f"Expected exactly {sorted(EXPECTED_SKILLS)}; found {sorted(names)}"
        )

    for path in paths:
        label = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            errors.append(f"{label}: missing YAML frontmatter delimiters")
            continue
        end = lines.index("---", 1)
        try:
            metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
        except yaml.YAMLError as error:
            errors.append(f"{label}: invalid YAML: {error}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"{label}: frontmatter must be a mapping")
            continue
        name = metadata.get("name")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or len(name) > 64
            or name != path.parent.name
        ):
            errors.append(f"{label}: name must match its kebab-case directory (max 64)")
        description = metadata.get("description")
        if (
            not isinstance(description, str)
            or not description.strip()
            or len(description) > 1024
        ):
            errors.append(f"{label}: description must be nonempty text (max 1024)")
        if not "\n".join(lines[end + 1 :]).strip():
            errors.append(f"{label}: skill body is empty")

    if (root / ".mcp.json").exists():
        errors.append(".mcp.json: use app Connectors instead")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Validated 4 maintenance skills and required template files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
