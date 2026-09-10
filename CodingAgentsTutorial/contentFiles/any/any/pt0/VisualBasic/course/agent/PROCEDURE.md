# How to run a step

The procedure for guiding a UiPath developer through the Coding Agents Tutorial.
Plain markdown. Any agent can follow it. `AGENTS.md` tells them to.

Use this when the user asks to start, continue or resume the course, asks what
step they are on, or asks for the next step.

The user builds automations every day and has never used a coding agent. Assume
no git command line.

The curriculum is in `README.md`. Read it. Do not restate it from memory.

`AGENTS.md` holds the full ruleset. Read it if it is there.

Expect it not to be. Installing the UiPath skills into an agent — which
`course/SETUP.md` tells the learner to do before they start — overwrites
`AGENTS.md` and `CLAUDE.md` with a skill-routing index, and the course rules go
with them. If `AGENTS.md` does not mention the course, this file is the whole
ruleset for running the course, and the rules below are the ones that bind. Do
not assume a rule you half-remember from somewhere else.

It is not a substitute for knowing the project. `.claude/rules/project-context.md`
survives the same overwrite and holds the authoring detail — activity gotchas,
naming conventions, the analyzer rules. Read it before you edit a `.xaml`.

This procedure does not replace your other skills. Steps 3, 4 and 5 author
workflows; use a UiPath RPA skill for `.xaml` work if you have one. If that
skill wants to carry on to the next task, the course rules win: one step, then
stop.

## The rules

**One step, then stop.** Run one step, name the next, hand over its first
learner line, and do none of its work. "Continue", "next" and "resume" take them
to the next stop, not through the step.

**A check is a learner line.** Where the learner has to look at Studio and tell
you what they see, you report, you ask, and you end your turn. You do not answer
for them and you do not carry on.

**Commit only after they have confirmed.** Finishing the work is not finishing
the step; their confirmation is. If you have not asked what they see and had an
answer back, you have not reached the commit.

**If you commit too early, put it back yourself.** Do not hand them a git
command — this learner works in Studio's Git panel and the course assumes no git
command line. Return the change to pending so they can review and commit it,
then correct the `course/PROGRESS.md` row and say which rows you corrected. The
commit is easy to undo; the record is what survives.

**Never write a confirmation they did not give.** Machine evidence is yours to
report — `validate` output, a build result, a run result. Their judgement is
theirs. A row that blurs the two misrepresents the learner.

**Never revert a modified file quietly.** If a file you did not expect has
changed, name it and say why before you touch it.

**A scripted edit puts back the exact bytes it found at the file's edges.** Two
of these bite. Line endings: Studio writes CRLF on Windows, these copies are LF,
and normalising a whole file turns a twenty-line change into hundreds. And the
trailing newline: most `.xaml` here and `project.json` end mid-line, with no
final newline at all. Add one and git reports `\ No newline at end of file` as a
deletion on a line you never touched. `validate`, `build` and `run` all stay
green through both, so nothing warns you — only the diff does.

**A diff much larger than the change you made is a stop.** Check the size of the
diff before you report. Out of proportion means find out why and fix it before
the learner sees it. An unreviewable diff fails the step even when the build
passes, because reviewing the diff is the step.

**Never edit `README.md`.** It holds the course.

**Never run `git init`.** Step 1 is theirs, in Studio's Git panel.

**Do not reveal the planted bug before step 2 asks for it.**

**If step 3 cannot capture UI targets, repair it before you stop.** Do not
hand-write selectors to get past it. The failure is quiet — capture returns
success and the wrong tree, so judge the tree, not the exit code. Any of these
means the browser bridge is dead: no browser tabs reported for a window that
visibly has them; capture coming back from a desktop-accessibility subsystem
rather than the browser DOM; the portal's ids missing from the tree. Then check
four things in order, from the machine rather than by asking:

1. The extension is installed, and is the one for *this* platform — the name
   differs between platforms and the wrong one looks plausible. Read the
   browser's own record of what is installed; do not conclude from a name, and
   do not tell them to install anything before you have looked.
2. Its granted permissions include local files. That is the "Allow access to
   file URLs" switch; reading the permissions is quicker and surer than asking
   them to go and look. If it is off, that is the fix — give them the click path
   from `course/SETUP.md`.
