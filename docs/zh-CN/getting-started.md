# 快速开始

<!-- DOCS-NAV:START -->
[English (primary)](../en/getting-started.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）登录并准备余额](#section-1)
2. [2）创建 API Key](#section-2)
3. [3）选择模型与协议](#section-3)
4. [4）配置地址并发送请求](#section-4)
5. [5）查看计费记录](#section-5)
6. [参考资料](#section-6)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页帮助你选择接入方式并完成第一次「创建 Key → 调用 → 核对扣费」。详细界面截图见[站点操作指南](quickstart.md)。

<a id="section-1"></a>
## 1）登录并准备余额

进入 [UNEXHub](https://unexhub.ai/)，注册或登录。在[资金账户](https://unexhub.ai/console/topup)确认可用余额。

<a id="section-2"></a>
## 2）创建 API Key

打开 [API 密钥](https://unexhub.ai/console/token) →「创建 Key」。设置用途名称、有效期、渠道折扣和路由策略。创建后确认已启用，复制密钥，并按需设置预算上限。

![创建 API Key 的配置窗口](../../assets/create-key.png)

想走第三方上游时选择「第三方路由」。[第三方路由](third-party-routing.md)和第三方客户端是独立概念，不需要改用上游服务商的密钥。

<a id="section-3"></a>
## 3）选择模型与协议

打开[交易中心](https://unexhub.ai/market?tab=models)，复制当前可用的模型 ID。

| 用途 | 所需接口 | 教程 |
| --- | --- | --- |
| 代码调用或聊天客户端 | Chat Completions | [cURL / Python](chat-completions.md)、[Chatbox](chatbox.md)、[Cherry Studio](cherry-studio.md) |
| 终端编程 | OpenAI 兼容聊天接口 | [Aider](aider.md) |
| Claude Code 与其 VS Code 扩展 | Anthropic Messages，或本地转换 | [Claude Code](claude-code-install.md)、[VS Code](vscode-claude-code.md) |
| Codex | Responses，或本地转换 | [Codex 安装](codex-install.md) |
| 多工具配置与协议转换 | 取决于目标工具 | [CC Switch](cc-switch.md) |
| 个人 Agent | 所选模型的聊天／工具协议 | [openclaw-cn](openclaw-cn.md) |
| AI 编辑器 | 取决于自定义网关支持 | [Cursor](cursor.md)、[Windsurf](windsurf.md) |

Messages、Responses 与 CC MAX 的站点支持尚未实测或确认，查看[协议兼容说明](compatibility.md)后选择直连或转换模式。

<a id="section-4"></a>
## 4）配置地址并发送请求

SDK Base URL 为 `https://api.unexhub.ai/v1`；常规 Chatbox API Host 和 Cherry Studio 自动补全模式填写根地址 `https://api.unexhub.ai`。

按所选教程填写 Key 与模型 ID，发送一句简短问候。每种工具的地址格式不同，不要把同一个地址字段原样复制到所有工具中。

<a id="section-5"></a>
## 5）查看计费记录

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

连接失败先看[常见问题](faq.md)。需要完整安装教程时，返回[文档目录](README.md)选择对应工具。

<a id="section-6"></a>
## 参考资料

- [UNEXHub marketplace](https://unexhub.ai/market?tab=models)

<!-- DOCS-PAGER:START -->

---

[← 中文目录](README.md) · [下一篇：控制台完整操作 →](quickstart.md)
<!-- DOCS-PAGER:END -->
