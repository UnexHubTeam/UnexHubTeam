# Agent APIs: user identity

[Agent API reference](README.md) · [Documentation home](../README.md) · [简体中文](../../zh-CN/agent-api/users.md)

Updated: 2026-11-04

Use the platform user ID to associate application records with a user. Usernames and display names may change.

## On this page

- [Read the user ID](#user-id)
- [Get the current user's profile](#current-user)

<a id="user-id"></a>
## Read the user ID

Mode A and Mode B inject `UNEX_USER_ID` into the container backend. Read it directly without an API request, for example in Python:

```python
import os

user_id = os.environ["UNEX_USER_ID"]
```

The variable is a string; the profile and balance APIs return the same ID as numeric `data.id`. A new instance for the same platform user keeps that user's ID. A user ID supplied by a browser is not proof of identity.

<a id="current-user"></a>
## Get the current user's profile

```http
GET /api/agents/managed/user
```

Use the injected managed key as described in [Authentication and URLs](README.md#authentication-and-urls). The endpoint reads the key owner's current profile; it accepts no user-selection parameter.

```bash
curl "${UNEX_API_BASE_URL%/v1}/api/agents/managed/user" \
  --header "Authorization: Bearer ${UNEX_API_KEY}"
```

Example response with fictional values:

```json
{
  "success": true,
  "message": "",
  "data": {
    "id": 42,
    "username": "alice",
    "display_name": "Alice"
  }
}
```

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | integer | Platform user ID |
| `username` | string | Username |
| `display_name` | string | Display name |

The key and user/Agent access must remain valid. Revoked keys and stopped instances cannot use this endpoint. Query again to refresh changed profile information; responses use `Cache-Control: no-store`.

---

[← Agent API reference](README.md) · [Wallet balance →](wallet.md)
