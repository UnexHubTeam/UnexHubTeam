# GPT-Codex installation tutorial

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/codex-install.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install Node.js for the npm method](#section-1)
2. [2) Install Codex CLI](#section-2)
3. [3) Create a UNEXHub key](#section-3)
4. [4) Configure the provider](#section-4)
5. [5) Set the key and launch](#section-5)
6. [6) Verify and review billing](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Install OpenAI Codex CLI and configure model requests through UNEXHub. See [Codex](codex.md) for daily commands and configuration details.

> Current Codex custom providers use the Responses protocol. A successful `/v1/chat/completions` request does not establish direct Codex compatibility. UNEXHub `/v1/responses` support has not been tested. If only Chat Completions is available, use [CC Switch local routing](cc-switch.md).

<a id="section-1"></a>
## 1) Install Node.js for the npm method

Install the current LTS from [Node.js](https://nodejs.org/en/download). Open a new terminal and confirm that `node --version` and `npm --version` print version numbers.

<a id="section-2"></a>
## 2) Install Codex CLI

macOS / Linux / WSL:

```bash
npm install -g @openai/codex
codex --version
```

Windows PowerShell:

```powershell
npm.cmd install -g @openai/codex
codex.cmd --version
```

On Windows, `.cmd` avoids the npm wrapper that PowerShell script policy may block. If Homebrew is already installed on macOS, you can instead use `brew install --cask codex`. Choose one installation method.

<a id="section-3"></a>
## 3) Create a UNEXHub key

Create a dedicated key such as `codex-test` in [API Keys](https://unexhub.ai/console/token). Set its routing policy, expiration, and budget. Confirm Responses and tool-call support for the model, then copy its ID.

<a id="section-4"></a>
## 4) Configure the provider

Open your user-level configuration: `~/.codex/config.toml` on macOS/Linux, or `%USERPROFILE%\.codex\config.toml` on Windows. Create the directory and file if needed.

Merge the following settings and replace the model ID. `model_provider` must match the `unexhub` table name. Do not duplicate existing TOML keys or sections.

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

This direct configuration requires an available Responses gateway. The Base URL ends at `/v1`, not `/responses`. The key is read from an environment variable; this method does not require replacing an existing `auth.json`.

<a id="section-5"></a>
## 5) Set the key and launch

In a terminal opened in your project directory, on macOS/Linux/WSL:

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
codex
```

Windows PowerShell, from your project directory:

```powershell
$env:UNEXHUB_API_KEY = "YOUR_API_KEY"
codex.cmd
```

These variables apply to the current terminal and its child processes. For persistence, use OS user environment settings or a secret manager, then reopen the terminal. Do not put a real key on GitHub.

<a id="section-6"></a>
## 6) Verify and review billing

Send “Reply with one short greeting. Do not read or modify files.” After receiving a response, review the request below. ChatGPT sign-in and UNEXHub API-key access are distinct; this tutorial uses a custom provider with the UNEXHub key.

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

<a id="section-7"></a>
## References

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Provider configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

<!-- DOCS-PAGER:START -->

---

[← Previous: Claude Code in VS Code](vscode-claude-code.md) · [Documentation home](README.md) · [Next: Codex →](codex.md)
<!-- DOCS-PAGER:END -->
