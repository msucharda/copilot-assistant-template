# My personal coding assistant

A repository you own locally: describe how you work, capture useful lessons,
and build coding skills that improve with use. This template supports the
AGEL GitHub Copilot workshop on **2 November 2026**. All workshop work happens
in the **GitHub Copilot desktop app**.

This repository is the **development copy**. Workshop participants clone the
internal AGEL copy below, not this development repository.

## Start here

You need Git, access to the AGEL template, and a working Copilot desktop app.
The app bundles GitHub CLI; `gh skill` is a preview feature. The documented
command was verified with **gh 2.102.1**. Examples assume Windows and
PowerShell; participant operating systems still need confirmation.

1. Clone the shared template into your own local folder:

   ```powershell
   git clone https://github.com/agel-data-and-ai-temp-poc/copilot-assistant-template.git my-coding-assistant
   cd my-coding-assistant
   git config --local pull.rebase false
   ```

   Keep `origin` pointing to this shared template. Use a clone, not a fork
   or GitHub's "Use this template" workflow. Your personal commits stay
   local; **do not push them to `origin`**.
2. Open this local repository in the Copilot desktop app. Start a session
   over this repository and ask:

   > Use assistant-setup to set up my coding assistant.

   Answer questions about your role, team, systems and working preferences.
   The skill shows the proposed English `AGENTS.md`, waits for confirmation,
   fills it, and creates a local commit. If Git has no commit identity,
   supply one for this repository when asked.
3. Check that `AGENTS.md` describes you and the commit appears in `git log -1`.
   The four maintenance skills are discovered from `.agents/skills/`
   in this repository; no personal installation is required to start.

## The four maintenance skills

| Ask Copilot to use | Result |
|---|---|
| `assistant-setup` | Fill or revise your profile through a conversation and commit it locally. |
| `assistant-learn` | Propose a reusable lesson, wait for your confirmation, and commit it in your own content. |
| `assistant-skill` | Create or improve your own skill, then install/reinstall it for use across repositories. |
| `assistant-share` | Generalize a personal skill and hand it to the AGEL marketplace contribution workflow. |

These are instructions for an agent, not deterministic programs. Inspect the
proposed changes and the results. A skill must report failed or unfinished
steps rather than claim they succeeded.

## Put knowledge in the right layer

| Layer | What belongs there | Where it applies |
|---|---|---|
| Personal assistant repository | Your profile, confirmed lessons and personal skills | Profile and project skills apply in sessions over this repository; installed skills apply across repositories. |
| Code repository | Codebase facts in `AGENTS.md`, `CONTEXT.md` and ADRs | Sessions working on that codebase |
| AGEL marketplace | Generalized skills and plugins for colleagues | Repositories where the plugin is available |
| Copilot Project memory | Useful ongoing Project context | That Copilot Project, subject to the app's memory settings |

Create a Copilot Project for ongoing work on a code repository. Keep its tasks
and sessions together; use Project memory for continuing context, not as the
only copy of a documented engineering decision. Commit lasting codebase
decisions in that repository. Your personal assistant repository is a separate
place to develop your workflow.

`AGENTS.md` in this assistant repository is **not automatically loaded into
unrelated code repositories**. Installed personal skills carry their own
instructions; put necessary codebase context in the code repository.
Global preferences live in `~/.copilot/copilot-instructions.md`; this template
does not configure them.

## Capture a lesson

After a correction or non-obvious discovery, ask:

> Use assistant-learn to propose one useful lesson from this session.

The skill proposes the exact text and destination and waits for your answer
before writing. Personal rules go in `AGENTS.md`; repeatable procedures go in
your own skills. A separate note needs a reference so future sessions can find
it. Codebase-only facts stay with that codebase. Changes are committed locally.
The skill never edits the shared `assistant-*` maintenance skills.

## Develop, try and install your own skill

1. In a session over this assistant repository, ask:

   > Use assistant-skill to turn my repeated code-review checklist into a skill.

   Your source lives in `.agents/skills/<name>/SKILL.md`. Personal names
   must not start with `assistant-`; that namespace belongs to the template.
2. Try it here. To try an uninstalled coding skill in a different repository,
   give that Copilot session its absolute `SKILL.md` path and ask it to follow
   the file, for example:

   > Read D:\work\my-coding-assistant\.agents\skills\my-review\SKILL.md and use it for this task.

3. `assistant-skill` installs the current source itself. The command, run from
   this assistant repository with `<name>` replaced by the real skill name, is:

   ```shell
   gh skill install --from-local . <name> --agent github-copilot --scope user --allow-hidden-dirs --force
   ```

   The installed copy is in `~/.copilot/skills/<name>/` and is available across
   repositories. Hidden `.agents/` directories require `--allow-hidden-dirs`.
   `--force` replaces an existing installed copy.
4. Edit the **repository source**, not the installed copy. Reinstall after
   **every change**; `assistant-skill` does this on update runs too.
   Local installation copies files and adds `metadata.local-path` to the
   installed frontmatter. `gh skill update` skips these local installations;
   it cannot replace the reinstall command. If a session does not discover
   the installed skill, start a new session and try its trigger.

## Share with colleagues

Ask `assistant-share` to generalize one of your personal skills. It prepares
a separate candidate under `sharing/<name>/`, removes private details and
asks you to confirm the proposed contribution.

Sharing goes only through
[`agel-data-and-ai-temp-poc/ai-dev-marketplace`](https://github.com/agel-data-and-ai-temp-poc/ai-dev-marketplace).
You must be able to **create a branch and open a pull request** there.
The `marketplace-maintenance` plugin must provide `marketplace-create-skill`
and `marketplace-submit-update`; `assistant-share` hands off to them for
plugin placement, validation, versioning and the PR.

The desktop app's marketplace plugin installation route is not yet verified.
Ask the facilitator to make the required plugin available; this guide does
not invent a Customize UI sequence or CLI command.

The workshop's Matt Pocock skills come from a **separately vendored plugin in
the AGEL marketplace**. Do not also install the upstream `mattpocock/skills`
plugin: that creates duplicate skills. This template contains no domain skills.

## Optional Jira connection

If you want Jira context, connect **Atlassian Rovo** through **Connectors in the
Copilot desktop app**. This template contains no `.mcp.json`. Jira is optional:
setup, learning, skill creation and template updates work without it.
The workshop team cannot currently test the AGEL Jira connection.

## Update from the template

Save and commit your personal work first, then run in this repository:

```shell
git status
git pull
```

Setup configures `pull.rebase=false` in this clone so `git pull` merges newer
template commits with your local commits. Your personal history remains local.
The path ownership contract keeps those edits separate:

| Owner | Paths |
|---|---|
| Template | `README.md`, `.agents/skills/assistant-*/` |
| You | `AGENTS.md` after setup, your own skill directories, and every other path |

After v1, template releases change only template-owned paths. Keep your
personal rules out of those paths, or you can create pull conflicts.
`AGENTS.md` ships as a skeleton **once**; later releases leave it unchanged.
Do not resolve an unexpected conflict by discarding your personal content.
Ask the facilitator to inspect it before continuing.

The assistant clone is not a backup service. Your local-only commits are not
stored in the shared remote; arrange your own approved backup if needed.

## Template development and verification

Template maintainers: see [CONTRIBUTING.md](CONTRIBUTING.md) for validation,
the release ownership contract and the remaining real-app checks.
