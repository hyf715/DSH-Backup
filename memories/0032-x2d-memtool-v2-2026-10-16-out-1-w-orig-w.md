---
id: 32
tags: x2d lut axis-semantics composite
pinned: false
created_at: 2026-10-16T06:31:10.802000+00:00
updated_at: 2026-10-16T06:31:10.802000+00:00
---

X2D memtool v2 轴语义定案（2026-10-16）：复合公式 out=(1-w)*orig + w*LUT(orig) 的输入轴必须是颜色正确轴 (R'→r, G'→g, B'→b)——即从基底表取 st[2]（R'平面）、st[1]（G'）、st[0]（B'）作为 LUT 的 (r,g,b) 输入。注入器 ec1706_3dlut_inject.py 旧实现用 (B'→r) 轴是 R/B 互换 bug（黑白 LUT 无法暴露，彩色 LUT 会蓝红互换）；cube_hw_bake.py L128 (base[2],base[1],base[0]) 是正确的。修复后 memtool C 复合: main 11档 md5 1520f0a4、pyra 5档 md5 8a51a7ed、取景 active_lut（lcdc 基底+hp5@100）md5 219d8500（vs bake 33³ float 参考 e1177f5d 差≤25 LSB = 16³ 量化差）。设备/宿主双端 md5 全链路验证通过。
