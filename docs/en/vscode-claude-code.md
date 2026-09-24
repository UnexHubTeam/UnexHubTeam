# Install Claude Code in VS Code

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/vscode-claude-code.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1) Install VS Code](#section-1)
2. [2) Install the official extension](#section-2)
3. [3) Configure UNEXHub](#section-3)
4. [4) Configure the extension and reload](#section-4)
5. [5) Open the panel and verify](#section-5)
6. [6) Review billing and troubleshoot](#section-6)
7. [References](#section-7)
</details>
<!-- DOCS-TOC:END -->


Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Use Anthropic's official VS Code extension to call models through UNEXHub from your editor.

> Direct access requires Anthropic Messages support in UNEXHub. See [Protocol compatibility](compatibility.md). The current official extension bundles a CLI for its chat panel. Install the standalone CLI separately only if you also want to run `claude` in a terminal.

<a id="section-1"></a>
## 1) Install VS Code

Install your platform's version from [VS Code](https://code.visualstudio.com/) and open a test project folder.

<a id="section-2"></a>
## 2) Install the official extension

Press `Cmd+Shift+X` on macOS or `Ctrl+Shift+X` on Windows. Search for `Claude Code`, verify the publisher is **Anthropic** and the extension ID is `anthropic.claude-code`, then install it.

<a id="section-3"></a>
## 3) Configure UNEXHub

Create a dedicated UNEXHub key and confirm an available Messages model ID. Open user-level `~/.claude/settings.json`, or `%USERPROFILE%\.claude\settings.json` on Windows, and merge this `env` object into the existing JSON:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.unexhub.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CLAUDE_MODEL_ID"
  }
}
```

Replace the key and model placeholders. Do not put credentials in repository-tracked `.vscode/settings.json` or `.claude/settings.json` files.

<a id="section-4"></a>
## 4) Configure the extension and reload

In VS Code user settings, search for `Claude Code login`. For the third-party gateway setup, enable **Disable Login Prompt** as described in the extension documentation. Run `Developer: Reload Window` from the command palette.

The extension also supports `claudeCode.environmentVariables`, but keeping shared gateway settings in the Claude Code user configuration avoids conflicting addresses or keys.

<a id="section-5"></a>
## 5) Open the panel and verify

Open Claude Code from the sidebar or toolbar, start a conversation, and send “Reply with one short greeting. Do not read or modify files.” Check the selected model and, where available, the gateway and authentication information in the status view.

An editor launched from the Dock or Start menu may not inherit temporary shell variables. Use the user settings above, or fully quit VS Code and start it with `code .` from the configured terminal.

<a id="section-6"></a>
## 6) Review billing and troubleshoot

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

If prompted for an official login, check gateway configuration and the extension login setting. For 401, check the key and authentication method. For 404, check Messages support and the root address. The standalone CLI and bundled extension CLI may have different versions; record both when troubleshooting.

<a id="section-7"></a>
## References

- [Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)

<!-- DOCS-PAGER:START -->

---

[← Previous: Claude Code](claude-code.md) · [Documentation home](README.md) · [Next: Install Codex →](codex-install.md)
<!-- DOCS-PAGER:END -->
