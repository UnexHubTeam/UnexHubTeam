# Frequently asked questions

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/faq.md)

Website: [UNEXHub](https://unexhub.ai/) · Interface reviewed: 2026-09-22

## 1) Which API address should I use?

Use `https://api.unexhub.ai/v1` for the Python SDK's `base_url`. For direct HTTP calls, use `https://api.unexhub.ai/v1/chat/completions`.

For the standard Cherry Studio API address and Chatbox API Host, enter the root `https://api.unexhub.ai`; the client appends the path. If your version explicitly requests an SDK Base URL, follow that field's instructions. Avoid `/v1/v1`.

## 2) Why do I receive 401 or an authentication error?

Check that the key is complete, enabled, unexpired, and valid for the environment. Direct HTTP calls use `Authorization: Bearer YOUR_API_KEY`. Client key fields take only the key, without `Bearer`.

## 3) Why is there a quota error when my account has funds?

Check the key's daily, monthly, and total budget limits as well. Available account balance and per-key budget limits are separate conditions.

## 4) Why do I receive 400, 404, or a model-not-found error?

Check the endpoint path, JSON body, and exact model ID. Confirm that the model supports the protocol and is currently available. Look for a duplicated `/v1`. A model shown in a screenshot is not guaranteed to be callable.

## 5) How do third-party routes differ from third-party clients?

Routing controls which upstream channel category UNEXHub uses. A client is the application sending requests. Cherry Studio and Chatbox can use third-party routing keys or keys with other policies. UNEXHub handles upstream routing; the client still uses the UNEXHub address and key.

## 6) What should I do about 429, 5xx, or timeouts?

For 429, reduce concurrency and frequency, and follow the server's retry guidance. For 5xx or timeouts, check [service status](https://unexhub.ai/status) and request logs. Before retrying, check whether the original request completed and was billed.

Use the API's `error` message and console records to identify the specific cause.

## 7) Why can I not find a successful request in billing?

Verify the signed-in account and API environment. Expand the date range, clear unnecessary filters, and refresh. Search by key name, model, and request time together. The response `id` may differ from the console's Request ID.

## 8) Why can one chat message create multiple requests?

The client may run model tests, automatic retries, title generation, or multiple-model replies. Conversation history can also increase input usage. Review individual logs instead of treating the message count as the request count.

## 9) Why does the charge differ from the client estimate?

Use Request Detail Analysis → Billing Details → Final Charge in UNEXHub. Input, output, and cache pricing, as well as routing conditions, may affect the amount. Equivalent quota tokens are monetary accounting units, not tokens processed by the model.

## 10) How do I confirm that setup is complete?

- The key is enabled, with the intended routing policy and budget.
- The code or client returns a model reply.
- You can locate the request in the logs.
- You have reviewed Final Charge, including any test or retry requests.
- If needed, you have exported a statement for the correct date range.

## 11) Can Claude Code or Codex use the chat endpoint directly?

Claude Code requires Anthropic Messages; current Codex requires Responses. Substituting `/v1/chat/completions` does not convert those protocols. Confirm UNEXHub support or use [CC Switch](cc-switch.md) local conversion when only chat is available. See [Protocol compatibility](compatibility.md).

## 12) Why are my Windows environment settings not taking effect?

`$env:NAME = "value"` affects the current PowerShell and its child processes. `setx` updates user variables without changing the current window. Reopen the terminal before launching the tool. Editors started from a Dock or Start menu may not inherit temporary shell variables either.

## 13) What if PowerShell blocks an npm or Codex script?

For npm installations, use `npm.cmd`, `codex.cmd`, or `openclaw-cn.cmd`. These tutorials do not require changing the user's execution policy for those wrappers.

## 14) Why does a protocol error remain with CC Switch?

Check the target app, API Format or Needs Local Routing, model mapping, running proxy, and takeover switch. Saving a provider alone does not convert requests. Disable takeover and restore the desired settings before stopping the proxy.

## 15) Is CC MAX a UNEXHub model or plan?

It has not been confirmed. Polo's page describes its own dedicated channel, which does not establish a UNEXHub model, plan, or matching version restrictions. See [CC MAX](cc-max.md) for the details to obtain and setup steps.

## 16) What if the editor has no custom Base URL setting?

A field for an original provider's key does not automatically support UNEXHub keys. Check the conditions in [Cursor](cursor.md)/[Windsurf](windsurf.md), or use [Aider](aider.md) in the integrated terminal.

Continue reading: [Quickstart](quickstart.md) · [Third-party routing](third-party-routing.md) · [Billing records](billing.md)
