# CC MAX

[Documentation](README.md) · English | [简体中文](../zh-CN/cc-max.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

This page corresponds to **CC MAX** in PoloAPI's sidebar. The source describes a Polo channel dedicated to Claude Code. It is not a separate client to install or a confirmed UNEXHub product of the same name.

> The equivalent UNEXHub channel, dedicated address, and version restrictions have not been confirmed. This page describes setup after such a channel is enabled. For ordinary Claude access, use the [Claude Code tutorial](claude-code.md).

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

Polo's specific version range and client-only restrictions apply to its channel. They do not establish UNEXHub compatibility.

## 2) Install the client and record its version

Use the [Claude Code installation tutorial](claude-code-install.md) and run `claude --version`. For VS Code, follow the [extension tutorial](vscode-claude-code.md) and record the extension version.

Choose a particular client version only when UNEXHub provides an explicit compatibility requirement.

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

## 4) Launch and verify

Restart the CLI or reload VS Code. Check the gateway address and send a short greeting. On failure, record the CLI/extension versions, error, model, and Request ID, then check channel access.

## 5) Review charges

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

If the dedicated service uses another environment, review records in the console it specifies. Without dedicated-channel details, use ordinary model access, third-party routing, or the CC Switch conversion workflow elsewhere in this guide.

## References

- [PoloAPI CC MAX channel reference](https://poloapi.apifox.cn/9111206m0)
- [Claude gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
