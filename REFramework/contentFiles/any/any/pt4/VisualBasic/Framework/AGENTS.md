# REFramework agent guide (VisualBasic, Cross-platform)

The project root is the folder above this one (it holds `project.json`); every path here is relative to it. This guide lives in `Framework/` because Studio overwrites the root `AGENTS.md`/`CLAUDE.md` with generic files.

- Edit `.xaml`/`.cs` with the **uipath-rpa** skill, not by hand, then validate with `uip rpa analyze .`.
- To build or change a process, follow **Build a process** in order and obey **Rules**.

| | |
|---|---|
| Compatibility | Cross-platform (Portable). Windows, macOS, Linux and serverless robots. |
| Language | VisualBasic, fixed for every workflow |
| .NET | *Minimum Robot version* in Project Settings: 24.10 = .NET 8 (default, runs everywhere incl. serverless), 26.10 = .NET 10 (Robot 26.10+ only). |
| Configuration | `Data/Config.json` |
| Transactions | Orchestrator queue by default; replaceable |
| Running | Foreground (`requiresUserInteraction: true`): attended robots start it from Assistant; Orchestrator needs an unattended robot. Serverless needs Background (Project Settings) and Minimum Robot version 24.10. |

## Build a process

1. **Clarify with the user**: what one transaction is (ask if unclear; a batch of PDFs is usually one transaction per PDF), where transactions come from, which applications are driven and how they log in, which failures are business rule exceptions (bad data; retrying will not help) and which values differ per environment.
2. **Configure** `Data/Config.json`: set `logF_BusinessProcessName`; for each per-environment value, add a key to Settings. Credentials go in Orchestrator assets, never in the file (it ships in clear text). Keep `MaxRetryNumber` at `0` while developing.
3. **Connect the source.**
   - Queue: Select the queue on *Get Transaction Item* (`GetTransactionData.xaml`). It ships empty; Studio records the choice as a queue resource of the project. Something else (a dispatcher, an API) fills the queue. Keep `MaxRetryNumber` `0`; retries are set on the queue.
   - Other source: change `TransactionItem`'s type in `Main.xaml` and the matching argument in `GetTransactionData.xaml` (`out_`), `Process.xaml` and `SetTransactionStatus.xaml` (`in_`), then *Import Arguments* on each Invoke Workflow File. In `GetTransactionData.xaml`, load the data when `in_TransactionNumber` is 1, return `io_dt_TransactionData.Rows(in_TransactionNumber - 1)`, and return `Nothing` when there are no more items (that ends the run). Set `MaxRetryNumber` to the in-process retries wanted.
4. **Applications**: open and log in in `InitAllApplications.xaml`; close in `CloseAllApplications.xaml` (runs on every exit and between retries); add *Kill Process* per application in `KillAllProcesses.xaml` (ships empty).
5. **Business logic** in `Process.xaml`, for **one** transaction; move larger steps to their own workflows and invoke them, passing `in_Config`. Throw `New BusinessRuleException("Amount is negative")` for bad data; let every other exception propagate.
6. **Logging values** in `GetTransactionData.xaml`: `out_TransactionID` (e.g. invoice number), optionally `out_TransactionField1`/`2` (e.g. date, amount). No sensitive data.
7. **Verify**: adapt `Tests/`, run them, and `uip rpa analyze .`. On a fresh project this fails with the `Queue name` error until a queue is selected (see The queue).

**Example, adding a queue field:** the dispatcher adds `InvoiceNo` to the item's specific content; `Process.xaml` reads `in_TransactionItem.SpecificContent("InvoiceNo").ToString`; `GetTransactionData.xaml` sets `out_TransactionID` to the same value so it appears in the logs.

## Rules

- No catch-all Try Catch around `Process.xaml` and no Global Exception Handler: the framework classifies and routes exceptions itself.
- Do not restructure `Main.xaml` or rename framework workflows or their arguments; extend them.
- Pass `in_Config` to every new Invoke Workflow File in a framework workflow (a missing binding is only a warning).
- Invoke paths are relative to the project root: `Framework/Process.xaml`.
- Keep every `sap2010:WorkflowViewState.IdRef` unique when copying activities.
- `MaxRetryNumber` stays `0` with a queue. No secrets in `Data/Config.json`, log messages or logging fields.

## Reference

### Layout

```text
project.json               entry point Main.xaml
Main.xaml                  state machine
Data/Config.json           configuration
Framework/                 framework workflows (and this guide)
Tests/                     test cases, Tests.xlsx
```

### Configuration

Two objects, **Settings** (per environment) and **Constants**. `InitAllSettings.xaml` reads both (`in_ConfigSections`) into the `Config` dictionary. Every workflow except `KillAllProcesses`/`CloseAllApplications` receives `Config` as `in_Config`; read with `CInt(in_Config("MaxRetryNumber"))`.

| Name | Default | Meaning |
|---|---|---|
| `logF_BusinessProcessName` | `Framework` | Groups related processes' logs. |
| `MaxRetryNumber` | `0` | In-process retries after a system exception; `0` with a queue. |
| `MaxConsecutiveSystemExceptions` | `0` | Stop the job after this many in a row; `0` = off. |
| `RetryNumberGetTransactionItem` / `RetryNumberSetTransactionStatus` | `2` | Retries of those activities when they throw. |
| `ShouldMarkJobAsFaulted` | `False` | Fault the job if Initialization fails or the consecutive limit is hit. |
| `LogMessage_*`, `ExceptionMessage_ConsecutiveErrors` | | Static text of framework messages. |

### States (`Main.xaml`)

