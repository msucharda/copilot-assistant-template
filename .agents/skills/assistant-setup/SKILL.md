---
name: assistant-setup
description: "Personalize the coding assistant through a conversation about role, team, systems and working preferences, then commit AGENTS.md locally. Use for first setup or when the user asks to update their assistant profile."
---

# Set up my coding assistant

Turn the participant's answers into a concise, English `AGENTS.md`.

## Steps

1. Locate the user's personal assistant repository and read its `AGENTS.md`
   and `README.md`. If this session is in another repository, ask for the
   assistant repository path before editing. Inspect the working tree and
   preserve existing participant content.
2. Ask one question at a time about each unfilled area:
   - Role: what work should the assistant help with?
   - Team: how does the team collaborate?
   - Systems: which technologies and systems matter to that work?
   - Working preferences: how should the assistant communicate and approach tasks?

   Ask for missing information rather than inventing answers. The user may
   leave an area unspecified; record that choice. On a repeat run, ask what
   changed instead of repeating the full interview.
3. Show the proposed English `AGENTS.md`, including the existing confirmed
   learnings, and ask the user to confirm it. Wait for confirmation before
   writing. Replace the setup placeholders with the confirmed answers.
   Keep the file short; procedural instructions belong in personal skills.
4. Configure merge-based template updates in this clone:

   ```shell
   git config --local pull.rebase false
   ```

   Keep `origin` unchanged. Check that Git has a commit identity. If it is
   missing, ask the user to configure an identity for this repository; do
   not invent one or change global configuration.
5. Review the `AGENTS.md` diff with the user. Commit only this file locally:

   ```shell
   git add -- AGENTS.md
   git commit --only -m "Personalize my coding assistant" -- AGENTS.md
   ```

   If it already matches the confirmed profile, report that no new commit
   is needed. If a command fails, report the error and the unfinished step.
   Do not push.

## Done when

- Role, team, systems and working preferences reflect the user's confirmed
  answers or explicit choices to leave an area unspecified.
- Existing learnings remain intact, and `AGENTS.md` has a local commit.
- `origin` still points to the shared template and pulls use merge.
