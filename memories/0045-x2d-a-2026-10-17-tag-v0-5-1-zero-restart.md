---
id: 45
tags: x2d isp hotwrite lut milestone
pinned: true
created_at: 2026-10-17T07:54:10.271000+00:00
updated_at: 2026-10-17T07:54:10.271000+00:00
---

X2D 零重启切滤镜（方案 A 内存热写，2026-10-17 实测，tag v0.5.1-zero-restart）：`memtool composite <pid> <lut_id> <intensity>` 用 len-prefix 锚点定位 camera-service 里 ec1706_config 的映射基址，直接写 `/proc/PID/mem`（main 11 切片 + pyra 5 切片，写完 verify）→ **取景与成片都立即生效，camera-service 全程不重启**（热写 ~0.3s 基址缓存命中时；冷启首次扫描 1~3s），实测日志 `[pyra2] write 122880B @0x... verify: OK` + `HIT main len-anchor`。这替代了"cfwrite+rename 后 ctl.restart camera-service"的 2 秒黑屏方案；写盘仍保留（只为下次开机 ISP 读盘）。当前流程：`/lut_view` 毫秒级改 active_lut.bin（取景即时）→ 1s 后 `/lut_select` 写盘+热写（成片即时）→ 1.6s 后 `/lut_commit` 优先热写、失败才回退重启（后台校验 pid 是否真换）。**注意**：会诊报告说的"官方 userlut 热载通道(star-bus)"在本固件**不存在**——`userlut`/`star_bus` 在 /system/lib64 与 /system/bin 全盘 0 命中（dji_mb_ctrl/duss_shell 存在但命令 id 需逆向）。另：提交链路曾只挂"抽屉收起"，导致切滤镜永远不提交；现在 HUD 有独立 commitTimer + worker status 里有"标记>5s 自动补提交"的安全网。
