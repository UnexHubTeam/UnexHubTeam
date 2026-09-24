# Cursor

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/cursor.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install and open Cursor](#section-1)
2. [2) Check for a custom-address setting](#section-2)
3. [3) Enter the key, Base URL, and model](#section-3)
4. [4) Verify the connection](#section-4)
5. [5) Review costs and feature scope](#section-5)
6. [References](#section-6)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Configure custom-model chat in Cursor with a UNEXHub key. Availability of built-in completion and other features depends on the current version and plan.

<a id="section-1"></a>
## 1) Install and open Cursor

Install from [Cursor](https://cursor.com/), open a project, and go to Cursor Settings → Models. Prepare a dedicated UNEXHub key and an available Chat Completions model ID.

<a id="section-2"></a>
## 2) Check for a custom-address setting

Look for **Override OpenAI Base URL** or an equivalent option in the OpenAI provider settings. The current official BYOK page confirms API-key support but does not explicitly guarantee arbitrary Base URLs on that page.

If your version has no custom-address control, entering a UNEXHub key into the official OpenAI field is insufficient. Use [Aider](aider.md) in Cursor's integrated terminal, or [Claude Code](claude-code.md)/[Codex](codex.md) with the required protocol.

<a id="section-3"></a>
## 3) Enter the key, Base URL, and model

For versions with the custom-address option:

| Field | Value |
| --- | --- |
| OpenAI API Key | Your complete UNEXHub key, without `Bearer`. |
| Override OpenAI Base URL | `https://api.unexhub.ai/v1` |
| Model | An exact model ID available on the selected route. |

Save the settings. If manual model entry is needed, select Add Model, enter the exact ID, and enable it. Enter a Base URL, not the full `/chat/completions` endpoint.

<a id="section-4"></a>
## 4) Verify the connection

Select Verify or the current equivalent. If verification uses a fixed model that is unavailable, check its UNEXHub availability, then test using the model you configured.

Open Chat, select the model, and send “Reply with one short greeting. Do not read or modify files.” Verification requests may also be billed.

<a id="section-5"></a>
## 5) Review costs and feature scope

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

The official documentation limits custom keys to chat models. Tab completion continues to use Cursor's built-in models. Review Cursor plan charges separately from UNEXHub model charges; a custom key does not redirect every editor feature to UNEXHub.

<a id="section-6"></a>
## References

- [Cursor API keys](https://cursor.com/help/models-and-usage/api-keys)

<!-- DOCS-PAGER:START -->

---

[← Previous: Cherry Studio](cherry-studio.md) · [Documentation home](README.md) · [Next: Windsurf →](windsurf.md)
<!-- DOCS-PAGER:END -->
