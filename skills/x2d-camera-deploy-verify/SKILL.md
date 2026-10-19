---
name: x2d-camera-deploy-verify
description: Deploy files/services/LUTs to a Hasselblad X2D 100C over ADB or factory USB and verify them losslessly (md5, syntax, service state, on-screen check), including the SELinux, transport and cache pitfalls that break naive attempts.
whenToUse: Use when pushing scripts, binaries, LUT binaries or config to the X2D camera, restarting its init-managed services (x2d-lut-watch, x2d-speed-buff), or validating that a camera-side change actually took effect.
metadata:
  authoredBy: dsh-self-evolve
  updatedAt: 2026-10-16T23:54:19.665Z
  version: 6
  createdAt: 2026-10-15T12:03:53.177Z
---

# X2D 100C 部署与验证

## 0. 选择传输通道（先试 adb）
- `adb devices`：相机重启后 **adb 可能重新枚举**（不要假定永久失效）。可用时优先 adb（快、无损）。
- adb 不可用时用 factory USB（`x2d_play_software.reader()`）：
  - 命令长度上限 ~231B；输出经过非 ASCII 过滤 → **文本一律 base64 拉取**，不要直接 `cat`（中文注释会被吞字节，得到损坏的脚本基线）。
  - 二进制/大文件用 `adb push`；只能走 factory 时先 `tar czf` 压缩再分块 `echo <chunk> | base64 -d` 拼接。
- 退出码陷阱：`adb shell "cmd; echo rc=$?"` 里的 `$?` 会被**本地** shell 展开，得到的是 adb 的退出码。远程退出码必须写成单引号：`adb shell 'cmd; echo rc=$?'`。

## 1. 写 /system（ro 分区）
```
mount -o remount,rw /system
cp /data/local/tmp/new_file /system/etc/<dir>/<file>      # 覆盖已有文件 OK
chmod 755 /system/etc/<dir>/<file>
chcon u:object_r:system_file:s0 /system/etc/<dir>/<file>
sync; mount -o remount,ro /system
```
**SELinux 陷阱**：remount rw 之后，**覆盖已有文件可以**，但 `mkdir` / 新建 inode 会被拒（`Permission denied`，即使 uid=0）。新增目录/文件请放 `/data/local/tmp/`（例如 LUT 硬件 bin 目录就用 `/data/local/tmp/lut-hw/`），只把"必须替换的既有文件"写 /system。
- **`chcon` 在 adb 的 su 域必然 `Permission denied`**（uid=0 也一样，2026-10-17 实测）。覆盖已有文件时标签会自动继承（`ls -Z` 仍是 `u:object_r:system_file:s0`），所以 chcon 本可省略；**真正危险的是把它串进 `&&` 链**：`cp … && chmod … && chcon … && sync && mount -o remount,ro` 会在 chcon 处中断，导致 `sync` 和回 ro **都没执行**，文件看着已更新但 `/system` 被留在 rw。写法：`chcon … || true`，或把收尾拆成单独一条命令并 `mount | grep ' /system '` 复核。

## 2. 重启 init 服务（脚本/二进制改动后必须）
- init 托管的 `sh 脚本` 一旦启动就按旧代码解释执行：改文件后必须 `setprop ctl.restart <svc>`（如 `x2d-lut-watch`），否则跑的还是旧逻辑。
- **绝不** stop/start 或 kill `camera-gui`、`weston`、`camera-storage` 之外的相机核心；`camera-storage` 只允许 `ctl.restart`（stop/start 会卡在 stopped → "错误19 无法读取图片"）。`camera-gui` = 相机屏幕，碰它会黑屏。
- 校验：`getprop init.svc.<name>` 应为 `running`，再 `tail` 该守护的日志确认新配置被读到。

## 3. 验证（不要只看"命令没报错"）
1. `md5sum <device path>` 与本地 `md5 -q <local file>` 必须一致——有损传输过就会不一致。
2. `sh -n <脚本>` 在**设备真实 shell** 上做语法校验（本机 `bash -n` 不等于 mksh 通过）。
3. 服务状态 + 日志新行（例如守护启动后应打印新的 config 行）。
4. 功能验证若涉及 `worker` 这类脚本：**adb shell 的 SELinux 上下文不是 root 语义**，对 `0700` 的 root 目录执行 `chmod` 会失败，叠加 `set -eu` 直接非零退出 → 必须用 factory reader（root + `u:r:hbl_camera_service:s0`，与 server 子进程同域）调用，或走真实 HTTP 路径（`toybox nc 127.0.0.1 18763`，设备上没有 curl）。

