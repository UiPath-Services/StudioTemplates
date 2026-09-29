# Setup: get an agent

Do this once, before the course. It is not part of the hour.

Pick one:

| You want | Go to |
|---|---|
| The quickest start, nothing to install | **A. Autopilot** |
| Claude Code or Codex, docked inside Studio like Autopilot | **B. An agent as a Studio panel** |
| Claude Code, Codex, Antigravity or another agent, in a terminal | **C. An agent in a terminal** |
| The UiPath CLI and skills on your whole machine, for every editor and agent you use | **D. Machine-wide install** |

A needs nothing. B and C are a few toggles in Studio. D is one command.

## A. Autopilot

Built into Studio. Reads this project's `AGENTS.md` on its own.

1. Open this project in Studio.
2. Open the Autopilot panel:
   - Windows: `Ctrl+Alt+I`
   - Mac: `⌥⌘I` (Option+Command+I)

   Or click **Ask Autopilot** on the project's start page, next to Open Main
   Workflow.
3. Say: `start the course`

If the shortcut does nothing, Autopilot is not enabled for your organisation or
is not connected. The panel says so when you open it from the start page. That is
a governance setting. Ask your admin, or use B or C.

## B. An agent as a Studio panel

Claude Code and Codex can run inside Studio as a panel on the right, next to
Properties. This works like Autopilot, with the agent you already use.

1. Install the agent itself and sign in to it:
   - Claude Code: https://claude.com/claude-code
   - Codex: https://github.com/openai/codex
2. In Studio, go to **Tools > Coding Agents**.
3. Under **UiPath CLI**, make sure the switch is **Enabled**.
4. Find your agent in the list. **CLI status** should say **Installed**. If it
   says **Not installed**, Studio cannot find the agent; finish step 1.
5. Turn **UiPath skills** to **On**. Studio installs the UiPath skills into that
   agent so it knows how to work with UiPath projects.
6. Turn **Studio extension** on. For Claude Code it says **Installed**; for Codex
   it says **Available** until you switch it on.
7. Back in the project, the agent has its own tab in the right-hand panel bar.
   Open it and say: `start the course`

Antigravity, Kiro and OpenCode have no Studio panel. Use C.

## C. An agent in a terminal

Studio has a terminal built in: the **Terminal** tab at the bottom, next to
Output and Errors. It opens in the project folder, so there is nothing to
navigate to. Any other terminal works too; just `cd` into the project folder
first.

1. Install the agent and sign in to it:
   - Claude Code: https://claude.com/claude-code
   - Codex: https://github.com/openai/codex
   - Antigravity: https://antigravity.google
2. In Studio, **Tools > Coding Agents**: switch **UiPath CLI** to **Enabled**
   and turn **UiPath skills** to **On** for your agent. If **CLI status** says
   **Not installed**, Studio cannot find the agent; check step 1.
3. Open the **Terminal** tab. If it was already open, close it and open it
   again so it picks up the CLI on your PATH.
4. Start the agent: `claude`, `codex`, or the command your agent uses.
5. Say: `start the course`

No separate UiPath sign-in is needed. The CLI that Studio provides uses the
account you are signed in to Studio with.

## D. Machine-wide install

Use this if you want the `uip` CLI and the UiPath skills available everywhere on
your machine, not only through Studio: other editors, Cursor, several agents at
once, or a terminal outside Studio. It is what the UiPath docs describe.

You need Node.js 20 or later and admin rights. The installer checks Node,
installs the `uip` CLI, installs the UiPath skills into the agents it finds, and
adds the .NET SDK and Python.

macOS or Linux:

```bash
curl -fsSL https://download.uipath.com/uipath-cli/install.sh | bash
```

Windows, in PowerShell:

```powershell
irm https://download.uipath.com/uipath-cli/install.ps1 | iex
```

Then sign in. This copy of the CLI is separate from the one inside Studio, so it
needs its own login:

```bash
uip login
```

Check it:

```bash
uip --help
uip skills list
```

The list should include `uipath-rpa`. To add skills to one more agent later:

```bash
uip skills install --agent claude     # or: codex, cursor, gemini, copilot, opencode
```

Then open your agent in the project folder, or in Studio's Terminal tab, and say:
`start the course`

