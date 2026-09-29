# UNEXHub Developer Documentation

Build with the UNEXHub API, configure supported clients, review billing, or publish an Agent.

使用 UNEXHub API、配置客户端、核对计费，或发布 Agent。

**[English documentation (primary)](docs/en/README.md) · [简体中文（辅助翻译）](docs/zh-CN/README.md)**

[Chat Completions API](docs/en/chat-completions.md) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [UNEXHub console ↗](https://unexhub.ai/)

> English is the primary documentation language. Simplified Chinese is maintained as a companion translation.
>
> Agent tutorial status: **Mode A · Platform-managed Dedicated Server remains a technical preview. Mode B · Cloudflare Container has an external-registry deployment workflow, with credential isolation and per-user persistence still pending.**

Updated / 更新: 2026-09-29

## Find the right guide / 精准查找

| Goal | English guide | 中文指南 |
| --- | --- | --- |
| Get an API key and make your first call | [Quickstart](docs/en/quickstart.md) | [快速开始](docs/zh-CN/quickstart.md) |
| Choose an API protocol and endpoint | [Protocols and endpoints](docs/en/compatibility.md) | [协议与端点](docs/zh-CN/compatibility.md) |
| Send an API request with cURL or Python | [Chat Completions API](docs/en/chat-completions.md) | [Chat Completions API](docs/zh-CN/chat-completions.md) |
| Set up Chatbox or Cherry Studio | [Client setup guides](docs/en/README.md#apps-and-editors) | [客户端配置指南](docs/zh-CN/README.md#apps-and-editors) |
| Set up Claude Code, Codex, or Aider | [Coding agent setup guides](docs/en/README.md#cli-and-coding-agents) | [编程 Agent 配置指南](docs/zh-CN/README.md#cli-and-coding-agents) |
| Review usage and export billing records | [Billing and usage](docs/en/billing.md) | [计费与用量](docs/zh-CN/billing.md) |
| Troubleshoot an issue | [Troubleshooting](docs/en/faq.md) | [故障排查](docs/zh-CN/faq.md) |

## Recommended paths / 推荐路径

### API integration

1. [Choose an integration](docs/en/getting-started.md)
2. [Create a key and make a first call](docs/en/quickstart.md)
3. [Confirm protocol compatibility](docs/en/compatibility.md)
4. [Use the Chat Completions API guide](docs/en/chat-completions.md)
5. [Review billing](docs/en/billing.md)

### Agent development

| Mode | Status | Documentation |
| --- | --- | --- |
| Mode A · Platform-managed Dedicated Server | **Technical preview** — real-node validation and entry security remain required; frontend ZIP upload is currently blocked. | [English guide](docs/en/agent-development-mode-a.md) · [中文指南](docs/zh-CN/agent-development-mode-a.md) |
| Mode B · Cloudflare Container | **Current external-registry workflow** — long-lived credential injection remains a barrier to safe third-party image releases; per-user persistence is not yet implemented. | [English guide](docs/en/agent-development-upload.md) · [中文指南](docs/zh-CN/agent-development-upload.md) |

Mode A users choose a whole-node specification before launch. Mode B developers select a container instance type that is locked when the version is published. Both modes currently treat container files as temporary data.

## Browse documentation / 浏览全部文档

| Section | English | 简体中文 |
| --- | --- | --- |
| Start here | [Getting started](docs/en/getting-started.md) · [Console walkthrough](docs/en/quickstart.md) · [Compatibility](docs/en/compatibility.md) | [快速开始](docs/zh-CN/getting-started.md) · [控制台操作](docs/zh-CN/quickstart.md) · [协议兼容](docs/zh-CN/compatibility.md) |
| API and account | [Chat Completions](docs/en/chat-completions.md) · [Routing](docs/en/third-party-routing.md) · [Billing](docs/en/billing.md) · [FAQ](docs/en/faq.md) | [聊天补全](docs/zh-CN/chat-completions.md) · [路由](docs/zh-CN/third-party-routing.md) · [计费](docs/zh-CN/billing.md) · [常见问题](docs/zh-CN/faq.md) |
| Apps and editors | [Chatbox](docs/en/chatbox.md) · [Cherry Studio](docs/en/cherry-studio.md) · [Cursor](docs/en/cursor.md) · [Windsurf](docs/en/windsurf.md) | [Chatbox](docs/zh-CN/chatbox.md) · [Cherry Studio](docs/zh-CN/cherry-studio.md) · [Cursor](docs/zh-CN/cursor.md) · [Windsurf](docs/zh-CN/windsurf.md) |
| CLI and coding agents | [Aider](docs/en/aider.md) · [Claude Code](docs/en/claude-code.md) · [Codex](docs/en/codex.md) · [CC Switch](docs/en/cc-switch.md) · [openclaw-cn](docs/en/openclaw-cn.md) | [Aider](docs/zh-CN/aider.md) · [Claude Code](docs/zh-CN/claude-code.md) · [Codex](docs/zh-CN/codex.md) · [CC Switch](docs/zh-CN/cc-switch.md) · [openclaw-cn](docs/zh-CN/openclaw-cn.md) |
| Agent development | [Mode A · Platform-managed Dedicated Server](docs/en/agent-development-mode-a.md) · [Mode B · Cloudflare Container](docs/en/agent-development-upload.md) | [模式 A · 平台托管独立节点](docs/zh-CN/agent-development-mode-a.md) · [模式 B · Cloudflare 容器](docs/zh-CN/agent-development-upload.md) |
| Reference | [Chat Completions API](docs/en/chat-completions.md) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) | [Chat Completions API](docs/zh-CN/chat-completions.md) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc) |

For the complete A–Z index and guided sequence, open the [English documentation home](docs/en/README.md) or [中文目录](docs/zh-CN/README.md).
