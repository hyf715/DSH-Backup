---
id: 36
tags: x2d lut deploy sigpipe build grmod
pinned: false
created_at: 2026-10-16T11:36:59.141000+00:00
updated_at: 2026-10-16T11:36:59.141000+00:00
---

[x2d LUT 三件部署完成 + server .so 构建坑 2026-10-16] X2D LUT 修复已实机部署（未整机重启）：(1) `/system/etc/x2d-lut/memtool` = **1f63b5d3**（v6，成片 main/pyra 也改 composite_view + 0% 时删 active_lut.bin 直通）；(2) `/system/lib64/libx2d_speed_server.so` = **735d7e70**（含 `signal(13,SIG_IGN)` 忽略 SIGPIPE + write 失败只丢本连接）；(3) `/system/etc/X2dPlayPage.qml` = **c0eb865a**（固定 6 档 0/20/40/60/80/100 + 松手才提交）。备份都在 /data/local/tmp：memtool.bak-pre-v6=7d836603、libx2d_speed_server.so.bak-pre-v2=58387ce4、X2dPlayPage.qml.bak-pre-v6=ead1fcac。实测 /status 通、lut_select 0 删 active、100 重建=源LUT、server 全程存活、/system=ro。【**关键坑**：自建 libx2d_speed_server.so 必须带 `DT_NEEDED libc.so`】——原构建用 `clang -target aarch64-linux-gnu -fuse-ld=lld -nostdlib ... <stub>/libc.so`；若只用 NDK `-nostdlib` 不加 stub，产物无 NEEDED 且 BIND_NOW，LD_PRELOAD 时未定义符号（open/write/signal…）无法解析 → init 起服务立即退出（init.svc=stopped）。修法：先造空 stub（`-Wl,-soname,libc.so`）再 `-Wl,--no-as-needed` 链进去。另：`x2d-speed-buff` 是 **oneshot**，用 `ctl.restart` 只会停不会起，必须 `ctl.stop` 再 `ctl.start`。](/system) remount ro 偶尔报 Device or resource busy，`cd /; sync` 后重试即可。
