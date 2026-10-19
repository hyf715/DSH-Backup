---
id: 46
tags: x2d keys hud probe
pinned: false
created_at: 2026-10-18T12:04:57.192000+00:00
updated_at: 2026-10-18T12:04:57.192000+00:00
---

X2D 实体键键码与可达性（2026-10-18 实机探测，logcat tag `X2D_HUD_KEY_DEBUG`/`X2D_LUT_KEY_TOGGLE`）：固件把 **AF-D 映射成字母 "D"（Qt key=68, scan=40）**、**AE-L 映射成 "L"（key=76, scan=46）**；波轮是 Key_Up/Down/Left/Right(16777235/37/34/36)。**可达性关键**：Qt Quick 键盘事件只发给有焦点的项及其祖先，所以这两个键只有在 LUT 抽屉展开（HUD 持焦点）时才能被 LutHud 的 Keys.onPressed 收到；抽屉收起时焦点在原生 `LiveView_root`，**AF-D 会被原生"对焦驱动"消费（不冒泡）**、AE-L 等也不到达 HUD。已排除：① QML `Shortcut{context: Qt.ApplicationShortcut}` 全局热键 —— 该静态 Qt 未编译 `QQuickShortcut`（camera-gui 二进制 0 命中），② 相机菜单自定义按键里**没有 AF-D**（只有 ISO/WB、M、滚轮点击、镜头控制环可改）。要拿真·全局物理热键必须在 C++ 层抢（`build_native_preload.py` 的二进制 QML 资源补丁路线，但它依赖的外部工具 `inspect_menu_resources.py` 本机已不存在）。
