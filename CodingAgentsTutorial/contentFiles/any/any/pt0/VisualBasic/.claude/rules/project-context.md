<!-- discovery-metadata: cs=0 xaml=5 deps=4 -->
# Project context

UiPath Process project used as course material. Rules are in `AGENTS.md`.
Curriculum is in `README.md`, which Studio opens automatically; it is the landing page and the whole course.

## Shape

- Process. `targetFramework: Portable`, `expressionLanguage: VisualBasic`,
  `isTemplate: true`.
- Entry point `Main.xaml`. XAML only, no coded workflows.
- Dependencies: `UiPath.System.Activities`, `UiPath.Excel.Activities`,
  `UiPath.Testing.Activities`, `UiPath.UIAutomation.Activities`.

Cross-platform, so the `*X` Excel activities and `BuildDataTable` do not load.
Excel uses `UiPath.Excel.Activities.ReadRange` / `WriteRange` (`ui:` prefix),
which need no Excel install. Tables are built with `GenerateDataTable` from a
header line.

## Files

| Path | Purpose |
|---|---|
| `Main.xaml` | Reads claims, validates each, writes the summary. |
| `Workflows/ReadExpenses.xaml` | `Data/expenses.xlsx` to DataTable. |
| `Workflows/ValidateExpense.xaml` | One claim against the receipt and notes rules. |
| `Workflows/WriteSummary.xaml` | Results to `Data/summary.xlsx`. |
| `Tests/ValidateExpense_Tests.xaml` | Test case, registered in `designOptions.fileInfoCollection`. |
| `assets/expenses.html` | Practice portal. Element ids in its header comment. |
| `Data/expenses.xlsx` | Six claims, sheet `Expenses`. |
| `specs/step-03-pdd.md` | Step 3 PDD. |
| `README.md` | The course. Never edit. |
| `course/SETUP.md` | How the learner gets an agent. |
| `course/PROGRESS.md` | Agent-written log, one row per step. |
| `course/agent/PROCEDURE.md` | How the agent runs a step. Pointed to from `AGENTS.md`. |

`Data/summary.xlsx` is generated output, rewritten by every run. Never staged.

## Conventions

- DataTable variables `dt_`; arguments `in_dt_` / `out_dt_` (ST-NMG-009,
  ST-NMG-011).
- Argument names match `^(in|out|io)_(dt_)?[A-Za-z]+[0-9]*$` (ST-NMG-002).
- Unique display names within a workflow (ST-NMG-004).
- Every container body wrapped in a `Sequence`.
- Data and asset paths use forward slashes. `WorkflowFileName` on Invoke
  Workflow File uses backslashes (`Workflows\ValidateExpense.xaml`), which is
  what Studio emits and resolves on both platforms.
- Test assertions set `ContinueOnFailure="False"`. With the default `True`, a
  failing assertion still returns `Success` / exit 0 from `uip rpa run`. Verified
  both ways.
- `InvokeWorkflowFile.Arguments` takes direct child arguments, no
  `scg:Dictionary` wrapper. The wrapper is cleared on load.

## Gotchas found here

- `VerifyExpressionWithOperator.FirstExpression` / `SecondExpression` are
  `InArgument<Object>`. Use property elements typed `x:Object` with `[bracket]`
  expressions. A bare literal passes `validate` and `build`, then fails at
  runtime: "Literal only supports value types and the immutable type
  System.String." `LogMessage.Message` accepts a bare literal; this does not.
- UIAutomation is unused until course step 3, so the analyzer reports ST-USG-010.
- The analyzer reports a missing Automation Hub URL (ST-USG-034). Org setting,
  not fixable here.
- One unconfigured UI target fails `validate`, `build` and `run` for the whole
  project, including files that do not use UIA.

## Commands

```bash
uip rpa validate --file-path "<relative path>" --project-dir "<PROJECT_DIR>"
uip rpa build "<PROJECT_DIR>"
uip rpa run --file-path "Main.xaml" --project-dir "<PROJECT_DIR>"
uip rpa run --file-path "Tests/ValidateExpense_Tests.xaml" --project-dir "<PROJECT_DIR>"
```

A `Windows` target-framework project cannot be validated, built or run on macOS
or Linux. That is one reason this project is `Portable`.

## Packaging

Delete `.local/` before sharing this folder. `uip` and Studio regenerate it on
every run, and it contains absolute paths from whoever built last. It is
not tracked, so a git share is clean; a folder copy or zip is not.

```bash
rm -rf ".../Coding Agents Tutorial/.local"
find ".../Coding Agents Tutorial" -name '.DS_Store' -delete
```

Same for `.objects/`, `.settings/`, `.project/`, `.tmh/`, `.entities/`,
`.templates/` and `Data/summary.xlsx`.

## Adapters

`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/coding-agents-course.mdc` and
`.claude/skills/coding-agents-course/SKILL.md` contain no course content. Each
points at `AGENTS.md` and `course/agent/PROCEDURE.md`. To support another tool,
copy one adapter under that tool's filename; never copy the content.
