---
id: 37
tags: x2d grmod menu pitfall qml
pinned: true
created_at: 2026-10-16T11:46:05.531000+00:00
updated_at: 2026-10-16T11:46:05.531000+00:00
---

[x2d 耍起菜单消失的坑 2026-10-16] **每 boot camera-gui 只能挂载一次原生菜单**：libx2d_native_menu.so 的 constructor 用 `open("/tmp/x2d-native-menu-attempt", O_CREAT|O_EXCL|O_WRONLY)` 做防崩保护——文件已存在则 `status("SKIPPED_RETRY")` 直接 return，不注入菜单树 → **"耍起/Tweaks" 入口整条消失**（回退原厂）。所以**同一 boot 内第二次 `setprop ctl.restart camera-gui` 会让耍起菜单没了**！【恢复】必须清掉 /tmp/x2d-native-menu-attempt（/tmp 是 tmpfs，**重启相机即清**），再启 camera-gui。【难点】adb shell（su 域）**删不掉**该文件：rm/mv/truncate/chmod 全 Permission denied（SELinux 域隔离），`runcon u:r:hbl_camera_service:s0` 也被拒（Cannot set context: Permission denied）。只能靠①整机重启（/tmp tmpfs 清空，最可靠），或②借同域进程代删（x2d-lut-watch 或 x2d-speed-buff 的 worker 都跑在 u:r:hbl_camera_service:s0，可在脚本里加一次性 `rm -f /tmp/x2d-native-menu-attempt`，用 /blackbox 标记文件 gate）。【部署 QML 的正确姿势】改 /system/etc/X2d*.qml 后要么先清标记再重启 camera-gui，要么直接整机重启——**不要连续两次 ctl.restart camera-gui**。preload 状态写在 /tmp/x2d-native-menu-preload.status（DISABLED/SKIPPED_RETRY/BUILD_MISMATCH/FEATURE_MASK_INVALID 等）。
