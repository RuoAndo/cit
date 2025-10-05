# 4-core step CPU load: 25% -> 50% -> 75% -> 100%
# �e�i�K3�b�A�v12�b�B�q�v���Z�X���R�A�Œ�(ProcessorAffinity)���Čʂɕ��ׁB
# �Ǘ��҂ł̎��s�����i�e�a�x�ύX�⍂����\�^�C�}�[�ɕK�v�ȏꍇ����j

$stages       = @(0.25, 0.5, 0.75, 1.0)  # �e�i�K�̖ڕW����
$stageSeconds = 3                         # �e�i�K�̕b��
$periodMs     = 200                       # �������(����\?15.6ms���m�ۂ��邽��200ms����)
$wantCores    = 4
$useHiRes     = $false                    # ������\(1ms)�^�C�}�[���g���Ȃ� $true

$maxCores = [Environment]::ProcessorCount
if ($maxCores -lt $wantCores) {
  Write-Warning "����PC�̘_���R�A���� $maxCores �ł��B$wantCores �� $maxCores �ɒ������܂��B"
  $wantCores = $maxCores
}

# �q�v���Z�X�����s����R�[�h�ibusy/idle�ŖڕW�g�p�������j
$childTemplate = @"
`$ErrorActionPreference = 'Stop'

# --- �C��: ������\�^�C�}�[(1ms) ---
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
        # busy��������
        `$busyMs  = [double]`$periodMs * `$level
        # idle��������
        `$idleMs  = [double]`$periodMs - `$busyMs

        # busy: �y���v�Z���񂷁iSqrt��JIT�œK���ŏ����ɂ����j
        while (((Get-Date) - `$start).TotalMilliseconds -lt `$busyMs) {
          [Math]::Sqrt(987654321) | Out-Null
        }

        # idle: Start-Sleep��15.6ms���݂Ȃ̂ŁA�ł��邾���X�s���Ő��x�ێ�
        if (`$idleMs -ge 20) {
          Start-Sleep -Milliseconds ([int]`$idleMs)
        } else {
          `$idleUntil = `$start.AddMilliseconds(`$periodMs)
          while ((Get-Date) -lt `$idleUntil) {
            Start-Sleep -Milliseconds 0  # �ł��邾������
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

# �e���v�����ߍ���
$childScript = $childTemplate.
  Replace('STAGES', ($stages -join ',')).
  Replace('STAGESEC', "$stageSeconds").
  Replace('PERIOD', "$periodMs").
  Replace('HIRESON', ($(if ($useHiRes) {'$true'} else {'$false'})))

# -EncodedCommand �ň��S�ɓn��
$encBytes = [Text.Encoding]::Unicode.GetBytes($childScript)
$encCmd   = [Convert]::ToBase64String($encBytes)

# �R�A���Ƃ̃r�b�g�}�X�N�i0,1,2,3 �� 0x1,0x2,0x4,0x8�j
$masks = foreach ($i in 0..($wantCores-1)) { [int]([math]::Pow(2,$i)) }

$procs = @()
for ($i=0; $i -lt $wantCores; $i++) {
  $p = Start-Process -FilePath "powershell" `
    -ArgumentList @("-NoProfile","-WindowStyle","Hidden","-EncodedCommand",$encCmd) `
    -PassThru
  Start-Sleep -Milliseconds 200
  try {
    $p.Refresh()
    # IntPtr �Őe�a�x�Z�b�g
    $p.ProcessorAffinity = [IntPtr]::new($masks[$i])
    Write-Host ("Started worker on core #{0} (PID {1}, Affinity 0x{2:X})" -f $i, $p.Id, $masks[$i])
  } catch {
    Write-Warning "�R�A�Œ�Ɏ��s�iPID $($p.Id)�j�B�Ǘ��҂Ŏ��s���K�v�ȏꍇ������܂��B"
  }
  $procs += $p
}

# �i���\��
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

# �I���҂�
foreach ($p in $procs) {
  if (!$p.HasExited) { $p.WaitForExit() }
}
Write-Host "Done. All workers finished."
