Add-Type -AssemblyName System.Windows.Forms
$wshell = New-Object -ComObject WScript.Shell
$wshell.AppActivate("ssh root@104.238.214.91")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("Zyanite777#628152{ENTER}")
