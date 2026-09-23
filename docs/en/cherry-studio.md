# Cherry Studio integration tutorial

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/cherry-studio.md)

Website: [UNEXHub](https://unexhub.ai/) · Interface reviewed: 2026-09-22

Prepare a UNEXHub key and a currently available model ID using [Quickstart](quickstart.md). To use third-party upstream channels, first create a [third-party routing key](third-party-routing.md).

This tutorial uses text models that support Chat Completions. Follow the sequence: install → add provider → enter the address and key → add a model → enable it → chat.

## 1) Install Cherry Studio and open Settings

Install and launch Cherry Studio. Open Settings → Model Services and add a provider. Labels may vary by version; refer to the [official provider configuration guide](https://docs.cherryai.com.cn/pre-basic/providers/providers).

## 2) Add a custom provider

Name it `UNEXHub` and configure an OpenAI-compatible endpoint. In older versions with a Provider Type field, select OpenAI.

Choose the protocol supported by the selected UNEXHub model, rather than assuming a protocol from the model's brand.

## 3) Enter the API key and API address

| Setting | Value |
| --- | --- |
| Provider name | `UNEXHub` |
| API key | Your complete UNEXHub key, without the `Bearer` prefix. |
| API address | `https://api.unexhub.ai` |

For standard chat configuration, enter the root address. Cherry Studio appends `/v1/chat/completions`. If your version explicitly asks for an SDK Base URL, use `https://api.unexhub.ai/v1`.

The final request URL should be:

```text
https://api.unexhub.ai/v1/chat/completions
```

## 4) Add a model

Fetch the model list, find the model, and select the plus button beside it. If fetching fails and your version supports manual entry, add a model manually and use the ID described in the next step.

## 5) Enter the exact model ID and enable the provider

Copy the exact ID from the [UNEXHub model details](https://unexhub.ai/market?tab=models) into the Model ID field. You can customize the display name, but the actual model ID sent to the API must match.

Finish adding the model and enable the provider with its toggle. Run the connection check and select the model to verify the configuration. This check may incur API charges.

## 6) Return to chat and select the model

Create a conversation and choose the model under `UNEXHub`. Send “Reply with one short greeting.” After receiving a reply, note the test time, key name, and model ID.

## 7) Review billing in UNEXHub

Open [Request Logs](https://unexhub.ai/console/log) and filter by date, key name, and model. Open the request details → Billing Details and review Final Charge.

![Request logs: date range, type, filters, and search](../../assets/log-filters.png)

Model checks, automatic retries, and title generation may cause extra calls; include them in your review. See [Billing records and exports](billing.md) for details, or [FAQ](faq.md) if the connection fails.
