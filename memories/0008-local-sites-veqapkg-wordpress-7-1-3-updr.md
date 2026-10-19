---
id: 8
tags: wordpress updraftplus googledrive proxy clash local-by-flywheel troubleshooting
pinned: false
created_at: 2026-10-12T04:13:30.611000+00:00
updated_at: 2026-10-12T04:13:30.611000+00:00
---

Local Sites/veqapkg (WordPress 7.1.3 / UpdraftPlus 1.26.8 / Local by Flywheel, localhost:10004) Google Drive 备份排查（2026-10-12）：根因不是慢而是完全传不上——PHP/libcurl 不读 macOS 系统代理，只认 http_proxy/https_proxy 环境变量（该机未设），所以 UpdraftPlus 裸连 googleapis.com 被墙，每个包在 Google/IO/Curl.php:120 烧 15s×3 重试后报 "failed to access parent folder"，0 字节上传。修法：wp-config.php 加 WP_PROXY_HOST=127.0.0.1 / WP_PROXY_PORT=7890 / WP_PROXY_BYPASS_HOSTS（googledrive.php 会映射成 CURLOPT_PROXY）；用 fsockopen 探测 7890 是否活着再 define，Clash 没开时自动退回直连不拖累 wp.org。关键环境事实：Clash Party 混合端口 127.0.0.1:7890；该机走代理是严重不对称——下载 2.8MB/s，上传仅 36KB/s（直连 Cloudflare 上行可到 1.26MB/s），所以 1GB 备份经代理要 ~8 小时。Local 的 MySQL 只能走 unix socket（127.0.0.1 会 ERROR 1130），socket 在 ~/Library/Application Support/Local/run/<siteid>/mysql/mysqld.sock；Local PHP CLI 在 lightning-services/php-8.2.29+0/bin/darwin-arm64/bin/php。CLI 里 require wp-config.php 会因 socket 路径报"Error establishing a database connection"，验证 WP 行为改走 web 路由（临时 php 放 webroot + curl localhost:10004）更可靠。
