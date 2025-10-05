# 4-core step CPU load: 25% -> 50% -> 75% -> 100%
# �e�i�K3�b�A�v12�b�B�R�A���ʃv���Z�X�{ProcessorAffinity�ŌŒ�B
# �Ǘ��҂ł̎��s�����i�e�a�x�ύX�ɕK�v�ȏꍇ������j

$stages       = @(0.25, 0.5, 0.75, 1.0)  # �i�K�I����
$stageSeconds = 3                         # �e�i�K�̕b��
$periodMs     = 50                        # �������(�������قǐ��x��)
$wantCores    = 4

$maxCores = [Environment]::ProcessorCount
if ($maxCores -lt $wantCores) {
    Write-Warning "����PC�̘_���R�A���� $maxCores �ł��B$wantCores �� $maxCores �ɒ������܂��B"
    $wantCores = $maxCores
}

# �q�v���Z�X�����s����R�[�h�ibusy/idle�ŖڕW�g�p�������j
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

# �X�e�[�W�^�b���^�����𖄂ߍ���
$childScript = $childTemplate.
    Replace('STAGES', ($stages -join ',')).
    Replace('STAGESEC', "$stageSeconds").
    Replace('PERIOD', "$periodMs")

# �R�A���Ƃ̃r�b�g�}�X�N�i0,1,2,3�R�A �� 0x1,0x2,0x4,0x8�j
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
        Write-Warning "�R�A�Œ�Ɏ��s�iPID $($p.Id)�j�B�Ǘ��҂Ŏ��s���K�v�ȏꍇ������܂��B"; 
    }
    $procs += $p
}

# �i���\���i�e�v���Z�X���j
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

# �I���҂�����Еt��
foreach ($p in $procs) {
    if (!$p.HasExited) { $p.WaitForExit() }
}
Write-Host "Done. All workers finished."
