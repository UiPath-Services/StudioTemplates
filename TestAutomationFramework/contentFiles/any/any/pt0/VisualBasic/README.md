# Test Automation Framework (VisualBasic)

A UiPath test project template. Every test case runs inside one execution template (`.templates\TestExecutionTemplate.xaml`) that loads configuration, applies time limits, runs the SetUp and TearDown hooks and records failures.

## Run the sample

1. Configure the entries in `Config\Assets.json`, or remove the example entries before running. To try the sample without Orchestrator assets, use an empty array (`[]`).
2. Open the project in Studio Desktop and select `Tests\SampleTestCase.xaml` in Test Explorer.
3. Ensure `.templates\TestExecutionTemplate.xaml` is selected as the test's execution template, then run the test from Test Explorer.

Running the workflow directly with a bare CLI Run command bypasses the execution template, so configuration initialization and the setup/teardown hooks do not run.

## Execution template flow

1. `Framework\InitializeConfig.cs` loads the Config files into the `Config` global variable.
2. `TestName` (the running test case) is added to Config from the current job.
3. The run configuration (TestName, TestTimeout) is logged.
4. Inside a Timeout Scope of `TestTimeout`: `Hooks\SetUp.xaml`, then the test case.
5. Catch: a Verify Expression (False) records the exception and requests a screenshot when supported by the runtime environment, `Framework\FinalizeTestRun.xaml` runs with the exception, then the exception is rethrown.
6. Finally: `FinalizeTestRun` runs with `Nothing` (reached when the test did not throw).
7. `FinalizeTestRun` runs `Hooks\TearDown.xaml` within `TearDownTimeout`. A TearDown failure is logged and never fails the test.

## Config files

All entries end up in one dictionary, keyed by `Name` (names must be unique across the three files). Settings and Constants contain values, which are logged during initialization. Assets.json contains asset references; asset values are not logged by the initializer. Store secrets in Orchestrator Credential assets, never in Settings or Constants.

| File | Entry format |
|------|--------------|
| `Config\Settings.json`, `Config\Constants.json` | `{ "Name", "Value", "Description" }`. `Value` is text and may be empty. |
| `Config\Assets.json` | `{ "Name", "AssetName", "Folder", "Type", "Description" }`. `Type` is `Asset` (default) or `Credential`. An empty `Folder` means the job's folder. |

`TestTimeout` (required) and `TearDownTimeout` (optional) are settings in `hh:mm:ss`, stored as `TimeSpan`. `TestName` is reserved.

### Examples (all start with `example_`)

**Every `example_` entry is a placeholder. Remove it from, or replace it in, a real project.**

| Entry | File | Shows | Read it with |
|-------|------|-------|--------------|
| `example_ApplicationUrl`, `example_Environment` | Settings.json | a text setting | `Config("example_ApplicationUrl").ToString` |
| `example_DateFormat`, `example_MaxRetryCount` | Constants.json | a constant (numbers are text) | `Config("example_DateFormat").ToString`, `CInt(Config("example_MaxRetryCount"))` |
| `example_ApiEndpoint` | Assets.json, `Type` Asset | a text or value asset, returned as Orchestrator returns it | `Config("example_ApiEndpoint").ToString` |
| `example_ApplicationCredential` | Assets.json, `Type` Credential | a credential asset | `CType(Config("example_ApplicationCredential"), System.Net.NetworkCredential)`, then `.UserName` and `.SecurePassword` |

All assets are loaded when the test starts. The two example assets do not exist in any Orchestrator, so a project that still has them fails at `InitializeConfig` (the error names the entry, the asset, the folder and the expected type). Either delete them from `Assets.json` or create assets with those names (a Text asset and a Credential asset) in the job's folder.

Initialization stops with a message naming the file, the entry and the allowed values when a file is missing or is not a JSON array, an entry is malformed, a `Type` is not `Asset` or `Credential`, or a timeout is not `hh:mm:ss`. Secret-type Orchestrator assets are not supported. Use Credential assets for secrets and Text assets for non-sensitive values.

## Reading config

`Config("Name")` in a VB expression, for example `Config("TestTimeout")`. Values are objects: convert as needed (`CType(Config("TestTimeout"), TimeSpan)`).

## Screenshots

- Failure: the template's Catch requests a screenshot. Availability depends on the runtime environment and screenshot support.
- Evidence of a success: add a Verify Expression that checks a True condition with "Take screenshot in case of succeeding assertion" enabled.

## Hooks

- `Hooks\SetUp.xaml` runs before every test, inside `TestTimeout`. A failure fails the test, requests a screenshot where supported, and still runs TearDown.
- `Hooks\TearDown.xaml` runs after every test. `in_Exception` is `Nothing` when the test ran to the end; a failed Verify that continues on failure is not an exception.
