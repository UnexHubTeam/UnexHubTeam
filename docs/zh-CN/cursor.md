# Cursor

<!-- DOCS-NAV:START -->
[English (primary)](../en/cursor.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）安装并打开 Cursor](#section-1)
2. [2）检查自定义地址入口](#section-2)
3. [3）填写密钥、Base URL 和模型](#section-3)
4. [4）验证连接](#section-4)
5. [5）查看计费与功能边界](#section-5)
6. [参考资料](#section-6)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页配置 Cursor 的自定义模型聊天，使用 UNEXHub Key 查询费用。Cursor 内置补全和其他功能的支持范围，以当前版本及套餐为准。

<a id="section-1"></a>
## 1）安装并打开 Cursor

从 [Cursor 官网](https://cursor.com/)安装，打开项目，再进入「Cursor Settings → Models」。准备专用 UNEXHub Key 与可用的 Chat Completions 模型 ID。

<a id="section-2"></a>
## 2）检查自定义地址入口

在 OpenAI 配置区域查找 **Override OpenAI Base URL** 或同义的自定义地址选项。当前官方 BYOK 说明确认支持 API Key，但未在该说明页明确保证任意自定义 Base URL。

如果你的版本没有自定义地址选项，不能仅把 UNEXHub Key 填入官方 OpenAI 密钥栏。可在 Cursor 集成终端使用 [Aider](aider.md)，或按所需协议使用 [Claude Code](claude-code.md)／[Codex](codex.md)。

<a id="section-3"></a>
## 3）填写密钥、Base URL 和模型

在支持自定义地址的版本中填写：

| 字段 | 内容 |
| --- | --- |
| OpenAI API Key | 完整 UNEXHub Key，不加 `Bearer`。 |
| Override OpenAI Base URL | `https://api.unexhub.ai/v1` |
| Model | 当前路由支持的准确模型 ID。 |

保存配置。若需手动添加模型，点击 `Add Model`，输入准确 ID 并启用。配置界面的地址应为 Base URL，不能填完整 `/chat/completions`。

<a id="section-4"></a>
## 4）验证连接

点击 `Verify` 或当前版本对应的验证入口。若验证使用固定模型而报模型不可用，核对该模型是否在 UNEXHub 开放，再使用你已配置的模型测试。

打开 Chat 面板，选择该模型，发送「只回复一句问候，不读取或修改文件」。验证请求本身也可能计费。

<a id="section-5"></a>
## 5）查看计费与功能边界

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

官方说明中，自带 API Key 适用于聊天模型，Tab 补全继续使用 Cursor 内置模型。Cursor 套餐费用和 UNEXHub 模型费用分别核对，不要因为配置了 Key 就假定所有编辑器功能都改走 UNEXHub。

<a id="section-6"></a>
## 参考资料

- [Cursor API keys](https://cursor.com/help/models-and-usage/api-keys)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：Cherry Studio](cherry-studio.md) · [中文目录](README.md) · [下一篇：Windsurf →](windsurf.md)
<!-- DOCS-PAGER:END -->
