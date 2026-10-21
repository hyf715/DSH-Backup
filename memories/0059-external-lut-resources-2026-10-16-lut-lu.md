---
id: 59
tags: lut resources x2d verified
pinned: false
created_at: 2026-10-21T00:47:19.286000+00:00
updated_at: 2026-10-21T00:47:19.286000+00:00
---

[external-lut-resources 2026-10-16 核实] 外部 LUT 资源核实结论（详见 ~/lut-lab/EXTERNAL-LUT-RESOURCES.md）：① LeicaLab (Rla102277/LeicaLab) 9 款 17³ cube 已三线性上采样为 33³，就绪于 ~/lut-lab/leicalab_33/ 和 ~/Desktop/leica-luts/leicalab-9款/（Soft/Hard/Zone Mono、Olive、Dusk、Slide、Tungsten、Pastel、Sunny，MIT，相机实测误差 4-8 codes），可直接拷入 X2D /system/etc/x2d-lut/ 用；② Nikon-Recipes (shouryan01) 142 款 NP3/NCP 真实但需写 NCP→cube 转换器（NCP 是 XML 参数格式；含 Leica STD/Vivid、Kodachrome、Portra 系列）；③ Fotufilm (DhaliwalX/fotufilm-engine) 官方**无 .cube 导出**（只有 PNG/JPEG/WebP/TIFF），简报"导出 33/65 阶 cube"说法不实，要 cube 需自写色阶 ramp 渲染烘制；④ Spektrafilm-android 仅参考。通用重采样工具：~/lut-lab/resample_cube.py（用法 resample_cube.py in.cube out.cube [size]）。
