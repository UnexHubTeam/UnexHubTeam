# Windsurf

[English (primary)](../en/windsurf.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页保留截图中的 Windsurf 教程入口，并区分内置助手与集成终端接入。

> 核对时，Windsurf 的模型文档重定向到 Devin Desktop 文档，未确认任意 UNEXHub Base URL 的原生配置入口。Polo 页面中的通用 OpenAI 设置和环境变量方法不能据此认定适用于所有当前版本。

## 1）安装并打开编辑器

从 [Windsurf 官网](https://windsurf.com/)进入当前官方下载安装入口，打开测试项目。检查版本、模型设置和自带 Key（BYOK）选项。

## 2）判断是否提供自定义网关

只有当前版本明确支持「自定义 OpenAI 兼容地址」时，才填写下面的信息：

| 字段 | 内容 |
| --- | --- |
| API Key | 专用 UNEXHub Key，不加 `Bearer`。 |
| SDK Base URL | `https://api.unexhub.ai/v1` |
| Model ID | 当前可用、协议匹配的模型 ID。 |

若字段要求根地址或完整端点，应按其说明调整，并检查最终请求路径。不要照抄参考教程中的 `/vi`，正确版本路径是 `/v1`。

只有原厂 Key 输入框、没有自定义网关地址时，无法由该输入框完成 UNEXHub 接入。系统中的 `OPENAI_BASE_URL` 也不保证内置助手会读取。

## 3）使用集成终端接入 UNEXHub

需要在这个编辑器内使用 UNEXHub 时，可打开「Terminal → New Terminal」，按 [Aider 教程](aider.md)完成安装，然后配置：

macOS / Linux：

```bash
export OPENAI_API_BASE='https://api.unexhub.ai/v1'
export OPENAI_API_KEY='YOUR_API_KEY'
aider --model openai/YOUR_MODEL_ID
```

Windows PowerShell：

```powershell
$env:OPENAI_API_BASE = "https://api.unexhub.ai/v1"
$env:OPENAI_API_KEY = "YOUR_API_KEY"
aider --model openai/YOUR_MODEL_ID
```

替换模型与 Key。这条路径使用编辑器中的终端工具，不会把内置 Cascade／Devin 助手的配置改成 UNEXHub。

## 4）验证对话并查看费用

在 Aider 中输入 `/ask Reply with one short greeting. Do not edit files.`。如果你使用的是已支持自定义网关的原生设置，则在相应聊天面板发送同样的简短消息。

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

原生模型套餐和终端工具发出的 UNEXHub 请求分别计费。需要排查时记录编辑器版本、所走接入方式和错误信息。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/9103817m0)
- [Current model documentation](https://docs.devin.ai/desktop/models)
- [Aider compatible APIs](https://aider.chat/docs/llms/openai-compat.html)
