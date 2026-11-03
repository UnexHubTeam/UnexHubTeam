# Agent API：钱包

[Agent API 参考](README.md) · [中文目录](../README.md) · [English (primary)](../../en/agent-api/wallet.md)

更新日期：2026-11-04

## 本页目录

- [获取当前用户余额](#balance)

<a id="balance"></a>
## 获取当前用户余额

```http
GET /api/agents/managed/quota
```

由 Agent 后端使用与用户资料接口相同的注入 Key 和[鉴权方式](README.md#authentication-and-urls)。返回 Key 所属用户的钱包余额，不是这把 API Key 的独立限额；无需传入用户 ID。

```bash
curl "${UNEX_API_BASE_URL%/v1}/api/agents/managed/quota" \
  --header "Authorization: Bearer ${UNEX_API_KEY}"
```

响应示例，数据为虚构值：

```json
{
  "success": true,
  "message": "",
  "data": {
    "id": 42,
    "quota": 1000000,
    "gift_quota": 200000,
    "gift_expire_time": 1795000000,
    "total": 1200000
  }
}
```

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `id` | integer | 当前平台用户 ID |
| `quota` | integer | 充值余额，平台额度单位 |
| `gift_quota` | integer | 赠送余额，平台额度单位 |
| `gift_expire_time` | integer | 赠送额度到期时间，Unix 秒时间戳 |
| `total` | integer | 合计余额：`quota + gift_quota` |

额度值**不是货币金额或分**。展示金额时应遵循平台公布的换算规则，不要硬编码兑换比例。其他并发使用可能改变余额，本次查询不能保证后续请求一定成功。

可在用户打开余额页面或请求完成后刷新。将[查询失败](README.md#responses-and-errors)与零余额分别处理，响应带有 `Cache-Control: no-store`。

---

[← 用户身份](users.md) · [Agent API 参考](README.md)
