# ---------------------------------------
# Healing Vault – One-Click Launcher
# ---------------------------------------

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
$SrcPath = Join-Path $ProjectRoot "src"

Write-Host ""
Write-Host "🧠 Starting Healing Vault..." -ForegroundColor Cyan

# Activate venv if not active
if (-not $env:VIRTUAL_ENV) {
    if (Test-Path $VenvActivate) {
        Write-Host "🔹 Activating virtual environment..." -ForegroundColor Yellow
        & $VenvActivate
    } else {
        Write-Host "❌ venv not found. Did you create it?" -ForegroundColor Red
        exit 1
    }
}

# Move to src
Set-Location $SrcPath

# Run app
python run.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Healing Vault encountered an error." -ForegroundColor Red
    exit $LASTEXITCODE
} else {
    Write-Host "✅ Healing Vault exited successfully." -ForegroundColor Green
}