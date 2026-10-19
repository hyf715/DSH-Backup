---
id: 40
tags: x2d lut verification weston-hook
pinned: false
created_at: 2026-10-16T23:54:19.678000+00:00
updated_at: 2026-10-16T23:54:19.678000+00:00
---

X2D LUT 取景链验证要点（2026-10-17 实测）：weston hook 的日志 /data/local/tmp/weston_lut_hook.log 是**带缓冲**写的，直接 tail 可能读到几十秒前的旧内容——曾因此误判"hook 在读缓存"。正确验证方式：比对日志里最新一条 `my_lut 0000:` 的前 16 字节与 /data/local/tmp/active_lut.bin 的 `od -An -tx1 -N16`，并等待 ≥10s；两者一致即说明 hook 已应用。写 active_lut.bin 后画面确实会在数秒内跟着变（用户肉眼确认：写 trix400@100 变黑白、写 velvia@100 变高饱和）。另外 /data/local/tmp/weston_lut_hook.log 每次 boot 只出现一条 `hook v2 installed`，可用出现次数判断该日志是否跨 boot。
