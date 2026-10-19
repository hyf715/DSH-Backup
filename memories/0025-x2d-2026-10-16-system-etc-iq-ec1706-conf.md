---
id: 25
tags: x2d ec1706 isp lut native-pipeline
pinned: false
created_at: 2026-10-16T01:22:41.997000+00:00
updated_at: 2026-10-16T01:22:41.997000+00:00
---

X2D 成片色彩管线（2026-10-16 深挖确认）：运行时只读 /system/etc/iq/ec1706_config.bin（flatbuffer，非 json！dji_rcam.conf 指明 config_name），加载者 librcam.so（camera-service 内，DjiCamCfg_LoadCfgFile→_DjiCamCfg_LoadIQBinFile，共享内存）。成片链：main_ccm(3x3矩阵)→main_3dlut(lut_data: lerp_lut_mem_3d, 11档色温2400-10000K)→main_gtm(contrast_curve_r/g/b)→main_r2y→cfc→JPEG；pyra_3dlut0/1/2 管预览缩略图，lcdc_3dlut0/1 管取景显示。main_3dlut.lut_data 总量 67584 u32 = 11档 × 6144 u32(24576B = 3平面×4096×12bit，与 weston 24576B 硬件 LUT 完全同构，打包 u32=(高16位,低16位)各12bit，每档 24KB 原位覆写 = 注入点)。bin 内数据起点 0x17168c 等。librcam 自带官方热更通道：调试命令 [load json|reload|userlut lut_file lut_type lut_size] 走 star-bus（可达性未证实）。flatc -b 反编译重编会膨胀 6.7MB→39.6MB 不可取，注入必须原位覆写。
