# How to run a step

The procedure for guiding a UiPath developer through the Coding Agents Tutorial.
Plain markdown. Any agent can follow it. `AGENTS.md` tells them to.

Use this when the user asks to start, continue or resume the course, asks what
step they are on, or asks for the next step.

The user builds automations every day and has never used a coding agent. Assume
no git command line.

The curriculum is in `README.md`. Read it. Do not restate it from memory.

The rules are in `AGENTS.md` and apply whether or not this file is loaded. Where
the two overlap, `AGENTS.md` wins.

This procedure does not replace your other skills. Steps 3, 4 and 5 author
workflows; use a UiPath RPA skill for `.xaml` work if you have one. If that
skill wants to carry on to the next task, the course rules win: one step, then
stop.

## When a conversation starts, or you do not know where they are

This is the resume procedure. Run it once per conversation, not once per
message. It exists for the learner who closed Studio on Tuesday and comes back
on Thursday.

Once you know where they are, you know. On later messages in the same
conversation, do not read the files again, do not check git again, and do not
say where they are again. Go to the next pause point. If you logged step 1 a
moment ago, they are at step 2, and one word from them is enough to hand over
step 2's first line.

1. Read `README.md` and `course/PROGRESS.md`.
2. Work out the current step. Rules below.
3. Tell the user where they are in one sentence. "You're on step 3 of 5, build
   from the PDD. Step 2 was committed as a3f9c1."
4. Check: working tree clean, expected files present, previous step verified.
5. Name the step in one line. The learner follows this conversation and may not
   have `README.md` open. Everything they need to act comes from you: why, the
   line to say, and after your work, what to check. Take the lines and checks
   from `README.md`. Do not invent them and do not embellish them.
6. Run one step, stopping at every pause point listed below. A pause means you
   end your turn. Where `README.md` says the user types the instruction, give
   them the text and end your turn. Where the work is yours, do it and end your
   turn.
7. Verify against the check in `README.md`. Evidence, not impressions.
8. Commit, naming the step.
9. Append one row to `course/PROGRESS.md`.
10. Stop. Name the next step and give its first learner line. Do none of its
    work.

### Step 1

There is no repository yet.

- Skip the working-tree check in item 4. Confirm the files are present. "Not a
  git repository" is the starting condition, not an error.
- Before they commit, copy `course/gitignore.template` to `.gitignore` if there
  is no `.gitignore` yet. Studio's working folders churn on every open, and
  without this their first commit is hundreds of files and step 2's diff is
  unreadable. Creating a file is not initialising the repository.
- The initial commit in item 8 is theirs, made in Studio's Git panel. Wait for
  them. Read its hash for the `course/PROGRESS.md` row; if you cannot, put `—`
  in Commit and what they told you in Verification. Then write the row and
  commit it yourself, `Step 1: log progress`, so step 2 opens on a clean tree.
  You may not init the repository. You may commit to it.

## What a reply looks like

Short. The learner follows this conversation; `README.md` is a reference they
may not have open. A reply carries what they need to act: what happened, if
anything did; what to check, from `README.md`; and the next line to say. Your
closing text becomes a button in some tools, so the line goes last.

After your work, before the next line:

> Fixed. In Studio's Git diff panel you should see one condition changed in the
> receipt rule and nothing else. Tell me what you see.

Handing over a line. One sentence on what it is for, then the line:

> Part A asks the agent to look without touching anything, so you can check its
> answer before you trust it with a change. Say:
>
> > The receipt rule is that any expense of 50 or more needs a receipt. Check
> > whether the project implements that correctly. Do not change anything yet.

Finishing a step:

> Committed as b7e214 and logged.
>
> Step 3 starts with:
>
> > Read specs/step-03-pdd.md and tell me how you'd implement it. Don't build
> > anything yet.

Resuming after a break, the only time you state the position:

> You're on step 3 of 5, build from the PDD. Step 2 was committed as b7e214.
>
> Step 3 starts with:
>
> > Read specs/step-03-pdd.md and tell me how you'd implement it. Don't build
> > anything yet.

Too much, and why:

> You're on step 2 of 5: Find the bug, then fix it; step 1 was recorded against
> commit 8382d68. I'm checking the course checkpoint and Git state before
> handing you the read-only bug-hunt instruction.

They were told the position a moment ago. Checkpoints and Git state are your
business, not theirs. Three sentences and none of them is the line.

## Pause points

The rule is in `AGENTS.md`: every "Say to the agent" line and every item under
**Check** in `README.md` is a stop, and you end your turn there until the learner
has told you what they saw. The list below is
that rule applied to each step, so you can see the shape. The rule is what
binds. If this list and `README.md` ever disagree, follow
`README.md`.

