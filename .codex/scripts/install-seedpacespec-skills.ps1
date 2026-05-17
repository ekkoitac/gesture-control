[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\skills'),
    [string]$TargetRoot = 'C:\Users\Saitama\.codex\skills',
    [switch]$IncludeShared
)

$ErrorActionPreference = 'Stop'

function Resolve-OrCreateDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }

    return (Resolve-Path -LiteralPath $Path).Path
}

$resolvedSourceRoot = (Resolve-Path -LiteralPath $SourceRoot).Path
$resolvedTargetRoot = Resolve-OrCreateDirectory -Path $TargetRoot

$skillDirs = Get-ChildItem -Directory -LiteralPath $resolvedSourceRoot |
    Where-Object { $_.Name -like 'seedpacespec-*' } |
    Sort-Object Name

if ($IncludeShared) {
    $sharedDir = Join-Path $resolvedSourceRoot '_shared'
    if (Test-Path -LiteralPath $sharedDir) {
        $skillDirs += Get-Item -LiteralPath $sharedDir
    }
}

if (-not $skillDirs) {
    throw "No seedpacespec skill directories found under '$resolvedSourceRoot'."
}

foreach ($skillDir in $skillDirs) {
    if ($skillDir.Name -ne '_shared' -and $skillDir.Name -notlike 'seedpacespec-*') {
        throw "Refusing to sync unexpected directory '$($skillDir.FullName)'."
    }

    $targetPath = Join-Path $resolvedTargetRoot $skillDir.Name
    $resolvedParent = (Resolve-Path -LiteralPath (Split-Path -Parent $targetPath)).Path
    if ($resolvedParent -ne $resolvedTargetRoot) {
        throw "Refusing to write outside target root: '$targetPath'."
    }

    if ($PSCmdlet.ShouldProcess($targetPath, "Sync from '$($skillDir.FullName)'")) {
        if (Test-Path -LiteralPath $targetPath) {
            Remove-Item -LiteralPath $targetPath -Recurse -Force
        }
        Copy-Item -LiteralPath $skillDir.FullName -Destination $targetPath -Recurse -Force
        Write-Host "Synced $($skillDir.Name)"
    }
}

Write-Host "SeedpaceSpec skill sync complete: $resolvedTargetRoot"
