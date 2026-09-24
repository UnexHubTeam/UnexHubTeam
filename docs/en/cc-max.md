# CC MAX

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/cc-max.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Obtain the channel details](#section-1)
2. [2) Install the client and record its version](#section-2)
3. [3) Configure the dedicated address and key](#section-3)
4. [4) Launch and verify](#section-4)
5. [5) Review charges](#section-5)
6. [References](#section-6)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

This page is a compatibility checklist for a dedicated Claude Code channel sometimes described as **CC MAX**. It is not a separate client to install, and UNEXHub availability has not been confirmed.

> The equivalent UNEXHub channel, dedicated address, and version restrictions have not been confirmed. This page describes setup after such a channel is enabled. For ordinary Claude access, use the [Claude Code tutorial](claude-code.md).

<a id="section-1"></a>
## 1) Obtain the channel details

Check UNEXHub model/routing information or request the following from [support@unexhub.com](mailto:support@unexhub.com):

| Detail | What to confirm |
| --- | --- |
| Base URL | The dedicated gateway root and whether it uses the standard API domain or another dedicated domain. |
| Key and route | Whether your UNEXHub key has access to the channel. |
| Model ID | Exact callable IDs and any helper-model mapping. |
| Protocol | Anthropic Messages, streaming, and tool support. |
| Client scope | CLI, VS Code extension, and other supported clients. |
| Versions and billing | Recommended versions, prices, budgets, and log location. |

Do not assume version ranges or client-only restrictions from another service apply to UNEXHub. Use only requirements confirmed by UNEXHub for the current channel.

<a id="section-2"></a>
## 2) Install the client and record its version

Use the [Claude Code installation tutorial](claude-code-install.md) and run `claude --version`. For VS Code, follow the [extension tutorial](vscode-claude-code.md) and record the extension version.

Choose a particular client version only when UNEXHub provides an explicit compatibility requirement.

<a id="section-3"></a>
## 3) Configure the dedicated address and key

Merge the following into user-level `~/.claude/settings.json`, replacing every placeholder:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "YOUR_CONFIRMED_CC_MAX_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CONFIRMED_CC_MAX_MODEL_ID"
  }
}
```

The standard API address is not prefilled because this dedicated channel has not been confirmed. If the service requires `x-api-key`, change the credential variable to `ANTHROPIC_API_KEY`.

<a id="section-4"></a>
## 4) Launch and verify

Restart the CLI or reload VS Code. Check the gateway address and send a short greeting. On failure, record the CLI/extension versions, error, model, and Request ID, then check channel access.

<a id="section-5"></a>
## 5) Review charges

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

If the dedicated service uses another environment, review records in the console it specifies. Without dedicated-channel details, use ordinary model access, third-party routing, or the CC Switch conversion workflow elsewhere in this guide.

<a id="section-6"></a>
## References

- [Claude gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)

<!-- DOCS-PAGER:START -->

---

[← Previous: CC Switch](cc-switch.md) · [Documentation home](README.md) · [Next: openclaw-cn →](openclaw-cn.md)
<!-- DOCS-PAGER:END -->
