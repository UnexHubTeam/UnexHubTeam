# openclaw-cn integration tutorial

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/openclaw-cn.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install Node.js](#section-1)
2. [2) Install openclaw-cn](#section-2)
3. [3) Run onboarding](#section-3)
4. [4) Add a custom model](#section-4)
5. [5) Select the default model and finish onboarding](#section-5)
6. [6) Start the gateway and open the control interface](#section-6)
7. [7) Send a message and review costs](#section-7)
8. [References](#section-8)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

`openclaw-cn` is a Chinese community distribution of OpenClaw. This guide follows its community onboarding flow with UNEXHub settings. It is separate from UNEXHub's own UnexClaw product.

<a id="section-1"></a>
## 1) Install Node.js

Install Node.js 22.12.0 or later from [Node.js](https://nodejs.org/en/download). This minimum comes from the reviewed npm package's `engines` field. Recheck the requirement when upgrading.

```bash
node --version
npm --version
```

<a id="section-2"></a>
## 2) Install openclaw-cn

macOS / Linux:

```bash
npm install -g openclaw-cn@latest
openclaw-cn --version
```

Windows PowerShell:

```powershell
npm.cmd install -g openclaw-cn@latest
openclaw-cn.cmd --version
```

The `.cmd` entry point avoids changing the user's PowerShell execution policy for this guide. Confirm that you are installing the community package associated with [jiulingyun/openclaw-cn](https://github.com/jiulingyun/openclaw-cn).

<a id="section-3"></a>
## 3) Run onboarding

```bash
openclaw-cn onboard
```

On Windows, use `openclaw-cn.cmd onboard`. Read the introduction, continue, and select Quick Start. Preserve existing values if you already have a configuration, then edit the model provider.

<a id="section-4"></a>
## 4) Add a custom model

Choose Custom Model → Compatible Interface → OpenAI Compatible and enter:

| Field | Value |
| --- | --- |
| Provider name | `UNEXHub` |
| Base URL | `https://api.unexhub.ai/v1` |
| API Key | A dedicated UNEXHub key, such as `openclaw-test`. |
| Model ID | An exact available ID supporting Chat Completions, streaming, and tools. |

If the version distinguishes Chat Completions from Responses, select Chat Completions. This uses the protocol shown in the site's examples. Choose Anthropic Compatible only after UNEXHub confirms Messages support, using the supplied root address.

<a id="section-5"></a>
## 5) Select the default model and finish onboarding

Choose the new provider and model. For initial testing, skip external messaging channels, extra skills, and startup hooks. Follow the wizard's selection hints, such as Space to select and Enter to confirm.

Finish gateway setup. For a background service, the community documentation offers `openclaw-cn onboard --install-daemon`. A foreground gateway is sufficient for the first test.

<a id="section-6"></a>
## 6) Start the gateway and open the control interface

If onboarding has not already started it, run in a new terminal:

```bash
openclaw-cn gateway --port 18789 --verbose
```

Do not start a second instance if the gateway is already running. Open the **HTTP control-interface URL** printed by the terminal and connect as prompted. A `ws://` WebSocket address is not a browser page. Keep token-bearing local access links on your device.

<a id="section-7"></a>
## 7) Send a message and review costs

Choose the UNEXHub model in the chat page and send “Reply with one short greeting. Take no other actions.” After the local conversation works, follow the community's channel-specific documentation to connect services such as Feishu.

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

If text works but agent tools fail, check tool support and protocol conversion. A text reply alone does not verify the full agent workflow.

<a id="section-8"></a>
## References

- [Community project](https://github.com/jiulingyun/openclaw-cn)
- [npm package metadata](https://registry.npmjs.org/openclaw-cn/latest)

<!-- DOCS-PAGER:START -->

---

[← Previous: CC MAX](cc-max.md) · [Documentation home](README.md) · [Next: Mode B Agent development →](agent-development-upload.md)
<!-- DOCS-PAGER:END -->
