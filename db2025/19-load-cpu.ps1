# 4-core step CPU load: 25% -> 50% -> 75% -> 100%
# 各段階3秒、計12秒。子プロセスをコア固定(ProcessorAffinity)して個別に負荷。
# 管理者での実行推奨（親和度変更や高分解能タイマーに必要な場合あり）

$stages       = @(0.25, 0.5, 0.75, 1.0)  # 各段階の目標負荷
$stageSeconds = 3                         # 各段階の秒数
$periodMs     = 200                       # 制御周期(分解能?15.6msを確保するため200ms推奨)
$wantCores    = 4
$useHiRes     = $false                    # 高分解能(1ms)タイマーを使うなら $true

$maxCores = [Environment]::ProcessorCount
if ($maxCores -lt $wantCores) {
  Write-Warning "このPCの論理コア数は $maxCores です。$wantCores → $maxCores に調整します。"
  $wantCores = $maxCores
}

# 子プロセスが実行するコード（busy/idleで目標使用率を作る）
$childTemplate = @"
`$ErrorActionPreference = 'Stop'

# --- 任意: 高分解能タイマー(1ms) ---
function Enable-HiResTimer {
  Add-Type -Namespace WMM -Name Time -MemberDefinition @'
    [System.Runtime.InteropServices.DllImport("winmm.dll", EntryPoint="timeBeginPeriod")]
    public static extern uint timeBeginPeriod(uint uPeriod);
    [System.Runtime.InteropServices.DllImport("winmm.dll", EntryPoint="timeEndPeriod")]
    public static extern uint timeEndPeriod(uint uPeriod);
'@
  [void][WMM.Time]::timeBeginPeriod(1)
}
function Disable-HiResTimer {
  try { [void][WMM.Time]::timeEndPeriod(1) } catch {}
}

function Invoke-Load([double[]] `$levels, [int] `$stageSeconds, [int] `$periodMs, [bool] `$hires) {
  if (`$hires) { Enable-HiResTimer }
  try {
    foreach (`$level in `$levels) {
      `$until = (Get-Date).AddSeconds(`$stageSeconds)
      while ((Get-Date) -lt `$until) {
        `$start = Get-Date
        # busy相当時間
        `$busyMs  = [double]`$periodMs * `$level
        # idle相当時間
        `$idleMs  = [double]`$periodMs - `$busyMs

        # busy: 軽い計算を回す（SqrtはJIT最適化で消えにくい）
        while (((Get-Date) - `$start).TotalMilliseconds -lt `$busyMs) {
          [Math]::Sqrt(987654321) | Out-Null
        }

        # idle: Start-Sleepは15.6ms刻みなので、できるだけスピンで精度維持
        if (`$idleMs -ge 20) {
          Start-Sleep -Milliseconds ([int]`$idleMs)
        } else {
          `$idleUntil = `$start.AddMilliseconds(`$periodMs)
          while ((Get-Date) -lt `$idleUntil) {
            Start-Sleep -Milliseconds 0  # できるだけ譲る
          }
        }
      }
    }
  } finally {
    if (`$hires) { Disable-HiResTimer }
  }
}

Invoke-Load @(STAGES) STAGESEC PERIOD HIRESON
"@

# テンプレ埋め込み
$childScript = $childTemplate.
  Replace('STAGES', ($stages -join ',')).
  Replace('STAGESEC', "$stageSeconds").
  Replace('PERIOD', "$periodMs").
  Replace('HIRESON', ($(if ($useHiRes) {'$true'} else {'$false'})))

# -EncodedCommand で安全に渡す
$encBytes = [Text.Encoding]::Unicode.GetBytes($childScript)
$encCmd   = [Convert]::ToBase64String($encBytes)

# コアごとのビットマスク（0,1,2,3 → 0x1,0x2,0x4,0x8）
$masks = foreach ($i in 0..($wantCores-1)) { [int]([math]::Pow(2,$i)) }

$procs = @()
for ($i=0; $i -lt $wantCores; $i++) {
  $p = Start-Process -FilePath "powershell" `
    -ArgumentList @("-NoProfile","-WindowStyle","Hidden","-EncodedCommand",$encCmd) `
    -PassThru
  Start-Sleep -Milliseconds 200
  try {
    $p.Refresh()
    # IntPtr で親和度セット
    $p.ProcessorAffinity = [IntPtr]::new($masks[$i])
    Write-Host ("Started worker on core #{0} (PID {1}, Affinity 0x{2:X})" -f $i, $p.Id, $masks[$i])
  } catch {
    Write-Warning "コア固定に失敗（PID $($p.Id)）。管理者で実行が必要な場合があります。"
  }
  $procs += $p
}

# 進捗表示
$totalSec = $stages.Count * $stageSeconds
$start = Get-Date
while ($true) {
  $elapsed = (Get-Date) - $start
  if ($elapsed.TotalSeconds -ge $totalSec) { break }
  $sec  = [int][Math]::Floor($elapsed.TotalSeconds)
  $step = [Math]::Min([int][Math]::Floor($sec / $stageSeconds), $stages.Count-1)
  Write-Host ("Elapsed {0,2}s / {1}s | Stage {2}/{3} -> Target {4:P0}" -f $sec, $totalSec, ($step+1), $stages.Count, $stages[$step])
  Start-Sleep -Seconds 1
}

# 終了待ち
foreach ($p in $procs) {
  if (!$p.HasExited) { $p.WaitForExit() }
}
Write-Host "Done. All workers finished."
