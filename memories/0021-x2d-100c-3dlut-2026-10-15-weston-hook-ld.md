---
id: 21
tags: x2d 3dlut weston lut hardware
pinned: true
created_at: 2026-10-15T12:03:41.451000+00:00
updated_at: 2026-10-15T12:03:41.451000+00:00
---

X2D 100C 硬件 3DLUT 格式与取景实时套色（2026-10-15 实机定案）：weston hook（LD_PRELOAD libweston_lut_hook_dump.so，读 /data/local/tmp/active_lut.bin）在每次 duss_hal_display_plane_tdlut_set 时替换 DMA 数据，实现取景实时 LUT。数据 24576B = 3 平面 × 4096 个 u16 LE（12bit 有效），平面序 [B'][G'][R']（offset 0/8192/16384），平面内索引 t = R + 16*G + 256*B（R 输入最快）。关键陷阱：identity（R=G=B 恒等）与黑白 LUT 三通道等值，**无法暴露任何 R/B 通道错位**——只有高饱和彩色 LUT（如 velvia）才能验证通道映射；验证可用"纯色角点"（纯红输入应 R'≈4095）或与原厂 stock LUT 的平面-轴依赖签名对照（原厂 P0←B轴, P1←G轴, P2←R轴）。修改 active_lut.bin 后无需重启 weston，切换拍摄模式/重进取景触发一次 tdlut_set 即生效。
