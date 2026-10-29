# Maintaining the template

This file is for template maintainers. `AGENTS.md` is the participant's
profile skeleton, not a maintainer policy file.

## Contract

Issue [#1](https://github.com/msucharda/copilot-assistant-template/issues/1)
defines the v0/v1 scope. The template ships exactly four maintenance skills:
`assistant-setup`, `assistant-learn`, `assistant-skill`, `assistant-share`.
Keep their names stable. Domain skills and the vendored Matt Pocock plugin
belong in the separate AGEL marketplace.

Participants clone the shared repository, retain `origin`, and make local
commits. They merge template updates with `git pull`; they do not push
personal work to the template.

**After v1, releases may change only `README.md` and files under the four
`.agents/skills/assistant-*/` directories.** Ship `AGENTS.md` once and then
leave it unchanged. All other paths become participant-owned too, including
this file, scripts, tests and CI configuration. Finish that infrastructure
before v1. A later infrastructure change needs a separate delivery decision;
do not silently broaden the release contract.

Before a later release, inspect its complete diff against the previous
release and reject any changed path outside that allowlist. Do not rely on
the upgrade fixture alone: it demonstrates the contract when releases honor
it, not permission to change participant-owned paths.

## Local validation

Use Python 3.12 or newer, Git, and **gh 2.102.1** with `gh skill` support.
From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts\validate.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

CI runs the validator and the full test suite on Windows and Linux.
`scripts/validate.py` checks the distributable template: four exact skill
names, valid YAML, required metadata and content. It is not a validator for
a participant clone that has added personal skills. Review English wording,
behavior and trigger quality manually; metadata validation cannot prove them.

The Git integration test uses real temporary repositories. It makes a local
participant commit with a filled `AGENTS.md`, a learning and a personal
skill, then updates both template-owned path types and runs **`git pull`**.
It inherits a synthetic global `pull.ff=only` and applies setup's local
`pull.rebase=false` and `pull.ff=true` settings. It checks preservation, a
clean working tree and the merge history without changing real global config.

The CLI integration test installs and reinstalls through `gh skill` using
an explicit temporary **`--dir`**. It checks copied files and
`metadata.local-path`. It never uses `--scope user` or the maintainer's
`~/.copilot/skills`. The participant-facing user-scope command remains a live
acceptance check; a temporary directory is not evidence that the app loaded
the installed skill.

## Real-app acceptance checks

Run these with an agreed participant account and disposable clone in the
Copilot desktop app, not by changing a maintainer's personal installation.
Keep the observed result separate from the intended behavior.

| Criterion | Check | Evidence to record |
|---|---|---|
| AC1 | Fresh clone; invoke `assistant-setup`; answer all four areas; confirm the profile. | Filled `AGENTS.md`, local commit, unchanged `origin` |
| AC2 | Invoke `assistant-learn` with a pre-existing edit in its target; separate that work, reject one proposal, then confirm one. | Pause for pre-existing edits; no write on rejection; only the confirmed learning enters its local commit |
| AC3 | Create a personal skill with `assistant-skill`, use it in another repository, change it and run the skill again. | User-scope installation, observed behavior, refreshed installed content |
| AC4 | Invoke `assistant-share` with a personal skill and the marketplace plugin available. | Generalized candidate, branch/PR prerequisite stated, both marketplace skill handoffs |
| AC5 | Run the automated clone/pull test. | Conflict-free merge retaining participant content |
| AC6 | Run the validator and review all skill text. | Valid metadata and English content |

AC1-AC4 remain open until observed in the real app. Do not claim a prompt
inspection or CLI-copy test completes them. Marketplace access is required
for an actual submission. The app's plugin installation route, participant
operating systems and AGEL Jira connection are not yet verified.

## Milestones and publication

- v0: review-ready PR by 30 October 2026, 10:00 CET; colleague trial at 13:30.
- v1: 1 November 2026, 18:00 CET.
- The coordinator publishes approved milestones of this development
  repository's `main` to the internal AGEL copy. This implementation task
  does not write to the AGEL organization.

Use `Part of #1` in the PR while real-app criteria remain open. Record live
checks, open questions, deviations and follow-ups in the PR.
