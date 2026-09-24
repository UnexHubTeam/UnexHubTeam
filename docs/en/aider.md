# Aider

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/aider.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install Aider](#section-1)
2. [2) Set the API address and key](#section-2)
3. [3) Select the model and launch](#section-3)
4. [4) Optionally save non-secret settings](#section-4)
5. [5) Test a conversation](#section-5)
6. [6) Review costs](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Aider is a terminal coding assistant with support for custom OpenAI-compatible APIs. This tutorial uses UNEXHub's Chat Completions address.

<a id="section-1"></a>
## 1) Install Aider

Use the official installer method from a terminal with Python:

```bash
python -m pip install aider-install
aider-install
aider --version
```

If macOS/Linux only provides `python3`, use `python3 -m pip install aider-install` for the first line. With the Windows Python Launcher, use `py -m pip install aider-install`. The installer creates an isolated environment for Aider. If the command is missing afterward, reopen the terminal and check the Python scripts directory in PATH.

<a id="section-2"></a>
## 2) Set the API address and key

Create a dedicated UNEXHub key such as `aider-test`. On macOS/Linux:

```bash
export OPENAI_API_BASE='https://api.unexhub.ai/v1'
export OPENAI_API_KEY='YOUR_API_KEY'
```

Windows PowerShell:

```powershell
$env:OPENAI_API_BASE = "https://api.unexhub.ai/v1"
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

Aider uses `OPENAI_API_BASE`. Replace the key placeholder and keep the address ending at `/v1`.

<a id="section-3"></a>
## 3) Select the model and launch

From a test project directory, run:

```bash
aider --model openai/YOUR_MODEL_ID
```

`openai/` is the Aider/LiteLLM provider prefix. The remainder is the exact UNEXHub model ID. Keep this prefix when using the compatible-provider workflow, even for a model from another brand.

<a id="section-4"></a>
## 4) Optionally save non-secret settings

In user-level `~/.aider.conf.yml`, save:

```yaml
model: openai/YOUR_MODEL_ID
openai-api-base: https://api.unexhub.ai/v1
```

Keep the key in an environment variable. Replace the model ID and merge with any existing settings. Aider may warn that an unfamiliar model lacks context-size or pricing metadata. That alone does not indicate API failure; use UNEXHub records for actual billing.

<a id="section-5"></a>
## 5) Test a conversation

In Aider's interactive interface, enter:

```text
/ask Reply with one short greeting. Do not edit files.
```

After a reply, add the files you want to work on and start editing. Helper models, commit-message generation, and other automatic tasks may create additional requests. Check the model selections in your configuration.

<a id="section-6"></a>
## 6) Review costs

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

<a id="section-7"></a>
## References

- [Aider installation](https://aider.chat/docs/install.html)
- [OpenAI-compatible API configuration](https://aider.chat/docs/llms/openai-compat.html)

<!-- DOCS-PAGER:START -->

---

[← Previous: Windsurf](windsurf.md) · [Documentation home](README.md) · [Next: Install Claude Code →](claude-code-install.md)
<!-- DOCS-PAGER:END -->
