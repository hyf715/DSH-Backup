---
id: 55
tags: dsh halogen flashnext timeout tailscale
pinned: false
created_at: 2026-10-20T08:33:21.730000+00:00
updated_at: 2026-10-20T08:33:21.730000+00:00
---

DSH 对 halogen(flashnext=halogen-qwen3.8-flash-next @100.75.181.46:8000)的"Request timed out"根因(2026-10-20): ①默认 streamIdleTimeoutMs=300000ms(5分钟, dsh-llm-pi-ai lib/index.js:911 的 DEFAULT_STREAM_IDLE_TIMEOUT_MS)、openai SDK 默认总超时 600s; ②halogen 服务器走 Tailscale DERP 中继(未直连, RTT 465-780ms), 大上下文(26万token)prefill 实测仅 56s、18万token 99s, 不至于撞 5 分钟——真正的超时触发是"连接无任何流式字节超 300s"(stream idle timeout), 常见于服务器恰好忙(slots=2 被占)+ DERP 抖动叠加; ③会话上下文膨胀(该会话曾 269260 tokens 超 262144 报 400)是放大器。修复: cordis.patch.yml 的 llm-pi-ai providers.halogen 加 timeoutMs: 900000 + streamIdleTimeoutMs: 900000(字段在 Config schema 里支持, MAX_TIMER_DELAY_MS=2147483647)。注意 llm-pi-ai 的 profileOptions 里 maxRetries: 0, 重试由外层 retryPolicy 控制(默认 5 次)。
