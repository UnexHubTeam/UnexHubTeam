# Install Claude Code on Windows and macOS

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/claude-code-install.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Prepare your environment](#section-1)
2. [2) Install Claude Code](#section-2)
3. [3) Set the API address, key, and model](#section-3)
4. [4) Verify a first conversation](#section-4)
5. [5) Save the configuration](#section-5)
6. [6) Review billing](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Install Claude Code, then configure the UNEXHub gateway. For ongoing CLI use, see [Claude Code](claude-code.md).

> Connection requirement: your UNEXHub key and model must support Anthropic Messages, streaming, and tool calls. The Chat Completions example was reviewed; Messages has not been tested. See [Protocol compatibility](compatibility.md). If only Chat Completions is available, consider [CC Switch protocol conversion](cc-switch.md).

<a id="section-1"></a>
## 1) Prepare your environment

Use a Windows or macOS terminal. On native Windows, [Git for Windows](https://git-scm.com/downloads/win) is recommended for the Bash tool. Use the Linux command for WSL.

The official native installer does not require Node.js. If you choose npm instead, the current official instructions require Node.js 22 or later.

[Create a dedicated UNEXHub key](quickstart.md), such as `claude-code-test`, and check its balance, routing policy, and budget.

<a id="section-2"></a>
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

<a id="section-3"></a>
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

<a id="section-4"></a>
## 4) Verify a first conversation

Start `claude` in a test project directory. Run `/status` to check the gateway address and credential type. Send “Reply with one short greeting. Do not read or modify files.”

A text reply confirms basic connectivity. Code editing and agent workflows also require tool support. A Messages protocol error cannot be fixed by substituting the Chat Completions path.

<a id="section-5"></a>
## 5) Save the configuration

Follow the [Claude Code configuration tutorial](claude-code.md) to merge settings into your user-level `~/.claude/settings.json`, or `%USERPROFILE%\.claude\settings.json` on Windows. Preserve existing fields and keep real keys out of repository files.

<a id="section-6"></a>
## 6) Review billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

<a id="section-7"></a>
## References

- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)

<!-- DOCS-PAGER:START -->

---

[← Previous: Aider](aider.md) · [Documentation home](README.md) · [Next: Claude Code →](claude-code.md)
<!-- DOCS-PAGER:END -->
