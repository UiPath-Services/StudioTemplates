### Robotic Enterprise Framework ###

A cross-platform (Portable) REFramework project. It runs on macOS, Linux and Windows, and is
delivered as a UiPath Solution because the transaction queue is declared as a solution resource.

* State Machine layout for the phases of the automation
* High-level logging, exception handling and recovery
* Tunable values live as **project Global Constants**
* The transaction queue is a **solution resource**
* Credentials come from Orchestrator assets
* Gets transaction data from an Orchestrator queue and writes the status back
* Takes a screenshot when a transaction fails with a system exception

Full reference documentation is in the **Documentation** folder.


### How It Works ###

1. **INITIALIZE PROCESS**
 + Global Constants supply every tunable value; nothing is read from a configuration file
 + ./Framework/*KillAllProcesses* - Force-closes anything left running by a previous execution
 + ./Framework/*InitAllApplications* - Opens and logs in to the applications the process uses

2. **GET TRANSACTION DATA**
 + ./Framework/*GetTransactionData* - Fetches the next transaction from the queue named by the `TransactionQueue` solution resource. Returning nothing ends the process

3. **PROCESS TRANSACTION**
 + *Process* - Your business logic; runs once per transaction
 + ./Framework/*SetTransactionStatus* - Records the outcome: Success, Business Rule Exception or System Exception
 + ./Framework/*RetryCurrentTransaction* - Decides whether a system exception is retried
 + ./Framework/*TakeScreenshot* - Invoked on a system exception only

4. **END PROCESS**
 + ./Framework/*CloseAllApplications* - Logs out and closes the applications used


### Configuration ###

Tunable values are **Global Constants**, declared in `.project/globalVariables.json` and edited
through Studio's Data Manager. They are typed and compiled into the project, so every workflow can
use them directly - `MaxRetryNumber`, not a dictionary lookup - and no workflow needs a `Config`
argument.

Store secrets as Orchestrator assets and read them with *Get Asset* / *Get Credential*. Never put
credentials in Global Constants; they are compiled into the package in clear text.


### The Transaction Queue ###

The queue is the solution resource **TransactionQueue**
(`resources/solution_folder/queue/TransactionQueue.json`). The solution owns its identity and
provisions it at deploy time, and *Get Transaction Item* in `GetTransactionData.xaml` refers to it
by that name - rename one and rename the other.

The folder is deliberately left unset so the robot's own Orchestrator folder applies. Deploy the
process into the folder that holds the queue. Queue activities always need a folder in scope; run
one outside a folder and Orchestrator answers
`400 - A folder is required for this action. Error code: 1101`, which reads like an authentication
failure but is not.


### Exception Handling ###

Exceptions fall into two categories, and the category decides whether the transaction is retried.

| Category | Class | Retried? | Meaning |
|---|---|---|---|
| Business Exception | `BusinessRuleException` | No | The data breaks a rule of the process. Retrying changes nothing until a human intervenes, so the transaction is skipped |
| System Exception | any other `Exception` | Yes | A technical fault, often transient. The transaction is retried and the applications are re-initialised between attempts |

Throw `BusinessRuleException` explicitly from `Process.xaml` and let everything else propagate. Do
not wrap `Process.xaml` in a catch-all Try Catch, and do not add a Global Exception Handler - the
framework's own per-state handling is what classifies and routes the exception.

When a queue manages retries, keep `MaxRetryNumber` at 0 and configure the retry count on the queue
in Orchestrator. `MaxConsecutiveSystemExceptions` stops the job once that many system exceptions
occur back to back; 0 disables that guard.


### Exception Screenshots ###

When a transaction fails with a **system exception**, `Framework/SetTransactionStatus.xaml` invokes
`Framework/TakeScreenshot.xaml`, which captures the whole desktop and writes a PNG into the folder
named by the `ExScreenshotsFolderPath` Global Constant (`Exceptions_Screenshots` by default).
Successful transactions and business rule exceptions produce no screenshot.

The file name is the path passed in with a timestamp inserted before the extension, for example
`Exceptions_Screenshots/ExceptionScreenshot_2026-08-28_112451_186.png`. The coded workflow returns
the path it actually wrote; `TakeScreenshot.xaml` assigns that back to `io_FilePath` and logs
`Screenshot saved at: <path>`, and `SetTransactionStatus.xaml` puts the same path into the queue
item's `Details` field.


### Logging ###

The framework logs transaction statuses, exceptions and state transitions. The static parts of
those messages are the `LogMessage_*` Global Constants below.

Custom log fields are added with *Add Log Fields* and removed immediately afterwards with
*Remove Log Fields*, so a field applies only to the intended message. The fields are
`logF_TransactionID`, `logF_TransactionField1`, `logF_TransactionField2`, `logF_TransactionNumber`
and `logF_TransactionStatus`, plus `LogF_BusinessProcessName`, added once at start-up to group the
logs of related sub-processes. They are useful for reporting - in an invoice automation, the invoice
number, date and total map neatly onto the transaction ID and the two spare fields.

Never log sensitive data; logs are not encrypted.


### For a New Project ###

1. Set the Global Constants in Studio's Data Manager - at minimum `LogF_BusinessProcessName`, which
   is stamped on every log message the framework emits
2. Point the `TransactionQueue` resource at your queue, or replace *Get Transaction Item* in
   `GetTransactionData.xaml` if the source is not a queue
3. Implement `InitAllApplications.xaml`, `CloseAllApplications.xaml` and `KillAllProcesses.xaml`
   for the applications your process drives
4. Implement `Process.xaml`, throwing `BusinessRuleException` for data problems
5. If you change the type of the `TransactionItem` variable in `Main.xaml` - to `DataRow` for
   spreadsheet rows, for example - change it in `GetTransactionData.xaml`, `Process.xaml` and
   `SetTransactionStatus.xaml` too, then use *Import Arguments* on each Invoke Workflow File
6. Keep `MaxRetryNumber` at 0 while developing so failures surface immediately


### Test Framework ###

`Tests/MainTestCase.xaml` runs every workflow listed on the **Tests** sheet of `Tests/Tests.xlsx`,
classifies each outcome as Success, BusinessRuleException or SystemException, writes the Status
(PASS/FAIL) and Comments back to the **Result** sheet, and asserts that no row failed. Only
workflows that take no arguments can be listed, because the loop invokes them without passing any.

`GetTransactionDataTestCase`, `ProcessTestCase`, `InitAllApplicationsTestCase` and
`WorkflowTestCaseTemplate` are samples to extend for your process. The two that touch the queue need
a reachable Orchestrator queue and folder.

Excel is read and written with the Workbook activities, which use a file-based engine and need no
Excel installation. `Tests/MainTestCase.xaml` is the only Excel consumer in the project.


### Global Constants ###

| Name | Type | Value | Description |
|---|---|---|---|
| `LogF_BusinessProcessName` | `String` | `"REFramework_CrossPlatform"` | Logging field which allows grouping of log data of two or more subprocesses under the same business process name |
| `MaxRetryNumber` | `Int32` | `0` | Must be 0 if working with Orchestrator queues. If > 0, the robot will retry the same transaction which failed with a system exception. Must be an integer value. |
| `MaxConsecutiveSystemExceptions` | `Int32` | `0` | The number of consecutive system exceptions allowed. If MaxConsecutiveSystemExceptions is reached, the job is stopped. To disable this feature, set the value to 0. |
| `ExScreenshotsFolderPath` | `String` | `"Exceptions_Screenshots"` | Where to save exceptions screenshots - can be a full or a relative path. |
| `LogMessage_GetTransactionData` | `String` | `"Processing Transaction Number: "` | Static part of logging message. Calling Get Transaction Data. |
| `LogMessage_GetTransactionDataError` | `String` | `"Error getting transaction data for Transaction Number: "` | Static part of logging message. Error retrieving Transaction Data. |
| `LogMessage_Success` | `String` | `"Transaction Successful."` | Static part of logging message. Processed Transaction succesful. |
| `LogMessage_BusinessRuleException` | `String` | `"Business rule exception."` | Static part of logging message. Processed Transaction failed with business exception. |
| `LogMessage_ApplicationException` | `String` | `"System exception."` | Static part of logging message. Processed Transaction failed with application exception. |
| `ExceptionMessage_ConsecutiveErrors` | `String` | `"The maximum number of consecutive system exceptions was reached. "` | Error message in case MaxConsecutiveSystemExceptions number is reached. |
| `RetryNumberGetTransactionItem` | `Int32` | `2` | The number of times Get Transaction Item activity is retried in case of an exception. Must be an integer >= 1. |
| `RetryNumberSetTransactionStatus` | `Int32` | `2` | The number of times Set transaction status activity is retried in case of an exception. Must be an integer >= 1. |
| `ShouldMarkJobAsFaulted` | `Boolean` | `False` | Must be TRUE or FALSE. If the value is TRUE and an error occurs in Initialization state or the MaxConsecutiveSystemExceptions is reached, the job is marked as Faulted. |

### Prerequisites and Troubleshooting ###

* **.NET SDK 8.0** must be on `PATH` - the workflow compiler requires it by name. A newer SDK may be
  installed alongside it.
* **A Studio licence** on the signed-in organization, otherwise `uip rpa validate` / `build` / `run`
  fail with `HelmFeatureNotAvailableException`.
* **After hand-editing `.project/globalVariables.json`**, delete `.local/.jit` and `.local/install`
  and restart the Studio host, or newly added names resolve as `'<name>' is not declared`. The
  compiled globals assembly is cached per host session and outlives the source change. The same fix
  applies to a `CS1705` about `System.Private.CoreLib` versions.
* **Running from the CLI**, `uip rpa run` writes `.local/.codedworkflows/CodedWorkflow.cs` but not
  the `WorkflowRunnerService` it references, so runs after the first fail with
  *"WorkflowRunnerService does not exist"*. Clear `.local/.codedworkflows`, `.local/.jit` and
  `.local/install` before each CLI run. Studio is unaffected.
* **`Error code: 1002`** on a queue activity means the named queue does not exist in the folder -
  check the queue resource and the deployment folder.

**Dependencies**

`UiPath.Excel.Activities` 3.6.1 · `UiPath.System.Activities` 26.6.3 · `UiPath.Testing.Activities` 25.10.2 · `UiPath.UIAutomation.Activities` 26.10.3
