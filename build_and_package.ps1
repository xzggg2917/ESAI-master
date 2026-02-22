# Complete build and packaging automation script
# Builds executable and creates Windows installer

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ESAI Complete Build & Package Process" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build the executable
Write-Host "[Step 1/2] Building executable..." -ForegroundColor Yellow
& .\build.ps1

if (-not (Test-Path "dist\ESAI\ESAI.exe")) {
    Write-Host ""
    Write-Host "Build failed! Cannot proceed with installer creation." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Executable build successful!" -ForegroundColor Green

# Step 2: Create installer (if Inno Setup is installed)
Write-Host ""
Write-Host "[Step 2/2] Creating Windows installer..." -ForegroundColor Yellow

# Common Inno Setup installation paths
$innoSetupPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe"
)

$innoSetup = $null
foreach ($path in $innoSetupPaths) {
    if (Test-Path $path) {
        $innoSetup = $path
        break
    }
}

if ($innoSetup) {
    Write-Host "Found Inno Setup at: $innoSetup" -ForegroundColor Gray
    
    # Create output directory
    if (-not (Test-Path "installer_output")) {
        New-Item -ItemType Directory -Path "installer_output" | Out-Null
    }
    
    # Compile installer
    & $innoSetup installer.iss
    
    if (Test-Path "installer_output\ESAI-Setup-v1.0.0.exe") {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Packaging Complete!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Created files:" -ForegroundColor Cyan
        Write-Host "  1. Portable: dist\ESAI\ESAI.exe" -ForegroundColor White
        Write-Host "  2. Installer: installer_output\ESAI-Setup-v1.0.0.exe" -ForegroundColor White
        Write-Host ""
        Write-Host "Installer size:" -ForegroundColor Yellow
        $installerSize = (Get-Item "installer_output\ESAI-Setup-v1.0.0.exe").Length / 1MB
        Write-Host "  $([math]::Round($installerSize, 2)) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "Ready for distribution!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Installer creation failed!" -ForegroundColor Red
        Write-Host "Check installer.iss for errors" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "Inno Setup not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create an installer:" -ForegroundColor White
    Write-Host "  1. Download Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor Gray
    Write-Host "  2. Install it" -ForegroundColor Gray
    Write-Host "  3. Run this script again" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Or use the portable version: dist\ESAI\ESAI.exe" -ForegroundColor Cyan
}
