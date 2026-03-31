# Test Automation Framework

A UiPath Studio template for test automation projects. Provides a structured execution lifecycle with built-in exception handling, multi-browser support, video recording, and Orchestrator asset management.

## Features

- **Structured test lifecycle** with guaranteed SetUp/TearDown execution
- **Multi-browser support** — Chrome, Firefox, Edge with automatic fallback
- **Video recording** — ffmpeg-based desktop capture attached as test evidence
- **Orchestrator asset integration** — JSON-configured asset loading
- **BDD test structure** — Given/When/Then pattern for all test cases
- **Execution context detection** — automatically detects Studio vs Orchestrator runs
- **Timeout protection** — configurable per-test execution timeout
- **Screenshot on failure** — automatic screenshots when assertions fail

## Test Execution Lifecycle

Every test follows a strict, guaranteed execution flow:

```
FrameworkSetup
  |-- Load assets from Data/Assets.json
  |-- Detect execution source (Studio or Orchestrator)
  |-- Configure test variables (TestType, Browser, Timeout, Recording)
  |
StartRecording (if enabled)
  |
SetUp
  |-- App: Launch application under test
  |-- Web: Configure and start browser
  |
RunTest (with configurable timeout)
  |-- [Your test case runs here via Placeholder]
  |
TearDown (always executes, even on failure)
  |-- App: Close application
  |-- Web: Close browser (with force-kill fallback)
  |
StopRecording (always executes in Finally block)
  |-- Attach video to test case
```

Each phase is wrapped in its own TryCatch. If SetUp fails, TearDown still runs. If recording is active, StopRecording always executes in the Finally block.

## Test Arguments

These arguments are configured on each test case and passed to the execution template:

| Argument | Type | Values | Default | Description |
|----------|------|--------|---------|-------------|
| `TestType` | String | `App`, `Web` | `Web` | Routes SetUp/TearDown to application or browser handlers |
| `Browser` | String | `Chrome`, `Firefox`, `Edge` | `Chrome` | Browser to use for web tests. Falls back to system default if unrecognized |
| `TestExecTimeOut` | String | TimeSpan format | `00:20:00` | Maximum execution time for the test case (20 minutes default) |
| `Recording` | String | `True`, `False` | `False` | Enable ffmpeg desktop recording. Video is attached to test results |

### Setting Arguments in Test Cases

Arguments are set as default values on each test case file. For example, `TestCaseWeb.xaml` declares:

```
TestType = "Web"
Browser = "Chrome"
```

These flow through the execution template (`TestFramework.xaml`) and control the entire lifecycle.

## Project Variants

The template ships four variants to cover different expression languages and target frameworks:

| Variant | Language | Target | Test Types | Use Case |
|---------|----------|--------|------------|----------|
| pt0 | VisualBasic | Windows | App + Web | Desktop and web testing on Windows |
| pt1 | C# | Windows | App + Web | Desktop and web testing on Windows (C#) |
| pt2 | VisualBasic | Portable | Web only | Cross-platform web testing |
| pt3 | C# | Portable | Web only | Cross-platform web testing (C#) |

**Windows variants** (pt0/pt1) include `Application/StartApplication.xaml` and `StopApplication.xaml` for desktop app testing. **Portable variants** (pt2/pt3) support web testing only.

## Project Structure

```
.templates/
  TestFramework.xaml           # Execution template (orchestrates the lifecycle)
  TestCaseAppTemplate.xaml     # Template for new desktop app tests
  TestCaseWebTemplate.xaml     # Template for new web tests

TestFramework/
  SetUp.xaml                   # Routes to App or Web setup
  TearDown.xaml                # Routes to App or Web teardown
  Application/                 # (Windows variants only)
    StartApplication.xaml      # Launch the application under test
    StopApplication.xaml       # Close the application
  Browser/
    StartBrowser.xaml          # Configure and launch browser
    StopBrowser.xaml           # Close browser with force-kill fallback
  Utils/
    DetectLocalBuild.xaml      # Detect Studio vs Orchestrator execution
    InitAllAssets.xaml          # Load assets from JSON into dictionary
  VideoRecording/
    StartRecording.cs          # Start ffmpeg desktop capture
    StopRecording.cs           # Stop recording and attach to test case

Tests/
  TestCaseApp.xaml             # Example desktop app test (Windows only)
  TestCaseWeb.xaml             # Example web test

Data/
  Assets.json                  # Orchestrator asset definitions
```

## Asset Configuration

Assets are defined in `Data/Assets.json` and loaded into a shared dictionary during FrameworkSetup:

```json
[
  {
    "Name": "MyCredential",
    "Asset": "OrchestratorAssetName",
    "OrchestratorAssetFolder": "Shared",
    "Description": "Login credentials for the application"
  }
]
```

| Field | Required | Description |
|-------|----------|-------------|
| `Name` | Yes | Dictionary key to access the asset in workflows |
| `Asset` | Yes | Asset name in UiPath Orchestrator |
| `OrchestratorAssetFolder` | No | Orchestrator folder path (empty for default) |
| `Description` | No | Documentation only, not used at runtime |

Access assets in workflows via: `Assets("MyCredential")`

## Video Recording

Video recording captures the desktop during test execution using ffmpeg.

- **Format**: WebM (VP8 codec, 4 FPS, 71% scale)
- **Storage**: System temp folder as `{TestName}_{GUID}.webm`
- **ffmpeg location**: Auto-detected from UiPath Studio installation (per-machine or per-user)
- **Attachment**: Video is automatically attached to the test case via `testing.AttachDocument()`

Enable by setting `Recording = "True"` on the test case.

## Adding a New Test Case

1. In UiPath Studio, right-click `Tests/` and create a new test case from the `TestCaseWebTemplate` or `TestCaseAppTemplate`
2. Verify the **Execution Template** is set to `.templates\TestFramework.xaml` — this is configured in the test case properties under `executionTemplatePath`. Without this, the test lifecycle (SetUp, TearDown, recording, timeout) will not execute
3. Set the `TestType` argument (`App` or `Web`) and optionally `Browser`
4. Implement your test logic in the **Given**, **When**, **Then** sections:
   - **Given** — Set up preconditions (login, navigate, prepare test data)
   - **When** — Execute the steps to reproduce (the actual test actions)
   - **Then** — Verify results and assert pass/fail criteria
5. The test is automatically registered in `project.json` under `fileInfoCollection`

## Global Variables

| Variable | Type | Constant | Value | Purpose |
|----------|------|----------|-------|---------|
| `TestTimeOut` | String | Yes | `"00:20:00"` | Default test timeout (20 minutes) |
| `TimeOutMessage` | String | Yes | `"Time out exceeded"` | Timeout error message |
| `TestSetup` | Dictionary(String, Object) | No | — | Runtime test configuration |
| `Assets` | Dictionary(String, Object) | No | — | Orchestrator assets loaded from JSON |

## Dependencies

| Package | Version |
|---------|---------|
| UiPath.System.Activities | 26.2.1 |
| UiPath.Testing.Activities | 25.10.1 |
| UiPath.UIAutomation.Activities | 25.10.28 |

Requires UiPath Studio 23.10.4 or later.

## Documentation

- [UiPath Test Cloud Documentation](https://docs.uipath.com/test-cloud/)
