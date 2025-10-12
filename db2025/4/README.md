<pre>
基本
ts：サンプル取得時刻（UTC, ISO8601 例: 2025-10-12T13:45:05.489170Z）
hostname / username：記録したマシン名／ユーザー名（識別用）

CPU（全体）
cpu_percent：全コア合成のCPU使用率 [%]。psutil.cpu_percent(interval=…) の結果。
temp_c：CPU温度 [℃]。LHM/OpenHardwareMonitor/ACPIの順で取得。権限や機種により NULL になることあり。

CPU（内訳・統計）
cpu_user_pct：ユーザ空間のCPU使用率 [%]
cpu_system_pct：カーネル（システム）時間のCPU使用率 [%]
cpu_idle_pct：アイドル時間の割合 [%]
cpu_iowait_pct：I/O待ちの割合 [%]（Windowsでは常にNULLのことあり）
cpu_ctx_switches：コンテキストスイッチ回数（累積→瞬時取得時点のカウンタ）
cpu_interrupts：ハードウェア割り込み回数（累積）
cpu_soft_intr：ソフトウェア割り込み回数（累積；OSによりNULL）
cpu_syscalls：システムコール回数（累積；プラットフォーム依存でNULL）
cpu_logical：論理CPU数（ハイパースレッディング含む）
cpu_physical：物理コア数（取得不可な環境ではNULL）
CPU（周波数）
cpu_freq_mhz：現在の平均CPU周波数 [MHz]
cpu_freq_min_mhz / cpu_freq_max_mhz：CPU周波数の想定最小/最大 [MHz]（環境でNULLあり）
per_core_cpu：各コアのCPU使用率 [%] の配列を JSON文字列で保存（例：[3.1, 7.4, …]）
per_core_freq：各コアの現在周波数 [MHz] の配列を JSON文字列で保存（取得不可ならNULL）

メモリ（RAM）
mem_percent：メモリ使用率 [%]
mem_total：総メモリ容量 [バイト]
mem_available：新規割当てに利用可能なメモリ推定値 [バイト]

mem_used：使用中メモリ [バイト]（OSの定義に依存）
mem_free：完全な未使用メモリ [バイト]
mem_cached：ページキャッシュ量 [バイト]（WindowsではNULLのことあり）
mem_buffers：バッファ量 [バイト]（Linux中心・WindowsではNULL）
mem_shared：共有メモリ量 [バイト]（OS依存・多くはNULL）

スワップ
swap_percent：スワップ使用率 [%]
swap_total / swap_used / swap_free：スワップ総量／使用量／空き [バイト]
swap_sin / swap_sout：スワップイン／アウトの累積バイト数（OSによりNULL）

負荷平均（UNIX系）
load1 / load5 / load15：1/5/15分のロードアベレージ（Windowsは通常 NULL)

</pre>
  <
</pre>