3. The browser's native-messaging manifest still names a file that exists. A
   product upgrade can leave it pointing at a wrapper that has moved, and that
   produces every symptom above *with* a correct extension and file access on —
   so gather all four findings before you conclude anything. A stale manifest
   looks exactly like a missing extension, and it is the one most often
   misdiagnosed: the numbering is the order to look in, not permission to stop at
   the first thing that looks wrong. Repair it by reinstalling the extension from
   Assistant or Studio, which rewrites the manifest. Never write a product path
   of your own into it.
4. The operating system has granted automation permissions.
5. **The tool opened a different browser than the one that is set up.**
   `uip rpa uia interact browser open` uses the machine's default browser. On
   macOS that is often Safari, which has no per-extension file-URL switch at all,
   so a portal opened there comes back as a discarded tab with no page tree while
   every check above reports healthy. Look at which browser the output names. If
   it is not the one carrying the UiPath extension, say so and open the portal in
   that one instead — this is the cause the others miss, and the one that looks
   least like a fault.

Say what was wrong even when you fix it. A silent repair teaches nothing, and
this is the setup most likely to bite them again on their own machine. A marker
on a tab saying it is a local or restricted page means that tab is not
inspectable; no marker means it is — absence is the good case.

Where a browser keeps this state differs by browser, platform and version, and
product paths move between releases. Find it on the machine in front of you.
Never carry a path, an extension id or a version over from another machine, from
these notes, or from memory.

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
8. Report the check, then ask them to confirm one specific thing in one
   specific place — see "What a reply looks like". End your turn. Nothing below this
   line happens until they have answered. This is the last pause of the step and
   the easiest one to lose: the work is done, the evidence is green, and
   committing feels like tidying up. It is not. A commit they did not review
   turns the thing they were meant to learn into something you did for them.
9. When they have confirmed, commit, naming the step.
10. Append one row to `course/PROGRESS.md`. The row records what they told you,
    not what you concluded.
11. Stop. Name the next step and give its first learner line. Do none of its
    work.

### Step 1

There is no repository yet.

- Skip the working-tree check in item 4. Confirm the files are present. "Not a
  git repository" is the starting condition, not an error.
- Do not create or edit a `.gitignore`. Studio may write a default one when they
  initialise the repository, or there may be none at all; either way it is
  theirs, not yours to manage.
- Once they say the first commit is in, look at what it contains before you go
  on, and say what you see. On a fresh template that is around twenty files and
  there is nothing to report.
- Expect the noise to arrive later, not here. `.local/`, `.project/`,
  `.settings/` and `Data/summary.xlsx` do not exist in a fresh template — your
  own first `uip rpa run`, in step 2, creates them. So the first time the learner
  opens a diff, it will contain folders neither of you put there. Say so at that
  moment, name them as Studio's caches and generated output, and tell them a
  `.gitignore` is the usual fix and it is theirs to add. Do not wait to be asked
  and do not quietly work around it.
- That leaves you with a working tree that will not come clean, and three rules
  that pull against each other. The order of precedence is: never create a
  `.gitignore`, never revert a file quietly, and only then aim for a clean tree.
  So when you stage a step, stage the files you changed for that step and say
  which. Do not stage generated output — `Data/summary.xlsx` is rewritten by
  every run — and do not quietly revert it to tidy up. If the tree cannot be
  clean without breaking one of the first two rules, leave it dirty and say why.
  A learner who understands the noise is better off than one handed a clean tree
  by a rule you broke.
- The initial commit in item 9 is theirs, made in Studio's Git panel. Wait for
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

How a stop ends depends on one thing: **did you change any files?**

**You changed nothing.** There is nothing for them to review, so end with the
next line — the one that acts on what you just reported. Report the finding in
full, say plainly that nothing changed, and hand over the instruction. Do not
ask them to confirm the finding, and do not send them into Studio to re-verify
something you have already quoted to them. They are reading your answer, which
is the whole point of a read-only stop; making them audit it as well is
busywork, and it stalls the turn on a question they cannot answer.

> `Workflows/ValidateExpense.xaml` compares `in_Amount > 50`, so a claim for
> exactly 50.00 with no receipt is accepted — row `E-1005` in the data is
> exactly that. The rejection message beside it already says "50.00 or more",
> so the condition contradicts its own message. Nothing changed; the working
> tree is clean.
>
> Part B is the fix, scoped to that one condition so the diff stays one line.
> Say:
>
> > Fix it. Change only that condition.

**You changed files.** Now the opposite holds, and this is the confirmation the
course exists to teach: they read the diff before it is kept. Name the panel and
what they should see in it, then wait. "Tell me what you see in the diff panel"
is right here, because there is something in front of them that you cannot see
for them.

