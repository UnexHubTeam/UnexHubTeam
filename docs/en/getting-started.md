# Quick start

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/getting-started.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Choose an integration and complete your first key → request → billing workflow. See the [site guide](quickstart.md) for detailed console screenshots.

## 1) Sign in and check funds

Register or sign in at the [UNEXHub](https://unexhub.ai/). Check available funds in [Funds Account](https://unexhub.ai/console/topup).

## 2) Create an API key

Open [API Keys](https://unexhub.ai/console/token) → Create Key. Set a purpose-specific name, expiration, channel discount, and routing policy. Confirm that the key is enabled, copy it, and set a budget if needed.

![API key creation dialog](../../assets/create-key.png)

Select Third-party Routing to use third-party upstream channels. [Third-party routing](third-party-routing.md) is independent of the client application and does not require an upstream provider's key.

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

## 4) Configure the address and send a request

The SDK Base URL is `https://api.unexhub.ai/v1`. Standard Chatbox API Host and Cherry Studio auto-append settings take the root `https://api.unexhub.ai`.

Enter the key and model ID using the selected tutorial, then send a short greeting. Address formats differ between tools; do not copy one field value into every tool without checking.

## 5) Review billing

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

For connection problems, see [FAQ](faq.md). Return to [Documentation](README.md) for the complete installation tutorials.

## References

- [PoloAPI quick start](https://poloapi.apifox.cn/9100436m0)
- [UNEXHub marketplace](https://unexhub.ai/market?tab=models)
