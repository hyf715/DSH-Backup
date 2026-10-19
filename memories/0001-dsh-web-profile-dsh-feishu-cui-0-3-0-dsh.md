---
id: 1
tags: deploy dsh plugin
pinned: false
created_at: 2026-10-07T01:26:27.077000+00:00
updated_at: 2026-10-07T01:26:27.077000+00:00
---

DSH 插件部署（本机 web profile）：dsh-feishu-cui@0.3.0、dsh-memory@0.1.0、dsh-self-evolve@0.1.0 已装在 ~/.dsh/profiles/web。后两者是为 DSH 0.1.x 写的，本机是 0.2.0-rc.2，靠 allow-version 精确豁免装上（豁免记录在 plugin manager，仅对这两个包+这个 DSH 版本有效）。飞书凭据存在 ~/.dsh/.credentials.yaml 的 FEISHU_CUI_APP_ID / FEISHU_CUI_APP_SECRET。
