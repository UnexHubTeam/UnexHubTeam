# CC Switch

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/cc-switch.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install CC Switch](#section-1)
2. [2) Add UNEXHub as a provider](#section-2)
3. [3) Claude Code: convert Chat Completions to Messages](#section-3)
4. [4) Codex: convert Responses to Chat Completions](#section-4)
5. [5) Verify and restore](#section-5)
6. [6) Review billing](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

CC Switch manages provider configurations for Claude Code, Codex, and other tools, and offers local protocol conversion. It is not a model service; you still need a UNEXHub key and an available model.

<a id="section-1"></a>
## 1) Install CC Switch

Download the platform-specific package from [official Releases](https://github.com/farion1231/cc-switch/releases). On macOS, you can also run:

```bash
brew install --cask cc-switch
```

Install the target [Claude Code](claude-code-install.md) or [Codex](codex-install.md) client first. Preserve your existing provider configuration before switching so you can restore it.

<a id="section-2"></a>
## 2) Add UNEXHub as a provider

Select the target application tab → Add Provider → Custom. Name it `UNEXHub` and enter a dedicated API key. If fetching models fails, enter the exact model ID manually.

Choose the address according to the target application and connection mode:

| Target and mode | Address | Upstream protocol |
| --- | --- | --- |
| Direct Claude Code | `https://api.unexhub.ai` | Anthropic Messages; confirm availability first. |
| Direct Codex | `https://api.unexhub.ai/v1` | Responses; confirm availability first. |
| Local conversion to UNEXHub chat | Use full URL mode below or inspect path concatenation. | Chat Completions. |

Do not apply a universal “omit `/v1`” rule to every app. Inspect the effective configuration. See [Codex](codex.md) and [Claude Code](claude-code.md) for direct-access examples.

<a id="section-3"></a>
## 3) Claude Code: convert Chat Completions to Messages

If the upstream supports only Chat Completions:

1. In the Claude provider's Advanced Options, select **OpenAI Chat Completions** as **API Format**.
2. In versions offering **Full URL Mode**, enable it and enter `https://api.unexhub.ai/v1/chat/completions`. Otherwise, use the prefix required by that version's path rules and verify that it reaches the same endpoint.
3. Enter the real upstream model ID. If primary/helper mappings are offered, use available IDs for each.
4. Save and enable the provider, start the local proxy, enable **Claude Code takeover**, and restart Claude Code.

Conversion requires a running proxy with takeover enabled. Saving a provider alone does not convert the protocol.

<a id="section-4"></a>
## 4) Codex: convert Responses to Chat Completions

1. Switch to the Codex provider tab and add or edit UNEXHub.
2. Enable **Needs Local Routing**.
3. In **Model Mapping**, enter the actual UNEXHub model ID and an optional display name.
4. Configure the UNEXHub upstream address according to the version's fields. If full URL mode is offered, use the complete chat endpoint. The final request must reach `/v1/chat/completions`.
5. Start local routing, enable **Codex takeover**, activate the provider, and restart Codex to refresh its model list.

The local proxy converts Codex Responses requests to upstream Chat Completions. Keep it running while using the client. Let CC Switch generate its local address rather than copying someone else's proxy port.

<a id="section-5"></a>
## 5) Verify and restore

Send “Reply with one short greeting. Do not read or modify files.” in the target tool. Confirm that CC Switch and UNEXHub both show the request.

Tools, reasoning content, and streaming conversion depend on CC Switch and the upstream model. Test the required workflow after basic text connectivity. To stop using the proxy, disable takeover and restore the previous provider through CC Switch before exiting the proxy.

<a id="section-6"></a>
## 6) Review billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

CC Switch's local usage view helps investigation; UNEXHub records determine the final charge. This workflow uses a UNEXHub API key and does not require another provider's subscription or OAuth access.

<a id="section-7"></a>
## References

- [CC Switch](https://github.com/farion1231/cc-switch)
- [Provider manual](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/2-providers/2.1-add.md)

<!-- DOCS-PAGER:START -->

---

[← Previous: Codex](codex.md) · [Documentation home](README.md) · [Next: CC MAX →](cc-max.md)
<!-- DOCS-PAGER:END -->
