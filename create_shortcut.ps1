$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Agent V2.lnk"
$PythonPath = (Get-Command python).Source
$ScriptPath = Join-Path $PWD "agent_gui.py"
$IconPath = Join-Path $PWD "public\agent_icon.ico" # Use generated icon

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonPath
$Shortcut.Arguments = """$ScriptPath"""
$Shortcut.WorkingDirectory = $PWD.Path
$Shortcut.Description = "Launch Agent V2 Lite UI"

if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}

$Shortcut.Save()

Write-Host "Shortcut created at: $ShortcutPath"
