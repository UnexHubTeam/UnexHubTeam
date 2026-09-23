# CC MAX

[文档目录](README.md) · 简体中文 | [English](../en/cc-max.md)

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页对应 PoloAPI 目录中的 **CC MAX**。原页描述的是 Polo 的 Claude Code 专用中转渠道，不是需要安装的新客户端，也不是 UNEXHub 已确认存在的同名产品。

> UNEXHub 的同名渠道、专用地址及版本限制尚未核实。本页给出专用渠道开通后的接入流程；普通 Claude 接入直接使用 [Claude Code 教程](claude-code.md)。

## 1）取得专用渠道信息

在 UNEXHub 模型与路由说明中核对，必要时向 [support@unexhub.com](mailto:support@unexhub.com)取得：

| 信息 | 需要确认的内容 |
| --- | --- |
| Base URL | 专用网关的根地址，是否使用标准 API 域名或其他专用域名。 |
| Key 与路由 | 当前 UNEXHub Key 是否具备该渠道权限。 |
| 模型 ID | 可调用的准确 ID 与辅助模型映射。 |
| 协议 | Anthropic Messages、流式与工具调用支持。 |
| 客户端范围 | CLI、VS Code 扩展及其他客户端的支持情况。 |
| 版本与费用 | 推荐版本、渠道价格、预算限制和日志归属。 |

Polo 原文列出的特定客户端版本区间及“只支持指定客户端”限制，属于 Polo 渠道信息，不能作为 UNEXHub 的兼容结论。

## 2）安装客户端并记录版本

按 [Claude Code 安装教程](claude-code-install.md)安装 CLI，执行 `claude --version`。需要 VS Code 时按[官方扩展教程](vscode-claude-code.md)安装，并记录扩展版本。

仅在 UNEXHub 提供了明确兼容要求时，才按其要求选择对应客户端版本。

## 3）配置专用地址和密钥

将以下内容合并到用户级 `~/.claude/settings.json`，替换全部占位符：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "YOUR_CONFIRMED_CC_MAX_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "YOUR_CONFIRMED_CC_MAX_MODEL_ID"
  }
}
```

这里没有默认填入标准 API 地址，以免将未经确认的专用渠道当作已开放功能。若服务要求 `x-api-key`，将认证变量改为 `ANTHROPIC_API_KEY`。

## 4）启动并验证

重新启动 CLI 或重新加载 VS Code。检查网关地址，发送一次简短问候。失败时记录 CLI／扩展版本、错误信息、模型和 Request ID，再核对专用渠道权限。

## 5）核对扣费

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

若专用服务使用不同环境，应在该服务指定的控制台查询记录。没有专用渠道信息时，仍可使用本套文档中的普通模型、第三方路由或 CC Switch 转换流程。

## 参考资料

- [PoloAPI CC MAX channel reference](https://poloapi.apifox.cn/9111206m0)
- [Claude gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)
