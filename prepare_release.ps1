# Automated Release Preparation Script
# Prepares all files needed for GitHub Release

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ESAI Release Preparation Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$version = "1.0.0"
$portableZip = "ESAI-v$version-Portable-Windows.zip"
$installerExe = "installer_output\ESAI-Setup-v$version.exe"

# Step 1: Check if build exists
Write-Host "[Step 1/4] Checking build status..." -ForegroundColor Yellow

if (-not (Test-Path "dist\ESAI\ESAI.exe")) {
    Write-Host "Build not found. Building now..." -ForegroundColor Yellow
    & .\build_and_package.ps1
    
    if (-not (Test-Path "dist\ESAI\ESAI.exe")) {
        Write-Host "Build failed! Cannot prepare release." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Build found" -ForegroundColor Green

# Step 2: Create portable ZIP
Write-Host ""
Write-Host "[Step 2/4] Creating portable ZIP..." -ForegroundColor Yellow

if (Test-Path $portableZip) {
    Remove-Item $portableZip -Force
}

Compress-Archive -Path "dist\ESAI\*" -DestinationPath $portableZip -CompressionLevel Optimal

if (Test-Path $portableZip) {
    $zipSize = (Get-Item $portableZip).Length / 1MB
    Write-Host "✓ Created: $portableZip ($([math]::Round($zipSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create portable ZIP" -ForegroundColor Red
    exit 1
}

# Step 3: Check installer
Write-Host ""
Write-Host "[Step 3/4] Checking installer..." -ForegroundColor Yellow

if (Test-Path $installerExe) {
    $installerSize = (Get-Item $installerExe).Length / 1MB
    Write-Host "✓ Found: $installerExe ($([math]::Round($installerSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "⚠ Installer not found" -ForegroundColor Yellow
    Write-Host "  To create installer, install Inno Setup and run:" -ForegroundColor Gray
    Write-Host "  .\build_and_package.ps1" -ForegroundColor Gray
}

# Step 4: Generate checksums
Write-Host ""
Write-Host "[Step 4/4] Generating checksums..." -ForegroundColor Yellow

Write-Host ""
Write-Host "SHA256 Checksums:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

$zipHash = (Get-FileHash $portableZip -Algorithm SHA256).Hash
Write-Host ""
Write-Host "Portable ZIP:" -ForegroundColor White
Write-Host "  File: $portableZip" -ForegroundColor Gray
Write-Host "  SHA256: $zipHash" -ForegroundColor Gray

if (Test-Path $installerExe) {
    $installerHash = (Get-FileHash $installerExe -Algorithm SHA256).Hash
    Write-Host ""
    Write-Host "Installer:" -ForegroundColor White
    Write-Host "  File: $installerExe" -ForegroundColor Gray
    Write-Host "  SHA256: $installerHash" -ForegroundColor Gray
}

# Save checksums to file
$checksumFile = "CHECKSUMS.txt"
$checksumContent = @"
ESAI v$version - SHA256 Checksums
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
==========================================

Portable Version:
File: $portableZip
SHA256: $zipHash

"@

if (Test-Path $installerExe) {
    $checksumContent += @"
Windows Installer:
File: $installerExe
SHA256: $installerHash

"@
}

$checksumContent | Out-File -FilePath $checksumFile -Encoding UTF8

Write-Host ""
Write-Host "✓ Checksums saved to: $checksumFile" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Release Preparation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Files ready for upload:" -ForegroundColor Cyan
Write-Host ""

Get-ChildItem -Path . -Filter "ESAI-v*.zip" | ForEach-Object {
    Write-Host "  ✓ $($_.Name)" -ForegroundColor White
    Write-Host "    Size: $([math]::Round($_.Length / 1MB, 2)) MB" -ForegroundColor Gray
    Write-Host "    Path: $($_.FullName)" -ForegroundColor Gray
    Write-Host ""
}

if (Test-Path $installerExe) {
    $installer = Get-Item $installerExe
    Write-Host "  ✓ $($installer.Name)" -ForegroundColor White
    Write-Host "    Size: $([math]::Round($installer.Length / 1MB, 2)) MB" -ForegroundColor Gray
    Write-Host "    Path: $($installer.FullName)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/xzggg2917/ESAI-master/releases/new" -ForegroundColor White
Write-Host "  2. Tag version: v$version" -ForegroundColor White
Write-Host "  3. Upload the files listed above" -ForegroundColor White
Write-Host "  4. Copy release notes from RELEASE_GUIDE.md" -ForegroundColor White
Write-Host "  5. Click 'Publish release'" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: RELEASE_GUIDE.md" -ForegroundColor Gray
