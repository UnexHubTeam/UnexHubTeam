# Agent API 参考

[中文目录](../README.md) · [模式 A](../agent-development-mode-a.md) · [模式 B](../agent-development-upload.md) · [English (primary)](../../en/agent-api/README.md)

更新日期：2026-11-04

适用于通过平台启动的模式 A / B Agent 后端。接口按能力分类，各专题分别说明端点与响应字段。

## 接口分类

| 分类 | 可用能力 |
| --- | --- |
| [用户身份](users.md) | [读取用户 ID](users.md#user-id) · [查询用户名与昵称](users.md#current-user) |
| [钱包](wallet.md) | [查询当前用户余额](wallet.md#balance) |

<a id="authentication-and-urls"></a>
## 鉴权与请求地址

平台向容器后端提供以下变量：

| 变量 | 用途 |
| --- | --- |
| `UNEX_API_KEY` | 当前用户 Agent 实例的托管 API Key |
| `UNEX_API_BASE_URL` | 模型 API 基址，以 `/v1` 结尾 |
| `UNEX_USER_ID` | 当前平台用户 ID，字符串形式 |

请求携带 `Authorization: Bearer <UNEX_API_KEY>`。以下接口使用 `/api/agents/...` 路径，应先移除 `UNEX_API_BASE_URL` 末尾的 `/v1`，再拼接端点路径。无需新增环境变量或开发者密钥。

变量由后端读取，Key 不进入镜像、前端构建、浏览器响应或日志。变量缺失时，请确认应用是否由平台启动，不要改用个人 Key。模型接入与部署要求见对应模式指南。

<a id="responses-and-errors"></a>
## 响应与错误处理

成功响应包含 `success: true` 和 `data` 对象。读取已说明的字段，并兼容后续新增字段。本参考中的接口均为只读。

同时检查 HTTP 状态和 `success`；查询失败时不要显示为空用户或零余额。

| 结果 | 建议处理 |
| --- | --- |
| `401` / `403` | 检查 Key 及当前用户、Agent 的访问权限，不无限重试 |
| `404` | 检查请求地址，并向平台支持确认接口是否可用 |
| `429` | 延迟后重试 |
| `5xx` | 提示暂时不可用，并限制重试次数 |

---

[← 模式 B 指南](../agent-development-upload.md) · [中文目录](../README.md) · [用户身份 →](users.md)
