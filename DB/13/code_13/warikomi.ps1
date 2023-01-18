$Start_Time = (Get-date).second
Write-Host "Type CTRL-C to Terminate..."
$n = 1
Try
{
    While($true)
    {
        Write-Host $n
        $n ++
        Start-Sleep -m 5000
    }
}
Finally
{
    $End_Time = (Get-date).second
    $Time_Diff = $End_Time - $Start_Time
    Write-Host "Total time in seconds"$Time_Diff
}[void][Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$loop = 0
"Please press 'Ctrl-t' to stop."

$rawui = $Host.ui.rawui
$keystates = [System.Management.Automation.Host.ControlKeyStates]
$modifier = $keystates::LeftCtrlPressed -bor $keystates::RightCtrlPressed
$keymap = [System.Windows.Forms.Keys]
for ($termination = $FALSE; $termination -eq $FALSE; )
{
    while ($rawui.KeyAvailable)
    {
        $keyinput = $rawui.Readkey("NoEcho,IncludeKeyUp,IncludeKeyDown")
        if (($keyinput.VirtualKeycode -eq $keymap::T) -and `
            ($keyinput.ControlKeyState -band $modifier))
        {
            $termination = $TRUE
            break
        }
    }
    $loop++
    "Running (" + $loop + ")"
    Start-Sleep 1
}[void][Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$loop = 0
"Please press 'Ctrl-t' to stop."

$rawui = $Host.ui.rawui
$keystates = [System.Management.Automation.Host.ControlKeyStates]
$modifier = $keystates::LeftCtrlPressed -bor $keystates::RightCtrlPressed
$keymap = [System.Windows.Forms.Keys]
for ($termination = $FALSE; $termination -eq $FALSE; )
{
    while ($rawui.KeyAvailable)
    {
        $keyinput = $rawui.Readkey("NoEcho,IncludeKeyUp,IncludeKeyDown")
        if (($keyinput.VirtualKeycode -eq $keymap::T) -and `
            ($keyinput.ControlKeyState -band $modifier))
        {
            $termination = $TRUE
            break
        }
    }
    $loop++
    "Running (" + $loop + ")"
    Start-Sleep 1
}