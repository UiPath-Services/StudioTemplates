param(
    [string] $shouldGetTemplatesFromConfig = $false,

    [string] $templatesConfig = "$PSScriptRoot\templates.config",

    [string] $commitHash,

    [string] $outputDirectory
)

Write-Host "Creating the hashset..."
$set = New-Object System.Collections.Generic.HashSet[string]
Write-Host "Deciding wether to use the templates.config file or check the commit differences"
Write-Host "shouldGetTemplatesFromConfig equals $shouldGetTemplatesFromConfig"
if ($shouldGetTemplatesFromConfig -eq $true) {
    Write-Host "Reading from config file $templatesConfig"
    [xml]$templatesXmlDoc = Get-Content -Path $script:templatesConfig
    Write-Host "Extracting items..."
    $templates = $templatesXmlDoc | Select-Object -ExpandProperty templates | Select-Object -ExpandProperty template

    foreach ($template in $templates) {
        Write-host "Appending $($template.name)"
        $set.Add($template.name) >$null 2>&1  # last part is used to prevent logging the output
    }
} else {
    Write-Host "Build reason is $Env:BUILD_REASON"
    if ($Env:BUILD_REASON -eq "PullRequest") {
        Write-Host "Checking the commit difference for the PR"
        # get changed files from last commit
        $files=$(git diff-tree --no-commit-id --name-only $Env:SYSTEM_PULLREQUEST_TARGETBRANCH $Env:SYSTEM_PULLREQUEST_SOURCEBRANCH)
    } else {
        Write-Host "Checking the commit difference for $commitHash"
        # get changed files from last commit
        $files=$(git diff-tree --no-commit-id --name-only -r $commitHash)
    }

    $list=$files -split ' '
    $count=$list.Length
    Write-Host "Total changed $count files"
    Write-Host $list
    Write-Host "Iterating through the list of modified files"
    for ($i = 0; $i -lt $list.Length; $i++)
    {
        $endOfDirectoryName = $list[$i].IndexOf("/")
        if ($endOfDirectoryName -gt 0) {
            Write-Host "Getting the root path..."
            $targetPackage = $list[$i].Substring(0, $endOfDirectoryName)
            Write-Host "Appending $targetPackage to hashset..."
            $set.Add($targetPackage) >$null 2>&1  # last part is used to prevent logging the output
        }
    }
}

Write-Host "The list of modified paths: $set"
$absolutePath = $Env:BUILD_SOURCESDIRECTORY
Write-Host "Absolute path is $absolutePath"
foreach ($directory in $set) {
    Write-Host "Current directory is $directory"
    $directoryPath = "$absolutePath\$directory"
    Write-Host "Directory path is $directoryPath"
    $nuspecPath = Get-ChildItem $directoryPath -Recurse -Depth 1 -Filter *.nuspec | Select-Object -First 1 | % { $_.FullName }
    Write-Host ".nuspec path is $nuspecPath"
    if ($nuspecPath -And (Test-Path $nuspecPath)) {          
        $Command = "nuget pack $nuspecPath -OutputDirectory $outputDirectory"
        Write-Host $Command
        Invoke-Expression $Command
    } else {
        Write-Host "##vso[task.LogIssue type=warning;] $nuspecPath file not found"
    }
}