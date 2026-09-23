# 第三方路由接入教程

[文档目录](README.md) · 简体中文 | [English](../en/third-party-routing.md)

适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

第三方路由决定 UNEXHub 将请求转发到哪类上游渠道。Cherry Studio、Chatbox 是第三方客户端；两者可以配合使用，客户端也可以使用其他路由策略的 Key。

## 1）创建第三方路由 Key

打开 [API 密钥](https://unexhub.ai/console/token) →「用户视图」（如显示）→「创建 Key」。

填写用途名称，例如 `cherry-thirdparty` 或 `chatbox-thirdparty`，设置有效期和渠道折扣，在「路由策略」中选择「第三方路由」，然后创建。

![创建 API Key 时选择第三方路由](../../assets/third-party-routing.png)

截图中的名称为表单示例。建议为每个客户端单独创建 Key，创建后确认「已启用」，复制密钥，并设置预算上限。

## 2）选择可用模型

进入[交易中心](https://unexhub.ai/market?tab=models)，查看模型状态、协议和价格。选择当前路由支持的模型，复制准确 ID。

如果页面提供供应商或渠道对比，可同时比较可用性与价格。渠道折扣条件过严可能减少可用渠道；第三方路由并不保证始终更便宜或始终可用。

## 3）填写接入信息

| 配置 | 填写值 |
| --- | --- |
| API 根地址 | `https://api.unexhub.ai` |
| SDK Base URL | `https://api.unexhub.ai/v1` |
| 完整聊天端点 | `https://api.unexhub.ai/v1/chat/completions` |
| API Key | 第 1 步创建的 UNEXHub Key。 |
| 模型 ID | 第 2 步复制的当前可用模型 ID。 |

第三方路由由 UNEXHub 处理，继续使用 UNEXHub 地址和 Key。无需把地址换成上游服务商，也无需填写上游服务商的 Key。

## 4）发起调用

按照[快速上手](quickstart.md)中的 cURL 示例，或使用 [Cherry Studio](cherry-studio.md)、[Chatbox](chatbox.md)，发送一次简短请求，例如「请用一句话打招呼」。

请求流程：代码或客户端 → UNEXHub 鉴权与路由 → 可用的第三方渠道 → 返回模型结果。

## 5）查看第三方调用与扣费

进入[调用日志](https://unexhub.ai/console/log)，按专用 Key 名称、模型和时间筛选。打开详情，核对「最终扣费」；如果详情显示渠道信息，同时核对该字段。

![调用日志中的时间范围、类型、筛选与查询入口](../../assets/log-filters.png)

客户端的检测、模型测试、自动重试、标题生成和多模型回复可能产生额外请求，历史对话也可能增加输入量。一条可见消息不一定只对应一笔请求。

费用以 UNEXHub 的最终扣费为准；客户端自身订阅费用需另行核对。详见[计费记录与账单导出](billing.md)。
