import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def copy_template(destination):
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("README.md", "AGENTS.md"):
        shutil.copy2(ROOT / name, destination / name)
    shutil.copytree(ROOT / ".agents", destination / ".agents")


class TemplateValidationTests(unittest.TestCase):
    def run_validator(self, root):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate.py"), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_template_passes_public_validation_command(self):
        result = self.run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_duplicate_frontmatter_keys_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="assistant validation ") as directory:
            root = Path(directory)
            copy_template(root)
            skill = root / ".agents" / "skills" / "assistant-setup" / "SKILL.md"
            skill.write_text(
                '---\nname: wrong-name\nname: assistant-setup\n'
                'description: "Set up an assistant."\n---\n# Setup\n',
                encoding="utf-8",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("duplicate", result.stderr.lower())

    def test_invalid_skill_metadata_is_reported_with_the_file_path(self):
        examples = {
            "missing description": "---\nname: assistant-setup\n---\n# Setup\n",
            "wrong name": '---\nname: wrong\ndescription: "Set up."\n---\n# Setup\n',
            "malformed YAML": "---\nname: [broken\n---\n# Setup\n",
            "non-mapping": "---\n- assistant-setup\n---\n# Setup\n",
            "missing body": '---\nname: assistant-setup\ndescription: "Set up."\n---\n',
            "missing delimiters": "# Setup without frontmatter\n",
        }
        for label, content in examples.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix="assistant invalid metadata "
            ) as directory:
                root = Path(directory)
                copy_template(root)
                skill = root / ".agents" / "skills" / "assistant-setup" / "SKILL.md"
                skill.write_text(content, encoding="utf-8")
                result = self.run_validator(root)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("assistant-setup/SKILL.md", result.stderr)

    def test_distributable_template_rejects_an_extra_domain_skill(self):
        with tempfile.TemporaryDirectory(prefix="assistant extra skill ") as directory:
            root = Path(directory)
            copy_template(root)
            extra = root / ".agents" / "skills" / "extra-review"
            extra.mkdir()
            (extra / "SKILL.md").write_text(
                '---\nname: extra-review\ndescription: "Review changes."\n---\n# Review\n',
                encoding="utf-8",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("extra-review", result.stderr)


class TemplateUpgradeTests(unittest.TestCase):
    def test_git_pull_preserves_participant_profile_learnings_and_skills(self):
        with tempfile.TemporaryDirectory(prefix="assistant upgrade ") as directory:
            temporary = Path(directory)
            upstream = temporary / "shared template"
            participant = temporary / "personal assistant"
            hooks = temporary / "empty hooks"
            hooks.mkdir()
            environment = os.environ.copy()
            environment.update(
                GIT_CONFIG_GLOBAL=os.devnull,
                GIT_CONFIG_NOSYSTEM="1",
                GIT_TERMINAL_PROMPT="0",
                GIT_MERGE_AUTOEDIT="no",
            )
            # Keep tests independent of the maintainer's Git identity and hooks.
            for key in list(environment):
                if key.startswith("GIT_CONFIG_KEY_") or key.startswith(
                    "GIT_CONFIG_VALUE_"
                ):
                    del environment[key]
            environment.pop("GIT_CONFIG_COUNT", None)
            environment.pop("GIT_DIR", None)
            environment.pop("GIT_WORK_TREE", None)
            environment.pop("GIT_INDEX_FILE", None)

            def git(repo, *arguments):
                result = subprocess.run(
                    ["git", "-c", f"core.hooksPath={hooks}", "-C", str(repo), *arguments],
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    result.returncode, 0, result.stdout + result.stderr
                )
                return result.stdout.strip()

            def identity(repo):
                git(repo, "config", "user.name", "Template Test")
                git(repo, "config", "user.email", "template-test@example.invalid")
                git(repo, "config", "commit.gpgsign", "false")

            copy_template(upstream)
            git(upstream, "init", "--initial-branch=main")
            identity(upstream)
            git(upstream, "add", ".")
            git(upstream, "commit", "-m", "Release initial template")
            git(temporary, "clone", str(upstream), str(participant))
            identity(participant)
            git(participant, "config", "pull.rebase", "false")
            original_origin = git(participant, "remote", "get-url", "origin")

            profile = (
                "# My coding assistant\n\n## Role\nDeveloper\n\n## Team\nExample team\n"
                "\n## Systems\nJava\n\n## Working preferences\nUse concise diffs.\n"
                "\n## Confirmed learnings\nUse the codebase's existing test runner.\n"
            )
            learning = "# Learning\n\nExplain the cause before proposing a workaround.\n"
            personal_skill = (
                '---\nname: personal-checklist\ndescription: "Apply my checklist."\n'
                "---\n# Personal checklist\n\nReview the changed behavior.\n"
            )
            (participant / "AGENTS.md").write_text(profile, encoding="utf-8")
            (participant / "learnings").mkdir()
            (participant / "learnings" / "debugging.md").write_text(
                learning, encoding="utf-8"
            )
            personal_path = participant / ".agents" / "skills" / "personal-checklist"
            personal_path.mkdir()
            (personal_path / "SKILL.md").write_text(personal_skill, encoding="utf-8")
            git(participant, "add", ".")
            git(participant, "commit", "-m", "Personalize assistant and record learning")
            personal_commit = git(participant, "rev-parse", "HEAD")

            readme = upstream / "README.md"
            new_readme = readme.read_text(encoding="utf-8") + "\nTemplate release note.\n"
            readme.write_text(new_readme, encoding="utf-8")
            maintenance = upstream / ".agents" / "skills" / "assistant-learn" / "SKILL.md"
            new_maintenance = (
                maintenance.read_text(encoding="utf-8")
                + "\nTemplate release clarification.\n"
            )
            maintenance.write_text(new_maintenance, encoding="utf-8")
            git(upstream, "add", ".")
            git(upstream, "commit", "-m", "Update template-owned documentation")
            template_commit = git(upstream, "rev-parse", "HEAD")

            git(participant, "pull")

            self.assertEqual(
                (participant / "AGENTS.md").read_text(encoding="utf-8"), profile
            )
            self.assertEqual(
                (participant / "learnings" / "debugging.md").read_text(encoding="utf-8"),
                learning,
            )
            self.assertEqual(
                (personal_path / "SKILL.md").read_text(encoding="utf-8"), personal_skill
            )
            self.assertEqual(
                (participant / "README.md").read_text(encoding="utf-8"), new_readme
            )
            self.assertEqual(
                (participant / maintenance.relative_to(upstream)).read_text(
                    encoding="utf-8"
                ),
                new_maintenance,
            )
            self.assertEqual(git(participant, "status", "--porcelain"), "")
            self.assertEqual(
                git(participant, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:],
                [personal_commit, template_commit],
            )
            self.assertEqual(
                git(participant, "remote", "get-url", "origin"), original_origin
            )


class LocalSkillInstallationTests(unittest.TestCase):
    def test_local_install_and_force_reinstall_copy_current_skill_and_supporting_files(self):
        executable = shutil.which("gh")
        self.assertIsNotNone(executable, "gh 2.102.1 with gh skill support is required")
        with tempfile.TemporaryDirectory(prefix="assistant install ") as directory:
            temporary = Path(directory)
            source = temporary / "assistant source"
            destination = temporary / "isolated installation"
            copy_template(source)
            source_skill = source / ".agents" / "skills" / "assistant-setup"
            reference = source_skill / "references" / "example.md"
            reference.parent.mkdir()
            reference.write_text("First supporting-file revision.\n", encoding="utf-8")
            source_file = source_skill / "SKILL.md"
            original = source_file.read_text(encoding="utf-8")
            environment = os.environ.copy()
            environment["GH_PROMPT_DISABLED"] = "1"

            def install():
                # --dir is mandatory here; never write to the real user skill directory.
                result = subprocess.run(
                    [
                        executable,
                        "skill",
                        "install",
                        "--from-local",
                        str(source),
                        "assistant-setup",
                        "--agent",
                        "github-copilot",
                        "--allow-hidden-dirs",
                        "--force",
                        "--dir",
                        str(destination),
                    ],
                    cwd=source,
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            install()
            installed_skill = destination / "assistant-setup"
            installed_file = installed_skill / "SKILL.md"
            installed = installed_file.read_text(encoding="utf-8")
            frontmatter = yaml.safe_load(installed.split("---", 2)[1])
            self.assertEqual(frontmatter["name"], "assistant-setup")
            self.assertIsInstance(frontmatter["metadata"]["local-path"], str)
            self.assertTrue(frontmatter["metadata"]["local-path"])
            self.assertEqual(
                installed.split("---", 2)[2].strip(),
                original.split("---", 2)[2].strip(),
            )
            self.assertEqual(
                (installed_skill / "references" / "example.md").read_text(
                    encoding="utf-8"
                ),
                "First supporting-file revision.\n",
            )
            self.assertEqual(source_file.read_text(encoding="utf-8"), original)

            updated = original + "\nSecond skill revision.\n"
            source_file.write_text(updated, encoding="utf-8")
            reference.write_text("Second supporting-file revision.\n", encoding="utf-8")
            install()
            self.assertEqual(
                installed_file.read_text(encoding="utf-8").split("---", 2)[2].strip(),
                updated.split("---", 2)[2].strip(),
            )
            self.assertEqual(
                (installed_skill / "references" / "example.md").read_text(
                    encoding="utf-8"
                ),
                "Second supporting-file revision.\n",
            )
            self.assertEqual(source_file.read_text(encoding="utf-8"), updated)


if __name__ == "__main__":
    unittest.main()
