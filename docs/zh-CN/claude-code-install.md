# Claude Code 安装教程（Windows / macOS）

[English (primary)](../en/claude-code-install.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页先安装 Claude Code，再配置 UNEXHub 网关。命令行日常使用见 [Claude Code](claude-code.md)。

> 接入条件：UNEXHub 为你的 Key 和模型提供 Anthropic Messages 兼容接口、流式响应与工具调用。本次已核对 Chat Completions 示例，尚未实测 Messages。先查[协议兼容说明](compatibility.md)；仅有 OpenAI 兼容聊天接口时，可使用 [CC Switch 协议转换](cc-switch.md)。

## 1）准备环境

使用 Windows 或 macOS 终端。Windows 原生安装建议安装 [Git for Windows](https://git-scm.com/downloads/win)，便于使用 Bash 工具；WSL 使用 Linux 安装命令。

官方原生安装方式无需预先安装 Node.js。若选择 npm 安装，当前官方说明要求 Node.js 22 或更高版本。

在 UNEXHub [创建专用 Key](quickstart.md)，例如 `claude-code-test`，确认余额、路由与预算。

## 2）安装 Claude Code

macOS / Linux / WSL：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

也可选择包管理器安装，两种方式任选一种：macOS 使用 `brew install --cask claude-code`；Windows 使用 `winget install Anthropic.ClaudeCode`。

重新打开终端，检查安装：

```bash
claude --version
```

## 3）配置 API 地址、Key 和模型

确认 Messages 已开放后，替换下面的占位符。Base URL 使用根地址，不添加 `/v1` 或 `/messages`。

macOS / Linux / WSL：

```bash
export ANTHROPIC_BASE_URL='https://api.unexhub.ai'
export ANTHROPIC_AUTH_TOKEN='YOUR_API_KEY'
export ANTHROPIC_MODEL='YOUR_CLAUDE_MODEL_ID'
claude
```

Windows PowerShell：

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.unexhub.ai"
$env:ANTHROPIC_AUTH_TOKEN = "YOUR_API_KEY"
$env:ANTHROPIC_MODEL = "YOUR_CLAUDE_MODEL_ID"
claude
```

本教程使用 Bearer 鉴权对应的 `ANTHROPIC_AUTH_TOKEN`。如果 UNEXHub 明确要求 `x-api-key`，改用 `ANTHROPIC_API_KEY`；同一配置中只保留实际需要的鉴权方式。`YOUR_CLAUDE_MODEL_ID` 必须替换为当前渠道可用的准确 ID。

## 4）验证首次对话

进入一个测试项目目录启动 `claude`。先运行 `/status`，确认网关地址和凭据类型，再发送「只回复一句问候，不读取或修改文件」。

返回文本只说明基本连接成功；代码编辑和 Agent 工作流还需模型支持工具调用。`/v1/messages` 的协议错误不能通过更换成 Chat Completions 路径解决。

## 5）保存配置，供下次使用

按 [Claude Code 配置教程](claude-code.md)将配置合并进用户级 `~/.claude/settings.json`。Windows 对应 `%USERPROFILE%\.claude\settings.json`。保留已有配置字段，不要将真实 Key 放入仓库文件。

## 6）查看计费

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

## 参考资料

- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
