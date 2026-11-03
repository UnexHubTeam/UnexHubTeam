# Agent APIs: wallet

[Agent API reference](README.md) · [Documentation home](../README.md) · [简体中文](../../zh-CN/agent-api/wallet.md)

Updated: 2026-11-04

## On this page

- [Get the current user's balance](#balance)

<a id="balance"></a>
## Get the current user's balance

```http
GET /api/agents/managed/quota
```

From the Agent backend, use the same injected key and [authentication](README.md#authentication-and-urls) as the profile API. The response describes the key owner's wallet, rather than a separate allowance for this API key. No user ID parameter is required.

```bash
curl "${UNEX_API_BASE_URL%/v1}/api/agents/managed/quota" \
  --header "Authorization: Bearer ${UNEX_API_KEY}"
```

Example response with fictional values:

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

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | integer | Current platform user ID |
| `quota` | integer | Recharge balance in platform quota units |
| `gift_quota` | integer | Gift balance in platform quota units |
| `gift_expire_time` | integer | Gift expiry timestamp, in Unix seconds |
| `total` | integer | Combined balance: `quota + gift_quota` |

Quota values are **not currency amounts or cents**. Use the platform's published conversion rules for monetary displays; do not hard-code a conversion rate. The balance can change through other concurrent usage, so it does not guarantee that a later request will succeed.

Refresh when the user opens a balance view or after a request finishes. Handle [query failures](README.md#responses-and-errors) separately from a zero balance. Responses use `Cache-Control: no-store`.

---

[← User identity](users.md) · [Agent API reference](README.md)
