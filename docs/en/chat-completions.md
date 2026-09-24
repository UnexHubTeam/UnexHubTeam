# Create a chat completion

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/chat-completions.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [Endpoint](#section-1)
2. [Request headers](#section-2)
3. [Request body](#section-3)
4. [Request example: cURL](#section-4)
5. [Request example: Python](#section-5)
6. [Response](#section-6)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Interface reviewed: 2026-09-22

Send messages to text models that support the Chat Completions interface. This page shows a minimal non-streaming request.

<a id="section-1"></a>
## Endpoint

```http
POST https://api.unexhub.ai/v1/chat/completions
```

SDK Base URL: `https://api.unexhub.ai/v1`.

<a id="section-2"></a>
## Request headers

| Name | Value | Required |
| --- | --- | --- |
| `Authorization` | `Bearer YOUR_API_KEY` | Yes |
| `Content-Type` | `application/json` | Yes |

Replace `YOUR_API_KEY` with an enabled, unexpired UNEXHub key. See [Quickstart](quickstart.md) to create one.

<a id="section-3"></a>
## Request body

| Parameter | Type | Description |
| --- | --- | --- |
| `model` | string | Required. The exact ID of an available model. |
| `messages` | array | Required. The conversation messages. |
| `messages[].role` | string | The example uses `user` for a user message. |
| `messages[].content` | string | The example sends a text prompt. |
| `stream` | boolean | Explicitly set to `false` here for a complete response. |

```json
{
  "model": "YOUR_MODEL_ID",
  "messages": [
    {"role": "user", "content": "Reply with one short greeting."}
  ],
  "stream": false
}
```

<a id="section-4"></a>
## Request example: cURL

Replace the key and model ID, then run this in a Bash-compatible terminal. `-i` also prints response headers so you can record a request identifier if provided.

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
export UNEXHUB_BASE_URL='https://api.unexhub.ai/v1'

curl -sS -i "$UNEXHUB_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $UNEXHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "YOUR_MODEL_ID",
    "messages": [
      {"role": "user", "content": "Reply with one short greeting."}
    ],
    "stream": false
  }'
```

<a id="section-5"></a>
## Request example: Python

Install the dependency and set the `UNEXHUB_API_KEY` and `UNEXHUB_BASE_URL` environment variables from the example above:

```bash
python3 -m pip install openai
```

Save the following as `call_model.py`, replace `YOUR_MODEL_ID`, and run `python3 call_model.py`.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UNEXHUB_API_KEY"],
    base_url=os.environ["UNEXHUB_BASE_URL"],
    max_retries=0,
)
response = client.chat.completions.create(
    model="YOUR_MODEL_ID",
    messages=[{
        "role": "user",
        "content": "Reply with one short greeting."
    }],
    stream=False,
)
print(response.choices[0].message.content)
print(response.usage)
```

Automatic SDK retries are disabled in this example to make the initial request easier to reconcile with the logs. Choose either request example.

<a id="section-6"></a>
## Response

Successful requests typically return HTTP 200. The following is an illustrative response fragment, not a measured API result. Additional fields and usage details depend on the actual response.

```json
{
  "choices": [
    {"message": {"role": "assistant", "content": "Hello!"}}
  ],
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 9,
    "total_tokens": 17
  }
}
```

| Field | Purpose |
| --- | --- |
| `choices[0].message.content` | The text reply. |
| `usage.prompt_tokens` | Input token count, when returned. |
| `usage.completion_tokens` | Output token count, when returned. |
| `usage.total_tokens` | Total token count, when returned. |

Token usage is not a charge amount. Review the final deduction in [Billing records](billing.md) after the call. For errors, see [FAQ](faq.md).

For optional parameters, streaming, and other model protocols, consult the model details and the [protocol compatibility notes](compatibility.md).

<!-- DOCS-PAGER:START -->

---

[← Previous: Protocol compatibility](compatibility.md) · [Documentation home](README.md) · [Next: Third-party routing →](third-party-routing.md)
<!-- DOCS-PAGER:END -->
