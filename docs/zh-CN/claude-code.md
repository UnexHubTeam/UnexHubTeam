# Claude Code

[English (primary)](../en/claude-code.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

Claude Code 是终端编程助手。本页说明通过 UNEXHub 的持久配置、启动、模型选择及计费核对；首次安装见 [Windows / macOS 安装教程](claude-code-install.md)。

## 1）确认协议与接入信息

需要 Anthropic Messages 兼容网关、有效 Key 和可用模型 ID。UNEXHub 的该协议尚未实测；先核对[兼容说明](compatibility.md)，或使用 [CC Switch](cc-switch.md)转换已支持的 Chat Completions 接口。

## 2）方式一：当前终端临时配置

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

替换占位符。临时变量只影响此终端及其启动的程序，关闭终端后需要重新设置。

## 3）方式二：用户级配置文件

编辑 `~/.claude/settings.json`，Windows 对应 `%USERPROFILE%\.claude\settings.json`。将以下内容合并到已有 `env` 对象中：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.unexhub.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CLAUDE_MODEL_ID"
  }
}
```

Base URL 使用根地址。Bearer 对应 `ANTHROPIC_AUTH_TOKEN`；若服务明确要求 `x-api-key`，改用 `ANTHROPIC_API_KEY`。删除或统一冲突配置，不要同时维护多套不同值。

如果需要覆盖 Opus、Sonnet、Haiku 别名，可按官方网关说明分别配置 `ANTHROPIC_DEFAULT_OPUS_MODEL`、`ANTHROPIC_DEFAULT_SONNET_MODEL`、`ANTHROPIC_DEFAULT_HAIKU_MODEL`。每个值都必须是已开放的模型 ID，辅助任务也可能使用这些模型并计费。

## 4）启动并验证

在项目目录执行：

```bash
claude
```

运行 `/status` 查看接入状态。发送「只回复一句问候，不读取或修改文件」验证连接，再开始实际编程任务。CLI 也支持非交互调用：

```bash
claude -p "Reply with one short greeting. Do not read or modify files."
```

## 5）使用与排错

需要恢复历史会话时使用 `claude --resume`；更换配置后重新启动 CLI。收到 401 时核对实际生效的密钥和鉴权方式；收到 Messages 路径或工具参数错误时，核对网关协议与模型能力。

普通文本调用成功不代表所有工具、长上下文或后台任务都受支持；先以所选模型与渠道的能力为准。

## 6）查看费用

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/9109750m0)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
- [Settings](https://code.claude.com/docs/en/settings)
