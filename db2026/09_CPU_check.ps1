$data = Invoke-RestMethod "http://127.0.0.1:8085/data.json"

function Show-SensorTree {
    param(
        $Node,
        [string]$Parent = ""
    )

    $path = "$Parent/$($Node.Text)"

    if ($path -match '(?i)CPU|Processor|Core|Package') {
        [PSCustomObject]@{
            Path  = $path
            Value = $Node.Value
        }
    }

    foreach ($child in @($Node.Children)) {
        if ($null -ne $child) {
            Show-SensorTree -Node $child -Parent $path
        }
    }
}

Show-SensorTree -Node $data |
    Format-Table -AutoSize -Wrap