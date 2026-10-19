---
id: 3
tags: hasselblad x2d lut architecture dev-plan
pinned: false
created_at: 2026-10-11T10:51:04.320000+00:00
updated_at: 2026-10-11T10:51:04.320000+00:00
---

X2D 机内 LUT 功能首选架构（用户认可的白皮书方案）：方案A=后台 Daemon 监听机内 JPEG 生成事件，用 C 程序按 .cube 3D LUT 映射覆盖 JPEG，3FR RAW 不动，零时序风险；取景实时 LUT（Qt GLSL shader）二期。注意：工具包实际注入机制是直接替换 /system 白名单文件 + /proc/PID/mem RAM 补丁（freeze/patch/verify/restore），不是 bind mount；400MP 像素位移应走原厂 Auto4/6/16 模式而非自驱 IBIS。
