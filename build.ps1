#Requires -Version 5.1
<#
.SYNOPSIS
    Yum Agent Company VSIX build script.

.NOTES
    ASCII-only output on purpose. Korean text in console scripts can break
    on Windows code pages when launched by double-click.
#>

$ErrorActionPreference = 'Stop'

try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
} catch {
    # Older hosts may not allow changing encoding. Build can continue.
}

$env:NO_COLOR = '1'
$env:FORCE_COLOR = '0'
$env:NPM_CONFIG_UNICODE = 'false'

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

function Step($Text) {
    Write-Host ""
    Write-Host $Text -ForegroundColor Yellow
}

function Require-Command($Name, $InstallHint) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "$Name not found. $InstallHint"
    }
}

function Run-Cmd($File, [string[]]$ArgsList) {
    Write-Host "  > $File $($ArgsList -join ' ')" -ForegroundColor DarkGray
    & $File @ArgsList
    if ($LASTEXITCODE -ne 0) {
        throw "$File failed with exit code $LASTEXITCODE"
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Yum Agent Company VSIX Builder" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

Step "[1/5] Checking tools"
Require-Command "node" "Install Node.js LTS, then reopen terminal."
Require-Command "npm" "Install Node.js LTS, then reopen terminal."
Run-Cmd "node" @("--version")
Run-Cmd "npm" @("--version")

Step "[2/5] Validating package.json"
Run-Cmd "node" @("-e", "JSON.parse(require('fs').readFileSync('package.json','utf8')); console.log('package.json OK')")

Step "[3/5] Installing dependencies"
if (-not (Test-Path "node_modules")) {
    Run-Cmd "npm" @("install")
} else {
    Write-Host "  node_modules OK" -ForegroundColor Green
}

Step "[4/5] Compiling extension"
Run-Cmd "npm" @("run", "compile")

Step "[5/5] Packaging VSIX"
$vsceCmd = Get-Command vsce -ErrorAction SilentlyContinue
if ($vsceCmd) {
    Run-Cmd "vsce" @("package", "--allow-missing-repository", "--no-dependencies")
} else {
    Run-Cmd "npx" @("--yes", "@vscode/vsce", "package", "--allow-missing-repository", "--no-dependencies")
}

$vsix = Get-ChildItem -Path $ProjectDir -Filter "*.vsix" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $vsix) {
    throw "VSIX file not found after packaging."
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  BUILD SUCCESS" -ForegroundColor Green
Write-Host "  $($vsix.FullName)" -ForegroundColor White
Write-Host "  Size: $([math]::Round($vsix.Length / 1MB, 2)) MB" -ForegroundColor Gray
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Install:" -ForegroundColor Cyan
Write-Host "  code --install-extension `"$($vsix.FullName)`"" -ForegroundColor Gray
