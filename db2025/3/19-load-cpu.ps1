# 4-core step CPU load: 25% -> 50% -> 75% -> 100%
# 各段階3秒、計12秒。コアを個別プロセス＋ProcessorAffinityで固定。
# 管理者での実行推奨（親和度変更に必要な場合がある）

$stages       = @(0.25, 0.5, 0.75, 1.0)  # 段階的負荷
$stageSeconds = 3                         # 各段階の秒数
$periodMs     = 50                        # 制御周期(小さいほど精度↑)
$wantCores    = 4

$maxCores = [Environment]::ProcessorCount
if ($maxCores -lt $wantCores) {
    Write-Warning "このPCの論理コア数は $maxCores です。$wantCores → $maxCores に調整します。"
    $wantCores = $maxCores
}

# 子プロセスが実行するコード（busy/idleで目標使用率を作る）
$childTemplate = @"
`$ErrorActionPreference = 'Stop'
function Invoke-Load([double[]] `$levels, [int] `$stageSeconds, [int] `$periodMs) {
  foreach (`$level in `$levels) {
    `$until = (Get-Date).AddSeconds(`$stageSeconds)
    while ((Get-Date) -lt `$until) {
      `$start = Get-Date
      # busy
      while ((Get-Date) - `$start -lt [TimeSpan]::FromMilliseconds(`$periodMs * `$level)) {
        [Math]::Sqrt(987654321) | Out-Null
      }
      # idle
      Start-Sleep -Milliseconds ([int]([Math]::Max(0, `$periodMs * (1 - `$level))))
    }
  }
}
Invoke-Load @(STAGES) STAGESEC PERIOD
"@

# ステージ／秒数／周期を埋め込む
$childScript = $childTemplate.
    Replace('STAGES', ($stages -join ',')).
    Replace('STAGESEC', "$stageSeconds").
    Replace('PERIOD', "$periodMs")

# コアごとのビットマスク（0,1,2,3コア → 0x1,0x2,0x4,0x8）
$masks = foreach ($i in 0..($wantCores-1)) { [int]([math]::Pow(2,$i)) }

$procs = @()
for ($i=0; $i -lt $wantCores; $i++) {
    $p = Start-Process -FilePath "powershell" `
        -ArgumentList @("-NoProfile","-WindowStyle","Hidden","-Command",$childScript) `
        -PassThru
    Start-Sleep -Milliseconds 200
    try {
        $p.Refresh()
        $p.ProcessorAffinity = $masks[$i]
        Write-Host ("Started worker on core #{0} (PID {1}, Affinity 0x{2:X})" -f $i, $p.Id, $masks[$i])
    } catch {
        Write-Warning "コア固定に失敗（PID $($p.Id)）。管理者で実行が必要な場合があります。"; 
    }
    $procs += $p
}

# 進捗表示（親プロセス側）
$totalSec = $stages.Count * $stageSeconds
$start = Get-Date
while ($true) {
    $elapsed = (Get-Date) - $start
    if ($elapsed.TotalSeconds -ge $totalSec) { break }
    $sec = [int][Math]::Floor($elapsed.TotalSeconds)
    $step = [int][Math]::Floor($sec / $stageSeconds)
    $step = [Math]::Min($step, $stages.Count-1)
    Write-Host ("Elapsed {0,2}s / {1}s | Stage {2}/{3} -> Target {4:P0}" -f $sec, $totalSec, ($step+1), $stages.Count, $stages[$step])
    Start-Sleep -Seconds 1
}

# 終了待ち＆後片付け
foreach ($p in $procs) {
    if (!$p.HasExited) { $p.WaitForExit() }
}
Write-Host "Done. All workers finished."
