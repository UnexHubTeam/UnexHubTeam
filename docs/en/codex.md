# Codex

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/codex.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Choose direct access or local conversion](#section-1)
2. [2) Configure a custom provider](#section-2)
3. [3) Set the API key](#section-3)
4. [4) Launch and use Codex](#section-4)
5. [5) Multiple configurations and troubleshooting](#section-5)
6. [6) Review calls and billing](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

This page covers Codex CLI integration. For initial installation, see the [GPT-Codex installation tutorial](codex-install.md).

<a id="section-1"></a>
## 1) Choose direct access or local conversion

The current official configuration reference only supports `responses` for `wire_api`. Use the direct configuration below when UNEXHub exposes `/v1/responses` for the target model. That endpoint has not been tested here.

If only `/v1/chat/completions` is available, use [CC Switch local routing](cc-switch.md) to convert it. Do not set `wire_api` to `chat` or use the full chat endpoint as `base_url`.

<a id="section-2"></a>
## 2) Configure a custom provider

Edit user-level `~/.codex/config.toml`, or `%USERPROFILE%\.codex\config.toml` on Windows, and merge:

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

Replace the model ID. Ensure `model_provider` matches `[model_providers.unexhub]`. Keep provider and authentication settings in the user-level file rather than relying on project-level overrides.

<a id="section-3"></a>
## 3) Set the API key

macOS / Linux:

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
```

Windows PowerShell:

```powershell
$env:UNEXHUB_API_KEY = "YOUR_API_KEY"
```

These are session settings. For persistence, use OS user environment settings or a secret manager. Setting only `OPENAI_API_KEY` does not populate the `UNEXHUB_API_KEY` expected by this configuration.

<a id="section-4"></a>
## 4) Launch and use Codex

From your project directory, choose one of these modes:

```bash
codex
```

Single execution:

```bash
codex exec "Reply with one short greeting. Do not read or modify files."
```

Temporarily select another available model:

```bash
codex --model YOUR_RESPONSES_MODEL_ID
```

If PowerShell blocks the npm script wrapper, replace `codex` with `codex.cmd`. Reasoning parameters, image inputs, and tools depend on model capabilities. Establish connectivity before enabling extra options.

<a id="section-5"></a>
## 5) Multiple configurations and troubleshooting

Define distinct `[model_providers.<id>]` sections for different providers and select the correct `model_provider`. Current profile-file syntax differs from older releases. Consult official advanced configuration before using profiles, and do not copy older `[models]` routing examples.

For 401, check `UNEXHUB_API_KEY` in the current terminal. For 404, check the `/v1` Base URL and Responses support. For unsupported parameters, remove optional reasoning settings and check capabilities. For missing models, verify the exact ID; after updating a CC Switch model mapping, restart Codex.

<a id="section-6"></a>
## 6) Review calls and billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

<a id="section-7"></a>
## References

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Provider configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

<!-- DOCS-PAGER:START -->

---

[← Previous: Install Codex](codex-install.md) · [Documentation home](README.md) · [Next: CC Switch →](cc-switch.md)
<!-- DOCS-PAGER:END -->
