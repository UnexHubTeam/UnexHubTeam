# Windsurf

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/windsurf.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install and open the editor](#section-1)
2. [2) Determine whether a custom gateway is supported](#section-2)
3. [3) Use UNEXHub in the integrated terminal](#section-3)
4. [4) Verify and review billing](#section-4)
5. [References](#section-5)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

This page preserves the requested Windsurf tutorial entry and distinguishes built-in assistant access from integrated-terminal access.

> During review, the Windsurf model documentation redirected to Devin Desktop documentation. An arbitrary UNEXHub Base URL setting was not confirmed. Do not assume that generic OpenAI settings or environment variables work in every current version.

<a id="section-1"></a>
## 1) Install and open the editor

Use the current official download entry from [Windsurf](https://windsurf.com/) and open a test project. Check the version, model settings, and bring-your-own-key options.

<a id="section-2"></a>
## 2) Determine whether a custom gateway is supported

Enter the following only if your version explicitly offers a custom OpenAI-compatible address:

| Field | Value |
| --- | --- |
| API Key | A dedicated UNEXHub key, without `Bearer`. |
| SDK Base URL | `https://api.unexhub.ai/v1` |
| Model ID | An available model ID matching the protocol. |

If the field requests a root address or full endpoint, follow its instructions and inspect the resulting request path. The correct version path is `/v1`; do not copy the `/vi` typo in the reference tutorial.

An original-provider key field without a custom gateway address does not establish UNEXHub support. The built-in assistant is not guaranteed to read `OPENAI_BASE_URL` from your environment.

<a id="section-3"></a>
## 3) Use UNEXHub in the integrated terminal

To use UNEXHub within the editor, open Terminal → New Terminal, install [Aider](aider.md), and configure:

macOS / Linux:

```bash
export OPENAI_API_BASE='https://api.unexhub.ai/v1'
export OPENAI_API_KEY='YOUR_API_KEY'
aider --model openai/YOUR_MODEL_ID
```

Windows PowerShell:

```powershell
$env:OPENAI_API_BASE = "https://api.unexhub.ai/v1"
$env:OPENAI_API_KEY = "YOUR_API_KEY"
aider --model openai/YOUR_MODEL_ID
```

Replace the key and model. This runs a terminal tool inside the editor; it does not reconfigure the built-in Cascade/Devin assistant.

<a id="section-4"></a>
## 4) Verify and review billing

In Aider, enter `/ask Reply with one short greeting. Do not edit files.` If using a native version that supports custom gateways, send the same short prompt in its chat panel.

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

Native model-plan charges and UNEXHub requests from terminal tools are separate. Record the editor version, integration method, and error details when troubleshooting.

<a id="section-5"></a>
## References

- [Current model documentation](https://docs.devin.ai/desktop/models)
- [Aider compatible APIs](https://aider.chat/docs/llms/openai-compat.html)

<!-- DOCS-PAGER:START -->

---

[← Previous: Cursor](cursor.md) · [Documentation home](README.md) · [Next: Aider →](aider.md)
<!-- DOCS-PAGER:END -->
