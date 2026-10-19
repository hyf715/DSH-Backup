---
id: 23
tags: x2d lut watch.sh speed-buff pipeline
pinned: true
created_at: 2026-10-15T12:03:41.476000+00:00
updated_at: 2026-10-15T12:03:41.476000+00:00
---

X2D 方案 B「取景/成片双通道直出」现状（2026-10-15 部署）：取景通道 = speed-buff worker 在 lut_select/lut_on 时把 /data/local/tmp/lut-hw/<id>.bin 拷成 /data/local/tmp/active_lut.bin（lut_off 删除恢复原厂），lut_select/lut_on/lut_off 同时写 /blackbox/x2d-play-lut.preference；成片通道 = watch.sh（init 服务 x2d-lut-watch）检测新 JPG/3FR → patch_3fr（改 3FR 内嵌预览，回放所见）→ JPG 预览直出（复用套好色的 3888×2918 预览覆盖 DCIM 同名 JPG，~2s，不做 100MP 全尺寸烘焙）→ **最后** setprop ctl.restart camera-storage 清回放缓存 → 标记 PROCESSED。顺序必须是"CACHE-CLEAR 在所有文件写入之后"，否则新起的 camera-storage 会缓存旧图，回放显示未套色。
