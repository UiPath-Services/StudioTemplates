# Robotic Enterprise Framework (VisualBasic, Portable)

This guide covers the UiPath RPA project one folder up (`project.json` at the project root), created
from the Robotic Enterprise Framework template. Build, validate and run it with Studio or the `uip
rpa` CLI.

This guide is kept in `Framework/` because Studio replaces the project-root `AGENTS.md` and
`CLAUDE.md` with its own generic files when it creates a project. Paths below are relative to the
project root.

**If you are an agent asked to build or change a process in this project, follow [Building a
process](#building-a-process) in order, and respect [Rules](#rules).** The rest of the file is
reference material for those steps.

| | |
|---|---|
| Expression language | **VisualBasic**, fixed at project creation, applies to every workflow |
| Target framework | **Portable**, runs on Windows, macOS and Linux |
| Configuration | `Data/Config.json` |
| Transaction source | Orchestrator queue by default; any other source can replace it |
| Licence | MIT |

Prose documentation ships at `Documentation/`. **Its configuration and queue sections are out of
date**: they describe Studio Global Constants and a solution queue resource, neither of which this
project uses. Where it and this file disagree, this file is correct.

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
- Let every other exception propagate. The framework classifies it as a system exception, retries
  the transaction if retries are configured, and re-initialises the applications.

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
project.json                     project definition; the entry point is Main.xaml
Main.xaml                        the state machine
Data/Config.json                 configuration: Settings + Constants
Framework/                       the framework workflows
Tests/                           test cases, plus Tests.xlsx
Documentation/                   reference PDF
```

### Configuration

`Data/Config.json` has two objects: **Settings** (values that change per environment) and
**Constants** (values that rarely change). `Framework/InitAllSettings.xaml` reads both (argument
`in_ConfigSections`) into one `Config` dictionary during the Initialization state. Every framework
workflow except `KillAllProcesses` and `CloseAllApplications` receives it as the `in_Config`
argument. Read a value with `CInt(in_Config("MaxRetryNumber"))` or
`in_Config("logF_BusinessProcessName").ToString`. To add a tunable value, add a key to the Settings
or Constants object.

| Name | Default | Meaning |
|---|---|---|
| `logF_BusinessProcessName` | `Framework` | Groups the logs of related processes under one business process name. |
| `MaxRetryNumber` | `0` | In-process retries after a system exception. `0` with a queue. |
| `MaxConsecutiveSystemExceptions` | `0` | Stops the job after this many system exceptions in a row. `0` disables it. |
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
| Process Transaction | Process one transaction and record the outcome: Success, Business Exception or System Exception. | `Process`, `SetTransactionStatus` (which may invoke `RetryCurrentTransaction`, `CloseAllApplications`, `KillAllProcesses`) |
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
uip rpa analyze .                           # validate + workflow analyzer
uip rpa run --file-path Tests/InitAllSettingsTestCase.xaml
```

### Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `The <path> workflow cannot be found` on an Invoke Workflow File | The path is not relative to the project root, or the project was opened one folder too high. |
| `feature not available` on validate, build or run | A Studio licence must be assigned to the signed-in user on the active organization. |
| `400 - A folder is required for this action. Error code: 1101` | A queue activity ran with no Orchestrator folder in scope. |
| `Error code: 1002` | The named queue does not exist in that folder. |
| Workflow compiler cannot be found | .NET SDK 8.0 must be on `PATH`; the compiler requires it by name. |
| `WorkflowRunnerService does not exist` after the first `uip rpa run` | Clear `.local/.codedworkflows`, `.local/.jit` and `.local/install` before each CLI run. Studio is unaffected. |
| CS1705 about `System.Runtime` 10.0.0.0 vs 8.0.0.0 when compiling `CodedWorkflows` | The project targets .NET 8 (Minimum Robot version 24.10) while Studio runs on .NET 10. Set Minimum Robot version to 26.10 in Project Settings (or in the New Project dialog), close the project, delete `.local` and reopen. The project then needs Robot 26.10 or newer, which rules out older robots and, for now, serverless. |

---

## Publishing

- **As a process:** Studio *Publish*, or `uip rpa pack . <output-dir>` and upload the `.nupkg`. The
  package becomes a process in the target folder.
- **In a solution:** create the project with *Create in solution* (or add it to an existing solution
  with `uip solution projects add <path>`), then publish the solution from Studio or with
  `uip solution pack` / `publish` / `deploy`. The transaction queue is not declared as a solution
  resource; create it in Orchestrator, or add it to the solution with `uip solution resources add`.

Run `uip <group> --help` for the current form of any command.
