# Security / 安全报告

请不要在公开 issue 中贴出 token、cookie、API keys、`Rh-Comfy-Auth`、`cos_url` 签名参数、用户 ID、隐私素材及服务器凭据。

发现敏感信息泄露时：先在相关平台撤销/轮换凭据，再通过 GitHub 仓库所有者可用的非公开联系方式反馈。如果没有非公开联系渠道，请在问题被确认前不要公开传播可利用的秘密字符串。

本仓库只应包含静态 JSON、Markdown、Python 校验脚本。`.gitignore` 无法清除**已经提交的 Git 历史**中的秘密；出现泄露必须额外清理历史并轮换凭据。
