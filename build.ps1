# ESAI Build Script
# Builds a standalone Windows executable with English interface

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ESAI Application Build Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Check if PyInstaller is installed
Write-Host "Checking PyInstaller..." -ForegroundColor Yellow
$pyinstaller = python -m pip show pyinstaller 2>$null
if (-not $pyinstaller) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

# Clean previous builds
Write-Host ""
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "dist") { Remove-Item -Recurse -Force dist }

# Build the application
Write-Host ""
Write-Host "Building ESAI application..." -ForegroundColor Green
Write-Host "This may take several minutes..." -ForegroundColor Gray

# Set locale to English for build process
$env:LANG = "en_US.UTF-8"
$env:LC_ALL = "en_US.UTF-8"

# Run PyInstaller with spec file
pyinstaller --clean ESAI.spec

# Check if build was successful
if (Test-Path "dist\ESAI\ESAI.exe") {
    Write-Host ""
    Write-Host "Copying resource files..." -ForegroundColor Yellow
    Copy-Item "logo.ico" "dist\ESAI\" -Force
    Copy-Item "rj.png" "dist\ESAI\" -Force  
    Copy-Item "save.png" "dist\ESAI\" -Force
    Write-Host "✓ Resource files copied" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\ESAI\ESAI.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Distribution folder contents:" -ForegroundColor Yellow
    Get-ChildItem "dist\ESAI" | Format-Table Name, Length -AutoSize
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Yellow
    Write-Host "  .\dist\ESAI\ESAI.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "To create installer, see: CREATE_INSTALLER.md" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "Build FAILED!" -ForegroundColor Red
    Write-Host "Check the output above for errors" -ForegroundColor Red
    exit 1
}
