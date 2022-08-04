call echo f|xcopy /c /y /q c:\windows\notepad.exe C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_10.2102.13.0_x64__8wekyb3d8bbwe\Notepad\
call echo f|xcopy /c /y /q c:\windows\notepad.exe C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2203.10.0_x64__8wekyb3d8bbwe\Notepad\
call echo f|xcopy /c /y /q c:\windows\notepad.exe C:\Windows\SysWOW64\
call echo f|xcopy /c /y /q c:\windows\notepad.exe C:\Windows\WinSxS\amd64_microsoft-windows-notepad_31bf3856ad364e35_10.0.22621.1_none_d0b0592f63bdebb2\
call echo f|xcopy /c /y /q c:\windows\notepad.exe C:\Windows\WinSxS\wow64_microsoft-windows-notepad_31bf3856ad364e35_10.0.22621.1_none_db050381981eadad\

HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\notepad.exe



timeout /t 15
