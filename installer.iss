; ESAI Installer Script for Inno Setup
; Creates a Windows installer with English-only interface

#define MyAppName "ESAI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Dalian University of Technology"
#define MyAppURL "https://github.com/xzggg2917/ESAI-master"
#define MyAppExeName "ESAI.exe"
#define MyAppDescription "Environmental Suitability Assessment Index"

[Setup]
; Application information
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppComments={#MyAppDescription}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; Output configuration
OutputDir=installer_output
OutputBaseFilename=ESAI-Setup-v{#MyAppVersion}
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/max
SolidCompression=yes
LZMAUseSeparateProcess=yes

; Visual appearance
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; License
LicenseFile=LICENSE

; IMPORTANT: Force English language only
ShowLanguageDialog=no
Language=english

; Windows version requirements
MinVersion=6.1sp1
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
; Only English language available
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Create a Quick Launch shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main application files
Source: "dist\ESAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Include license
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; Include readme
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "README.txt"

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{group}\README"; Filename: "{app}\README.txt"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "{#MyAppDescription}"

; Quick Launch shortcut (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any created files
Type: filesandordirs; Name: "{app}"

[Code]
// Custom code to ensure English language throughout installation
function InitializeSetup(): Boolean;
begin
  // Force English locale
  Result := True;
end;

// Custom welcome message
function InitializeWizard(): Boolean;
begin
  Result := True;
end;

// Check for required dependencies
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
end;
