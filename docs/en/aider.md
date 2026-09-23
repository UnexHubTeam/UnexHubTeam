# Aider

[Documentation](README.md) · English (primary) | [简体中文（辅助翻译）](../zh-CN/aider.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Aider is a terminal coding assistant with support for custom OpenAI-compatible APIs. This tutorial uses UNEXHub's Chat Completions address.

## 1) Install Aider

Use the official installer method from a terminal with Python:

```bash
python -m pip install aider-install
aider-install
aider --version
```

If macOS/Linux only provides `python3`, use `python3 -m pip install aider-install` for the first line. With the Windows Python Launcher, use `py -m pip install aider-install`. The installer creates an isolated environment for Aider. If the command is missing afterward, reopen the terminal and check the Python scripts directory in PATH.

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

## 3) Select the model and launch

From a test project directory, run:

```bash
aider --model openai/YOUR_MODEL_ID
```

`openai/` is the Aider/LiteLLM provider prefix. The remainder is the exact UNEXHub model ID. Keep this prefix when using the compatible-provider workflow, even for a model from another brand.

## 4) Optionally save non-secret settings

In user-level `~/.aider.conf.yml`, save:

```yaml
model: openai/YOUR_MODEL_ID
openai-api-base: https://api.unexhub.ai/v1
```

Keep the key in an environment variable. Replace the model ID and merge with any existing settings. Aider may warn that an unfamiliar model lacks context-size or pricing metadata. That alone does not indicate API failure; use UNEXHub records for actual billing.

## 5) Test a conversation

In Aider's interactive interface, enter:

```text
/ask Reply with one short greeting. Do not edit files.
```

After a reply, add the files you want to work on and start editing. Helper models, commit-message generation, and other automatic tasks may create additional requests. Check the model selections in your configuration.

## 6) Review costs

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

## References

- [PoloAPI](https://poloapi.apifox.cn/9111349m0)
- [Aider installation](https://aider.chat/docs/install.html)
- [OpenAI-compatible API configuration](https://aider.chat/docs/llms/openai-compat.html)
