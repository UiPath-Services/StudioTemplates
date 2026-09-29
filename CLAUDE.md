# StudioTemplates

Each top-level folder is one NuGet package of Studio project templates. CI just runs
`nuget pack <folder>/<Template>.nuspec` — the published version is the `<version>` in the
nuspec, and everything beside the nuspec is swept into the package.

## Template layout

```
contentFiles/any/any/pt{N}/.local/template.json   <- Studio metadata for this variant
contentFiles/any/any/pt{N}/{VisualBasic|CSharp}/  <- the project payload
```

Studio scans `pt0, pt1, …` until a gap, so a new variant is just the next index. There is no
manifest to register it in.

## TargetFramework

`Legacy` = net472, `Windows` = net8.0-windows, `Portable` = cross-platform. The field **filters**
the New Project wizard, it is not a default the user can override: the framework dropdown is built
from the distinct `TargetFramework` values across a package's `pt*` folders, and with only one the
user is locked to it. An absent field deserializes to `Legacy`.

The blank `Main.xaml` for each framework/language is maintained by Studio at
`Studio/UiPath.Studio.Plugin.Workflow.Shared/ProjectTemplates/Blank/{framework}/{language}/`.
Copy from there rather than hand-editing XAML; the Windows/Portable delta is only the
`PresentationFramework`/`WindowsBase`/`PresentationCore` references.

## Conventions worth knowing

- **Background-process templates omit `UiPath.UIAutomation.Activities`.** With
  `RequiresUserInteraction: false` there is no interactive session, so UI automation cannot run.
  Applies to BackgroundProcess, OrchestrationProcess and LongRunningAutomation. Don't "fix" a
  dangling UIAutomation assembly reference by adding the dependency — remove the reference.
- **Legacy variants are pinned to the 24.10 activity line.** 24.10 is the last LTS whose packages
  still ship a `.NETFramework` group; System 25.2.0, Excel 3.0.1, Mail 2.0.10 and WebAPI 2.3.0
  dropped it. Newer pins will not restore on a Legacy project.
- **Cross-platform variants drop Excel and Mail** — the activities that matter need the desktop
  Office apps. Studio's own `Blank/Portable` template does the same.
- **The payload must be a flat project, never a solution.** Studio's New Project wizard creates
  one project whose root is the destination folder: it writes `project.json` there from
  `template.json`, drops any `project.json` nested in the payload, and never opens a `.uipx`.
  A payload shaped as `<name>.uipx` + `<name>/project.json` therefore becomes one project rooted
  one level too high, and every project-relative Invoke Workflow File path breaks. Users get a
  solution by ticking *Create in solution* in the wizard.
- **Studio builds `project.json` from `template.json`, not from the payload.** The payload's
  `project.json` is replaced, so its `runtimeOptions` and `dotNetVersion` never reach the user.
  Set `RequiresUserInteraction` in `template.json` (Studio's own Blank template does); when it is
  absent Studio defaults to `true` (foreground).
- **Set `"DotNetVersion": "Net10"` in every variant's `template.json`, not only the one it is for.**
  The value is the `UiPath.Shared.DotNetVersion` enum (`Net8`, `Net6`, `Net10`); a missing field
  means `Net8`, and Studio then writes no `dotNetVersion` into `project.json`. The New Project
  wizard copies the .NET version from the variant it opens on (the Legacy one first) and keeps it
  when the user switches target framework, so a value set only on the Portable variant is
  overwritten. Studio ignores it for Legacy projects. A .NET 8 Portable project fails on a .NET 10
  Studio with CS1705 while compiling the `CodedWorkflows` helper.
- Release channels are `master/<Template>` branches; work in `feature/<target>/<name>`.