| State | Behaviour | Invokes |
|---|---|---|
| Initialization | First run (`Config Is Nothing`): read configuration, kill leftover processes. Then open applications. Failure goes to End Process. Re-entered after each system exception. | `InitAllSettings`, `KillAllProcesses`, `InitAllApplications` |
| Get Transaction Data | If Orchestrator requested a stop (`ShouldStop`), end. Otherwise fetch the next item; none or error ends. | `GetTransactionData` |
| Process Transaction | Process one item; outcome Success, Business or System Exception. | `Process`, `SetTransactionStatus` (may invoke `RetryCurrentTransaction`, `CloseAllApplications`, `KillAllProcesses`) |
| End Process | Close applications; on every exit path. | `CloseAllApplications`, `KillAllProcesses` |

### Shared variables (`Main.xaml`)

`Config` (Dictionary), `TransactionItem` (QueueItem; change for other sources), `TransactionNumber` (Int32, from 1), `TransactionID`/`TransactionField1`/`TransactionField2` (String, logging), `dt_TransactionData` (DataTable, tabular sources), `RetryNumber`, `ConsecutiveSystemExceptions` (Int32), `SystemException`, `BusinessException`, `ShouldStop` (Boolean).

### Workflows (`Framework/`)

| Workflow | Purpose | Arguments |
|---|---|---|
| `InitAllSettings.xaml` | Builds `Config` | `in_ConfigFile`, `in_ConfigSections`, `out_Config` |
| `KillAllProcesses.xaml` | Kills leftover processes | none |
| `InitAllApplications.xaml` | Opens and logs in to applications | `in_Config` |
| `GetTransactionData.xaml` | Next item; `Nothing` ends the run | `in_TransactionNumber`, `in_Config`, `out_TransactionItem`, `out_TransactionID`, `out_TransactionField1`, `out_TransactionField2`, `io_dt_TransactionData` |
| `Process.xaml` | Business logic, per item | `in_TransactionItem`, `in_Config` |
| `SetTransactionStatus.xaml` | Records the outcome; updates queue items only | `in_TransactionItem`, `in_Config`, `in_SystemException`, `in_BusinessException`, `in_TransactionID`, `in_TransactionField1`, `in_TransactionField2`, `io_RetryNumber`, `io_TransactionNumber`, `io_ConsecutiveSystemExceptions` |
| `RetryCurrentTransaction.xaml` | Retry decision | `in_Config`, `in_SystemException`, `in_QueueRetry`, `io_RetryNumber`, `io_TransactionNumber` |
| `CloseAllApplications.xaml` | Closes applications | none |

### The queue

*Get Transaction Item* ships with **no queue**. Until one is selected, validation (and `uip rpa analyze`) fails with `Value for a required activity argument 'Queue name' was not supplied`: expected, not a bug. Leave the activity's folder empty to use the process's folder. Queue activities need an Orchestrator folder in scope: `Error code: 1101` means none (it reads like an auth error), `Error code: 1002` means the queue is not in that folder.

### Exceptions and retries

`BusinessRuleException`: not retried, item skipped (Orchestrator: Business Exception). Any other exception: system exception, retried and applications re-initialised (Application Exception). With a queue the queue's *Max # retries* applies; without one, `MaxRetryNumber`.

### Screenshots

None: this variant has no screenshot workflow. Add one to the System Exception branch of `SetTransactionStatus.xaml` if needed.

### Logging

Fields `logF_TransactionID`, `logF_TransactionField1`, `logF_TransactionField2`, `logF_TransactionNumber`, `logF_TransactionStatus` are added per message and removed after it; `logF_BusinessProcessName` once at start. Logs are not encrypted.

### Expressions

VB: expressions sit in `[...]` inside attributes; names are not case-sensitive.

### Tests (`Tests/`)

| File | Purpose |
|---|---|
| `MainTestCase.xaml` | Runs each workflow on the *Tests* sheet of `Tests.xlsx`, writes PASS/FAIL to *Result*, asserts none failed. Argument-less workflows only. `Tests.xlsx` is read with Workbook activities (no Excel needed). |
| `GetTransactionDataTestCase.xaml`, `ProcessTestCase.xaml` | Fetch / process a real item; need the queue selected on *Get Transaction Item* and a folder. |
| `InitAllApplicationsTestCase.xaml`, `InitAllSettingsTestCase.xaml` | Start-up/shutdown; configuration loading. |
| `WorkflowTestCaseTemplate.xaml` | Given/When/Then template. |

### Troubleshooting

| Symptom | Fix |
|---|---|
| `Value for a required activity argument 'Queue name' was not supplied` | Select the queue on *Get Transaction Item*. |
| `The <path> workflow cannot be found` | Path not relative to the project root, or the project was opened one folder too high. |
| `feature not available` | Assign a Studio licence to the user on this organization. |
| Workflow compiler not found (CLI) | Put the .NET SDK 8.0 on `PATH`. |
| `WorkflowRunnerService does not exist` after the first `uip rpa run` | Clear `.local/.codedworkflows`, `.local/.jit`, `.local/install` before each CLI run. |
| CS1705 (`System.Runtime` 10.0.0.0 vs 8.0.0.0) compiling `CodedWorkflows` | Studio runs on .NET 10, project on .NET 8. Set Minimum Robot version 26.10, close, delete `.local`, reopen (then Robot 26.10+ only). |
| Job faults at once: `Error converting value "net10.0"` | Robot older than 26.10 (e.g. serverless). Set Minimum Robot version 24.10 and republish. |

## Publishing

- Process: Studio *Publish*, or `uip rpa pack . <out>` and upload the `.nupkg`.
- Solution: tick *Create new solution* when creating the project (or `uip solution projects add`), then publish with Studio or `uip solution pack` / `publish` / `deploy`. The queue picked on *Get Transaction Item* is a project resource, bound to a real queue at deploy.

Check `uip <group> --help` for current command forms.
