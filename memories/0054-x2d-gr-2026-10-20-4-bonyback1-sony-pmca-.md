---
id: 54
tags: x2d lut ricoh gr todo
pinned: false
created_at: 2026-10-20T01:11:52.307000+00:00
updated_at: 2026-10-20T01:11:52.307000+00:00
---

X2D 理光 GR 滤镜移植（2026-10-20）：已上车 4 款社区复刻（bonyback1/sony-pmca-ricoh-mod，Apache-2.0，17³ .cube 升采样到 64³）→ `gr_posi`(e773a40f)、`gr_nega`(92ca3204)、`gr_bw`(6965d4e6)、`gr_xpro`(1d4ef8b6)，manifest 37 款(`d7fdb9a1`)、HUD `52f14ae0`、controller `01078eee`，抽屉+自定义页已确认 37 款，commit 6060957 已推 main。**用户下一步：第二批补 Cinema Yellow/Cinema Green**。现状：全球无 GR IV 原厂提取的现成 .cube；精确路线 = 官方固件 fwdc248b.bin + Maxwooow/Ricoh-GRMod（GPL，含 slotInfo 解析 style 0x12/0x13 = Cinema Yellow/Green 的矩阵+曲线地址 + color/camera.ts 渲染管线 slotApply）；快速路线 = cubelut.cn/rilongbao.cn 同平台 17 款（免费注册+每款¥1，仅个人自用）。部署坑：多文件连续上传会互相覆盖（每次上传后必须立即 cp 到目标）；同一 reader 会话内串行上传比反复开关 USB 稳；改 /system/etc/X2d*.qml 后必须整机 reboot（camera-gui restart 杀注入）。
