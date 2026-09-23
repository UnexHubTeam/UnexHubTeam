# VS Code 安装 Claude Code 教程

[English (primary)](../en/vscode-claude-code.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

使用 Anthropic 发布的官方 VS Code 扩展，在编辑器内通过 UNEXHub 调用模型。

> 直连接入需确认 UNEXHub 支持 Anthropic Messages。相关条件见[协议兼容说明](compatibility.md)。当前官方扩展自带用于聊天面板的 CLI；只有在终端使用 `claude` 时才需要另装独立 CLI。

## 1）安装 VS Code

从 [VS Code 官网](https://code.visualstudio.com/)安装对应系统版本，然后打开一个测试项目文件夹。

## 2）打开扩展，安装官方 Claude Code

macOS 按 `Cmd+Shift+X`，Windows 按 `Ctrl+Shift+X`。搜索 `Claude Code`，核对发布者为 **Anthropic**、扩展标识为 `anthropic.claude-code`，然后安装。

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

## 4）设置扩展并重新加载窗口

打开 VS Code 用户设置，搜索 `Claude Code login`。配置第三方网关时，按官方扩展说明启用 **Disable Login Prompt**，然后执行命令面板中的 `Developer: Reload Window`。

扩展支持 `claudeCode.environmentVariables`，但共享网关配置建议统一放在 Claude Code 用户设置中，避免两个位置出现不同地址或密钥。

## 5）打开面板并验证

打开 Claude Code 侧栏或工具栏入口，新建会话，发送「只回复一句问候，不读取或修改文件」。确认所选模型正确，并核对状态中显示的网关和鉴权信息（若版本提供）。

若只在终端设置了临时环境变量，从 Dock 或开始菜单启动的 VS Code 可能无法读取它们；使用上面的用户级设置，或完全退出 VS Code 后从已设置变量的终端执行 `code .`。

## 6）查看计费与排错

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

提示登录官方账号时检查网关配置与扩展登录设置；401 检查密钥和鉴权方式；404 检查 Messages 支持与根地址。单独的 CLI 版本与扩展内置版本可能不同，排错时记录两者版本。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/8239570m0)
- [Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
