---
id: 49
tags: repo git x2d workflow
pinned: false
created_at: 2026-10-18T12:41:41.134000+00:00
updated_at: 2026-10-18T12:41:41.134000+00:00
---

X2D 工具包仓库（/Users/huangyingfeng/x2d-907-one-click-extension-toolkit）2026-10-18 收敛完成：**唯一开发分支 = `main`**（GitHub `hyf715/Hasselblad-LUT` 默认分支也已用 API 切成 main），`feature/lut-phase1` 已删除（本地+远端）；备份留在 `backup/local-main` 分支与标签 `backup-2026-10-18-pre-converge`、`v0.5.1-key-hardware`、`v0.5.1-zero-restart`、`v0.5.0-isp-direct`。两个 remote：`hyf`=本项目 GitHub（推送需 `http.proxy=http://127.0.0.1:7890`）、`origin`=上游 radium-wang/x2d-907-one-click-extension-toolkit。**坑**：该仓库原本是**浅克隆**（`.git/shallow`），推老历史/备份分支会报 `remote: fatal: did not receive expected object ... index-pack failed` —— 先 `git fetch --unshallow origin` 补全即可。GitHub 默认分支不改的话删不掉该分支（`refusing to delete the current branch`），可用 `git credential fill` 取到的 token 调 `PATCH /repos/<owner>/<repo>` 设置 `default_branch`。`.gitignore` 现在忽略 `*.bak-*` 与 `src/lut/lut-watch-v5.sh`。
