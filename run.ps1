<#
.SYNOPSIS
    Re-process a video and (optionally) run Alembic migrations.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Video,          # video path

    [Parameter(Mandatory=$true)]
    [string]$Output,         # output folder

    [switch]$Migrate,        # include to autogenerate & upgrade

    [string]$PoetryExe = "$Env:USERPROFILE\pipx\venvs\poetry\Scripts\poetry.exe"
)

# 0. basic checks
if (-not (Test-Path $PoetryExe)) { Write-Error "Poetry not found: $PoetryExe"; exit 1 }
if (-not (Test-Path $Video))     { Write-Error "Video video not found: $Video"; exit 1 }
if (-not (Test-Path $Output))    { New-Item -ItemType Directory -Path $Output | Out-Null }

# 1. optional migration
if ($Migrate) {
    Write-Host "> Alembic autogenerate..."
    & $PoetryExe run alembic revision --autogenerate -m "auto_$(Get-Date -f yyyyMMdd_HHmmss)"
    if ($LASTEXITCODE) { exit $LASTEXITCODE }

    Write-Host "> Alembic upgrade head..."
    & $PoetryExe run alembic upgrade head
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}

# 2. re-process video
Write-Host "> Processing video $Video -> $Output"
& $PoetryExe run python scripts\reprocess_video.py --Video $Video --output $Output
exit $LASTEXITCODE
