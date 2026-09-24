# VS Code 安装 Claude Code 教程

<!-- DOCS-NAV:START -->
[English (primary)](../en/vscode-claude-code.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）安装 VS Code](#section-1)
2. [2）打开扩展，安装官方 Claude Code](#section-2)
3. [3）配置 UNEXHub](#section-3)
4. [4）设置扩展并重新加载窗口](#section-4)
5. [5）打开面板并验证](#section-5)
6. [6）查看计费与排错](#section-6)
7. [参考资料](#section-7)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

使用 Anthropic 发布的官方 VS Code 扩展，在编辑器内通过 UNEXHub 调用模型。

> 直连接入需确认 UNEXHub 支持 Anthropic Messages。相关条件见[协议兼容说明](compatibility.md)。当前官方扩展自带用于聊天面板的 CLI；只有在终端使用 `claude` 时才需要另装独立 CLI。

<a id="section-1"></a>
## 1）安装 VS Code

从 [VS Code 官网](https://code.visualstudio.com/)安装对应系统版本，然后打开一个测试项目文件夹。

<a id="section-2"></a>
## 2）打开扩展，安装官方 Claude Code

macOS 按 `Cmd+Shift+X`，Windows 按 `Ctrl+Shift+X`。搜索 `Claude Code`，核对发布者为 **Anthropic**、扩展标识为 `anthropic.claude-code`，然后安装。

<a id="section-3"></a>
## 3）配置 UNEXHub

先创建专用 UNEXHub Key，确认可用的 Messages 模型 ID。打开用户级 `~/.claude/settings.json`（Windows 为 `%USERPROFILE%\.claude\settings.json`），将下面 `env` 字段合并到原有 JSON：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.unexhub.ai",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CLAUDE_MODEL_ID"
  }
}
```

替换密钥和模型占位符。不要把配置写入会提交到仓库的 `.vscode/settings.json` 或 `.claude/settings.json`。

<a id="section-4"></a>
## 4）设置扩展并重新加载窗口

打开 VS Code 用户设置，搜索 `Claude Code login`。配置第三方网关时，按官方扩展说明启用 **Disable Login Prompt**，然后执行命令面板中的 `Developer: Reload Window`。

扩展支持 `claudeCode.environmentVariables`，但共享网关配置建议统一放在 Claude Code 用户设置中，避免两个位置出现不同地址或密钥。

<a id="section-5"></a>
## 5）打开面板并验证

打开 Claude Code 侧栏或工具栏入口，新建会话，发送「只回复一句问候，不读取或修改文件」。确认所选模型正确，并核对状态中显示的网关和鉴权信息（若版本提供）。

若只在终端设置了临时环境变量，从 Dock 或开始菜单启动的 VS Code 可能无法读取它们；使用上面的用户级设置，或完全退出 VS Code 后从已设置变量的终端执行 `code .`。

<a id="section-6"></a>
## 6）查看计费与排错

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

提示登录官方账号时检查网关配置与扩展登录设置；401 检查密钥和鉴权方式；404 检查 Messages 支持与根地址。单独的 CLI 版本与扩展内置版本可能不同，排错时记录两者版本。

<a id="section-7"></a>
## 参考资料

- [Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：Claude Code](claude-code.md) · [中文目录](README.md) · [下一篇：安装 Codex →](codex-install.md)
<!-- DOCS-PAGER:END -->
