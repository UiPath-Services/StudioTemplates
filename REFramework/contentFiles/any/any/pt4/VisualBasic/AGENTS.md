# Robotic Enterprise Framework (cross-platform)

> This directory is a single UiPath RPA project (`project.json` at the root). Build, validate and run it
> with Studio or the `uip rpa` CLI. It is not a solution on its own: to manage it in one, tick
> *Create in solution* in Studio's New Project dialog, or add it with `uip solution projects add`.

## The Robotic Enterprise Framework

This project is the Robotic Enterprise Framework, a
template for **transactional** automations. It ships a state machine, a file-based configuration
model, structured logging, exception handling with retries, and a test harness, so those concerns
are solved before you start. Write your business logic in `Framework/Process.xaml`; most of the
rest is scaffolding you adapt.

| | |
|---|---|
| Expression language | **VisualBasic** — fixed at project creation, applies to every workflow |
| Target framework | **Portable** — runs on Windows, macOS and Linux |
| Transaction source | Orchestrator queue (the shape it ships wired for) |
| Licence | MIT |

Prose documentation ships at `Documentation/`. **Its configuration sections are
out of date**: they describe Studio Global Constants in `.project/globalVariables.json`, which this
project no longer uses. Configuration is `Data/Config.json` — see below. The rest of that document
(states, workflows, exception model, logging fields, queue) is accurate.

### Layout

```text
project.json                     project definition; the entry point is Main.xaml
Main.xaml                        the state machine
Data/Config.json                 configuration: Settings + Constants
Framework/                       the framework workflows
Tests/                           test cases, plus Tests.xlsx
Documentation/                   reference PDF
Exceptions_Screenshots/          written on system-exception failures
```

Invoke Workflow File paths (for example `Framework/InitAllSettings.xaml`) are relative to the
folder that holds `project.json`, not to the calling workflow.

### Configuration

`Data/Config.json` has two objects: **Settings** (values that change per environment) and
**Constants** (values that rarely change). `Framework/InitAllSettings.xaml` reads both into a single
`Config` dictionary during the Initialization state, and every framework workflow receives it as the
`in_Config` argument. Read a value with `CInt(in_Config("MaxRetryNumber"))`.

To add a tunable value, add a key to `Config.json` — nothing else is needed. **Never put credentials
there**: it ships inside the package in clear text. Store secrets as Orchestrator assets and read
them with *Get Asset* / *Get Credential*.

### States

`Main.xaml` is a state machine with four states.

| State | Behaviour |
|---|---|
| Initialization | Kill leftover processes, read config, initialise applications. Success → Get Transaction Data; failure → End Process. After a system exception the framework returns here so applications are re-initialised before the retry. |
| Get Transaction Data | Fetch the next transaction. None left, or an error → End Process. Otherwise → Process Transaction. |
| Process Transaction | Process one transaction. Outcome is Success, Business Exception or System Exception. A system exception may be retried; a business exception skips the transaction. |
| End Process | Close all applications and finish. Reached on normal completion and on abort alike. |

### Framework workflows

Every one of these takes `in_Config` except `KillAllProcesses`, `CloseAllApplications` and
`TakeScreenshot`. **When you add an Invoke Workflow File to a framework workflow, pass `in_Config`
through** — a missing binding is only a design-time warning, so it is easy to miss.

| Workflow | Purpose | Arguments |
|---|---|---|
| `InitAllSettings.xaml` | Reads `Config.json` into the `Config` dictionary | `in_ConfigFile`, `in_ConfigSections`, `out_Config` |
| `KillAllProcesses.xaml` | Terminates leftover processes. Ships empty — add Kill Process activities | none |
| `InitAllApplications.xaml` | Opens and authenticates the applications you drive | `in_Config` |
| `GetTransactionData.xaml` | Fetches the next transaction; returning Nothing ends the process | `in_TransactionNumber`, `in_Config`, `out_TransactionItem`, `out_TransactionID`, `out_TransactionField1`, `out_TransactionField2`, `io_dt_TransactionData` |
| `Process.xaml` | **Your business logic.** Runs once per transaction | `in_TransactionItem`, `in_Config` |
| `SetTransactionStatus.xaml` | Sets and logs the outcome, updates the queue item | `in_TransactionItem`, `in_Config`, `in_SystemException`, `in_BusinessException`, `in_TransactionID`, `in_TransactionField1`, `in_TransactionField2`, `io_RetryNumber`, `io_TransactionNumber`, `io_ConsecutiveSystemExceptions` |
| `RetryCurrentTransaction.xaml` | Decides whether to retry the same transaction | `in_Config`, `in_SystemException`, `in_QueueRetry`, `io_RetryNumber`, `io_TransactionNumber` |
| `TakeScreenshot.xaml` | Captures the desktop on a system exception | `in_Folder`, `io_FilePath` |
| `CloseAllApplications.xaml` | Closes applications gracefully. Runs on every exit path | none |

