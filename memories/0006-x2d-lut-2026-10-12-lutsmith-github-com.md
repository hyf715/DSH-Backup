---
id: 6
tags: hasselblad x2d lut lutsmith startup-studio reference
pinned: false
created_at: 2026-10-12T00:11:48.121000+00:00
updated_at: 2026-10-12T00:11:48.121000+00:00
---

X2D LUT 项目可复用的两个外部工具（2026-10-12 核实真实存在）：①LutSmith（github.com/Xkalin1990/LutSmith，单文件 HTML 离线跑，CC BY-NC 4.0）——能把 Lightroom 预设 .xmp/.lrtemplate 转成标准 .cube（tone/WB/curves/HSL/split-toning 会带过来，局部编辑/Clarity/Dehaze 丢弃），导出 17/33/65 点；自带胶片预设含黑白 Tri-X 400 和 HP5 Plus，可直接拿来当咱们 X2D 的黑白 LUT（比手搓 bw-film.cube 更专业）。用法：用户 Lightroom 调色→导 .xmp→LutSmith 转 .cube→喂给 lut-apply。②Hasselblad Startup Studio（github.com/radium-wang/hasselblad-startup-studio，Radium Wang 出品，MIT+Commons Clause）——X2D 100C/907X/CFV 100C 4.2.0 灰度开机图替换，其注入架构是咱们守护进程部署的安全范本：loader.S 机内资源读取+无效回原厂、首次原厂备份不可覆盖、事务式安装/恢复、保留原厂身份与键、USB 走 ADB+自写 C 桥(CRC/cookie)。注意它和咱们工具包同源（Radium Wang）。
