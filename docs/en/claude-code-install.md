# Install Claude Code on Windows and macOS

[Documentation](README.md) · English | [简体中文](../zh-CN/claude-code-install.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Install Claude Code, then configure the UNEXHub gateway. For ongoing CLI use, see [Claude Code](claude-code.md).

> Connection requirement: your UNEXHub key and model must support Anthropic Messages, streaming, and tool calls. The Chat Completions example was reviewed; Messages has not been tested. See [Protocol compatibility](compatibility.md). If only Chat Completions is available, consider [CC Switch protocol conversion](cc-switch.md).

## 1) Prepare your environment

Use a Windows or macOS terminal. On native Windows, [Git for Windows](https://git-scm.com/downloads/win) is recommended for the Bash tool. Use the Linux command for WSL.

The official native installer does not require Node.js. If you choose npm instead, the current official instructions require Node.js 22 or later.

[Create a dedicated UNEXHub key](quickstart.md), such as `claude-code-test`, and check its balance, routing policy, and budget.

## 2) Install Claude Code

macOS / Linux / WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Alternatively, use one package manager: `brew install --cask claude-code` on macOS, or `winget install Anthropic.ClaudeCode` on Windows.

Open a new terminal and check the installation:

```bash
claude --version
```

## 3) Set the API address, key, and model

After confirming Messages support, replace the placeholders below. Use the root Base URL, without `/v1` or `/messages`.

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

This example uses `ANTHROPIC_AUTH_TOKEN` for Bearer authentication. If UNEXHub explicitly requires `x-api-key`, use `ANTHROPIC_API_KEY` instead. Keep only the required authentication method. Replace `YOUR_CLAUDE_MODEL_ID` with an exact ID available on your route.

## 4) Verify a first conversation

Start `claude` in a test project directory. Run `/status` to check the gateway address and credential type. Send “Reply with one short greeting. Do not read or modify files.”

A text reply confirms basic connectivity. Code editing and agent workflows also require tool support. A Messages protocol error cannot be fixed by substituting the Chat Completions path.

## 5) Save the configuration

Follow the [Claude Code configuration tutorial](claude-code.md) to merge settings into your user-level `~/.claude/settings.json`, or `%USERPROFILE%\.claude\settings.json` on Windows. Preserve existing fields and keep real keys out of repository files.

## 6) Review billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

## References

- [PoloAPI](https://poloapi.apifox.cn/8239025m0)
- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
