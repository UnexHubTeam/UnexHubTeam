# Claude Code

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/claude-code.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Claude Code is a terminal coding assistant. This page covers persistent UNEXHub configuration, startup, model selection, and billing. For installation, see the [Windows/macOS tutorial](claude-code-install.md).

## 1) Confirm the protocol and connection details

You need an Anthropic Messages-compatible gateway, a valid key, and an available model ID. This protocol has not been tested on UNEXHub. Check [compatibility](compatibility.md), or use [CC Switch](cc-switch.md) to convert a supported Chat Completions endpoint.

## 2) Option one: temporary terminal configuration

macOS / Linux / WSL:

```bash
export ANTHROPIC_BASE_URL='https://api.unexhub.ai'
export ANTHROPIC_AUTH_TOKEN='YOUR_API_KEY'
export ANTHROPIC_MODEL='YOUR_CLAUDE_MODEL_ID'
claude
```

Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.unexhub.ai"
$env:ANTHROPIC_AUTH_TOKEN = "YOUR_API_KEY"
$env:ANTHROPIC_MODEL = "YOUR_CLAUDE_MODEL_ID"
claude
```

Replace the placeholders. Temporary variables affect this terminal and programs started from it. Set them again in a new terminal.

## 3) Option two: user-level configuration

Edit `~/.claude/settings.json`, or `%USERPROFILE%\.claude\settings.json` on Windows. Merge the following into the existing `env` object:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.unexhub.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CLAUDE_MODEL_ID"
  }
}
```

Use the root Base URL. `ANTHROPIC_AUTH_TOKEN` supplies a Bearer token; use `ANTHROPIC_API_KEY` instead if the service explicitly requires `x-api-key`. Remove or reconcile conflicting configuration values.

To map Opus, Sonnet, and Haiku aliases, follow the official gateway instructions for `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Every value must be an available model ID. Helper tasks may also use and bill these models.

## 4) Launch and verify

Run this from your project directory:

```bash
claude
```

Use `/status` to inspect the connection. Send “Reply with one short greeting. Do not read or modify files.” before starting a coding task. A non-interactive request is also available:

```bash
claude -p "Reply with one short greeting. Do not read or modify files."
```

## 5) Use and troubleshoot

Use `claude --resume` to restore a conversation. Restart the CLI after changing configuration. For 401, verify the active key and authentication method. For Messages-path or tool-parameter errors, check the gateway protocol and model capabilities.

A successful text response does not establish support for every tool, context size, or background task. Use capabilities supported by the selected model and route.

## 6) Review costs

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

## References

- [PoloAPI](https://poloapi.apifox.cn/9109750m0)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
- [Settings](https://code.claude.com/docs/en/settings)
