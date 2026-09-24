# 客户端与协议兼容说明

<!-- DOCS-NAV:START -->
[English (primary)](../en/compatibility.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）地址与协议速查](#section-1)
2. [2）聊天、Responses 和 Messages 的区别](#section-2)
3. [3）如何确认一个工具已成功接入](#section-3)
4. [4）网站与 API 地址](#section-4)
5. [5）参考入口状态](#section-5)
6. [参考资料](#section-6)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

同一模型名称可能出现在不同协议中。接入前同时确认「工具支持的协议」「UNEXHub 开放的端点」「当前 Key 的模型与路由权限」。

<a id="section-1"></a>
## 1）地址与协议速查

| 工具／模式 | 配置地址 | 最终协议或端点 | 本文核对范围 |
| --- | --- | --- | --- |
| cURL / Python 聊天 | SDK 为 `https://api.unexhub.ai/v1` | `POST /v1/chat/completions` | 已核对模型代码示例；未执行付费调用。 |
| Chatbox | API Host 为 `https://api.unexhub.ai` | Chat Completions | 已核对配置字段。 |
| Cherry Studio | 自动补全模式为根地址 | Chat Completions | 已对照官方客户端说明。 |
| Aider | `OPENAI_API_BASE` 到 `/v1` | Chat Completions | 已对照官方兼容 API 文档。 |
| openclaw-cn | OpenAI Compatible 到 `/v1` | Chat Completions 与工具调用 | 已核对社区安装与配置文档，未运行 Agent。 |
| Claude Code / VS Code 扩展直连 | 根地址；仅限已确认的 Messages 网关 | Anthropic Messages，通常为 `/v1/messages` | 官方网关配置已核对；UNEXHub 端到端兼容待确认。 |
| Codex 直连 | Base URL 到 `/v1` | Responses，通常为 `/v1/responses` | 官方配置已核对；UNEXHub 端到端兼容待确认。 |
| CC Switch 转换 | 依目标应用、API Format 和完整 URL 模式设置 | 本地转换为上游 Chat Completions | 已对照项目手册；未实测 UNEXHub 转换。 |
| Cursor 原生 | 自定义 Base URL 到 `/v1` | 由客户端模型配置决定 | 需当前版本提供自定义地址入口。 |
| Windsurf 原生 | 由当前版本的明确支持决定 | 由内置助手决定 | 未确认任意网关支持，提供集成终端方案。 |
| CC MAX | 必须取得专用渠道实际地址 | 取决于渠道声明 | UNEXHub 同名渠道尚未确认。 |

“已核对文档／界面”表示配置依据经过查阅，不等同于所有客户端已完成实际模型调用。

<a id="section-2"></a>
## 2）聊天、Responses 和 Messages 的区别

Chat Completions 使用 `messages` 请求体，常见客户端包括 Chatbox、Cherry Studio 和 Aider。Codex 当前使用 Responses 协议；Claude Code 使用 Anthropic Messages。三者的请求字段、流式事件、工具调用与返回格式不同，单纯更换 URL 后缀无法完成转换。

如果上游只提供 Chat Completions，可选择直接支持它的工具，或使用已配置并运行的 [CC Switch 本地转换](cc-switch.md)。转换是客户端侧的额外步骤，不代表 UNEXHub 原生开放了其他协议。

<a id="section-3"></a>
## 3）如何确认一个工具已成功接入

1. 模型与路由已开放，当前 Key 有效且预算充足。
2. 工具的最终请求地址、协议和鉴权方式正确。
3. 一次简短请求返回模型内容。
4. UNEXHub 调用日志出现相应记录，并可查看最终扣费。
5. 编程工具所需的流式、工具调用、辅助模型等功能另行通过验证。

<a id="section-4"></a>
## 4）网站与 API 地址

网站与控制台使用 `https://unexhub.ai/`；API 根地址为 `https://api.unexhub.ai`，OpenAI 兼容 SDK Base URL 为 `https://api.unexhub.ai/v1`。不要将网站地址用作 API Base URL。

向支持人员确认尚未开放或未明确的协议时，提供工具名称、版本、模型 ID 和所需端点即可，不要发送完整密钥。

<a id="section-5"></a>
## 5）参考入口状态

官方 [UnexHub Public API 开发文档](https://documenter.getpostman.com/view/57297668/2sBYArUsxK)以 Postman 集合形式发布，可用于查看当前公开端点。文档中存在端点不代表每个模型、路由、Key 或客户端都已支持相应协议；接入前仍需核对模型详情与账户权限。

<a id="section-6"></a>
## 参考资料

- [Codex protocol reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Claude gateway requirements](https://code.claude.com/docs/en/llm-gateway)
- [CC Switch provider manual](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/2-providers/2.1-add.md)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：控制台完整操作](quickstart.md) · [中文目录](README.md) · [下一篇：聊天补全 API →](chat-completions.md)
<!-- DOCS-PAGER:END -->
