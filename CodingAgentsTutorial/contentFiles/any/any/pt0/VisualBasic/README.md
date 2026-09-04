# Coding Agents Tutorial

Fix a bug, build from a PDD, add tests and try-catch, all by instructing a coding agent instead of dragging activities.

This is a working UiPath project: three workflows, a test, a spreadsheet of
expense claims and a practice web portal. One workflow has a bug. Finding it is
step 2.

## Start here

Open Autopilot (`Ctrl+Alt+I` on Windows, `⌥⌘I` on Mac, or **Ask Autopilot** on
the project's start page) and send:

> ### start the course

The agent takes it from there, one step at a time: what to say, what to check.
It records what happened in `course/PROGRESS.md` and never edits this file.
Coming back another day? Send **continue the course**.

Not using Autopilot? Do `course/SETUP.md` once, then send the same line to your
agent.

The steps are written out below if you want to read ahead. The agent walks you
through all of them either way.

---

## Step 1: Set the safety net (5 min)

Take a snapshot before anything changes, so every later change is something you
can undo. You initialise git in Studio's Git panel and make the first commit; the
agent is not allowed to do that part. Then ask the agent what the project does.
It reads the same files Studio does, so it can explain an unfamiliar project
before you change anything, and its answer gives you something to check against
the canvas.

**Say to the agent:**

> Describe this project. What does it do, what workflows exist, and where does
> the data come from?

**Check:**

- The Git panel shows a clean working tree.
- The description matches what you see on the canvas.
- Nothing has changed.

## Step 2: Find the bug, then fix it (15 min)

You read the agent's work in the visual diff, undo it, and put it back. Once
undo is cheap, you stop being careful and start being fast. Three parts.

**Part A, read only.**

**Say to the agent:**

> The receipt rule is that any expense of 50 or more needs a receipt. Check
> whether the project implements that correctly. Do not change anything yet.

**Check:**

- It names one workflow and quotes the exact comparison in it.
- It changed nothing.
- If the answer is vague, tighten the instruction. Do not switch agents.

**Part B, the first write.**

**Say to the agent:**

> Fix it. Change only that condition.

**Check:**

- In Studio's Git diff panel, one condition changed and nothing else. Studio
  shows it as activities, not XML.

**Part C, the revert drill.** Revert the change in the Git panel and watch it
disappear from the canvas. Re-apply it: ask the agent again, or do it yourself.
Commit.

**Check:**

- Working tree clean.

## Step 3: Build from a PDD (25 min)

The agent builds a browser automation from a business request. Before you start,
the UiPath browser extension must be installed with "Allow access to file URLs"
enabled, because the portal is a local file; on macOS, also grant Accessibility
and Screen Recording to UiPath in System Settings. Then try the portal by hand:
open `assets/expenses.html`, submit a claim, try one for 60.00 with no receipt,
and close it. You do not open it for the run. The automation opens the portal
itself and leaves it open for you to check.

**Say to the agent:**

> Read specs/step-03-pdd.md and tell me how you'd implement it. Don't build
> anything yet.

Read the plan. It is cheaper to correct than a built workflow. When it reads
right:

> Go ahead and implement it.

**Check:**

- The project runs without crashing and opens the portal itself.
- The portal's submissions table has three rows, `EXP-0001` to `EXP-0003`.
- The summary covers all six claims: three with confirmation numbers, three with
  a reason.
- Selectors target elements by `id`, not by position. The portal's ids are
  listed at the top of `assets/expenses.html`.

## Step 4: Let it test the work (10 min)

The agent writes a test, runs it, reads the result and fixes what fails.
`Tests/ValidateExpense_Tests.xaml` has one case for it to copy.

**Say to the agent:**

> Add test cases for the receipt rule, including exactly 50 with and without a
> receipt. Run them and fix anything that fails.

**Check:**

- An actual test run passes, shown to you or run from Test Explorer
  (`Ctrl+Alt+T` on Windows, `⌥⌘T` on Mac). If the agent says the tests pass but
  cannot show you, treat it as unverified.
- There is a case for 50.00 with a receipt and one without.

## Step 5: The bulk edit (10 min)

One instruction changes every workflow in the project. Try Catch and logging
across a project is an afternoon of clicking in the designer; here it is one
sentence and a diff review. "Every workflow" is five files: `Main.xaml`, the
three in `Workflows/`, and the one from step 3. Leave the test alone.

**Say to the agent:**

> Add a Try Catch to every workflow in this project. Log the exception message
> and the workflow name. Do not change any business logic.

**Check:**

- The diff touches all five files.
- The project still runs and still gives three accepted submissions.
- No business logic changed. Read the diff; do not take its word.

---

## Asking well

You have felt this by step 3:

> Vague: "make my automation better"
>
> Scoped: "add a Try Catch around the submit sequence, log the error message,
> and continue to the next row"

The first is a wish. The second is a work item. A good request names the file
and where it goes, the inputs and outputs with their types, the behaviour from
start to finish, which activities or packages to use or avoid, and what already
exists to reuse. When a request goes wrong, one of those was missing.

## Glossary

| Agent word | What it means |
|---|---|
| Context | What the agent can see of your project. Files, mostly. |
| Prompt | An instruction. Scope it like a ticket. |
| Diff | What changed. The Git panel shows it as activities. |
| Commit | A save point you can return to. |
| Working tree | Your files now, versus the last commit. Clean means no changes. |
| Revert | Undo a change already on disk. |
| Repository | The folder plus its history. |
| Stage | Choosing which changes go into the next commit. |
| Skill | A markdown file of instructions an agent loads when relevant. This course is two of them; the agent shows you where after step 5. |
| Context window | How much the agent can hold at once. Long conversations forget the start. |
| Hallucination | Confident nonsense. Why you check the diff. |

## If you get stuck

- The agent does your part, types the "Say to the agent" line itself, or offers
  to move on. Say: "Stop. That's my line. Wait for me."
- The agent starts building in step 1. Tell it to stop and re-read `AGENTS.md`.
- The agent edits this file. It is not allowed to. Revert it in the Git panel.
- In step 3 the build fails with "Target or Input UI Element must be set". One
  unconfigured target blocks the whole project, steps 4 and 5 included. Finish
  the targets, or revert step 3 in the Git panel and carry on.
- You lost your place. Say "continue the course".
- Nothing happens when you say "start the course". The agent did not load the
  project instructions. Say: "read AGENTS.md and course/agent/PROCEDURE.md, then
  start the course".
- A change made things worse. Revert it in the Git panel.
- The agent is confidently wrong. Start a new conversation.

Expect two or three rounds of build, look, ask for a change on any real piece of
work. Keep going while the problem is in one place and the overall shape is
right. Start over when it keeps producing variations of the same broken thing,
or you are on the third or fourth fix. Reverting and re-asking with a sharper
instruction beats talking an agent out of a hole.
