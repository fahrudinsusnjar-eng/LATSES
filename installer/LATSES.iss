#define AppName "LAT-CES Scientific Engineering"
#define AppVersion "1.1.0"
#define AppPublisher "LATSES"
#define AppExeName "LATSES.exe"

[Setup]
AppId={{B7C2C2F6-4B0B-4F65-9A19-6A0FAD8D5A11}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\LAT-CES
DefaultGroupName=LAT-CES
OutputDir=installer-output
OutputBaseFilename=LAT-CES-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Files]
Source: "..\dist\LATSES.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\LAT-CES Scientific Engineering"; Filename: "{app}\LATSES.exe"
Name: "{commondesktop}\LAT-CES Scientific Engineering"; Filename: "{app}\LATSES.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\LATSES.exe"; Description: "Start LAT-CES Scientific Engineering"; Flags: nowait postinstall skipifsilent
