# Chatbox 接入教程

[文档目录](README.md) · 简体中文 | [English](../en/chatbox.md)

适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

准备好 UNEXHub Key 和当前可用的模型 ID；创建方法见[快速上手](quickstart.md)。需要使用第三方渠道时，选择[第三方路由 Key](third-party-routing.md)。

本教程以 Chatbox 网页版的内置 OpenAI 配置为例，使用 OpenAI 兼容的 Chat Completions 接口。

## 1）打开 Chatbox

进入 [Chatbox 网页版](https://web.chatboxai.app/)，或打开已安装的桌面客户端。

## 2）打开设置，选择模型服务商

点击左下角「Settings」，进入「Model Provider」，选择「OpenAI」。

如果已有 OpenAI 配置需要保留，可选择「Add → Add Custom Provider」，名称填 `UNEXHub`，API Mode 选择 `OpenAI API Compatible`。不同版本的自定义配置字段可能不同，请核对最终请求地址。

## 3）填写 API Host 和 API Key

| 配置项 | 填写值 |
| --- | --- |
| API Key | 完整 UNEXHub Key，不加 `Bearer`。 |
| API Host | `https://api.unexhub.ai`，不加 `/v1`。 |
| Preview | 应显示 `https://api.unexhub.ai/v1/chat/completions`。 |

确认 Preview 没有出现 `/v1/v1` 或缺少 `/chat/completions`。

## 4）添加模型，测试并保存

在模型区域点击「New」，将 UNEXHub 模型详情中的准确标识填入 Model ID。点击「Test Model」验证后，点击「Save」；测试可能产生费用。

也可以尝试「Fetch」获取模型，但仍需核对模型是否适用于当前账户和路由。

## 5）关闭设置，选择模型

关闭设置或按 Esc，新建对话，在「Select Model」中选择刚配置的服务和模型。

## 6）发送消息并确认回复

发送「请用一句话打招呼」。收到回复后，记下调用时间、Key 名称和模型 ID；失败时检查 Key、API Host、Preview 和模型状态。

## 7）在 UNEXHub 查看计费记录

打开[调用日志](https://unexhub.ai/console/log)，按 Key 名称、模型和时间查找请求，在详情中查看「最终扣费」。

![调用日志中的时间范围、类型、筛选与查询入口](../../assets/log-filters.png)

一条聊天消息可能触发模型测试、重试或其他额外请求，客户端估算也可能与最终扣费不同。UNEXHub API 费用与 Chatbox 自身订阅费用分别核对。账单导出见[计费记录与账单导出](billing.md)。
