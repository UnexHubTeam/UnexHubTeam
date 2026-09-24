# GPT-codex 安装教程

<!-- DOCS-NAV:START -->
[English (primary)](../en/codex-install.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）安装 Node.js（npm 安装方式）](#section-1)
2. [2）安装 Codex CLI](#section-2)
3. [3）创建 UNEXHub Key](#section-3)
4. [4）配置 API 服务商](#section-4)
5. [5）设置 Key 并启动](#section-5)
6. [6）验证并查询扣费](#section-6)
7. [参考资料](#section-7)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本教程安装 OpenAI Codex CLI，并将模型请求配置到 UNEXHub。日常命令和配置说明见 [Codex](codex.md)。

> 当前 Codex 的自定义服务商使用 Responses 协议。仅验证 `/v1/chat/completions` 成功，不能证明 Codex 直连可用。UNEXHub 的 `/v1/responses` 支持尚未实测；如仅提供 Chat Completions，使用 [CC Switch 本地路由](cc-switch.md)。

<a id="section-1"></a>
## 1）安装 Node.js（npm 安装方式）

从 [Node.js 官网](https://nodejs.org/en/download)安装当前 LTS，重新打开终端，确认 `node --version` 和 `npm --version` 能输出版本号。

<a id="section-2"></a>
## 2）安装 Codex CLI

macOS / Linux / WSL：

```bash
npm install -g @openai/codex
codex --version
```

Windows PowerShell：

```powershell
npm.cmd install -g @openai/codex
codex.cmd --version
```

Windows 使用 `.cmd` 入口可避免调用被 PowerShell 脚本策略拦截的 npm 包装脚本。macOS 已有 Homebrew 时，也可选择 `brew install --cask codex`，无需重复安装。

<a id="section-3"></a>
## 3）创建 UNEXHub Key

在 [API 密钥](https://unexhub.ai/console/token)创建 `codex-test` 等专用 Key，设定路由、有效期和预算。在模型详情确认 Responses 与工具调用支持，再复制模型 ID。

<a id="section-4"></a>
## 4）配置 API 服务商

打开用户级配置文件：macOS / Linux 为 `~/.codex/config.toml`；Windows 为 `%USERPROFILE%\.codex\config.toml`。不存在时创建目录和文件。

将以下配置合并进去，替换模型 ID。`model_provider` 必须与下面的表名 `unexhub` 一致；不要重复添加同名 TOML 键或配置节。

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

该直连示例仅适用于已开放的 Responses 网关。Base URL 写到 `/v1`，不要填写完整 `/responses` 路径。密钥通过环境变量读取，无需为此覆盖已有 `auth.json`。

<a id="section-5"></a>
## 5）设置 Key 并启动

macOS / Linux / WSL，在项目目录的终端执行：

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
codex
```

Windows PowerShell，在项目目录执行：

```powershell
$env:UNEXHUB_API_KEY = "YOUR_API_KEY"
codex.cmd
```

这些变量仅对当前终端及其子进程生效。需要长期保存时使用操作系统的用户环境变量或密钥管理方式，并重开终端。不要把实际密钥写入 GitHub。

<a id="section-6"></a>
## 6）验证并查询扣费

发送「只回复一句问候，不读取或修改文件」。确认返回结果后，继续按下面流程查询消费。登录 ChatGPT 和使用 UNEXHub Key 是不同接入方式，本教程通过自定义服务商读取 UNEXHub Key。

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

<a id="section-7"></a>
## 参考资料

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Provider configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：VS Code 中的 Claude Code](vscode-claude-code.md) · [中文目录](README.md) · [下一篇：Codex →](codex.md)
<!-- DOCS-PAGER:END -->
