# Agent API：用户身份

[Agent API 参考](README.md) · [中文目录](../README.md) · [English (primary)](../../en/agent-api/users.md)

更新日期：2026-11-04

使用平台用户 ID 关联应用内的用户记录；用户名和昵称可能变化。

## 本页目录

- [读取用户 ID](#user-id)
- [获取当前用户资料](#current-user)

<a id="user-id"></a>
## 读取用户 ID

模式 A / B 启动时向容器后端注入 `UNEX_USER_ID`，直接读取即可，无需调用接口。例如 Python：

```python
import os

user_id = os.environ["UNEX_USER_ID"]
```

环境变量为字符串；用户资料和余额接口也会以数字形式返回同一用户的 `data.id`。同一平台用户重新创建实例后，用户 ID 保持不变。浏览器传入的用户 ID 不能作为身份凭据。

<a id="current-user"></a>
## 获取当前用户资料

```http
GET /api/agents/managed/user
```

按[鉴权与请求地址](README.md#authentication-and-urls)使用注入的托管 Key。接口读取 Key 所属用户的最新资料，不接受指定其他用户的参数。

```bash
curl "${UNEX_API_BASE_URL%/v1}/api/agents/managed/user" \
  --header "Authorization: Bearer ${UNEX_API_KEY}"
```

响应示例，数据为虚构值：

```json
{
  "success": true,
  "message": "",
  "data": {
    "id": 42,
    "username": "alice",
    "display_name": "爱丽丝"
  }
}
```

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `id` | integer | 平台用户 ID |
| `username` | string | 用户名 |
| `display_name` | string | 昵称 |

Key 及用户、Agent 的访问权限必须保持有效，Key 撤销或实例停止后不能继续查询。资料变更后再次请求即可刷新，响应带有 `Cache-Control: no-store`。

---

[← Agent API 参考](README.md) · [钱包余额 →](wallet.md)
