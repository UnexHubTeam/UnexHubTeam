# Aider

<!-- DOCS-NAV:START -->
[English (primary)](../en/aider.md) · [中文目录](README.md) · [公开 API 文档 ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1）安装 Aider](#section-1)
2. [2）设置 API 地址和密钥](#section-2)
3. [3）指定模型并启动](#section-3)
4. [4）可选：保存非敏感配置](#section-4)
5. [5）测试对话](#section-5)
6. [6）查看费用](#section-6)
7. [参考资料](#section-7)
</details>
<!-- DOCS-TOC:END -->


适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

Aider 是终端编程助手。它支持自定义 OpenAI 兼容接口，本页使用 UNEXHub 的 Chat Completions 地址。

<a id="section-1"></a>
## 1）安装 Aider

按照官方安装器方式，在已有 Python 的终端执行：

```bash
python -m pip install aider-install
aider-install
aider --version
```

macOS / Linux 若只有 `python3` 命令，将第一行改为 `python3 -m pip install aider-install`；Windows 使用 Python Launcher 时可执行 `py -m pip install aider-install`。官方安装器会为 Aider 创建独立环境。安装后找不到命令时重开终端并检查 Python scripts 目录是否在 PATH。

<a id="section-2"></a>
## 2）设置 API 地址和密钥

创建专用 UNEXHub Key，例如 `aider-test`。macOS / Linux：

```bash
export OPENAI_API_BASE='https://api.unexhub.ai/v1'
export OPENAI_API_KEY='YOUR_API_KEY'
```

Windows PowerShell：

```powershell
$env:OPENAI_API_BASE = "https://api.unexhub.ai/v1"
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

Aider 的配置名是 `OPENAI_API_BASE`。替换密钥占位符，地址写到 `/v1`。

<a id="section-3"></a>
## 3）指定模型并启动

进入测试项目目录，执行：

```bash
aider --model openai/YOUR_MODEL_ID
```

`openai/` 是 Aider／LiteLLM 的提供商前缀，后面才是 UNEXHub 的准确模型 ID。不要因为模型来自其他品牌就移除本教程所用的兼容提供商前缀。

<a id="section-4"></a>
## 4）可选：保存非敏感配置

在用户级 `~/.aider.conf.yml` 保存：

```yaml
model: openai/YOUR_MODEL_ID
openai-api-base: https://api.unexhub.ai/v1
```

Key 继续通过环境变量提供。配置文件中替换准确 ID，合并已有配置即可。Aider 不认识某模型时可能提示上下文或价格信息缺失，这不直接说明 API 不可用；费用按 UNEXHub 实际记录核对。

<a id="section-5"></a>
## 5）测试对话

在 Aider 交互界面输入：

```text
/ask Reply with one short greeting. Do not edit files.
```

收到回复后，再添加需要协作的文件并进入编辑工作流。辅助模型、提交消息生成或其他自动任务可能增加请求，检查当前配置中的模型选择。

<a id="section-6"></a>
## 6）查看费用

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

<a id="section-7"></a>
## 参考资料

- [Aider installation](https://aider.chat/docs/install.html)
- [OpenAI-compatible API configuration](https://aider.chat/docs/llms/openai-compat.html)

<!-- DOCS-PAGER:START -->

---

[← 上一篇：Windsurf](windsurf.md) · [中文目录](README.md) · [下一篇：安装 Claude Code →](claude-code-install.md)
<!-- DOCS-PAGER:END -->
