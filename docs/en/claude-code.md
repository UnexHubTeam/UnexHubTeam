# Claude Code

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/claude-code.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Confirm the protocol and connection details](#section-1)
2. [2) Option one: temporary terminal configuration](#section-2)
3. [3) Option two: user-level configuration](#section-3)
4. [4) Launch and verify](#section-4)
5. [5) Use and troubleshoot](#section-5)
6. [6) Review costs](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Claude Code is a terminal coding assistant. This page covers persistent UNEXHub configuration, startup, model selection, and billing. For installation, see the [Windows/macOS tutorial](claude-code-install.md).

<a id="section-1"></a>
## 1) Confirm the protocol and connection details

You need an Anthropic Messages-compatible gateway, a valid key, and an available model ID. This protocol has not been tested on UNEXHub. Check [compatibility](compatibility.md), or use [CC Switch](cc-switch.md) to convert a supported Chat Completions endpoint.

<a id="section-2"></a>
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

<a id="section-3"></a>
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

<a id="section-4"></a>
## 4) Launch and verify

Run this from your project directory:

```bash
claude
```

Use `/status` to inspect the connection. Send “Reply with one short greeting. Do not read or modify files.” before starting a coding task. A non-interactive request is also available:

```bash
claude -p "Reply with one short greeting. Do not read or modify files."
```

<a id="section-5"></a>
## 5) Use and troubleshoot

Use `claude --resume` to restore a conversation. Restart the CLI after changing configuration. For 401, verify the active key and authentication method. For Messages-path or tool-parameter errors, check the gateway protocol and model capabilities.

A successful text response does not establish support for every tool, context size, or background task. Use capabilities supported by the selected model and route.

<a id="section-6"></a>
## 6) Review costs

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

<a id="section-7"></a>
## References

- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
- [Settings](https://code.claude.com/docs/en/settings)

<!-- DOCS-PAGER:START -->

---

[← Previous: Install Claude Code](claude-code-install.md) · [Documentation home](README.md) · [Next: Claude Code in VS Code →](vscode-claude-code.md)
<!-- DOCS-PAGER:END -->