Reference: https://docs.uipath.com/coding-agents/standalone/latest/user-guide/install-and-set-up

## Where source control is in Studio

Steps 1 and 2 need you to commit and to read a diff yourself. Both live in one
panel.

Open **Source Control** from the branch icon in the left-hand bar — second from
the top, above the package and activities icons. The panel has three parts:

- **Changes** — every file you or the agent has modified, each marked `M`. Click
  one to see its diff.
- A **Message** box and a blue **Commit** button. On macOS `⌘↵` in the message
  box commits without reaching for the mouse.
- **GRAPH** at the bottom — the history, newest at the top, with a badge on the
  branch you are on.

Step 1 asks you to initialise the repository, which you also do from this panel
before there is anything in the graph. The agent is not allowed to do it for you;
that is deliberate, and it is the one thing in the course that is yours alone.

If your Studio looks different, it has moved between versions — tell the agent
so, rather than letting it guess.

## Step 3 needs the browser extension

Step 3 drives a real browser against `assets/expenses.html`. Steps 1, 2, 4 and 5
do not need any of this. Do it before step 3 rather than during it.

**1. Install the UiPath browser extension** for the browser you will actually
run in, from Studio (**Tools > UiPath Extensions**) or UiPath Assistant
(**Preferences > Browser Extensions**). Install it this way rather than from the
browser's own extension store: it is named differently on different platforms,
and installing from Studio gets you the right one without having to know which.

**2. Allow the extension to read local files.** The portal is a local `file://`
page, and an extension cannot see inside one unless it is allowed to. It is off
by default, nothing warns you, and the failure it causes says nothing about
files or permissions. The exact steps:

1. Copy this into Chrome's own address bar and press Enter:

   ```
   chrome://extensions/?id=pgnfaifdbfoiehcndkoeemaifhhbgkmm
   ```

   That id is the Windows extension. On macOS use
   `conkfbpnllelocpogdmbilgmnkabjfmf`. If you are not sure which you have, ask
   the agent — it can read the id off your machine and give you the exact link.

   It has to be pasted rather than clicked: Chrome blocks other applications
   from navigating you to its own settings pages, so nothing can open this for
   you from outside the browser.

2. You land on that extension's **Details** page. Scroll down past **Allow in
   Incognito**.
3. Turn on **Allow access to file URLs**.
4. **Quit the browser completely and reopen it** — not just the window. The
   permission is applied when the extension loads, so until you restart, the
   setting reads as on while the extension still behaves as if it is off. This
   is the step people skip, and skipping it looks exactly like the toggle not
   having worked.
5. Tell the agent it is done. It reads the setting back rather than taking your
   word for it, which is what catches a switch flipped on the wrong extension or
   in a different Chrome profile.

If step 3's switch is greyed out, stop — see the note below.

**If the switch is greyed out**, your machine is managed and Chrome policy is
pinning it. No amount of clicking will move it. The setting your IT team needs is `ExtensionSettings` with
`file_url_navigation_allowed: true` for the UiPath extension's id — Chrome 119
and later, named per extension, no wildcard. Ask them; it is a two-line policy
change and it fixes it for everyone on your build rather than just you.

**Use Chrome or Edge for step 3, and make it your default browser first.**
Safari has no per-extension file-URL switch, so the portal cannot be inspected
there at all — and the automation opens whichever browser is your machine
default, not whichever one you set up. On macOS that default is Safari unless you
have changed it. Getting this wrong produces the most confusing failure in the
course: every prerequisite reports healthy and the page is simply invisible.

**3. Grant the operating system's automation permissions.** On macOS that is
Accessibility and Screen Recording, under System Settings > Privacy & Security,
for Studio, Assistant and the terminal you run the agent in.

### If step 3 will not capture

The failure is quiet rather than loud. Capture appears to succeed but returns
desktop elements instead of page elements, and none of the portal's ids
(`employee-id`, `submit-btn`) appear.

Do not work around it, and do not let the agent hand-write selectors. Say:

> step 3 cannot capture the portal, check the browser prerequisites

The agent knows the signals to look for and what to check, and repairs what it
can without you going through settings yourself.

## If the agent ignores the course

Say:

> read AGENTS.md and course/agent/PROCEDURE.md, then start the course
