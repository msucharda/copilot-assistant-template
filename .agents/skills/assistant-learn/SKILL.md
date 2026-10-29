---
name: assistant-learn
description: "Propose a reusable lesson from a correction or non-obvious discovery, wait for confirmation, and commit it in participant-owned assistant content. Use when the user asks the assistant to learn or remember a working lesson."
---

# Learn from our work

Capture a confirmed lesson where the next relevant session can find it.

## Steps

1. Locate the personal assistant repository and read its `AGENTS.md` and
   relevant personal skills. Inspect existing lessons to avoid duplicates.
   Identify one reusable correction, recovery or non-obvious discovery.
   If there is no useful new lesson, say so and stop without editing.
2. Choose the knowledge layer:
   - A durable personal working preference belongs in this repository's
     `AGENTS.md`.
   - A repeatable personal procedure belongs in the participant's own
     `.agents/skills/<name>/SKILL.md` or one of its referenced files.
   - A fact specific to one codebase belongs in that code repository's
     `AGENTS.md`, `CONTEXT.md` or ADRs. Propose that destination and hand
     the task to a session over that repository rather than recording it
     as a universal personal rule.
   - A team-wide procedure is a candidate for `assistant-share`.

   For this skill's edits, use only participant-owned paths in the personal
   assistant repository. `README.md` and every
   `.agents/skills/assistant-*` directory are template-owned and must remain
   unchanged. If a lesson concerns a maintenance skill, propose a personal
   note in `AGENTS.md` instead of patching that skill.
3. Present the exact proposed text, destination path and reason it will
   help again. Include any new reference from `AGENTS.md` or `SKILL.md`
   needed to make a separate note discoverable. Ask the user to confirm
   this complete change and wait for an explicit answer.
   Rejection or no answer means no writes and no commit.
4. Apply only the confirmed change in English. Preserve unrelated edits.
   If it changes or creates a personal skill, invoke `assistant-skill`
   with the approved change to finish the skill and install/reinstall it.
   That skill handles the local commit; do not make a duplicate commit.
5. For a profile or note change, inspect the diff and commit only the
   confirmed participant-owned paths. Stage those exact paths, then use
   `git commit --only -m "Record a confirmed assistant learning" -- <paths>`
   with the actual paths, not the placeholder. Leave other staged work
   untouched. Report any command failure and the unfinished step.
   Do not push.

## Done when

- The user confirmed the exact lesson and destination before any write.
- Only participant-owned content changed and the lesson is discoverable.
- The confirmed change has a local commit, and any changed personal skill
  has been reinstalled through `assistant-skill`.
