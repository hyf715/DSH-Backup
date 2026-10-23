---
name: x2d-in-camera-halation-dual-output
description: X2D 100C 机内红晕后处理定型流程：双路落盘（100HASBL 红晕成片 + 116HASBL 原地替换 JPG）、脚本级 4KB 对齐（Phocus 下载）、绝不碰 3FR
whenToUse: 在 X2D 100C（4.2.0）机内做照片后处理（红晕/HDF/任何生成红晕 JPG 副本）并要满足：相机内可看效果、Phocus/Wi-Fi 可下载、原 RAW 安全、原图可查看时
metadata:
  authoredBy: dsh-self-evolve
  updatedAt: 2026-10-23T11:59:15.822Z
  version: 1
  createdAt: 2026-10-23T11:59:15.822Z
---

# X2D 机内红晕后处理（定型双路方案）

2026-10-23 真机验证通过（X2D 100C 4.2.0）。备份：hyf715/Hasselblad-LUT `src/halation/`。

## 相机死规矩（必须理解，否则白干）

1. **3FR+JPG 同名配对时，机内回放/放大 100% 强制读 3FR**（`CacheItem::bestFile` 优先类型 1）——替换 JPG 对机内回放**无效**，但天然满足"老图（原图）可查看"。
2. **Phocus/Wi-Fi 下载走 `O_DIRECT`（0x30000），文件长度必须 4096 整数倍**——否则"缩略图可见、全图下载失败"（`Httpd::sendFile` 严格比较返回长度）。
3. **`dd seek` 写 3FR 会 O_TRUNC 截断文件尾部**（尾部对齐填充丢失）→ 文件尺寸与 IFD 声明不符 → "下载图像失败"。**3FR 一个字节都不能碰**。

## 定型流程（双路落盘）

```
拍照（B9xxxxxx.3FR + B9xxxxxx.JPG，ISP 已套色）
  → halo-watch.sh（0.8s 轮询 + 水位线，仅 lut_id==cinestill800t 时工作）
  → lut-apply-hal v7 红晕处理（--no-lut --effect cinestill --grain 10，~40s/102MP）
  → 脚本级强制 4KB 对齐：pad=$(( (sz+4095)/4096*4096 )); truncate -s $pad
  → 双路：
       100HASBL/B9xxxxxx.JPG  ← 红晕成片（无 3FR 遮挡 → 机内看红晕 + Phocus 下载红晕）
       116HASBL/B9xxxxxx.JPG  ← 原地替换红晕（与 3FR 配对 → 机内回放读 3FR 显原图）
       116HASBL/B9xxxxxx.3FR  ← 不动
       /data/local/tmp/halo-jpg-bak/ ← 原 JPG 备份（只留 3 张防 /data 满）
  → setprop ctl.restart camera-storage + dbus browse /ssd/100HASBL 刷新索引
```

## 部署

```sh
cp lut-apply-hal /system/etc/x2d-lut/lut-apply-hal
cp halo-watch.sh /system/etc/x2d-lut/halo-watch.sh
setsid /system/bin/sh /system/etc/x2d-lut/halo-watch.sh >/dev/null 2>&1 < /dev/null &
```

## 关键陷阱清单

1. **4KB 对齐必须在脚本里做**（truncate 兜底）——C 二进制可能没含对齐（部署旧版），只靠二进制不可靠。
2. **输出目录用 100HASBL**：`[1-9][0-9]{2}HASBL` 格式 storage 能识别；编号必须 **小于当前最大拍摄目录**（相机按最大编号写新照片，100 < 116 不会被侵占）；不要用 `CineStill`（browse 失败）或 99xHASBL（会被相机侵占）。
3. **登记**：新目录（100HASBL）首次 browse 建立条目；重复 browse 已缓存目录不发现新文件，所以每次处理完 restart camera-storage + browse 100HASBL。
4. **EXIF/FlashPix 必须移植**：JPG 必须带 APP1 Exif + APP2 FlashPix，否则相册显示红色/下载失败。
5. **预览/缩略图是 FlashPix 原色**：相机全屏预览读内嵌缩略图（原图移植），放大/下载才是红晕主图。改 FlashPix 索引风险高（相机校验元数据），不建议。
6. **JPG 覆写要用 mv 原子替换 + 先备份原图**；覆写后 restart storage 刷新大小索引。

## 验证成功标准（真机）

1. 100HASBL 目录在相册可见，点开/放大**显示红晕**（无 3FR 遮挡）
2. 116HASBL 点开**显示原图**（3FR 优先）
3. Phocus/Wi-Fi 下载 100HASBL 红晕 JPG **成功**（4KB 对齐）
4. 3FR 大小/内容不变
5. `pgrep -f halo-watch` 单进程存活