"Start step N", "continue" or "next step" takes them to stop 1 of that step. You
hand over the instruction and end your turn. It does not mean run the step.

### Step 1

1. Explain in two or three sentences why a snapshot matters, and ask them to
   initialise the repository and make the first commit from Studio's source
   control. End your turn. The user does it.

   The path is in `course/SETUP.md` under "Where source control is in Studio":
   the **Source Control** panel, from the branch icon in the left-hand bar, with
   a **Message** box and a **Commit** button, and **GRAPH** below for history.
   Take it from there rather than from memory, and do not invent a menu name —
   the layout moves between Studio versions, and a confidently wrong one on your
   first reply costs their trust before the course has started. If theirs does
   not match, say so plainly and let them find it; admitting the gap is fine,
   guessing is not.

   If a repository already exists and is clean, say so and go to stop 2.
2. When they say it is done, confirm the working tree is clean. Hand them the
   step 1 line with its reason: an agent reads the same files Studio does, so
   it can tell them what an unfamiliar project does before they touch it, and
   its description gives them something to check against the canvas. End your
   turn.
3. When they send it, describe the project. Tell them what to compare against
   the canvas — name the workflows and what each one does. You changed nothing,
   so do not set them an audit; the description is the deliverable and they will
   notice themselves if it does not match what they see. Close by telling them
   to say so if anything looks wrong, and otherwise that step 2 is next. End
   your turn.
4. When they confirm it matches, log the row and commit it, name step 2, end
   your turn.

### Step 2

1. Hand them the Part A line with its reason: it asks the agent to look and
   report without changing anything, so they can check the answer before they
   trust it with an edit. End your turn.
2. When they send it, find the workflow and the comparison, and report both in
   full: the workflow, the exact condition, why it is wrong, and the row in
   `Data/expenses.xlsx` that proves it. Change nothing and say so.

   Then hand them the Part B line in the same turn, with its reason: "change
   only that condition" is the scope, and it is what keeps the diff to one line
   they can review. You changed nothing, so there is nothing for them to check
   — do not ask them to confirm the finding or to go and verify it in Studio.
   They read your answer and decide whether to let you fix it; that decision is
   the pause. End your turn.
3. When they send it, change the one condition. Tell them to open the Git diff
   panel and what to see there: one condition changed, nothing else. Then give
   them Part C, from `README.md`: revert the change in the Git panel, watch it
   disappear from the canvas, re-apply it by asking you or doing it themselves,
   commit, and tell you when it is committed. End your turn.
4. Part C is theirs: revert, re-apply, commit. **This step's work commit is the
   learner's, not yours** — it is the only one in the course that is, and the
   general rule at item 9 gives it to you. Part C wins: doing the revert and the
   re-commit by hand is the muscle the step exists to build, so do not commit it
   for them even after they confirm. If they ask you to re-apply the
   fix, do it and end your turn. When they say it is committed, log the row,
   name step 3, end your turn.

### Step 3

1. Point them at the prerequisites and at the portal to try by hand, and tell
   them the run will open the portal itself; they do not open it for the run.
   **Before any of that, clear the file-access gate.** The portal is a local
   `file://` page. The browser extension cannot read one unless it has been
   allowed to, that permission is **off by default**, and the failure it causes
   never mentions files or permissions — capture just returns a page-less tree
   25 minutes into the step. Clear it before you build, not after it fails.

   1. **Read the state.** Find the browser's own record of installed extensions
      and check whether the UiPath extension's granted hosts include local
      files. Report what you found either way. Do not ask them to go and look,
      and do not assume it is off because capture failed — say which it is.
   2. **You cannot set it yourself, so do not try.** The setting lives in an
      integrity-protected part of the browser's preferences: an edit is detected
      on next launch and reverted, so a change you make silently disappears and
      you would report success over a broken setup. It is protected precisely to
      stop software granting extension permissions without the person knowing.
      Their click is the consent, and it is the only thing that works.
   3. **If it is off, give them the numbered steps from `course/SETUP.md`**
      under "Allow the extension to read local files", with the extension id you
      just read substituted into the link. Quote them; do not paraphrase, and do
      not use an id from memory. Say why it is needed in one line: the portal is
      a local file and the extension cannot see inside one without this.

      Two details carry the whole thing. The link must be pasted into the
      browser's own address bar — Chrome blocks other applications from
      navigating to its settings pages, so you cannot open it for them and
      should not imply you can. And they must **quit and reopen the browser**
      afterwards, because the permission takes effect when the extension loads;
      without that the setting reads on while the extension still behaves as
      off, which looks identical to the toggle having failed.

      Then end your turn.
   4. **Verify, do not take their word.** When they say it is on, read the
      record again and confirm it changed. The setting is applied when the
      extension loads, so if it still reads off, have them reopen the browser and
      check once more. Only proceed when you have read it as on. A learner who
      flips the wrong extension's switch, or flips it in a different browser
      profile, will tell you in good faith that it is done.
   5. **Check the browser you will actually drive**, not whichever one is
      convenient. The automation opens the machine default. If that is Safari,
      the switch does not exist there at all and no amount of toggling will
      help — see `course/SETUP.md`.
   6. **On a managed Windows machine the switch may be greyed out.** Chrome
      policy can pin it, and on a corporate build it often does. The policy is
      `ExtensionSettings` with `file_url_navigation_allowed` set to `true` for
      that extension id — Chrome 119 and later, per id, no wildcard. If the
      switch will not move, that is the reason, and the fix belongs to whoever
      manages the machine. Say that plainly and offer to write the request for
      them; do not go near the registry yourself. Setting machine policy is an
      admin-scope, machine-wide change made on someone else's behalf, and it is
      further outside your remit than the toggle you already will not touch.

   Hand them the plan line with its reason: this is the shape of a real request,
   and a plan is cheaper to correct than a built workflow. End your turn.
