# 常见问题

<!-- DOCS-NAV:START -->
[English (primary)](../en/faq.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）API 地址应该填什么？](#section-1)
2. [2）返回 401，或提示鉴权失败？](#section-2)
3. [3）账户有余额，为什么还提示额度不足？](#section-3)
4. [4）返回 400、404，或提示模型不存在？](#section-4)
5. [5）第三方路由与第三方客户端有什么区别？](#section-5)
6. [6）返回 429、5xx 或连接超时？](#section-6)
7. [7）调用成功，却找不到计费记录？](#section-7)
8. [8）为什么聊天一条消息出现多笔请求？](#section-8)
9. [9）最终扣费与客户端估算不同？](#section-9)
10. [10）怎样算完成首次接入？](#section-10)
11. [11）Claude Code 和 Codex 可以直接用聊天端点吗？](#section-11)
12. [12）Windows 设置环境变量后不生效？](#section-12)
13. [13）PowerShell 提示不能运行 npm 或 Codex 脚本？](#section-13)
14. [14）用了 CC Switch 还是协议错误？](#section-14)
15. [15）CC MAX 是不是 UNEXHub 的模型或套餐？](#section-15)
16. [16）编辑器没有自定义 Base URL，怎么办？](#section-16)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

<a id="section-1"></a>
## 1）API 地址应该填什么？

Python SDK 的 `base_url` 填 `https://api.unexhub.ai/v1`。直接 HTTP 请求使用 `https://api.unexhub.ai/v1/chat/completions`。

Cherry Studio 常规 API 地址和 Chatbox API Host 填根地址 `https://api.unexhub.ai`，由客户端补全路径。客户端版本若明确要求 SDK Base URL，则遵循该字段说明，避免 `/v1/v1`。

<a id="section-2"></a>
## 2）返回 401，或提示鉴权失败？

检查密钥是否完整、已启用、未过期，是否属于当前环境。直接 HTTP 调用使用 `Authorization: Bearer YOUR_API_KEY`；客户端密钥栏只填写 Key，不加 `Bearer`。

<a id="section-3"></a>
## 3）账户有余额，为什么还提示额度不足？

同时检查 Key 的每日、每月及总额预算上限。账户余额和 Key 预算限制是两个不同条件。

<a id="section-4"></a>
## 4）返回 400、404，或提示模型不存在？

核对完整接口路径、JSON 请求体和准确模型 ID。确认模型支持所用协议且当前可用；检查是否重复拼接 `/v1`。截图中的示例模型不保证可调用。

<a id="section-5"></a>
## 5）第三方路由与第三方客户端有什么区别？

路由决定 UNEXHub 使用哪类上游渠道；客户端是发送请求的应用。Cherry Studio、Chatbox 都可以使用第三方路由 Key，也可以使用其他路由 Key。上游切换由 UNEXHub 处理，客户端继续填写 UNEXHub 的地址和密钥。

<a id="section-6"></a>
## 6）返回 429、5xx 或连接超时？

429 时降低并发和调用频率，按服务端提示重试。5xx 或超时时，查看[服务状态](https://unexhub.ai/status)和调用日志。重试前先确认原请求是否已经完成和扣费。

具体原因以接口 `error` 信息和控制台记录为准。

<a id="section-7"></a>
## 7）调用成功，却找不到计费记录？

核对登录账户与 API 环境一致，扩大时间范围，清除多余筛选并刷新。使用 Key 名称、模型和调用时间组合查找。响应 `id` 不一定等于控制台 Request ID。

<a id="section-8"></a>
## 8）为什么聊天一条消息出现多笔请求？

客户端可能执行模型测试、自动重试、标题生成或多模型回复。历史对话也会影响输入量。逐笔核对日志，不要把聊天消息数直接当成调用次数。

<a id="section-9"></a>
## 9）最终扣费与客户端估算不同？

以 UNEXHub「请求详情分析 → 计费详情 → 最终扣费」为准。不同输入、输出、缓存价格及路由条件会影响费用。等价额度 token 是金额折算单位，不是模型处理的 token 数。

<a id="section-10"></a>
## 10）怎样算完成首次接入？

- Key 已启用，路由策略和预算符合需要。
- 代码或客户端返回模型回复。
- 调用日志能定位到本次请求。
- 已核对最终扣费，并计入模型测试或重试产生的额外请求。
- 需要对账时，已按正确时间范围导出账单。

<a id="section-11"></a>
## 11）Claude Code 和 Codex 可以直接用聊天端点吗？

Claude Code 需要 Anthropic Messages；Codex 当前需要 Responses。不能仅将它们的地址替换成 `/v1/chat/completions`。先确认 UNEXHub 对应协议支持；只有聊天接口时，可使用 [CC Switch](cc-switch.md)本地转换。详见[协议兼容说明](compatibility.md)。

<a id="section-12"></a>
## 12）Windows 设置环境变量后不生效？

`$env:变量名 = "值"` 只影响当前 PowerShell 和子进程；`setx` 写入用户变量，但不会更新当前窗口。重开终端后再启动工具。通过 Dock 或开始菜单打开的编辑器，也可能读不到终端临时变量。

<a id="section-13"></a>
## 13）PowerShell 提示不能运行 npm 或 Codex 脚本？

对于 npm 安装方式，可使用 `npm.cmd`、`codex.cmd` 或 `openclaw-cn.cmd`。本套教程不要求为这些包装脚本修改整个用户的执行策略。

<a id="section-14"></a>
## 14）用了 CC Switch 还是协议错误？

检查目标应用、API Format 或 Needs Local Routing、模型映射、本地代理运行状态及接管开关。只保存服务商配置不会自动完成协议转换。停止代理前先关闭接管并恢复所需配置。

<a id="section-15"></a>
## 15）CC MAX 是不是 UNEXHub 的模型或套餐？

尚未确认。仅凭名称不能认定 UNEXHub 已提供同名模型、套餐或特定版本限制。配置前请先核对 [CC MAX](cc-max.md)列出的信息。

<a id="section-16"></a>
## 16）编辑器没有自定义 Base URL，怎么办？

只有官方提供商 Key 字段时，不能默认把 UNEXHub Key 当作原厂 Key。查看 [Cursor](cursor.md)／[Windsurf](windsurf.md)的适用条件，或在集成终端按 [Aider](aider.md)教程接入。

继续阅读：[快速上手](quickstart.md) · [第三方路由](third-party-routing.md) · [计费记录](billing.md)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：计费记录](billing.md) · [中文目录](README.md) · [下一篇：Chatbox →](chatbox.md)
<!-- DOCS-PAGER:END -->
