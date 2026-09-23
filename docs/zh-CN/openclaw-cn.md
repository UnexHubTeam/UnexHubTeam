# openclaw-cn 接入教程

[English (primary)](../en/openclaw-cn.md) · [中文目录](README.md) · 简体中文（辅助翻译）

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

`openclaw-cn` 是 OpenClaw 的中文社区发行版。本页按 PoloAPI 的安装向导顺序配置 UNEXHub；它与 UNEXHub 自有的 UnexClaw 产品不是同一安装流程。

## 1）安装 Node.js

从 [Node.js 官网](https://nodejs.org/en/download)安装 Node.js 22.12.0 或以上版本。该最低版本来自核对时 npm 包的 `engines` 字段；将来升级时也应核对新包要求。

```bash
node --version
npm --version
```

## 2）安装 openclaw-cn

macOS / Linux：

```bash
npm install -g openclaw-cn@latest
openclaw-cn --version
```

Windows PowerShell：

```powershell
npm.cmd install -g openclaw-cn@latest
openclaw-cn.cmd --version
```

Windows 可使用 `.cmd` 入口，无需为本文修改整个用户的 PowerShell 执行策略。确认安装的是 [jiulingyun/openclaw-cn](https://github.com/jiulingyun/openclaw-cn)对应的社区包。

## 3）启动配置向导

```bash
openclaw-cn onboard
```

Windows 使用 `openclaw-cn.cmd onboard`。阅读向导说明并继续，选择「快速开始」。如果已有配置，先保留现有值，再编辑模型提供商。

## 4）添加自定义模型

依次选择「自定义模型 → 兼容接口 → OpenAI Compatible」，填写：

| 字段 | 内容 |
| --- | --- |
| 提供商名称 | `UNEXHub` |
| Base URL | `https://api.unexhub.ai/v1` |
| API Key | 专用 UNEXHub Key，例如 `openclaw-test`。 |
| 模型 ID | 当前可用且支持 Chat Completions、流式与工具调用的准确 ID。 |

如果版本区分 Chat Completions 与 Responses，选择前者。本页默认走已有站点示例支持的聊天协议；仅在 UNEXHub 确认 Messages 可用时，才选择 Anthropic Compatible，并使用服务提供的根地址。

## 5）选择默认模型并完成向导

选择刚添加的提供商和模型。首次验证可暂时跳过外部消息通道、额外技能和启动钩子。按空格选择、按 Enter 确认的操作以向导提示为准。

完成网关设置。希望后台常驻时可按社区文档使用 `openclaw-cn onboard --install-daemon`；首次测试使用下面的前台方式即可。

## 6）启动网关并打开控制界面

如果向导尚未启动网关，在新终端执行：

```bash
openclaw-cn gateway --port 18789 --verbose
```

若已有网关进程，不要重复启动。打开终端给出的 **HTTP 控制界面 URL**，按提示连接；不要把 `ws://` WebSocket 地址直接当作网页地址。带访问令牌的本地链接保存在自己设备中。

## 7）发送消息并核对费用

在对话页选择 UNEXHub 模型，发送「只回复一句问候，不执行其他操作」。需要连接飞书等平台时，在本地对话通过后，再按社区对应通道教程配置。

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

如果 OpenAI Compatible 文本测试成功而 Agent 工具调用失败，核对模型的工具调用能力与协议转换，不能仅凭有模型回复就确认全部 Agent 功能可用。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/8239615m0)
- [Community project](https://github.com/jiulingyun/openclaw-cn)
- [npm package metadata](https://registry.npmjs.org/openclaw-cn/latest)
