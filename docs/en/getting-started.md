# Quick start

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/getting-started.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Sign in and check funds](#section-1)
2. [2) Create an API key](#section-2)
3. [3) Choose a model and protocol](#section-3)
4. [4) Configure the address and send a request](#section-4)
5. [5) Review billing](#section-5)
6. [References](#section-6)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Choose an integration and complete your first key → request → billing workflow. See the [site guide](quickstart.md) for detailed console screenshots.

<a id="section-1"></a>
## 1) Sign in and check funds

Register or sign in at the [UNEXHub](https://unexhub.ai/). Check available funds in [Funds Account](https://unexhub.ai/console/topup).

<a id="section-2"></a>
## 2) Create an API key

Open [API Keys](https://unexhub.ai/console/token) → Create Key. Set a purpose-specific name, expiration, channel discount, and routing policy. Confirm that the key is enabled, copy it, and set a budget if needed.

![API key creation dialog](../../assets/create-key.png)

Select Third-party Routing to use third-party upstream channels. [Third-party routing](third-party-routing.md) is independent of the client application and does not require an upstream provider's key.

<a id="section-3"></a>
## 3) Choose a model and protocol

Copy a currently available model ID from the [marketplace](https://unexhub.ai/market?tab=models).

| Use case | Required interface | Tutorial |
| --- | --- | --- |
| Code or chat clients | Chat Completions | [cURL / Python](chat-completions.md), [Chatbox](chatbox.md), [Cherry Studio](cherry-studio.md) |
| Terminal coding | OpenAI-compatible chat | [Aider](aider.md) |
| Claude Code and its VS Code extension | Anthropic Messages or local conversion | [Claude Code](claude-code-install.md), [VS Code](vscode-claude-code.md) |
| Codex | Responses or local conversion | [Codex installation](codex-install.md) |
| Provider management and conversion | Depends on the target tool | [CC Switch](cc-switch.md) |
| Personal agent | Chat/tool protocol supported by the model | [openclaw-cn](openclaw-cn.md) |
| AI editors | Depends on custom-gateway support | [Cursor](cursor.md), [Windsurf](windsurf.md) |

Messages, Responses, and CC MAX support on the site has not been tested or confirmed. Check [Protocol compatibility](compatibility.md) before choosing direct access or conversion.

<a id="section-4"></a>
## 4) Configure the address and send a request

The SDK Base URL is `https://api.unexhub.ai/v1`. Standard Chatbox API Host and Cherry Studio auto-append settings take the root `https://api.unexhub.ai`.

Enter the key and model ID using the selected tutorial, then send a short greeting. Address formats differ between tools; do not copy one field value into every tool without checking.

<a id="section-5"></a>
## 5) Review billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

For connection problems, see [FAQ](faq.md). Return to [Documentation](README.md) for the complete installation tutorials.

<a id="section-6"></a>
## References

- [UNEXHub marketplace](https://unexhub.ai/market?tab=models)

<!-- DOCS-PAGER:START -->

---

[← Documentation home](README.md) · [Next: Console walkthrough →](quickstart.md)
<!-- DOCS-PAGER:END -->
