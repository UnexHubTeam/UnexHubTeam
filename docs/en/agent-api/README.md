# Agent API reference

[Documentation home](../README.md) · [Mode A](../agent-development-mode-a.md) · [Mode B](../agent-development-upload.md) · [简体中文](../../zh-CN/agent-api/README.md)

Updated: 2026-11-04

For the backend of a platform-launched Mode A or Mode B Agent. APIs are grouped by capability; each page describes its endpoints and response fields.

## API categories

| Category | Available operations |
| --- | --- |
| [User identity](users.md) | [Read the user ID](users.md#user-id) · [Query username and display name](users.md#current-user) |
| [Wallet](wallet.md) | [Query the current user's balance](wallet.md#balance) |

## Authentication and URLs

The platform supplies these variables to the container backend:

| Variable | Purpose |
| --- | --- |
| `UNEX_API_KEY` | Managed API key for the current user's Agent instance |
| `UNEX_API_BASE_URL` | Model API base URL, ending in `/v1` |
| `UNEX_USER_ID` | Current platform user ID, as a string |

Send `Authorization: Bearer <UNEX_API_KEY>`. The APIs below use `/api/agents/...`, so remove the trailing `/v1` from `UNEX_API_BASE_URL` before appending the endpoint path. No new environment variables or developer secret are needed.

Read the injected variables in the backend. Keep the key out of images, frontend bundles, browser responses, and logs. If variables are missing, confirm that the application was started through the platform; do not substitute a personal key. Model access and deployment requirements are described in the mode guides.

## Responses and errors

Successful responses contain `success: true` and a `data` object. Read the documented fields and tolerate additional fields. All operations in this reference are read-only.

Check both the HTTP status and `success`; do not treat a failed query as an empty profile or a zero balance.

| Result | Action |
| --- | --- |
| `401` / `403` | Check the key and current user/Agent access; do not retry indefinitely |
| `404` | Check the URL and API availability with platform support |
| `429` | Back off before retrying |
| `5xx` | Show temporary unavailability and retry with a limit |

---

[← Mode B guide](../agent-development-upload.md) · [Documentation home](../README.md) · [User identity →](users.md)
