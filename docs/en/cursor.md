# Cursor

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/cursor.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Configure custom-model chat in Cursor with a UNEXHub key. Availability of built-in completion and other features depends on the current version and plan.

## 1) Install and open Cursor

Install from [Cursor](https://cursor.com/), open a project, and go to Cursor Settings → Models. Prepare a dedicated UNEXHub key and an available Chat Completions model ID.

## 2) Check for a custom-address setting

Look for **Override OpenAI Base URL** or an equivalent option in the OpenAI provider settings. Polo's tutorial uses this control. The current official BYOK page confirms API-key support but does not explicitly guarantee arbitrary Base URLs on that page.

If your version has no custom-address control, entering a UNEXHub key into the official OpenAI field is insufficient. Use [Aider](aider.md) in Cursor's integrated terminal, or [Claude Code](claude-code.md)/[Codex](codex.md) with the required protocol.

## 3) Enter the key, Base URL, and model

For versions with the custom-address option:

| Field | Value |
| --- | --- |
| OpenAI API Key | Your complete UNEXHub key, without `Bearer`. |
| Override OpenAI Base URL | `https://api.unexhub.ai/v1` |
| Model | An exact model ID available on the selected route. |

Save the settings. If manual model entry is needed, select Add Model, enter the exact ID, and enable it. Enter a Base URL, not the full `/chat/completions` endpoint.

## 4) Verify the connection

Select Verify or the current equivalent. If verification uses a fixed model that is unavailable, check its UNEXHub availability, then test using the model you configured.

Open Chat, select the model, and send “Reply with one short greeting. Do not read or modify files.” Verification requests may also be billed.

## 5) Review costs and feature scope

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

The official documentation limits custom keys to chat models. Tab completion continues to use Cursor's built-in models. Review Cursor plan charges separately from UNEXHub model charges; a custom key does not redirect every editor feature to UNEXHub.

## References

- [PoloAPI](https://poloapi.apifox.cn/9103814m0)
- [Cursor API keys](https://cursor.com/help/models-and-usage/api-keys)