2. When they send it, describe how you would build it. Build nothing. End your
   turn.
3. When they say go ahead, build it. Validate, build, run. Report every check
   in `README.md`'s step 3 block with evidence — count them there, do not assume
   how many there are — then ask them to look at the portal's submissions table
   and `Data/summary.xlsx`, and tell you what those two show. End your turn.

   One requirement is not in that list and matters more than the rest: the PDD
   says "the policy rules are already written down in the process. Use that
   check rather than a new copy of the rules." So invoke
   `Workflows/ValidateExpense.xaml` for the decision. Do not re-implement the
   threshold inline. Say explicitly that you reused it. If you copy the rule
   instead, every stated check still passes and step 4's tests end up guarding a
   copy nothing runs — which quietly removes the point of the whole course.
4. When they confirm the portal table and the summary, commit, log the row. In
   two lines, point them at "Asking well" in `README.md`: the vague line against
   the scoped one they just used. Name step 4, end your turn.

### Step 4

1. Hand them the line with its reason: the agent can write a test, run it and
   read the failure itself, and "run them" is what turns a claim into a result
   they can see. End your turn.
2. When they send it, add the cases, run them, fix what fails, show the run
   output. Tell them the check: the run passed, and there is a case for 50.00
   with a receipt and one without. Then ask them to open Test Explorer in Studio
   and tell you which cases are listed and how they ran. End your turn.

   How to add one, because this is the part the wording hides: in UiPath one
   `.xaml` is one test case. `Tests/ValidateExpense_Tests.xaml` is a single case
   with a single id registered in `project.json` under
   `designOptions.fileInfoCollection`. So each new case is a new file next to it,
   copying that file's shape, and each one needs its own entry there with its own
   fresh `testCaseId` GUID. Adding more assertions inside the existing file
   instead gives you one case that happens to assert several things — Test
   Explorer shows one, and the learner's check asks to see them listed. Register
   every file you add; an unregistered test does not run.

   This is the one place you edit `project.json` without asking. The rule about
   asking first covers package versions, not test registration.
3. When they confirm, commit, log the row, name step 5, end your turn.

### Step 5

1. Hand them the line with its reason: one sentence changes every workflow in
   the project, and "do not change any business logic" is what keeps the diff
   safe to review. End your turn.
2. When they send it, add the Try Catch to every workflow in the project.
   Count them first rather than trusting a number: `Main.xaml`, everything under
   `Workflows/`, and whatever step 3 added. `README.md` says five, which is right
   for the ordinary path — but it is four if step 3 was reverted, and six if step
   3 produced two workflows. Report the number you found and use it. Tests are
   not workflows; leave `Tests/` alone.

   Validate, build, run. Tell them the check: the diff touches exactly those
   files, no business logic changed, and the run still gives three accepted
   submissions. Then ask them to open Studio's Git diff panel on any of those
   files and tell you whether they see the Try Catch wrapped around the existing
   activities with nothing else changed. End your turn.
3. Wait. The Try Catch is written but not confirmed, and stop 2 ended your
   turn. Do nothing until they come back and tell you what the diff looks like.
   Not the commit, not the log row, and above all not the completion page —
   opening that before they have seen the diff celebrates work they have not
   reviewed, on the one step whose whole subject is reviewing a five-file diff.
