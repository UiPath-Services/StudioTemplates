# Robotic Enterprise Framework (VisualBasic, Windows)

This directory is a UiPath solution (`UiPath_REFramework.uipx`) holding one RPA project,
`UiPath_REFramework/`, created from the Robotic Enterprise Framework template. Drive solution
operations (pack, publish, deploy) through the `uip solution` CLI and do not hand-edit the `.uipx`.

**If you are an agent asked to build or change a process in this project, follow [Building a
process](#building-a-process) in order, and respect [Rules](#rules).** The rest of the file is
reference material for those steps.

| | |
|---|---|
| Expression language | **VisualBasic**, fixed at project creation, applies to every workflow |
| Target framework | **Windows** (.NET 8, `net8.0-windows`), Windows only |
| Configuration | `Data/Config.json` |
| Transaction source | Orchestrator queue by default; any other source can replace it |
| Licence | MIT |

Prose documentation ships at `UiPath_REFramework/Documentation/`. **Its configuration sections are
out of date**: they describe Studio Global Constants, which this project no longer uses. Where it
and this file disagree, this file is correct.

## What the framework is

The Robotic Enterprise Framework (REFramework) is a template for **transactional** automations. A
**transaction** is one unit of work that can be processed independently of the others: one invoice,
one queue item, one spreadsheet row, one email. The framework loops over transactions and applies
the same steps to each, and it already solves configuration, logging, exception handling with
retries, application recovery and testing. You write the business logic for one transaction in
`Framework/Process.xaml`, connect the applications the process uses, and choose where transactions
come from. Almost everything else is scaffolding you adapt, not rewrite.

## Building a process

### 1. Understand the process and find the transaction

Before editing anything, establish with the user:

- **What one transaction is.** This is the key design decision. If it is unclear, ask. A process
  that handles "a batch of PDFs" usually has one transaction per PDF, not one per batch.
- **Where transactions come from.** An Orchestrator queue (the default), a spreadsheet or table, a
  mailbox, a folder of files, an API.
- **Which applications the process drives**, and how they are logged in to.
- **Which failures are business rule exceptions** (the data is wrong, retrying will not help: a
  missing attachment, a negative amount) and which are system exceptions (a timeout, a crashed
  application, a lost connection).
- **Which values change per environment** (URLs, file paths, queue and folder names) and which
  credentials are needed.

### 2. Set the configuration

Open `Data/Config.json` and set at least `logF_BusinessProcessName` to the name of the process; it
is stamped on every log message. Add a value for every environment-specific item found in step 1 (a
key in the Settings object). Keep `MaxRetryNumber` at `0` while developing.

Never put credentials in the configuration file; it ships inside the package in clear text. Store
them as Orchestrator credential assets and read them with *Get Credential* where they are needed.

### 3. Connect the transaction source

**Orchestrator queue (default).** Select your queue on *Get Transaction Item* in
`GetTransactionData.xaml`. Read the item's data in `Process.xaml` as
`in_TransactionItem.SpecificContent("FieldName").ToString`. Something else must fill the queue (a
separate dispatcher process, an API, a person); this project only consumes it. With a queue, keep
`MaxRetryNumber` at `0` and configure retries on the queue itself, because Orchestrator already
retries failed items.

**Any other source.** Change the type of the `TransactionItem` variable in `Main.xaml`, for example
to `DataRow` for spreadsheet rows, `MailMessage` for emails or `String` for file paths. Change the
matching argument type in `GetTransactionData.xaml` (`out_TransactionItem`), `Process.xaml` and
`SetTransactionStatus.xaml` (`in_TransactionItem`), then run *Import Arguments* on every Invoke
Workflow File that passes it. Updating one file and not the others shows up as argument-mismatch
errors at design time. Then replace *Get Transaction Item* in `GetTransactionData.xaml`:

- Load the source once, on the first call (when `in_TransactionNumber` is 1), into
  `io_dt_TransactionData` (or your own variable).
- Return item number `in_TransactionNumber`, for a table
  `io_dt_TransactionData.Rows(in_TransactionNumber - 1)`, and return `Nothing` in
  `out_TransactionItem` once `in_TransactionNumber` exceeds `io_dt_TransactionData.Rows.Count`.
  Returning `Nothing` is what ends the process.
- `SetTransactionStatus.xaml` only updates queue items when the transaction is a `QueueItem`, so it
  needs no other change.
- Set `MaxRetryNumber` to the number of in-process retries you want (for example 2), because there
  is no queue to retry for you.

### 4. Connect the applications

- `Framework/InitAllApplications.xaml`: open and log in to every application the process uses. Read
  URLs and paths from `in_Config`, credentials from assets.
- `Framework/CloseAllApplications.xaml`: close them gracefully, logging out where appropriate. It
  runs on every exit path and between retries.
- `Framework/KillAllProcesses.xaml`: add a *Kill Process* activity for each application, to clear
  anything left over from a crash. It ships with only a log message.

### 5. Write the business logic

Implement `Framework/Process.xaml`: the steps for **one** transaction. For anything larger than a
few activities, put the steps in their own workflows (for example under a `Process/` folder) and
invoke them from `Process.xaml`, passing `in_Config` and the data they need.

- Throw a business rule exception when the data breaks a rule: *Throw* with `New
  BusinessRuleException("Invoice amount is negative")`. The transaction is marked as a business
  exception and skipped.
- Let every other exception propagate. The framework classifies it as a system exception, takes a
  screenshot, retries the transaction if retries are configured, and re-initialises the
  applications.

### 6. Fill in the logging fields

In `GetTransactionData.xaml`, set `out_TransactionID` to something that identifies the transaction
(an invoice number, a file name) and optionally `out_TransactionField1` / `out_TransactionField2` to
values worth reporting on (a date, an amount). They are attached to the framework's log messages as
`logF_TransactionID`, `logF_TransactionField1` and `logF_TransactionField2`, which makes the logs
usable for reporting. Never put sensitive data in them.

### 7. Test and verify

Adapt the test cases in `Tests/` to the process (see [Tests](#tests)), run them, and validate the
project (see [Checking your work](#checking-your-work)) before handing it back.

## Rules

- **Do not** wrap `Process.xaml` in a catch-all Try Catch, and **do not** add a Global Exception
  Handler. Both hide exceptions from the framework's own handler, which is what classifies and
  routes them.
- **Do not** restructure `Main.xaml`'s state machine or rename the framework workflows and their
  arguments. Extend the workflows instead.
- **Pass `in_Config` through** whenever you add an Invoke Workflow File to a framework workflow. A
  missing binding is only a design-time warning, so it is easy to miss.
- Invoke Workflow File paths are relative to the project root (the folder holding `project.json`),
  not to the calling workflow: `Framework/Process.xaml`, never `../Framework/Process.xaml`.
- Keep `MaxRetryNumber` at `0` with an Orchestrator queue.
- No credentials or other secrets in `Data/Config.json`, in log messages or in the logging fields.

## Reference

### Layout

```text
UiPath_REFramework.uipx              solution manifest, one project
UiPath_REFramework/
    project.json                     project definition; the entry point is Main.xaml
    Main.xaml                        the state machine
    Data/Config.json                 configuration: Settings + Constants
    Framework/                       the framework workflows
    Tests/                           test cases, plus Tests.xlsx
    Documentation/                   reference PDF
    Exceptions_Screenshots/          written on system-exception failures
resources/solution_folder/
    queue/TransactionQueue.json      the transaction queue, as a solution resource
    package/, process/               package and process resources
```

Paths in the rest of this file are relative to the project folder `UiPath_REFramework/`, which is
the root for every Invoke Workflow File path.

### Configuration

`Data/Config.json` has two objects: **Settings** (values that change per environment) and
**Constants** (values that rarely change). `Framework/InitAllSettings.xaml` reads both (argument
`in_ConfigSections`) into one `Config` dictionary during the Initialization state. Every framework
workflow except `KillAllProcesses`, `CloseAllApplications` and `TakeScreenshot` receives it as the
`in_Config` argument. Read a value with `CInt(in_Config("MaxRetryNumber"))` or
`in_Config("logF_BusinessProcessName").ToString`. To add a tunable value, add a key to the Settings
or Constants object.

| Name | Default | Meaning |
|---|---|---|
| `logF_BusinessProcessName` | `Framework` | Groups the logs of related processes under one business process name. |
| `MaxRetryNumber` | `0` | In-process retries after a system exception. `0` with a queue. |
| `MaxConsecutiveSystemExceptions` | `0` | Stops the job after this many system exceptions in a row. `0` disables it. |
| `ExScreenshotsFolderPath` | `Exceptions_Screenshots` | Where exception screenshots are written. Full or relative path. |
| `RetryNumberGetTransactionItem` | `2` | Retries of *Get Transaction Item* when it throws. |
| `RetryNumberSetTransactionStatus` | `2` | Retries of *Set Transaction Status* when it throws. |
| `ShouldMarkJobAsFaulted` | `False` | Mark the job as Faulted when Initialization fails or `MaxConsecutiveSystemExceptions` is reached. |
| `LogMessage_*`, `ExceptionMessage_ConsecutiveErrors` | | The static text of the framework's log and error messages. |

### States

`Main.xaml` is a state machine with four states.

| State | Behaviour | Invokes |
|---|---|---|
| Initialization | Read the configuration (first run only), kill leftover processes, open the applications. Success goes to Get Transaction Data, failure to End Process. After a system exception the framework comes back here, so applications are re-initialised before the next transaction. | `InitAllSettings`, `KillAllProcesses`, `InitAllApplications` |
| Get Transaction Data | Fetch the next transaction. None left, or an error, goes to End Process; otherwise Process Transaction. | `GetTransactionData` |
| Process Transaction | Process one transaction and record the outcome: Success, Business Exception or System Exception. | `Process`, `SetTransactionStatus` (which may invoke `RetryCurrentTransaction`, `TakeScreenshot`, `CloseAllApplications`, `KillAllProcesses`) |
| End Process | Close all applications and finish. Reached on normal completion and on abort alike. | `CloseAllApplications`, `KillAllProcesses` |

### Shared variables

Declared in `Main.xaml` and passed to the invoked workflows.

| Name | Type | Meaning |
|---|---|---|
| `TransactionItem` | `QueueItem` | The transaction being processed. Change the type to match the source (step 3). |
| `TransactionNumber` | `Int32` | Sequential counter of transactions, starting at 1. |
| `TransactionID`, `TransactionField1`, `TransactionField2` | `String` | Logging values for the current transaction (step 6). |
| `dt_TransactionData` | `DataTable` | Holds the transactions when the source is a table. |
| `RetryNumber` | `Int32` | Retries made on the current transaction. |
| `ConsecutiveSystemExceptions` | `Int32` | Compared against `MaxConsecutiveSystemExceptions`. |
| `SystemException`, `BusinessException` | `Exception`, `BusinessRuleException` | Carry the outcome of Process Transaction to the next state. |

### Framework workflows

| Workflow | Purpose | Arguments |
|---|---|---|
| `InitAllSettings.xaml` | Reads the configuration into the `Config` dictionary | `in_ConfigFile`, `in_ConfigSections`, `out_Config` |
| `KillAllProcesses.xaml` | Terminates leftover processes. Ships empty | none |
| `InitAllApplications.xaml` | Opens and logs in to the applications | `in_Config` |
| `GetTransactionData.xaml` | Fetches the next transaction; returning `Nothing` ends the process | `in_TransactionNumber`, `in_Config`, `out_TransactionItem`, `out_TransactionID`, `out_TransactionField1`, `out_TransactionField2`, `io_dt_TransactionData` |
| `Process.xaml` | **Your business logic**, once per transaction | `in_TransactionItem`, `in_Config` |
| `SetTransactionStatus.xaml` | Records and logs the outcome, updates the queue item | `in_TransactionItem`, `in_Config`, `in_SystemException`, `in_BusinessException`, `in_TransactionID`, `in_TransactionField1`, `in_TransactionField2`, `io_RetryNumber`, `io_TransactionNumber`, `io_ConsecutiveSystemExceptions` |
| `RetryCurrentTransaction.xaml` | Decides whether to retry the same transaction | `in_Config`, `in_SystemException`, `in_QueueRetry`, `io_RetryNumber`, `io_TransactionNumber` |
| `TakeScreenshot.xaml` | Captures the desktop on a system exception | `in_Folder`, `io_FilePath` |
| `CloseAllApplications.xaml` | Closes the applications. Runs on every exit path | none |

### The transaction queue

*Get Transaction Item* in `Framework/GetTransactionData.xaml` ships with no queue selected. Select
the Orchestrator queue on the activity before the first run; Studio records it as a queue resource
of the project, so it can be bound to a queue in each environment at deploy time. Leave the
activity's folder empty to use the folder the process runs in.

Queue activities need an Orchestrator folder in scope. Without one Orchestrator answers `400 - A
folder is required for this action. Error code: 1101`, which reads like an authentication failure
but is not. `Error code: 1002` means the named queue does not exist in that folder.

### Exceptions and retries

| Category | Class | Retried? | Meaning |
|---|---|---|---|
| Business | `BusinessRuleException` | No | The data breaks a business rule. Retrying changes nothing, so the transaction is skipped. Orchestrator shows it as a *Business Exception*. |
| System | any other `Exception` | Yes | A technical fault, often transient. The transaction is retried and the applications are re-initialised. Orchestrator shows it as an *Application Exception*. |

With a queue, retries are the queue's (its *Max # retries* setting) and `MaxRetryNumber` stays `0`.
Without a queue, `MaxRetryNumber` sets how many times the same transaction is retried in process.
`MaxConsecutiveSystemExceptions` stops a persistent fault from failing every remaining transaction.

### Exception screenshots

On a system exception, `SetTransactionStatus.xaml` invokes `TakeScreenshot.xaml`, which writes a PNG
of the desktop into `ExScreenshotsFolderPath` with a timestamp in the file name.
`TakeScreenshot.xaml` uses the *Take Screenshot* activity. The path is logged and, for a queue item,
written to its details so it can be found from Orchestrator. Successful transactions and business
exceptions produce no screenshot.

### Logging

The framework logs every state change, transaction outcome and exception. It adds the custom log
fields `logF_TransactionID`, `logF_TransactionField1`, `logF_TransactionField2`,
`logF_TransactionNumber` and `logF_TransactionStatus` with *Add Log Fields* and removes them
straight after the message, so they apply only to that message. `logF_BusinessProcessName` is added
once at start-up. Logs are not encrypted: never log sensitive data.

### Expressions

Expressions are VisualBasic. They are written in square brackets inside attributes, for example
`[in_Config("MaxRetryNumber")]`, and names are not case-sensitive.

### Tests

| File | Purpose |
|---|---|
| `Tests/MainTestCase.xaml` | Runs every workflow listed on the *Tests* sheet of `Tests.xlsx`, records PASS/FAIL on the *Result* sheet, then asserts no row failed. Only workflows without arguments can be listed. |
| `Tests/GetTransactionDataTestCase.xaml` | Checks that a transaction is retrieved. Needs a reachable queue and folder. |
| `Tests/ProcessTestCase.xaml` | Runs `Process.xaml` against a retrieved transaction. Same prerequisites. |
| `Tests/InitAllApplicationsTestCase.xaml` | Checks application start-up and shutdown. |
| `Tests/InitAllSettingsTestCase.xaml` | Checks the configuration is read into the `Config` dictionary. |
| `Tests/WorkflowTestCaseTemplate.xaml` | Blank Given/When/Then template for new test cases. |

Treat them as samples: add cases for the process's own workflows, especially the business rule
exceptions it throws.

### Checking your work

```bash
uip rpa analyze UiPath_REFramework          # validate + workflow analyzer
uip solution pack . --dry-run               # restore, compile, validate, analyze
```

### Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `The <path> workflow cannot be found` on an Invoke Workflow File | The path is not relative to the project root, or the project was opened one folder too high. |
| `feature not available` on validate, build or run | A Studio licence must be assigned to the signed-in user on the active organization. |
| `400 - A folder is required for this action. Error code: 1101` | A queue activity ran with no Orchestrator folder in scope. |
| `Error code: 1002` | The named queue does not exist in that folder. |
| Workflow compiler cannot be found | .NET SDK 8.0 must be on `PATH`; the compiler requires it by name. |

---

## The `.uipx` Manifest

`<solution>.uipx` is a JSON document at the solution root listing every project in the solution. Skeleton:

```json
{
    "DocVersion": "1.0.0",
    "StudioMinVersion": "2025.10.0",
    "SolutionId": "<uuid>",
    "Projects": [
        {
            "Type": "Process",
            "ProjectRelativePath": "MyProcess/project.json",
            "Id": "<uuid>"
        }
    ]
}
```

Typical layout:

```text
my-solution/
    my-solution.uipx          ← solution manifest
    AGENTS.md                 ← this file (Codex, Cursor, generic agents)
    CLAUDE.md                 ← identical copy (Claude Code)
    ProjectA/
        project.json
        bindings_v2.json      ← per-project resource declarations
        ...
    ProjectB/
        project.uiproj
        ...
```

You must manage membership via the CLI, never by editing the manifest. All these operations work entirely on local files (`.uipx` plus the solution-builder artefacts on disk) and do not require `uip login` — auth is only needed once you reach `pack` / `publish` / `deploy` / `upload`.

| Intent | Command |
|---|---|
| Create a solution | `uip solution init <name>` |
| Register an existing subfolder of the solution dir as a project (no copying — use after scaffolding *inside* the solution dir, e.g. `uip rpa create-project --location <solution-dir>`) | `uip solution projects add <project-path> [<solution-file>]` |
| Add a project from outside the solution — copies the folder at `<path>` into the solution dir and registers it (`<path>` is a local filesystem path) | `uip solution projects import <path>` |
| Unregister a project (does not delete the project files on disk) | `uip solution projects remove <project-path> [<solution-file>]` |
| List projects in the solution | `uip solution projects list` |

The `uip ... init` scaffolders (`agent init`, `maestro flow init`, `maestro bpmn init`, `maestro case init`, `api-workflow init`) **auto-register** the new project when run inside a solution directory — they walk up for the enclosing `.uipx` and add it to `Projects[]` automatically, so a separate `project add` is not needed. Pass `--skip-solution-registration` to scaffold standalone without registering; the output's `Data.SolutionRegistration.Status` is then `OptedOut`. The full set of `Status` values is: `Registered` / `AlreadyRegistered` (added in this run / already present), `NotInSolution` (no enclosing `.uipx` found), `OptedOut` (`--skip-solution-registration` passed), `Skipped` (a candidate solution was found but registration was not safe to attempt — e.g. multiple `.uipx` in one directory, or the project sits outside the solution dir), and `Failed` (manifest read/parse/write error).

## Project Types

A solution can contain multiple projects of different types. The table below lists each project type and the `uip` command that scaffolds a fresh one (or marks the row when no scaffolding command exists).

| Type | Description | Scaffold with | Skill |
|---|---|---|---|
| `Process` | RPA process — Studio workflow (XAML, Coded C#, or Hybrid) | `uip rpa create-project --name <name>` | `uipath-rpa` |
| `Tests` | Test Automation project | `uip rpa create-project --template-id TestAutomationProjectTemplate --name <name>` | `uipath-rpa` |
| `Flow` | Maestro Flow — long-running orchestrated workflow | `uip maestro flow init <name>` | `uipath-maestro-flow` |
| `CaseManagement` | Maestro Case — stateful business process (SLA, approvals, HITL) | `uip maestro case init <name>` | `uipath-maestro-case` |
| `ProcessOrchestration` | Maestro BPMN — long-running orchestrated process | `uip maestro bpmn init <name>` | `uipath-maestro-bpmn` |
| `Agent` | LLM agent project — **low-code** (configured via `agent.json`; no Python) or **coded** (Python: LangGraph / LlamaIndex / OpenAI Agents). Both subtypes share `ProjectType: "Agent"`; the discriminator is `agent.json#type`. | `uip agent init <path>` (low-code) · `uip codedagent new [name]` (coded — see the `uipath-agents` skill for the full flow) | `uipath-agents` |
| `AppV2` | Coded App — web application | `uip codedapp init <path>` | `uipath-coded-apps` |
| `Function` | UiPath Function (JS / TS / Python) | `uip function new [name]` | none |
| `Api` | API Workflow project | `uip api-workflow init <name>` | none |
| `Connector` | Integration Service connector | no CLI scaffolding — use `uip is connectors` to list / get / export existing connectors | none |
| `WebApp` | Legacy low-code UiPath App (the coded variant is `AppV2`) | no CLI scaffolding | none |

All skill should be installed by running the command: `uip skills install`. The general-purpose `uipath-platform` skill covers what isn't in a type-specific skill.

**`Library` is not a project type here.** A library is a reusable `.nupkg` consumed as a NuGet dependency, so `projects add` / `import` reject it and auto-registration returns `SolutionRegistration.Status: "Skipped"`. Publish it on its own (`uip rpa pack <project-dir> <output-path>`, then `uip or libraries upload --file <nupkg-path>`) and either reference it from a project's dependencies or attach it to this solution as a resource: `uip solution resources add --source remote --kind Library --name <library-name>`.

The type lives in either `project.uiproj` (top-level `ProjectType`) or `project.json` (`designOptions.outputType`, falling back to top-level `ProjectType` when `outputType` is absent — read or write either field). The `init` scaffolders above auto-register when run inside a solution directory (unless `--skip-solution-registration` is passed). For other scaffolders, register the project with the solution after scaffolding: use `uip solution projects add <project-path> [<solution-file>]` when the project already lives inside the solution directory (registers in place, no copy), or `uip solution projects import <path>` to copy a project from outside the solution dir into it and register it. If you pass an unknown type to those commands, they reject with the exhaustive accepted list — trust that error over this table.

## End-to-End Lifecycle

Run `uip login` first — most steps below need an authenticated session, including `solution pack` in some cases.

```bash
# 1. Authenticate
#    Interactive (browser OAuth):
uip login
#    Non-interactive (CI / CD) with client credentials:
uip login --client-id <ID> --client-secret <SECRET> --tenant <TENANT>

# 1a. (Optional) Restore project dependencies before packing. Resolves NuGet
#     deps (including authenticated Orchestrator feeds) so pack can compile.
#     Useful in CI: login -> restore -> pack. Takes <solutionPath> only; it
#     does not produce a package. Pack also restores internally, so this is an
#     optimization, not a requirement.
uip solution restore .

# 2. Pack the solution into a .zip. Two positional args:
#    <solutionPath>  — solution dir (containing .uipx) or a .uis file
#    <output-path>   — directory where the .zip is written (required unless --dry-run)
uip solution pack . ./out

# 2a. (Optional) Validate the solution against the strict deploy-time
#     pipeline without producing a package — useful as a CI gate.
uip solution pack . --dry-run

# 3. Publish the packed .zip to Orchestrator
uip solution publish ./out/<package>.zip

# 4. Fetch the default deployment configuration for the published package
uip solution deploy config get <package-name> --destination config.json

# 5. (Optional) Customize the config — see "Deployment Configuration" below

# 6. Deploy. By default this also activates; pass --skip-activate to defer.
uip solution deploy run \
    --name <deployment-name> \
    --package-name <package-name> \
    --package-version <version> \
    --folder-name <new-folder> \
    --parent-folder-path Shared \
    --config-file config.json

# 7. The deploy returns a pipeline deployment ID — track it:
uip solution deploy status <pipeline-deployment-id>

# 8. List every deployment in the active tenant
uip solution deploy list
```

**Activation lifecycle.** `deploy run` activates by default. To split the steps:

```bash
uip solution deploy run --skip-activate ...                      # leaves "Inactive (Ready to activate)"
uip solution deploy activate <deployment-name>     # activate later
uip solution deploy uninstall <deployment-name> --yes   # remove the deployment + its resources (--yes required; the CLI never prompts)
```

`uninstall` and `activate` take the deployment name as a **positional** argument (no `--name` flag). `status` takes the **pipeline deployment ID** (the GUID returned by `deploy run`), also positional.

## Package Signing

`solution pack` can sign each packed project `.nupkg` with a code-signing certificate. Signing is opt-in: add `--signing-certificate-path <cert.pfx>` to the pack command. The certificate password (`--signing-certificate-password`) is optional — passing it as `env.VAR` (e.g. `env.SIGNING_PASSWORD`) is recommended, though an inline value also works. An optional timestamp server is set with `--signing-timestamp-server <url>`.

## Workflow Analyzer and Governance

`solution pack` runs the workflow analyzer over every RPA project. Two things control it:

```bash
uip solution pack . ./out --skip-analyze                             # don't run the analyzer at all
uip solution pack . ./out --governance-file-path ./policy.json       # analyze against a local policy file
uip solution pack . ./out --automation-ops-profile StudioWeb         # analyze against the tenant policy
```

`--skip-analyze` turns off only the analyzer rules — the compiler still restores, compiles, and validates, so a broken project still fails the pack.

The analyzer rule configuration comes from whichever governance flag you use. `--governance-file-path` reads a local policy file. `--automation-ops-profile` downloads the policy published in AutomationOps for the signed-in tenant; its value is the product to fetch (`StudioWeb`, `Development`, `Business`, …). With neither flag the analyzer uses the rules shipped with the WorkflowCompiler. The two are mutually exclusive. If the tenant policy can't be fetched — no session, or nothing published — the pack falls back to the shipped rules instead of failing.

## Studio Web (Browser Editing)

Studio Web is a separate target from the Orchestrator deploy chain — it hosts a browser-based collaborative editor for solutions. The `solution upload` command pushes the local solution there and returns a `DesignerUrl` to open the solution in a browser; this is independent of `pack` / `publish` / `deploy` and does *not* produce a runtime-deployable artifact.

```bash
uip solution upload .                      # upload solution dir to Studio Web as a new solution; returns DesignerUrl
uip solution upload . --force              # force-replace the existing Studio Web solution referenced by .uipx (destroys cloud version history)
uip solution download <solution-id>        # round-trip a Studio Web solution back to disk
uip solution delete <solution-id> --yes    # remove a solution from Studio Web (--yes required; the CLI never prompts)
```

`upload` accepts a solution directory, a `.uipx` file, or a `.uis` file. It probes Studio Web for the bundled `SolutionId` first: if the cloud has no solution with that id, the upload imports as new; if a solution with that id already exists, the upload is refused unless `--force` is passed. Forcing replaces the cloud project in place and **wipes its Studio Web version history**, so use `--force` deliberately. To upload a copy as an unrelated cloud solution instead of overwriting, scaffold a fresh solution with `uip solution init` (or remove the `SolutionId` from the local `.uipx`) and re-run upload.

## Per-Project Bindings (`bindings_v2.json`)

Each project declares the resources it needs (assets, queues, buckets, processes, …) in a `bindings_v2.json` file at the project root. These declarations drive the solution's resource inventory.

After editing a project's bindings, or after `solution projects import` (which doesn't auto-sync resources), reconcile the solution-level inventory:

```bash
uip solution resources refresh     # re-scan every project, sync new / removed resources
```

`solution resources refresh` creates new resources for bindings not yet in the solution and imports from Orchestrator when a matching resource already exists.

Inspect the current solution inventory:

```bash
uip solution resources list        # everything declared in this solution
```

## Deployment Configuration

The deploy config is a JSON file fetched from Orchestrator that lists every resource the solution will provision (or reuse) and every property you can override. It is **separate from `bindings_v2.json`** — bindings declare *what a project needs*, the deploy config decides *how that maps to Orchestrator at deploy time*.

```bash
# Fetch the default config to a file
uip solution deploy config get <package-name> --destination config.json

# Set a property on a single resource
uip solution deploy config set config.json <resource-name> <property> <value>
# e.g. set config.json MyQueue maxNumberOfRetries 5

# Set a property on every resource (limited; supports e.g. conflictFixingAction)
uip solution deploy config set config.json --all <property> <value>

# Link a resource slot to an existing Orchestrator resource (instead of creating a new one)
uip solution deploy config link config.json <resource-name> \
    --name <existing-resource-name> \
    --folder-path Shared/Production

# Remove a link — the resource will be created at deploy time again
uip solution deploy config unlink config.json <resource-name>

# Apply the customized config:
uip solution deploy run ... --config-file config.json
```

If a deploy fails on a configuration issue, the CLI prints the offending resource and an `Instructions` field. Read those before retrying — most failures are an `existing-resource-name` typo, a wrong `--folder-path`, or a property that the resource type does not accept.

## Resource Types in Orchestrator

The CLI talks about the same resource types Orchestrator does:

- **Assets** — key-value configuration. Asset value types: `Text`, `Bool`, `Integer`, `Credential`, `Secret`.
- **Queues** & **Queue Items** — work-item queues for distributed transactional processing; queue items are the rows.
- **Storage Buckets** & **Bucket Files** — file storage for automation data.
- **Connections** — Integration Service connections to external systems (Salesforce, ServiceNow, …).
- **Processes / Releases** — published packages bound to a folder.
- **Triggers** & **Webhooks** — event-, time-, or queue-based job firing; outbound HTTP notifications.
- **Entities** — Data Service tables. Add or bind with kind `Entity`.
- **ChoiceSets** — enumerations used by entity fields. Add with kind `ChoiceSet`.

Resources outside a solution are managed under the orchestrator tool, which exposes per-type subgroups (`uip or assets …`, `uip or queues …`, `uip or buckets …`, `uip or bucket-files …`, `uip or libraries …`, `uip or queue-items …`, `uip or triggers …`, `uip or webhooks …`). Run `uip or --help` for the live list. Example:

```bash
uip or assets list          # list assets in the active folder
uip or assets create        # create an asset (see --help)
```

## Output Conventions for Agents

Two rules make automation reliable:

1. **Never redirect or drop stderr.** Errors and confirmations go to stderr — `2>/dev/null` will silently hide failures and produce false retries.
2. **Use `--output-filter <jmespath>`** to extract specific fields rather than piping JSON through external tools. The expression is applied to the `Data` array — start with `[]`, not with `Data[]`. On list commands with a default `--limit`, an explicit `--limit` is required with `--output-filter` (the filter only sees the records fetched). Example: `uip solution packages list --limit 100 --output-filter "[].name"`.

Standard success shape: `{ "Result": "Success", "Code": "<CommandCode>", "Data": ... }`.
Standard failure shape: `{ "Result": "Failure", "Message": "<short>", "Instructions": "<actionable>" }`.

List commands always return `Data: []` on empty results — never a message object — so consumers can rely on a consistent array shape.

## Discovering Commands

This file is a starting map, not a reference. The live source of truth is the CLI itself:

```bash
uip --help                       # top-level groups
uip solution --help              # every solution verb
uip solution deploy --help       # the deploy subgroup
uip <command> --help             # full options for any command
```

For concept or API documentation beyond CLI usage, fetch `https://docs.uipath.com/llms.txt` for the product index, then the relevant `.md` page (e.g. `https://docs.uipath.com/orchestrator/automation-cloud/latest/api-guide/assets-requests.md`).

Adjacent groups commonly used alongside solutions:

| Group | Purpose |
|---|---|
| `uip login`, `uip login tenant` | Authenticate, switch tenants |
| `uip or folders` | Manage Orchestrator folders |
| `uip or assets`, `uip or queues`, `uip or buckets`, `uip or bucket-files`, `uip or libraries`, `uip or queue-items`, `uip or triggers`, `uip or webhooks` | Manage Orchestrator resources directly |
| `uip rpa` | RPA workflow lifecycle (compile, validate, execute, scaffold) |
| `uip maestro` | Maestro Flow / Case / BPMN scaffolding |
| `uip agent`, `uip codedagent` | Coded agent lifecycle |
| `uip codedapp` | Coded Apps lifecycle |
| `uip function` | UiPath Functions |
| `uip tm` | Test Manager (test projects, sets, executions) |
| `uip is` | Integration Service (connectors, connections) |
| `uip tools` | Manage CLI tool extensions |

## Troubleshooting Quick Map

| Symptom | First thing to check |
|---|---|
| `Not authenticated` / 401 | `uip login`, then re-run |
| Command targets the wrong tenant | `uip login tenant set <tenant>`; verify with `uip login status` |
| Pack succeeds but publish 409s | Version conflict — bump the version (`uip solution pack . ./out -v <new-version>`) or delete the colliding version with `uip solution packages delete <package-name> <version> --yes` (only if intentional; `--yes` required) |
| `deploy run` fails on a resource conflict | `uip solution deploy config link config.json <resource> --name <existing> --folder-path <path>` to map to the existing one, or change `conflictFixingAction` via `config set` |
| `Resource not found` after deploy | `uip solution resources refresh` to re-sync from each project's `bindings_v2.json`; if still missing, the resource was never declared in any project |
| Output looks empty | You may have redirected stderr — confirmations and errors go there. Re-run without `2>` |

---

For deeper detail, consult:

- The official Solutions Management guide: <https://docs.uipath.com/solutions-management/automation-cloud/latest>
- The `uipath-platform` skill — auth, Orchestrator (folders, assets, queues, buckets, robots, packages, processes), solution lifecycle (pack / publish / deploy), Integration Service, and the `uip` CLI.
- The `uipath-solution-design` skill — turn a Process Design Document (PDD) into an implementation-ready Solution Design Document (SDD) and pick scope (single product vs. multi-project Solution composing RPA / Flow / Case / Agents / Apps / API Workflows).
