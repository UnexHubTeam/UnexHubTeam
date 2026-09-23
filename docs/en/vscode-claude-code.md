# Install Claude Code in VS Code

[Documentation](README.md) · English | [简体中文](../zh-CN/vscode-claude-code.md)

Website: [UNEXHub](https://unexhub.ai/) · Updated: 2026-09-23

Use Anthropic's official VS Code extension to call models through UNEXHub from your editor.

> Direct access requires Anthropic Messages support in UNEXHub. See [Protocol compatibility](compatibility.md). The current official extension bundles a CLI for its chat panel. Install the standalone CLI separately only if you also want to run `claude` in a terminal.

## 1) Install VS Code

Install your platform's version from [VS Code](https://code.visualstudio.com/) and open a test project folder.

## 2) Install the official extension

Press `Cmd+Shift+X` on macOS or `Ctrl+Shift+X` on Windows. Search for `Claude Code`, verify the publisher is **Anthropic** and the extension ID is `anthropic.claude-code`, then install it.

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

## 4) Configure the extension and reload

In VS Code user settings, search for `Claude Code login`. For the third-party gateway setup, enable **Disable Login Prompt** as described in the extension documentation. Run `Developer: Reload Window` from the command palette.

The extension also supports `claudeCode.environmentVariables`, but keeping shared gateway settings in the Claude Code user configuration avoids conflicting addresses or keys.

## 5) Open the panel and verify

Open Claude Code from the sidebar or toolbar, start a conversation, and send “Reply with one short greeting. Do not read or modify files.” Check the selected model and, where available, the gateway and authentication information in the status view.

An editor launched from the Dock or Start menu may not inherit temporary shell variables. Use the user settings above, or fully quit VS Code and start it with `code .` from the configured terminal.

## 6) Review billing and troubleshoot

Note the request time, key name, and model ID. Filter [UNEXHub Request Logs](https://unexhub.ai/console/log) using those values, then open Details → Billing Details and review Final Charge. Retries, helper models, and tool-use loops may create multiple requests. See [Billing records and exports](billing.md) to export a statement.

If prompted for an official login, check gateway configuration and the extension login setting. For 401, check the key and authentication method. For 404, check Messages support and the root address. The standalone CLI and bundled extension CLI may have different versions; record both when troubleshooting.

## References

- [PoloAPI](https://poloapi.apifox.cn/8239570m0)
- [Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
