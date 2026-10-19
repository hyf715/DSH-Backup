---
id: 5
tags: hasselblad x2d lut cross-compile ndk libjpeg
pinned: false
created_at: 2026-10-11T23:33:51.654000+00:00
updated_at: 2026-10-11T23:33:51.654000+00:00
---

X2D LUT 相机版交叉编译配方（已验证 QEMU guest PASS）：相机 libjpeg.so 是 libjpeg-turbo **v62**（不是 IJG v90！用错头文件会报 "Wrong JPEG library version: library is 62, caller expects 90"）。正确做法：用 libjpeg-turbo 2.1.5.1 的头文件 + 自写 jconfig.h（#define JPEG_LIB_VERSION 62 + BITS_IN_JSAMPLE 8 + HAVE_* ），用 Android NDK r27 编译：`aarch64-linux-android28-clang -O2 -I<libjpeg-turbo> -Wl,-dynamic-linker,/system/bin/linker64 lut-apply.c -L<提取的相机lib> -ljpeg -lm`。必须加 -Wl,-dynamic-linker,/system/bin/linker64（否则 zig/clang 默认静态无 INTERP，DevKit 校验拒绝）。相机 libjpeg.so/libm.so/libc.so 从固件 OTA 提取：ota.zip → brotli 解 system.new.dat.br → 按 transfer.list 组装 ext4 → dissect.extfs 的 ExtFS(io.BytesIO(img)).get('/lib64/libjpeg.so')（注意类名是 ExtFS 不是 extfs，无 mount()）。zig 0.17 编 android.28 报 "unable to provide libc"（缺 NDK 头），musl 静态虽能编但 DevKit 要动态 linker64，故最终用 NDK。
