# 站点操作指南-快速上手调用大模型 API

[English (primary)](../en/quickstart.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

API Base URL：[https://api.unexhub.ai/](https://api.unexhub.ai/)

新用户先完成注册、登录，再按下面的步骤调用模型。

**API 调用流程：** 注册用户 → 充值余额 → 创建 API Key → 选择路由策略 → 设置有效期和预算 → 选择模型 → 发起调用 → 查看计费记录。

**API 接入信息 = URL + API Key。** 调用时还需要准确的模型 ID，可从交易中心的模型详情页复制。

| 配置 | 填写值                                                  |
| --- |---------------------------------------------------------|
| API 根地址 | `https://api.unexhub.ai`                                |
| SDK Base URL | `https://api.unexhub.ai/v1`                             |
| API Key | 你创建的完整密钥；示例中以 `YOUR_API_KEY` 代替。        |
| 模型 ID | 当前可用的准确模型标识；示例中以 `YOUR_MODEL_ID` 代替。 |

## 1）充值

进入控制台 → 个人中心 → [资金账户](https://unexhub.ai/console/topup)，确认账户有可用余额。

余额不足时点击「充值」，按页面提示选择金额并完成支付。返回资金账户确认已入账，再开始调用。

![资金账户中的充值与明细导出入口](../../assets/funds-entry.png)

## 2）创建 API Key

### a. 进入 API 密钥，点击创建 Key

打开控制台 → [API 密钥](https://unexhub.ai/console/token)。如果页面显示视图切换，先选择「用户视图」，再点击「创建 Key」。

![API 密钥页面中的用户视图与创建 Key 入口](../../assets/api-keys-entry.png)

### b. 填写名称、有效期和路由策略

名称可填 `demo-api-test`，然后选择有效期、渠道折扣和路由策略，确认后点击「创建」。

![创建 API Key：名称、有效期、渠道折扣与路由策略](../../assets/create-key.png)

| 配置项 | 说明 |
| --- | --- |
| 名称 | 建议按项目或客户端命名，方便查找消费记录。 |
| 有效期 | 按需要选择永不过期、30 天、90 天或 1 年。 |
| 渠道折扣 | 通过滑块设置条件；可用渠道和价格以当前页面为准。 |
| 路由策略 | 可选自动路由、官方路由、第三方路由。 |

自动路由会综合价格、可用性和响应情况选择渠道；页面提示需申请时，先完成开通。官方路由和第三方路由的价格、可用性可能不同。第三方渠道的完整操作见[第三方路由接入教程](third-party-routing.md)。

### c. 检查密钥状态并设置预算

返回 Key 列表，确认新 Key 已出现且为「已启用」，点击「复制密钥」。在 Key 卡片的「预算上限」中，可设置每日、每月或总额上限。

将密钥保存到环境变量或密钥管理工具中。不要把真实密钥提交到 GitHub，也不要写入公开网页前端。不同应用使用不同 Key，便于查询和控制费用。

### d. 在交易中心选择模型

打开[交易中心 → 模型](https://unexhub.ai/market?tab=models)，搜索需要的模型，核对可用状态和价格，再进入详情。

### e. 复制准确的模型 ID，查看协议和代码

从模型详情页复制模型 ID，注意大小写、连字符和版本后缀。确认模型支持本教程使用的 Chat Completions 接口。

![模型详情页中的模型 ID 与协议位置](../../assets/model-details.png)

> 图中 `gpt-5.5` 仅演示模型详情位置，核对时「开始使用」不可用。请从交易中心选择当前账户及路由可用的模型，不要直接照抄截图中的模型名称或价格。

## 3）获取中转信息

打开所选模型详情 →「代码」，查看接入地址与调用格式。模型代码示例使用：

```text
Base URL: https://api.unexhub.ai/v1
API Key:  YOUR_API_KEY
```

![模型代码示例中的 Base URL 与密钥占位符](../../assets/model-code.png)

> 截图用于说明 `base_url` 与 `api_key` 的位置。实际运行时替换密钥和模型 ID。

网站与控制台使用 `https://unexhub.ai/`；API 调用使用 `https://api.unexhub.ai/v1`。不要将网站地址填入 `base_url`。

## 4. 使用方法

API Key 放在 HTTP Header 中：

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

以下示例用于支持 Chat Completions 的文本模型。替换 `YOUR_API_KEY` 和 `YOUR_MODEL_ID`，在 macOS、Linux 或兼容 Bash 的终端运行。成功调用会按实际用量计费。

```bash
export UNEXHUB_API_KEY='YOUR_API_KEY'
export UNEXHUB_BASE_URL='https://api.unexhub.ai/v1'

curl -sS -i "$UNEXHUB_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $UNEXHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "YOUR_MODEL_ID",
    "messages": [
      {"role": "user", "content": "Reply with one short greeting."}
    ],
    "stream": false
  }'
```

正常返回时，可在 JSON 的 `choices[0].message.content` 中读取模型回复。`usage` 如有返回，可用于查看输入、输出和总 token 用量。

Python 示例和参数说明见[创建聊天补全](chat-completions.md)。使用客户端可直接参考 [Cherry Studio 接入教程](cherry-studio.md)或 [Chatbox 接入教程](chatbox.md)。

## 5）替换 API 地址

已有 OpenAI 兼容代码时，把原先的 API 地址替换为 UNEXHub 对应地址，同时更换 Key 和模型 ID。

| 接入方式 | 应填写的地址 |
| --- | --- |
| Python SDK 的 `base_url` | `https://api.unexhub.ai/v1` |
| 直接发送 HTTP 请求 | `https://api.unexhub.ai/v1/chat/completions` |
| Cherry Studio 常规 API 地址 | `https://api.unexhub.ai`，由客户端补全路径。 |
| Chatbox 的 API Host | `https://api.unexhub.ai`，不加 `/v1`。 |

最终聊天请求应到达 `/v1/chat/completions`。如果客户端明确要求 SDK Base URL，则填到 `/v1`，避免出现 `/v1/v1`。

其他协议、图像、音频和视频接口，请以所选模型详情及 [协议兼容说明](compatibility.md)为准。

## 6）查看计费记录

### a. 找到本次调用

进入控制台 → [调用日志](https://unexhub.ai/console/log)，选择覆盖调用时间的日期范围。成功请求可按「消费」筛选；排查失败时选择「全部」或「错误」。

点击「添加筛选」，按令牌名称、模型名称或 Request ID 定位，再点击「查询」。

![调用日志中的时间范围、类型、筛选与查询入口](../../assets/log-filters.png)

### b. 查看最终扣费

打开匹配记录的「详情」→「请求详情分析」→「计费详情」，核对模型、输入与输出用量和「最终扣费」。以最终扣费作为本次实际消费金额。

### c. 查询汇总与导出账单

进入[资金账户](https://unexhub.ai/console/topup)，按日期和「API 消费」筛选。点击「明细导出」→ 选择「当前筛选结果」或「全部记录」→ 确认记录数 →「导出 Excel」。

资金记录可能按日汇总；逐笔费用请查调用日志。详细解释见[查看计费记录与导出账单](billing.md)。

## 联系支持

遇到问题先查看[常见问题](faq.md)和[服务状态](https://unexhub.ai/status)。联系 [support@unexhub.com](mailto:support@unexhub.com) 时，提供调用时间及所在时区、模型、Key 名称、Request ID 和错误信息，不要发送完整密钥。
