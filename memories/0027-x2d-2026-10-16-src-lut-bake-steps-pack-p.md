---
id: 27
tags: x2d step4 steps-pack userlut report
pinned: false
created_at: 2026-10-16T01:53:49.731000+00:00
updated_at: 2026-10-16T01:53:49.731000+00:00
---

X2D 取景步进包转原厂基底复合（2026-10-16 完成）：新增 src/lut/bake_steps_pack.py（--cubes --out --base --steps，生成 lut-hw-steps 格式 000..100 步进 bin）；cube_hw_bake.py 支持 --base/--mix（base=None 时 identity 基座 mix=0 输出恒等、mix=1 输出纯 cube，需在 bake 内对 u/v/w 也做 mix 混合否则 000 步错误）。全量 609 个（29 LUT×21 步）原厂基底复合包已生成 /tmp/lut-hw-steps-stock.tgz：000= lcdc_stock_base.bin 逐字节、100= Cube(Stock(x))、中间步= (1-w)Stock+w·Cube(Stock) 线性插值精确（≤1LSB）。注意：纯蓝输入 t=3840 在 100 步从 4095 降到 ~1465 是黑白胶片的正常拉灰（Cube(Stock(蓝)) 结果），非错误。librcam userlut 热更通道已定位：iq 命令组（[load [json file] | reload | userlut [lut_file] [lut_type] [lut_size]]）走 star-bus注册（cam_container_star_bus_register_cmd_process，PLT stub @0x36360，5 处调用点 @0x83fb4/0x84214/0x84244/0x84570/0x845a0），设备有 dji_mb_ctrl/duss_shell 潜在入口但精确 cmd_set/cmd_id 未锁定（需 ghidra 级或枚举探针）。子代理A独立报告 /tmp/pivot/REPORT-STRUCTURE.md 与字节级验证互证：672 hex 行=lcdc0/1(297×2)+main(33)+pyra0/1/2(15×3)，第673条是 main_blc.vbl_fpn_sw 零填充干扰项；每行 2048 u32 token lo16先/hi16后 各装 12bit；平面序[B',G',R']、idx=R+16G+256B；数据只在 data[0] global 实例；main==lcdc old-hw/liveview 组逐 token 相同；成片链 3DLUT 在 GTM 后(YUV域)、3FR 重处理链在 R2Y 前(RGB域)；pyra 5 档案 axis=[lut3d]。jsonc2json.py 已修尾逗号跨空行正则+大写0X两bug。