Read a queue field as `in_TransactionItem.SpecificContent("FieldName")`.

### Exceptions

| Category | Class | Retried? | Meaning |
|---|---|---|---|
| Business | `BusinessRuleException` | No | The data breaks a business rule. Retrying changes nothing, so the transaction is skipped. |
| System | any other `Exception` | Yes | A technical fault, often transient. The transaction is retried and applications are re-initialised. |

Throw business exceptions explicitly from `Process.xaml`. **Do not** wrap `Process.xaml` in a
catch-all Try Catch and **do not** add a Global Exception Handler — both defeat the framework's own
handler, which is what classifies and routes the exception. `MaxConsecutiveSystemExceptions` aborts
the job once that many system exceptions occur back to back.

### The transaction queue

*Get Transaction Item* in `GetTransactionData.xaml` reads the queue named by the
`OrchestratorQueueName` setting in `Config.json` (default `TransactionQueue`), in the folder named by
`OrchestratorQueueFolder`. The queue is not created for you: create it in Orchestrator or point the
setting at an existing queue. `OrchestratorQueueFolder` is empty by default, so the robot's own
folder applies; set it to a folder path to read a queue from another folder.

### Adapting it

- Set `logF_BusinessProcessName` in `Config.json` — it is stamped on every log message.
- Set `OrchestratorQueueName` (and `OrchestratorQueueFolder` if needed) to your queue, or replace *Get Transaction Item* if the source is not a queue.
- Implement `InitAllApplications`, `CloseAllApplications` and `KillAllProcesses` for your applications.
- Implement `Process.xaml`. Throw `BusinessRuleException` for data problems; let everything else propagate.
- **Changing the transaction type** (default `QueueItem`) means changing the `TransactionItem`
  variable in `Main.xaml` *and* `GetTransactionData.xaml`, `Process.xaml` and
  `SetTransactionStatus.xaml`, then re-running Import Arguments on each Invoke Workflow File.
  Updating one and not the others surfaces as argument-mismatch errors at design time.
- Keep `MaxRetryNumber` at 0 while developing so failures surface immediately.

### Tests

| File | Purpose |
|---|---|
| `Tests/MainTestCase.xaml` | Runs every workflow listed on the *Tests* sheet of `Tests.xlsx`, classifies each outcome, writes PASS/FAIL back to the *Result* sheet, then asserts no row failed. Only argument-less workflows can be listed. |
| `Tests/GetTransactionDataTestCase.xaml` | Verifies a transaction is retrieved. Needs a reachable queue and a folder. |
| `Tests/ProcessTestCase.xaml` | Exercises `Process.xaml` against a retrieved transaction. Same prerequisites. |
| `Tests/InitAllApplicationsTestCase.xaml` | Verifies application initialisation and shutdown. |
| `Tests/InitAllSettingsTestCase.xaml` | Verifies `Config.json` is read into the `Config` dictionary. |
| `Tests/WorkflowTestCaseTemplate.xaml` | Blank Given/When/Then template for your own cases. |

`Tests.xlsx` is read with the **Workbook** activities, which are file-based and need no Excel
installation — which is why this Portable variant still depends on `UiPath.Excel.Activities`.
`Tests/MainTestCase.xaml` is the only Excel consumer in the project.

### Checking your work

```bash
uip rpa analyze .                           # validate + workflow analyzer
uip rpa run --file-path Tests/InitAllSettingsTestCase.xaml
```

A clean analyze is the bar to clear before committing a change to this project.

### Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `feature not available` on validate, build or run | A Studio licence must be assigned to the signed-in user on the active organization. |
| Workflow compiler cannot be found | .NET SDK 8.0 must be on `PATH` — the compiler requires it by name. A newer SDK may sit alongside it. |
| `WorkflowRunnerService does not exist` after the first `uip rpa run` | Clear `.local/.codedworkflows`, `.local/.jit` and `.local/install` before each CLI run. Studio itself is unaffected. |
| `400 — A folder is required for this action. Error code: 1101` | A queue activity ran with no Orchestrator folder in scope. Reads like an auth failure; it is not. |
| `Error code: 1002` | The named queue does not exist in that folder. Check `OrchestratorQueueName` and `OrchestratorQueueFolder` in `Config.json`. |

---

## Publishing

- **As a process:** Studio *Publish*, or `uip rpa pack . <output-dir>` and upload the `.nupkg`. The
  package becomes a process in the target folder.
- **In a solution:** create the project with *Create in solution* (or add it to an existing solution
  with `uip solution projects add <path>`), then publish the solution from Studio or with
  `uip solution pack` / `publish` / `deploy`. The transaction queue is not declared as a solution
  resource; create it in Orchestrator, or add it to the solution with `uip solution resources add`.

Run `uip <group> --help` for the current form of any command.
