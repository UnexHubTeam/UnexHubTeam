# Client and protocol compatibility

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/compatibility.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Address and protocol reference](#section-1)
2. [2) Chat Completions, Responses, and Messages](#section-2)
3. [3) Confirm that an integration works](#section-3)
4. [4) Website and API addresses](#section-4)
5. [5) API reference availability](#section-5)
6. [References](#section-6)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

The same model name may appear behind different protocols. Check the tool's protocol, the endpoints UNEXHub exposes, and the model/route permissions on your key.

<a id="section-1"></a>
## 1) Address and protocol reference

| Tool or mode | Configuration address | Protocol or endpoint | Verification scope |
| --- | --- | --- | --- |
| cURL / Python chat | SDK Base URL `https://api.unexhub.ai/v1` | `POST /v1/chat/completions` | Model code example reviewed; no paid call executed. |
| Chatbox | API Host `https://api.unexhub.ai` | Chat Completions | Configuration fields reviewed. |
| Cherry Studio | Root address in auto-append mode | Chat Completions | Official client instructions reviewed. |
| Aider | `OPENAI_API_BASE` ending at `/v1` | Chat Completions | Official compatible-API instructions reviewed. |
| openclaw-cn | OpenAI Compatible ending at `/v1` | Chat Completions and tools | Community installation and onboarding documentation reviewed; agent not run. |
| Direct Claude Code / VS Code extension | Root of a confirmed Messages gateway | Anthropic Messages, typically `/v1/messages` | Official gateway settings reviewed; UNEXHub end-to-end support unconfirmed. |
| Direct Codex | Base URL ending at `/v1` | Responses, typically `/v1/responses` | Official configuration reviewed; UNEXHub end-to-end support unconfirmed. |
| CC Switch conversion | Depends on target app, API Format, and full URL mode | Local conversion to upstream Chat Completions | Project manual reviewed; UNEXHub conversion not tested. |
| Native Cursor | Custom Base URL ending at `/v1` | Depends on client model settings | Requires a custom-address control in the current version. |
| Native Windsurf | Depends on explicit support in the current version | Depends on the built-in assistant | Arbitrary gateways unconfirmed; terminal alternative provided. |
| CC MAX | Obtain the actual dedicated-channel address | Depends on channel specifications | Equivalent UNEXHub channel unconfirmed. |

A reviewed document or interface provides a configuration basis; it does not mean that every client has completed an actual model call.

<a id="section-2"></a>
## 2) Chat Completions, Responses, and Messages

Chat Completions uses a `messages` request body and works with clients such as Chatbox, Cherry Studio, and Aider. Current Codex uses Responses. Claude Code uses Anthropic Messages. Their request fields, stream events, tools, and response formats differ. Changing only the URL suffix does not convert the protocol.

If the upstream only supports Chat Completions, use a compatible client or a configured, running [CC Switch local converter](cc-switch.md). Client-side conversion does not mean UNEXHub natively exposes the other protocol.

<a id="section-3"></a>
## 3) Confirm that an integration works

1. The model and route are available, and the key is valid with sufficient budget.
2. The tool uses the correct final address, protocol, and authentication method.
3. A short request returns model content.
4. A matching UNEXHub request log appears with a final charge.
5. Separately verify streaming, tools, helper models, and other features required by the coding workflow.

<a id="section-4"></a>
## 4) Website and API addresses

The website and console use `https://unexhub.ai/`. The API root is `https://api.unexhub.ai`, and the OpenAI-compatible SDK Base URL is `https://api.unexhub.ai/v1`. Do not use the website URL as an API Base URL.

To ask support about an unclear protocol, provide the tool, version, model ID, and required endpoint. Do not send a complete key.

<a id="section-5"></a>
## 5) API reference availability

The official [UnexHub Public API reference](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) is published as a Postman collection. Use it to inspect currently documented public endpoints. Endpoint presence alone does not guarantee that every model, route, key, or client supports the protocol; confirm model details and account permissions before integration.

<a id="section-6"></a>
## References

- [Codex protocol reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Claude gateway requirements](https://code.claude.com/docs/en/llm-gateway)
- [CC Switch provider manual](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/2-providers/2.1-add.md)

<!-- DOCS-PAGER:START -->

---

[← Previous: Console walkthrough](quickstart.md) · [Documentation home](README.md) · [Next: Chat Completions API →](chat-completions.md)
<!-- DOCS-PAGER:END -->
