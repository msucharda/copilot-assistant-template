---
name: assistant-share
description: "Generalize a personal skill for the AGEL marketplace and hand it to marketplace-create-skill and marketplace-submit-update. Use when the user wants to share a reusable personal workflow with colleagues."
---

# Share a personal skill

Prepare a reusable contribution to
`agel-data-and-ai-temp-poc/copilot-marketplace` by default.

## Explicit destination exception

Use a different destination only when all three conditions hold:

1. The user explicitly names the destination as `owner/repo` in their request.
2. The marketplace checkout's `origin`, read with
   `git -C "<marketplace-root>" remote get-url origin`, points to that exact
   repository. Inspect its host and owner/repository for HTTPS or SSH remotes;
   ignore only an optional `.git` suffix. An origin alone or an inferred
   handoff is not authorization.
3. `<marketplace-root>/.github/plugin/marketplace.json` has
   `"name": "copilot-marketplace"`.

If any condition fails, stop and report the mismatch before editing or
handing off. Do not select a substitute or change `origin` to make it match.
Keep the AGEL identity in the catalog, plugin manifests and participant-facing
documentation. The exception changes only this contribution's destination,
not the personal assistant repository's `origin` or template-update workflow.
State the exception in the output and carry the user's explicit target and
the three checks into both marketplace skill handoffs. Recheck them before
any push or PR; the PR must disclose the exception too.

## Steps

1. Read the selected personal skill and every supporting file it uses.
   Clarify the reusable goal and intended audience. Default to the AGEL
   marketplace; resolve an explicitly requested destination using the
   exception rule above before editing or handing off.
2. State the prerequisite before submission: the participant must be able
   to create a branch and open a pull request in the resolved marketplace.
   Also check that `marketplace-create-skill` and
   `marketplace-submit-update` from the `marketplace-maintenance` plugin
   are available. If either prerequisite is missing, prepare the local
   candidate but stop before submission, name the missing prerequisite,
   and ask the workshop facilitator for access or plugin installation.
   Use the documented `copilot-marketplace` installation commands in
   `README.md`; never infer an alternate destination from plugin installation.
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
5. Establish the handoff before any marketplace edit. Keep the assistant
   root and marketplace root as two distinct absolute paths. Verify the
   marketplace root and capture its base commit with:

   ```shell
   git -C "<marketplace-root>" rev-parse --show-toplevel
   git -C "<marketplace-root>" rev-parse HEAD
   ```

   Replace the placeholder with the confirmed checkout. The returned root
   must be that checkout, and the base must come from it, not from the
   assistant repository. Carry this handoff across confirmation turns:
   candidate path, confirmed destination, marketplace root, base commit,
   approved shared name, behavior, version changes and requested stop point.
6. Invoke `marketplace-create-skill` with the available skill-invocation
   tool and supply that handoff. Reading its `SKILL.md` alone is not the
   handoff; do not implement its workflow inline instead of invoking it.
   Follow its installed instructions for placement and validation.
   Marketplace work belongs in the marketplace checkout: use `git -C`
   for Git commands, and set that checkout as the working directory in
   **every** shell call that runs npm or the validator. A previous shell's
   `Set-Location` does not carry into a new call.
7. Invoke `marketplace-submit-update` for the same contribution and pass
   the same marketplace root and recorded base. If the creation skill
   already invoked it, continue that invocation rather than making a
   second submission. Await each dependency install, test and validator
   command to completion in order. If a check fails, report its command,
   working directory and error before correcting the cause; an install
   failure is not permission to invent a package file or skip the check.
   Follow the requested stop point, including a local-only rehearsal's
   prohibition on push/PR. Report the actual PR or the precise pending step.

## Done when

- A generalized candidate preserves the original and has user approval.
- Both marketplace skills received the handoff, or a missing prerequisite
  is explicitly reported as blocking submission.
- The handoff's root and base belong to the marketplace checkout, all
  required checks completed there, and their actual results are reported.
- The participant knows that sharing requires a branch and PR in the
  resolved marketplace. Any explicit destination exception is verified and
  disclosed. A local candidate alone is not a published skill.
