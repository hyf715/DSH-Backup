---
id: 22
tags: x2d lut cube bug bake
pinned: true
created_at: 2026-10-15T12:03:41.466000+00:00
updated_at: 2026-10-15T12:03:41.466000+00:00
---

.cube 文件行序（X2D LUT 工具链致命坑，2026-10-15 修复）：标准 .cube 是 **R 最快、B 最慢**，行索引 idx = r + N*g + N²*b（等价于 lut.c 的 LUTAT(b*S²+g*S+r)，也等价于 "red varies fastest"）。cube_hw_bake.py（.cube→硬件 24576B）早期误按 "R 最慢" 索引，导致输入 R/B 轴转置，取景出现蓝↔红；同一批 cube 的软件路径 lut.c 一直是对的，所以成片正常、取景异常。判定方法：对 6 种轴排列做"对角性打分"（胶片 LUT 近似对角），25 款彩色 cube 全部以 0.15~0.62 优势选中 RGB 序；纯色角点检查（idx=N-1 应是纯红输入）可快速判读。灰度 cube（hp5/trix400）分辨不出，取标准序无害。
