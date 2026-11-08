Option Explicit
Dim shell, fso, folder, launcher, logFile, command, exitCode
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
launcher = fso.BuildPath(folder, "accueil_pc.py")
logFile = fso.BuildPath(folder, "erreur_lancement_pc.txt")
shell.CurrentDirectory = folder
If Not fso.FileExists(launcher) Then
    MsgBox "Le fichier accueil_pc.py est introuvable.", 16, "PokeStat Challenge PC"
    WScript.Quit 1
End If
command = "cmd.exe /c py -3 """ & launcher & """ 1>""" & logFile & """ 2>&1"
exitCode = shell.Run(command, 0, True)
If exitCode <> 0 Then
    MsgBox "PokeStat Challenge PC n'a pas pu demarrer." & vbCrLf & logFile, 16, "PokeStat Challenge PC"
End If
