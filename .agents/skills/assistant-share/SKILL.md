---
name: assistant-share
description: "Generalize a personal skill for the AGEL marketplace and hand it to marketplace-create-skill and marketplace-submit-update. Use when the user wants to share a reusable personal workflow with colleagues."
---

# Share a personal skill

Prepare a reusable contribution to
`agel-data-and-ai-temp-poc/copilot-marketplace`.

## Steps

1. Read the selected personal skill and every supporting file it uses.
   Clarify the reusable goal and intended audience. The AGEL marketplace
   is the only sharing destination for this workflow.
2. State the prerequisite before submission: the participant must be able
   to create a branch and open a pull request in
   `agel-data-and-ai-temp-poc/copilot-marketplace`.
   Also check that `marketplace-create-skill` and
   `marketplace-submit-update` from the `marketplace-maintenance` plugin
   are available. If either prerequisite is missing, prepare the local
   candidate but stop before submission, name the missing prerequisite,
   and ask the workshop facilitator for access or plugin installation.
   Use the documented `copilot-marketplace` installation commands in
   `README.md`; keep this contribution's destination on the AGEL copy.
3. Prepare the generalized candidate under the participant-owned
   `sharing/<name>/` directory in the personal assistant repository.
   Preserve the original personal skill. Include the required supporting
   files and keep relative references working.
   Replace personal details, team-only assumptions, machine paths,
   credentials and private examples with neutral parameters or examples.
   Remove installation tracking metadata such as `metadata.local-path`
   from the candidate. Keep the skill's useful behavior and write it in
   English. If private context cannot be separated from the procedure,
   explain why the candidate is not ready to share.
4. Show the generalized diff and a short list of removed private context
   categories, without repeating sensitive values. Ask the user to
   confirm the candidate and the marketplace destination before handing
   it off for publication.
5. Invoke `marketplace-create-skill` and follow its installed instructions
   for plugin selection, naming, layout, frontmatter and validation.
   Supply the candidate's path, purpose, trigger situations, supporting
   files and the confirmed destination. That skill owns creation in the
   marketplace clone; do not substitute a personal assistant push.
6. Continue with `marketplace-submit-update` for its branch, version,
   validation, PR and review workflow. It may already be invoked by the
   creation skill; continue the same submission rather than creating a
   second PR. Follow the currently installed instructions and report the
   actual PR or the precise blocked step.

## Done when

- A generalized candidate preserves the original and has user approval.
- Both marketplace skills received the handoff, or a missing prerequisite
  is explicitly reported as blocking submission.
- The participant knows that sharing requires a branch and PR in the
  AGEL marketplace. A local candidate alone is not a published skill.
