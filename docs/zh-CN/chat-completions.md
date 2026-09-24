# 创建聊天补全

<!-- DOCS-NAV:START -->
[English (primary)](../en/chat-completions.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [接口地址](#section-1)
2. [请求头](#section-2)
3. [请求体](#section-3)
4. [请求示例：cURL](#section-4)
5. [请求示例：Python](#section-5)
6. [响应说明](#section-6)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 界面核对：2026-09-22

通过 Chat Completions 接口向支持该协议的文本模型发送消息。本页展示最小的非流式请求。

<a id="section-1"></a>
## 接口地址

```http
POST https://api.unexhub.ai/v1/chat/completions
```

SDK Base URL：`https://api.unexhub.ai/v1`。

<a id="section-2"></a>
## 请求头

| 名称 | 值 | 必填 |
| --- | --- | --- |
| `Authorization` | `Bearer YOUR_API_KEY` | 是 |
| `Content-Type` | `application/json` | 是 |

`YOUR_API_KEY` 替换为已启用且未过期的 UNEXHub Key，创建方法见[快速上手](quickstart.md)。

<a id="section-3"></a>
## 请求体

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 必填。当前可用的准确模型 ID。 |
| `messages` | array | 必填。对话消息数组。 |
| `messages[].role` | string | 本例为 `user`，表示用户消息。 |
| `messages[].content` | string | 本例使用文本提示词。 |
| `stream` | boolean | 本例显式设为 `false`，一次性返回结果。 |

```json
{
  "model": "YOUR_MODEL_ID",
  "messages": [
    {"role": "user", "content": "Reply with one short greeting."}
  ],
  "stream": false
}
```

<a id="section-4"></a>
## 请求示例：cURL

替换密钥和模型 ID 后，在 Bash 兼容终端执行。`-i` 会同时打印响应头，便于记录请求标识（如有）。

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

<a id="section-5"></a>
## 请求示例：Python

安装依赖，并设置上面示例中的 `UNEXHUB_API_KEY`、`UNEXHUB_BASE_URL` 环境变量：

```bash
python3 -m pip install openai
```

将以下内容保存为 `call_model.py`，替换 `YOUR_MODEL_ID`，执行 `python3 call_model.py`。

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UNEXHUB_API_KEY"],
    base_url=os.environ["UNEXHUB_BASE_URL"],
    max_retries=0,
)
response = client.chat.completions.create(
    model="YOUR_MODEL_ID",
    messages=[{
        "role": "user",
        "content": "Reply with one short greeting."
    }],
    stream=False,
)
print(response.choices[0].message.content)
print(response.usage)
```

示例关闭 SDK 自动重试，便于首次调用后逐笔核对日志。两种语言示例任选一种即可。

<a id="section-6"></a>
## 响应说明

成功时通常返回 HTTP 200。以下是响应字段示意，非实际调用结果；其他字段及用量明细以实际响应为准。

```json
{
  "choices": [
    {"message": {"role": "assistant", "content": "Hello!"}}
  ],
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 9,
    "total_tokens": 17
  }
}
```

| 字段 | 用途 |
| --- | --- |
| `choices[0].message.content` | 读取文本回复。 |
| `usage.prompt_tokens` | 输入 token 数，如有返回。 |
| `usage.completion_tokens` | 输出 token 数，如有返回。 |
| `usage.total_tokens` | 总 token 数，如有返回。 |

响应中的 token 用量不能直接当成扣费金额。调用后进入[计费记录](billing.md)核对最终扣费；错误排查见[常见问题](faq.md)。

其他可选参数、流式响应及不同模型协议，请查阅模型详情和 [协议兼容说明](compatibility.md)。

<!-- DOCS-PAGER:START -->

---

[← 上一篇：协议兼容说明](compatibility.md) · [中文目录](README.md) · [下一篇：第三方路由 →](third-party-routing.md)
<!-- DOCS-PAGER:END -->
