---
id: 52
tags: x2d lut deploy camera-gui injection
pinned: false
created_at: 2026-10-19T13:43:09.647000+00:00
updated_at: 2026-10-19T13:43:09.647000+00:00
---

X2D LUT 运维关键事实（2026-10-19 实测）：`setprop ctl.restart camera-gui` 会让 `LD_PRELOAD /system/lib64/libx2d_native_menu.so` 的注入链路失效——新进程里 .so 仍被映射（/proc/PID/maps 有），但 Bootstrap.qml 不再加载，菜单「自定义」模块与 LUT 抽屉同时消失，logcat 零输出；**只有整机 `reboot` 能可靠恢复注入**。所以凡改 /system/etc/X2d*.qml（HUD / Bootstrap / PlayPage / SpeedBuffController）都必须"部署→reboot→验证"，不要用 camera-gui restart。另：滤镜列表有两个独立来源——抽屉读 LutHud.qml 的 catalogExtension，菜单「自定义」页读 X2dSpeedBuffController.qml 的 lutCatalog，两者要同时更新否则数量不一致。设备现状（2026-10-19 收尾）：33 张 hw 表在 /data/local/tmp/lut-hw（29 原有 + ir_aerochrome 74e64092、ir_wood 598ebf97、leica_brass f080c58f、leica_chrome 31ebbbfe），manifest fab4aa73（33 款），HUD 78962b86，controller b3f6fe65，/system ro。
