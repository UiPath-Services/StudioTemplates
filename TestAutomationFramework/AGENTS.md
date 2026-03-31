# Test Automation Framework — Developer Guide

## Project Overview

The **Test Automation Framework** is a UiPath testing template designed for testing projects. It extends the main capabilities of a test automation process by leveraging exception handling and testing best practices.

- **Expression Language:** VisualBasic
- **Target Framework:** Windows
- **Output Type:** Tests
- **Key Dependencies:** UiPath.System.Activities, UiPath.Testing.Activities, UiPath.UIAutomation.Activities

---

## Project Structure

```
├── .templates/
│   └── TestFramework.xaml          # Main execution template (SetUp → RunTest → TearDown)
├── Data/
│   └── Assets.json                 # Orchestrator asset definitions
├── TestFramework/
│   ├── Application/
│   │   ├── StartApplication.xaml   # Launch the Application Under Test (AUT)
│   │   └── StopApplication.xaml    # Close the AUT gracefully
│   ├── Browser/
│   │   ├── StartBrowser.xaml       # Configure and launch browser for web tests
│   │   └── StopBrowser.xaml        # Close browser (with force-kill fallback)
│   ├── Utils/
│   │   ├── DetectLocalBuild.xaml   # Detect if running from Studio or Orchestrator
│   │   └── InitAllAssets.xaml      # Load assets from JSON into a dictionary
│   ├── VideoRecording/
│   │   ├── StartRecording.cs       # Start ffmpeg video recording (coded workflow)
│   │   └── StopRecording.cs        # Stop ffmpeg video recording (coded workflow)
│   ├── SetUp.xaml                  # Test setup dispatcher (routes to App or Web setup)
│   └── TearDown.xaml               # Test teardown dispatcher (routes to App or Web teardown)
├── Tests/
│   ├── TestCaseApp.xaml            # Example test case for desktop app testing
│   └── TestCaseWeb.xaml            # Example test case for web testing
├── WorkFlows/
│   └── (reusable workflows go here)
└── project.json
```

---

## Test Execution Flow

The framework follows a strict lifecycle for every test execution:

```
FrameworkSetup → SetUp → RunTest (with TimeOut) → TearDown → VideoRecording Stop
```

1. **FrameworkSetup** — Loads assets, detects execution source, configures test variables
2. **SetUp** — Launches the application or browser based on `TestType` (App/Web)
3. **RunTest** — Executes the actual test case (injected via Placeholder activity)
4. **TearDown** — Closes the application or browser, cleans up
5. **VideoRecording** — Stops recording in the Finally block (always executes)

Each phase is wrapped in a `TryCatch` block for resilience.

---

## Logging Conventions

### Pattern
All log messages MUST follow this pattern:

```
"WorkflowName - Description"
```

**Examples:**
- `"StartApplication - Start"`
- `"StartBrowser - Using Chrome browser"`
- `"TearDown - End"`
- `"InitAllAssets - Asset and Name information is required to create the Assets dictionary"`

### Log Levels

| Level    | When to Use                                                    |
|----------|----------------------------------------------------------------|
| `Info`   | Normal flow: phase start/end, informational messages           |
| `Warn`   | Warning conditions, TODO placeholders, non-critical issues     |
| `Error`  | Exceptions caught in TryCatch blocks, failures                 |
| `Trace`  | Detailed debugging information (use sparingly)                 |

### Rules
- **Always prefix** messages with the workflow name for easy log filtering
- **Never use `Fatal`** for placeholder/TODO messages — use `Warn` instead
- **No leading or trailing spaces** in log messages
- **Use consistent level syntax:** `Level="Info"` (not `Level="[UiPath.Core.Activities.LogLevel.Info]"`)
- **Always specify a log level** — do not leave it blank
- **TODO placeholders** should follow: `"WorkflowName - TODO: Description"`

---

## Test Case Conventions

### Given-When-Then Structure
Test cases follow the **Given-When-Then** pattern:

- **Given** — Pre-conditions and test data setup
- **When** — Steps to reproduce (actual test actions)
- **Then** — Verify output, assert results, determine PASS/FAIL

### Test Types
The framework supports two test types via the `TestType` argument:

| TestType | SetUp Action         | TearDown Action      |
|----------|---------------------|---------------------|
| `App`    | StartApplication    | StopApplication     |
| `Web`    | StartBrowser        | StopBrowser         |

If `TestType` is not set, a `BusinessRuleException` is thrown.

### Browser Configuration
- Supported browsers: `Chrome`, `Firefox`, `Edge`
- Default: `Chrome` (if no browser is specified)
- Browser is configurable via the `Browser` argument on `TestFramework.xaml`

---

## Annotation Conventions

All workflow main sequences MUST have an annotation that describes:
1. **What the workflow does** — A brief summary
2. **What the user should customize** — Clear instructions for extending
3. **Examples** — Bullet points of typical customizations

---

## Naming Conventions

### Workflow Files
- Use **PascalCase** for workflow file names: `StartApplication.xaml`, `DetectLocalBuild.xaml`
- Place workflows in the appropriate subdirectory under `TestFramework/`

