# Creating Windows Installer for ESAI

## Overview

This guide explains how to create a professional Windows installer using **Inno Setup** with full English interface.

## Prerequisites

1. **Completed Build**: Run `build.ps1` first to create `dist\ESAI\` folder
2. **Inno Setup**: Download from [jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)

## Installation Steps

### 1. Install Inno Setup

Download and install Inno Setup (Unicode version recommended).

### 2. Create Installer Script

Save the following as `installer.iss`:

```iss
; ESAI Installer Script
; English-only interface regardless of system locale

#define MyAppName "ESAI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Dalian University of Technology"
#define MyAppURL "https://github.com/xzggg2917/ESAI-master"
#define MyAppExeName "ESAI.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=ESAI-Setup-v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
; Force English language
ShowLanguageDialog=no
Language=english

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\ESAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
// Force English locale during installation
function InitializeSetup(): Boolean;
begin
  // This ensures installer runs in English
  Result := True;
end;
```

### 3. Build the Installer

1. **Open Inno Setup Compiler**
2. **File → Open** → Select `installer.iss`
3. **Build → Compile** (or press Ctrl+F9)

The installer will be created in `installer_output\ESAI-Setup-v1.0.0.exe`

## Alternative: Using Inno Setup via Command Line

```powershell
# Compile installer from command line
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## Complete Build Process

### Option 1: Step by Step

```powershell
# 1. Build the executable
.\build.ps1

# 2. Create installer (if Inno Setup installed)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Option 2: Full Automation Script

Create `build_and_package.ps1`:

```powershell
# Complete build and packaging script
Write-Host "Building ESAI application..." -ForegroundColor Cyan
.\build.ps1

if (Test-Path "dist\ESAI\ESAI.exe") {
    Write-Host "`nCreating Windows installer..." -ForegroundColor Cyan
    
    $innoSetup = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (Test-Path $innoSetup) {
        & $innoSetup installer.iss
        
        if (Test-Path "installer_output\ESAI-Setup-v1.0.0.exe") {
            Write-Host "`nPackaging complete!" -ForegroundColor Green
            Write-Host "Installer: installer_output\ESAI-Setup-v1.0.0.exe" -ForegroundColor Cyan
        }
    } else {
        Write-Host "Inno Setup not found. Install from:" -ForegroundColor Yellow
        Write-Host "https://jrsoftware.org/isdl.php" -ForegroundColor Gray
    }
}
```

## Installer Features

✅ **English-only interface** (forced, not system-dependent)  
✅ **Modern wizard style**  
✅ **Desktop icon option**  
✅ **Uninstaller included**  
✅ **Start menu shortcuts**  
✅ **License agreement (MIT)**  
✅ **Professional appearance**

## Testing the Installer

1. Run `ESAI-Setup-v1.0.0.exe`
2. Verify all text is in English
3. Complete installation
4. Test the installed application
5. Test uninstallation

## Troubleshooting

### Missing DLL Errors
If users report missing DLL errors, ensure all dependencies are included:
```bash
# Run dependency walker on ESAI.exe
# Add missing DLLs to [Files] section in installer.iss
```

### Application Won't Start
- Check Windows Defender/Antivirus hasn't quarantined it
- Verify all resource files (rj.png, logo.ico, save.png) are included
- Test on a clean Windows installation

## Distribution

The final installer can be distributed via:
- GitHub Releases
- Direct download link
- University repository
- Academic paper supplementary materials

## Notes

- Installer is **always in English** regardless of Windows language
- Application interface is **always in English** (as designed)
- MIT License is included automatically
- Digital signing recommended for production release