## 4. 相机 LUT 特有事项
- 硬件 LUT：24576B，3 平面 × 4096 u16 LE，平面序 `[B'][G'][R']`，索引 `t = R + 16G + 256B`（R 最快）。软件路径 `lut.c` 用 `LUTAT(b*S²+g*S+r)`。
- `.cube` 标准行序 = **R 最快**（`idx = r + N·g + N²·b`）。烘焙器若按 R 最慢索引会把输入 R/B 轴转置 → 取景蓝↔红。
- **identity / 黑白 LUT 无法验证通道映射**（三通道等值），必须用高饱和彩色 LUT 或纯色角点（纯红输入 → R'≈4095）验证。
- 改 `/data/local/tmp/active_lut.bin` 后无需重启 weston：切换拍摄模式/重进取景触发一次 `tdlut_set` 即生效（hook 每次调用重读该文件）。
- 回放/传输的成片缓存：**所有文件写入必须在 `setprop ctl.restart camera-storage` 之前完成**，之后再标记 PROCESSED；顺序反了会让新起的 camera-storage 缓存旧图，回放/导出显示未套色。

## 4b. 交叉编译相机二进制（lut-apply 亲测配方）
- 必须用 **NDK clang（bionic）**：`/opt/homebrew/share/android-ndk/toolchains/llvm/prebuilt/darwin-x86_64/bin/aarch64-linux-android28-clang`。用 `zig cc -target aarch64-linux-gnu` 会链到 glibc，产物在相机上报 `CANNOT LINK EXECUTABLE ... library "libm.so.6" not found` 而不可用（**这个坑真实发生过：随包 lut-apply 就是这样坏掉的**）。
- **libjpeg 头必须是 v6b(62) ABI**：相机 `libjpeg.so` 是 `JPEG_LIB_VERSION 62`，用 Homebrew 的 v80 头编译会运行时 `Wrong JPEG library version: library is 62, caller expects 80`。做法：复制 jpeglib.h/jconfig.h/jmorecfg.h/jerror.h 到私有目录，把 jconfig.h 里 `#define JPEG_LIB_VERSION` 改成 62，`-I` 指向该目录。
- 链接期用"符号桩"libjpeg.so（只提供 undefined 的 `jpeg_*` 符号），运行期由相机 `/system/lib64/libjpeg.so` 解析；产物 DT_NEEDED 应只有 `libjpeg.so libdl.so libc.so`。**构建后应断言不含 libc.so.6/libm.so.6**。
- 新二进制上台前先放 `/data/local/tmp`（用 `adb shell` 测，它是 `u:r:su:s0` 可 exec）；**factory shell 的相机域不能 exec /data/local/tmp 下的文件**（秒退且无输出）。正式部署到 `/system/etc/x2d-lut/` 后由守护（`u:r:shell:s0`）执行 ✓。
- 计时：`adb shell` 是 su 域，读 `/proc/uptime` 会被拒（改用 mksh 的 `time`，输出 real/user/sys）；factory shell 是相机域，可读 `/proc/uptime` 但不能 exec /data/local/tmp 二进制——两者配合使用。
- 性能剖析法：编一个"空操作"变体（把热函数体清空）量地板值。lut-apply 实测 11.3MP：JPEG 解码+编码 ~1.36s，三线性插值浮点 ~1.6s / 整数版 ~1.2s；把 LUT 重采样到 17³（14.7KB 进 L1）**无收益**（说明是算力瓶颈，不是缓存）。

## 4c. 相机侧 .so（speed server / native menu）构建与部署
- **CPU 目标必须保守**：zig 默认目标会发出相机 CPU 不支持的指令 → 进程 **SIGILL 崩溃**（`dmesg` 里可见 `send_signal sig=4`，`/data/tombstones/tombstone_*` 有转储；`init.svc.<svc>` 变 stopped 且端口拒连）。实测有效的编译参数：`zig cc -target aarch64-linux-gnu -mcpu=generic -mno-outline-atomics -O2 -g0 -fPIC -shared -nostdlib -fno-stack-protector -fno-builtin -Wl,--strip-all -Wl,--no-undefined -Wl,-z,noexecstack -Wl,-soname,<name>.so` （仓库 brightness 构建里的 `-mno-outline-atomics` 就是同一原因的补丁）。注意 zig 用 `-mcpu=`，`-march=armv8-a` 不被接受。
- 链接期桩库：本机没有相机系统镜像（`X2D_SYSTEM_ROOT`）时，用"未定义符号清单"现造桩 `libc.so`（函数型 `void f(void){}`、对象型 `char f[8];`）并以**文件路径**传给链接器，产物才会带 `DT_NEEDED libc.so` ✓；否则 .so 无 DT_NEEDED（在 shell 里能预加载，但在 camera-gui 里可能行为不同）。
- **部署后不要用 `kill -9 $(pidof sh)`**：会把正在执行命令的 shell 自己杀掉，后续命令静默不执行（本次因此白跑一轮）。用具体 PID 或 `pkill -f '<唯一串>'`；且 factory shell 的 PATH 里可能没有 `awk`/`pkill`（`grep -c` 无匹配时返回 1，会让命令"失败"→ 加 `|| true`）。
- 服务是 `oneshot`：部署后 `setprop ctl.start x2d-speed-buff`（停掉时）或 `ctl.restart`；用 `getprop init.svc.<svc>` + 端口 LISTEN 条目（`/proc/net/tcp` 里 `0100007F:494B ... 0A`）双重确认 ✓。
- **先验证"已装产物"是否包含你依赖的功能**：`strings` 比对（例：旧 `libx2d_speed_server.so` 7600B 缺 `lut_select`/`notice_status`/`freeNoticeReady` → 菜单 LUT 永远切不了、UI 因 `freeNoticeReady` 恒 false 而整页置灰）。随包 `.app` 里两份陈旧产物（glibc lut-apply + 旧 speed server）就是这么来的 ✓。