4. When they have confirmed the diff, commit, log the row, then run "After step
   5" below — including opening `course/complete.html`. Stop.

## If you cannot run git or a shell

`README.md` offers Autopilot as the first way to take this course, and Autopilot
may have no shell and no git. Everything below assumes you can read a commit
hash and commit a file. If you cannot:

- Say so once, at step 1, before they rely on you for it. Do not discover it at
  step 5.
- The learner commits every step themselves, in Studio, which they were going to
  do for steps 1 and 2 anyway. Hand them the message to use.
- Put `—` in the Commit column and what they told you in Verification. A row
  with `—` and a real observation is worth more than no row.
- Keep appending to `course/PROGRESS.md` even so. It is the only thing that
  survives a closed conversation, and "the last logged step plus one" is how you
  resume. If you cannot write it either, say that at step 1 too: without it,
  every new conversation starts from step 1 and they will have to tell you where
  they are.
- At the end, open `course/complete.html` with whatever you can source and let
  the rest read as absent. Do not skip the page for want of a hash.

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

The format is one row per step, five columns:

```
| Step | Status | What happened | Commit | Verification |
```

`Status` is `done`, `skipped` or `failed`. Nothing else.

Put the short commit hash in Commit, or `—`. Put
evidence in Verification: "Diff: one condition changed", "Test run passed",
"user-confirmed: three rows in portal table". Not "looks good".

## After step 5

Only once step 5 is confirmed by the learner, committed and logged. If you have
not had their answer on the five-file diff, you are still at step 5 stop 3 and
none of this has happened yet.

Then: the course is over and they will not know unless you say so. Do not wait
to be asked whether there is a step 6.

1. Say the course is complete, in one line.
2. Open `course/complete.html` in their browser, passing what actually happened
   in the URL fragment. Do not rewrite the file; it reads its own parameters:

   ```
   course/complete.html#commits=<step1>,<step2>,<step3>,<step4>,<step5>&started=<ISO>&tests=<n>&files=<n>&difflines=<n>
   ```

   Take the five hashes from `course/PROGRESS.md`, oldest first. Get `started`
   from the first commit: `git log -1 --format=%aI <step 1 hash>`. The other
   three, exactly:

   - `tests` — how many test cases exist, counted from
     `designOptions.fileInfoCollection` in `project.json`.
   - `files` — how many workflows step 5 wrapped, the number you reported at
     step 5 stop 2.
   - `difflines` — added plus deleted lines from the first commit to now:
     `git diff --shortstat <step 1 hash> HEAD`. No `~1`: step 1's commit is the
     root, so `<hash>~1` does not exist and the command fails outright.
   - `status` — one word per step, in order, from the Status column of
     `course/PROGRESS.md`: `done`, `failed` or `skipped`. Pass it whenever any
     step is not `done`, or the page reports a clean sweep over a step that
     failed. Leave a commit slot empty for a step with no hash —
     `commits=a1b2c3,,d4e5f6` — because the page reads the slots by position and
     a missing one shifts every label after it. Every parameter is optional and the
   page shows absent data as absent, so pass only what you can source — never a
   figure you estimated.

   Pass the values as a **query string**, not a fragment: `complete.html?commits=...`.
   macOS `open` silently strips a `#...` fragment from a `file://` URL, so a page
   opened that way shows "not supplied" against every figure and looks like it
   was given nothing. The page reads either, and the query string survives.

   Hand the opener an absolute `file://` URL, not a path — given a path it reads
   the `?...` as part of the filename and you get "file does not exist". The
   project folder name usually contains a space, so percent-encode it. Then look
   at the page: if the run report still reads "not supplied", the parameters did
   not arrive, and opening it in the browser directly rather than through the
   platform opener does preserve them.
3. Then, in three or four sentences with the real paths: what ran the course was
   three markdown files in their own project. `README.md` is the curriculum,
   this file is the procedure, `AGENTS.md` holds the rules. Invite them to open
   this one and read the pause points. They can write their own for real work.

   If your tool loaded this through `.claude/skills/coding-agents-course/SKILL.md`,
   mention that it is a short file that points here.

4. Point them at
   https://docs.uipath.com/coding-agents/standalone/latest/user-guide/overview
   and stop. There is no step 6.

The page carries the one thing the course never joins up: the tests from step 4
guard the bug from step 2. Do not explain that in chat — it is on the page, and
they should find it there and try it themselves.
