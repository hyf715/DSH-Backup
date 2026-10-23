---
id: 63
tags: x2d halation cinestill postprocess phocus 4k-align
pinned: false
created_at: 2026-10-23T11:59:15.807000+00:00
updated_at: 2026-10-23T11:59:15.807000+00:00
---

X2D 机内 CineStill 红晕后处理**定型方案**（2026-10-23 真机验证通过，hyf715/Hasselblad-LUT commit 8878cbb）：双路落盘——① 100HASBL/B9xxxxxx.JPG = 红晕成片（该目录无 3FR 遮挡，相机回放/放大读 JPG 主图→红晕可见；Phocus 下载红晕）；② 116HASBL/B9xxxxxx.JPG 原地替换为红晕（与 3FR 配对，相机回放 100% 强制读 3FR→天然显示原图，满足"老图可查看"）；③ 3FR 一个字节不动；④ 原 JPG 备份 /data/local/tmp/halo-jpg-bak（留 3 张）。关键三坑：A) **Phocus/Wi-Fi 下载走 O_DIRECT，JPEG 文件长度必须 4096 整数倍**，否则"缩略图可见、全图下载失败"——脚本里必须 truncate -s $(( (sz+4095)/4096*4096 )) 强制兜底（部署的 C 二进制可能是旧版未含对齐）；B) 3FR+JPG 同名配对时机内回放只读 3FR（CacheItem::bestFile 优先类型 1），替换 JPG 对机内回放无效；C) 绝不 dd 改 3FR（dd 默认 O_TRUNC 截断尾部→"下载图像失败"）。脚本路径 /system/etc/x2d-lut/halo-watch.sh（final-watcher，0.8s 轮询+水位线+browse 100HASBL 刷新索引）。
