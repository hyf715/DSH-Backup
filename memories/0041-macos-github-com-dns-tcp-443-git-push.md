---
id: 41
tags: 环境 git 网络 proxy x2d
pinned: false
created_at: 2026-10-17T00:01:50.710000+00:00
updated_at: 2026-10-17T00:01:50.710000+00:00
---

本机（macOS）访问 github.com 经常被墙：DNS 能解析但 TCP 443 不通，`git push` 会报 `Failed to connect to github.com port 443` / `curl 28`。本机 Clash 类代理监听 **127.0.0.1:7890**（可用），7891 不可用。绕行办法是一次性带代理，不改全局配置：`git -c http.proxy=http://127.0.0.1:7890 push <remote> <branch>`，`ls-remote` 同理。x2d-907 工具包仓库远端名是 `hyf`（https://github.com/hyf715/Hasselblad-LUT.git），主用分支 `hyf/feature/lut-phase1`；仓库已设 `http.version HTTP/1.1` 以避免 HTTP2 framing 报错。验证推送是否真成功要比对 `git ls-remote` 的 SHA 与本地 `git rev-parse HEAD`（只测可达性会误报）。
