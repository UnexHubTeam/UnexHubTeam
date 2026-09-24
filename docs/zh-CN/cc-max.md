# CC MAX

<!-- DOCS-NAV:START -->
[English (primary)](../en/cc-max.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）取得专用渠道信息](#section-1)
2. [2）安装客户端并记录版本](#section-2)
3. [3）配置专用地址和密钥](#section-3)
4. [4）启动并验证](#section-4)
5. [5）核对扣费](#section-5)
6. [参考资料](#section-6)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

本页是 **CC MAX** 类 Claude Code 专用渠道的兼容性核对清单。它不是需要安装的新客户端，UNEXHub 是否提供同名产品或渠道尚未确认。

> UNEXHub 的同名渠道、专用地址及版本限制尚未核实。本页给出专用渠道开通后的接入流程；普通 Claude 接入直接使用 [Claude Code 教程](claude-code.md)。

<a id="section-1"></a>
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

不要把其他服务的客户端版本区间或客户端限制直接套用于 UNEXHub；仅采用 UNEXHub 针对当前渠道明确确认的要求。

<a id="section-2"></a>
## 2）安装客户端并记录版本

按 [Claude Code 安装教程](claude-code-install.md)安装 CLI，执行 `claude --version`。需要 VS Code 时按[官方扩展教程](vscode-claude-code.md)安装，并记录扩展版本。

仅在 UNEXHub 提供了明确兼容要求时，才按其要求选择对应客户端版本。

<a id="section-3"></a>
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

<a id="section-4"></a>
## 4）启动并验证

重新启动 CLI 或重新加载 VS Code。检查网关地址，发送一次简短问候。失败时记录 CLI／扩展版本、错误信息、模型和 Request ID，再核对专用渠道权限。

<a id="section-5"></a>
## 5）核对扣费

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

若专用服务使用不同环境，应在该服务指定的控制台查询记录。没有专用渠道信息时，仍可使用本套文档中的普通模型、第三方路由或 CC Switch 转换流程。

<a id="section-6"></a>
## 参考资料

- [Claude gateway configuration](https://code.claude.com/docs/en/llm-gateway-connect)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：CC Switch](cc-switch.md) · [中文目录](README.md) · [下一篇：openclaw-cn →](openclaw-cn.md)
<!-- DOCS-PAGER:END -->
