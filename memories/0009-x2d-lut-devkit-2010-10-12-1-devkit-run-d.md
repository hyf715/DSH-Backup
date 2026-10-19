---
id: 9
tags: x2d devkit lut fat16 venv troubleshooting
pinned: false
created_at: 2026-10-12T09:42:25.145000+00:00
updated_at: 2026-10-12T09:42:25.145000+00:00
---

X2D LUT DevKit 运行/部署关键坑（2010-10-12 排查）：(1) 跑 DevKit 脚本（run_demo_vm.py / run_app.py）必须用 DevKit 自带 venv `~/Hasselblad-X-System-QEMU-DevKit/.venv-mac/bin/python`，不能用 conda base 的 /usr/local/bin/python3，否则报 ModuleNotFoundError: brotli（venv 里有 brotli/PySide6/Pillow）。(2) QEMU 用 `fat:ro` 挂载 payload-stage，FAT16 上限 516MB；lut_demo 每版带 51-69MB 帧，多版累积（0_1_0~0_1_6 共 7 版=505MB）会顶爆，boot 时报 "Directory does not fit in FAT16 (capacity 516.06 MB)"，会话 starting→stopped 0 帧。prepare() 不重建 payload-stage，旧版是 install 累积的，删了就永久生效。修法：删 payload-stage/apps/lut_demo/ 下除激活版外的所有版本（激活版读 active-app.json 的 version）。(3) 桌面启动脚本已放 ~/Desktop/LUT-Demo-DevKit.command（双击启动 GUI，自动用对 venv+清旧版+杀残留 QEMU）。GUI 里点 Run app→选 lut_demo 看 23 款 LUT（11 富士+12 LutSmith）循环。
