---
id: 10
tags: x2d lut leica haldclut devkit argb
pinned: false
created_at: 2026-10-13T09:46:22.996000+00:00
updated_at: 2026-10-13T09:46:22.996000+00:00
---

[x2d LUT Leica 烘焙 + DevKit lut_demo 帧管线] 把 Lightroom Look 预设（含 Adobe 私有 r7400/RGBTable 密文）转成 .cube 的标准解法 = HaldCLUT 色卡烘焙，不要逆向密文：(1) `src/lut/hald_bake.py gen` 生成 512×512 中性恒等色卡（level=64, Q=8, 布局 R=x%L / G=y%L / B=tile_x+tile_y*Q）；(2) 用户在 Lightroom 里对色卡逐个套 Look、只套那一个、Look 强度 100%、导出 PNG(非JPEG)/sRGB/原尺寸；(3) `hald_bake.py extract` 读回成 .cube（.cube 顺序 red 最快：for b: for g: for r）。恒等自测 max err≈0.0019(8bit量化)，对渲染像素抽查 err=0.000000。工具在 ~/x2d-907-one-click-extension-toolkit/src/lut/hald_bake.py，纯 Pillow 无 numpy。6 款 Leica FOTOS 预设原文件在 ~/Downloads/LeicaFoto配置文件，导入手机LR/（classic/blue/Contemporary/eternal/selenium/Sepia）。注意：3D LUT 装不下 Clarity(局部对比)，色彩/色调忠实、局部微反差近似。

DevKit lut_demo（QEMU 帧动画 mock，非实时 lut-apply）：装在 ~/Library/Application Support/X2DII-DevKit/library/5ae67d16a24b00f9/payload-stage/apps/lut_demo/0_1_6/，bin/app 用 `frame_%02d.argb` 动态读帧（不硬编码帧数，fopen 失败即停），加帧即多循环。帧格式 = 1024×768 裸像素 **B,G,R,A（Wayland ARGB8888，alpha 在最后）**——写成 A,R,G,B 会 alpha 位置+红蓝全反。加/改帧要同步更新该目录 manifest.json 的 files[].sha256/size。GUI "请先编译应用" 报错 = 下拉框停在"内置 Hello 示例"(key=None)，要选 `lut_demo · 0_1_6` 再点"运行应用"（"编译应用"按钮只编译内置 hello Wayland 示例）。list_packages 从 payload-stage/apps 读、verify=False。现 demo 已 29 帧（00-22 原富士/LutSmith，23-28 Leica，统一底图 DSC06572）。
