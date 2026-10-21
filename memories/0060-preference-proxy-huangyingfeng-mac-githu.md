---
id: 60
tags: preference proxy git network
pinned: false
created_at: 2026-10-21T03:22:31.501000+00:00
updated_at: 2026-10-21T03:22:31.501000+00:00
---

[preference/proxy] 本机（huangyingfeng 的 Mac）访问 GitHub / 外网克隆要走本地代理 127.0.0.1:7890（Clash，端口实测 OPEN）。git 用法：`git -c http.proxy=http://127.0.0.1:7890 clone ...` 或 export https_proxy=http://127.0.0.1:7890。2026-10-21 用户明确提醒"克隆仓库记得走代理"；当时不走代理克隆 104MB 私有仓耗时约 9 分钟。
