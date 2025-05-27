$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $rootDir

Write-Host "Entering virtual environment..." -ForegroundColor Green


Set-Location -Path ".\env"


.\Scripts\Activate.ps1


Set-Location -Path ".."

Write-Host "Virtual environment activated." -ForegroundColor Green
Write-Host "You are now at: $PWD" -ForegroundColor Yellow