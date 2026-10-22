---
name: x2d-album-register-new-file
description: X2D 相册新增/替换照片文件的正确登记协议——新文件落盘后必须 ctl.restart camera-storage 触发扫描 + dbus browse 登记，否则成为索引外孤儿导致 MD5 校验/导出失败
whenToUse: 在 X2D 100C（4.2.0）上机内后处理新增/替换 DCIM 照片（再签名、滤镜烘焙、红晕/HDF 副本），或排查"文件存在但相册不显示 / 导出 MD5 校验失败"时
metadata:
  authoredBy: dsh-self-evolve
  updatedAt: 2026-10-22T03:51:28.426Z
  version: 1
  createdAt: 2026-10-22T03:51:28.426Z
---

# X2D 相册登记协议（新增/替换 DCIM 照片的正确姿势）

2026-10-22 实机验证（X2D 100C 4.2.0，B9008123 红晕副本登记成功）。

## 根因：双图并存/替换为什么会 MD5 报错
- camera-storage 维护相册索引（CacheItem）；新文件落盘后不触发索引 = "索引外孤儿"
- `ctl.restart camera-storage` 单独用：只重启服务，**不保证**新目录被扫描登记
- `dbus browse` 单独用：对**已有索引**的目录有效；对**手工新建的 DCF 目录**返回空数组
- **两者都有才是闭环**：restart 触发扫描 → browse 确认条目

## 正确流程（实测通过）
```sh
# 1. 落盘到独立 DCF 目录（3位数字+HASBL，如 998HASBL），B+7位编号
D=/mnt/media_rw/ssd/DCIM/998HASBL
mkdir -p $D; chown media_rw:media_rw $D; chmod 770 $D
(set -C; cat /data/local/tmp/redhalo.jpg > $D/B9008123.JPG.partial)  # 独占防半写
cmp src $D/B9008123.JPG.partial && mv $D/B9008123.JPG.partial $D/B9008123.JPG
chown media_rw:media_rw $D/B9008123.JPG; chmod 770 $D/B9008123.JPG

# 2. ★触发扫描（必须先 restart）
setprop ctl.restart camera-storage; sleep 4

# 3. ★登记 + 校验（必须 grep 到文件名，不能只看 rc）
/system/bin/dbus-send --system --print-reply --reply-timeout=5000 \
  --dest=com.hasselblad.storage /storage com.hasselblad.storage.browse \
  string:/ssd/998HASBL int32:0 > /tmp/browse.log
grep -q 'B9008123' /tmp/browse.log   # 必须命中，否则登记没成功
```

## 验证登记的 browse 返回（成功样例）
```
dict entry("display_path" string "/ssd/998HASBL/B9008123")
dict entry("full_path"    string "/mnt/media_rw/ssd/DCIM/998HASBL/B9008123.JPG")
dict entry("name"         string "B9008123")
dict entry("type"         int32 4)   # CacheItemInfo: 1=3FR, 4=JPG, 6=HEIC
dict entry("size"         int32 25235749)
dict entry("persistent"   boolean true)
```

## 关键陷阱
- **命令长度 231B 上限**：工厂 factory_shell / adb shell 长命令报 `command is too long`，必须拆成多条短命令分步执行
- **路径前缀**：browse 用 `/ssd/DCIM/...` 的简写 `/ssd/<DIR>`；full_path 返回真实 `/mnt/media_rw/ssd/DCIM/...`
- **type 优先级**：同名 3FR/JPG 相册项优先 3FR（官方 CacheItem::bestFile）——副本必须独立编号，不能与原图同名
- **新目录命名**：必须是 `[1-9][0-9]{2}HASBL`（100-999），避开相机滚动目录编号
- SELinux 上下文自动继承 exfat:s0，无需手动 chcon；属主必须 media_rw:media_rw

## 验证成功 = browse 返回含该文件名条目（不能只看 rc/退出码）
