# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UiPath Test Automation Framework — a NuGet package template (`UiPath.Template.TestAutomationFramework`) that ships four project variants for UiPath Studio testing projects. The package provides scaffolding for test automation with exception handling, video recording, and multi-browser support.

## Build & Package

```bash
# Pack the NuGet template package
nuget pack UiPath.Template.TestAutomationFramework.nuspec -OutputDirectory ./output
```

There is no compile step or test runner in this repo — the `.xaml` and `.cs` files are consumed as UiPath Studio templates at install time.

## Architecture

### Four Project Variants

The `contentFiles/any/any/` directory contains four independent variants:

| Directory | Language | Target |
|-----------|----------|--------|
| `pt0/VisualBasic/` | VB | Windows |
| `pt1/CSharp/` | C# | Windows |
| `pt2/VisualBasic/` | VB | Cross-platform (Portable) |
| `pt3/CSharp/` | C# | Cross-platform (Portable) |

Each variant is self-contained with its own `project.json`, workflows, and tests. Changes to shared logic must be replicated across all four variants.

**Key differences between variants:**
- pt0/pt1 (Windows): Support both `App` and `Web` test types
- pt2/pt3 (Portable): Support `Web` test type only (no Application workflows)
- pt0: Uses coded workflows (.cs) for video recording; pt1/pt2/pt3 use XAML
- pt0: Has `.json` metadata files per workflow and coded workflow entry points in `project.json`

### Test Execution Lifecycle

Every test follows a strict flow orchestrated by `.templates/TestFramework.xaml`:

```
FrameworkSetup → SetUp → RunTest (with TimeOut) → TearDown → VideoRecording Stop (Finally)
```

- **SetUp/TearDown** dispatch based on `TestType` argument: `App` routes to `StartApplication`/`StopApplication`, `Web` routes to `StartBrowser`/`StopBrowser`
- Each phase is wrapped in its own `TryCatch`; TearDown always executes
- Video recording (ffmpeg-based) stops in the `Finally` block
- SetUp catch block runs TearDown before failing (cleanup guarantee)
- `VerifyExpression` with `TakeScreenshotInCaseOfFailingAssertion=True` for visual evidence
- `ContinueOnFailure` strategy: SetUp catch allows TearDown to run; RunTest catch continues to TearDown; TearDown catch stops immediately
- `Placeholder` activity in RunTest is replaced at build time with the actual test case
- `TimeoutScope` wraps the Placeholder with configurable timeout from `TestSetup("TestExecTimeOut")`

### Global State

- `TestSetup` dictionary — test configuration (TestType, Browser, TestName, etc.)
- `Assets` dictionary — Orchestrator assets loaded from `Data/Assets.json`

## Conventions

### Logging

All log messages must follow: `"WorkflowName - Description"`

- Use `Info` for normal flow, `Warn` for TODOs/non-critical issues, `Error` for exceptions
- Never use `Fatal` for placeholder/TODO messages
- Always specify a log level; use consistent syntax: `Level="Info"`

### Naming

- Workflow files: **PascalCase** (`StartApplication.xaml`)
- Variables: **camelCase** (`videoFilePath`)
- Arguments: **PascalCase** (`TestType`, `Browser`)
- Coded workflow arguments: `in_` prefix for inputs, `out_` prefix for outputs

### Coded Workflows

Coded workflows (.cs) extend `CodedWorkflow` base class with `[Workflow]` attribute on `Execute` method. Use tuple returns for multiple outputs. Log via `Log()` and attach test artifacts via `testing.AttachDocument()`. Follow the same `"WorkflowName - Description"` logging pattern as XAML workflows. See `AGENTS.md` for the full coded workflow conventions.

### Test Cases

Follow **Given-When-Then** BDD pattern. New tests go in `Tests/` and must be registered in `project.json` under `fileInfoCollection` with `executionTemplatePath` set to `.templates\TestFramework.xaml`.

### Annotations

All workflow main sequences must have an annotation describing: what it does, what to customize, and examples of typical customizations.

### Assets.json

```json
[{"Name": "FriendlyName", "Asset": "OrchestratorAssetName", "OrchestratorAssetFolder": ""}]
```

`Name` is the dictionary key; `Asset` is the Orchestrator asset name; `OrchestratorAssetFolder` is optional.

## XAML Editing Notes

- `System.Dnostics` (truncated `System.Diagnostics`) in namespace/assembly references is a known UiPath Studio serialization artifact — do not manually "fix" these
- When renaming `x:Class`, ensure the class name matches the file name and all DisplayNames referencing it
- DisplayNames on `InvokeWorkflowFile` activities should match the actual `WorkflowFileName` path
- Global variables are defined in `.project/globalVariables.json`: use `Constant: true` for immutable config, `false` for runtime state
