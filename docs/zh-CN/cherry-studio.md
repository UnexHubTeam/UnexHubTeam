# Cherry Studio 接入教程

<!-- DOCS-NAV:START -->
[English (primary)](../en/cherry-studio.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）安装 Cherry Studio，打开设置](#section-1)
2. [2）添加自定义服务商](#section-2)
3. [3）填写 API Key 和 API 地址](#section-3)
4. [4）添加模型](#section-4)
5. [5）填写准确的模型 ID，并启用服务商](#section-5)
6. [6）返回聊天页面，选择模型](#section-6)
7. [7）在 UNEXHub 查看计费记录](#section-7)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

准备好 UNEXHub Key 和当前可用的模型 ID；创建方法见[快速上手](quickstart.md)。需要通过第三方渠道调用时，先创建[第三方路由 Key](third-party-routing.md)。

本教程使用支持 Chat Completions 的文本模型，按“安装 → 添加服务商 → 填写地址和 Key → 添加模型 → 选择模型 → 对话”的顺序操作。

<a id="section-1"></a>
## 1）安装 Cherry Studio，打开设置

安装并启动 Cherry Studio，进入「设置 → 模型服务」，点击添加服务商。菜单名称可能因版本略有不同，可参考 [Cherry Studio 官方配置说明](https://docs.cherryai.com.cn/pre-basic/providers/providers)。

<a id="section-2"></a>
## 2）添加自定义服务商

名称填写 `UNEXHub`，配置 OpenAI 兼容端点。旧版如果显示「提供商类型」，选择 OpenAI。

选择协议时，以 UNEXHub 所选模型实际支持的接口为准，不要仅凭模型品牌选择其他协议。

<a id="section-3"></a>
## 3）填写 API Key 和 API 地址

| 配置项 | 填写值 |
| --- | --- |
| 服务商名称 | `UNEXHub` |
| API 密钥 | 完整 UNEXHub Key，只填密钥，不加 `Bearer`。 |
| API 地址 | `https://api.unexhub.ai` |

常规聊天配置使用根地址，由 Cherry Studio 补全 `/v1/chat/completions`。如果当前版本明确要求 SDK Base URL，则填 `https://api.unexhub.ai/v1`。

最终请求地址应为：

```text
https://api.unexhub.ai/v1/chat/completions
```

<a id="section-4"></a>
## 4）添加模型

点击「获取模型列表」，找到需要的模型，点击旁边的「+」加入列表。若获取失败且版本支持手动添加，点击添加模型，继续填写下一步中的模型 ID。

<a id="section-5"></a>
## 5）填写准确的模型 ID，并启用服务商

将 [UNEXHub 模型详情](https://unexhub.ai/market?tab=models)中的准确 ID 填入模型 ID 字段。显示名称可自行设置，实际发送的模型 ID 必须保持一致。

确认添加后，打开服务商的启用开关。点击「检测」并选择模型验证配置；检测可能产生 API 费用。

<a id="section-6"></a>
## 6）返回聊天页面，选择模型

新建对话，在模型选择器中选择 `UNEXHub` 下的模型，发送「请用一句话打招呼」。收到回复后，记下测试时间、Key 名称和模型 ID。

<a id="section-7"></a>
## 7）在 UNEXHub 查看计费记录

打开[调用日志](https://unexhub.ai/console/log)，按日期、Key 名称和模型筛选。打开请求详情 → 计费详情，核对「最终扣费」。

![调用日志中的时间范围、类型、筛选与查询入口](../../assets/log-filters.png)

模型检测、自动重试和标题生成可能产生额外调用；请一起核对。完整流程见[计费记录与账单导出](billing.md)，连接失败见[常见问题](faq.md)。

<!-- DOCS-PAGER:START -->

---

[← 上一篇：Chatbox](chatbox.md) · [中文目录](README.md) · [下一篇：Cursor →](cursor.md)
<!-- DOCS-PAGER:END -->