## 4d. ec1706_config.bin 原生 ISP 注入（方案 D，已实机验证 2026-10-16）
- 靶点：`/system/etc/iq/ec1706_config.bin` 由 librcam 在 camera-service 启动时加载（读的是 bin 不是 json）；运行时读取 `dji_rcam.conf` 的 config_name。
- `main_3dlut.lut_data` @ 0x171688（len 前缀 67584 = 11 色温档 × 6144 u32），每档 24576B，u32 打包 (hi16,lo16) 各 12bit，平面序 [B'][G'][R']，t=R+16G+256B——与 24576B 硬件 LUT 同构，可直喂。
- `pyra_3dlut0/1/2.tlut` @ 0x770b4 / 0x9517c / 0xb3244（len 30720 = 5 档案 × 3 平面），缩略图/多级预览链，与 main 同构。
- 部署流程（已全程验证）：mount rw → cp 覆盖（覆盖已有文件 OK，不 mkdir）→ chmod 755 → chcon u:object_r:system_file:s0 → sync → remount ro；生效 = `setprop ctl.restart camera-service`（PID 变化即成功，无需整机 reboot）；回滚 = cp .orig 回去 + 重启。
- **验证新配置已加载的最快方法：让用户拍一张**（camera-service 重启后 3 秒内可拍），比查内存/日志都快。JPG+3FR+缩略图全黑白 = 全链路命中。
- 内存热写铺路教训（方案 E 未做）：**设备 mksh 的 `$((0x...))` 算术会把十六进制解析成 0**（dd skip 变负数）——所有地址必须先由宿主机算成十进制页号写死。需要扫 /proc/PID/mem 时用 NDK C 工具（maps→pread→memmem），不要 dd+xxd 循环：既慢又长时间独占 Factory USB 接口（互斥锁），期间其它 factory_shell 调用全部 Access denied。
- 备份习惯：出厂 bin 本地存档 + 设备 .orig 双备份；当场验证 md5sum 与本地一致。

## 5. 设备 shell / 工具语义陷阱（2026-10-15 实测）
- **toybox `dd` 编译时关闭了 conv**：`conv=notrunc` 直接报 `dd: conv option disabled` 并以 rc=1 退出（什么都写不进去！）。`oflag` 也不支持（`unknown operand oflag`）。用 `2>/dev/null` 会把这条错误吞掉，表现为"命令成功但文件没变"——**排查大文件写入时绝不吞 stderr**。
- 但 toybox `dd` **默认就截断输出**，因此"原地更新文件中间/末尾"可以这样做（已验证字节级一致）：
  `dd if=payload of=target bs=4096 seek=$((OFF/4096))` （写后文件正好 = OFF+payload_size）
  `truncate -s <原大小> target` （放大补零；实测 F2FS 上放大区为 0）
  比"复制整份 210MB 再 mv"快 ~100 倍（30ms vs 3.8s）。
- 计时**不要用 `date +%s%N`**：相机时钟会被步进，长耗时项会算出负值。用单调时钟 `cat /proc/uptime`，并在宿主机上算差值。
- 守护循环里对每个文件跑一次 `grep -qxF "$f" "$清单"` 是 O(n²)：670 个文件 × 30KB 清单 ≈ **11.3 秒/轮**，期间"看不见"新照片。改用**水位线**（记最大已处理文件名，只处理 `> 水位` 的；水位文件消失=换卡/格式化则清空重扫），并保留一次廉价成员校验兜底。
- factory shell 的文本抓取会串行/丢字符（多条 md5 行会被并成一行）——**要可靠结果就让设备写文件再 `adb pull`**（adb 可用时）。
- 权限分层：`adb shell` 是 shell 上下文，读不了 DCIM（media_rw）也 chmod 不了 root 0700 目录；SSD 上的操作、worker 脚本测试都必须走 factory reader（root + `u:r:hbl_camera_service:s0`）。`/data` 只有 ~336MB 可用，别在那里放 200MB 级临时文件，用 SSD。