"Start step N", "continue" or "next step" takes them to stop 1 of that step. You
hand over the instruction and end your turn. It does not mean run the step.

### Step 1

1. Explain in two or three sentences why a git snapshot matters and what to
   click in the Git panel. End your turn. The user initialises git and commits.
   If a repository already exists and is clean, say so and go to stop 2.
2. When they say it is done, confirm the working tree is clean. Hand them the
   step 1 line with its reason: an agent reads the same files Studio does, so
   it can tell them what an unfamiliar project does before they touch it, and
   its description gives them something to check against the canvas. End your
   turn.
3. When they send it, describe the project. Tell them what to compare against
   the canvas. End your turn.
4. When they confirm it matches, log the row and commit it, name step 2, end
   your turn.

### Step 2

1. Hand them the Part A line with its reason: it asks the agent to look and
   report without changing anything, so they can check the answer before they
   trust it with an edit. End your turn.
2. When they send it, find the workflow and the comparison. Report both. Change
   nothing. Tell them the check: one workflow named, the exact comparison
   quoted, nothing changed. End your turn.
3. When they confirm, hand them the Part B line with its reason: "change only
   that condition" is the scope, and it is what makes the diff one line they
   can review. End your turn.
4. When they send it, change the one condition. Tell them to open the Git diff
   panel and what to see there: one condition changed, nothing else. Then give
   them Part C, from `README.md`: revert the change in the Git panel, watch it
   disappear from the canvas, re-apply it by asking you or doing it themselves,
   commit, and tell you when it is committed. End your turn.
5. Part C is theirs: revert, re-apply, commit. If they ask you to re-apply the
   fix, do it and end your turn. When they say it is committed, log the row,
   name step 3, end your turn.

### Step 3

1. Point them at the prerequisites and at the portal to try by hand, and tell
   them the run will open the portal itself; they do not open it for the run.
   Hand them the plan line with its reason: this is the shape of a real request,
   and a plan is cheaper to correct than a built workflow. End your turn.
2. When they send it, describe how you would build it. Build nothing. End your
   turn.
3. When they say go ahead, build it. Validate, build, run. Report the three
   checks with evidence. End your turn.
4. When they confirm the portal table and the summary, commit, log the row. In
   two lines, point them at "Asking well" in `README.md`: the vague line against
   the scoped one they just used. Name step 4, end your turn.

### Step 4

1. Hand them the line with its reason: the agent can write a test, run it and
   read the failure itself, and "run them" is what turns a claim into a result
   they can see. End your turn.
2. When they send it, add the cases, run them, fix what fails, show the run
   output. Tell them the check: the run passed, and there is a case for 50.00
   with a receipt and one without. End your turn.
3. When they confirm, commit, log the row, name step 5, end your turn.

### Step 5

1. Hand them the line with its reason: one sentence changes every workflow in
   the project, and "do not change any business logic" is what keeps the diff
   safe to review. End your turn.
2. When they send it, add the Try Catch to all five files. Validate, build, run.
   Tell them the check: the diff touches all five files, no business logic
   changed, and the run still gives three accepted submissions. End your turn.
3. When they confirm, commit, log the row, give the ending, stop.

## Working out the current step

`course/PROGRESS.md` is the record. The current step is the last logged step plus
one. No rows and no commits: step 1.

If the learner says they did a step the log does not have, ask what they did and
how they checked it, then log it `done` with `user-confirmed: <what they said>`
in Verification. If the log has a step they say they did not do, trust the log;
it was written after they confirmed.

Never infer completion from the code. A workflow that looks finished is not
evidence a step was taught.

## The log row

Logging a row means writing it and committing it, `Step N: log progress`.
Wherever this file says "log the row", do both. Never leave the row uncommitted.

Format is in `AGENTS.md`. Put the short commit hash in Commit, or `—`. Put
evidence in Verification: "Diff: one condition changed", "Test run passed",
"user-confirmed: three rows in portal table". Not "looks good".

## After step 5

Tell them what ran the course: two markdown files in their own project.
`AGENTS.md` holds the rules; this file holds the procedure. Invite them to open
it. It is plain English, and they can write their own for their real work.

If your tool loaded this through `.claude/skills/coding-agents-course/SKILL.md`,
mention that it is a short file that points here.

Three or four sentences, with the real path. Then point them to
https://docs.uipath.com/coding-agents/standalone/latest/user-guide/working-effectively
and stop. There is no step 6.
