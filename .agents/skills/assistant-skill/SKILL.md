---
name: assistant-skill
description: "Create or improve a personal coding skill in the assistant repository, then install or reinstall its current files for GitHub Copilot at user scope. Use when turning a repeatable workflow into a skill or changing an existing personal skill."
---

# Build and install a personal skill

Keep the editable source in the assistant repository and install a copy
for use in every code repository.

## Steps

1. Locate the personal assistant repository, read its `AGENTS.md`, and
   inspect the working tree and any existing target skill. Work from
   that repository root. Ask for the task, trigger situations and expected
   result when missing. A previously confirmed `assistant-learn` change
   supplies these requirements; avoid asking for the same approval again.
   Before editing, inspect status and staged/unstaged diffs of the intended
   target files. If they contain pre-existing changes or untracked content,
   pause for the user to commit or separate that work. A path-only commit
   includes all edits in each selected file. For a reinstall-only request,
   install the current source without committing pre-existing edits.
2. Agree on an English kebab-case name of at most 64 characters.
   Use `.agents/skills/<name>/` for source files. The `assistant-*`
   namespace belongs to the four template maintenance skills; choose a
   different name for personal work. Preserve an existing skill's useful
   behavior when changing it.
3. Write or update `SKILL.md` in English with YAML frontmatter:

   ```yaml
   ---
   name: example-skill
   description: "Describe the result. Use when the user needs the workflow."
   ---
   ```

   Match `name` to the directory name. State actionable steps and observable
   completion criteria. Include examples or supporting files only when
   needed, and link supporting instructions with the condition for reading
   them. Use the user's real workflow, not an invented domain example.
4. Try a representative prompt in this repository and inspect whether the
   skill produces the expected result. To try it from a code repository
   before installation, give that Copilot session the absolute path to this
   skill's `SKILL.md` and ask it to follow the file. Report what was actually
   tried; an unperformed or failed trial is not a successful test.
5. Install the current source, replacing `<name>` with the actual skill name.
   Run this command yourself from the assistant repository root:

   ```shell
   gh skill install --from-local . <name> --agent github-copilot --scope user --allow-hidden-dirs --force
   ```

   This copies files into `~/.copilot/skills/<name>/`; it is not a live link.
   Repeat this command after **every** source change, including this run
   when updating an existing skill. `--force` replaces the installed copy.
   `gh skill update` skips local installs; it does not refresh this copy.
   Inspect the installed `SKILL.md` and supporting files to confirm that
   the latest source was copied. The CLI adds `metadata.local-path` to the
   installed frontmatter; keep the repository source as the editing target.
6. If installation fails, report the command, error and pending installation.
   Keep the source change visible for repair; do not claim the skill is
   installed or substitute a different destination.
7. Review the source diff and commit only the intended skill files locally.
   Stage those exact paths, then use
   `git commit --only -m "Update my personal skill" -- <paths>` with their
   actual paths. If no source changed on a reinstall-only run, no new
   commit is needed. Leave other staged files untouched. Do not push.
8. Explain that the personal copy is available across repositories. If the
   current session does not discover it, start a new Copilot session in the
   target repository and try a prompt matching its description.

## Done when

- The English source skill exists under `.agents/skills/<name>/`.
- The current source was installed or reinstalled at user scope with the
  command above, and the copied content was inspected.
- Source changes made by this run have a local commit, and the trial result is stated
  accurately, including any pending live verification.
