param(
    [string]$Python = "python"
)

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment in $venvPath"
    & $Python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

$venvPython = Join-Path $venvPath "Scripts/python.exe"
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $projectRoot "requirements.txt")

Write-Host ""
Write-Host "Development environment is ready. Activate it with:"
Write-Host "  .\\.venv\\Scripts\\Activate.ps1"
