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

## Step 3 needs one more thing

Step 3 drives a browser. It needs the UiPath browser extension with "Allow
access to file URLs" enabled, and on macOS, Accessibility and Screen Recording
granted to UiPath. `README.md` covers this when you reach step 3. Steps 1, 2, 4
and 5 do not need it.

## If the agent ignores the course

Say:

> read AGENTS.md and course/agent/PROCEDURE.md, then start the course
