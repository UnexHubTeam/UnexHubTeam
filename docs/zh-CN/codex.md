# Codex

<!-- DOCS-NAV:START -->
[English (primary)](../en/codex.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）选择直连或本地转换](#section-1)
2. [2）配置自定义服务商](#section-2)
3. [3）设置 API Key](#section-3)
4. [4）启动和使用](#section-4)
5. [5）多配置与常见问题](#section-5)
6. [6）查看调用与计费](#section-6)
7. [参考资料](#section-7)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页对应命令行工具中的 Codex 接入指南。首次安装见 [GPT-codex 安装教程](codex-install.md)。

<a id="section-1"></a>
## 1）选择直连或本地转换

当前官方配置参考中，`wire_api` 仅支持 `responses`。当 UNEXHub 为目标模型开放 `/v1/responses` 时，可使用下面的直连配置。该端点本次未实测。

如果 UNEXHub 只提供 `/v1/chat/completions`，可通过 [CC Switch 本地路由](cc-switch.md)转换。不要将 `wire_api` 改成 `chat`，也不要把 `base_url` 写成完整聊天端点。

<a id="section-2"></a>
## 2）配置自定义服务商

编辑用户级 `~/.codex/config.toml`（Windows 为 `%USERPROFILE%\.codex\config.toml`），合并以下设置：

```toml
model_provider = "unexhub"
model = "YOUR_RESPONSES_MODEL_ID"

[model_providers.unexhub]
name = "UNEXHub"
base_url = "https://api.unexhub.ai/v1"
env_key = "UNEXHUB_API_KEY"
wire_api = "responses"
requires_openai_auth = false
```

替换模型 ID，确保 `model_provider` 与 `[model_providers.unexhub]` 一致。服务商和鉴权配置放在用户级文件，不依赖项目级配置来覆盖。

<a id="section-3"></a>
## 3）设置 API Key

macOS / Linux：

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
```

Windows PowerShell：

```powershell
$env:UNEXHUB_API_KEY = "YOUR_API_KEY"
```

这是当前会话设置；需要长期保存时使用用户环境变量或密钥管理工具。仅设置 `OPENAI_API_KEY` 不会填充本示例指定的 `UNEXHUB_API_KEY`。

<a id="section-4"></a>
## 4）启动和使用

进入项目目录，任选一种运行方式：

```bash
codex
```

单次执行：

```bash
codex exec "Reply with one short greeting. Do not read or modify files."
```

临时指定另一个已开放模型：

```bash
codex --model YOUR_RESPONSES_MODEL_ID
```

Windows npm 安装若遇到脚本策略拦截，将以上 `codex` 替换为 `codex.cmd`。不同模型的推理参数、图片输入和工具能力可能不同，首次连通后再按模型说明启用。

<a id="section-5"></a>
## 5）多配置与常见问题

需要多个服务商时，分别定义不同的 `[model_providers.<id>]`，并正确选择 `model_provider`。官方当前版本的独立 profile 文件格式与旧版不同；使用 profile 前查阅官方高级配置，不复制旧的 `[models]` 路由示例。

401：检查本终端是否设置了 `UNEXHUB_API_KEY`。404：检查 `/v1` Base URL 和 Responses 支持。参数不支持：先移除额外推理参数并确认模型能力。模型未列出：检查准确 ID；CC Switch 转换模式下更新模型映射后重新启动 Codex。

<a id="section-6"></a>
## 6）查看调用与计费

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

<a id="section-7"></a>
## 参考资料

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Provider configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：安装 Codex](codex-install.md) · [中文目录](README.md) · [下一篇：CC Switch →](cc-switch.md)
<!-- DOCS-PAGER:END -->
