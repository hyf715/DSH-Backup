---
id: 19
tags: dsh provider env troubleshooting
pinned: false
created_at: 2026-10-15T00:29:10.320000+00:00
updated_at: 2026-10-15T00:29:10.320000+00:00
---

dsh/pi-ai 解析 provider 密钥时 process.env 优先级高于 .credentials.yaml：若 shell 环境里有 DEEPSEEK_API_KEY=sk-none 之类的旧变量，会覆盖凭证库里的真 key，导致 401「API 密钥无效 AUTH」。2026-10-15 实锤：~/.zshrc 残留两段 halogen 工作站时代的环境变量导出（OPENAI_BASE_URL/OPENAI_API_KEY/DEEPSEEK_BASE_URL/DEEPSEEK_API_KEY=sk-none/DEEPSEEK_MODEL，均指向 100.75.181.46:8000），用户从终端启动 dsh web 时继承，deepseek-official provider 拿着 sk-none 请求 api.deepseek.com 被拒。已把 ~/.zshrc 中该段整块注释掉（保留注释说明）；配置文件还有 ~/.dsh/.credentials.yaml（真 key 一直在，curl 实测 200）。修复后必须用干净环境重启 dsh web：新开终端窗口，或先 unset OPENAI_API_KEY OPENAI_BASE_URL DEEPSEEK_API_KEY DEEPSEEK_BASE_URL DEEPSEEK_MODEL 再 nohup dsh web；重启会打断正在会话（agent 是其子进程），由用户手动执行。
