[void][Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$loop = 0
"Please press 'Ctrl-t' to attack."

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
            #$termination = $TRUE
            #break
            "Hit"
            python attack.py
        }
    }
    $loop++
    "Running (" + $loop + ")"
    Start-Sleep 5
}