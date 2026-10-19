---
id: 51
tags: dsh memory backup github launchd
pinned: false
created_at: 2026-10-19T02:58:36.430000+00:00
updated_at: 2026-10-19T02:58:36.430000+00:00
---

DSH 记忆 GitHub 备份系统（2026-10-18 搭好，仓库 github.com/hyf715/DSH-Backup，main 分支）：本地 ~/dsh-memory-backup/ 是 git 仓库，remote 用 HTTPS+PAT（token 嵌在 .git/config 的 remote URL 里，本地明文、不推上去）。export.py 以只读(mode=ro)连 ~/.dsh/memory/memory.db，导出 memories/<id>-<slug>.md（带 id/tags/pinned/时间戳 front matter）+ memories.jsonl（恢复用）+ 拷贝 ~/.dsh/skills/。backup.sh = 导出→git add→有变更才 commit→push origin HEAD（无变更跳过，push 失败不致命下次重试）。launchd 任务 com.huangyingfeng.dsh-memory-backup（~/Library/LaunchAgents/）**每天凌晨 01:00** 跑（用户指定，已从最初 03:30 改过来），日志 ~/.dsh/memory-backup.log。手动触发：bash ~/dsh-memory-backup/backup.sh。注意：时间戳在 DB 里是毫秒（export.py 已兼容）；推送走 HTTPS token 而非 SSH（用户 SSH key 未注册 GitHub）。恢复时 memories.jsonl 可反向导入 SQLite。
