Option Explicit

Dim shell, fso, folder, launcher, logFile, command, exitCode
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

folder = fso.GetParentFolderName(WScript.ScriptFullName)
launcher = fso.BuildPath(folder, "accueil.py")
logFile = fso.BuildPath(folder, "erreur_lancement.txt")
shell.CurrentDirectory = folder

If Not fso.FileExists(launcher) Then
    MsgBox "Le fichier accueil.py est introuvable dans :" & vbCrLf & folder, 16, "PokeStat Challenge"
    WScript.Quit 1
End If

If fso.FileExists(logFile) Then
    On Error Resume Next
    fso.DeleteFile logFile, True
    On Error GoTo 0
End If

command = "cmd.exe /c py -3 """ & launcher & """ 1>""" & logFile & """ 2>&1"
exitCode = shell.Run(command, 0, True)

If exitCode <> 0 Then
    MsgBox "PokeStat Challenge n'a pas pu demarrer." & vbCrLf & vbCrLf & _
           "Le detail de l'erreur se trouve dans :" & vbCrLf & logFile, _
           16, "PokeStat Challenge"
End If
