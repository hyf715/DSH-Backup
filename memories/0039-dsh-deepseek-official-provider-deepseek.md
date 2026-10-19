---
id: 39
tags: dsh deepseek provider llm pitfall
pinned: false
created_at: 2026-10-16T23:34:34.999000+00:00
updated_at: 2026-10-16T23:34:34.999000+00:00
---

DSH 里 `deepseek-official` 是**内置 provider**，由自带插件 `@deepseek-ai/dsh-llm-deepseek-api-key`（patch 条目 id `llm-deepseek`）注册，走 **Anthropic Messages 协议**（baseURL 默认 https://api.deepseek.com/anthropic，x-api-key 认证，key 从 credentials 服务 DEEPSEEK_API_KEY 解析，可用 DEEPSEEK_BASE_URL 环境变量覆盖）。默认模型 DEFAULT_MODELS = deepseek-flash（V4.1-Flash，vision）+ deepseek-v4-pro。坑：① 不要再在 llm-pi-ai.providers 里声明同名 deepseek-official，否则插件注册报 "configurable provider deepseek-official is already declared"、配置重载失败、切模型报"联系不上"；② patch 里给 llm-deepseek 配 `models: []` 会把默认模型清空，应配 `config: {}` 用默认。2026-10-17 已按此修复：撤掉 llm-pi-ai 里的重复声明，llm-deepseek 改 config: {}，agent-default-model 指向 deepseek-official/deepseek-flash，dump-config 通过。halogen 服务器 cap 65536 的教训仍有效：deepseek-official 官方端点无此 cap（max output 393216）。
