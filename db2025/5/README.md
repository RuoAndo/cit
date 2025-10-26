# CPU負荷をDB格納

<pre>
PS D:\cit\db2025\5> python .\35_dump_system_metrics.py
[INIT] removed: cpu_metrics.db
ts,cpu_percent,temp_c,cpu_user_pct,cpu_system_pct,cpu_idle_pct,cpu_iowait_pct,cpu_ctx_switches,cpu_interrupts,cpu_soft_intr,cpu_syscalls,cpu_logical,cpu_physical,cpu_freq_mhz,cpu_freq_min_mhz,cpu_freq_max_mhz,per_core_cpu,per_core_freq,mem_percent,mem_total,mem_available,mem_used,mem_free,mem_cached,mem_buffers,mem_shared,swap_percent,swap_total,swap_used,swap_free,swap_sin,swap_sout,load1,load5,load15,hostname,username
2025-10-24T02:45:35.179305Z,11.8,64.05000000000001,5.6,7.9,86.2,,3827935550,1247012304,0,427163764,4,2,2400.0,0.0,2401.0,"[25.9, 5.6, 4.7, 18.7]",[2400.0],64.2,17108365312,6122053632,10986311680,6122053632,,,,0.9,24696061952,226119680,24469942272,0,0,,,,DESKTOP-329HOL1,user
2025-10-24T02:45:36.231018Z,12.1,64.05000000000001,5.6,8.7,85.7,,3827964620,1247024045,0,427461168,4,2,2400.0,0.0,2401.0,"[15.3, 3.1, 9.2, 29.6]",[2400.0],64.3,17108365312,6104264704,11004100608,6104264704,,,,0.9,24696061952,226119680,24469942272,0,0,,,,DESKTOP-329HOL1,user
2025-10-24T02:45:37.306527Z,10.5,64.05000000000001,5.1,5.1,89.4,,3827979262,1247029578,0,427593468,4,2,2300.0,0.0,2401.0,"[25.0, 4.3, 8.8, 4.4]",[2300.0],64.3,17108365312,6102761472,11005603840,6102761472,,,,0.9,24696061952,226119680,24469942272,0,0,,,,DESKTOP-329HOL1,user
2025-10-24T02:45:38.365056Z,14.2,64.05000000000001,6.2,7.7,86.0,,3827998209,1247036886,0,427824668,4,2,2400.0,0.0,2401.0,"[30.9, 10.3, 2.9, 11.8]",[2400.0],64.4,17108365312,6098370560,11009994752,6098370560,,,,0.9,24696061952,226119680,24469942272,0,0,,,,DESKTOP-329HOL1,user
</pre>
  
データベースに格納されている項目

<pre>
ts, cpu_percent, temp_c,
cpu_user_pct, cpu_system_pct, cpu_idle_pct, cpu_iowait_pct,
cpu_ctx_switches, cpu_interrupts, cpu_soft_intr, cpu_syscalls,
cpu_logical, cpu_physical,
cpu_freq_mhz, cpu_freq_min_mhz, cpu_freq_max_mhz,
per_core_cpu, per_core_freq,
mem_percent, mem_total, mem_available, mem_used, mem_free, mem_cached, mem_buffers, mem_shared,
swap_percent, swap_total, swap_used, swap_free, swap_sin, swap_sout,
load1, load5, load15,
hostname, username
</pre>

# オンラインゲームのDB

<img src = "players.png">
