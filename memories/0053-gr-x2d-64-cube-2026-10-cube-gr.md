---
id: 53
tags: x2d ricoh-gr 3d-lut research
pinned: false
created_at: 2026-10-20T00:49:13.599000+00:00
updated_at: 2026-10-20T00:49:13.599000+00:00
---

理光 GR 滤镜 → X2D 64³ .cube 移植调研（2026-10 实网核实）：① 现成 .cube 没有 GR IV 原厂数据，全是第三方仿制——bonyback1/sony-pmca-ricoh-mod 有 4 个 .CUB（GRPOSI/GRNEGA/GRBW/GRXPRO，Apache-2.0，~133KB 推测 17³ 网格需插值到 64³）；cubelut.cn 与 rilongbao.cn 是同一平台镜像（作者 Tiger，17 款"理光"LUT，免费注册可下但页面声明禁二次分发，Rec.709/LOG 双版本）。② GR IV 原厂路线的钥匙是 Maxwooow/Ricoh-GRMod（GPL-2.0，GR IV 固件 1.11）：core/src/color/camera.ts 给出 Image Control 完整模型 display=curve_c(S(M1·S⁻¹(std)))，M1 Q13 + 17-knot 曲线 + P2 后置 Q9，Cinema Yellow=style 18、Cinema(Green) 之后是 34..39，look 可用性表 0x53dbf36c（含 Monochrome 列，6 款黑白名由 lemonadesaltbagel/GR4-MonoUnlock 确认：Standard/Solid/Soft/High Contrast/Grainy/HDR）。③ judge00/gr3-look-editor（MIT）是 GR III 系（2.10/1.60）同款思路 + spektrafilm-lut.py 渲染 LUT 工具模板。④ Reddit r/Lumix 1s5sxbv 真实存在：GR II POSI 是 luma 驱动三次多项式+饱和度 LUT（S=0.939×f(L)）非简单 RGB LUT，公式在正文无下载文件。