### Variables
- Use **camelCase** for local variables: `videoFilePath`, `ffmpegProcess`
- Use **PascalCase** for arguments: `TestType`, `Browser`, `TestExecTimeOut`

### DisplayNames
- Use descriptive DisplayNames that explain the activity's purpose
- For Log Messages: `"Log message for [context]"` or `"[WorkflowName] [Phase]"`

---

## Configuration & Assets

### Assets.json Format
Assets are defined in `Data/Assets.json` with the following structure:

```json
[
  {
    "Name": "FriendlyName",
    "Asset": "OrchestratorAssetName",
    "OrchestratorAssetFolder": ""
  }
]
```

- `Name` — The key used to access the asset in the `Assets` dictionary
- `Asset` — The asset name in Orchestrator
- `OrchestratorAssetFolder` — Optional folder path in Orchestrator (leave empty for default)

### Global Variables
The framework uses shared dictionaries accessible across workflows:
- `TestSetup` — Dictionary containing test configuration (TestType, Browser, TestName, etc.)
- `Assets` — Dictionary containing Orchestrator assets loaded from Assets.json

---

## Error Handling Best Practices

1. **Always wrap phases in TryCatch** — SetUp, RunTest, and TearDown each have their own TryCatch
2. **Use VerifyExpression for test assertions** — Includes screenshots on failure
3. **Log exceptions at Error level** — Include exception message and source
4. **TearDown runs even on failure** — Ensures cleanup always happens
5. **Video recording stops in Finally block** — Guarantees recording is saved

---

## Adding New Test Cases

1. Create a new `.xaml` file in the `Tests/` directory
2. Follow the **Given-When-Then** structure
3. Register it as a test case in `project.json` under `fileInfoCollection`
4. Set the `executionTemplatePath` to `.templates\TestFramework.xaml`
5. Add log messages following the standardized pattern

---

## Video Recording

- Recording is controlled by the `Recording` argument on `TestFramework.xaml`
- Videos are saved as `.webm` files in the system temp folder with format `{TestName}_{Guid}.webm`
- Recording starts before SetUp and stops in the Finally block (always executes)
- ffmpeg path is resolved in two stages: per-machine (`%ProgramFiles%\UiPath\Studio\ffmpeg\ffmpeg.exe`), then per-user (`%LocalAppData%\Programs\UiPath\Studio\ffmpeg\ffmpeg.exe`)
- Capture settings: gdigrab desktop capture, 4 FPS, 71% scale, VP8 codec, CRF 50, 1M max bitrate
- Graceful stop via stdin "q" command; Kill() as fallback; video attached via `testing.AttachDocument()` in finally block

---

## Coded Workflow Conventions

Coded workflows (`.cs` files) in this project follow these patterns:

### Class Structure
- Extend `CodedWorkflow` base class (from `UiPath.CodedWorkflows`)
- Mark the entry method with `[Workflow]` attribute
- Entry method is always named `Execute`

### Arguments
- Input arguments use `in_` prefix: `in_TestName`, `in_startRecording`
- Output arguments use `out_` prefix: `out_ffmpegProcess`, `out_VideoFilePath`
- Multiple outputs use C# tuple returns: `(Process out_ffmpegProcess, String out_VideoFilePath)`

### Service API
- `Log(message)` and `Log(message, LogLevel)` — injected by CodedWorkflow base
- `testing.AttachDocument(path)` — injected testing service for attaching artifacts
- Log messages must follow the same `"WorkflowName - Description"` pattern as XAML workflows

### Imports
- Only include `using` statements that are actually used
- Core imports: `System`, `System.Diagnostics`, `UiPath.CodedWorkflows`, `UiPath.Core`

---

## Workflow Review Checklist

When reviewing XAML workflows, verify:

- [ ] Log messages follow `"WorkflowName - Description"` pattern
- [ ] Log levels are appropriate (Info for flow, Warn for TODOs, Error for exceptions)
- [ ] No leftover project-specific assembly references (e.g., `SOSR.AppLibrary`, `RPA_T_BA_SOSR_Test.Core`)
- [ ] `x:Class` name matches the file name and DisplayName
- [ ] DisplayNames on InvokeWorkflowFile activities match the actual file path
- [ ] Annotations describe what the workflow does and what to customize
- [ ] TryCatch blocks have appropriate catch/finally logic (no silent exception swallowing)
- [ ] Variable and argument names follow conventions (camelCase/PascalCase)
- [ ] No typos in DisplayNames, annotations, or variable names

When reviewing coded workflows (.cs), verify:

- [ ] Extends `CodedWorkflow` with `[Workflow]` attribute on `Execute` method
- [ ] Arguments use `in_`/`out_` prefix convention
- [ ] No unused `using` statements
- [ ] Log messages follow `"WorkflowName - Description"` pattern
- [ ] Exceptions are logged before being handled (no silent catch blocks)
- [ ] Resources are cleaned up in finally blocks
