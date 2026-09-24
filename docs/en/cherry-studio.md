# Cherry Studio integration tutorial

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/cherry-studio.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install Cherry Studio and open Settings](#section-1)
2. [2) Add a custom provider](#section-2)
3. [3) Enter the API key and API address](#section-3)
4. [4) Add a model](#section-4)
5. [5) Enter the exact model ID and enable the provider](#section-5)
6. [6) Return to chat and select the model](#section-6)
7. [7) Review billing in UNEXHub](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Interface reviewed: 2026-09-22

Prepare a UNEXHub key and a currently available model ID using [Quickstart](quickstart.md). To use third-party upstream channels, first create a [third-party routing key](third-party-routing.md).

This tutorial uses text models that support Chat Completions. Follow the sequence: install → add provider → enter the address and key → add a model → enable it → chat.

<a id="section-1"></a>
## 1) Install Cherry Studio and open Settings

Install and launch Cherry Studio. Open Settings → Model Services and add a provider. Labels may vary by version; refer to the [official provider configuration guide](https://docs.cherryai.com.cn/pre-basic/providers/providers).

<a id="section-2"></a>
## 2) Add a custom provider

Name it `UNEXHub` and configure an OpenAI-compatible endpoint. In older versions with a Provider Type field, select OpenAI.

Choose the protocol supported by the selected UNEXHub model, rather than assuming a protocol from the model's brand.

<a id="section-3"></a>
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

<a id="section-4"></a>
## 4) Add a model

Fetch the model list, find the model, and select the plus button beside it. If fetching fails and your version supports manual entry, add a model manually and use the ID described in the next step.

<a id="section-5"></a>
## 5) Enter the exact model ID and enable the provider

Copy the exact ID from the [UNEXHub model details](https://unexhub.ai/market?tab=models) into the Model ID field. You can customize the display name, but the actual model ID sent to the API must match.

Finish adding the model and enable the provider with its toggle. Run the connection check and select the model to verify the configuration. This check may incur API charges.

<a id="section-6"></a>
## 6) Return to chat and select the model

Create a conversation and choose the model under `UNEXHub`. Send “Reply with one short greeting.” After receiving a reply, note the test time, key name, and model ID.

<a id="section-7"></a>
## 7) Review billing in UNEXHub

Open [Request Logs](https://unexhub.ai/console/log) and filter by date, key name, and model. Open the request details → Billing Details and review Final Charge.

![Request logs: date range, type, filters, and search](../../assets/log-filters.png)

Model checks, automatic retries, and title generation may cause extra calls; include them in your review. See [Billing records and exports](billing.md) for details, or [FAQ](faq.md) if the connection fails.

<!-- DOCS-PAGER:START -->

---

[← Previous: Chatbox](chatbox.md) · [Documentation home](README.md) · [Next: Cursor →](cursor.md)
<!-- DOCS-PAGER:END -->
