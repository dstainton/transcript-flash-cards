Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Scrum Flashcards.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = WScript.ScriptFullName.Replace("CREATE_SHORTCUT.vbs", "start_flashcards.bat")
    oLink.WorkingDirectory = WScript.ScriptFullName.Replace("\CREATE_SHORTCUT.vbs", "")
    oLink.Description = "Start Scrum Flashcards Application"
    oLink.IconLocation = "C:\Windows\System32\shell32.dll,13"
oLink.Save

MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & "You can now start the application from your desktop.", vbInformation, "Scrum Flashcards"

