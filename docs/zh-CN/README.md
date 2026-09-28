# UNEXHub 开发者文档

[English documentation (primary)](../en/README.md) · 简体中文（辅助翻译） · [项目首页](../../README.md)

[聊天补全 API](chat-completions.md) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc) · [UNEXHub 控制台 ↗](https://unexhub.ai/)

> 本页是中文文档地图。使用 `Ctrl+F` 或 `⌘+F` 可按产品、协议、任务或错误码精准查找。

文档更新：2026-09-28

## 精准找到教程

| 目标 | 直接入口 | 完成结果 |
| --- | --- | --- |
| 第一次调用 API | [控制台完整操作](quickstart.md) | 创建 Key、选择模型、发起调用并找到扣费记录 |
| 选择正确协议 | [协议兼容说明](compatibility.md) | 确认工具需要 Chat Completions、Responses 还是 Messages |
| 使用 cURL 或 Python | [聊天补全 API](chat-completions.md) | 使用准确模型 ID 发起鉴权请求 |
| 配置桌面客户端 | [Chatbox](chatbox.md) · [Cherry Studio](cherry-studio.md) | 将 UNEXHub 添加为 OpenAI 兼容服务商 |
| 配置编辑器 | [Cursor](cursor.md) · [Windsurf](windsurf.md) | 核对当前版本是否支持自定义网关 |
| 配置编程 Agent | [Claude Code](claude-code.md) · [Codex](codex.md) · [Aider](aider.md) | 选择正确协议与 Base URL |
| 查看或导出费用 | [计费记录](billing.md) | 定位请求、核对最终扣费并导出记录 |
| 排查错误 | [常见问题](faq.md) | 排查 401、404、429、5xx、模型与路径问题 |
| 查看 Agent 开发文档 | [模式 A · 平台托管独立节点](agent-development-mode-a.md) · [模式 B · Cloudflare 容器](agent-development-upload.md) | 选择模式 A 技术预览流程，或构建、推送、配置、测试并提交模式 B 容器 |

## 推荐阅读顺序

1. [快速开始：选择接入方式](getting-started.md)
2. [控制台完整操作：创建 Key 并首次调用](quickstart.md)
3. [协议兼容说明](compatibility.md)
4. [聊天补全 API](chat-completions.md)
5. [第三方路由](third-party-routing.md)
6. [计费记录与导出](billing.md)
7. [常见问题与排障](faq.md)

之后可直接跳到所需客户端、编辑器、编程 Agent 或 Agent 部署指南。每个主题页都会显示文档分类、本页目录及上一篇／下一篇链接。

<a id="start-here"></a>
## 开始使用

1. [快速开始：选择接入方式](getting-started.md)
2. [控制台完整操作：创建 Key 并首次调用](quickstart.md)
3. [协议兼容说明](compatibility.md)

<a id="api-and-account"></a>
## API 与账户

4. [聊天补全 API](chat-completions.md)
5. [第三方路由](third-party-routing.md)
6. [计费记录与导出](billing.md)
7. [常见问题与排障](faq.md)

<a id="apps-and-editors"></a>
## 客户端与编辑器

8. [Chatbox](chatbox.md)
9. [Cherry Studio](cherry-studio.md)
10. [Cursor](cursor.md)
11. [Windsurf](windsurf.md)

<a id="cli-and-coding-agents"></a>
## 命令行与编程 Agent

12. [Aider](aider.md)
13. [安装 Claude Code](claude-code-install.md)
14. [Claude Code](claude-code.md)
15. [VS Code 中的 Claude Code](vscode-claude-code.md)
16. [安装 Codex](codex-install.md)
17. [Codex](codex.md)
18. [CC Switch](cc-switch.md)
19. [CC MAX 兼容性核对](cc-max.md)
20. [openclaw-cn](openclaw-cn.md)

<a id="agent-development"></a>
## Agent 开发

| 模式 | 状态 | 入口 |
| --- | --- | --- |
| 模式 A · 平台托管独立节点 | **技术预览。** 入口安全、拓扑验证与持久化等已知缺口在生产使用前必须闭环。 | 21. [独立节点开发指南](agent-development-mode-a.md) |
| 模式 B · Cloudflare Container | **已提供** | 22. [开发与上传指南](agent-development-upload.md) · [中文 PDF](../../assets/documents/agent-development-upload.zh-CN.pdf) |

模式 A 指南说明开发者交付契约及各拓扑的预览限制。模式 B 指南包含容器规范、阿里云镜像推送、平台部署、托管凭据、发布检查和故障排查。

<a id="api-reference"></a>
## API 参考

- [聊天补全 API 指南](chat-completions.md)
- [客户端与协议兼容说明](compatibility.md)
- [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)
- [UNEXHub 模型交易中心 ↗](https://unexhub.ai/market?tab=models)
- [调用日志 ↗](https://unexhub.ai/console/log)
- [资金账户 ↗](https://unexhub.ai/console/topup)

## A–Z 索引

[Aider](aider.md) · [CC MAX](cc-max.md) · [CC Switch](cc-switch.md) · [Chatbox](chatbox.md) · [Cherry Studio](cherry-studio.md) · [Claude Code](claude-code.md) · [Claude Code 安装](claude-code-install.md) · [Codex](codex.md) · [Codex 安装](codex-install.md) · [Cursor](cursor.md) · [VS Code](vscode-claude-code.md) · [Windsurf](windsurf.md) · [常见问题](faq.md) · [第三方路由](third-party-routing.md) · [计费](billing.md) · [聊天补全](chat-completions.md) · [快速开始](getting-started.md) · [模式 A Agent 开发](agent-development-mode-a.md) · [模式 B Agent 开发](agent-development-upload.md) · [控制台操作](quickstart.md) · [协议兼容](compatibility.md) · [openclaw-cn](openclaw-cn.md)
